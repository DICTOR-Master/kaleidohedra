"""Step 3 (DICTO Yantra, over Q(sqrt5)): back-solve every candidate u (data/roots-D.json) and decide admissibility with certified balls (FLINT/Arb, python-flint).

For each candidate root u* (dyadic interval of width ~2^-1400 from s2_isolate.py, certified by exact signs), let U be a ball holding it.
  The coefficients of G, H1, D, A, B lie in K = Q(sqrt5); each is a + b s with s = sqrt5 evaluated as an Arb ball (arb(5).sqrt()).
  v = c/u with c = 2 sqrt5 - 4 (the Cleo-Antonius, u v = 2/phi^3).
  (1) t: all complex roots of A(t, U) (degree 20 in t; leading coefficient certified nonzero) are isolated (acb_poly.roots); a root is
      certified real when its ball meets the real axis and meets no other root ball's conjugate.  Admissibility needs 0 < t < v
      (t > 0: t1's corner to the right; t < v: b1 < b3).  Real roots certified outside (0, v) are rejected; a ball meeting 0 or v
      triggers more precision.
  (2) for each real t in (0, u): B(t, U) is evaluated; if its ball excludes 0, (u*, t) is not a common zero of A and B: rejected.
  (3) survivors: S from G(U, S) = 0 (both roots); S must be real with R < S < 1 (b7 < b9 < 1); H1 and D are evaluated; a ball
      excluding 0 rejects.
  (4) a survivor of (3) is proved to be a true solution of G = H1 = D = 0 by the Krawczyk test in (u, t, S) (unique solution in the
      box), and the whole yantra is rebuilt in ball arithmetic from the box and tested against #103 Theorem 1's admissibility
      (strict order b1 < ... < b9, w_i > 0, apexes on the correct side, corners in the closed disc: t1, t3, t7, t9 exactly on the circle
      by construction, the other five strictly inside) and the sign conditions that undo the squaring in (d) (b5 < 1/2 < Q).
Controls: positive, the known yantra (Theorem 9's interval) must reach (4) and pass; negative (a) the same u with B + 1 in place of B
must be rejected at (2); (b) a perturbed u (u* + 2^-200) must be rejected; (c) near miss: the undistorted Cleo-Antonius (u = 2/phi^2 =
3 - sqrt5 exactly, v = 1/phi: the Cleo-Icos cone above and the Antonius side below, #103 sec. 9.1 with beta = 0), which meets Huet's
conditions, (b) and (c) but not (d): A(t, 3 - sqrt5) must have a real root in (0, v) that the B test rejects; its bindu offset is reported.
FINAL ok iff every candidate is decided, exactly one admissible solution is found, it is Theorem 9's, and the controls behave."""
import json, os, sys, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = lambda *p: os.path.join(ROOT, *p)
import flint
from flint import arb, acb, fmpq, arb_mat
flint.ctx.prec = 2400
polys = json.load(open(D('data', 'polys-D.json'))); census = json.load(open(D('data', 'roots-D.json')))
P_ = {k: [(tuple(e), (int(c[0]), int(c[1]))) for e, c in polys[k]] for k in ('G', 'H1', 'D', 'A', 'B')}
def kval(c):                                             # a + b sqrt5 as a ball at the working precision
    return c[0] + c[1] * arb(5).sqrt() if c[1] else arb(c[0])
def cval(): return 2 * arb(5).sqrt() - 4                 # c = 2/phi^3
def deriv(p, var): return [(tuple(e[i] - (i == var) for i in range(3)), (c[0] * e[var], c[1] * e[var])) for e, c in p if e[var] > 0]
def ev(p, x):                                            # x = (u, t, S) balls; plain power sums (balls are tiny)
    pw = [{}, {}, {}]
    def pk(i, k):
        if k not in pw[i]: pw[i][k] = x[i] ** k
        return pw[i][k]
    tot = 0
    for e, c in p:
        tot += kval(c) * pk(0, e[0]) * pk(1, e[1]) * pk(2, e[2])
    return tot
