#!/usr/bin/env python3
"""LEAD 1: the full face-corona enumeration of GET A, GET B and Inchbald's solid (C).
For each centre X in {A, B, C} (fixed at the identity): every set of face-to-face neighbours, taken from the complete list of
valid placements of A, B and C (neighbours.py: 588 / 784 / 196, all 120 images, exact), that covers each of the 30 faces of X
exactly once, no two neighbours overlapping each other (exact). Counted by kind (how many A, B and C neighbours), with the
lattice corona flagged; mixed coronas (a neighbour of another solid than X) listed.

Exactness.
 * Cell crossing (interiors meet) is the separating-axis test on the 15 normals, done in exact integer arithmetic on Z[phi]
   pairs (x + y phi has the sign of a + b sqrt5, a = 2x + y, b = y, decided by integer comparisons), vectorised with numpy
   int64. This is the same test as zsurf.Geo.relation, which is exact for two cells on these axes.
 * Overlap of two placed solids: no crossing pair of +1 cells -> no overlap (the -1 cell only removes volume); a crossing pair of
   two 'clean' +1 cells (cells that do not cross the solid's -1 cell, so they lie inside the solid) -> overlap; otherwise the exact
   intersection volume in Q(phi) (mixlib.pair_volume on every crossing cell pair, signs applied), overlap iff > 0.
 * The only floating point is a bounding-sphere prefilter with a 1e-6 margin (float error ~1e-12): pairs it drops cannot meet.
 * Exact cover: the coronas are far too many to list (the pilot found over 6 x 10^8 on a third of GET A's candidates), so they
   are COUNTED exactly, by kind, as a polynomial in the numbers of A, B and C neighbours: depth-first branching on the face with
   fewest candidates, splitting the rest into independent parts (candidates linked by conflict or a shared face) whose counts
   multiply, with a memo (the method of #SAT model counters). Parallel over the first two branchings. Python integers: no overflow.
Restart: conflict chunks, exact pair volumes and finished count branches are appended to data/corona-cache/ and reused.
Controls (all must pass for FINAL ok): the candidate counts equal neighbours.py's (588/784/196); exactly one all-lattice corona
for A and for B (the lattice corona); every inner corona of the four exact patches (patch-fibonacci, patch-abc, free-patch-AB,
free-patch-A2) is a conflict-free exact cover of the table, hence counted; a random sample of candidate pairs agrees with the
independent mixlib.overlaps; on small random sub-instances the counter, a plain enumeration and pysat (CaDiCaL) agree, by kind;
pysat on the full table agrees with the count on which sets of solids occur, and its witnesses (one corona per set) and four patch
coronas are re-verified with mixlib.overlaps.
Usage: corona_enum.py <k10 dir> <inchbald json> <out json> <centres, e.g. ABC> [--workers N] [--limit N] [--seed S] [--memo-max M]
  --limit N: pilot only, keep N candidates per centre (all those needed by the controls, plus random others)."""
import sys, os, json, time, random, hashlib, argparse
from collections import Counter
import multiprocessing as mp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

ap = argparse.ArgumentParser()
ap.add_argument('k10'); ap.add_argument('inch'); ap.add_argument('out'); ap.add_argument('centres')
ap.add_argument('--workers', type=int, default=max(1, os.cpu_count() - 2)); ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--memo-max', type=int, default=500_000)      # memo entries per worker before it is cleared (memory bound)
ARGS = ap.parse_args()
t0 = time.time()
STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(STUDY, 'data', 'corona-cache' + ('-pilot' if ARGS.limit else '')); os.makedirs(CACHE, exist_ok=True)
NAMES = 'ABC'; NCEN = len(ARGS.centres)
def el(): return f't={time.time() - t0:.0f}s'
def progress(frac, what): print(f'PROGRESS {min(max(frac, 0.0), 1.0):.4f} {what} {el()}', flush=True)

sol = load_solids(ARGS.k10, ARGS.inch)
EF = np.array([[zfloat(c) for c in e] for e in G.E])
for nm in NAMES:
    s = sol[nm]; s['neg'] = [c for c, sg in s['cells'] if sg < 0]
    s['clean'] = [sg > 0 and not any(G.relation(c[0], c[1], k[0], k[1]) == 'cross' for k in s['neg']) for c, sg in s['cells']]
