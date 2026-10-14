# Truncated rhombi (DICTO, 2026-10-14): the rhombic dodecahedron's rhombus (diagonals 1 : sqrt2, angles 70.53° / 109.47°) and the
# golden rhombus (diagonals 1 : phi, angles 63.43° / 116.57°), with their corners cut off. Two questions, as for the FUJI family:
# (1) for which cuts is the truncated rhombus cyclic (all corners on one circle), so that a pyramid with equal side edges stands
#     on it; (2) which solids have truncated rhombi as faces when their face planes are all at the same depth (the "even spacing"
#     that fixed the dictosphere): the rhombic dodecahedron with the cube's or the octahedron's planes, the rhombic triacontahedron
#     with the icosahedron's or the dodecahedron's planes. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.optimize import brentq
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
RHOMBI = {'RD rhombus': math.sqrt(2), 'golden rhombus': phi}       # long / short diagonal
def rhombus(q):          # unit short diagonal along y, long diagonal q along x
    return np.array([[q / 2, 0], [0, .5], [-q / 2, 0], [0, -.5]])
def cut(P, which, t):    # cut corners: 'sharp' (on the long diagonal), 'blunt' (short diagonal), 'all'; t = fraction of side cut
    out = []
    for i in range(4):
        A, B, C = P[i - 1], P[i], P[(i + 1) % 4]; sharp = i % 2 == 0
        if which == 'all' or (which == 'sharp') == sharp:
            out += [B + (A - B) * t, B + (C - B) * t]
        else: out.append(B)
    return np.array(out)
def circ_spread(P):      # how far the corners are from lying on one circle (centred at the rhombus centre, by symmetry)
    r = np.linalg.norm(P, axis=1); return r.max() - r.min()
res = {'cyclic': {}}
for name, q in RHOMBI.items():
    ang = math.degrees(2 * math.atan(1 / q))
    for which in ('sharp', 'blunt', 'all'):
        f = lambda t: (lambda r: r[0] - r[1])(sorted(set(np.round(np.linalg.norm(cut(rhombus(q), which, t), axis=1), 12)))[:2] if False else 0)
        # corners' distances from the centre: for 'sharp' the 2 blunt corners (0.5) and the 4 cut points; equal when cyclic
        def g(t):
            P = cut(rhombus(q), which, t); r = np.linalg.norm(P, axis=1); return r.max() - r.min()
        ts = np.linspace(1e-4, 0.4999, 4000); vals = [g(t) for t in ts]; k = int(np.argmin(vals))
        t0 = ts[k]
        if vals[k] < 1e-3:
            from scipy.optimize import minimize_scalar
            t0 = minimize_scalar(g, bounds=(max(1e-4, t0 - 0.01), min(.4999, t0 + 0.01)), method='bounded', options=dict(xatol=1e-13)).x
            P = cut(rhombus(q), which, t0); L = [float(np.linalg.norm(P[i] - P[(i + 1) % len(P)])) for i in range(len(P))]
            res['cyclic'][f'{name}, {which} corners'] = dict(rhombus_angle=round(ang, 4), cut_fraction=round(float(t0), 9), spread=float(g(t0)),
                                                         sides=sorted({round(x, 6) for x in L}), radius=float(np.linalg.norm(P[0])))
        else:
            res['cyclic'][f'{name}, {which} corners'] = dict(rhombus_angle=round(ang, 4), cyclic='never')
# equal-depth solids
def solid(normals_a, normals_b):
    H = [list(n) + [-1.0] for n in normals_a] + [list(n) + [-1.0] for n in normals_b]
    V = HalfspaceIntersection(np.array(H, float), np.zeros(3)).intersections; V = np.unique(np.round(V, 9), axis=0)
    h = ConvexHull(V); faces = {}
    for e in np.unique(np.round(h.equations, 7), axis=0):
        on = np.where(np.abs(V @ e[:3] + e[3]) < 1e-6)[0]; c = V[on].mean(0); a = V[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        Q = V[on[np.argsort(np.arctan2((V[on] - c) @ b, (V[on] - c) @ a))]]
        L = [round(float(np.linalg.norm(Q[i] - Q[(i + 1) % len(Q)])), 5) for i in range(len(Q))]
        A = [round(math.degrees(math.acos(np.clip((Q[i - 1] - Q[i]) @ (Q[(i + 1) % len(Q)] - Q[i]) / np.linalg.norm(Q[i - 1] - Q[i]) / np.linalg.norm(Q[(i + 1) % len(Q)] - Q[i]), -1, 1))), 2) for i in range(len(Q))]
        key = (len(Q), tuple(sorted(set(L))), tuple(sorted(set(A)))); faces[key] = faces.get(key, 0) + 1
    return {f'{k[0]}-gon x{v}: sides {list(k[1])}, angles {list(k[2])}': v for k, v in faces.items()}
U = lambda vs: [np.array(v, float) / np.linalg.norm(v) for v in vs]
rd = U([p for s in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((s[0], s[1], 0)))])
cube = U([p for i in range(3) for p in [tuple(1 if j == i else 0 for j in range(3)), tuple(-1 if j == i else 0 for j in range(3))]])
octa = U(list(itertools.product((1, -1), repeat=3)))
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
E = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]
rt = U([ico[a] + ico[b] for a, b in E])                      # 30 two-fold directions: the triacontahedron's faces
five = U(list(ico))                                            # 12 five-fold: the dodecahedron's faces
tri = U([ico[a] + ico[b] + ico[c] for a, b, c in itertools.combinations(range(12), 3)
         if all(abs(np.linalg.norm(ico[x] - ico[y]) - 2) < 1e-9 for x, y in ((a, b), (b, c), (a, c)))])   # 20 three-fold
res['equal_depth'] = {'RD + cube planes (cuts the 4-valent, sharp corners)': solid(rd, cube),
                      'RD + octahedron planes (cuts the 3-valent, blunt corners)': solid(rd, octa),
                      'RT + dodecahedron planes (cuts the 5-valent, sharp corners)': solid(rt, five),
                      'RT + icosahedron planes (cuts the 3-valent, blunt corners)': solid(rt, tri)}
json.dump(res, open(os.path.join(ROOT, 'rhombi.json'), 'w'), indent=1); print(json.dumps(res, indent=1))
