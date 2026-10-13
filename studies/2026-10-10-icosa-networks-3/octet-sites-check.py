# Check (2026-10-13) for the DICTO Icosahedral Octet world: the site rules of src/app/octet-data.js fill space. Octahedron cells at
# (a/2)n, n integer with even sum; tetrahedron cells at (a/4)s, s odd, inverted when sum(s) = 1 mod 4; Frog Chorus at (a/2)n, odd sum.
# Random points in one cube of the lattice must each lie in exactly one piece.
import json, itertools, numpy as np
s = open('src/app/octet-data.js').read(); D = json.loads(s[s.index('{'):s.rindex('}') + 1]); a = D['a']; C = D['cells']
def solid(V, F):
    V = np.array(V); T = [(V[f[0]], V[f[i]], V[f[i + 1]]) for f in F for i in range(1, len(f) - 1)]
    return V.min(0), V.max(0), np.array(T)
def inside(sol, p):
    lo, hi, T = sol
    if np.any(p < lo - 1e-9) or np.any(p > hi + 1e-9): return False
    a_, b_, c_ = T[:, 0] - p, T[:, 1] - p, T[:, 2] - p
    la, lb, lc = [np.linalg.norm(x, axis=1) for x in (a_, b_, c_)]
    num = np.einsum('ij,ij->i', a_, np.cross(b_, c_))
    den = la * lb * lc + np.einsum('ij,ij->i', a_, b_) * lc + np.einsum('ij,ij->i', b_, c_) * la + np.einsum('ij,ij->i', c_, a_) * lb
    return abs(2 * np.arctan2(num, den).sum()) > 2 * np.pi
def placed(cell, t, invert=False):
    return [solid([(-np.array(v) if invert else np.array(v)) + t for v in V], [f[::-1] for f in F] if invert else F) for _, V, F in cell]
for view, tetcell, extra in [('caps', 'tet', False), ('allIco', 'tetIco', False), ('frog', None, True)]:
    sols = []
    R = range(-2, 4)
    for n in itertools.product(R, repeat=3):
        n = np.array(n)
        if n.sum() % 2 == 0:
            sols += placed(C['oct'], n * a / 2) if view != 'frog' else placed(C['oct'][:1], n * a / 2)
        elif view == 'frog':
            sols += placed(C['frog'], n * a / 2)
    if view == 'frog':
        tetcell = 'tetIco'
    for sv in itertools.product(range(-3, 8, 2), repeat=3):
        sv = np.array(sv); t = sv * a / 4
        cell = C[tetcell] if view != 'frog' else C['tetIco'][:1]
        sols += placed(cell, t, invert=(sv.sum() % 4 == 1))
    rng = np.random.default_rng(1); pts = rng.uniform(0, a, (1500, 3))
    counts = [sum(inside(s_, p) for s_ in sols) for p in pts]
    print(view, 'pieces', len(sols), '| points in exactly one piece:', counts.count(1), 'of', len(counts), '| none', counts.count(0), '| two+', sum(c > 1 for c in counts))