PR = G.pairs
Dx = np.array([[G.D[(x, y, i)][0] for (x, y) in PR] for i in range(n)], dtype=np.int64)
Dy = np.array([[G.D[(x, y, i)][1] for (x, y) in PR] for i in range(n)], dtype=np.int64)
def sign_arr(x, y):
    a, b = 2*x + y, y
    s = np.where((a >= 0) & (b >= 0), np.where((a == 0) & (b == 0), 0, 1), 0)
    s = np.where((a <= 0) & (b <= 0) & ~((a == 0) & (b == 0)), -1, s)
    mixed = ((a > 0) & (b < 0)) | ((a < 0) & (b > 0))
    return np.where(mixed, np.where(a*a > 5*b*b, np.sign(a), np.sign(b)), s)
def intervals(cells):
    P = np.array([c[0] for c in cells], dtype=np.int64); bx, by = P @ Dx, P @ Dy
    lox, loy, hix, hiy = bx.copy(), by.copy(), bx.copy(), by.copy()
    for ci, c in enumerate(cells):
        for dd in c[1]:
            vx, vy = Dx[dd], Dy[dd]; pos = sign_arr(vx, vy) > 0
            hix[ci] += np.where(pos, vx, 0); hiy[ci] += np.where(pos, vy, 0)
            lox[ci] += np.where(pos, 0, vx); loy[ci] += np.where(pos, 0, vy)
    return lox, loy, hix, hiy
assert int(sign_arr(np.array([1]), np.array([-1]))[0]) < 0 and int(sign_arr(np.array([-1]), np.array([1]))[0]) > 0   # 1 - phi < 0

# ---------------- exact pair volumes, cached on disk ----------------
VOLF = os.path.join(CACHE, 'pairvol.jsonl'); VOL = {}
def kjson(k): return [[list(k[0][0]), list(k[0][1])], [list(k[1][0]), list(k[1][1])]]
def kload(j): return ((tuple(j[0][0]), tuple(j[0][1])), (tuple(j[1][0]), tuple(j[1][1])))
if os.path.exists(VOLF):
    for line in open(VOLF):
        try: k, a, b = json.loads(line)
        except Exception: continue          # a line cut by a kill
        VOL[kload(k)] = Q(Fr(a), Fr(b))
def vol_worker(k):
    v = pair_volume(*k); return k, str(v.a), str(v.b)
def ensure_volumes(keys, pool=None):
    miss = sorted({k for k in keys if k not in VOL})
    if not miss: return 0
    it = pool.imap_unordered(vol_worker, miss, chunksize=4) if pool else map(vol_worker, miss)
    with open(VOLF, 'a') as fh:
        for k, a, b in it:
            VOL[k] = Q(Fr(a), Fr(b)); fh.write(json.dumps([kjson(k), a, b]) + '\n')
    return len(miss)

# ---------------- the placed solids as arrays ----------------
K = max(len(sol[nm]['cells']) for nm in NAMES)
def arrays(placed):
    """placed: list of (name, cells). Returns exact interval arrays (N, K, 15), signs (N, K), clean (N, K)."""
    N = len(placed); A = [np.zeros((N, K, 15), np.int64) for _ in range(4)]; SG = np.zeros((N, K), np.int64); CL = np.zeros((N, K), bool)
    for i, (nm, cells) in enumerate(placed):
        iv = intervals([c for c, _ in cells]); k = len(cells)
        for a, v in zip(A, iv): a[i, :k] = v
        SG[i, :k] = [s for _, s in cells]; CL[i, :k] = sol[nm]['clean']
    return A, SG, CL
def cross_block(Ai, Aj):
    """Ai: 4 arrays (Ki, 15) of one solid; Aj: 4 arrays (J, Kj, 15). Exact cross[J, Ki, Kj]."""
    lox, loy, hix, hiy = Ai; LX, LY, HX, HY = Aj
    g1 = sign_arr(LX[:, None, :, :] - hix[None, :, None, :], LY[:, None, :, :] - hiy[None, :, None, :])
    g2 = sign_arr(lox[None, :, None, :] - HX[:, None, :, :], loy[None, :, None, :] - HY[:, None, :, :])
    return ~((g1 >= 0) | (g2 >= 0)).any(axis=3)
def classify(cr, sgi, sgj, cli, clj):
    """cr: (Ki, Kj) exact cell crossing. 0 = no overlap, 1 = overlap, 2 = needs the exact volume"""
    valid = (sgi[:, None] != 0) & (sgj[None, :] != 0); cr = cr & valid
    pos = cr & (sgi[:, None] > 0) & (sgj[None, :] > 0)
    if not pos.any(): return 0
    if (pos & cli[:, None] & clj[None, :]).any(): return 1
    return 2
