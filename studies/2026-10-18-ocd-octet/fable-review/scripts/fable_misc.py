# Fable review 2026-10-18 -- small exact side checks: (1) angle-sum audit of the step-12 face lists (a planar n-gon's interior
# angles must sum to (n-2)*180); (2) the key's side faces as half golden rhombi, exactly; (3) the shape of the middle hull H
# (face sizes, the two tip pentagons, the shear between them). -> data/fable-misc.json
import sys, os, json, math, itertools, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.join(HERE, '..', '..'); sys.path.insert(0, os.path.join(STUDY, 'scripts')); sys.path.insert(0, HERE)
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z, MARK
OUT = {}
# (1) step-12 angle sums
S12 = json.load(open(os.path.join(STUDY, 'data', 'step12-faces.json')))
def deg(s):
    try: return float(s.split()[-1])
    except Exception: return None
audit = {}
for piece, faces in S12['pieces'].items():
    bad = []; n_ok = 0; n_tested = 0
    for f in faces:
        angs = f.get('angles')
        if not angs or len(angs) < 3: continue
        vals = [deg(a) for a in angs]
        if any(v is None for v in vals): continue
        n_tested += 1; tot = sum(vals); expect = (len(vals) - 2) * 180
        if abs(tot - expect) > 0.05: bad.append(dict(source=f.get('source'), angles=angs, sum=round(tot, 2), expected=expect))
        else: n_ok += 1
    audit[piece] = dict(faces_with_angles=n_tested, angle_sum_ok=n_ok, angle_sum_wrong=len(bad), examples=bad[:6])
OUT['step12_angle_sum_audit'] = audit
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'examples'} for k, v in audit.items()}, indent=1))
# (2) key side faces: triangle apex + 2 base corners; exact squared edges and cos of angles
S3 = json.load(open(os.path.join(STUDY, 'data', 'step3-key-candidate.json'))); K = [[q(x) for x in p] for p in S3['key']]; apex, base = K[0], K[1:]
def cos_exact(u, w):   # returns (cos^2 exact, sign) and float degrees
    uw = dot(u, w); c2 = qd(qm(uw, uw), qm(dot(u, u), dot(w, w))); return qs_(c2), sgn(uw), math.degrees(math.acos(max(-1, min(1, qf(uw) / math.sqrt(qf(dot(u, u)) * qf(dot(w, w)))))))
tri = [apex, base[0], base[1]]
e2 = [dot(vsub(tri[(i + 1) % 3], tri[i]), vsub(tri[(i + 1) % 3], tri[i])) for i in range(3)]
angs = [cos_exact(vsub(tri[i - 1], tri[i]), vsub(tri[(i + 1) % 3], tri[i])) for i in range(3)]
OUT['key_side_face'] = dict(edges2=[qs_(e) for e in e2], angles_deg=[round(a[2], 3) for a in angs], cos2_exact=[a[0] for a in angs],
                            apex_sides_equal=e2[0] == e2[2], apex_cos2_is_1_over_5=angs[0][0] == qs_((Fr(1, 5), Fr(0))) and angs[0][1] < 0,
                            note='half golden rhombus cut along its long diagonal has angles 116.57 (cos^2 = 1/5, cos < 0) and 31.72, 31.72')
