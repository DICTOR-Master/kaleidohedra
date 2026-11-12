"""LEAD 1 check (12 Nov 2026): the viewpoint turn written as u -> lambda u, v -> v/lambda, lambda = sqrt((1 + beta)/(1 - beta)),
read directly from the sri-yantra data: K1 (the Cleo-Octangula, u = 2/phi^2, v = 1/sqrt2) and its image V1 (figures/viewpoint.json,
written by viewpoint.py at the centring beta). Slopes from the depth frame: u = w7/(b7 - a7) (t7, from O), v = w3/(a3 - b3) (t3,
from T). POSITIVE: u_V1 = lambda u_K1 and v_V1 = v_K1/lambda to 28 digits (beta is stored to 30). NEGATIVE: the old written form
u -> u/lambda, v -> v lambda misses by more than 10^-3. Also: u v kept; the turn beta -> -beta sends V1 back to K1 (lambda -> 1/lambda).
usage: python lead1_direction.py <sri-yantra figures folder>"""
import sys, json, mpmath as mp
mp.mp.dps = 50
F = sys.argv[1] if len(sys.argv) > 1 else '../../2026-11-08-sri-yantra/figures'
K = json.load(open(f'{F}/kites.json'))['K1']; V = json.load(open(f'{F}/viewpoint.json'))['V1']
g = lambda d: {int(k): mp.mpf(x['a']) for k, x in d.items()}
def slopes(Y):
    b, w, a = g(Y['b']), g(Y['w']), g(Y['apex'])
    return w[7] / (b[7] - a[7]), w[3] / (a[3] - b[3])
uK, vK = slopes(K); uV, vV = slopes(V)
be = mp.mpf(V['beta']); lam = mp.sqrt((1 + be) / (1 - be))
phi = (1 + mp.sqrt(5)) / 2
tol = mp.mpf(10) ** -35
tolb = mp.mpf(10) ** -28                    # viewpoint.json stores beta to 30 digits, so lambda is good to about 1e-31
checks = {
    'K1 slopes are 2/phi^2 and 1/sqrt2': abs(uK - 2 / phi**2) < tol and abs(vK - 1 / mp.sqrt(2)) < tol,
    'POSITIVE: u_V1 = lambda u_K1': abs(uV - lam * uK) < tolb,
    'POSITIVE: v_V1 = v_K1 / lambda': abs(vV - vK / lam) < tolb,
    'u v kept': abs(uV * vV - uK * vK) < tol,
    'turn beta -> -beta (lambda -> 1/lambda) sends V1 back to K1': abs(uV / lam - uK) < tolb and abs(vV * lam - vK) < tolb,
    'NEGATIVE: the old form u -> u/lambda misses by > 1e-3': abs(uV - uK / lam) > mp.mpf('1e-3'),
    'NEGATIVE: the old form v -> v lambda misses by > 1e-3': abs(vV - vK * lam) > mp.mpf('1e-3'),
}
print(f'beta = {mp.nstr(be, 25)}, lambda = {mp.nstr(lam, 25)}')
print(f'K1: u = {mp.nstr(uK, 20)}, v = {mp.nstr(vK, 20)};  V1: u = {mp.nstr(uV, 20)}, v = {mp.nstr(vV, 20)}')
print(f'lambda u_K1 - u_V1 = {mp.nstr(lam * uK - uV, 3)};  u_K1/lambda - u_V1 = {mp.nstr(uK / lam - uV, 6)}')
for k, c in checks.items(): print(('  ok   ' if c else '  FAIL ') + k)
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, c in checks.items() if not c))