def amb_terms(cells_i, cells_j, cr):
    """the crossing cell pairs of an ambiguous pair: [(normalised key, sign)]"""
    out = []
    for ci, cj in np.argwhere(cr):
        if ci >= len(cells_i) or cj >= len(cells_j): continue
        (a, sa), (b, sb) = cells_i[ci], cells_j[cj]
        out.append((norm_pair(a, b), sa*sb))
    return out
def decide(terms):
    v = ZERO
    for k, s in terms: v = v + (VOL[k] if s > 0 else -VOL[k])
    assert v.sign() >= 0, 'negative overlap volume'
    return v.sign() > 0

# ---------------- worker globals (set before each fork) ----------------
W = {}
def conf_worker(rows):
    """conflicts of rows i against all j > i (exact). Returns definite conflicts and ambiguous pairs with their cell terms."""
    ARR, SG, CL, CTR, RR, CELLS = W['ARR'], W['SG'], W['CL'], W['CTR'], W['RR'], W['CELLS']; N = len(SG)
    conf = []; amb = []
    for i in rows:
        js = np.arange(i + 1, N)
        js = js[np.linalg.norm(CTR[js] - CTR[i], axis=1) <= RR[js] + RR[i] + 1e-6]
        for b0 in range(0, len(js), 128):
            jb = js[b0:b0 + 128]
            cr = cross_block([a[i] for a in ARR], [a[jb] for a in ARR])
            for jj, j in enumerate(jb):
                c = classify(cr[jj], SG[i], SG[j], CL[i], CL[j])
                if c == 1: conf.append((int(i), int(j)))
                elif c == 2: amb.append((int(i), int(j), [(kjson(k), s) for k, s in amb_terms(CELLS[i], CELLS[j], cr[jj])]))
    return rows, conf, amb

def popc(x): return x.bit_count()
# ---- counting exact covers by kind: a polynomial {(nA, nB, nC): count}, with component splitting and a memo (as #SAT counters) ----
ONE = {(0, 0, 0): 1}
SHIFT = {'A': (1, 0, 0), 'B': (0, 1, 0), 'C': (0, 0, 1)}
def pmul(p, q):
    r = {}
    for ka, va in p.items():
        for kb, vb in q.items():
            k = (ka[0] + kb[0], ka[1] + kb[1], ka[2] + kb[2]); r[k] = r.get(k, 0) + va*vb
    return r
def bits(m):
    while m:
        low = m & -m; yield low.bit_length() - 1; m ^= low
class CoverCounter:
    """number of sets S of allowed candidates covering every face in `faces` exactly once with no two in conflict, by kind.
    BAN[i] = i itself, its conflicts, and every candidate sharing a face with it (a symmetric relation). After any choice the
    remaining problem splits into independent parts: candidates linked by BAN form the parts; the count is the product."""
    def __init__(s, COVER, FM, BAN, Y):
        s.COVER, s.FM, s.BAN, s.SH = COVER, FM, BAN, [SHIFT[y] for y in Y]; s.memo = {}; s.nodes = 0
    def count(s, faces, alw):
        if faces == 0: return ONE
        rel = 0
        for f in bits(faces):
            c = s.COVER[f] & alw
            if not c: return {}
            rel |= c
        key = (faces, rel)
        r = s.memo.get(key)
        if r is not None: return r
        s.nodes += 1
        comps = []; rem = rel
        while rem:
            i = (rem & -rem).bit_length() - 1; comp = 0; front = 1 << i
            while front:
                comp |= front; nb = 0
                for j in bits(front): nb |= s.BAN[j]
                front = nb & rem & ~comp
            rem &= ~comp; fm = 0
            for j in bits(comp): fm |= s.FM[j]
            comps.append((fm, comp))
        if len(comps) > 1 or comps[0][0] != faces:
            covered = 0
            for fm, _ in comps: covered |= fm
            if covered != faces: r = {}                       # a face no candidate can cover
            else:
                r = ONE
                for fm, cm in sorted(comps, key=lambda z: popc(z[1])):
                    r = pmul(r, s.count(fm, cm))
                    if not r: break
        else:
            best = None; bc = 1 << 30
            for f in bits(faces):
                c = popc(s.COVER[f] & rel)
                if c < bc: bc = c; best = s.COVER[f] & rel
            r = {}
            for i in bits(best):
                sub = s.count(faces & ~s.FM[i], rel & ~s.BAN[i]); sh = s.SH[i]
                for k, v in sub.items():
                    kk = (k[0] + sh[0], k[1] + sh[1], k[2] + sh[2]); r[kk] = r.get(kk, 0) + v
        s.memo[key] = r
        return r
