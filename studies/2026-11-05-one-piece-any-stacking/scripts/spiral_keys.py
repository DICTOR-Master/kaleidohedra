"""DICTO 11-06: the double-spiral key on Narcissus, as rods and notches along edges.
Census (edge_census.py): every face of N touches one neighbour (face keys mate one-to-one), every edge is shared by 3 or 4 pieces.
So a spiral key runs ALONG edges. Edge labels: R (a rod on the edge line, owned by this piece), N (a notch that takes a rod), 0 (plain).
Edge-line rule (rigid, physical): around each edge line either every piece is plain, or exactly one has R and all others have N.
(A notch takes the rod of whichever neighbour owns it: the "accept either" freedom a face key lacks.)
Strand = edge path on N from a hexagon corner down to the apex, turning one way round the axis; the double spiral = a strand as rods
plus its mirror image (in one of the 3 mirror planes of N) as notches. For each design and each placement rule (proper motions only,
or mirror copies too):
  (a) PATCH: some stacking word of K slabs admits a keyed filling of an n x n patch (interior lines only);
  (b) PERIODIC: for periodic words (period <= PMAX) and in-plane periods m <= MMAX, a keyed filling that repeats (torus) exists.
A design that passes (a) and fails every (b) is a CANDIDATE (to be pushed to larger sizes). Heartbeat per design; FINAL line always.
Usage: spiral_keys.py [K n PMAX MMAX [zigzag]]
zigzag (DICTO 11-06 "how about a zig zag variant"): strands are edge paths or closed loops whose turns round the axis ALTERNATE
(left, right, left ...), e.g. the crown of six diagonal edges hexagon corner - middle corner - hexagon corner; designs = a zigzag alone
or with its mirror image, rods and notches spread in the count ratio."""
import sys, time, itertools
import numpy as np
from scipy.spatial import ConvexHull
try:
    from pysat.solvers import Cadical153
