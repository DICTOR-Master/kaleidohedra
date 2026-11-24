# Recheck of the shadow screen on a random sample of non-hits (double precision, as the original screen).
# Own code: corners by triple-plane solves, face cycles, edges; an edge is "on a mirror" of G when both unit end
# vectors are within tol of one mirror plane. The miss of a die for G is the largest over edges of the smallest
# such distance; a die is a hit for G when the miss is below tol.
import sys, json, random, os, time
import numpy as np
from dirs import directions, catalogue, ST
from die_num import build, edges, mirror_miss, solid_angles
nsamp = int(sys.argv[1]); outp = sys.argv[2]
D, FAM = directions('set'); Df = np.array([[float(x) for x in v] for v in D]); U = Df / np.linalg.norm(Df, axis=1)[:, None]
def mir(fams):
    M = []
    for f in fams:
        for v in U[[i for i, g in enumerate(FAM) if g == f]]:
            if not any(np.abs(v + m).max() < 1e-9 for m in M): M.append(v)
    return np.array(M)
MIR = {'Oh': mir(['C6', 'RD12']), 'IhA': mir(['C6', 'RT24']), 'IhB': mir(['C6', 'RT24p'])}
assert [len(MIR[k]) for k in MIR] == [9, 15, 15]
hits = {(h['src'], h['sid']) for h in json.load(open(os.path.join(ST, '2026-11-24-aequi-exact-dice', 'data', 'shadow_hits.json')))}
cat = catalogue(); assert len(cat) == 15192
non = [r for r in cat if (r[0], r[1]) not in hits]; assert len(non) == 15192 - 14
random.seed(20261124); sample = random.sample(non, nsamp)
pos = [r for r in cat if (r[0], r[1]) in hits]
res = []; t0 = time.time()
for tag, group in (('hit', pos), ('sample', sample)):
    for r in group:
        V, fc = build(U[r[2]], np.array(r[3])); E = edges(fc)
        fairres = max(abs(o - 4 * np.pi / r[4]) for o in solid_angles(V, fc))
        miss = {g: float(mirror_miss(V, E, MIR[g])) for g in MIR}
        res.append(dict(tag=tag, src=r[0], sid=r[1], N=r[4], corners=len(V), fair_residual=float(fairres), miss=miss, min_miss=min(miss.values())))
    print('PROGRESS', tag, len(res), '%.0fs' % (time.time() - t0), flush=True)
json.dump(res, open(outp, 'w'), indent=1)
H = [x for x in res if x['tag'] == 'hit']; S = [x for x in res if x['tag'] == 'sample']
tol = 1e-7
print('hits passing (some G, miss < 1e-7):', sum(x['min_miss'] < tol for x in H), 'of', len(H), ' largest hit miss %.1e' % max(x['min_miss'] for x in H))
print('sample non-hits passing:', sum(x['min_miss'] < tol for x in S), 'of', len(S))
w = min(S, key=lambda x: x['min_miss'])
print('smallest miss in sample: %.3e (%s %s)' % (w['min_miss'], w['src'], w['sid']))
print('largest fairness residual (all): %.1e' % max(x['fair_residual'] for x in res))
ok = all(x['min_miss'] < tol for x in H) and all(x['min_miss'] >= tol for x in S) and max(x['fair_residual'] for x in res) < 1e-8
print('FINAL ok' if ok else 'FINAL disagree')
