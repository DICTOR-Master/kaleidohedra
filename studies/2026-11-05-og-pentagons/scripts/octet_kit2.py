# DICTO 5 Nov 2026: octet kit for the cut OG (rectified truncated icosahedron) with a pentagonal connector across every octahedron edge.
# Octahedra |x|+|y|+|z| <= R (R = 2 phi/3) at fcc points; across each shared edge two cut OGs show parallel pentagons -> connector = hull of both.
# Leftover = conventional cube (side 2R) minus all cut OGs and connectors; its pieces are classified by shape (congruence signature) and counted.
import json, math, itertools, numpy as np, manifold3d as m3
from fractions import Fraction as F
from scipy.spatial import ConvexHull
s5 = math.sqrt(5); phi = (1 + s5)/2; R = 2*phi/3
D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: float(F(a)) + float(F(b))*s5)(*x.split("|")) if isinstance(x, str) else float(x)
V = np.array([[q(x) for x in p] for p in D["V"]]); V -= V.mean(0); r = np.linalg.norm(V, axis=1); C = V[r < .69]; TIPS = V[r > .69]
U = TIPS/np.linalg.norm(TIPS, axis=1)[:, None]
def hull(P): P = np.asarray(P, float); return m3.Manifold.hull_points(P.tolist() if hasattr(m3.Manifold, "hull_points") else P)
def pent(c, u): return c + C[np.abs(C @ u - 0.63932) < 2e-3]
cen = [R*np.array(v, float) for v in itertools.product(range(-2, 3), repeat=3) if sum(v) % 2 == 0]   # octahedron centres (fcc), wide enough
box = m3.Manifold.cube([2*R]*3).translate([-R/2]*3)     # conventional cell, offset so no centre sits on its faces
lo = np.array([-R/2]*3); hi = lo + 2*R
near = [c for c in cen if np.all(c > lo - 1.2*R) and np.all(c < hi + 1.2*R)]
solids = []; conns = 0
for c in near: solids.append(hull(C + c))
for a, b in itertools.combinations(near, 2):
    d = b - a
    if abs(np.linalg.norm(d) - R*math.sqrt(2)) > 1e-9: continue        # neighbours sharing an edge
    e = d/np.linalg.norm(d); ua = U[np.argmax(U @ e)]; ub = U[np.argmax(U @ -e)]
    assert U[np.argmax(U @ e)] @ e > .95, "no tip points at the edge"
    solids.append(hull(np.vstack([pent(a, ua), pent(b, ub)]))); conns += 1
OG = hull(C); og_v = OG.volume(); con_v = solids[-1].volume()
# overlaps: connector vs its two OGs, connectors among themselves
U_all = m3.Manifold.batch_boolean(solids, m3.OpType.Add); tot = sum(s.volume() for s in solids)
print(f"cut OG volume {og_v:.6f}; connector volume {con_v:.6f}; pieces built {len(solids)} ({conns} connectors); overlap volume (sum - union) {tot - U_all.volume():.2e}")

def octa(c): return hull(np.array([[R,0,0],[-R,0,0],[0,R,0],[0,-R,0],[0,0,R],[0,0,-R]]) + c)
O0 = octa(np.zeros(3)); Tp = hull(np.array([[R,0,0],[0,R,0],[0,0,R],[R,R,R]])*1.0)   # tetrahedron on the (1,1,1) face of O0
T_ = hull(np.array([[R,0,0],[0,R,0],[0,0,R]]) + 0)  # placeholder
Tp = hull(np.array([[R,0,0],[0,R,0],[0,0,R],[R,R,R]]))
# true octet tetrahedron on face (1,1,1): fourth corner at (R,R,R)*(2/3)? check by volume ratio octa:tet = 4:1
print("octa/tet volume ratio", round(O0.volume()/Tp.volume(), 4))
for nm, cell in (("octahedron", O0), ("tetrahedron", Tp)):
    rest = cell - U_all; parts = rest.decompose(); cv = cell.volume()
    print(f"{nm}: volume {cv:.6f}, taken by OG+connectors {(cell ^ U_all).volume():.6f}, rest in {len(parts)} pieces:")
    ks = {}
    for p in parts:
        P = np.unique(np.round(np.array(p.to_mesh().vert_properties)[:, :3], 7), axis=0); k = (round(p.volume(), 6), len(P)); ks[k] = ks.get(k, 0) + 1
    for k, n in sorted(ks.items(), key=lambda t: -t[0][0]): print(f"   piece volume {k[0]} corners {k[1]} x{n}")
# how each connector divides between cells
c0 = solids[len(near)]; print("one connector:", round(c0.volume(), 6), "inside octahedra", round(sum((c0 ^ octa(c)).volume() for c in near), 6))
print("FINAL ok")
