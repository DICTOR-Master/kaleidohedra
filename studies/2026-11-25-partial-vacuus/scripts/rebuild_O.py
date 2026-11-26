# DICTO · rebuild the Ogdoecontahedron shell O of Double Vision exactly (26 Nov 2026). With Claude (Anthropic).
# DICTO: "rebuild octahedron shell and store data". O = polar of the Hecatodihedron H (progenitors #34: "the Ogdoecontahedron O (its
# polar in the unit sphere)"), placed on the Dharma's ID at scale 3φ²/4 (Double Vision's middle toggle; study 2026-10-16-progenitors,
# fullcycle_add_o.py, data/full-cycle.json st.O, render precision). Here: O_exact = c · poles(H_exact) from the exact H of
# stations-exact.json (Q(√5)); c fitted to the stored O, identified in Q(√5), and every corner checked against the stored copy.
# Then the same nested-pair pit test as the golden cycle, with O added. Writes data-double-vision-O.json (exact corners as a + b√5).
import json, os, numpy as np, sympy as sp
from scipy.spatial import ConvexHull, Delaunay
HERE = os.path.dirname(os.path.abspath(__file__)); r5 = 5 ** .5
ST = json.load(open(os.path.join(HERE, '../../2026-10-25-gnomon-shapes/stations-exact.json')))
FC = json.load(open(os.path.join(HERE, '../../2026-10-16-progenitors/data/full-cycle.json')))
S5 = sp.sqrt(5); ex = lambda q: sp.Rational(q[0]) + sp.Rational(q[1]) * S5
C = {k: np.array([[float(ex(c)) for c in v] for v in vs]) for k, vs in ST.items()}
Hx = [[ex(c) for c in v] for v in ST['H']]
H = ConvexHull(C['H']); planes = {}
for e, sm in zip(H.equations, H.simplices): planes.setdefault(tuple(np.round(e, 9)), set()).update(sm)
poles = []
for k, idx in planes.items():     # exact pole: plane through three exact corners, n·x = d  ->  pole n/d
    i, j, l = list(idx)[:3]; a, b, c = (sp.Matrix(Hx[t]) for t in (i, j, l))
    n = (b - a).cross(c - a); d = n.dot(a)
    if d < 0: n, d = -n, -d
    poles.append([sp.nsimplify(sp.radsimp(x / d)) for x in n])
P = np.array([[float(x) for x in p] for p in poles]); Ostore = np.array(FC['st']['O']['v'], float)
print('H faces', len(planes), '-> O corners', len(P), '; stored O corners', len(Ostore))
# frames: the stored full cycle and the golden-cycle stations must share the ID (checked)
IDs = np.array(FC['st']['ID']['v'], float); same = all(np.min(np.linalg.norm(IDs - x, axis=1)) < 1e-5 for x in C['ID'])
c = float(np.linalg.norm(Ostore, axis=1).max() / np.linalg.norm(P, axis=1).max())
cx = sp.nsimplify(c, [S5], tolerance=1e-7); print('frames shared (ID):', same, '; scale c =', c, '=', cx)
Ox = [[sp.radsimp(cx * x) for x in p] for p in poles]; O = np.array([[float(x) for x in p] for p in Ox])
match = all(np.min(np.linalg.norm(Ostore - x, axis=1)) < 1e-5 for x in O) and len(O) == len(Ostore)
print('exact O matches the stored O (1e-5, render precision):', match)
def split(x):
    x = sp.radsimp(sp.expand(x)); b = sp.Rational(sp.expand(x).coeff(S5)); a = sp.Rational(sp.expand(x - b * S5)); return [str(a), str(b)]
json.dump(dict(name='O (Ogdoecontahedron) at its Double Vision station', note='corners a + b*sqrt5, exact; polar of H scaled by c', c=str(cx),
               corners=[[split(x) for x in p] for p in Ox]), open(os.path.join(HERE, '../data-double-vision-O.json'), 'w'), indent=1)
C['O'] = O; rng = np.random.default_rng(0)
def faces(Pt):
    Hh = ConvexHull(Pt); out = {}
    for e, sm in zip(Hh.equations, Hh.simplices): out.setdefault(tuple(np.round(e, 7)), set()).update(sm)
    return out
hits = []
for X in C:
    for Y in C:
        if X == Y or 'O' not in (X, Y) or 'tips' in X + Y: continue
        In, Out = C[X], C[Y]; F = faces(Out)
        if not all(np.max(Out @ np.array(k[:3])) >= np.max(In @ np.array(k[:3])) - 1e-9 for k in F): continue
        dIn = Delaunay(In); s = []; ok = True
        for k, idx in F.items():
            n = np.array(k[:3]); d = -k[3]; hit = [p for p in In if np.linalg.norm(np.cross(p, n)) < 1e-8 and p @ n > 0]
            if len(hit) != 1: ok = False; break
            a = hit[0]; base = Out[list(idx)]
            for _ in range(200):
                w = rng.dirichlet(np.ones(len(base) + 1)); x = w[:-1] @ base + w[-1] * a
                if dIn.find_simplex(x) >= 0 and np.linalg.norm(x - a) > 1e-6: ok = False; break
            if not ok: break
            s.append(round(a @ n / d, 9))
        print(f'{X:8s} in {Y:8s}: nested; full set of pits in the gap: {ok and len(set(s)) == 1}', flush=True)
        if ok and len(set(s)) == 1: hits.append((X, Y, s[0]))
print('pairs with O holding a full set of pits:', hits)
print('FINAL ok' if (same and match) else 'FINAL FAIL (O does not match the stored station)')
