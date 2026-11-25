"""The 63 dice whose symmetry group is larger than the frame maps realise (two-placement dihedral dice): Resonus vs mirrors decided
directly. The Resonus plane u^perp of a face line u is a mirror iff the reflection in u^perp maps every face orbit onto itself
(a symmetry of the fair die; float test on exact directions, decisive at the separation printed by aequi_overlaps)."""
import gzip, os, sys, json, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]; sys.path.insert(0, HERE)
import aequi_overlaps as AO
def order(g):
    T = {'Ih': 120, 'I': 60, 'Oh': 48, 'O': 24, 'Td': 24, 'Th': 24, 'T': 12, 'Ci': 2, 'Cs': 2, 'C1': 1}
    if g in T: return T[g]
    m = re.match(r'([DCS])(\d+)([hdv]?)$', g); L, n, s = m.group(1), int(m.group(2)), m.group(3)
    return (4 * n if s else 2 * n) if L == 'D' else (n if L == 'S' else (2 * n if s else n))
REC = {(r['part'], r['study'], int(r['sid'])): r for r in AO.PA.records()}
out = []
for l in gzip.open(os.path.join(HERE, '..', 'data', 'aequi-overlaps.jsonl.gz'), 'rt'):
    o = json.loads(l)
    if order(o['group']) == o['group_order']: continue
    r = REC[(o['part'], o['study'], o['sid'])]; idx = [int(x) for x in r['idx']]; sizes = [int(x) for x in r['sizes']]
    lab = np.repeat(np.arange(len(sizes)), sizes); P = AO.DIRS[idx]
    lines = sorted({AO.LINE[i] for i in idx}); good = 0
    for li in lines:
        u = AO.DIRS[li]; S = np.eye(3) - 2 * np.outer(u, u); img = P @ S.T
        d2 = np.linalg.norm(img[:, None, :] - P[None, :, :], axis=2); j = d2.argmin(1)
        if d2.min(1).max() < 1e-9 and all(lab[j] == lab): good += 1
    out.append(dict(part=o['part'], sid=o['sid'], label=o['label'], resonus=len(lines), resonus_planes_that_are_mirrors=good, R_sub_M=good == len(lines)))
json.dump(out, open(os.path.join(HERE, '..', 'data', 'bigger-groups.json'), 'w'), indent=1, ensure_ascii=False)
print('dice', len(out), '| R inside mirrors', [(x['label'], x['resonus']) for x in out if x['R_sub_M']])
print('FINAL ok' if len(out) == 63 else 'FINAL FAIL')
