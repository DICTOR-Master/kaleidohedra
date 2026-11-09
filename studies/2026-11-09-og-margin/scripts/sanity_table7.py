# DICTO #43 Conjecture 1, study 2026-11-09: known-case sanity. The exact t_min(D_k), k = 0..8, of this study's exact_family.py must
# equal, digit for digit, the exact values of #43 Table 7 as logged by the 2026-10-21 nesting-proof run (tmin-exact.log).
# usage: python3 sanity_table7.py <nesting-proof/tmin-exact.log> <data/exact-family.json>
import sys, re, json
old = {}
for line in open(sys.argv[1]):
    m = re.match(r'PASS t_min\(D_(\d+)\) = [0-9.]+ = (\S+) is the exact max', line)
    if m: old[int(m.group(1))] = m.group(2)
new = json.load(open(sys.argv[2]))['k']
ok = True
for k in range(9):
    a, b = old.get(k), new.get(str(k), {}).get('t_min_exact')
    same = a is not None and a == b; ok &= same
    print(f'k = {k}: {"identical" if same else "DIFFERENT"} ({len(a or "")} characters)')
print('FINAL ok' if ok else 'FINAL FAIL: Table 7 not reproduced exactly')
