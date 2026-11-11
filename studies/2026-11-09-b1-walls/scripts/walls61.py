"""Run swap_walls.py at six spacings in parallel (one process each); START at once, PROGRESS per spacing finished, FINAL ok when all
six walks reach U(s)."""
import subprocess, os
from concurrent.futures import ThreadPoolExecutor
S = ['1/8', '1/6', '1/5', '9/40', '6/25', '49/200']; os.makedirs('walls', exist_ok=True); done = [0]
print(f'START Hopscotch walk at {len(S)} spacings', flush=True)
def run(s):
    f = 'walls/w_' + s.replace('/', 'o') + '.txt'
    with open(f, 'w') as out: subprocess.run([os.path.expanduser('python3'), '-u', 'swap_walls.py', s], stdout=out, stderr=subprocess.STDOUT)
    done[0] += 1; last = open(f).read().strip().splitlines()[-1]; print(f'PROGRESS {done[0] / len(S):.2f} s = {s}: {last}', flush=True); return last
with ThreadPoolExecutor(6) as ex: L = list(ex.map(run, S))
print('FINAL ok' if all(x.startswith('FINAL ok') for x in L) else 'FINAL FAIL: ' + '; '.join(x for x in L if not x.startswith('FINAL ok')))
