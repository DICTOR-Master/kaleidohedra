"""LEAD 6 (12 Nov 2026): #43 Theorem 3 (beat k <-> 5 - k, fixed point 5/2) written as a TURN ROW of the bridge table, verified exactly
in Q(sqrt5). The proof itself is bird 4 of studies/2026-11-09-icosahedral-line (ledger: SETTLED, never retried); this script checks
the row's own entries, in the same columns as the other turn rows (line, antipol rule, turn, fixed point, what sits there, walls/
measure, controls):
  line      beat line of Universal PiTet: S_0 = ID (circumradius phi), S_{k+1} = T(S_k) = {x : v.x <= v.v, v a corner of S_k};
            hop S_{k+4} = c S_k, c = 35 - 15 sqrt5 (so S_k is defined for every integer k)
  antipol   polar about rho^2 = c^m (15 - 5 sqrt5):  polar(S_k) = S_{5 + 4m - k}
  turn      k -> 5 - k (m = 0); with the hop the turn centres are exactly 1/2 + 2Z (5/2, 1/2 = the phi^2 companion, 9/2, ...)
  fixed     5/2: no station is self-antipol; the antipol PAIR GTI | FPD, GTI inscribed in the reference sphere (every corner at
            rho^2), FPD circumscribed about it (every facet at distance rho) -- the discrete form of "every face tangent"
  measure   shell ratios t_k = min{t : S_k in t S_{k-1}}: t_k = t_{6-k}; the fixed shells (centres 1/2, 5/2) carry the largest ratios
Controls: POSITIVE, the continuous C-O row with the same row code: P_mu^v = P_{3/mu}, fixed point sqrt3 = every face tangent;
NEGATIVE, no turn centre at 3/2 + 2Z (polar(S_k) is homothetic only to S_j with j = 5 - k mod 4; the four residues are pairwise
non-homothetic), no station self-polar, the wrong turn constant (k -> 4 - k) fails, and the unit sphere maps no station onto a station."""
import sys, os, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-09-icosahedral-line', 'scripts'))
from q5 import *
t0 = time.time(); checks = {}
def key(v): return tuple((x.a, x.b) for x in v)
def cset(C): return frozenset(key(x) for x in C)
# stations, exactly as bird 4 builds them
mids = set()
for i, a in enumerate(AX5):
    for b in AX5[i + 1:]:
        d = sub(a, b)
        if dot(d, d) == Q5(4): mids.add(scl(Q5(Fr(1, 2)), add(a, b)))
ID = sorted(mids, key=lambda v: tuple(x.f() for x in v))
def T(C): return [x for x, _ in corners([(v, dot(v, v)) for v in C])]
def planes_of(C): return [(y, ONE) for y, _ in corners([(v, ONE) for v in C])]
def polar(C, rho2): return [x for x, _ in corners([(v, rho2) for v in C])]
base = [ID]
for k in range(1, 4): base.append(T(base[-1]))
c = Q5(35, -15)
def S(k):                      # S_k for every integer k, by the hop S_{k+4} = c S_k
    m, r = divmod(k, 4); f = ONE
    for _ in range(abs(m)): f = f * c if m > 0 else f / c
    return [scl(f, v) for v in base[r]]
checks['hop: T(S_3) = c S_0 (so S_k is defined for all k by S_{k+4} = c S_k)'] = cset(T(base[3])) == cset(S(4))
names = {0: 'ID', 1: 'RT', 2: 'GTI', 3: 'FPD'}
print('corners per residue:', {names[r]: len(base[r]) for r in range(4)})
rho2 = Q5(15, -5)
# ANTIPOL rule of the row, for m = -1, 0, 1 and k = -4..9
ok = True; n = 0
for m in (-1, 0, 1):
    r2 = rho2
    for _ in range(abs(m)): r2 = r2 * c if m > 0 else r2 / c
    for k in range(-4, 10):
        ok &= cset(polar(S(k), r2)) == cset(S(5 + 4 * m - k)); n += 1
checks[f'antipol rule polar_(c^m rho^2)(S_k) = S_(5+4m-k), rho^2 = 15 - 5 sqrt5, m = -1, 0, 1, k = -4..9 ({n} cases)'] = ok
checks['turn k -> 5 - k is an involution on the line and conjugates T to T^-1: polar(T(S_k)) = T^-1(polar(S_k)), k = 0..5'] = \
    all(cset(polar(T(S(k)), rho2)) == cset(S(5 - k - 1)) for k in range(6))
checks['companion: polar_(phi^2)(S_k) = S_(1-k), k = -3..4 (centre 1/2 = 5/2 - 2: the same turn class)'] = \
    all(cset(polar(S(k), PHI * PHI)) == cset(S(1 - k)) for k in range(-3, 5))
# FIXED POINT 5/2: the antipol pair GTI | FPD
rG = set(dot(v, v) for v in S(2)); rF = set(d * d / dot(n_, n_) for n_, d in planes_of(S(3)))
checks['fixed point 5/2: GTI inscribed (every corner at radius^2 rho^2) and FPD circumscribed (every facet at distance^2 rho^2)'] = \
    rG == {rho2} and rF == {rho2}
checks['the same pair one hop down: ID inscribed in phi^2, RT circumscribed about it (centre 1/2)'] = \
    set(dot(v, v) for v in S(0)) == {PHI * PHI} and set(d * d / dot(n_, n_) for n_, d in planes_of(S(1))) == {PHI * PHI}
