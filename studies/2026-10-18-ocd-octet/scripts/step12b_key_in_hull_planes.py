# DICTO 2026-10-18 octet study -- STEP 12b: exact check of a step-12 coincidence: do key faces lie exactly in star-hull planes
# (of any of the 12 facing-star hulls round either OCD)?
from exactpoly import *
S1 = load('step1-ocd-exact.json'); S5 = load('step5-keyed-octet.json')
V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
i1 = [i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]; o = [Z, R, R]
def sgnv(c): return [R if sgn(x) > 0 else (qn(R) if sgn(x) < 0 else Z) for x in c]
PH = []
for i in five:
    oo = sgnv(V[i]); st = [V[j] for j in sorted({j for f in S1['faces'] if i in f for j in f})]
    for c in ([Z, Z, Z], o): PH += shift(planes_of(st + [vsub(oo, p) for p in st]), c)
def same_plane(a, b):
    (n1, d1), (n2, d2) = a, b
    cr = cross(n1, n2)
    if any(x != Z for x in cr): return False
    k = next(i for i in range(3) if n1[i] != Z); t = qd(n2[k], n1[k]); return qm(d1, t) == d2
hits = {}
for k, K in S5['keys'].items():
    for lab, t in (('ocd1', [Z, Z, Z]), ('ocd2', o)):
        for kp in shift(planes_of([[q(x) for x in p] for p in K]), t):
            if any(same_plane(kp, hp) for hp in PH): hits[f'{lab} {k}'] = hits.get(f'{lab} {k}', 0) + 1
print('key faces lying exactly in star-hull planes:', hits)
save('step12b-key-hull-planes.json', dict(mark=MARK, step='12b', key_faces_in_hull_planes=hits))