base_e2 = [dot(vsub(base[(i + 1) % 3], base[i]), vsub(base[(i + 1) % 3], base[i])) for i in range(3)]
OUT['key_base_equilateral'] = len({qs_(e) for e in base_e2}) == 1
print('key side face', OUT['key_side_face']['angles_deg'])
# (3) the middle hull H
from scipy.spatial import ConvexHull
S1 = json.load(open(os.path.join(STUDY, 'data', 'step1-ocd-exact.json'))); V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R']); faces = S1['faces']
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
i1 = [i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]; c1 = V[i1]; o = [Z, R, R]; c2 = vsub(o, c1)
star = [V[j] for j in sorted({j for f in faces if i1 in f for j in f})]; Hp = star + [vsub(o, p) for p in star]
Hf = np.array([[qf(x) for x in p] for p in Hp]); h = ConvexHull(Hf)
hull_idx = sorted(set(h.vertices)); OUT['H_hull_corners'] = len(hull_idx)
a = c1; aa = dot(a, a); proj = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
rel = [proj(vsub(p, c1)) for p in star]; rr = [dot(t, t) for t in rel]; rt = max(rr, key=qf)
tips1 = [p for p, x in zip(star, rr) if x == rt]; tips2 = [vsub(o, p) for p in tips1]
OUT['H_corners_are_the_10_tips'] = sorted(tuple(Hp[i]) for i in hull_idx) == sorted(tuple(p) for p in tips1 + tips2)
# face sizes: exact planes, corners on each
planes = []
for s_ in h.simplices:
    A, B, C = Hp[s_[0]], Hp[s_[1]], Hp[s_[2]]; n = cross(vsub(B, A), vsub(C, A)); d = dot(n, A)
    if all(x == Z for x in n): continue
    if any(sgn(qs(dot(n, p), d)) > 0 for p in Hp): n = [qn(x) for x in n]; d = qn(d)      # orient outward before deduping
    key = None
    for (n2, d2) in planes:
        if all(x == Z for x in cross(n, n2)) and sgn(dot(n, n2)) > 0 and all(qm(d, n2[i]) == qm(d2, n[i]) for i in range(3)): key = 1; break
    if key is None: planes.append((n, d))
sizes = sorted(sum(1 for i in hull_idx if dot(n, Hp[i]) == d) for n, d in planes)
OUT['H_faces'] = len(planes); OUT['H_face_sizes'] = sizes
# the two tip pentagons: perpendicular to the axis? (all tips of star 1 have the same a-component)
ax1 = {qs_(dot(p, a)) for p in tips1}; ax2 = {qs_(dot(p, a)) for p in tips2}
OUT['tip_pentagons_perpendicular_to_axis'] = len(ax1) == 1 and len(ax2) == 1
# regular pentagon? equal edges round the ring
tf = np.array([[qf(x) for x in p] for p in tips1]); cen = tf.mean(0); u = tf[0] - cen; w = np.cross(np.array([qf(x) for x in a]), u)
order = np.argsort(np.arctan2((tf - cen) @ w, (tf - cen) @ u)); ring = [tips1[i] for i in order]
edges = {qs_(dot(vsub(ring[(i + 1) % 5], ring[i]), vsub(ring[(i + 1) % 5], ring[i]))) for i in range(5)}
OUT['tip_pentagon_regular'] = len(edges) == 1
# axial height between the pentagons and the sideways shift of their centres (= tip radius?)
cen1 = [qm(sum((p[k] for p in tips1), Z) if False else qa(qa(qa(qa(tips1[0][k], tips1[1][k]), tips1[2][k]), tips1[3][k]), tips1[4][k]), qr(Fr(1, 5))) for k in range(3)]
cen2 = vsub(o, cen1); dv = vsub(cen2, cen1); axial = qd(dot(dv, a), aa); side = proj(dv)
OUT['pentagon_centres_axial_gap'] = qf(axial) * math.sqrt(qf(aa)); OUT['pentagon_centres_sideways_shift'] = math.sqrt(qf(dot(side, side)))
OUT['pentagon_circumradius'] = math.sqrt(qf(rt)); OUT['sideways_shift_equals_circumradius_exact'] = dot(side, side) == rt
OUT['tip_pentagon_edge'] = math.sqrt(qf(list(edges)[0].split('|') and dot(vsub(ring[1], ring[0]), vsub(ring[1], ring[0]))))
OUT['axial_gap_equals_sideways_shift_exact'] = qm(qm(dot(dv, a), dot(dv, a)), qinv(aa)) == rt      # (dv.a)^2/|a|^2 == r_tip^2
OUT['corner_to_tip_axial_drop'] = qf(qd(dot(vsub(c1, tips1[0]), a), aa)) * math.sqrt(qf(aa)); OUT['c1_c2_axial'] = qf(qd(dot(vsub(c1, c2), a), aa)) * math.sqrt(qf(aa))
OUT['note'] = 'ring 2 = point reflection of ring 1 through m: in projection a half turn, which for a regular pentagon equals a 36-degree turn'
print(json.dumps({k: v for k, v in OUT.items() if k != 'step12_angle_sum_audit'}, indent=1, default=str))
OUT['mark'] = MARK; json.dump(OUT, open(os.path.join(HERE, '..', 'data', 'fable-misc.json'), 'w'), indent=1, ensure_ascii=False)
