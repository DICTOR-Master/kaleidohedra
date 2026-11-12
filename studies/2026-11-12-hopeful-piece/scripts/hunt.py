# hunt.py, 12 Nov 2026 (aim 3, DICTO: "put more work on dbb aim 3"; keying PAUSED "until another hopeful piece comes to us").
# The hunt for a new hopeful piece: ONE piece whose shape alone (bumps and dents, no colour labels) admits no periodic filling.
#
# Families (README "Plan"):
#   K  keyed RD: one rhombic dodecahedron, on each rhombic face tiny square pyramids at the 4 points of one generic orbit of the
#      rhombus's symmetries (keyed_rd.py's first orbit, (u, v) = (3/10, 1/7)); a height field H on the 48 points (bump > 0, dent < 0).
#      By the registration theorem (rd-bridge README) every tiling by congruent copies sits on one fcc lattice, face to face; mirror
#      images are allowed here (congruent copies, as Chair44 allows), so every site takes one of the 48 orientations of O_h, and two
#      neighbours fit iff at every point a bump meets a dent of the same size (h + h' = 0). The 48 points form one free O_h orbit,
#      so a piece with symmetry group G is a G-invariant function on the 48 points (48/|G| free heights).
#   P  poly-RD: n face-joined RDs, no keys (shape alone), all free polyforms up to n = NMAX.
# Kill test per candidate: (1) arc consistency of the 48 orientations (none left = untileable); (2) index 1 (one orientation
#   repeated); (3) SAT (pysat Cadical153) on every fcc torus of index <= IMAX, one torus per O_h-orbit of sublattices (the tile set is
#   closed under O_h, so congruent tori give the same answer); (4) the ball of radius R round a site (UNSAT = untileable).
#   Verdicts: "killed k" (periodic, torus index k), "untileable R" / "untileable AC", "SURVIVOR" (no torus up to IMAX and fills R = RMAX).
# Controls (mode control): plain RD periodic at 1; all-bump RD untileable; marked-RD sets from the RD bridge through the same engine
#   (CELL+EPART periodic at 4; CELLFRAME no torus <= 16 as in job rd-cut16s; FRAME+EFR, certified aperiodic, no torus);
#   P: single RD periodic at 1, the cuboctahedral shell of 12 RDs (hole inside) untileable.
# Credit: any Chair44 mechanism is Tsiokos's (arXiv 2609.19214); the marked-RD control data use Kamenetsky's frames (vendor, MIT).
# usage: hunt.py control <rules.json> IMAX
#        hunt.py K <family spec> IMAX RMAX SHARD/NSHARDS out.json        family spec: classes:<orders>:<alphabet> | rand:<orders>:<alph>:<N>:<seed> | pair:<alph>:<N>:<seed>
#        hunt.py P NMAX IMAXP RMAX SHARD/NSHARDS out.json
import sys, os, json, itertools, time, random
import numpy as np
from fractions import Fraction as Q
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
T0 = time.time()
def log(*a): print(*a, f'({time.time() - T0:.0f}s)', flush=True)
# ---------------------------------------------------------------- O_h
NB = [d for d in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, d)) == 2]; assert len(NB) == 12
NBI = {d: i for i, d in enumerate(NB)}; NEG = [NBI[tuple(-x for x in d)] for d in NB]
OH = [tuple(tuple(s[i] if j == p[i] else 0 for j in range(3)) for i in range(3)) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
IDG = OH.index(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
DET = [round(np.linalg.det(np.array(M))) for M in OH]; ROTS = [g for g in range(48) if DET[g] == 1]; assert len(ROTS) == 24
OHI = {M: i for i, M in enumerate(OH)}
def app(M, x): return tuple(sum(M[i][j] * x[j] for j in range(3)) for i in range(3))
def mul(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
MUL = np.array([[OHI[mul(A, B)] for B in OH] for A in OH]); INVG = [OHI[tuple(zip(*M))] for M in OH]
GD = np.array([[NBI[app(M, d)] for d in NB] for M in OH])           # GD[g, d] = index of g.d
# ---------------------------------------------------------------- key points on the faces
def face_frame(e):
    nz = [i for i in range(3) if e[i] != 0]; z = next(i for i in range(3) if e[i] == 0)
    c1 = [0, 0, 0]; c1[nz[0]] = e[nz[0]]; c2 = [0, 0, 0]; c2[nz[1]] = e[nz[1]]
    return tuple(Q(e[i], 2) for i in range(3)), tuple(Q(c1[i] - c2[i], 2) for i in range(3)), tuple(Q(1 if i == z else 0) for i in range(3))
U0, V0 = Q(3, 10), Q(1, 7)
POS, FACE = [], []
for fi, e in enumerate(NB):
    C, U, V = face_frame(e)
    for a, b in [(s * U0, t * V0) for s in (1, -1) for t in (1, -1)]:
        assert abs(a) + 2 * abs(b) < 1                                 # inside the rhombus
        POS.append(tuple(C[i] + a * U[i] + b * V[i] for i in range(3))); FACE.append(fi)
PIDX = {p: k for k, p in enumerate(POS)}
ACT = np.array([[PIDX[app(M, p)] for p in POS] for M in OH])        # g . point k = point ACT[g, k]
assert all(sorted(r) == list(range(48)) for r in ACT.tolist())
assert all((ACT[g] != np.arange(48)).all() for g in range(48) if g != IDG)   # free action: the 48 points are one regular O_h orbit
ACTINV = np.array([ACT[INVG[g]] for g in range(48)])
MATCH = []                                                          # per direction d: 4 pairs (point on face d, point of the neighbour at d)
for di, d in enumerate(NB):
    pr = []
    for k, p in enumerate(POS):
        if FACE[k] != di: continue
        q = tuple(p[i] - d[i] for i in range(3)); pr.append((k, PIDX[q]))
    assert len(pr) == 4 and all(FACE[q] == NEG[di] for _, q in pr); MATCH.append(pr)
MA = np.array([[k for k, _ in pr] for pr in MATCH]); MB = np.array([[q for _, q in pr] for pr in MATCH])
def fit_table(H):
    """F[g, d, h]: piece in orientation g at x and piece in orientation h at x + NB[d] meet flush. Oriented field H_g[m] = H[ACTINV[g, m]]."""
    HG = H[ACTINV]                                                    # (48 orientations, 48 world points)
    F = np.empty((48, 12, 48), bool)
    for d in range(12):
        A = HG[:, MA[d]]; B = HG[:, MB[d]]
        F[:, d, :] = (A[:, None, :] + B[None, :, :] == 0).all(-1)
    return F
def canon(H):
    HG = H[ACTINV]; allv = np.concatenate([HG, -HG]) + 8
    return min(r.astype(np.uint8).tobytes() for r in allv)
# ---------------------------------------------------------------- generic engine on a state set with fit table F (S, 12, S)
def arc(F):
    v = np.ones(F.shape[0], bool)
    while True:
        ok = np.ones_like(v)
        for d in range(12): ok &= (F[:, d, :] & v[None, :]).any(1)
        nv = v & ok
        if (nv == v).all(): return v
        v = nv
def index1(F, st): return any(all(F[s, d, s] for d in range(12)) for s in st)
B3 = np.array([(1, 1, 0), (1, 0, 1), (0, 1, 1)]); B3I = np.linalg.inv(B3)
def hnf(rows):
    M = [list(map(int, r)) for r in rows]
    for col, last in ((2, 2), (1, 1), (0, 0)):
        while True:
            nz = [r for r in range(last + 1) if M[r][col] != 0]
            p = min(nz, key=lambda r: abs(M[r][col])); M[p], M[last] = M[last], M[p]
            done = True
            for r in range(last):
                q = M[r][col] // M[last][col]; M[r] = [a - q * b for a, b in zip(M[r], M[last])]
                if M[r][col] != 0: done = False
            if done: break
        if M[last][col] < 0: M[last] = [-a for a in M[last]]
    a, d = M[0][0], M[1][1]
    M[1] = [x - (M[1][0] // a) * y for x, y in zip(M[1], M[0])]
    M[2] = [x - (M[2][1] // d) * y for x, y in zip(M[2], M[1])]
    M[2] = [x - (M[2][0] // a) * y for x, y in zip(M[2], M[0])]
    return tuple(map(tuple, M))
def sublattices(imax, mult=1):
    out = []
    for n in range(1, imax + 1):
        if n % mult: continue
        for a in range(1, n + 1):
            if n % a: continue
            for d in range(1, n // a + 1):
                if (n // a) % d: continue
                f = n // a // d
                for b in range(a):
                    for c_ in range(a):
                        for e in range(d): out.append((n, ((a, 0, 0), (b, d, 0), (c_, e, f))))
    return out
def torus_orbits(imax, group, mult=1):
    """one representative per orbit of sublattices of the fcc lattice (index <= imax) under the point group"""
    allt = sublattices(imax, mult); keys = {M for _, M in allt}; reps = {}
    for n, M in allt:
        W = np.array(M) @ B3                                               # world generators (rows)
        best = None
        for g in group:
            img = np.rint((W @ np.array(OH[g]).T) @ B3I).astype(int)
            k = hnf(img.tolist()); assert k in keys, (M, k)
            if best is None or k < best: best = k
        reps.setdefault(best, [n, 0]); reps[best][1] += 1
    assert sum(c for _, c in reps.values()) == len(allt)
    return sorted(((n, M, c) for M, (n, c) in reps.items()), key=lambda t: (t[0], t[1])), len(allt)
def torus_nbr(M):
    W = np.array(M) @ B3; G = W.T.astype(float); Gi = np.linalg.inv(G)
    def red(v):
        f = Gi @ np.array(v, float); f = f - np.floor(f + 1e-9); return tuple(np.round(f, 6))
    x0 = (0, 0, 0); reps = {red(x0): x0}; todo = [x0]
    while todo:
        x = todo.pop()
        for d in NB:
            y = tuple(a + b for a, b in zip(x, d)); k = red(y)
            if k not in reps: reps[k] = y; todo.append(y)
    S = list(reps.values()); idx = {red(x): i for i, x in enumerate(S)}
    n = round(abs(np.linalg.det(G)) / 2); assert len(S) == n, (len(S), n)
    return np.array([[idx[red(tuple(a + b for a, b in zip(x, d)))] for d in NB] for x in S])
def ball(R):
    S = {(0, 0, 0): 0}; fr = [(0, 0, 0)]
    for _ in range(R):
        nf = []
        for x in fr:
            for d in NB:
                y = tuple(a + b for a, b in zip(x, d))
                if y not in S: S[y] = len(S); nf.append(y)
        fr = nf
    return [[S.get(tuple(a + b for a, b in zip(x, d)), -1) for d in NB] for x in S]
def sat_fill(F, st, nbr):
    """sites with neighbour table nbr (-1 = outside); every site one state from st; neighbours fit"""
    m = len(st); n = len(nbr); var = lambda i, a: 1 + i * m + a
    Fs = F[np.ix_(st, range(12), st)]; succ = [[(np.nonzero(Fs[a, d])[0] + 1).tolist() for d in range(12)] for a in range(m)]
    s = Cadical153(); top = n * m
    for i in range(n):
        lits = [var(i, a) for a in range(m)]; s.add_clause(lits)
        if m > 1:
            enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
            for cl in enc.clauses: s.add_clause(cl)
    for i in range(n):
        for d in range(12):
            j = nbr[i][d]
            if j < 0: continue
            o = j * m
            for a in range(m): s.add_clause([-var(i, a)] + [o + b for b in succ[a][d]])
    r = s.solve(); s.delete(); return r
TCACHE = {}
def tori(imax, group, mult=1):
    k = (imax, tuple(group), mult)
    if k not in TCACHE:
        reps, tot = torus_orbits(imax, group, mult); TCACHE[k] = ([(n, M, c, torus_nbr(M).tolist()) for n, M, c in reps], tot)
    return TCACHE[k]
BALLS = {R: ball(R) for R in (1, 2, 3, 4)}
def judge(F, imax, rmax, group):
    v = arc(F); st = np.nonzero(v)[0].tolist()
    if not st: return 'untileable AC'
    if index1(F, st): return 'killed 1'
    reps, _ = tori(imax, group)
    for n, M, c, nbr in reps:
        if n == 1: continue
        if n == 5 and not sat_fill(F, st, BALLS[2]): return 'untileable R2'
        if sat_fill(F, st, nbr): return f'killed {n}'
    for R in range(2, rmax + 1):
        if not sat_fill(F, st, BALLS[R]): return f'untileable R{R}'
    return 'SURVIVOR'
# ---------------------------------------------------------------- subgroups of O_h
def closure(gens):
    S = {IDG}; fr = [IDG]
    while fr:
        a = fr.pop()
        for b in gens:
            c = int(MUL[a, b])
            if c not in S: S.add(c); fr.append(c)
    return frozenset(S)
def subgroups():
    S2 = {closure([a, b]) for a in range(48) for b in range(a, 48)}
    S3 = {closure(sorted(H) + [c]) for H in S2 for c in range(48)}
    allS = S2 | S3; assert len(allS) == 98, len(allS)
    cls = {}
    for H in allS:
        key = min(tuple(sorted(int(MUL[MUL[g, h], INVG[g]]) for h in H)) for g in range(48))
        cls.setdefault(key, H)
    assert len(cls) == 33, len(cls)
    return sorted(cls.values(), key=lambda H: (-len(H), sorted(H)))
def orbits_on_points(G):
    seen = [-1] * 48; orb = []
    for k in range(48):
        if seen[k] >= 0: continue
        o = sorted({int(ACT[g, k]) for g in G})
        for x in o: seen[x] = len(orb)
        orb.append(o)
    return orb
def gname(G):
    ords = sorted(len(closure([g])) for g in G); dets = sum(DET[g] == -1 for g in G)
    return f'|G|={len(G)} improper={dets} orders={"".join(map(str, ords))}'
# ---------------------------------------------------------------- polyforms
def norm(cells):
    m = min(cells); return tuple(sorted(tuple(a - b for a, b in zip(c, m)) for c in cells))
def free_canon(cells): return min(norm([app(OH[g], c) for c in cells]) for g in range(48))
def polyforms(nmax):
    levels = {1: {((0, 0, 0),)}}
    for n in range(2, nmax + 1):
        nxt = set()
        for P in levels[n - 1]:
            Ps = set(P)
            for c in P:
                for d in NB:
                    y = tuple(a + b for a, b in zip(c, d))
                    if y not in Ps: nxt.add(free_canon(list(P) + [y]))
        levels[n] = nxt
    return levels
def poly_sat(P, anchors, need, red):
    """exact cover by the 48 images of P: placements with some cell on an anchor; cells mapped by red (torus) or kept (ball);
    every site in need covered exactly once, no site covered twice, no placement covering one site twice"""
    imgs = {norm([app(OH[g], c) for c in P]) for g in range(48)}; pl = set()
    for I in imgs:
        for x in anchors:
            for c0 in I:
                cells = tuple(red(tuple(a + b - e for a, b, e in zip(x, c, c0))) for c in I)
                if len(set(cells)) == len(cells): pl.add(tuple(sorted(cells)))
    pl = sorted(pl); cover = {}
    for p, cells in enumerate(pl):
        for cc in cells: cover.setdefault(cc, []).append(p + 1)
    s = Cadical153(); top = len(pl)
    for x in need:
        if not cover.get(x): s.delete(); return False
        s.add_clause(cover[x])
    for cc, lits in cover.items():
        if len(lits) > 1:
            enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
            for cl in enc.clauses: s.add_clause(cl)
    r = s.solve(); s.delete(); return r
def poly_judge(P, imaxp, rmax):
    n = len(P); reps, _ = tori(min(imaxp, 8 * n) if n > 1 else 1, list(range(48)), n)
    for N, M, c, nbr in reps:
        W = np.array(M) @ B3; Gi = np.linalg.inv(W.T.astype(float))
        def red(v, Gi=Gi, W=W):
            f = Gi @ np.array(v, float); f = f - np.floor(f + 1e-9); return tuple(np.rint(f @ W).astype(int).tolist())
        S = sorted({red(x) for x in torus_points(M)}); assert len(S) == N
        if poly_sat(P, S, S, red): return f'killed {N}'
    for R in range(1, rmax + 1):
        bx = ball_xyz(R)
        if not poly_sat(P, bx, bx, lambda y: y): return f'untileable R{R}'
    return 'SURVIVOR'
def torus_points(M):
    W = np.array(M) @ B3; G = W.T.astype(float); Gi = np.linalg.inv(G); seen = {}; todo = [(0, 0, 0)]
    def key(v):
        f = Gi @ np.array(v, float); f = f - np.floor(f + 1e-9); return tuple(np.round(f, 6))
    seen[key((0, 0, 0))] = (0, 0, 0)
    while todo:
        x = todo.pop()
        for d in NB:
            y = tuple(a + b for a, b in zip(x, d)); k = key(y)
            if k not in seen: seen[k] = y; todo.append(y)
    return list(seen.values())
def ball_xyz(R):
    S = {(0, 0, 0)}; fr = [(0, 0, 0)]
    for _ in range(R):
        nf = []
        for x in fr:
            for d in NB:
                y = tuple(a + b for a, b in zip(x, d))
                if y not in S: S.add(y); nf.append(y)
        fr = nf
    return sorted(S)
# ---------------------------------------------------------------- modes
mode = sys.argv[1]
if mode == 'control':
    RJ, IMAX = sys.argv[2], int(sys.argv[3]); ok = True
    F0 = fit_table(np.zeros(48, int)); v = judge(F0, IMAX, 2, list(range(48))); log('control K plain RD:', v); ok &= v == 'killed 1'
    F1 = fit_table(np.ones(48, int)); v = judge(F1, IMAX, 2, list(range(48))); log('control K all bumps:', v); ok &= v.startswith('untileable')
    Hs = np.zeros(48, int); Hs[0] = 1; v = canon(Hs) == canon(-Hs[ACTINV[5]]); log('control canon (turned + inverted copy same):', v); ok &= v
    _, tot = tori(16, list(range(48))); log('tori index <= 16:', tot, '(rd-bridge: 737 + 2224 = 2961)'); ok &= tot == 2961
    log('torus orbits under O_h:', len(tori(16, list(range(48)))[0]), '; under O:', len(tori(16, ROTS)[0]))
    PL = polyforms(1)[1]; v = poly_judge(next(iter(PL)), 4, 2); log('control P single RD:', v); ok &= v == 'killed 1'
    shell = free_canon(list(NB)); v = poly_judge(shell, 0, 1); log('control P cuboctahedral shell (hole):', v); ok &= v.startswith('untileable')
    R = json.load(open(RJ))
    exp = {'CELL+EPART': 'killed 4', 'CELLFRAME': f'no torus <= {IMAX}', 'FRAME+EFR': f'no torus <= {IMAX}'}
    for name, D in R.items():
        T = D['types']; rot = [OHI[tuple(map(tuple, M))] for M in D['rot']]; assert sorted(rot) == sorted(ROTS)
        RIX = {g: i for i, g in enumerate(rot)}; S = T * 24; F = np.zeros((S, 12, S), bool)
        allowed = {}
        for a, ld, b, q in D['rules']: allowed.setdefault((a, ld), []).append((b, q))
        for a in range(T):
            for r in range(24):
                Rg = rot[r]
                for d in range(12):
                    for b, q in allowed.get((a, int(GD[Rg, d])), ()):
                        F[a * 24 + r, d, b * 24 + RIX[int(MUL[rot[q], Rg])]] = True
        v = arc(F); st = np.nonzero(v)[0].tolist(); reps, tot = tori(IMAX, ROTS); verdict = f'no torus <= {IMAX}'
        for i, (n, M, c, nbr) in enumerate(reps):
            if sat_fill(F, st, nbr): verdict = f'killed {n}'; break
            print(f'PROGRESS {(i + 1) / len(reps):.3f} control {name} torus {i + 1}/{len(reps)} index {n}', flush=True)
        log(f'control {name}: {T} types, states viable {len(st)}/{S}: {verdict} (expected {exp.get(name)})'); ok &= verdict == exp.get(name)
    print('FINAL ok' if ok else 'FINAL FAIL: a control failed', flush=True)
elif mode == 'K':
    spec, IMAX, RMAX, SH, OUT = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
    k_sh, n_sh = map(int, SH.split('/')); parts = spec.split(':'); fam = parts[0]
    if fam == 'pair': parts = [fam, '1'] + parts[1:]
    orders = [int(x) for x in parts[1].split(',')]; alph = np.arange(-int(parts[2]), int(parts[2]) + 1); A = len(alph)
    classes = [G for G in subgroups() if len(G) in orders] if fam != 'pair' else [frozenset([IDG])]
    res = {}; surv = []; total = 0; mine = 0; t_last = time.time()
    def run(ci, H):
        global mine
        v = judge(fit_table(H), IMAX, RMAX, list(range(48))); mine += 1
        nm = f'C{ci} ' + gname(classes[ci]); res.setdefault(nm, {}); res[nm][v] = res[nm].get(v, 0) + 1
        if v == 'SURVIVOR': surv.append([gname(classes[ci]), H.tolist()]); log('SURVIVOR', gname(classes[ci]), H.tolist())
        return v
    if fam == 'classes':
        # EXHAUSTIVE, one representative per congruence class (x bump<->dent): H is counted in class G iff its full symmetry group
        # is exactly G (stabiliser size |G|, G-invariant) and H is the least of its images under N(G) x {+-1} (those are exactly
        # the images that are again G-invariant with stabiliser G). Raw assignments are split over shards by index mod NSHARDS.
        plan = []
        for ci, G in enumerate(classes):
            orb = orbits_on_points(G); pt = np.zeros(48, int)
            for oi, o in enumerate(orb): pt[o] = oi
            NG = [g for g in range(48) if {int(MUL[MUL[g, h], INVG[g]]) for h in G} == set(G)]
            plan.append((ci, G, len(orb), pt, NG))
        RAW = sum(A ** m for _, _, m, _, _ in plan); done_raw = 0
        log(f'family {spec}: {len(classes)} subgroup classes {[gname(G) for G in classes]}, raw assignments {RAW}, shard {SH}')
        for ci, G, m, pt, NG in plan:
            idx = np.arange(k_sh, A ** m, n_sh, dtype=np.int64)
            for b0 in range(0, len(idx), 20000):
                ib = idx[b0:b0 + 20000]; dig = (ib[:, None] // (A ** np.arange(m, dtype=np.int64))[None, :]) % A
                Hb = alph[dig][:, pt]                                       # (B, 48)
                stab = (Hb[:, ACTINV] == Hb[:, None, :]).all(2).sum(1)
                for H in Hb[stab == len(G)]:
                    hb = (H + 8).astype(np.uint8).tobytes(); ims = H[ACTINV[NG]]
                    if any(((s_ * r) + 8).astype(np.uint8).tobytes() < hb for r in ims for s_ in (1, -1)): continue
                    total += 1; run(ci, H)
                done_raw += len(ib)
                if time.time() - t_last > 60: t_last = time.time(); print(f'PROGRESS {done_raw * n_sh / RAW:.3f} shard {SH} raw {done_raw}, candidates {total}', flush=True)
    elif fam == 'pair':
        # PAIRED random keyed RDs (no symmetry): the 12 faces are split into 6 random pairs; one face of each pair gets random heights,
        # its partner the complementary heights placed so that the two faces fit in one relative position (a random one of the 4
        # orientations h of the neighbour that present the partner face). Built so that faces have partners; tiling not assumed.
        N, seed = int(parts[3]), int(parts[4]); rng = np.random.default_rng(seed); seen = set()
        while total < N:
            perm = rng.permutation(12); H = np.zeros(48, int)
            for a_, b_ in zip(perm[0::2], perm[1::2]):
                d = int(a_); hs = [h for h in range(48) if int(GD[INVG[h], NEG[d]]) == int(b_)]; h = hs[int(rng.integers(len(hs)))]
                for m, m2 in MATCH[d]:
                    H[m] = alph[int(rng.integers(A))]; H[ACTINV[h][m2]] = -H[m]
            c = canon(H)
            if c in seen: continue
            seen.add(c); total += 1; run(0, H)
            if total % max(1, N // 50) == 0: print(f'PROGRESS {total / N:.3f} shard {SH} {total}/{N}', flush=True)
    else:
        N, seed = int(parts[3]), int(parts[4]); rng = np.random.default_rng(seed); seen = set()
        orbs = []
        for G in classes:
            pt = np.zeros(48, int)
            for oi, o in enumerate(orbits_on_points(G)): pt[o] = oi
            orbs.append((len(G) and 48 // len(G), pt))
        while total < N:
            ci = int(rng.integers(len(classes))); m, pt = orbs[ci]
            H = alph[rng.integers(A, size=m)][pt]; c = canon(H)
            if c in seen: continue
            seen.add(c); total += 1; run(ci, H)
            if total % max(1, N // 50) == 0: print(f'PROGRESS {total / N:.3f} shard {SH} {total}/{N}', flush=True)
    json.dump(dict(spec=spec, shard=SH, imax=IMAX, rmax=RMAX, candidates=total, counts=res, survivors=surv), open(OUT, 'w'))
    log('COUNTS', SH, total, json.dumps(res))
    print('PROGRESS 1.000 shard', SH, 'done', flush=True); print('FINAL ok', flush=True)
elif mode == 'P':
    NMAX, IMAXP, RMAX, SH, OUT = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
    k_sh, n_sh = map(int, SH.split('/')); lv = polyforms(NMAX)
    log('free poly-RDs by size:', {n: len(v) for n, v in lv.items()})
    allP = [P for n in range(1, NMAX + 1) for P in sorted(lv[n])]; mine = allP[k_sh::n_sh]; res = []; cnt = {}; step = max(1, len(mine) // 50)
    for i, P in enumerate(mine):
        v = poly_judge(P, IMAXP, RMAX); res.append([len(P), P, v]); cnt[(len(P), v)] = cnt.get((len(P), v), 0) + 1
        if v == 'SURVIVOR': log('SURVIVOR poly', P)
        if (i + 1) % step == 0 or i + 1 == len(mine): print(f'PROGRESS {(i + 1) / len(mine):.3f} shard {SH} {i + 1}/{len(mine)}', flush=True)
    json.dump(dict(nmax=NMAX, imaxp=IMAXP, rmax=RMAX, shard=SH, counts={f'{n}|{v}': c for (n, v), c in cnt.items()}, results=res), open(OUT, 'w'))
    log('COUNTS', SH, {f'{n}|{v}': c for (n, v), c in sorted(cnt.items())})
    print('FINAL ok', flush=True)
