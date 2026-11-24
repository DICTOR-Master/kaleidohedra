"""Compare the outputs in data/ term by term; write the b-files. Run: python3 compare.py"""
import re, ast
def line(f, prefix=None):
    for s in open('data/' + f):
        if prefix is None or s.startswith(prefix):
            s = s.split(':', 1)[1] if (prefix and ':' in s) else s
            s = s.strip().strip('[]')
            if re.fullmatch(r'[-\d, ]+', s): return [int(t) for t in s.split(',')]
ok = True
# Entry 2
asis = line('o_e2_asis200.txt'); asis57 = line('o_e2_asis57.txt')
geo = {k: line('o_e2_geo.txt', k) for k in ['bilayer1 B (h) lower', 'bilayer1 B (h) upper', 'bilayer3 C (h) lower', 'bilayer3 C (h) upper', 'bilayer0 A (c) lower', 'bilayer2 A (c) upper']}
gf = line('o_pari.txt', 'entry2_gf')
c3 = line('o_oeis_checks.txt', 'C3 4H site (bilayer 1 [B, h], atom 0)')
c3c = line('o_oeis_checks.txt', 'C3 4H site (bilayer 0 [A, c], atom 0)')
e2 = [ok]
t = [asis57 == asis[:58], all(geo[k] == asis for k in geo if '(h)' in k), gf == asis, c3 == asis[:len(c3)],
     geo['bilayer0 A (c) lower'] == geo['bilayer2 A (c) upper'] == (c3c + geo['bilayer0 A (c) lower'][len(c3c):]) ]
print('Entry 2: program as written (n<=57) prefix of n<=200 run:', t[0]); print('Entry 2: geometric method, all 4 h sites (B, C; lower, upper) == program, n = 0..200:', t[1])
print('Entry 2: empirical g.f. == program, n = 0..200:', t[2]); print('Entry 2: study oeis_checks.py C3 4H h site rerun == program, n = 0..%d:' % (len(c3) - 1), t[3])
print('Entry 2: c-site check (A bilayers) consistent:', t[4])
ok &= all(t)
with open('../../papers/oeis-submissions/working/b-entry2-4H.txt', 'w') as f:
    for n, v in enumerate(asis): f.write(f'{n} {v}\n')
# Sweep 1
pf = line('o_pyro.txt', '1,0'); lg = line('o_lg.txt', '1,0'); wk = line('o_walks.txt', 'closed walks per site'); pa = line('o_pari.txt', 'sweep1_formula'); pg = line('o_pari.txt', 'sweep1_gf')
t = [len(pf) == 41 and pf == lg, wk == pf[:31], pa == pf, pg == pf]
print('Sweep 1: study pyrochlore.py (formula) == fresh line-graph DP, n = 0..40:', t[0]); print('Sweep 1: study walks.py direct DP == formula, n = 0..30:', t[1])
print('Sweep 1: PARI formula program == formula, n = 0..40:', t[2]); print('Sweep 1: PARI g.f. expansion == formula, n = 0..40:', t[3])
ok &= all(t)
with open('../../papers/oeis-submissions/working/b-sweep1-pyrochlore.txt', 'w') as f:
    for n, v in enumerate(pf): f.write(f'{n} {v}\n')
print('FINAL ok' if ok else 'FINAL FAIL')
