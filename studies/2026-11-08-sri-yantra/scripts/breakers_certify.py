"""The condition breakers of #103 (DICTO 15 Nov 2026: "maybe the yantra diagrams could be used to construct the nearby inadmissible
condition breakers"). Each breaker is rebuilt in Arb ball arithmetic (python-flint) from the two uniqueness studies of 15 Nov 2026:
  studies/2026-11-15-yantra-uniqueness       (Kulaichev's conditions, polynomials G, H1, D over Q in (u, t, S), v = u)
  studies/2026-11-15-dicto-yantra-uniqueness (DICTO Yantra conditions, polynomials over Q(sqrt5), v = (2 sqrt5 - 4)/u)
For the true solutions of G = H1 = D = 0 the seed (u, t, S) from the study's census log is refined by Newton steps and then certified
by the Krawczyk test (exactly one solution in a box of radius 1e-100); the near miss u = 3 - sqrt5 (undistorted Cleo-Antonius, no
condition (d)) is certified the same way in (t, S) on G = H1 = 0 with u exact. The yantra is rebuilt with the studies' construct()
(copied line for line from their s3_backsolve.py) and each failed condition is measured as a certified ball. Every failure list must
equal the study's (guard). Rh345 (u = 3/4) is read from its stored exact coordinates (rhombus345-coordinates.json).
usage: python3 breakers_certify.py      (writes ../data/breakers.json; FINAL ok iff every certificate and guard passes)"""
import json, os
import flint
from flint import arb, arb_mat
flint.ctx.prec = 1000
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '..', '..')
KDIR = os.path.join(ST, '2026-11-15-yantra-uniqueness'); DDIR = os.path.join(ST, '2026-11-15-dicto-yantra-uniqueness')
S5 = lambda: arb(5).sqrt()


def load_polys(path, field):
    p = json.load(open(path))
    if field == 'Q': return {k: [(tuple(e), (int(c), 0)) for e, c in p[k]] for k in ('G', 'H1', 'D')}
    return {k: [(tuple(e), (int(c[0]), int(c[1]))) for e, c in p[k]] for k in ('G', 'H1', 'D')}


def kv(c): return c[0] + c[1] * S5() if c[1] else arb(c[0])
def deriv(p, var): return [(tuple(e[i] - (i == var) for i in range(3)), (c[0] * e[var], c[1] * e[var])) for e, c in p if e[var] > 0]


def ev(p, x):
    pw = [{}, {}, {}]
    def pk(i, k):
        if k not in pw[i]: pw[i][k] = x[i] ** k
        return pw[i][k]
    tot = arb(0)
    for e, c in p: tot += kv(c) * pk(0, e[0]) * pk(1, e[1]) * pk(2, e[2])
    return tot


def construct(u, t, S, v):
    """#103 construction, line for line as s3_backsolve.py of both studies (only v differs: v = u, or v = (2 sqrt5 - 4)/u)."""
    one = arb(1)
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
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q),
         8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return b, w, a


def fails_of(b, w, a):
    """#103 Theorem 1 admissibility and the side of the centre, with the studies' labels; every comparison must be decided."""
    f = []; und = []
    def need(ok, bad, label):
        if ok: return
        (f if bad else und).append(label)
    for i in range(1, 9): need(b[i] < b[i + 1], b[i] >= b[i + 1], f'b{i} < b{i + 1}')
    for i in range(1, 10): need(w[i] > 0, w[i] <= 0, f'w{i} > 0')
    for i in range(1, 10):
        if i <= 5: need(a[i] > b[i], a[i] <= b[i], f'apex t{i} below its base')
        else: need(a[i] < b[i], a[i] >= b[i], f'apex t{i} above its base')
    for i in (2, 4, 5, 6, 8):
        p = w[i]**2 + b[i]**2 - b[i]; need(p < 0, p >= 0, f'corner t{i} inside the disc')
    need(b[5] < arb(1) / 2, b[5] >= arb(1) / 2, 'b5 < 1/2 (centre below the bindu base)')
    need(b[6] > arb(1) / 2, b[6] <= arb(1) / 2, 'Q > 1/2 (centre above the bindu apex, so inside)')
    return f, und


