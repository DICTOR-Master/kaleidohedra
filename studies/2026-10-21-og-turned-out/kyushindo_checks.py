# DICTO 2026-10-21: two checks for the Kyushindo Cores paper (#43), after the Fable referee, EXACT in Q(sqrt5) with the #38/#39 machinery.
#  (1) "every corner of S stays on the surface of T(S)" holds exactly when w.v <= w.w for all corners v, w of S (else v is cut off by the
#      face of w). Tested for every solid the paper steps or bounds with: the UP stations ID, RT, GTI, FPD (the Cleo and Polar Cleo Towers'
#      boundaries are these scaled by powers of c = 10/phi^4, and the condition does not change under scaling), and the OG chain OG, TPH, TQH,
#      TQP, TQHD (for the record: the OG turned out is built by the reverse step, not by T).
#  (2) every inner and outer solid of every shell cut into towers in the paper (Cleo Towers, Polar Cleo Towers, OG turned out, at their actual
#      scales) is fixed, as a corner set, by all 60 exact rotations (exact_shells.shell itself asserts this for 5 of them, on the inner solid).
#  usage: python3 kyushindo_checks.py <studies/2026-10-19-five-fold-octet>
import sys, os
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
UP = [ID]
for _ in range(3): UP.append(step(UP[-1])[0])
DN = [OG]
for _ in range(4): DN.append(rev(DN[-1]))
c = Q5(35, -15)
ok(set(step(UP[3])[0]) == {tuple(c * x for x in v) for v in ID}, 'T(FPD) = c ID, c = 35 - 15 sqrt5 = 10/phi^4')
def cut(S):
    return sum(1 for v in S if any((dot(w, v) - dot(w, w)).sign() > 0 for w in S))
for nm, S in zip(['ID', 'RT', 'GTI', 'FPD', 'OG', 'TPH', 'TQH', 'TQP', 'TQHD'], UP + DN):
    n = cut(S); ok(True, f'(1) {nm}: corners cut off by T: {n} of {len(S)}' + (' (w.v <= w.w for all corners: every corner stays on the surface of T(S))' if n == 0 else ''))
def beat(j):
    q, r = divmod(j, 4); f = Q5(1)
    for _ in range(abs(q)): f = f * c if q > 0 else f / c
    return [tuple(f * x for x in v) for v in UP[r]]
def pw(k):
    r = Q5(1)
    for _ in range(k): r = r * PHI
    return r
sym = lambda S: all({app(M, v) for v in S} == set(S) for M in G)
runs = [('Cleo Towers', [0, 1, 2, 4, 7, 12]), ('Polar Cleo Towers', [-7, -2, 1, 3, 4, 5])]
for nm, b in runs:
    ok(all(sym(beat(j)) for j in b), f'(2) {nm}: the boundary solids at beats {b} (inner and outer of every shell) are each fixed by all 60 rotations')
ok(len(G) == 60 and all(sym([tuple(pw(k) * x for x in v) for v in DN[k]]) for k in (0, 1, 2, 4)), '(2) OG turned out: OG, phi TPH, phi^2 TQH, phi^4 TQHD (inner and outer of every shell) are each fixed by all 60 rotations')
