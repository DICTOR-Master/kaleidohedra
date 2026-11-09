# s4_starturn.py -- the turn for stars: the flag line S*(mu) = G.Delta(mu) of every regular polytope of s1 (25: 5 Platonic,
# 4 Kepler-Poinsot, 6 convex regular 4-polytopes, 10 Schlafli-Hess), its flag-wise antipol and t_min*(mu). Study
# 2026-11-09-regular-stars-census.
# For each polytope (flag from data/flags.json, exact):
#  (a) the antipol identity on the corner sets: corners of Delta^v(mu) = h^-2 corners of Delta(c/mu), exactly, at every sample;
#  (b) t_min*(mu) = max a+.b+ (folded into G's chamber), exactly at the samples (nodes, turned nodes, midpoints, quarter points, and
#      the fixed point hR when it lies in Q(sqrt5)); the turn symmetry t_min*(mu) = t_min*(c/mu) exactly;
#  (c) control: for the convex polytopes t_min* equals the closed form of the turn theorem, E min(U_mu, U_c/mu)/h^2, exactly;
#  (d) a 4001-point float scan in log mu: argmax, symmetry, concavity of log t_min* in log mu, and the unfolded value (g = 1 only,
#      the convex formula applied to the star's own flag radii) for comparison.
# Usage: ~/geom/bin/python -u s4_starturn.py <flags.json> <out json>
import sys, json, time, math
import numpy as np
from regstar import *
import turnlib as TL
FL, OUT = sys.argv[1:3]; T0 = time.time()
rows = json.load(open(FL))
GV = {'Td': TL.tetrahedron(), 'Oh': TL.cube(), 'Ih': TL.icosahedron(), 'A4': TL.simplex4(), 'B4': TL.tesseract(),
      'F4': TL.cell24(), 'H4': TL.cell600()}
ZS = {3: (Q5(1), Q5(Fr(37, 100)), Q5(Fr(11, 100))), 4: (Q5(1), Q5(Fr(37, 100)), Q5(Fr(11, 100)), Q5(Fr(23, 1000)))}
CH = {}
for g, V in GV.items():
    M = mirrors_of(V); CH[g] = Chamber(M, ZS[len(V[0])])
def ratsqrt(x):
    if x < 0: return None
    n, d = x.numerator, x.denominator; a, b = math.isqrt(n), math.isqrt(d)
    return Fr(a, b) if a * a == n and b * b == d else None
def sqrt_q5(x):
    """exact positive square root in Q(sqrt5) if it exists, else None"""
    if x.sign() <= 0: return None
    n = ratsqrt(x.a * x.a - 5 * x.b * x.b)
    if n is None: return None
    for s_ in (n, -n):
        p2, r2_ = (x.a + s_) / 2, (x.a - s_) / 10
        p, r = ratsqrt(p2), ratsqrt(r2_)
        if p is None or r is None: continue
        for y in (Q5(p, r), Q5(p, -r), Q5(-p, r), Q5(-p, -r)):
            if y.sign() > 0 and y * y == x: return y
    return None