def count_worker(task):
    tid, faces, alw, sh = task
    cc = W['CC']
    if len(cc.memo) > W['MEMO_MAX']: cc.memo.clear()
    sub = cc.count(faces, alw)
    return tid, [[[k[0] + sh[0], k[1] + sh[1], k[2] + sh[2]], v] for k, v in sub.items()], cc.nodes

def enumerate_covers(COVER, FM, BAN, N, cap):
    """plain depth-first enumeration (for cross-checks on small sub-instances); None if more than cap"""
    FULL = (1 << 30) - 1; out = []
    def rec(cov, alw, ch):
        if len(out) > cap: return
        if cov == FULL: out.append(tuple(sorted(ch))); return
        best = None; bc = 1 << 30
        for f in range(30):
            if cov >> f & 1: continue
            m = COVER[f] & alw; c = popc(m)
            if c < bc:
                bc = c; best = m
                if c == 0: return
        for i in bits(best): rec(cov | FM[i], alw & ~BAN[i], ch + [i])
    rec(0, (1 << N) - 1, [])
    return None if len(out) > cap else out
def build_tables(neigh, conf, sub=None):
    """bitset tables over the candidates `sub` (indices into neigh, renumbered 0..)"""
    idx = list(range(len(neigh))) if sub is None else list(sub); pos = {i: k for k, i in enumerate(idx)}; N = len(idx)
    COVER = [0]*30; FM = [0]*N
    for k, i in enumerate(idx):
        for f in neigh[i]['shared']: COVER[f] |= 1 << k; FM[k] |= 1 << f
    BAN = [(1 << k) for k in range(N)]
    for i, j in conf:
        if i in pos and j in pos: a, b = pos[i], pos[j]; BAN[a] |= 1 << b; BAN[b] |= 1 << a
    for f in range(30):
        for k in bits(COVER[f]): BAN[k] |= COVER[f]
    return idx, COVER, FM, BAN
def run_pool(fn, items, workers):
    ctx = mp.get_context('fork')
    with ctx.Pool(workers) as pool:
        for r in pool.imap_unordered(fn, items): yield r

# ---------------- the four exact patches: inner coronas (controls) ----------------
def patch_tiles():
    D = os.path.join(STUDY, 'data'); out = {}
    for nm in ('patch-fibonacci', 'patch-abc'):
        d = json.load(open(os.path.join(D, nm + '.json'))); out[nm] = [(T['Y'], T['g'], tuple(T['t'])) for T in d['tiles']]
    BL = np.array(sol['A']['basis'])
    SHAPE = {'A': ('A', IDENT, (0,)*6), 'B': ('B', IDENT, (0,)*6), "A'": ('A', 40, (0, 0, 0, 1, 1, 0))}   # as free_patch.py
    for nm in ('free-patch-AB', 'free-patch-A2'):
        d = json.load(open(os.path.join(D, nm + '.json'))); L = []
        for c, lab in d['assign'].items():
            c = tuple(int(x) for x in c.strip('()').split(',')); Yn, g, w = SHAPE[lab]
            L.append((Yn, g, tuple(int(x) for x in np.array(c) @ BL + np.array(w))))
        out[nm] = L
    return out
def patch_coronas(X, key2idx, SX):
    """for each patch tile of solid X with all 30 faces matched: its face neighbours, carried to the frame where the tile is X at
    the identity (faces translated by -t, then the inverse symmetry), as a sorted tuple of candidate indices."""
    res = {}; missing = 0; ntiles = 0
    for pname, tiles in patch_tiles().items():
        F = [tfaces(sol[Y]['faces'], g, t) for Y, g, t in tiles]; where = {}
        for i, Fi in enumerate(F):
            for f, s in Fi.items(): where.setdefault(f, []).append((i, s))
        for i, (Y, g, t) in enumerate(tiles):
            if Y != X or not all(len(where[f]) == 2 for f in F[i]): continue
            nbs = {j for f in F[i] for j, _ in where[f] if j != i}
            def rel(Fj): return apply_sym(G, {(tuple(a - b for a, b in zip(f[0], t)), f[1], f[2]): s for f, s in Fj.items()}, SYMS[INV[g]])
            assert rel(F[i]) == SX, 'frame change does not return the centre to the identity'
            idx = []
            for j in nbs:
                k = frozenset(rel(F[j]).items())
                if k not in key2idx: missing += 1; break
                idx.append(key2idx[k])
            else:
                ntiles += 1; res.setdefault(tuple(sorted(idx)), []).append(pname)
    return res, missing, ntiles

