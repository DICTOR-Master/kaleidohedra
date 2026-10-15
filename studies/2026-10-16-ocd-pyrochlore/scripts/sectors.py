# Step 13b (DICTO: "the key may be icosa or dodeca based"). The shell between the OCD and its dual nesting Hecatodihedron
# (scale 4/9, all 102 faces through OCD corners) sliced by the solids' own frame: 20 icosahedral sectors (cones over an
# icosahedron's faces, centred on the 3-fold axes: the OCD hexagons) and 12 dodecahedral sectors (cones over a dodecahedron's
# faces, centred on the 5-fold axes: the OCD's outer corners, the Heca pentagons). Float, with the sum check.
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, '../_lib'); import geomcheck as gc
O = np.array(json.load(open('data/network.json'))['ocd']); r = np.linalg.norm(O, axis=1); ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9])
EO = ConvexHull(O).equations; pl = []
for e in EO:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
Hc = np.array([e[:3] / -e[3] for e in pl]) * (4 / 9)              # the dual nesting Hecatodihedron
EH = ConvexHull(Hc).equations
def meet(hs):
    A = np.array(hs); nrm = np.linalg.norm(A[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], nrm], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if rr.status != 0 or rr.x[3] < 1e-9: return 0.0
    X = HalfspaceIntersection(A, rr.x[:3]).intersections
    try: return ConvexHull(X).volume
    except Exception: return 0.0
shell_v = ConvexHull(Hc).volume - ConvexHull(O).volume
def cone_hs(P):   # the cone from the centre over the convex spherical polygon with corner directions P (ordered), as n.x <= 0
    c = P.mean(0); hs = []
    for i in range(len(P)):
        m = np.cross(P[i], P[(i + 1) % len(P)]); m = m if m @ c > 0 else -m; hs.append(np.r_[-m, 0.0])
    return hs
def order(P, c):
    u = c / np.linalg.norm(c); a = P[0] - (P[0] @ u) * u; a /= np.linalg.norm(a); b = np.cross(u, a)
    return P[np.argsort(np.arctan2(P @ b, P @ a))]
I5 = ax['5']; D3 = ax['3']
ifaces = [order(I5[list(t)], I5[list(t)].sum(0)) for t in itertools.combinations(range(12), 3) if all(I5[a] @ I5[b] > 0.4 for a, b in itertools.combinations(t, 2))]
dfaces = [order(D3[[j for j in range(20) if D3[j] @ v > 0.79]], v) for v in I5]
assert len(ifaces) == 20 and len(dfaces) == 12 and all(len(f) == 5 for f in dfaces)
# the shell inside a sector = sector cone ∩ Heca ∩ outside the OCD; outside the OCD is not convex, so: sector ∩ Heca minus sector ∩ OCD
def sector_shell(F):
    hs = cone_hs(F); return meet(hs + list(EH)) - meet(hs + list(EO))
iv = [sector_shell(F) for F in ifaces]; dv = [sector_shell(F) for F in dfaces]
phi = (1 + 5 ** .5) / 2
out = [f'shell (Heca - OCD) = {shell_v:.6f}',
       f'20 icosahedral sectors (on the hexagons): each {np.mean(iv):.6f} (spread {np.ptp(iv):.1e}); sum {sum(iv):.6f}; sum check {abs(sum(iv) - shell_v) < 1e-7}',
       f'12 dodecahedral sectors (on the pentagons): each {np.mean(dv):.6f} (spread {np.ptp(dv):.1e}); sum {sum(dv):.6f}; sum check {abs(sum(dv) - shell_v) < 1e-7}',
       f'dodecahedral sector / icosahedral sector = {np.mean(dv) / np.mean(iv):.6f} (5/3 = 1.666667 for equal shares; log_phi of the ratio {np.log(np.mean(dv) / np.mean(iv)) / np.log(phi):.4f})']
# what the OCD itself puts in each sector, for comparison (the I-D split of the solid)
io = [meet(cone_hs(F) + list(EO)) for F in ifaces]; do = [meet(cone_hs(F) + list(EO)) for F in dfaces]
ih = [meet(cone_hs(F) + list(EH)) for F in ifaces]; dh = [meet(cone_hs(F) + list(EH)) for F in dfaces]
out.append(f'OCD per sector: icosahedral {np.mean(io):.6f}, dodecahedral {np.mean(do):.6f}; Heca per sector: icosahedral {np.mean(ih):.6f}, dodecahedral {np.mean(dh):.6f}')
out.append(f'shell share of each sector: icosahedral {np.mean(iv) / np.mean(ih):.6f}, dodecahedral {np.mean(dv) / np.mean(dh):.6f}')
print('\n'.join(out)); open('data/sectors.txt', 'w').write('\n'.join(out) + '\n')
