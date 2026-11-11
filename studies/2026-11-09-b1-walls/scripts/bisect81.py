"""B1 #81: the one unknown window edge of the dodecahedron chain, between closure (period 4 entered at step 3, at 1.07) and endless growth
(1.11). Bisect with the numerical chain (chain_num5.py, 12 steps) to width 1e-7, then name the edge among simple golden numbers.
START at once, PROGRESS per halving, FINAL ok with the edge."""
import subprocess, os, sympy as sp
PY = os.path.expanduser('python3')
def closes(s):
    out = subprocess.run([PY, 'chain_num5.py', repr(s), '12'], capture_output=True, text=True).stdout
    return 'closure: (' in out
lo, hi = 1.07, 1.11
assert closes(lo) and not closes(hi)
print(f'START bisection on [{lo}, {hi}]', flush=True)
k = 0
while hi - lo > 1e-7:
    m = (lo + hi) / 2
    if closes(m): lo = m
    else: hi = m
    k += 1; print(f'PROGRESS {min(1, k / 19):.2f} edge in [{lo:.9f}, {hi:.9f}]', flush=True)
e = (lo + hi) / 2
cand = sp.nsimplify(e, [sp.sqrt(5)], tolerance=2e-7, rational=False)
print(f'edge ≈ {e:.9f}; simplest golden form within 2e-7: {cand} = {float(cand):.9f}')
print('FINAL ok' if hi - lo <= 1e-7 and closes(lo) and not closes(hi) else 'FINAL FAIL: the interval did not close cleanly')
