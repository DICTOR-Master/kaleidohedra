"""Certificate 4: certified counts at four points of the rhombus branch, by #103 Proposition 11's pipeline (certified_counts.py).

Points (u = v):  29/50 (c = 0.3364, below the window);  sqrt(2/phi^3) (c = 2/phi^3, the rhombus image of the DICTO Yantra under
#103 Theorem 5's viewpoint map);  7/10 (c = 0.49, inside);  3/4 (c = 0.5625, Rh345, above the window).
At each point the branch (ycert.branch at 1900 bits) encloses every base depth, half-width and apex to about 570 digits; the
enclosures are padded outward by 10^-555 and written as stage5-K.json, and certified_counts.py K is run on them unchanged
(identities decided exactly in the case K model with the closing numerator Fc of inputs/stage2-K.json).
Expected: 45 / 41 triangles / 18 / 28 at 29/50 and 3/4; 43 / 43 / 18 / 24 at sqrt(2/phi^3) and 7/10.
usage: python -u cert4_counts.py"""
import sys, os, json, time, shutil, subprocess
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import flint
from flint import arb, fmpq
flint.ctx.prec = 1900
import mpmath as mp
mp.mp.dps = 600
import ycert as Y
from cert1_sweep import tguess
flint.ctx.prec = 1900                                    # cert1_sweep sets 256 on import

PHI3 = 2 * arb(5).sqrt() - 4                             # 2/phi^3 = 2 sqrt5 - 4
POINTS = [('u29_50', arb(fmpq(29, 50)), '45'), ('u_cleo_antonius', PHI3.sqrt(), '43'), ('u7_10', arb(fmpq(7, 10)), '43'),
          ('u3_4', arb(fmpq(3, 4)), '45')]
PAD = mp.mpf(10) ** -555
def fmt(z):
    lo = mp.mpf(z.lower().str(590, radius=False)) - PAD; hi = mp.mpf(z.upper().str(590, radius=False)) + PAD
    return [mp.nstr(lo, 560, strip_zeros=False), mp.nstr(hi, 560, strip_zeros=False)]
allok = True; summary = {}
for tag, U, exp in POINTS:
    Sb, Tb, _ = Y.branch(U, tguess(float(U.mid())))
    y = Y.build(U, Tb, Sb)
    adm = all(q > 0 for _, q in Y.admissibility(y))
    wd = max((mp.mpf(arb(z.rad()).str(5, radius=False)) for d in ('b', 'w', 'a') for z in y[d].values()), default=0)
    W = os.path.join(ROOT, 'data', 'counts', tag); os.makedirs(W, exist_ok=True)
    json.dump({'case': tag, 'u': U.str(40), 'b': {str(i): fmt(z) for i, z in y['b'].items()},
               'w': {str(i): fmt(z) for i, z in y['w'].items()}, 'a': {str(i): fmt(z) for i, z in y['a'].items()}},
              open(os.path.join(W, 'stage5-K.json'), 'w'))
    for f in ('stage2-K.json', 'model.py'): shutil.copy(os.path.join(ROOT, 'inputs', f), W)
    say(f'{tag}: u = {U.str(20)}, c = {(U * U).str(20)}; enclosures widest radius {mp.nstr(wd, 3)}; admissible (strict) {adm}; running certified_counts.py K {exp}')
    p = subprocess.run([sys.executable, '-u', os.path.join(HERE, 'certified_counts.py'), 'K', exp], cwd=W, capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    open(os.path.join(ROOT, 'logs', f'cert4_counts-{tag}.log'), 'w').write('\n'.join(out) + '\n')
    for line in out: print('    ' + line[:260])
    ok = adm and bool(out) and out[-1].strip() == 'FINAL ok'
    summary[tag] = dict(u=U.str(30), expected=exp, ok=ok)
    allok = allok and ok
for f in ('stage2-K.json', 'model.py'):
    for tag, _, _ in POINTS:
        try: os.remove(os.path.join(ROOT, 'data', 'counts', tag, f)); shutil.rmtree(os.path.join(ROOT, 'data', 'counts', tag, '__pycache__'), ignore_errors=True)
        except OSError: pass
json.dump(summary, open(os.path.join(ROOT, 'data', 'counts', 'summary.json'), 'w'), indent=1)
print('FINAL ok' if allok else 'FINAL FAIL')
