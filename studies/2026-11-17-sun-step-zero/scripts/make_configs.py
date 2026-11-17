"""Writes the census configurations of this study (data/configs_{pilot,a,b}.jsonl) from the 13 main settings of 16 Nov
(studies/2026-11-15-sun-granulation/scripts/sun_matrix.jsonl, read unchanged). Paths are relative to this study's folder.
Usage: make_configs.py (run from the study folder)"""
import json
OLD = '../2026-11-15-sun-granulation'
STEPS = [1, 2, 3, 4, 6, 8]
MAIN13 = ['en_T0.0_s1.5_hmax300', 'en_T0.0_s1.5_thr0.25', 'en_uz0.1_s1.5_hmax1200', 'en_uz0.1_s1.5_hmax300', 'en_uz0.1_s1.5_hmax600',
          'en_uz0.1_s1.5_thr0.0', 'en_uz0.1_s1.5_thr0.25', 'en_uz0.1_s1.5_thr0.5', 'en_uz0.1_s3.0_thr0.25', 'qs_uz0.1_s1.5_hmax600',
          'qs_uz0.1_s1.5_thr0.0', 'qs_uz0.1_s1.5_thr0.25', 'qs_uz0.1_s1.5_thr0.5']
sun = []
for l in open(f'{OLD}/scripts/sun_matrix.jsonl'):
    if not l.strip(): continue
    c = json.loads(l); tag = c['out'].split('/')[-1][:-5]
    if tag in MAIN13: sun.append((tag, c))
assert len(sun) == 13, len(sun)
def ctl(name, data, z, out):
    sg, h = (0, 'hmax:0.01') if z == 0 else (1.5, 'hmax:0.5')          # the 16 Nov control settings
    return dict(data=data, run=name, var='img', dz=0.0, sigma=sg, h=h, steps=STEPS, W=60, out=out)
A, B = [], []
for tag, c in sun:
    A.append(dict(c, data=f'{OLD}/data/bifrost', steps=STEPS, out=f'data/sun/{tag}.json'))
    B.append(dict(c, data='work/order', run=c['run'] + '-shuf', steps=STEPS, out=f'data/order/{tag}-shuf.json'))
for v in (1, 2):
    for z in (0, 1):
        A.append(ctl(f'voronoi_n500_v{v}.0_z{z}.0_s1', f'{OLD}/data/control-s1', z, f'data/control/voronoi_n500_v{v}.0_z{z}.0_s1.json'))
        B.append(ctl(f'voronoi_n500_v{v}.0_z{z}.0_s2', 'work/control-s2', z, f'data/holdout/voronoi_n500_v{v}.0_z{z}.0_s2.json'))
B.append(ctl('voronoi_n500_v1.0_z0.0_s1-shuf', 'work/order', 0, 'data/order/voronoi_n500_v1.0_z0.0_s1-shuf.json'))
P = [dict(A[[t for t, _ in sun].index('en_uz0.1_s1.5_thr0.25')], nframes=40, out='results/pilot/sun_primary.json'),
     dict(A[13], nframes=40, out='results/pilot/control_v1_z0.json')]
for name, L in (('pilot', P), ('a', A), ('b', B)):
    with open(f'data/configs_{name}.jsonl', 'w') as f:
        for c in L: f.write(json.dumps(c) + '\n')
    print(name, len(L))
print('FINAL ok' if (len(A), len(B), len(P)) == (17, 18, 2) else 'FINAL FAIL config counts')
