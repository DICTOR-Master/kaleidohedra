"""#61 below s = 1/4: the Swap Rule defect D(s, λ) on a grid over #61's range λ in [λ-(c), U(s)] (8 values), 6 spacings in parallel.
Each point: swap4.py (exact, 6 words). Ends FINAL ok when every point is computed (clashes are results, listed)."""
import subprocess, sys, json, os
from fractions import Fraction as Fr
from concurrent.futures import ThreadPoolExecutor
S = [Fr(1, 8), Fr(1, 6), Fr(1, 5), Fr(9, 40), Fr(6, 25), Fr(49, 200)]
def lams(s):
    lo = -Fr(1, 4) - s / 8; hi = min(Fr(1, 3) + s / 24, 3 * s / 8)
    return [lo + (hi - lo) * k / 7 for k in range(8)]
os.makedirs('grid', exist_ok=True); done = [0]; total = len(S)
print(f'START {len(S)} spacings x 8 λ, one process per spacing', flush=True)   # first line at once (SILENT START guard)
def run(s):
    L = lams(s); f = f'grid/g_{s.numerator}o{s.denominator}.txt'
    with open(f, 'w') as out:
        subprocess.run([os.path.expanduser('~/geom/bin/python'), 'swap4.py', str(s), ','.join(str(x) for x in L)], stdout=out, stderr=subprocess.STDOUT, cwd='.')
    done[0] += 1; print(f'PROGRESS {done[0] / total:.2f} spacing {s} done', flush=True); return f
with ThreadPoolExecutor(6) as ex: files = list(ex.map(run, S))
rows = 0
for f in files:
    for line in open(f):
        if line.startswith('{'): rows += 1
print(f'points computed {rows} of {8 * len(S)}', flush=True)
print('FINAL ok' if rows == 8 * len(S) else 'FINAL FAIL: missing points')