# NEGATIVE: homothety classes -- polar_1(S_k) is homothetic to S_j only for j = 5 - k (mod 4)
def shape(C):                  # homothety-invariant signature: sorted squared radii divided by the largest, plus the corner count
    R = sorted(set(dot(v, v) for v in C), key=lambda q: q.f()); top = R[-1]
    return (len(C), tuple(r / top for r in R))
def homothetic(A, B):          # exact: same signature and A = s B with s^2 = (max r_A^2)/(max r_B^2), s found from a matching corner
    if shape(A) != shape(B): return False
    ra = max((dot(v, v) for v in A), key=lambda q: q.f()); rb = max((dot(v, v) for v in B), key=lambda q: q.f())
    va = [v for v in A if dot(v, v) == ra]
    for vb in (v for v in B if dot(v, v) == rb):
        # s from the first nonzero coordinate of a matching direction
        for v in va:
            i = next(j for j in range(3) if vb[j] != ZERO)
            s = v[i] / vb[i]
            if s > ZERO and scl(s, vb) == v and cset([scl(s, w) for w in B]) == cset(A): return True
        break
    return False
sig = [shape(base[r]) for r in range(4)]
print('signatures (corner count, squared radii / largest):', {names[r]: (sig[r][0], [q.f() for q in sig[r][1]]) for r in range(4)})
print('   RT and FPD share the signature (32 corners, same radius ratio):', sig[1] == sig[3], '-- the exact homothety test decides')
checks['the four residues ID, RT, GTI, FPD are pairwise non-homothetic (exact homothety test, positive scale)'] = \
    all(not homothetic(base[i], base[j]) for i in range(4) for j in range(4) if i != j) and all(homothetic(base[i], base[i]) for i in range(4))
hom = {(k, j): homothetic(polar(base[k], ONE), base[j]) for k in range(4) for j in range(4)}
print('polar_1(S_k) homothetic to S_j:', sorted(kj for kj, h in hom.items() if h))
checks['polar(S_k) ~ S_j exactly when j = 5 - k mod 4: every turn of the line is k -> 5 + 4m - k, centres 1/2 + 2Z only'] = \
    all(h == ((k + j) % 4 == 1) for (k, j), h in hom.items())
checks['NEGATIVE: no turn centre at 3/2 (polar(RT) not homothetic to GTI; polar(ID) not homothetic to FPD)'] = not hom[(1, 2)] and not hom[(0, 3)]
checks['NEGATIVE: no station is self-antipol (5 - k = k has no integer solution; polar_rho(S_k) != S_k, k = 0..5)'] = \
    all(cset(polar(S(k), rho2)) != cset(S(k)) for k in range(6))
checks['NEGATIVE: the wrong turn k -> 4 - k fails at every k = 0..4'] = all(cset(polar(S(k), rho2)) != cset(S(4 - k)) for k in range(5))
checks['NEGATIVE: about the unit sphere no station maps onto a station (k, j in -4..9)'] = \
    all(cset(polar(S(k), ONE)) != cset(S(j)) for k in range(4) for j in range(-4, 10))
# MEASURE: shell ratios
def ratio(Cin, Cout):
    best = None; pl = planes_of(Cout)
    for v in Cin:
        for n_, d in pl:
            q = dot(n_, v) / d
            if best is None or q > best: best = q
    return best
tk = {k: ratio(S(k), S(k - 1)) for k in range(-2, 8)}
for k in range(1, 5): print(f'shell {k - 1}->{k}: t = {tk[k]} = {tk[k].f():.9f}')
checks['shell ratios: t_k = t_(6-k) for k = -2..7 (the turn reflects the shells)'] = all(tk[k] == tk[6 - k] for k in range(-2, 8) if 6 - k in tk)
checks['shell values exact: t_1 = (5 - sqrt5)/2, t_2 = t_4 = 3/phi^2, t_3 = 5 - 5 sqrt5/3'] = \
    tk[1] == Q5(Fr(5, 2), Fr(-1, 2)) and tk[2] == tk[4] == Q5(3) / (PHI * PHI) and tk[3] == Q5(5, Fr(-5, 3))
checks['the fixed shells (centres 1/2 and 5/2) carry the two largest ratios'] = min(tk[1], tk[3]) > max(tk[2], tk[4])
# POSITIVE control: the continuous C-O row with the same antipol rule (normals e_i with d = 1, (+-1,+-1,+-1) with d = mu)
def P_mu(mu):
    pl = [(tuple(Q5(int(i == j)) * s for j in range(3)), ONE) for i in range(3) for s in (ONE, -ONE)]
    pl += [((Q5(a), Q5(b), Q5(e)), mu) for a in (1, -1) for b in (1, -1) for e in (1, -1)]
    return pl
def antipol(pl): return [(n_, dot(n_, n_) / d) for n_, d in pl]
def cs(pl): return cset([x for x, _ in corners(pl)])
co_ok = all(cs(antipol(P_mu(Q5(mu)))) == cs(P_mu(Q5(3) / Q5(mu))) for mu in (Fr(5, 4), Fr(3, 2), Fr(2), Fr(5, 2)))
checks['POSITIVE control (C-O row): antipol(P_mu) = P_(3/mu) at mu = 5/4, 3/2, 2, 5/2'] = co_ok
for k, v in checks.items(): print(('  ok   ' if v else '  FAIL ') + k)
print(f'time {time.time() - t0:.0f} s')
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
