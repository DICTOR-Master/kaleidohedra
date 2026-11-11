"""Does the 600-cell's corner set carry the One World's nesting? (DICTO 11 Nov, after reading One World: "no improvements possible due
to most recent discoveries?") In the 600-cell (edge 1 after scaling): find the hidden dodecahedra (edge d), the cubes whose 8 corners
are corners of one such dodecahedron (Euclid XIII.17: edge phi d), the tetrahedra inside those cubes (edge phi sqrt2 d), and the
icosahedra and octahedra concentric with a dodecahedron; report edge ratios exactly-recognised and counts."""
import sys, numpy as np, sympy as sp
from scipy.spatial import cKDTree
sys.argv = ['x', 'H4']
exec(open('inhabitance.py').read().split('res = {}; t00')[0])
phi = (1 + 5 ** .5) / 2
R, bonds = chain_any(list(GR['H4'])); Rm = np.array(R); G = group(R)
x = np.linalg.solve(Rm, np.array((0, 0, 0, 1), float)); P = dedupe(G @ x); tree = cKDTree(P)
e = np.linalg.norm(P - P[0], axis=1); e = e[e > 1e-9].min(); P = P / e; tree = cKDTree(P)
H = hidden(P, tree)
def edge(S): Q = P[list(S)]; d = np.linalg.norm(Q[:, None] - Q[None], axis=2); return d[d > 1e-9].min()
def rec(v): return sp.nsimplify(v, [sp.sqrt(5), sp.sqrt(2)], tolerance=1e-7)
Ds = list(H['D']); Cs = list(H['C']); Ts = list(H['T']); Is = list(H['I']); Os = list(H['O'])
print('through corner 0: D', len(Ds), 'C', len(Cs), 'T', len(Ts), 'I', len(Is), 'O', len(Os))
print('edges D', sorted({str(rec(edge(s))) for s in Ds}), 'C', sorted({str(rec(edge(s))) for s in Cs}), 'I', sorted({str(rec(edge(s))) for s in Is}))
cen = lambda S: P[list(S)].mean(0)
for D in Ds:
    dE = edge(D); cubes = [C for C in Cs if C <= D]; tets = [T for T in Ts if any(T <= C for C in cubes)]
    ico = [I for I in Is if np.linalg.norm(cen(I) - cen(D)) < 1e-7]; octs = [O for O in Os if np.linalg.norm(cen(O) - cen(D)) < 1e-7]
    print(f'dodecahedron edge {rec(dE)}: Euclid cubes inside {len(cubes)} (edge/dE {rec(edge(cubes[0]) / dE) if cubes else "-"}), tetrahedra in them {len(tets)} '
          f'(edge/dE {rec(edge(tets[0]) / dE) if tets else "-"}); concentric icosahedra {len(ico)} (edge/dE {sorted({str(rec(edge(i) / dE)) for i in ico})}), '
          f'concentric octahedra {len(octs)} (edge/dE {sorted({str(rec(edge(o) / dE)) for o in octs})})')
    break
