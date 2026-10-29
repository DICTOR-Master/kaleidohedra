# Five pyramids study (DICTO, 2026-10-27): exact library of the pieces used.
# Every piece is given by exact sympy vertices and outward-wound faces. Sources:
#   regular solids, face pyramids, half octahedron P: classical, built here;
#   Cleo-Icos = icosahedron face pyramid (#29, #44); Antonius = middle third of the prolate golden rhombohedron (#20, #44);
#   Admiral Cap = krp-core edgeRoof.js (#47); AXE = M-S t6, CLEO = M-S t4, Tricap = M-S t3, Hound Tooth = M-S t2
#   (krp-core mosseri-sadoc.js; edge tables from the reference library shapes/mosseri-sadoc-tiles.json);
#   Weirdstone (tet corner cap) and Tadpole (tet edge cap): k-research studies/2026-10-10-icosa-networks-3/data;
#   Penta-cleo: krp-core cleo-sphere.js.
import itertools, json, sys
import sympy as sp
import numpy as np
from scipy.spatial import ConvexHull

s5, s2, s3 = sp.sqrt(5), sp.sqrt(2), sp.sqrt(3)
phi = (1 + s5) / 2

def V3(*a): return sp.Matrix([sp.nsimplify(x) if not isinstance(x, sp.Basic) else x for x in a])

def fl(V): return np.array([[float(x) for x in v] for v in V])

def hull_faces(V):
    """Faces of the convex hull, coplanar triangles merged, ccw seen from outside."""
    P = fl(V); H = ConvexHull(P); groups = {}
    for simp, eq in zip(H.simplices, H.equations):
        key = tuple(np.round(eq, 7)); groups.setdefault(key, set()).update(simp.tolist())
    F = []
    for key, idx in groups.items():
        n = np.array(key[:3]); idx = list(idx); c = P[idx].mean(0)
        u = P[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); F.append(idx)
    return F

def orient(V, F):
    """Make faces outward (positive signed volume)."""
    P = fl(V); vol = 0
    for f in F:
        for k in range(1, len(f) - 1):
            vol += np.dot(P[f[0]], np.cross(P[f[k]], P[f[k + 1]]))
    return F if vol > 0 else [list(reversed(f)) for f in F]

def tetra_from_edges(d):  # d = (d01, d02, d03, d12, d13, d23), exact
    d01, d02, d03, d12, d13, d23 = d
    x2 = (d01**2 + d02**2 - d12**2) / (2 * d01); y2 = sp.sqrt(sp.simplify(d02**2 - x2**2))
    x3 = (d01**2 + d03**2 - d13**2) / (2 * d01)
    y3 = sp.simplify((d03**2 + d02**2 - d23**2 - 2 * x3 * x2) / (2 * y2))
    z3 = sp.sqrt(sp.simplify(d03**2 - x3**2 - y3**2))
    return [sp.Matrix([0, 0, 0]), sp.Matrix([d01, 0, 0]), sp.Matrix([x2, y2, 0]), sp.Matrix([x3, y3, z3])]

def ico():
    V = []
    for a, b in itertools.product((1, -1), repeat=2):
        V += [sp.Matrix([0, a * sp.Rational(1, 2), b * phi / 2]), sp.Matrix([a * sp.Rational(1, 2), b * phi / 2, 0]),
              sp.Matrix([b * phi / 2, 0, a * sp.Rational(1, 2)])]
    return V

def dodeca():  # edge 1/phi... scaled: vertices (+-1,+-1,+-1), (0,+-1/phi,+-phi) etc, edge 2/phi
    V = [sp.Matrix(s) for s in itertools.product((1, -1), repeat=3)]
    for a, b in itertools.product((1, -1), repeat=2):
        V += [sp.Matrix([0, a / phi, b * phi]), sp.Matrix([a / phi, b * phi, 0]), sp.Matrix([b * phi, 0, a / phi])]
    return V

def nearest(V, i, d):
    return [j for j in range(len(V)) if j != i and sp.simplify((V[j] - V[i]).norm() - d) == 0]