def coeffs_in(p, var, x):                                # coefficients of p in variable var (others evaluated at x)
    deg = max(e[var] for e, c in p); out = [0] * (deg + 1)
    for e, c in p:
        term = kval(c)
        for i in range(3):
            if i != var and e[i]: term = term * x[i] ** e[i]
        out[e[var]] += term
    return [arb(0) + c if not isinstance(c, arb) else c for c in out]
def ball(k, a, b):                                       # dyadic interval [a/2^k, b/2^k] as an arb ball
    lo, hi = fmpq(int(a), 1 << k), fmpq(int(b), 1 << k)
    return arb((lo + hi) / 2, (hi - lo) / 2)
def real_roots_in(coeffs, lo, hi):
    """certified real roots of the polynomial (arb coefficients, low to high) in the open interval (lo, hi).
    returns (list of arb, undecided flag)."""
    while abs(coeffs[-1]).upper() == 0 and len(coeffs) > 1: coeffs = coeffs[:-1]
    if coeffs[-1].contains(0): return None, 'leading coefficient not certified nonzero'
    rts = flint.acb_poly([acb(c) for c in coeffs]).roots(tol=arb(2) ** (-(flint.ctx.prec // 3)), maxprec=4 * flint.ctx.prec)   # isolating balls refined
    n = len(rts); out = []
    for i, r in enumerate(rts):
        if not r.imag.contains(0): continue
        cj = acb(r.real, -r.imag)
        if any(j != i and cj.overlaps(rts[j]) for j in range(n)): return None, 'real/nonreal undecided'
        x = r.real
        if (x < lo) or (x > hi): continue                    # certified outside (arb comparison true for the whole ball)
        if not ((x > lo) and (x < hi)): return None, f'root ball {x} meets the end of the range'
        out.append(x)
    return out, None
def construct(u, t, S):
    """the yantra from (u, t, S), the same construction as s1_system.py (v = c/u)."""
    v = cval() / u; one = arb(1)
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: arb(0)}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return b, w, a
def admissible(u, t, S):
    b, w, a = construct(u, t, S); fails = []; undecided = []
    def need(cond_true, cond_false, label):
        if cond_true: return
        (fails if cond_false else undecided).append(label)
    for i in range(1, 9): need(b[i] < b[i + 1], b[i] >= b[i + 1], f'b{i} < b{i + 1}')
    for i in range(1, 10): need(w[i] > 0, w[i] <= 0, f'w{i} > 0')
    for i in range(1, 10):
        if i <= 5: need(a[i] > b[i], a[i] <= b[i], f'apex t{i} below its base')
        else: need(a[i] < b[i], a[i] >= b[i], f'apex t{i} above its base')
    for i in (2, 4, 5, 6, 8):
        p = w[i]**2 + b[i]**2 - b[i]; need(p < 0, p >= 0, f'corner t{i} inside the disc')
    need(b[5] < arb(1) / 2, b[5] >= arb(1) / 2, 'b5 < 1/2 (centre below the bindu base)')
    need(b[6] > arb(1) / 2, b[6] <= arb(1) / 2, 'Q > 1/2 (centre above the bindu apex, so inside)')
    return fails, undecided, (b, w, a)
def krawczyk(x0, rad):
    """Krawczyk test for F = (G, H1, D) on the box x0 +- rad; True = exactly one solution in the box."""
    F = [P_['G'], P_['H1'], P_['D']]; J = [[deriv(f, j) for j in range(3)] for f in F]
    X = [arb(c.mid(), rad) for c in x0]; y = [arb(c.mid()) for c in x0]
    Fy = [ev(f, y) for f in F]
    Jy = arb_mat([[ev(J[i][j], y) for j in range(3)] for i in range(3)]).mid()
    Y = Jy.inv().mid()
    JX = arb_mat([[ev(J[i][j], X) for j in range(3)] for i in range(3)])
    M = arb_mat([[1 if i == j else 0 for j in range(3)] for i in range(3)]) - Y * JX
    d = arb_mat([[X[i] - y[i]] for i in range(3)]); fy = arb_mat([[Fy[i]] for i in range(3)])
    K = arb_mat([[y[i]] for i in range(3)]) - Y * fy + M * d
    inside = all(X[i].contains_interior(K[i, 0]) for i in range(3))
    return inside, [K[i, 0] for i in range(3)], X
def census_at(U, Bpoly=None, label=''):
    """returns a list of (status, detail)."""
    Bp = Bpoly or P_['B']; out = []
    ts, err = real_roots_in(coeffs_in(P_['A'], 1, (U, None, None)), arb(0), cval() / U)
    if err: return [('UNDECIDED', 't-roots: ' + err)]
    if not ts: return [('REJECT', 'A(t, u) has no real root with 0 < t < v')]
    for tau in ts:
        Bv = ev(Bp, (U, tau, arb(0)))
        if not Bv.contains(0): out.append(('REJECT', f't = {tau.str(12, radius=False)}: B = {Bv.str(5, radius=False)} != 0')); continue
        Rr = arb(1) / (1 + U**2)
        Ss, err = real_roots_in(coeffs_in(P_['G'], 2, (U, None, None)), Rr, arb(1))
        if err: out.append(('UNDECIDED', 'S-roots: ' + err)); continue
        if not Ss: out.append(('REJECT', f't = {tau.str(12, radius=False)}: no S root of G in (R, 1)')); continue
        for Sv in Ss:
            h1 = ev(P_['H1'], (U, tau, Sv)); dd = ev(P_['D'], (U, tau, Sv))
            if not h1.contains(0) or not dd.contains(0):
                out.append(('REJECT', f't = {tau.str(12, radius=False)}, S = {Sv.str(12, radius=False)}: H1 = {h1.str(5, radius=False)}, D = {dd.str(5, radius=False)}')); continue
            out.append(('SURVIVOR', (tau, Sv)))
    return out
ok = True; survivors = []
undecided_total = 0; ncand = sum(len(c['roots01']) for c in census); done = 0
st1 = json.load(open(D('inputs', 'stage1-D.json')))
records = []
for c in census:
    for ridx, (k, a, b) in enumerate(c['roots01']):
        for prec in (2400, 4800, 9600):
            flint.ctx.prec = prec
            U = ball(k, a, b)                             # built at the working precision
            res = census_at(U)
            if not any(s == 'UNDECIDED' for s, _ in res): break
        say(f'factor {c["index"]} (degree {c["degree"]}) root {ridx}: u = {U.str(15, radius=False)}')
        for s, det in res:
            if s == 'SURVIVOR':
                tau, Sv = det
                say(f'   SURVIVOR: t = {tau.str(20, radius=False)}, S = {Sv.str(20, radius=False)}')
                survivors.append((c['index'], ridx, U, tau, Sv))
            else:
                say(f'   {s}: {det}')
                if s == 'UNDECIDED': undecided_total += 1
        records.append({'factor': c['index'], 'degree': c['degree'], 'root': ridx, 'u': U.str(30, radius=False),
                        'outcome': [(s, det if isinstance(det, str) else 'survivor') for s, det in res]})
        done += 1; print(f'PROGRESS {done / ncand:.3f} candidate {done}/{ncand}')
say('undecided:', undecided_total, ' survivors:', len(survivors))
ok = undecided_total == 0
final = []
flint.ctx.prec = 2400
for fi, ri, U, tau, Sv in survivors:
    inside, K, X = krawczyk((U, tau, Sv), arb(10) ** -300)
    say(f'Krawczyk on the box of radius 1e-300 around ({fi}, {ri}): unique solution certified = {inside}')
    if not inside: ok = False; continue
    fails, und, (b, w, a) = admissible(*K)
    say('   admissibility fails:', fails, ' undecided:', und)
    in10 = census[fi]['is_f160'] and census[fi].get('theorem9_root_index') == ri
    say(f'   this is Theorem 9\'s root of f160: {in10}')
    if not fails and not und: final.append((fi, ri, in10, K, b, w))
    elif und: ok = False
say('ADMISSIBLE SOLUTIONS:', len(final))
ok = ok and len(final) == 1 and final[0][2]
if final:
    fi, ri, in10, K, b, w = final[0]
    say('   u =', K[0].str(40, radius=False), ' t =', K[1].str(40, radius=False), ' S =', K[2].str(40, radius=False))
# ---------------- controls ----------------
flint.ctx.prec = 2400
c348 = [c for c in census if c['is_f160']][0]; k, a, b = c348['roots01'][c348['theorem9_root_index']]; U0 = ball(k, a, b)
Bplus = P_['B'] + [((0, 0, 0), (1, 0))]
negA = census_at(U0, Bplus)
negA_ok = all(s == 'REJECT' for s, _ in negA)
say('negative control (a) B + 1 at the true u:', negA_ok, [s for s, _ in negA])
negB = census_at(U0 + arb(2) ** -200)
negB_ok = all(s == 'REJECT' for s, _ in negB)
say('negative control (b) u + 2^-200:', negB_ok, [s for s, _ in negB])
UCA = 3 - arb(5).sqrt()                                  # undistorted Cleo-Antonius: u = 2/phi^2, v = 1/phi
ts, err = real_roots_in(coeffs_in(P_['A'], 1, (UCA, None, None)), arb(0), cval() / UCA)
rh = census_at(UCA)
rh_ok = (err is None and len(ts or []) >= 1 and all(s_ == 'REJECT' for s_, d in rh) and any('B =' in d for s_, d in rh))
miss = []
for tau in (ts or []):                                   # bindu offset: incircle centre depth minus 1/2, for each (b)-(c) yantra
    Ss, e2 = real_roots_in(coeffs_in(P_['G'], 2, (UCA, None, None)), arb(1) / (1 + UCA**2), arb(1))
    for Sv in (Ss or []):
        h1 = ev(P_['H1'], (UCA, tau, Sv))
        if not h1.contains(0): continue                    # not on the closing curve
        b_, w_, a_ = construct(UCA, tau, Sv); hh = b_[6] - b_[5]; hw_ = w_[1] * hh / (b_[6] - b_[1])
        r_ = hw_ * hh / (hw_ + (hw_**2 + hh**2).sqrt())
        shape = [f_ for f_ in admissible(UCA, tau, Sv)[0] if not f_.startswith(('b5 < 1/2', 'Q > 1/2'))]   # Theorem 1 admissibility only
        miss.append({'t': tau.str(10, radius=False), 'S': Sv.str(10, radius=False), 'bindu_centre_minus_half': (b_[5] + r_ - arb(1) / 2).str(5, radius=False),
                     'theorem1_admissible': not shape, 'fails': shape})
say('control (c) undistorted Cleo-Antonius, u = 3 - sqrt5: real t roots of A in (0, v):', [x.str(12, radius=False) for x in (ts or [])],
    '; outcome:', rh, '; bindu centre offset where H1 also vanishes (if any):', miss, '; ok:', rh_ok)
json.dump({'records': records, 'admissible': [{'factor': f[0], 'root': f[1], 'theorem10': f[2], 'u': f[3][0].str(60, radius=False),
           't': f[3][1].str(60, radius=False), 'S': f[3][2].str(60, radius=False),
           'b': {i: f[4][i].str(40, radius=False) for i in f[4]}} for f in final],
           'controls': {'B_plus_1': negA_ok, 'u_perturbed': negB_ok, 'cleo_antonius_undistorted': rh_ok, 'bindu_offset': miss}}, open(D('data', 'census-D.json'), 'w'), indent=1, default=str)
ok = ok and negA_ok and negB_ok and rh_ok
print('FINAL ok' if ok else 'FINAL FAIL: see above')
