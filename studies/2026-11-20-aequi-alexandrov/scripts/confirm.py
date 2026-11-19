# Confirm every die found by alex.py's die-finder to 80 digits with the refinement of study 2026-11-19-aequi-complete
# (exact.py: mpmath findroot on one depth per orbit, corners by Cramer's rule from face triples; every face
# |Ω − 4π/N| < 1e-50, every corner on its planes and inside all others to 1e-50), then its centroid (floats).
# usage: confirm.py alex.jsonl out.jsonl NPROC
import json, sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-19-aequi-complete', 'scripts'))
from groups import DIRS
from exact import refine, centroid
from multiprocessing import Pool
def work(r):
    idx = [j for j in r['idx']]; sizes = r['sizes']
    base = dict(kind=r['kind'], cls=r['cls'], group=r['group'], m=r['m'], subset=r['subset'], verdict=r['verdict'])
    try:
        ex = refine(dict(idx=idx, sizes=sizes, depths=r['die_finder']['die']['depths']))
    except Exception as e:
        return dict(base, exact_ok=False, error=repr(e))
    D = np.repeat([float(x) for x in ex['depths60']], sizes)
    cen, vol = centroid(np.array(ex['verts']), ex['faces'], DIRS[idx], D)
    dep = [float(x) for x in ex['depths60']]
    return dict(base, exact_ok=ex['exact_ok'], res_omega=ex['res_omega'], res_inc=ex['res_inc'], max_violation=ex['max_violation'],
                depths60=ex['depths60'], corners=ex['corners'], sides=sorted(len(f) for f in ex['faces']),
                depth_ratio_max=max(dep) / min(dep), centroid=cen.tolist(), centroid_offset=float(np.linalg.norm(cen) / vol ** (1 / 3)))
if __name__ == '__main__':
    rows = []
    sets = {(r['kind'], r['cls'], r['m'], tuple(r['subset'])): r for r in map(json.loads, open(os.path.join(HERE, '..', 'data', 'sets.jsonl')))}
    for L in open(sys.argv[1]):
        r = json.loads(L)
        if r['die_finder']['die'] is None: continue
        s = sets[(r['kind'], r['cls'], r['m'], tuple(r['subset']))]
        r['idx'] = [j for O in s['orbits'] for j in O]; rows.append(r)
    with Pool(int(sys.argv[3])) as pool:
        out = pool.map(work, rows)
    with open(sys.argv[2], 'w') as fo:
        for o in out: fo.write(json.dumps(o) + '\n')
    hold = [o for o in out if o['verdict'] == 'holds']; eq = [o for o in out if o['verdict'] != 'holds']
    print('dice to confirm', len(hold), '| confirmed to 80 digits', sum(o['exact_ok'] for o in hold))
    print('equality limits (condition fails with equality)', len(eq), '| confirmed as dice', sum(o['exact_ok'] for o in eq))
    print('largest depth ratio', max(o['depth_ratio_max'] for o in hold if o['exact_ok']))
    print('smallest centroid offset / volume^(1/3)', min(o['centroid_offset'] for o in hold if o['exact_ok']))
    ok = all(o['exact_ok'] for o in hold) and not any(o['exact_ok'] for o in eq)
    print('FINAL ok' if ok else 'FINAL FAIL: a found die did not confirm, or an equality limit confirmed')
