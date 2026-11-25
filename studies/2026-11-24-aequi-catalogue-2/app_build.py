# DICTO · Aequi catalogue 2 into the picker (25 Nov 2026). With Claude (Anthropic).
# For every catalogued die Nos. 1236-10725: rebuild its faces from the subgroup orbits it was found under (classes file of its batch),
# give each searched orbit one of the die's depths (the assignment that makes the die fair), CHECK fairness (every face subtends 4 pi / N,
# |error| < 1e-9), compute the die's full symmetry group numerically (orthogonal maps carrying faces with their depths onto faces) and its
# face orbits, and CHECK them against the catalogue (group order, m, orbit sizes, corners). Writes app_dice.json (one row per die).
# Usage: python app_build.py <certify-extend study dir> <out.json> [NPROC]
import sys, json, gzip, csv, itertools, os
import numpy as np
from multiprocessing import Pool
from scipy.spatial import HalfspaceIntersection
EXT = sys.argv[1]; OUT = sys.argv[2]; NP = int(sys.argv[3]) if len(sys.argv) > 3 else 20
sys.path.insert(0, os.path.join(EXT, 'scripts')); from groups import DIRS
D = np.array(DIRS, float); D = D / np.linalg.norm(D, axis=1)[:, None]
BATCH = {'2a': ('aequi2a', 'classes2a.json'), 'caps1': ('aequi2caps', 'classes-study1.json'),
         'caps2': ('aequi2caps2', 'classes-study1.json'), 'caps3': ('aequi2caps3', 'classes-study1.json')}
def load(b):
    f, c = BATCH[b]
    return json.load(gzip.open(os.path.join(EXT, 'data', f + '.json.gz')))['new'], json.load(open(os.path.join(EXT, 'data', c)))
def solid_angles(idx, dep):
    H = np.hstack([D[idx], -np.array(dep)[:, None]])
    V = HalfspaceIntersection(H, np.zeros(3)).intersections
    V = np.unique(np.round(V, 12), axis=0)
    om, sides = [], []
    for k, i in enumerate(idx):
        on = V[np.abs(V @ D[i] - dep[k]) < 1e-9]
        c = on.mean(0); u = on[0] - c; u /= np.linalg.norm(u); w = np.cross(D[i], u)
        on = on[np.argsort(np.arctan2((on - c) @ w, (on - c) @ u))]
        s = 0.0
        for a, b in zip(on, np.roll(on, -1, 0)):
            num = np.dot(c, np.cross(a, b)); den = np.linalg.norm(c) * np.linalg.norm(a) * np.linalg.norm(b) + np.dot(c, a) * np.linalg.norm(b) + np.dot(c, b) * np.linalg.norm(a) + np.dot(a, b) * np.linalg.norm(c)
            s += 2 * np.arctan2(num, den)
        om.append(abs(s)); sides.append(len(on))
    return np.array(om), sides, len(V)
def symmetries(idx, dep):
    N = D[idx]; dp = np.array(dep); maps = []
    a = 0; b = next(k for k in range(1, len(idx)) if abs(abs(N[0] @ N[k]) - 1) > 1e-6)
    A = np.array([N[a], N[b], np.cross(N[a], N[b])]).T
    for i in range(len(idx)):
        if abs(dp[i] - dp[a]) > 1e-9: continue
        for k in range(len(idx)):
            if k == i or abs(dp[k] - dp[b]) > 1e-9 or abs(N[i] @ N[k] - N[a] @ N[b]) > 1e-9: continue
            for sg in (1, -1):
                B = np.array([N[i], N[k], sg * np.cross(N[i], N[k])]).T
                R = B @ np.linalg.inv(A)
                if np.abs(R @ R.T - np.eye(3)).max() > 1e-9: continue
                img = N @ R.T
                M = np.abs(img @ N.T - 1) < 1e-9
                if not (M.sum(1) == 1).all(): continue
                perm = M.argmax(1)
                if np.abs(dp[perm] - dp).max() > 1e-9: continue
                maps.append(perm)
    return maps
def work(row):
    no, b, sid = row
    new, cls = DATA[b]; r = new[sid]
    if (r['group'], r['m'], r['N']) != CATROW[no]: return dict(no=no, ok=False, err='catalogue row differs from source')
    out = dict(no=no, batch=b, sid=sid, group=r['group'], ok=False)
    fu = r['found_under'][0]; C = cls[fu['cls']]
    orbs = [C['orbits'][j] for j in fu['subset']]
    if sorted(d for o in orbs for d in o) != sorted(r['idx']): out['err'] = 'orbit union differs from idx'; return out
    vals = sorted(set(r['depths']))
    for asg in itertools.product(vals, repeat=len(orbs)):
        idx = [d for o in orbs for d in o]; dep = [asg[j] for j, o in enumerate(orbs) for _ in o]
        try: om, sides, nv = solid_angles(idx, dep)
        except Exception: continue
        if np.abs(om - 4 * np.pi / len(idx)).max() < 1e-9: break
    else:
        out['err'] = 'no fair depth assignment'; return out
    maps = symmetries(idx, dep)
    # orbits of the full group
    seen, forb = set(), []
    for k in range(len(idx)):
        if k in seen: continue
        o = sorted({int(p[k]) for p in maps}); seen |= set(o); forb.append(o)
    sizes = sorted(len(o) for o in forb)
    chk = dict(order=len(maps) == r['sym_order'], m=len(forb) == r['m'], sizes=sizes == sorted(r['sizes']), corners=nv == r['corners'],
               fair=float(np.abs(om - 4 * np.pi / len(idx)).max()))
    out.update(chk=chk, ok=chk['order'] and chk['m'] and chk['sizes'] and chk['corners'],
               N=len(idx), m=len(forb), c=nv, h=int(r['chiral']),
               orbits=[[int(idx[k]) for k in o] for o in forb], depths=[float(dep[o[0]]) for o in forb],
               sides=[sorted({sides[k] for k in o}) for o in forb], labels=r['orbit_labels'], sizes_rec=r['sizes'])
    return out
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalogue.csv')
rows = []; CATROW = {}
BMAP = {'2a': '2a', '2caps': 'caps1', '2caps2': 'caps2', '2caps3': 'caps3'}
for x in csv.DictReader(open(CAT)):
    if x['source_batch'] == 'reserved': continue
    rows.append((int(x['No']), BMAP.get(x['source_batch'], x['source_batch']), int(x['source_id']))); CATROW[int(x['No'])] = (x['group'], int(x['m']), int(x['N']))
DATA = {b: load(b) for b in sorted({r[1] for r in rows})}
# source_id = position in the batch's 'new' list (checked: No. 2471 -> 2a 1214 is D3d, m 4, N 42)
if __name__ == '__main__':
    pilot = os.environ.get('PILOT')
    todo = rows[:int(pilot)] if pilot else rows
    res = []
    with Pool(NP) as P:
        for k, r in enumerate(P.imap(work, todo, chunksize=8)):
            res.append(r)
            if k % 500 == 0: print('PROGRESS %.3f dice %d' % (k / len(todo), k), flush=True)
    bad = [r for r in res if not r['ok']]
    json.dump(res, open(OUT, 'w'))
    print('dice', len(res), 'ok', len(res) - len(bad), 'bad', len(bad))
    for r in bad[:10]: print('  BAD', r['no'], r.get('err'), r.get('chk'))
    print('FINAL ok' if not bad and len(res) == len(todo) else 'FINAL FAIL')
