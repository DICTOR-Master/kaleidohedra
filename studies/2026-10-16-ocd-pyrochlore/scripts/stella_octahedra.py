# OCD Stella + octahedra (DICTO 2026-10-16: "it would also fill well with an octahedron of some kind, perhaps utilising the stella"). Float.
# The octahedron whose 8 faces lie in a site's 8 joint walls (the cell's hexagon planes) meets every joint neighbour flat. Its 6 tips pass the
# square walls (each 1/48 of the cell beyond each wall; octahedron = 9/8 of the cell). Arrangements on the OCD's bcc packing (simple cubic
# sublattice A = Z³-type sites, B = the body centres):
#  (1) octahedra on A, OCD Stellas on B: tips meet tips -> cut to the cell = truncated octahedron (no longer an octahedron).
#  (2) octahedra on A-even (NaCl colouring of A), OCD Stellas elsewhere: every tip enters an OCD Stella's cell on A-odd; those Stellas are notched
#      by the tips (6 square-pyramid notches), the B Stellas are whole.  -> data/stella-octahedra.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
D = json.load(open('data/stella-cut-exact.json')); S = np.array(D['S']['v']); C = np.array(D['cell']['v'])
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
def vol_h(H):
    A, b = H[:, :3], -H[:, 3]; nr = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if not r.success or r.x[3] < 1e-9: return 0.0
    return ConvexHull(HalfspaceIntersection(H, r.x[:3]).intersections).volume
HC = planes(C); vC = ConvexHull(C).volume; vS = ConvexHull(S).volume; HS = planes(S)
hexw = np.array([e for e in HC if sum(abs(C @ e[:3] + e[3]) < 1e-7) == 6]); sqw = np.array([e for e in HC if sum(abs(C @ e[:3] + e[3]) < 1e-7) == 4])
Oct = hexw; vO = vol_h(Oct)
out = ['DICTO · dictospheres.com', 'OCD Stella + octahedra (float)', f'cell {vC:.6f}; OCD Stella {vS:.6f} ({vS / vC:.4%}); joint-wall octahedron {vO:.6f} = {vO / vC:.4f} × cell',
       f'  hexagon walls {len(hexw)}, square walls {len(sqw)}']
tip = vol_h(np.vstack([Oct, -sqw[0][None, :] * np.r_[1, 1, 1, 1]]))   # one tip beyond one square wall: inside Oct, outside the cell's square plane
out.append(f'  one tip beyond a square wall: {tip:.6f} = 1/{vC / tip:.2f} of the cell')
# (1)
out.append(f'(1) octahedra on A cut to the cell (= the cell): fill (vS + vC)/(2 vC) = {(vS + vC) / (2 * vC):.4%}; partner is the truncated octahedron itself')
# (2) a tip from the neighbour across square wall w: the neighbour's octahedron, shifted by 2 * (distance to the wall) along the wall normal
notch = 0.0
for w in sqw:
    n = w[:3] / np.linalg.norm(w[:3]); dist = -w[3] / np.linalg.norm(w[:3]); s = 2 * dist * n
    Osh = Oct.copy(); Osh[:, 3] = Oct[:, 3] - Oct[:, :3] @ s        # octahedron at the neighbour site
    notch += vol_h(np.vstack([HS, Osh]))
vSn = vS - notch
f2 = (vO + vSn + 2 * vS) / (4 * vC)
out.append(f'(2) octahedra on A-even, OCD Stellas on A-odd (notched by 6 tips) and on B (whole):')
out.append(f'    notched Stella volume {vSn:.6f} (notches {notch:.6f}, {notch / vS:.2%} of the Stella); octahedron {vO:.6f}')
out.append(f'    per 4 sites: 1 octahedron + 1 notched Stella + 2 Stellas = {vO + vSn + 2 * vS:.6f} of 4 cells {4 * vC:.6f}: fill {f2:.4%}')
out.append(f'    the octahedron overlaps nothing else: its tips enter only the notched Stellas\' cells, and its faces lie on the joint walls')
print('\n'.join(out)); open('data/stella-octahedra.txt', 'w').write('\n'.join(out) + '\n')