def bindu(b, w):
    """the bindu triangle (t1's legs, t5's base): half-width at t5's base, inradius, incentre depth, exradius opposite t1's apex"""
    hh = b[6] - b[5]; hw = w[1] * hh / (b[6] - b[1]); L = (hw**2 + hh**2).sqrt()
    r = hw * hh / (hw + L); rex = hw * hh / (L - hw)
    return dict(hw=hw, r=r, inc=b[5] + r, rex=rex, exc=b[5] - rex)


def newton_krawczyk(F, x, fixed, rad=arb(10) ** -100):
    """F: list of polys in (u, t, S); x: dict var index -> seed float string; fixed: dict var index -> ball. Returns certified balls."""
    vars_ = sorted(x); n = len(vars_)
    J = [[deriv(f, j) for j in vars_] for f in F]
    def full(vals):
        z = [None] * 3
        for k, v in fixed.items(): z[k] = v
        for k, v in zip(vars_, vals): z[k] = v
        return z
    y = [arb(x[k]) for k in vars_]
    for _ in range(40):
        z = full(y); Fy = arb_mat([[ev(f, z)] for f in F]); Jy = arb_mat([[ev(J[i][j], z) for j in range(n)] for i in range(n)])
        d = Jy.mid().inv() * Fy.mid(); y = [arb((y[i] - d[i, 0]).mid()) for i in range(n)]
        if all(abs(d[i, 0].mid()) < arb(10) ** -250 for i in range(n)): break
    X = [arb(v.mid(), rad) for v in y]; z = full(y)
    Fy = arb_mat([[ev(f, z)] for f in F]); Y = arb_mat([[ev(J[i][j], z) for j in range(n)] for i in range(n)]).mid().inv().mid()
    JX = arb_mat([[ev(J[i][j], full(X)) for j in range(n)] for i in range(n)])
    M = arb_mat([[1 if i == j else 0 for j in range(n)] for i in range(n)]) - Y * JX
    K = arb_mat([[y[i]] for i in range(n)]) - Y * Fy + M * arb_mat([[X[i] - y[i]] for i in range(n)])
    ok = all(X[i].contains_interior(K[i, 0]) for i in range(n))
    return ok, full([K[i, 0] for i in range(n)])


def s(z, d=40): return z.str(d, radius=False)


