# keyed_rd.py, DICTO 12 Nov 2026 ("go ahead with the keyed RD"). Turn the certified 62-type marking (scheme H18) into SHAPE, the way
# Chair44 does for the chair (Tsiokos): tiny square pyramids (bumps +h, dents -h) at fixed positions on each rhombic face of each marked
# RD; two RD faces meet flush only if at every position a bump meets a dent of the same size (h_A + h_B = 0).
# Positions per face: K orbits of the rhombus's symmetry group (180-degree turn and the two diagonal mirrors), in face coordinates
# (u along the long diagonal, v along the short), generic so that every face isometry permutes them without fixed points.
# Unknowns: h[type, canonical face, position]. Each ALLOWED neighbour pair (type a, face dir, type b, relative turn) gives equations
# h_a(p) = -h_b(p') for every position (p' = p seen from b). Types with a symmetry (several canonical turns) force h invariant.
# Union-find with signs -> classes; a class forced equal to its own negative is 0 (flat). Each other class gets its own size 1, 2, ...
# CHECK (exhaustive): for every (type a, face direction, type b, every one of the 24 turns of b): the faces fit <=> the pair is allowed.
# Controls: allowed pairs fit by construction (asserted); the count of fitting pairs must equal the count of allowed pairs exactly.
# usage: keyed_rd.py <level k> <scheme> <K orbits> <out.json>
import sys, os, json, itertools
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, 'vendor'))
K_, SCH, KORB, KOUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), os.path.abspath(sys.argv[4])   # KOUT: cut_down.py (exec'd below) sets its own OUT (12 Nov fault)
src = open(os.path.join(here, 'cut_down.py')).read(); src = src[:src.index('def sublattices')]
sys.argv = ['cut_down.py', K_, '1', '/dev/null']; exec(src)
from fractions import Fraction as Q
f = SCHEMES[SCH]; lab = {}; tid = {}
for x in sites:
    L, arg = canon(f(entries(x))); lab[x] = (tid.setdefault(L, len(tid)), tuple(sorted(RI[R] for R in arg)))
