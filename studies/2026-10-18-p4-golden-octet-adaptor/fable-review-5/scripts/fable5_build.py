# Fable review 5, PHASE 2 (2026-10-18): geometry of the continuous creased-kite relief on the star-centred W, exactly as drawn in
# fable5_drawing.py. For each of the 8 flat faces (own frame: A = OCD centre at the origin, u along A->E, w toward T, n outward) the
# relief height h(u,w) = heights(row) * d(rho) * fade(u,w): kite rows parallel to the seam A->E with a row axis on it, roofs/troughs
# alternating by row, d(rho) 2.0 mm at the socket rim fading to 1.1 mm (60 mm octahedron edge), fade to zero within 2.4 mm of the two
# oblique edges A-T and E-T. Bump faces (A0E0T+-, A1E1T+-) use +h, dent faces (A0E1T+-, A1E0T+-) use -h (= the g^-1 / sigma / iota
# images, proved in fable-review-4). Output: data/relief-geometry.json (clipped relief triangles in 3D per face, frames, parameters).
import sys, os, json, math, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', '..', 'fable-review-3', 'scripts'))
from fable3_engine import *
from fable3_engine import loadS, f3, qv, hull_poly, Poly
from q5 import *
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; OCD = hull_poly(V, 'OCD'); Vf = np.array([f3(v) for v in V]); R = qf(q(S1['R']))
G = json.load(open(os.path.join(H, '..', 'data', 'continuous-kites.json'))); K = G['kite']; a, b, D, s, xs = K['long_edge'], K['short_edge'], K['long_diagonal'], K['half_short_diagonal'], math.sqrt(K['short_edge'] ** 2 - K['half_short_diagonal'] ** 2)
scale_mm = 60.0 / (R * math.sqrt(2)); D_RIM, D_FAR, RHO_RIM, RHO_FAR, FADE = 2.0 / scale_mm, 1.1 / scale_mm, 0.667, 0.95, 2.4 / scale_mm
m = np.array([0, R / 2, R / 2]); A0, A1, E0, E1, Tp, Tm = np.zeros(3), np.array([0, R, R]), np.array([0, R, 0]), np.array([0, 0, R]), np.array([R / 2, R / 2, R / 2]), np.array([-R / 2, R / 2, R / 2])
faces = {'1': (A0, E0, Tp, +1), '0': (A0, E0, Tm, +1), '7': (A1, E1, Tm, +1), '6': (A1, E1, Tp, +1), '3': (A0, E1, Tp, -1), '2': (A0, E1, Tm, -1), '5': (A1, E0, Tm, -1), '4': (A1, E0, Tp, -1)}
def frame(A, E, T):
    U = (E - A) / np.linalg.norm(E - A); Wv = (T - A) - ((T - A) @ U) * U; Wv /= np.linalg.norm(Wv); N = np.cross(U, Wv)
    if (m - A) @ N > 0: N = -N
    return U, Wv, N
tri2 = np.array([[0, 0], [R, 0], [R / 2, R / math.sqrt(2)]])     # the face triangle in every face frame (all 8 faces congruent)
# --- the tiling and heights (as in the drawing)
K0 = np.array([[D, 0], [xs, s], [0, 0], [xs, -s]])
def kite(j, kk): return K0 + np.array([kk * D, j * s]) if j % 2 == 0 else np.array([kk * D + xs, j * s]) - K0
def row_sign(j): return 0.0 if j == 0 else (1 if j % 2 == 1 else -1) * (1 if j > 0 else -1)
def depth(pt):
    rho = math.hypot(pt[0], pt[1]); f = min(1.0, max(0.0, (rho - RHO_RIM) / (RHO_FAR - RHO_RIM))); return D_RIM + (D_FAR - D_RIM) * f
def dist_seg(pt, a_, b_):
    t = max(0.0, min(1.0, ((pt[0] - a_[0]) * (b_[0] - a_[0]) + (pt[1] - a_[1]) * (b_[1] - a_[1])) / ((b_[0] - a_[0]) ** 2 + (b_[1] - a_[1]) ** 2)))
    return math.hypot(pt[0] - a_[0] - t * (b_[0] - a_[0]), pt[1] - a_[1] - t * (b_[1] - a_[1]))
def fade(pt): return min(1.0, dist_seg(pt, tri2[0], tri2[2]) / FADE, dist_seg(pt, tri2[1], tri2[2]) / FADE)
def vertex_height(pt, j):
    """pre-fade height of a tiling vertex on row level j (w = j s): sign * d(rho) / 2"""
    return row_sign(j) * depth(pt) / 2
