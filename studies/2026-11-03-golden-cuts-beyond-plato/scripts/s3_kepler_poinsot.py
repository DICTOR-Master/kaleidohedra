"""Step 3. Golden cuts of the four Kepler-Poinsot solids.
Each has regular faces {p} (p = 5, 3, 5/2, 5/2), equal edges and all corners on one sphere, so as in #88 the cut plane
perpendicular to the centre-corner line meets every edge at a corner at the same distance x (checked here: every edge
makes the same angle with the centre-corner line). A face {p} cut at x becomes a 2n-gon whose sides alternate between
the corner sides k x, k = 2cos(pi/p), and the original sides 1 - 2x: for the pentagram k = 2cos(2pi/5) = 1/phi.
Golden: x = phi/(k + 2 phi) or 1/(phi k + 2), exactly as #88 Theorem 2. For the pentagram faces we also record whether
the cut passes the crossing points of the pentagram (at 1/phi^2 of the edge from each tip), and the corner polygon
(the vertex figure: {5/2} for the great dodecahedron and great icosahedron, {5} for the small stellated dodecahedron,
{3} for the great stellated dodecahedron).
usage: python s3_kepler_poinsot.py -> ../data/s3-kepler-poinsot.json
"""
import json, os, itertools
import numpy as np
import sympy as sp
import gcb

phi = (1 + sp.sqrt(5)) / 2; G = float(phi)
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True); assert ok, name


def rings(V, size, side):
    """All regular pentagons/triangles (5 or 3 coplanar points, equal sides `side` in cyclic order) among V."""
    D = np.linalg.norm(V[:, None] - V[None], axis=2); out = set()
    for c in itertools.combinations(range(len(V)), size):
        P = V[list(c)]
        if size > 3 and abs(np.linalg.det(np.c_[P[1:4] - P[0]])) > 1e-9: continue
        if size == 5 and np.linalg.matrix_rank(P[1:] - P[0], 1e-9) != 2: continue
        # cyclic order around the centre
        cen = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); u = P[0] - cen; w = np.cross(n, u)
        order = sorted(c, key=lambda i: np.arctan2((V[i] - cen) @ w, (V[i] - cen) @ u))
        if all(abs(D[order[i], order[(i + 1) % size]] - side) < 1e-9 for i in range(size)):
            out.add(tuple(order))
    return [list(o) for o in out]


ico = gcb.platonic('icosahedron'); dod = gcb.platonic('dodecahedron')
KP = {}
# great dodecahedron: icosahedron corners, faces = the pentagons of the 5 neighbours of each corner (side 1), convex
KP['great dodecahedron'] = dict(V=ico, faces=rings(ico, 5, 1.0), step=1, p=sp.Integer(5), vf='{5/2}')
# great icosahedron: icosahedron corners, faces = equilateral triangles of side phi
KP['great icosahedron'] = dict(V=ico, faces=rings(ico, 3, G), step=1, p=sp.Integer(3), vf='{5/2}')
# small stellated dodecahedron: the same pentagons as the great dodecahedron, traversed as pentagrams (edge phi)
KP['small stellated dodecahedron'] = dict(V=ico, faces=rings(ico, 5, 1.0), step=2, p=sp.Rational(5, 2), vf='{5}')
# great stellated dodecahedron: dodecahedron corners, faces = the inner pentagon rings (side phi), as pentagrams
KP['great stellated dodecahedron'] = dict(V=dod, faces=rings(dod, 5, G), step=2, p=sp.Rational(5, 2), vf='{3}')
NF = {'great dodecahedron': 12, 'great icosahedron': 20, 'small stellated dodecahedron': 12, 'great stellated dodecahedron': 12}
out = []
for name, K in KP.items():
    V, Fr, step, p = K['V'], K['faces'], K['step'], K['p']
    check(f'{name}: {len(Fr)} faces found (expected {NF[name]})', len(Fr) == NF[name])
    F = [[f[(step * i) % len(f)] for i in range(len(f))] for f in Fr]     # face polygons as traversed (pentagram for step 2)
    E = gcb.edges_of(F); L = np.array([np.linalg.norm(V[a] - V[b]) for a, b in E]); V = V / L[0]
    check(f'{name}: {len(E)} edges, all equal', len(E) == 30 and np.ptp(L) < 1e-9)
    # every edge at a corner makes the same angle with the centre-corner line
    ang = []
    for v in range(len(V)):
        es = [b if a == v else a for a, b in E if v in (a, b)]
        ang.append([float((V[w] - V[v]) @ (-V[v]) / np.linalg.norm(V[v])) for w in es])
    ang = np.array(ang)
    check(f'{name}: every edge meets its corner\'s centre line at the same angle (cos {ang[0,0]:.9f})', np.ptp(ang) < 1e-9)
    k = sp.radsimp(2 * sp.cos(sp.pi / p)) if p != sp.Rational(5, 2) else 1 / phi
    check(f'{name}: k = 2cos(pi/{p}) = {k}', abs(float(k) - 2 * np.cos(np.pi / float(p))) < 1e-12)
    rec = {'solid': name, 'face': f'{{{p}}}', 'faces': len(F), 'corner_polygon': K['vf'], 'k': str(k), 'cuts': []}
    for lab, x in (('greater (corner sides long)', sp.radsimp(phi / (k + 2 * phi))), ('lesser (original sides long)', sp.radsimp(1 / (phi * k + 2)))):
        xf = float(x)
        # cut every face: the cut point on edge (v,w) at distance x from v
        ok = True
        for f in F:
            m = len(f); sides = []
            for i in range(m):
                u, v, w = f[i - 1], f[i], f[(i + 1) % m]
                pin = V[v] + xf * (V[u] - V[v]); pout = V[v] + xf * (V[w] - V[v]); pnext = V[w] + xf * (V[v] - V[w])
                sides += [np.linalg.norm(pout - pin), np.linalg.norm(pnext - pout)]
            cs, os_ = np.array(sides[0::2]), np.array(sides[1::2])
            ok &= np.ptp(cs) < 1e-9 and np.ptp(os_) < 1e-9 and abs(max(cs[0], os_[0]) / min(cs[0], os_[0]) - G) < 1e-9
        r = sp.radsimp(max(k * x, 1 - 2 * x, key=lambda e: float(e)) / min(k * x, 1 - 2 * x, key=lambda e: float(e)))
        check(f'{name} {lab}: x = {x} (~{xf:.6f}); every cut face alternates kx, 1-2x with ratio phi (exact {sp.simplify(r - phi) == 0}, float {ok})', ok and sp.simplify(r - phi) == 0 and 0 < xf < .5)
        c = {'cut': lab, 'x': str(sp.nsimplify(sp.simplify(x), [sp.sqrt(5)])), 'x_decimal': xf}
        if p == sp.Rational(5, 2):
            c['passes_crossings'] = bool(xf > float(1 / phi ** 2))
            c['crossing_at'] = '1/phi^2 = ' + str(sp.radsimp(1 / phi ** 2))
        rec['cuts'].append(c)
    out.append(rec)
json.dump({'kepler_poinsot': out, 'checks': CHECKS}, open(os.path.join(DATA, 's3-kepler-poinsot.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
