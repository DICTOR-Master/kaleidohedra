# DICTO #43 Conjecture 1, gnomon study 2026-11-09 (DICTO proposed a gnomon argument): checks on the float data.
#   s_k >= 1 (Lemma G) and t_k >= R_k/R_{k+1} >= 1; gnomon criterion log t_k <= delta_k = log(s_k t_k) and delta_k <= log(3/phi^2)
#   classical gnomon test: all face counts distinct (no two D_k similar)
#   monotonicity tests the gnomon route hoped for: r(D_j) for j >= 12, oscillation log(R/r)
#   the new-face reduction: r_{k+1} = min(persistent-face minimum, new-face minimum) and r_{k+1} >= min(r_k, new-face minimum)
# usage: python3 gnomon_checks.py data/gnomon-float.json data/gnomon-axes.json
import sys, json, math
F = json.load(open(sys.argv[1]))['k']; A = json.load(open(sys.argv[2]))['k']
phi = (1 + 5 ** .5) / 2; L = math.log(3 / phi ** 2); ok = True; e = 1e-9
print(f'log(3/phi^2) = {L:.6f}')
print(' k   s_k        t_k        delta_k    t <= e^delta   R_k/R_k+1')
for a, b in zip(F, F[1:]):
    rr = a['R'] / b['R']; c1 = a['s'] >= 1 - e and a['t'] >= rr - e and rr >= 1 - e
    c2 = math.log(a['t']) <= a['delta'] + e and a['delta'] <= L + e
    ok &= c1 and c2
    print(f"{a['k']:2d}  {a['s']:.6f}  {a['t']:.6f}  {a['delta']:.6f}  {'yes' if c2 else 'NO '}           {rr:.6f}{'' if c1 else '  FAIL s/t'}")
mx = max(F[:-1], key=lambda x: x['delta']); mx2 = max((x for x in F[:-1] if x['k'] != 3), key=lambda x: x['delta'])
print(f"largest delta: {mx['delta']:.6f} at k = {mx['k']} (log 3/phi^2 = {L:.6f}); next {mx2['delta']:.6f} at k = {mx2['k']}; "
      f"max delta for k >= 10: {max(x['delta'] for x in F[10:-1]):.6f}, for k >= 20: {max(x['delta'] for x in F[20:-1]):.6f}")
cnt = [x['faces'] for x in F]; distinct = len(set(cnt)) == len(cnt); ok &= distinct
print(f'face counts D_0..D_{len(cnt) - 1} all distinct: {distinct}')
drops = [(x['k'], y['k'], x['r'], y['r']) for x, y in zip(F, F[1:]) if x['k'] >= 12 and y['r'] < x['r'] - e]
print(f'r(D_j) falls for j >= 12 at {len(drops)} steps; largest fall: ' + str(max(drops, key=lambda d: d[2] - d[3])))
od = [(x['k'], y['k']) for x, y in zip(F, F[1:]) if y['osc_log_R_over_r'] > x['osc_log_R_over_r'] + e]
print(f'oscillation log(R/r) rises at {len(od)} steps: {od}')
for a in A:
    nm = a['r_next_new']; pm = a['r_next_persistent']
    c = abs(a['r_next'] - min(x for x in (nm, pm) if x is not None)) < e and a['r_next'] >= min(a['r'], nm) - e
    ok &= c and (a['G1_min'] is None or a['G1_min'] > -e)
on_pers = [a['k'] + 1 for a in A if not a['r_next_on_new_face']]
print(f'r(D_j) attained only on a persistent face (never on a new one) for j = {on_pers}')
print('FINAL ok' if ok else 'FINAL FAIL: a gnomon check failed')