def clip(poly, conv):
    out = [tuple(pp) for pp in poly]
    for i in range(len(conv)):
        A_, B_ = conv[i], conv[(i + 1) % len(conv)]; inp = out; out = []
        if not inp: break
        side = lambda pt: (B_[0] - A_[0]) * (pt[1] - A_[1]) - (B_[1] - A_[1]) * (pt[0] - A_[0])
        for n_ in range(len(inp)):
            cur, prev = inp[n_], inp[n_ - 1]; sc, sp = side(cur), side(prev)
            if sc >= 0:
                if sp < 0: t = sp / (sp - sc); out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
                out.append(cur)
            elif sp >= 0: t = sp / (sp - sc); out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
    return out
def plane_height(tri3, pt):
    """height at pt from the plane through 3 (u, w, h) points (barycentric)"""
    (x1, y1, h1), (x2, y2, h2), (x3, y3, h3) = tri3; det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    l1 = ((y2 - y3) * (pt[0] - x3) + (x3 - x2) * (pt[1] - y3)) / det; l2 = ((y3 - y1) * (pt[0] - x3) + (x1 - x3) * (pt[1] - y3)) / det; return l1 * h1 + l2 * h2 + (1 - l1 - l2) * h3
# relief triangles in the face frame: each kite -> 2 triangles creased along the long diagonal (nose, tail, side)
rel = []
for j in range(-2, 10):
    for kk in range(-3, 6):
        Kj = kite(j, kk); nose, up, tail, dn = Kj
        for side_pt in (up, dn):
            jside = int(round(side_pt[1] / s))                      # the side corner lies on the axis level of the neighbouring row
            T3 = [(nose[0], nose[1], vertex_height(nose, j)), (tail[0], tail[1], vertex_height(tail, j)), (side_pt[0], side_pt[1], vertex_height(side_pt, jside))]
            c = clip([nose, tail, side_pt], tri2)
            if len(c) < 3: continue
            area = abs(sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c))) / 2)
            if area < 1e-9: continue
            pts = [(pt[0], pt[1], plane_height(T3, pt) * fade(pt)) for pt in c]
            for i in range(1, len(pts) - 1): rel.append([pts[0], pts[i], pts[i + 1]])
# sanity: max |h|, heights zero on the triangle boundary
maxh = max(abs(p_[2]) for t_ in rel for p_ in t_)
bnd = [abs(p_[2]) for t_ in rel for p_ in t_ if abs(p_[1]) < 1e-9 or abs(dist_seg(p_[:2], tri2[0], tri2[2])) < 1e-9 or abs(dist_seg(p_[:2], tri2[1], tri2[2])) < 1e-9]
out = dict(mark='DICTO · dictospheres.com', R=R, m=m.tolist(), cell=[A0.tolist(), A1.tolist(), E0.tolist(), E1.tolist(), Tp.tolist(), Tm.tolist()], scale_mm=scale_mm,
           params=dict(d_rim_mm=D_RIM * scale_mm, d_far_mm=D_FAR * scale_mm, rho_rim=RHO_RIM, rho_far=RHO_FAR, fade_mm=FADE * scale_mm, row_spacing=s, kite_length=D, kite_long_edge=a, kite_short_edge=b, xs=xs),
           relief_triangles_uvh=rel, max_height=maxh, max_height_mm=maxh * scale_mm, boundary_heights_max=max(bnd) if bnd else 0.0, n_triangles=len(rel), faces={}, ocd_V=Vf.tolist())
for name, (A, E, T, sign) in faces.items():
    U, Wv, N = frame(A, E, T); out['faces'][name] = dict(A=A.tolist(), E=E.tolist(), T=T.tolist(), U=U.tolist(), W=Wv.tolist(), N=N.tolist(), sign=sign)
    assert abs(np.linalg.norm(E - A) - R) < 1e-12 and abs((T - A) @ Wv - R / math.sqrt(2)) < 1e-9 and abs((T - A) @ U - R / 2) < 1e-9
json.dump(out, open(os.path.join(H, '..', 'data', 'relief-geometry.json'), 'w'))
print('triangles', len(rel), 'max |h| mm', round(maxh * scale_mm, 3), 'boundary max |h|', out['boundary_heights_max'], 'faces', {k: v['sign'] for k, v in out['faces'].items()})