def main():
    PK = load_polys(os.path.join(KDIR, 'data', 'polys-K.json'), 'Q'); PD = load_polys(os.path.join(DDIR, 'data', 'polys-D.json'), 'K')
    c = lambda: 2 * S5() - 4
    # seeds: census logs of the studies (logs/s3_backsolve.log: SURVIVOR lines), u from data/census-*.json records
    B = [  # key, study, polys, seed (u, t, S), v rule, expected failure list (study log, verbatim)
        ('K066866', 'Kulaichev', PK, ('0.668656315401935110672481395168', '0.12600012263503690807', '0.97571625261253856290'), 'u',
         ['b4 < b5', 'b6 < b7', 'w5 > 0', 'w6 > 0', 'apex t4 below its base', 'corner t4 inside the disc', 'corner t6 inside the disc',
          'b5 < 1/2 (centre below the bindu base)']),
        ('D057120', 'DICTO', PD, ('0.571195314832402357654740275346', '0.25507696550874666909', '0.97735522577053243609'), 'c/u',
         ['b5 < 1/2 (centre below the bindu base)']),
        ('D067176', 'DICTO', PD, ('0.671758400623298761936957007201', '0.14750898383271932810', '0.96894915084577402898'), 'c/u',
         ['b4 < b5', 'b6 < b7', 'w5 > 0', 'w6 > 0', 'apex t4 below its base', 'corner t4 inside the disc', 'corner t6 inside the disc',
          'b5 < 1/2 (centre below the bindu base)']),
        ('D088628', 'DICTO', PD, ('0.886279995315526396794499922112', '0.11180484675360204881', '0.94716590963912499512'), 'c/u',
         ['b4 < b5', 'b6 < b7', 'w5 > 0', 'w6 > 0', 'apex t4 below its base', 'corner t4 inside the disc', 'corner t6 inside the disc']),
    ]
    out = {}; good = True
    def record(key, study, u, t, S, v, cert, expect, note):
        nonlocal good
        b, w, a = construct(u, t, S, v); f, und = fails_of(b, w, a); bi = bindu(b, w)
        same = (f == expect) and not und
        good = good and cert and same
        m = {}
        m['b4_minus_b5'] = b[4] - b[5]; m['b6_minus_b7'] = b[6] - b[7]; m['w5'] = w[5]; m['w6'] = w[6]
        m['apex4_minus_b4'] = a[4] - b[4]
        for i in (4, 6): m[f'corner{i}_outside'] = (w[i]**2 + (b[i] - arb(1) / 2)**2).sqrt() - arb(1) / 2
        m['b5_minus_half'] = b[5] - arb(1) / 2; m['incentre_minus_half'] = bi['inc'] - arb(1) / 2
        m['excentre_minus_half'] = bi['exc'] - arb(1) / 2; m['inradius'] = bi['r']; m['exradius'] = bi['rex']
        out[key] = dict(study=study, note=note, u=s(u, 60), v=s(v, 60), t=s(t, 60), S=s(S, 60), krawczyk=cert, fails=f,
                        fails_match_study=same, b={i: s(b[i]) for i in b}, w={i: s(w[i]) for i in w}, apex={i: s(a[i]) for i in a},
                        measures={k: s(x, 12) for k, x in m.items()})
        print(f'{key}: u = {s(u, 20)}  Krawczyk {cert}  fails {f}  match study {same}  undecided {und}')
        print('   ', {k: s(x, 6) for k, x in m.items()})
    for key, study, P, seed, vr, expect in B:
        ok, z = newton_krawczyk([P['G'], P['H1'], P['D']], {0: seed[0], 1: seed[1], 2: seed[2]}, {})
        u, t, S = z; v = u if vr == 'u' else c() / u
        record(key, study, u, t, S, v, ok, expect, 'true solution of G = H1 = D = 0 (box radius 1e-100)')
    # near miss: undistorted Cleo-Antonius, u = 3 - sqrt5 exact, v = 1/phi; G = H1 = 0 (no (d)); seed from census-D.json controls
    u = 3 - S5()
    ok, z = newton_krawczyk([PD['G'], PD['H1']], {1: '0.1907221629', 2: '0.9602057772'}, {0: u})
    record('CA0', 'DICTO', u, z[1], z[2], c() / u, ok, [], 'u = 3 - sqrt5 exact; G = H1 = 0 certified in (t, S); (d) not imposed')
    off = arb(out['CA0']['measures']['incentre_minus_half'])
    good = good and abs(off + arb('0.058132')) < arb('0.000001')
    print('near miss bindu offset agrees with census-D.json (-0.058132):', abs(off + arb('0.058132')) < arb('0.000001'))
    # Rh345 from its stored exact coordinates (50 digits)
    e = json.load(open(os.path.join(HERE, '..', 'data', 'rhombus345-coordinates.json')))['Rh345']
    g = lambda d: {int(k): arb(x['a']) for k, x in d.items()}
    b, w, a = g(e['b']), g(e['w']), g(e['apex']); bi = bindu(b, w); f, und = fails_of(b, w, a)
    good = good and not f and not und
    out['Rh345'] = dict(study='Kulaichev', note='stored exact coordinates (field of degree 20), 50 digits', u='3/4', v='3/4',
                        fails=f, b={i: s(b[i]) for i in b}, w={i: s(w[i]) for i in w}, apex={i: s(a[i]) for i in a},
                        measures={'incentre_minus_half': s(bi['inc'] - arb(1) / 2, 12), 'inradius': s(bi['r'], 12)})
    print('Rh345 fails', f, ' incentre - 1/2 =', s(bi['inc'] - arb(1) / 2, 6))
    json.dump(out, open(os.path.join(HERE, '..', 'data', 'breakers.json'), 'w'), indent=1)
    print('wrote data/breakers.json')
    print('FINAL ok' if good else 'FINAL FAIL')


if __name__ == '__main__':
    main()
