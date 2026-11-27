"""Step 12 merge (27 Nov 2026): collect the SHARD files of fair_centroid.py (PAIR mode) into one gzipped file and summarise.
With Claude (Anthropic)."""
import os, sys, json, gzip, glob
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); K = int(sys.argv[1]); tag = sys.argv[2]
fs = sorted(glob.glob(os.path.join(HERE, f'../fairdice_centroid_{tag}_shard*.json')))
R = [x for f in fs for x in json.load(open(f))]
print('shard files', len(fs), 'of', K, '; dice checked', len(R))
fair = [x for x in R if x['fair']]
print('fair from the centre of mass:', len(fair), 'of', len(R))
print('fair by symmetry order:', sorted(Counter(x['symmetry_order'] for x in fair).items(), reverse=True))
bad = [x for x in R if not x['fair']]
print('not fair:', [(x['index'], x['symmetry_order'], f"{x['centroid_offset']:.1e}", f"{x['max_angle_dev']:.1e}", x['pattern_kept']) for x in bad][:60])
print('max angle cross-check deviation among fair:', max((x['max_angle_dev'] for x in fair), default=0))
json.dump(R, gzip.open(os.path.join(HERE, f'../fairdice_centroid_{tag}.json.gz'), 'wt'))
ctl = [x for x in R if x['symmetry_order'] == 120]
print('controls (full symmetry) fair:', [x['fair'] for x in ctl])
exp = len(json.load(gzip.open(os.path.join(HERE, '../fairdice_icosidodecahedron_symmetric.json.gz')))) if sys.argv[3] == 'auto' else int(sys.argv[3])
print('expected', exp)
ok = len(fs) == K and len(R) == exp and ctl and all(x['fair'] for x in ctl)
if ok:
    for f in fs: os.remove(f)
print('FINAL ok' if ok else 'FINAL FAIL')
