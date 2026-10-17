# DICTO 2026-10-18 bcc golden kit -- STEP 4: the facing five-fold stars of two envelopes (RT) at third neighbours, seen down the axis,
# and an exact search for a Penrose link: is the sideways offset d of the two five-fold corners a short golden combination of the stars'
# own spoke/tip vectors (as in the octet, where d = (two spokes)/phi gave a thick Penrose rhombus)? -> data/step4-stars.json (+2D)
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]
S3 = load('step3-keys.json')['checks']; f0 = S3['facing_fivefold_pairs'][0]; t = [q(x) for x in f0['t']]
nn2 = lambda v: min((dot(vsub(v, u), vsub(v, u)) for u in RT if u != v), key=qf)
five = [v for v in RT if sum(1 for u in RT if u != v and dot(vsub(v, u), vsub(v, u)) == nn2(v)) == 5]
c1 = next(v for v in five if any(all(a == b for a, b in zip(vsub(t, v), vsub(t, u))) and qf(dot(vsub(vsub(t, v), v), vsub(vsub(t, v), v))) < 0.4 for u in five))
c2 = vsub(t, c1); a = c1; aa = dot(a, a); P = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
e2 = nn2(c1); spokes_pts = [u for u in RT if u != c1 and dot(vsub(c1, u), vsub(c1, u)) == e2]
faces = [(n, d) for n, d in planes_of(RT) if dot(n, c1) == d]
tips_pts = []
for n, d in faces:
    on = [u for u in RT if dot(n, u) == d]; far = [u for u in on if u != c1 and u not in spokes_pts]; tips_pts += far
spk = [P(vsub(u, c1)) for u in spokes_pts]; tps = [P(vsub(u, c1)) for u in tips_pts]
dvec = P(vsub(c2, c1)); along = qd(dot(vsub(c2, c1), a), aa)
pw = {}; x = ONE
for k in range(0, 5): pw[k] = x; x = qm(x, PHI)
x = ONE
for k in range(0, -5, -1): pw[k] = x; x = qd(x, PHI)
vecs = [('spoke', i, v) for i, v in enumerate(spk)] + [('tip', i, v) for i, v in enumerate(tps)]
found = []
for (n1, i1, v1), (n2, i2, v2) in itertools.combinations_with_replacement(vecs, 2):
    for k1, k2 in itertools.product(range(-4, 5), repeat=2):
        for s1, s2 in itertools.product((1, -1), repeat=2):
            w = vadd(vmul(v1, pw[k1] if s1 > 0 else qn(pw[k1])), vmul(v2, pw[k2] if s2 > 0 else qn(pw[k2])))
            if all(p == q_ for p, q_ in zip(w, dvec)): found.append(f'{"+" if s1 > 0 else "-"}phi^{k1} {n1}{i1} {"+" if s2 > 0 else "-"}phi^{k2} {n2}{i2}')
single = [f'phi^{k} {n}{i}' for (n, i, v) in vecs for k in range(-4, 5) for s in (1, -1) if all(p == q_ for p, q_ in zip(vmul(v, pw[k] if s > 0 else qn(pw[k])), dvec))]
r_sp = qf(dot(spk[0], spk[0])) ** .5; r_tp = qf(dot(tps[0], tps[0])) ** .5; r_d = qf(dot(dvec, dvec)) ** .5
checks = dict(spokes=len(spk), tips=len(tps), spoke_radius=r_sp, tip_radius=r_tp, offset_sideways=r_d, offset_along=qf(along) * qf(aa) ** .5,
              offset_over_tip_radius=r_d / r_tp, offset_over_spoke_radius=r_d / r_sp, d_is_single_scaled_vector=single, d_as_two_scaled_vectors=found[:12])
print(json.dumps(checks, indent=1))
af = np.array([qf(x_) for x_ in a]); af /= np.linalg.norm(af); ub = np.cross(af, [1, 0, 0]); ub /= np.linalg.norm(ub); wb = np.cross(af, ub)
f2 = lambda v: [float(np.array([qf(x_) for x_ in v]) @ ub), float(np.array([qf(x_) for x_ in v]) @ wb)]
star1 = []; star2 = []
for n, d in faces:
    on = [u for u in RT if dot(n, u) == d]; cf = np.array([f2(vsub(u, c1)) for u in on]); cc = cf.mean(0)
    order = np.argsort(np.arctan2(cf[:, 1] - cc[1], cf[:, 0] - cc[0])); star1.append([cf[i].tolist() for i in order])
    cf2 = np.array([f2(vsub(vsub(t, u), c1)) for u in on]); cc2 = cf2.mean(0); o2 = np.argsort(np.arctan2(cf2[:, 1] - cc2[1], cf2[:, 0] - cc2[0])); star2.append([cf2[i].tolist() for i in o2])
save('step4-stars.json', dict(mark=MARK, step=4, checks=checks, star1=star1, star2=star2, c2=f2(dvec)))
