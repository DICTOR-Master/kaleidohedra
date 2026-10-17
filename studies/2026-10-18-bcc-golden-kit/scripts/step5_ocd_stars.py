# DICTO 2026-10-18 bcc golden kit -- STEP 5 (option 2): the OCD's own five-fold corners (inside the envelopes) at the same facing third
# neighbours. The sideways offset is the same as for the envelope corners (both corners lie on the same axis), so test it against the
# OCD's five-kite star: inner corners, tips, and their phi-scaled pairs (exact). -> data/step5-ocd-stars.json
import itertools
from exactpoly import *
S1 = json.load(open(os.path.join(HERE, '..', '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
V = [[q(x) for x in v] for v in S1['V']]
S3 = load('step3-keys.json')['checks']; t = [q(x) for x in S3['facing_fivefold_pairs'][0]['t']]
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
pairs = [(i, j) for i in five for j in five if all(a == b for a, b in zip(vsub(t, V[i]), V[j])) is False and False]
# corner c1 of the OCD at 0 facing the OCD at t: the five-fold corner whose antiparallel copy t - c1 is a five-fold corner of the neighbour
cand = [i for i in five if any(all(a == b for a, b in zip(vsub(t, V[i]), vsub(t, V[j]))) for j in five) and any(all(a == b for a, b in zip([qn(x) for x in V[i]], V[j])) for j in five)]
best = min(cand, key=lambda i: qf(dot(vsub(vsub(t, V[i]), V[i]), vsub(vsub(t, V[i]), V[i]))))
c1 = V[best]; c2 = vsub(t, c1); a = c1; aa = dot(a, a); P = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
star = sorted({j for f in S1['faces'] if best in f for j in f}); rel = [P(vsub(V[j], c1)) for j in star if j != best]
rr = [dot(x, x) for x in rel]; rt = max(rr, key=qf); ri = min(rr, key=qf)
tips = [x for x, y in zip(rel, rr) if y == rt]; inner = [x for x, y in zip(rel, rr) if y == ri]
dvec = P(vsub(c2, c1)); along = qd(dot(vsub(c2, c1), a), aa)
pw = {0: ONE}
for k in range(1, 6): pw[k] = qm(pw[k - 1], PHI); pw[-k] = qd(pw[-(k - 1)], PHI)
vecs = [('tip', i, v) for i, v in enumerate(tips)] + [('inner', i, v) for i, v in enumerate(inner)]
eq = lambda w: all(p == q_ for p, q_ in zip(w, dvec))
single = [f'{s}phi^{k} {n}{i}' for (n, i, v) in vecs for k in range(-5, 6) for s in ('+', '-') if eq(vmul(v, pw[k] if s == '+' else qn(pw[k])))]
two = []
for (n1, i1, v1), (n2, i2, v2) in itertools.combinations_with_replacement(vecs, 2):
    for k1, k2 in itertools.product(range(-5, 6), repeat=2):
        for s1, s2 in itertools.product((1, -1), repeat=2):
            if eq(vadd(vmul(v1, pw[k1] if s1 > 0 else qn(pw[k1])), vmul(v2, pw[k2] if s2 > 0 else qn(pw[k2])))): two.append(f'{s1:+d}phi^{k1} {n1}{i1} {s2:+d}phi^{k2} {n2}{i2}')
ratios = dict(offset2_over_tip2=qs_(qd(dot(dvec, dvec), rt)), offset2_over_inner2=qs_(qd(dot(dvec, dvec), ri)))
par = [f'{n}{i}' for (n, i, v) in vecs if all(x == Z for x in cross(v, dvec))]
gap = vsub(c2, c1)
checks = dict(corner_c1=[qs_(x) for x in c1], tips=len(tips), inner=len(inner), tip_radius=qf(rt) ** .5, inner_radius=qf(ri) ** .5,
              offset_sideways=qf(dot(dvec, dvec)) ** .5, offset_along=qf(along) * qf(aa) ** .5, corner_gap=qf(dot(gap, gap)) ** .5, ratios=ratios,
              offset_parallel_to=par, single_scaled=single, two_scaled=two[:12])
print(json.dumps(checks, indent=1)); save('step5-ocd-stars.json', dict(mark=MARK, step=5, checks=checks))