exec(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refine_snip.py')).read())   # REFINE=n: exact-keying refinement (12 Nov)
T = len(tid)
allowed = set(); seen = set()
for x in lab:
    for d in NB:
        y = vadd(x, d)
        if y not in lab or (lab[x], lab[y], d) in seen: continue
        seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
        for r in Ra:
            R = ROT[r]
            for q in Rb: allowed.add((a, apply(R, d), b, RI[compose(ROT[q], inverse(R))]))
SYMS = {a: set() for a in range(T)}                         # turns S with S.(canonical label) = canonical label: S = R' R^-1 over argmin
for x in lab:
    a, Ra = lab[x]
    if len(SYMS[a]) < len(Ra):
        R0 = ROT[Ra[0]]; SYMS[a] = {RI[compose(ROT[r], inverse(R0))] for r in Ra}
print(f'{SCH}: {T} types, {len(allowed)} allowed (type, face, type, turn) pairs; symmetric types {sum(len(s) > 1 for s in SYMS.values())}', flush=True)
# face geometry: face toward neighbour direction e (one of NB) on the RD at the origin: centre e/2; long diagonal between the two
# 4-valent corners (the coordinate axes where e is nonzero), short diagonal along the axis where e is 0.
def face_frame(e):
    nz = [i for i in range(3) if e[i] != 0]; z = next(i for i in range(3) if e[i] == 0)
    c1 = [0, 0, 0]; c1[nz[0]] = e[nz[0]]; c2 = [0, 0, 0]; c2[nz[1]] = e[nz[1]]
    U = tuple(Q(c1[i] - c2[i], 2) for i in range(3)); V = tuple(Q(1 if i == z else 0) for i in range(3))
    C = tuple(Q(e[i], 2) for i in range(3)); return C, U, V
BASE = [(Q(3, 10), Q(1, 7)), (Q(1, 6), Q(2, 9)), (Q(2, 5), Q(1, 11)), (Q(1, 8), Q(3, 13))][:KORB]   # generic (u, v) seeds
OFFS = [(s * u, t * v) for u, v in BASE for s in (1, -1) for t in (1, -1)]
def positions(e):
    C, U, V = face_frame(e); return [tuple(C[i] + a * U[i] + b * V[i] for i in range(3)) for a, b in OFFS]
POS = {e: positions(e) for e in NB}
PIDX = {e: {p: j for j, p in enumerate(POS[e])} for e in NB}
def var(a, e, j): return (a * 12 + NB.index(e)) * len(OFFS) + j
NV = T * 12 * len(OFFS)
par = list(range(NV)); sgn = [1] * NV                        # value(v) = sgn[v] * value(root)
def find(v):
    if par[v] == v: return v, 1
    r, s = find(par[v]); par[v] = r; sgn[v] *= s; return r, sgn[v]
ZERO = set()
def union(u, v, s):                                         # impose value(u) = s * value(v)
    (ru, su), (rv, sv) = find(u), find(v)
    if ru == rv:
        if su != s * sv: ZERO.add(ru)                       # x = -x: this class is flat
        return
    par[ru] = rv; sgn[ru] = s * sv * su                     # value(ru) = su * value(u) ... keep: value(u) = su*value(ru)
def b_point(p, e, q):
    """point p on a's face e, seen from b at e with relative turn q: ROT[q] (p - e)"""
    return apply(ROT[q], tuple(p[i] - e[i] for i in range(3)))
for a, e, b, q in sorted(allowed):
    eb = apply(ROT[q], tuple(-x for x in e))
    for j, p in enumerate(POS[e]):
        pb = b_point(p, e, q)
        assert pb in PIDX[eb], 'positions not mapped onto positions (face isometry)'
        union(var(a, e, j), var(b, eb, PIDX[eb][pb]), -1)
for a in range(T):                                          # symmetric labels: heights invariant under the label's own turns
    for s_ in SYMS[a]:
        S = ROT[s_]
        for e in NB:
            for j, p in enumerate(POS[e]):
                p2 = apply(S, p); e2 = apply(S, e); union(var(a, e, j), var(a, e2, PIDX[e2][p2]), 1)
roots = {}; H = [0] * NV
for v in range(NV):
    r, s = find(v)
    if r in ZERO or any(find(z)[0] == r for z in ZERO): H[v] = 0; continue
    H[v] = s * roots.setdefault(r, len(roots) + 1)
flat = sum(1 for h in H if h == 0)
print(f'classes {len(roots)} (sizes 1..{len(roots)}), flat positions {flat} of {NV}', flush=True)
# 12 Nov (exact keying): indexed fit check, same relation as the exhaustive loop (b fits a at (e, q) iff b's mapped code = -a's code)
from collections import defaultdict as _dd
FITSET = set()
for e in NB:
    for q in range(24):
        eb = apply(ROT[q], tuple(-x for x in e)); mp = [PIDX[eb][b_point(p, e, q)] for p in POS[e]]
        idx = _dd(list)
        for b in range(T): idx[tuple(H[var(b, eb, k)] for k in mp)].append(b)
        for a in range(T):
            for b in idx.get(tuple(-H[var(a, e, j)] for j in range(len(POS[e]))), ()): FITSET.add((a, e, b, q))
fit = len(FITSET); bad_fit = sorted(FITSET - allowed); miss = sorted(allowed - FITSET)
print(f'pairs that fit: {fit}; allowed: {len(allowed)}; allowed but not fitting: {len(miss)}; fitting but NOT allowed: {len(bad_fit)}', flush=True)
FITREL = [(a, list(e), b, q) for a, e, b, q in sorted(FITSET)]
# next targeted refinement round (exact keying): face states joined by fits; every class holding an extra fit gets its faces recorded
_p = {}
def _f(u):
    while _p.setdefault(u, u) != u: _p[u] = _p[_p[u]]; u = _p[u]
    return u
for a, e, b, q in FITSET: _p[_f((a, e))] = _f((b, apply(ROT[q], tuple(-x for x in e))))
_badc = {_f((a, e)) for a, e, b, q in bad_fit}
NEXT = {}
for u in list(_p):
    if _f(u) in _badc: NEXT.setdefault(KEY[u[0]], []).append(list(u[1]))
print(f'next refinement round: {sum(len(v) for v in NEXT.values())} faces on {len(NEXT)} types', flush=True)
json.dump(dict(next_round={k: sorted(v) for k, v in NEXT.items()}, type_keys=[KEY[i] for i in range(T)], fit_relation=FITREL, type_labels=[repr(L) for L in tid], scheme=SCH, types=T, orbits=KORB, positions=[[str(x) for x in o] for o in OFFS], classes=len(roots), flat=flat,
               fit=fit, allowed=len(allowed), bad_fit=len(bad_fit), miss=len(miss),
               heights={f'{a}:{e}': [H[var(a, e, j)] for j in range(len(OFFS))] for a in range(T) for e in NB}), open(KOUT, 'w'))
ok = not miss and not bad_fit
print('VERDICT', 'KEYED: the bumps and dents admit exactly the allowed face pairs' if ok else 'NOT YET: the features accept forbidden pairs (more positions or a finer scheme needed)', flush=True)
print('FINAL ok' if not miss else 'FINAL FAIL: an allowed pair does not fit (construction error)', flush=True)
