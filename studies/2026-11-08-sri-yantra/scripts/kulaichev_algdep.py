"""Kulaichev's yantra exactly, by the algdep route: solve the Kulaichev-Rao-Pustynski system (kulaichev_numeric.py) to DPS digits,
then let PARI/GP find the minimal polynomial of each key number (u = slope of the great triangles, Q = b6, S = b9) by LLL
(algdep), degree up to DMAX. A polynomial is accepted only if (1) it vanishes at the number to far more digits than its
coefficients need (residual < 10^-(DPS/2)) and (2) the same polynomial is found again at a lower precision (stability).
Exact proof of the whole system in that field is the next step (by resultants), once the polynomials are known.
Usage: kulaichev_algdep.py [DPS] [DMAX]   (run on compute-host with python3)"""
import sys, time, mpmath as mp
DPS = int(sys.argv[1]) if len(sys.argv) > 1 else 600
DMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 48
import kulaichev_numeric as K          # brings its start values and equations (runs its 80-digit solve once)
import cypari2; pari = cypari2.Pari(); pari.set_real_precision(DPS + 50); pari.allocatemem(2 * 10**9)
mp.mp.dps = DPS + 40
t0 = time.time()
sol = mp.findroot(lambda u, Q, S: K.eqs(u, Q, S), tuple(mp.mpf(x) for x in K.sol), tol=mp.mpf(10) ** -(DPS + 10))
print('solved to', DPS, 'digits in %.0f s' % (time.time() - t0), flush=True)
names = ['u', 'Q', 'S']; found = {}
for name, x in zip(names, sol):
    s = mp.nstr(x, DPS + 20)
    for d in range(2, DMAX + 1, 2 if False else 1):
        p_hi = pari(f'algdep({s}, {d})'); p_lo = pari(f'algdep({mp.nstr(x, DPS * 2 // 3)}, {d})')
        res = abs(complex(pari(f'subst({p_hi}, x, {s})')))
        if p_hi == p_lo and p_hi.poldegree() == d and res < 10 ** (-(DPS // 2)):
            found[name] = (d, str(p_hi)); print(f'{name}: degree {d}: {p_hi}', flush=True); break
        if d % 8 == 0: print(f'  {name}: no polynomial up to degree {d} ({time.time() - t0:.0f} s)', flush=True)
    else:
        print(f'{name}: none up to degree {DMAX} at {DPS} digits', flush=True)
print('found:', {k: v[0] for k, v in found.items()})
print('FINAL ok' if len(found) == 3 else f'FINAL FAIL: polynomials found for {sorted(found)} only (raise DPS/DMAX)')