# ---------------- main ----------------
summary = {'centres': {}, 'args': vars(ARGS)}; allok = True; fails = []
for ci_, X in enumerate(ARGS.centres):
    base = ci_/NCEN; span = 1/NCEN
    SX = sol[X]['faces']; CX = sol[X]['cells']; SXs = sorted(SX.items())
    AX, SGX, CLX = arrays([(X, CX)]); AXi = [a[0] for a in AX]
    # 1. candidates (as neighbours.py)
    neigh = []; seenF = set(); nvol_c = 0
    for Y in NAMES:
        imgs = {}
        for gi in range(120): imgs.setdefault(canon_t(tfaces(sol[Y]['faces'], gi, (0,)*6)), gi)
        for gi in sorted(imgs.values()):
            F0 = tfaces(sol[Y]['faces'], gi, (0,)*6); byp = {}
            for f, s in F0.items(): byp.setdefault((f[1], f[2], s), f)
            for f, s in SX.items():
                g = byp[(f[1], f[2], -s)]; t = tuple(a - b for a, b in zip(f[0], g[0]))
                FY, CY = place(sol, Y, gi, t); key = frozenset(FY.items())
                if key in seenF: continue
                seenF.add(key)
                AY, SGY, CLY = arrays([(Y, CY)])
                cr = cross_block(AXi, [a for a in AY])[0]
                c = classify(cr, SGX[0], SGY[0], CLX[0], CLY[0])
                if c == 2:
                    terms = amb_terms(CX, CY, cr); nvol_c += ensure_volumes([k for k, _ in terms]); c = 1 if decide(terms) else 0
                if c == 1: continue
                shared = [i for i, (ff, ss) in enumerate(SXs) if FY.get(ff) == -ss]
                neigh.append({'Y': Y, 'g': gi, 't': list(t), 'shared': shared, 'faces': FY, 'cells': CY, 'key': key})
    ncount = {Y: sum(1 for m in neigh if m['Y'] == Y) for Y in NAMES}
    print(X, 'valid face neighbours:', ncount, 'new exact volumes', nvol_c, el(), flush=True)
    if ncount != {'A': 588, 'B': 784, 'C': 196}: allok = False; fails.append(f'{X}: neighbour counts {ncount} differ from neighbours.py')
    B = np.array(sol[X]['basis'])
    def in_lattice(t):
        s_, *_ = np.linalg.lstsq(B.T.astype(float), np.array(t, float), rcond=None)
        return bool((np.round(s_).astype(int) @ B == np.array(t)).all())
    for m in neigh:
        m['lattice'] = m['Y'] == X and m['key'] == frozenset(tfaces(SX, IDENT, m['t']).items()) and in_lattice(m['t'])
    key2idx = {m['key']: i for i, m in enumerate(neigh)}
    targets, tmiss, ttiles = patch_coronas(X, key2idx, SX)
    print(X, 'patch control: inner tiles', ttiles, 'distinct inner coronas', len(targets), 'neighbours missing from the candidates', tmiss, flush=True)
    if tmiss: allok = False; fails.append(f'{X}: {tmiss} patch neighbours not among the candidates')
    if ARGS.limit and len(neigh) > ARGS.limit:          # pilot: keep the lattice and patch neighbours, then random others
        keep = {i for i, m in enumerate(neigh) if m['lattice']} | {i for t in targets for i in t}
        rest = [i for i in range(len(neigh)) if i not in keep]; random.Random(ARGS.seed).shuffle(rest)
        keep = sorted(keep | set(rest[:max(0, ARGS.limit - len(keep))]))
        old = {i: k for k, i in enumerate(keep)}; neigh = [neigh[i] for i in keep]
        targets = {tuple(sorted(old[i] for i in t)): v for t, v in targets.items()}
        key2idx = {m['key']: i for i, m in enumerate(neigh)}
        print(X, 'PILOT: candidates limited to', len(neigh), flush=True)
    N = len(neigh)
    fp = hashlib.sha256(json.dumps([[m['Y'], m['g'], m['t']] for m in neigh]).encode()).hexdigest()[:16]
    for m in neigh:
        P = np.array([np.array(v, float) @ EF for f in m['faces'] for v in corners(f, 6)]); m['c'] = P.mean(0); m['R'] = float(np.linalg.norm(P - m['c'], axis=1).max())
    # 2. pairwise conflicts (exact), in chunks, cached
    ARR, SG, CL = arrays([(m['Y'], m['cells']) for m in neigh])
    W.clear(); W.update(ARR=ARR, SG=SG, CL=CL, CTR=np.array([m['c'] for m in neigh]), RR=np.array([m['R'] for m in neigh]), CELLS=[m['cells'] for m in neigh])
    CF = os.path.join(CACHE, f'conf-{X}-{fp}.jsonl'); done = {};
    if os.path.exists(CF):
        for line in open(CF):
            try: r = json.loads(line)
            except Exception: continue
            done[r['chunk']] = r
    order = list(range(N)); CH = 8
    chunks = [order[k::(N + CH - 1)//CH] for k in range((N + CH - 1)//CH)]   # interleaved rows: even work per chunk
    todo = [(k, ch) for k, ch in enumerate(chunks) if k not in done]
    print(X, f'conflict chunks: {len(chunks)} ({len(done)} cached)', flush=True)
    if todo:
        with open(CF, 'a') as fh:
            nd = len(done)
            for rows, conf, amb in run_pool(conf_worker, [ch for _, ch in todo], ARGS.workers):
                k = chunks.index(rows); r = {'chunk': k, 'conf': conf, 'amb': amb}; fh.write(json.dumps(r) + '\n'); fh.flush(); done[k] = r; nd += 1
                if nd % 10 == 0 or nd == len(chunks): progress(base + span*0.5*nd/len(chunks), f'{X} conflict chunks {nd}/{len(chunks)}')
    conf = [tuple(p) for r in done.values() for p in r['conf']]
    amb = [(i, j, [(kload(k), s) for k, s in terms]) for r in done.values() for i, j, terms in r['amb']]
    progress(base + span*0.5, f'{X} conflicts: {len(conf)} definite, {len(amb)} need exact volumes')
    allkeys = {k for _, _, terms in amb for k, _ in terms}
    print(X, 'distinct cell-pair volumes needed', len(allkeys), 'cached', sum(1 for k in allkeys if k in VOL), flush=True)
    ctx = mp.get_context('fork')
    with ctx.Pool(ARGS.workers) as pool: nv = ensure_volumes(allkeys, pool)
    namb = 0
    for i, j, terms in amb:
        if decide(terms): conf.append((i, j)); namb += 1
    conf = sorted(set(conf))
    print(X, 'neighbour pairs in conflict:', len(conf), 'of', N*(N - 1)//2, f'(by exact volume: {namb} of {len(amb)}; new volumes {nv})', el(), flush=True)
    progress(base + span*0.6, f'{X} conflict table complete')
    # 2b. control: a sample of pairs against the independent mixlib.overlaps
    rng = random.Random(ARGS.seed + ci_); cset = set(conf)
    near = [(i, j) for i, j, _ in amb]; rng.shuffle(near)
    samp = near[:100] + [tuple(sorted(rng.sample(range(N), 2))) for _ in range(150)] + rng.sample(conf, min(50, len(conf)))
    bad = sum(1 for i, j in samp if overlaps(neigh[i]['cells'], neigh[j]['cells']) != ((i, j) in cset))
    print(X, 'sample control vs mixlib.overlaps:', len(samp), 'pairs, disagreements', bad, el(), flush=True)
    if bad: allok = False; fails.append(f'{X}: {bad} conflict decisions disagree with mixlib.overlaps')
    # 3. count the exact covers by kind (component-splitting counter, parallel over the first two branchings)
    FULL = (1 << 30) - 1
    _, COVER, FM, BAN = build_tables(neigh, conf)
    Yl = [m['Y'] for m in neigh]; LAT = [m['lattice'] for m in neigh]
    def kindof(t): return tuple(sum(1 for i in t if Yl[i] == c) for c in 'ABC')
    # control: every patch inner corona is a conflict-free exact cover in the table, so it is among those counted
    tbad = 0
    for t in targets:
        cov = Counter(f for i in t for f in neigh[i]['shared'])
        if sorted(cov) != list(range(30)) or any(v != 1 for v in cov.values()) or any(BAN[i] >> j & 1 for a, i in enumerate(t) for j in t[a + 1:]): tbad += 1
    print(X, 'patch inner coronas that are valid coronas of the table:', len(targets) - tbad, 'of', len(targets), flush=True)
    if tbad: allok = False; fails.append(f'{X}: {tbad} patch inner coronas rejected by the table')
    # control: the counter against plain enumeration and pysat on small random sub-instances
    rng = random.Random(ARGS.seed + 7 + ci_); xchk = 0; xbad = 0
    must = sorted({i for i, m in enumerate(neigh) if m['lattice']})
    for size in (60, 80, 100, 120, 140, 160, 200, 240):
        sub = sorted(set(must) | set(rng.sample(range(N), min(N, size))))
        idx, C2, F2, B2 = build_tables(neigh, conf, sub)
        sols = enumerate_covers(C2, F2, B2, len(idx), 300_000)
        if sols is None: continue
        pc = CoverCounter(C2, F2, B2, [Yl[i] for i in idx]).count(FULL, (1 << len(idx)) - 1)
        ek = Counter(kindof([idx[k] for k in t]) for t in sols)
        cl = []; top = len(idx)
        for f in range(30):
            enc = CardEnc.equals(lits=[k + 1 for k in bits(C2[f])], bound=1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv); cl += enc.clauses
        cl += [[-(a + 1), -(b + 1)] for a in range(len(idx)) for b in bits(B2[a]) if b > a and not any((F2[a] >> f & 1) and (F2[b] >> f & 1) for f in range(30))]
        ps = 0
        with Cadical153(bootstrap_with=cl) as S:
            while S.solve() and ps <= len(sols):
                mdl = S.get_model(); ch = [k for k in range(len(idx)) if mdl[k] > 0]; ps += 1; S.add_clause([-(k + 1) for k in ch])
        ok_ = dict(ek) == {k: v for k, v in pc.items() if v} and ps == len(sols); xchk += 1; xbad += not ok_
        print(X, f'   cross-check on {len(idx)} candidates: enumeration {len(sols)}, counter {sum(pc.values())}, pysat {ps}, agree {ok_}', flush=True)
    if xchk < 3 or xbad: allok = False; fails.append(f'{X}: counter cross-checks {xchk} run, {xbad} disagree')
    progress(base + span*0.62, f'{X} counter cross-checks done')
    # the full count
    CC = CoverCounter(COVER, FM, BAN, Yl)
    W.clear(); W.update(CC=CC, MEMO_MAX=ARGS.memo_max)
    states = [(0, (1 << N) - 1, (0, 0, 0), ())]; direct = Counter()
    for depth in range(2):
        nxt = []
        for cov, alw, sh, ch in states:
            faces = FULL & ~cov; best = None; bc = 1 << 30
            for f in bits(faces):
                c = popc(COVER[f] & alw)
                if c < bc: bc = c; best = COVER[f] & alw
            for i in bits(best):
                s2 = tuple(a + b for a, b in zip(sh, SHIFT[Yl[i]]))
                if cov | FM[i] == FULL: direct[s2] += 1
                else: nxt.append((cov | FM[i], alw & ~BAN[i], s2, ch + (i,)))
        states = nxt
    tasks = [(json.dumps(list(ch)), FULL & ~cov, alw, sh) for cov, alw, sh, ch in states]
    DF = os.path.join(CACHE, f'count-{X}-{fp}.jsonl'); ddone = {}
    if os.path.exists(DF):
        for line in open(DF):
            try: r = json.loads(line)
            except Exception: continue
            ddone[r['tid']] = r
    todo = [t for t in tasks if t[0] not in ddone]
    print(X, f'count tasks {len(tasks)} ({len(tasks) - len(todo)} cached)', el(), flush=True)
    with open(DF, 'a') as fh:
        nd = len(tasks) - len(todo); last = time.time()
        for tid, poly, nodes in run_pool(count_worker, todo, ARGS.workers):
            r = {'tid': tid, 'poly': poly}; fh.write(json.dumps(r) + '\n'); fh.flush(); ddone[tid] = r; nd += 1
            if time.time() - last > 60 or nd == len(tasks):
                last = time.time(); progress(base + span*(0.62 + 0.3*nd/max(1, len(tasks))), f'{X} count tasks {nd}/{len(tasks)}')
    poly = Counter(direct)
    for t in tasks:
        for k, v in ddone[t[0]]['poly']: poly[tuple(k)] += v
    poly = {k: v for k, v in poly.items() if v}
    total = sum(poly.values())
    lat_poly = CoverCounter(COVER, FM, BAN, Yl).count(FULL, sum(1 << i for i in must))
    nlat = sum(lat_poly.values())
    xi = 'ABC'.index(X); nmixed = sum(v for k, v in poly.items() if sum(k) != k[xi])
    bysets = Counter()
    for k, v in poly.items(): bysets[''.join(c for c, x in zip('ABC', k) if x)] += v
    print(X, 'face coronas:', total, '| mixed:', nmixed, '| all-lattice:', nlat, el(), flush=True)
    for k, v in sorted(poly.items(), key=lambda z: -z[1])[:40]: print('   ', X, f'A{k[0]} B{k[1]} C{k[2]}', 'count', v)
    print(X, 'coronas by the set of neighbour solids:', dict(sorted(bysets.items())), flush=True)
    if X in 'AB' and nlat != 1: allok = False; fails.append(f'{X}: {nlat} all-lattice coronas (expected exactly 1)')
    progress(base + span*0.93, f'{X} count complete')
    # 4. pysat on the full table: which sets of neighbour solids occur (with a witness each); must agree with the count
    clauses = []; top = N
    for f in range(30):
        enc = CardEnc.equals(lits=[i + 1 for i in bits(COVER[f])], bound=1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv); clauses += enc.clauses
    clauses += [[-(i + 1), -(j + 1)] for i, j in conf]
    sat_sets = {}; exm = {}
    for sset in ('A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC'):
        cl = list(clauses)
        for c in 'ABC':
            ids = [i + 1 for i in range(N) if Yl[i] == c]
            if c in sset: cl.append(ids)
            else: cl += [[-i] for i in ids]
        with Cadical153(bootstrap_with=cl) as S:
            sat_sets[sset] = S.solve()
            if sat_sets[sset]: mdl = S.get_model(); exm[sset] = tuple(i for i in range(N) if mdl[i] > 0)
    agree = all(sat_sets[s] == (bysets.get(s, 0) > 0) for s in sat_sets)
    print(X, 'pysat: solid sets with a corona', sat_sets, 'agrees with the count:', agree, flush=True)
    if not agree: allok = False; fails.append(f'{X}: pysat and the count disagree on solid sets')
    # 5. witnesses and patch coronas re-verified with mixlib.overlaps (independent code path)
    pick = list(exm.values()) + list(targets)[:4]; vbad = 0
    for t in pick:
        cov = Counter(f for i in t for f in neigh[i]['shared'])
        if sorted(cov) != list(range(30)) or any(v != 1 for v in cov.values()): vbad += 1; continue
        if any(overlaps(neigh[i]['cells'], neigh[j]['cells']) for a, i in enumerate(t) for j in t[a + 1:]): vbad += 1; continue
        if any(overlaps(CX, neigh[i]['cells']) for i in t): vbad += 1
    print(X, 'coronas re-verified with mixlib.overlaps:', len(pick), 'failures', vbad, el(), flush=True)
    if vbad: allok = False; fails.append(f'{X}: {vbad} coronas fail the independent check')
    def tile(i): m = neigh[i]; return [m['Y'], m['g'], m['t']]
    summary['centres'][X] = {
        'n_candidates': N, 'candidate_counts': ncount, 'pilot_limited': bool(ARGS.limit),
        'n_conflicts': len(conf), 'n_exact_volume_pairs': len(amb), 'n_coronas': str(total), 'n_mixed': str(nmixed), 'n_all_lattice': nlat,
        'kinds': [[list(k), str(v)] for k, v in sorted(poly.items(), key=lambda z: -z[1])],
        'by_solid_set': {k: str(v) for k, v in bysets.items()}, 'pysat_solid_sets': sat_sets,
        'patch_coronas': len(targets), 'patch_coronas_valid': len(targets) - tbad,
        'examples_by_solid_set': {k: [tile(i) for i in t] for k, t in exm.items()},
        'neighbours': [{'Y': m['Y'], 'g': m['g'], 't': m['t'], 'shared': m['shared'], 'lattice': m['lattice']} for m in neigh],
        'conflicts': conf, 'candidates_fingerprint': fp}
    json.dump(summary, open(ARGS.out, 'w'))
    progress(base + span, f'{X} done')
summary['fails'] = fails; summary['ok'] = allok
json.dump(summary, open(ARGS.out, 'w'))
print('total', el())
print('FINAL ok' if allok else 'FINAL FAIL ' + '; '.join(fails))
