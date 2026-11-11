"""Run swap_cells2.py for the five cells of the #61 chamber map in parallel; START at once, PROGRESS per cell finished, FINAL ok when all
five end FINAL ok (each = that cell proved for all s in its range)."""
import subprocess, os
from concurrent.futures import ThreadPoolExecutor
C = ['b', 'c1', 'c2', 'd1', 'd2']; os.makedirs(f"cells2-D{os.environ.get('D2', '12')}", exist_ok=True); done = [0]
print(f'START two-parameter proof, cells {C}', flush=True)
def run(c):
    f = f'cells2-D{os.environ.get('D2', '12')}/{c}.txt'
    with open(f, 'w') as out: subprocess.run([os.path.expanduser('python3'), '-u', 'swap_cells2.py', c], env={**os.environ, 'D2': os.environ.get('D2', '12')}, stdout=out, stderr=subprocess.STDOUT)
    done[0] += 1; last = open(f).read().strip().splitlines()[-1]; print(f'PROGRESS {done[0] / len(C):.2f} cell {c}: {last}', flush=True); return last
with ThreadPoolExecutor(5) as ex: L = list(ex.map(run, C))
print('FINAL ok' if all(x.startswith('FINAL ok') for x in L) else 'FINAL FAIL: ' + ' | '.join(x for x in L if not x.startswith('FINAL ok')))
