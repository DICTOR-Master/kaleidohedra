"""B1 #80 / #81 window edges (DICTO 10 Nov "run #80/#81 window edges alongside"): one exact symbolic chain per regime, in parallel; each
prints its steps' exact hops (walls) and the chain hop on which the closure identity holds = the regime's exact edges.
START at once, PROGRESS per run finished, FINAL ok when every run has ended (FINAL FAIL lines inside are results too: listed)."""
import subprocess, os
from concurrent.futures import ThreadPoolExecutor
PY = os.path.expanduser('python3')
RUNS = [('d-3o4', ['chain_sym5.py', '3/4', '5']), ('d-21o20', ['chain_sym5.py', '21/20', '8']), ('d-13o10', ['chain_sym5.py', '13/10', '6']),
        ('d-29o20', ['chain_sym5.py', '29/20', '3']), ('c-14o25', ['chain_sym.py', '14/25', '8'])]
os.makedirs('windows', exist_ok=True); done = [0]
print(f'START {len(RUNS)} exact chains (#81 dodecahedron at 3/4, 21/20, 13/10, 29/20; #80 cube at 14/25)', flush=True)
def run(r):
    name, args = r; f = f'windows/{name}.txt'
    with open(f, 'w') as out: subprocess.run([PY, '-u'] + args, stdout=out, stderr=subprocess.STDOUT, env={**os.environ, 'LO': '2/5', 'HI': '3/2'})
    done[0] += 1; last = (open(f).read().strip().splitlines() or ['(empty)'])[-1]; print(f'PROGRESS {done[0] / len(RUNS):.2f} {name}: {last}', flush=True); return last
with ThreadPoolExecutor(len(RUNS)) as ex: L = list(ex.map(run, RUNS))
print('FINAL ok' if all(x.startswith('FINAL') for x in L) else 'FINAL FAIL: a run ended without its FINAL line')
