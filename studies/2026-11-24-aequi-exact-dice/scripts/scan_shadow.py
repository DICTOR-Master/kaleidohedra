# Screen every catalogued fair die for the "shadow" property: every corner on a rotation axis of G and every edge on a
# mirror of G, for G = Oh (cube frame) or Ih in either icosahedron placement (A: vertices (0, ±phi, ±1); B: (0, ±1, ±phi)).
# Then the central projection of each face is a union of fundamental triangles of G (48 for Oh, 120 for Ih).
# Double precision screen only; every hit is proved exactly by prove_shadow.py.
# usage: scan_shadow.py OUT.json
import json, sys, os, glob, gzip
import numpy as np
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from groups import DIRS, DFAM
ST = os.path.normpath(os.path.join(HERE, '..', '..'))
F = np.array(DFAM)
GROUPS = {
    'Oh': dict(order=48, axes=['C6', 'O8', 'RD12'], mirrors=['C6', 'RD12']),
    'IhA': dict(order=120, axes=['C6', 'O8', 'D12', 'I12', 'RT24'], mirrors=['C6', 'RT24']),
    'IhB': dict(order=120, axes=['C6', 'O8', 'D12p', 'I12p', 'RT24p'], mirrors=['C6', 'RT24p']),
}
for g in GROUPS.values():
    g['A'] = DIRS[np.isin(F, g['axes'])]; g['M'] = DIRS[np.isin(F, g['mirrors'])]
def load():
    out = []
    for study in ['2026-11-19-aequi-complete', '2026-11-20-aequi-two-placements']:
        for f in sorted(glob.glob(os.path.join(ST, study, 'data', 'dice', '*.json'))):
            d = json.load(open(f))
            out.append(dict(src=study, sid=d['sid'], label=d['label'], group=d['group'], N=d['N'], idx=d['face_directions'],
                            sizes=d['orbit_sizes'], depths=[float(x) for x in d['depths_60_digits']]))
    for p in ['aequi2a', 'aequi2caps', 'aequi2caps2', 'aequi2caps3']:
        D = json.load(gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', p + '.json.gz')))
        for d in D['new']:
            out.append(dict(src='2026-11-24-aequi-certify-extend/' + p, sid=d['sid'], label=' + '.join(d['orbit_labels']), group=d['group'],
                            N=d['N'], idx=d['idx'], sizes=d['sizes'], depths=d['depths']))
    return out
def corners(idx, sizes, depths):
    U = DIRS[idx]; Dd = np.repeat(depths, sizes)
    hs = HalfspaceIntersection(np.hstack([U, -Dd[:, None]]), np.zeros(3)); V = []
    for v in hs.intersections:
        if not any(np.abs(v - w).max() < 1e-7 for w in V): V.append(v)
    V = np.array(V); inc = [set(np.where(np.abs(U @ v - Dd) < 1e-7)[0].tolist()) for v in V]
    return V, inc
def margin(V, inc, g):
    """0 for a shadow die; else how far it misses: the largest corner-to-nearest-axis distance, or (corners on axes)
    the largest over edges of the smallest mirror residual |n.v| + |n.w|"""
    Vn = V / np.linalg.norm(V, axis=1)[:, None]
    ax = max(np.abs(g['A'] - v).max(1).min() for v in Vn)
    if ax > 1e-7: return ax
    E = [(i, j) for i in range(len(V)) for j in range(i + 1, len(V)) if len(inc[i] & inc[j]) >= 2]
    return max((np.abs(g['M'] @ Vn[i]) + np.abs(g['M'] @ Vn[j])).min() for i, j in E)
def shadow(V, inc, g): return margin(V, inc, g) < 1e-7
if __name__ == '__main__':
    recs = load(); hits = []; cnt = {}; worst = []; fails = 0
    for k, r in enumerate(recs):
        cnt[r['src']] = cnt.get(r['src'], 0) + 1
        try: V, inc = corners(r['idx'], r['sizes'], r['depths'])
        except Exception as e: print('hull fail', r['src'], r['sid'], e); fails += 1; continue
        mg = {gn: margin(V, inc, g) for gn, g in GROUPS.items()}
        if min(mg.values()) >= 1e-7: worst.append((min(mg.values()), r['src'], r['sid'], r['label']))
        for gn, g in GROUPS.items():
            if mg[gn] < 1e-7:
                hits.append(dict(r, G=gn, corners=len(V))); print('HIT', gn, r['src'], r['sid'], r['group'], r['N'], r['label'], 'corners', len(V), flush=True)
        if k % 2000 == 0: print('PROGRESS %.3f' % (k / len(recs)), flush=True)
    print('scanned', cnt, 'total', len(recs)); print('hits', len(hits)); worst.sort()
    print('non-hits: smallest miss margins (how close the nearest non-shadow dice come to the shadow condition):')
    for w in worst[:8]: print('  %.3e' % w[0], w[1], w[2], w[3])
    json.dump(hits, open(sys.argv[1], 'w'), indent=1)
    print('FINAL ok' if fails == 0 and len(recs) == 15192 and all(w[0] > 1e-4 for w in worst) else 'FINAL FAIL (hull failures, record count or a near miss)')
