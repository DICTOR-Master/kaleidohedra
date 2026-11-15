#!/usr/bin/env python3
"""Read one scale of a public BossDB precomputed volume (bucket bossdb-open-data) into a local uint8 .npy (z, y, x).
Dataset: Paukner et al. 2024 (J. Microsc.?/ see README), BossDB collection paukner2024. No licence is stated for it: the volume is
kept on the compute machine outside git and is never redistributed; only derived counts are committed.
Usage: python bossfetch.py EXPERIMENT SCALE_KEY OUT.npy [x0 x1 y0 y1 z0 z1]"""
import sys, json, gzip, urllib.request, urllib.error, numpy as np, time
from concurrent.futures import ThreadPoolExecutor
exp, key, out = sys.argv[1], sys.argv[2], sys.argv[3]
base = f'https://bossdb-open-data.s3.amazonaws.com/paukner2024/{exp}/032019_DP_full_vol'
info = json.load(urllib.request.urlopen(base + '/info'))
sc = [s for s in info['scales'] if s['key'] == key][0]; X, Y, Z = sc['size']; cx, cy, cz = sc['chunk_sizes'][0]
x0, x1, y0, y1, z0, z1 = [int(v) for v in sys.argv[4:10]] if len(sys.argv) > 4 else (0, X, 0, Y, 0, Z)
V = np.lib.format.open_memmap(out, mode='w+', dtype=np.uint8, shape=(z1 - z0, y1 - y0, x1 - x0))
MISSING = []
jobs = [(a, b, c) for a in range(x0 // cx * cx, x1, cx) for b in range(y0 // cy * cy, y1, cy) for c in range(z0 // cz * cz, z1, cz)]
def get(j):
    a, b, c = j; a2, b2, c2 = min(a + cx, X), min(b + cy, Y), min(c + cz, Z)
    url = f'{base}/{key}/{a}-{a2}_{b}-{b2}_{c}-{c2}'
    for t in range(5):
        try:
            r = urllib.request.urlopen(url, timeout=60); d = r.read()
            if d[:2] == b'\x1f\x8b': d = gzip.decompress(d)
            break
        except urllib.error.HTTPError as e:
            if e.code in (403, 404): MISSING.append(url); return 0     # precomputed format: an absent chunk is background (zeros)
            if t == 4: raise
            time.sleep(2 * (t + 1))
        except Exception as e:
            if t == 4: raise
            time.sleep(2 * (t + 1))
    blk = np.frombuffer(d, np.uint8).reshape((c2 - c, b2 - b, a2 - a))   # precomputed raw = Fortran (x fastest) = C order (z, y, x)
    sa, sb, sc_ = max(a, x0), max(b, y0), max(c, z0); ea, eb, ec = min(a2, x1), min(b2, y1), min(c2, z1)
    V[sc_ - z0:ec - z0, sb - y0:eb - y0, sa - x0:ea - x0] = blk[sc_ - c:ec - c, sb - b:eb - b, sa - a:ea - a]
    return 1
done = 0
with ThreadPoolExecutor(16) as ex:
    for _ in ex.map(get, jobs):
        done += 1
        if done % max(1, len(jobs) // 20) == 0: print(f'PROGRESS {done / len(jobs):.2f} chunks {done}/{len(jobs)}', flush=True)
V.flush(); print('absent chunks (left as zeros):', len(MISSING), MISSING[:3]); print('shape', V.shape, 'mean', float(V[::4, ::4, ::4].mean()))
print('FETCH ok')