def build():
    L = {}
    def add(name, V, F=None, note=''):
        V = [sp.Matrix([sp.radsimp(x) for x in v]) for v in V]
        F = orient(V, F if F is not None else hull_faces(V)); L[name] = dict(V=V, F=F, note=note)
    # regular solids, edge 1
    T = [sp.Matrix(v) / (2 * s2) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    O = [sp.Matrix(v) / s2 for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
    I = ico()
    Cb = [sp.Matrix(v) / 2 for v in itertools.product((1, -1), repeat=3)]
    D = dodeca()
    add('Tetrahedron', T, note='regular, edge 1'); add('Octahedron', O, note='regular, edge 1'); add('Icosahedron', I, note='regular, edge 1')
    Z = sp.zeros(3, 1)
    # the five face pyramids (centre + one face)
    add('Q (tetrahedron face pyramid)', T[1:] + [Z], note='#44 T, #47 connector Q')
    add('Octahedron face pyramid', [O[0], O[2], O[4], Z], note='#44 O')
    # pick a genuine face: I[0] and two mutually adjacent neighbours
    nb = [j for j in range(12) if sp.simplify((I[j] - I[0]).norm() - 1) == 0]
    j, k = next((a, b) for a, b in itertools.combinations(nb, 2) if sp.simplify((I[a] - I[b]).norm() - 1) == 0)
    add('Cleo-Icos', [I[0], I[j], I[k], Z], note='icosahedron face pyramid (#29, #44)')
    add('Cube face pyramid', [v for v in Cb if v[2] > 0] + [Z], note='#44 C (no equilateral face)')
    # dodecahedron face pyramid: a pentagon of the dodecahedron
    e = 2 / phi; nbD = nearest(D, 0, e)
    a = nbD[0]; b = [x for x in nearest(D, a, e) if x != 0][0]; c = [x for x in nearest(D, 0, e) if x != a][0]
    d_ = [x for x in nearest(D, c, e) if x != 0 and sp.simplify((D[x] - D[b]).norm() - e) == 0][0]
    add('Dodecahedron face pyramid', [D[0], D[a], D[b], D[d_], D[c], Z], note='#44 D (no equilateral face)')
    add('Half octahedron P', O[:5], note='J1 square pyramid, #47 connector P')
    # Antonius: middle third of the golden rhombohedron spanned by the Cleo-Icos's three corner rays
    A, B, C = I[0], I[j], I[k]
    add('Antonius', [A, B, C, A + B, B + C, A + C], note='#20, #44')
    # Admiral Cap (krp-core edgeRoof.js, exact): faces given (non-convex: two tetrahedra over an icosahedron edge)
    Vc = [sp.Matrix([phi / 2, 0, -sp.Rational(1, 2)]), sp.Matrix([phi / 2, 0, sp.Rational(1, 2)]), sp.Matrix([phi**2 / 2, 0, 0]),
          sp.Matrix([sp.Rational(1, 2), -phi / 2, 0]), sp.Matrix([sp.Rational(1, 2), phi / 2, 0])]
    add('Admiral Cap', Vc, [[2, 1, 3], [2, 3, 0], [1, 0, 3], [2, 4, 1], [2, 0, 4], [4, 0, 1]], note='D16, #47 (icosahedron + 6 = octahedron)')
    # Mosseri-Sadoc tiles, edge codes for pairs 01 02 03 12 13 23 at the M-S scale (1, tau)
    codes = {'M-S t1': 'LSSSSS', 'Hound Tooth (M-S t2)': 'SSSSLL', 'Tricap (M-S t3)': 'LLSLSS', 'CLEO (M-S t4)': 'SSLSLL',
             'M-S t5': 'LLSLSL', 'AXE (M-S t6)': 'SLLLLL'}
    for nm, cd in codes.items():
        add(nm, tetra_from_edges([phi if ch == 'L' else sp.Integer(1) for ch in cd]), note='Mosseri-Sadoc tile, edges 1 and tau')
    # Weirdstone and Tadpole: exact from the 10-10 study data (Q(sqrt5) coordinates recovered and checked below)
    import os  # the 10-10 study's data; on dicto-big-brother a copy sits in ~/kres-tmp/pyramids/srcdata/
    base = next(p for p in [os.environ.get('SRCDATA', ''), os.path.expanduser('~/kres-tmp/pyramids/srcdata/'),
                            os.path.expanduser('~/k-research/studies/2026-10-10-icosa-networks-3/data/')] if p and os.path.isdir(p))
    for nm, fn in [('Weirdstone', 'tet-corner-cap-unit.json'), ('Tadpole', 'tet-edge-cap-unit.json')]:
        dd = json.load(open(base + fn))
        V = [sp.Matrix([sp.nsimplify(round(x, 9), [s5], tolerance=1e-8) for x in v]) for v in dd['vertices']]
        add(nm, V, dd['faces'], note='octet tetrahedron cap round the icosahedron of edge 1/2 (F21)')
    Vp = [[0.633155952013, -0.125000000786, 0.189057648658], [-0.090450850288, -0.125000000786, -0.258155949655],
          [-0.366844054276, -0.125000000786, 0.189057648658], [-0.17586104745, 0.375000002358, -0.119959347661]]
    add('Penta-cleo', [sp.Matrix(v) for v in Vp], note='#20 (float source; no equilateral face, not used exactly)')
    return L

def face_info(P):
    V, out = P['V'], []
    for f in P['F']:
        ls = [sp.radsimp(sp.sqrt(sp.expand(((V[f[i]] - V[f[(i + 1) % len(f)]]).T * (V[f[i]] - V[f[(i + 1) % len(f)]]))[0]))) for i in range(len(f))]
        out.append(ls)
    return out

if __name__ == '__main__':
    L = build()
    rep = {}
    for nm, P in L.items():
        fi = face_info(P)
        eqs = [ls[0] for ls in fi if len(ls) == 3 and all(sp.simplify(x - ls[0]) == 0 for x in ls)]
        # check planarity exactly
        planar = True
        for f in P['F']:
            if len(f) > 3:
                a, b, c = (P['V'][f[i]] for i in range(3)); n = (b - a).cross(c - a)
                planar &= all(sp.simplify((n.T * (P['V'][q] - a))[0]) == 0 for q in f[3:])
        rep[nm] = dict(nV=len(P['V']), faces=[[str(x) for x in ls] for ls in fi], n_equilateral=len(eqs),
                       equilateral_edges=sorted(set(str(x) for x in eqs)), planar=planar, note=P['note'])
        print(nm, '| faces', len(P['F']), '| equilateral', len(eqs), sorted(set(str(x) for x in eqs)), '| planar', planar)
    json.dump(rep, open('pieces-report.json', 'w'), indent=1)