out = []; allok = True
for row in rows:
    q = [vp(x) for x in row['q']]; r2 = [q5p(x) for x in row['r2']]; d = len(q)
    h2, R2 = r2[-1], r2[0]; c = h2 * R2; ch = CH[row['group']]
    nodes = sorted(set(r2), key=lambda x: x.f())
    convex = row['density'] == 1
    S = set(nodes) | {c / x for x in nodes}
    S = sorted({x for x in S if h2 <= x <= R2}, key=lambda x: x.f())
    samp = list(S)
    for a, b in zip(S, S[1:]):
        samp += [(a + b) / 2, (Z(3) * a + b) / 4, (a + Z(3) * b) / 4]
    hR = sqrt_q5(c)
    if hR is not None: samp.append(hR)
    samp = sorted(set(samp), key=lambda x: x.f())
    ex = []; ok = True
    for mu in samp:
        A = delta_vertices(q, r2, mu); B = antipol_vertices(q, r2, mu)
        Bt = [scal(ONE / h2, v) for v in delta_vertices(q, r2, c / mu)]
        a_ok = {key(v) for v in B} == {key(v) for v in Bt}
        t, arg = tmin_star(q, r2, mu, ch); t2, _ = tmin_star(q, r2, c / mu, ch)
        tu, _ = tmin_star(q, r2, mu, ch, fold=False)
        e = dict(mu=q5s(mu), mu_f=mu.f(), tmin=q5s(t), tmin_f=t.f(), unfolded=q5s(tu), antipol_ok=a_ok, turn_ok=(t == t2))
        e['unfolded_is_closed_form'] = (TL.tmin_closed(mu, nodes, h2, c) == tu); ok &= e['unfolded_is_closed_form']
        if convex:
            e['closed_form'] = q5s(TL.tmin_closed(mu, nodes, h2, c)); e['closed_ok'] = (TL.tmin_closed(mu, nodes, h2, c) == t)
            ok &= e['closed_ok']
        ok &= a_ok and e['turn_ok']
        ex.append(e)
    # the ends: t_min*(R^2) = q_0+ . q_{d-1}+ / h^2 (corner and facet centre folded into one chamber)?
    endv = dotv(ch.fold(q[0]), ch.fold(q[-1])) / h2
    tR, _ = tmin_star(q, r2, R2, ch); end_ok = (tR == endv); ok &= end_ok
    # the value at the turn, exactly (sympy): R(S*(hR))^2 / h^2 over the corners of Delta(hR) (|x+| = |x|), and the closed form there
    import sympy as sp
    sq5 = sp.sqrt(5); toS = lambda x: sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sq5
    hRs = sp.sqrt(toS(c)); rS = [toS(x) for x in r2]; best = None
    for j in range(d):
        for k in range(d):
            if r2[j].f() > hRs.evalf() > r2[k].f():
                sj = (rS[j] - hRs) / (rS[j] - rS[k]); v = (1 - sj) ** 2 * rS[j] + 2 * sj * (1 - sj) * rS[k] + sj ** 2 * rS[k]
                best = v if best is None or float(v) > float(best) else best
        if r2[j].f() <= float(hRs): best = rS[j] if best is None or float(rS[j]) > float(best) else best
        else:
            v = hRs ** 2 / rS[j]; best = v if best is None or float(v) > float(best) else best
    turn_val = sp.nsimplify(sp.radsimp(sp.simplify(best / rS[-1])))
    turn_poly = sp.minimal_polynomial(best / rS[-1], sp.Symbol('x'))
    # float scan
    lm = np.linspace(math.log(h2.f()), math.log(R2.f()), 4001); M = np.exp(lm)
    tf = np.array([tmin_star_f(q, r2, m, ch) for m in M]); tu = np.array([tmin_star_f(q, r2, m, ch, fold=False) for m in M])
    tc = np.array([tmin_star_f(q, r2, c.f() / m, ch) for m in M])
    lu = np.log(tu); du = lu[2:] - 2 * lu[1:-1] + lu[:-2]
    lt = np.log(tf); dd = lt[2:] - 2 * lt[1:-1] + lt[:-2]
    i = int(np.argmax(tf)); top = np.where(tf > tf.max() - 1e-9)[0]
    rec = dict(symbol=row['symbol'], name=row['name'], group=row['group'], d=d, density=row['density'], h2=q5s(h2), R2=q5s(R2),
               c=q5s(c), hR_f=math.sqrt(c.f()), nodes=[q5s(x) for x in nodes], exact=ex, exact_ok=ok,
               scan=dict(argmax_mu=float(M[i]), argmax_over_hR=float(M[i] / math.sqrt(c.f())), tmax=float(tf[i]),
                         top_interval=[float(M[top[0]]), float(M[top[-1]])], t_at_hR=tmin_star_f(q, r2, math.sqrt(c.f()), ch),
                         t_ends=[float(tf[0]), float(tf[-1])], symmetric=float(np.abs(tf - tc).max()),
                         log_concave=bool(dd.max() < 1e-7), max_second_diff=float(dd.max()),
                         fold_gain_max=float((tf / tu).max()), unfolded_argmax_over_hR=float(M[int(np.argmax(tu))] / math.sqrt(c.f())),
                         unfolded_max=float(tu.max()), unfolded_log_concave=bool(du.max() < 1e-7)),
               end_value=q5s(endv), end_value_f=endv.f(), end_formula_ok=end_ok, turn_value=str(turn_val), turn_value_f=float(turn_val),
               turn_minpoly=str(turn_poly), turn_is_global_max=bool(float(turn_val) >= tf.max() - 1e-9),
               curve=[[float(m), float(t), float(u)] for m, t, u in zip(M[::40], tf[::40], tu[::40])])
    allok &= ok and rec['scan']['symmetric'] < 1e-9
    s = rec['scan']
    print(f"{row['symbol']:12s} {row['name'][:30]:30s} dens {row['density']:3d} exact {ok} ({len(ex)} samples) | argmax/hR {s['argmax_over_hR']:.6f}"
          f" top [{s['top_interval'][0]:.5f},{s['top_interval'][1]:.5f}] hR {math.sqrt(c.f()):.5f} tmax {s['tmax']:.6f} t(hR) {s['t_at_hR']:.6f}"
          f" ends {s['t_ends'][0]:.4f},{s['t_ends'][1]:.4f} logconc {s['log_concave']} ({s['max_second_diff']:.2e}) foldgain {s['fold_gain_max']:.4f}"
          f" | end {q5s(endv)} turn {turn_val} unfolded: argmax/hR {s['unfolded_argmax_over_hR']:.6f} logconc {s['unfolded_log_concave']} | {round(time.time() - T0)} s", flush=True)
    out.append(rec); json.dump(out, open(OUT, 'w'), indent=1)
print('FINAL ok' if allok else 'FINAL FAIL: an exact check failed (antipol, turn symmetry or the convex closed form)')
