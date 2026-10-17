# DICTO 2026-10-18 octet study -- STEP 26: the plane trick on the cut-down tetrahedron (T+ minus its 4 key dents and 4 phi^-2 corners).
# Convex start: T+ cut by the 4 corner planes (a truncated tetrahedron). Cut it by every face plane of the 4 keys inside it (the golden
# envelope's own face planes), exactly; drop the cells inside keys. Then sort the cells into shapes (congruence by sorted squared edges
# and volume), with named angles (golden / Penrose / 60-90). -> data/step26-tet-cells.json
import itertools, math
from exactpoly import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
R = q(S1['R']); L = [[q(x) for x in v] for v in S2['lattice']]; Tp = [[q(x) for x in v] for v in S2['Tplus']]
ip2 = qinv(qm(PHI, PHI))
PT = planes_of(Tp)
cen = [qm(qa(qa(qa(Tp[0][k], Tp[1][k]), Tp[2][k]), Tp[3][k]), qr(Fr(1, 4))) for k in range(3)]
corner_planes = []
for i, v in enumerate(Tp):
    F = [vadd(v, vmul(vsub(p, v), ip2)) for j, p in enumerate(Tp) if j != i]   # the small corner's inner face
    n = cross(vsub(F[1], F[0]), vsub(F[2], F[0])); d = dot(n, F[0])
    if sgn(qs(dot(n, v), d)) < 0: n = [qn(x) for x in n]; d = qn(d)      # orient: n.x <= d is the corner side ... we keep the other side
    corner_planes.append((n, d))                                          # n.x <= d: the side away from the vertex
base = PT + corner_planes
def lat(c):
    o = [Z, Z, Z]
    for k, Lv in zip(c, L): o = vadd(o, vmul(Lv, qr(k)))
    return o
keys = []
for K in S5['keys'].values():
    Kq = [[q(x) for x in p] for p in K]
    for c in itertools.product(range(-1, 2), repeat=3):
        t = lat(c); Kt = [vadd(p, t) for p in Kq]
        if volume(intersect(planes_of(Kt) + base)) != Z: keys.append(Kt)
cut_planes = []
for K in keys:
    for n, d in planes_of(K):
        if not any(all(qd(a, n[k0]) == qd(b, nn[k0]) for a, b in zip(n, nn)) and qd(d, n[k0]) == qd(dd, nn[k0]) for nn, dd in cut_planes for k0 in [next(k for k in range(3) if n[k] != Z)] if nn[k0] != Z):
            cut_planes.append((n, d))
cells = [base]
for n, d in cut_planes:
    new = []
    for c in cells:
        for side in ((n, d), ([qn(x) for x in n], qn(d))):
            cc = c + [side]
            if volume(intersect(cc)) != Z: new.append(cc)
    cells = new
key_planes = [planes_of(K) for K in keys]
kept = []
for c in cells:
    corners = intersect(c); v = volume(corners)
    acc = [Z, Z, Z]
    for p in corners: acc = vadd(acc, p)
    mid = vmul(acc, qr(Fr(1, len(corners))))
    if any(all(sgn(qs(dd, dot(nn, mid))) > 0 for nn, dd in kp) for kp in key_planes): continue
    kept.append((corners, v))
def sig(C):
    e = sorted(qs_(dot(vsub(C[i], C[j]), vsub(C[i], C[j]))) for i in range(len(C)) for j in range(i + 1, len(C)))
    return (len(C), tuple(e))
types = {}
for C, v in kept: types.setdefault((sig(C), qs_(v)), []).append(C)
total = Z
for C, v in kept: total = qa(total, v)
expect = q('256/81|-104/81')
NAMED = {(Fr(1, 5), Fr(0)): 'golden', (Fr(3, 8), Fr(1, 8)): 'Penrose 36/144', (Fr(3, 8), Fr(-1, 8)): 'Penrose 72/108', (Fr(1, 4), Fr(0)): '60/120', (Fr(0), Fr(0)): '90', (Fr(1, 2), Fr(0)): '45/135'}
def face_angles(C):
    Cf = np.array([[qf(x) for x in p] for p in C]); hh = ConvexHull(Cf); names = set()
    for e in np.unique(np.round(hh.equations, 9), axis=0):
        idx = [i for i in range(len(C)) if abs(Cf[i] @ e[:3] + e[3]) < 1e-9]
        for i in idx:
            for j, k in itertools.combinations([x for x in idx if x != i], 2):
                u, w = vsub(C[j], C[i]), vsub(C[k], C[i]); uw = dot(u, w)
                if sgn(qs(qm(uw, uw), qm(dot(u, u), dot(w, w)))) == 0: continue
                c2 = qd(qm(uw, uw), qm(dot(u, u), dot(w, w)))
                if c2 in NAMED: names.add(NAMED[c2])
    return sorted(names)
summary = [dict(corners=k[0][0], volume=k[1], volume_float=qf(q(k[1])), count=len(v), named_angles=face_angles(v[0])) for k, v in sorted(types.items(), key=lambda kv: -qf(q(kv[0][1])))]
checks = dict(keys_in_tet=len(keys), cut_planes=len(cut_planes), cells=len(cells), cells_outside_keys=len(kept), shapes=len(types),
              total=qs_(total), total_equals_cut_down_tet=total == expect, summary=summary)
print(json.dumps(checks, indent=1)); save('step26-tet-cells.json', dict(mark=MARK, step=26, checks=checks))
