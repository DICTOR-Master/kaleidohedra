# DICTO #43 Conjecture 1, study 2026-11-09: checks the proved step inequalities on the float family, and the tail criteria.
#   (F1) R(D_{k+1}) = H(D_k) <= R(D_k)          (F2) r(D_{k+1}) >= r(D_k) cos theta_k   (theta_k = covering radius of D_k's normals)
#   (F3) t_min(D_k) <= R(D_k)/r(D_{k+1}) <= R(D_k)/(r(D_k) cos theta_k)
#   Inradius Lemma margin: for each K, inf_{j>K} r(D_j) against (phi^2/3) R(D_K)  (sufficient for every k >= K).
# usage: python3 tail_criteria.py data/float-family.json [K_exact]
import sys, json, math
d = json.load(open(sys.argv[1]))['k']; KEX = int(sys.argv[2]) if len(sys.argv) > 2 else 8
phi = (1 + 5 ** .5) / 2; T = 3 / phi ** 2; ok = True; eps = 1e-9
print(' k   t_min      R/r_next   (R/r)/cos(th)  theta(deg)   r         R')
for a, b in zip(d, d[1:]):
    f1 = abs(b['R'] - a['H']) < 1e-9 and b['R'] <= a['R'] + eps
    f2 = b['r'] >= a['r'] * math.cos(a['theta']) - eps
    f3 = a['t_min'] <= a['R'] / b['r'] + eps <= a['R'] / (a['r'] * math.cos(a['theta'])) + 2 * eps
    ok &= f1 and f2 and f3 and a['t_min'] <= T + eps
    print(f"{a['k']:2d}  {a['t_min']:.6f}  {a['R'] / b['r']:.6f}  {a['R'] / (a['r'] * math.cos(a['theta'])):.6f}     {math.degrees(a['theta']):7.3f}   {a['r']:.6f}  {a['R']:.6f}"
          f"  {'F1 F2 F3 ok' if f1 and f2 and f3 else 'FAIL ' + str((f1, f2, f3))}")
last = d[-1]['k']
print(f'\nInradius Lemma margins (needed: r(D_j) >= (phi^2/3) R(D_K) for all j > K; seen for K < j <= {last}):')
for K in range(KEX, last):
    need = d[K]['R'] / T; seen = min(x['r'] for x in d[K + 1:])
    print(f'  K = {K:2d}: need {need:.6f}, smallest seen {seen:.6f}, margin {seen / need - 1:+.2%}')
first = min(k for k in range(len(d) - 1) if all(x['R'] / (x['r'] * math.cos(x['theta'])) <= T for x in d[k:-1]))
print(f'\nper-step criterion (R/r)/cos(theta) <= 3/phi^2 holds for every k from {first} to {last - 1}')
s = sum(x['theta'] ** 2 for x in d[20:]); print(f'sum of theta_j^2, j = 20..{last}: {s:.5f}; product of cos theta_j: {math.prod(math.cos(x["theta"]) for x in d[20:]):.6f}')
print('FINAL ok' if ok else 'FINAL FAIL: a step inequality or the bound failed on the float data')