except ImportError: Cadical153 = None
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from n_slabs import narc, build, SITE, H
t0 = time.time()
def hb(m): print(f"HEARTBEAT {time.time()-t0:.0f}s {m}", flush=True)
K, NP, PMAX, MMAX = (int(x) for x in (sys.argv[1:5] if len(sys.argv) > 4 else (4, 2, 4, 2)))
# ---------- reference piece
P0 = narc(SITE['A'], H, 0, 'C')
D0 = np.linalg.norm(P0[:, None] - P0[None], axis=2)
def hull_edges(P):
    h = ConvexHull(P); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 7)), set()).update(sp)
    E = set()
    for eq, idx in F.items():
        idx = list(idx); n = np.array(eq[:3]); V = P[idx]; c = V.mean(0); u = V[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        o = [idx[i] for i in np.argsort(np.arctan2((V - c) @ w, (V - c) @ u))]
        for i in range(len(o)): E.add(tuple(sorted((o[i], o[(i + 1) % len(o)]))))
    return sorted(E), h
E0, h0 = hull_edges(P0); assert len(E0) == 18
EI = {e: i for i, e in enumerate(E0)}
# symmetry group of N as corner permutations (distance preserving), with handedness
def perms_matching(Da, Db):
    out = []
    def rec(m):
        k = len(m)
        if k == 10: out.append(tuple(m)); return
        for j in range(10):
            if j in m: continue
            if all(abs(Da[k, i] - Db[j, m[i]]) < 1e-6 for i in range(k)): rec(m + [j])
    rec([]); return out
SYM = perms_matching(D0, D0); assert len(SYM) == 6, len(SYM)
def handed(P, Q, p):   # +1 if the map P[i] -> Q[p[i]] is proper
    A = P[[0, 1, 2, 9]] - P[0]; B = Q[[p[0], p[1], p[2], p[9]]] - Q[p[0]]
    M = np.linalg.lstsq(A[1:], B[1:], rcond=None)[0]; return int(np.sign(np.linalg.det(M)))
# ---------- strands: paths to the apex (9), height non-increasing, azimuth turning one way
c = P0[:6, :2].mean(0)
az = lambda i: np.arctan2(*(P0[i, :2] - c)[::-1])
adj = {i: set() for i in range(10)}
for a, b in E0: adj[a].add(b); adj[b].add(a)
def turn(a, b):
    if b == 9 or np.linalg.norm(P0[a, :2] - P0[b, :2]) < 1e-9: return 0
    d = (az(b) - az(a) + np.pi) % (2 * np.pi) - np.pi; return int(np.sign(d))
strands = set()
def walk(path, sgn):
    a = path[-1]
    if a == 9:
        if len(path) >= 3: strands.add(tuple(tuple(sorted(e)) for e in zip(path, path[1:])))
        return
    for b in adj[a]:
        if b in path or P0[b, 2] > P0[a, 2] + 1e-9: continue
        t = turn(a, b)
        if t == -sgn: continue
        walk(path + [b], sgn)
for s in range(6):
    for sgn in (1, -1): walk([s], sgn)
strands = sorted(strands)
ZIG = len(sys.argv) > 5 and sys.argv[5] == 'zigzag'
if ZIG:
    strands = set()
    def zwalk(path, last):
        a = path[-1]
        if len(path) >= 3:
            strands.add(tuple(sorted(tuple(sorted(e)) for e in zip(path, path[1:]))))
            if path[0] in adj[a] and len(path) >= 4:
                t = turn(a, path[0])
                if t == 0 or t != last: strands.add(tuple(sorted(tuple(sorted(e)) for e in zip(path, path[1:] + [path[0]]))))
        for b in adj[a]:
            if b in path: continue
            t = turn(a, b)
            if t != 0 and t == last: continue          # zigzag: no two turns the same way in a row
            zwalk(path + [b], t if t != 0 else last)
    for s0 in range(10): zwalk([s0], 0)
    strands = sorted(strands)
mirrors = [p for p in SYM if handed(P0, P0, p) < 0]
designs = set()
# COUNT (pilot 11-06): a rod on an edge line takes space from every other piece there, so per edge-length class the notches must be
# (valence - 1) times the rods: hexagon edges (valence 4) N = 3R, all other edges (valence 3) N = 2R. A rod strand facing an equal
# notch strand can never tile. So the double spiral = the edge set of a strand and its mirror, with rods and notches spread over BOTH
# strands in that ratio (every split tried).
LEN = [round(float(np.linalg.norm(P0[a] - P0[b])), 4) for a, b in E0]
VAL = {L: (4 if abs(L - 0.5774) < 1e-3 else 3) for L in set(LEN)}
def canon(lab): return min(tuple(lab[EI[tuple(sorted((p[a], p[b])))]] for a, b in E0) for p in SYM)
USETS = set()
for st in strands:
    for mp in mirrors + ([None] if ZIG else []):
        ms = () if mp is None else tuple(sorted(tuple(sorted((mp[a], mp[b]))) for a, b in st))
        U = frozenset(set(st) | set(ms))
        if len(U) > 12: continue
        cu = min(tuple(sorted(EI[tuple(sorted((p[a], p[b])))] for a, b in U)) for p in SYM)
        USETS.add(cu)
print(f"edge sets (zigzag {'yes' if ZIG else 'no'}) up to symmetry: {len(USETS)}", flush=True)
for U in USETS:
    byL = {}
    for e in U: byL.setdefault(LEN[e], []).append(e)
    per = []
    for L, es in byL.items():
        opts = []
        k = VAL[L] - 1
        for r in range(0, len(es) // (k + 1) + 1):
            for R in itertools.combinations(es, r):
                rest = [e for e in es if e not in R]
                for Nn in itertools.combinations(rest, k * r):
                    if r == 0 and Nn: continue
                    opts.append((R, Nn))
        per.append(opts)
    for combo in itertools.product(*per):
        lab = [0] * 18
        for R, Nn in combo:
            for e in R: lab[e] = 1
            for e in Nn: lab[e] = 2
        if any(lab) and set(i for i in range(18) if lab[i]) == set(U): designs.add(canon(lab))
designs.add(tuple([0] * 18))   # control: no key, must give PATCH and PERIODIC
designs = sorted(designs)
print(f"strands {len(strands)}, double-spiral designs (count-feasible, + control) up to symmetry {len(designs)}; K={K} n={NP} PMAX={PMAX} MMAX={MMAX}", flush=True)
# ---------- tiling structure for a word
def structure(word, n):
    Ps = build(word, n=n); recs = []
    for Q in Ps:
        Dq = np.linalg.norm(Q[:, None] - Q[None], axis=2)
        al = perms_matching(D0, Dq)                     # all 6 alignments ref -> Q
        pl = [(p, handed(P0, Q, p)) for p in al]
        recs.append((Q, pl))
    lines = {}
    for qi, (Q, pl) in enumerate(recs):
        hq = ConvexHull(Q)
        for a, b in E0:   # edge in Q's own corner indexing = image of a ref edge under the identity alignment? use Q's hull edges
            pass
        Eq, _ = hull_edges(Q)
        for a, b in Eq:
            key = tuple(sorted((tuple(np.round(Q[a], 5)), tuple(np.round(Q[b], 5)))))
            # interior dihedral at this edge
            fn = [eq[:3] for eq in hq.equations if abs(eq[:3] @ Q[a] + eq[3]) < 1e-7 and abs(eq[:3] @ Q[b] + eq[3]) < 1e-7]
            fn = np.unique(np.round(fn, 6), axis=0); ang = np.pi - np.arccos(np.clip(fn[0] @ fn[1], -1, 1))
            lines.setdefault(key, []).append((qi, (a, b), ang))
    inner = {k: v for k, v in lines.items() if abs(sum(x[2] for x in v) - 2 * np.pi) < 1e-6}
    return Ps, recs, inner
def label_of(lab, p, a, b):
    inv = {p[i]: i for i in range(10)}
    return lab[EI[tuple(sorted((inv[a], inv[b])))]]
def solve(lab, recs, inner, mirror_ok, classes=None):
    s = Cadical153(); nv = [0]
    def new(): nv[0] += 1; return nv[0]
    X = {}
    for qi, (Q, pl) in enumerate(recs):
        ok = [k for k, (p, hd) in enumerate(pl) if mirror_ok or hd > 0]
        cls = classes[qi] if classes else qi
        for k in range(6): X.setdefault((cls, k), new())
        s.add_clause([X[(cls, k)] for k in ok])
        for k in range(6):
            if k not in ok: s.add_clause([-X[(cls, k)]])
        for k1, k2 in itertools.combinations(range(6), 2): s.add_clause([-X[(cls, k1)], -X[(cls, k2)]])
    for key, inc in inner.items():
        L = []
        for qi, (a, b), _ in inc:
            cls = classes[qi] if classes else qi; pl = recs[qi][1]
            v = {0: new(), 1: new(), 2: new()}
            for k, (p, hd) in enumerate(pl): s.add_clause([-X[(cls, k)], v[label_of(lab, p, a, b)]])
            s.add_clause([v[0], v[1], v[2]])
            L.append(v)
        for i, j in itertools.permutations(range(len(L)), 2):
            s.add_clause([-L[i][1], L[j][2]])        # a rod: every other piece notched
            s.add_clause([-L[i][1], -L[j][1]])
            s.add_clause([-L[i][2], -L[j][0]])       # a notch never beside a plain edge
        for i in range(len(L)): s.add_clause([-L[i][2]] + [L[j][1] for j in range(len(L)) if j != i])   # a notch needs a rod
    r = s.solve(); s.delete(); return r
# ---------- periodic classes: in-plane period m, vertical period from the word
a1 = np.array([1, 0.]); a2 = np.array([.5, np.sqrt(3) / 2]); Mlat = np.array([a1, a2]).T
def classes_for(Ps, word_unit, reps, m):
    p = len(word_unit)
    nl = len(word_unit) * reps + 1; per_layer = len(Ps) // nl
    layer = [i // per_layer for i in range(len(Ps))]
    cen = [P.mean(0) for P in Ps]
    # vertical translation: layer p vs layer 0
    L0 = [cen[i] for i in range(len(Ps)) if layer[i] == 0]; Lp = [cen[i] for i in range(len(Ps)) if layer[i] == p]
    tz = p * H
    def red(x):
        cc = np.linalg.solve(Mlat, x[:2]) / m; f = cc - np.floor(cc + 1e-7); return tuple(np.round(f, 4))
    # find in-plane shift t such that Lp = L0 + (t, tz) mod lattice: try t = Lp[j] - L0[0] for down-N of same orientation
    S0 = {red(x) + (round(x[2] % (2 * H), 4),) for x in L0}
    cand = None
    for y in Lp:
        t = y[:2] - L0[0][:2]
        if all((red(np.r_[x[:2] + t, 0]) + (round((x[2] + tz) % (2 * H), 4),)) in {red(z) + (round(z[2] % (2 * H), 4),) for z in Lp} for x in L0):
            cand = t; break
    if cand is None: return None
    # piece shapes must also match (orientation): compare corner sets
    key = {}
    cls = []
    for i in range(len(Ps)):
        q, r = divmod(layer[i], p)
        x = cen[i] - np.r_[q * cand, q * tz]
        k = (r,) + red(x) + (round(x[2], 4),)
        cls.append(key.setdefault(k, len(key)))
    # verify: pieces in one class are translates (same corner offsets)
    rep = {}
    for i, k in enumerate(cls):
        off = np.round(Ps[i] - cen[i], 5)
        if k in rep:
            if not np.allclose(rep[k], off): return None
        else: rep[k] = off
    return cls
def periodic_words(pmax):
    out = set()
    for p in range(1, pmax + 1):
        for w in itertools.product('ST', repeat=p):
            w = ''.join(w)
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)): continue
            out.add(min(w[i:] + w[:i] for i in range(p)))
    return sorted(out, key=lambda w: (len(w), w))
WORDS = itertools.product('ST', repeat=K - 1)
STRUCT = {}
def get(word, n):
    if (word, n) not in STRUCT: STRUCT[(word, n)] = structure(word, n)
    return STRUCT[(word, n)]
# periodic instances (built once)
PER = []
for wu in periodic_words(PMAX):
    for mult in (1, 2, 3):
        u = wu * mult; reps = 2
        Ps, recs, inner = get(u * reps, max(3, MMAX + 1))
        ok = None
        for m in range(1, MMAX + 1):
            cl = classes_for(Ps, u, reps, m)
            if cl is not None: PER.append((u, m, recs, inner, cl)); ok = True
        if ok: break
hb(f"periodic instances {len(PER)}: " + ', '.join(sorted({f'{u}/m{m}' for u, m, *_ in PER})))
res = []
for di, lab in enumerate(designs):
    for mirror_ok in (False, True):
        patch = None
        for w in itertools.product('ST', repeat=K - 1):
            w = ''.join(w); Ps, recs, inner = get(w, NP)
            if solve(lab, recs, inner, mirror_ok): patch = w; break
        per = None
        if patch:
            for u, m, recs, inner, cl in PER:
                if solve(lab, recs, inner, mirror_ok, cl): per = f'{u}/m{m}'; break
        verdict = 'NO PATCH' if not patch else ('PERIODIC ' + per if per else 'CANDIDATE')
        res.append((di, mirror_ok, verdict))
        hb(f"design {di} labels {''.join('0RN'[x] for x in lab)} mirrors={'yes' if mirror_ok else 'no'}: {verdict}" + (f" (patch word {patch})" if patch else ''))
from collections import Counter
print('SUMMARY', dict(Counter((mo, v.split()[0]) for _, mo, v in res)), flush=True)
cands = [(d, mo) for d, mo, v in res if v == 'CANDIDATE']
print(f"FINAL {'CANDIDATES ' + str(cands) if cands else 'no candidate'} {time.time()-t0:.0f}s", flush=True)
