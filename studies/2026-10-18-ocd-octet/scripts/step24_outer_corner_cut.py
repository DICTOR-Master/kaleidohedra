# DICTO 2026-10-18 octet study -- STEP 24: cut the outer corner (octahedron corner outside the golden envelope) into golden pieces.
# The +z axis is a 2-fold axis of the envelope (RT) through the centre of a face, so that face's plane z = h cuts off a square pyramid
# at the octahedron's corner lying wholly outside the envelope. Exact: h, the pyramid (is it the octahedron scaled by a power of phi?),
# and the rest of the outer corner below the plane, split into its convex parts (by the envelope's face planes), each tested for
# golden faces. -> data/step24-outer-corner.json
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; PR = planes_of(RT)
S1 = load('step1-ocd-exact.json'); R = q(S1['R'])
octa = [[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]; POC = planes_of(octa)
ez = [Z, Z, ONE]
zf = [(n, d) for n, d in PR if n[0] == Z and n[1] == Z and sgn(n[2]) > 0][0]; h = qd(zf[1], zf[0][2])
top = [([qn(x) for x in ez], qn(h))]                                   # z >= h
P = intersect(POC + top); vP = volume(P)
s_ = qs(R, h)                                                           # pyramid "radius"
ratio = qd(s_, R)
pw = {k: None for k in range(-6, 7)}; x = ONE
for k in range(0, 7): pw[k] = x; x = qm(x, PHI)
x = ONE
for k in range(0, -7, -1): pw[k] = x; x = qd(x, PHI)
power = [k for k, v in pw.items() if v == ratio]
# the outer corner below the plane: octahedron & z <= h & outside the envelope, near +z. Outside a convex body = union over its faces
# F of {beyond F's plane}; split by which envelope faces it lies beyond: for each face plane (n,d) with the region beyond it,
# piece_F = octa & z <= h & z >= |x|,|y| & n.x >= d & (not beyond any earlier face) -- a disjoint convex split.
cone = [([ONE, Z, qn(ONE)], Z), ([qn(ONE), Z, qn(ONE)], Z), ([Z, ONE, qn(ONE)], Z), ([Z, qn(ONE), qn(ONE)], Z)]
below = [(ez, h)]
pieces = []; done = []
for n, d in PR:
    reg = POC + below + [([qn(x_) for x_ in n], qn(d))] + done
    c = intersect(reg)
    v = volume(c) if c else Z
    if v != Z and qf(v) > 1e-12:
        cf = np.array([[qf(y) for y in p] for p in c])
        if cf[:, 2].mean() > 0.3 and np.abs(cf[:, :2]).max() < 0.75: pieces.append((n, d, c, v))
    done.append((n, d))                                                 # later pieces: not beyond this face
total_below = Z
for *_, v in pieces: total_below = qa(total_below, v)
outer = qd(qs(q(load('step2-octet-frame.json')['checks']['octa_volume']), volume(intersect(PR + POC))), qr(6))
def faces_info(c):
    Pf = np.array([[qf(y) for y in p] for p in c]); hh = ConvexHull(Pf); out = []
    for e in np.unique(np.round(hh.equations, 9), axis=0):
        idx = [i for i in range(len(c)) if abs(Pf[i] @ e[:3] + e[3]) < 1e-9]; out.append(len(idx))
    return sorted(out)
checks = dict(envelope_face_plane_z=qs_(h), pyramid_radius=qs_(s_), pyramid_over_octa=qs_(ratio), pyramid_is_octa_scaled_by_phi_power=power,
              pyramid_volume=qs_(vP), pyramid_float=qf(vP), outer_corner=qs_(outer), outer_float=qf(outer),
              below_pieces=[dict(volume=qs_(v), float=qf(v), corners=len(c), face_sizes=faces_info(c)) for n, d, c, v in pieces],
              below_total=qs_(total_below), pyramid_plus_below_equals_outer=qa(vP, total_below) == outer)
print(json.dumps(checks, indent=1))
save('step24-outer-corner.json', dict(mark=MARK, step=24, checks=checks, pieces=[[[qs_(y) for y in p] for p in c] for *_, c, _ in [(None, None, c, v) for n, d, c, v in pieces]]))
