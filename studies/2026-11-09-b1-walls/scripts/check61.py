"""Check the closed forms of #61's Swap defect below 1/4 against every exact hop of the wall walks (walls/w_<s>.txt).
Hops: [λ-(c), -9s/8] key clash; [-9s/8, -(4-s)/24] (only for s > 1/7) δ_tet = -(1-4s)^3/(54s),
δ_oct = (1-4s)^2 (72λ + 8 + 13s)/(108s); [max(-9s/8, -(4-s)/24), -5s/8] δ_oct = (8λ+5s)^3/(64s), δ_tet = -(8λ+5s)^2 (8λ+2-3s)/(64s);
[-5s/8, U(s)] δ = 0 (interior wall at -s/8)."""
import json, glob, sympy as sp
lam = sp.Symbol('lam'); ok = True
for f in sorted(glob.glob('walls/w_*.txt')):
    s = sp.Rational(f[8:-4].replace('o', '/'))
    walls_pred = [-9 * s / 8] + ([-(4 - s) / 24] if s > sp.Rational(1, 7) else []) + [-5 * s / 8, -s / 8, min(sp.Rational(1, 3) + s / 24, 3 * s / 8)]
    F = {'b': (lambda L: (1 - 4 * s) ** 2 * (72 * L + 8 + 13 * s) / (108 * s), lambda L: -(1 - 4 * s) ** 3 / (54 * s)),
         'c': (lambda L: (8 * L + 5 * s) ** 3 / (64 * s), lambda L: -(8 * L + 5 * s) ** 2 * (8 * L + 2 - 3 * s) / (64 * s)),
         'd': (lambda L: 0, lambda L: 0)}
    hops = [json.loads(l) for l in open(f) if l.startswith('{')]
    walls = [sp.Rational(hops[0]['from'])] + [sp.Rational(h['to']) for h in hops]
    res = []
    for h in hops:
        a, b = sp.Rational(h['from']), sp.Rational(h['to'])
        if h['clashes']: res.append(f'[{a},{b}] clash'); continue
        zone = 'b' if b <= -(4 - s) / 24 else 'c' if b <= -5 * s / 8 else 'd'
        good = True
        for role, fn in (('oct', F[zone][0]), ('tetX', F[zone][1]), ('tetY', F[zone][1])):
            for ctx, v in h[role].items():
                good &= sp.simplify(sp.sympify(v, locals={'lam': lam}) - fn(lam)) == 0
        res.append(f'[{a},{b}] {zone}:{"ok" if good else "MISMATCH"}'); ok &= good
    wp = all(w in walls for w in walls_pred) and all(h['clashes'] > 0 for h in hops if sp.Rational(h['to']) <= -9 * s / 8) and not any(h['clashes'] for h in hops if sp.Rational(h['from']) >= -9 * s / 8)
    print(f's = {s}: walls as predicted: {wp}; ' + '  '.join(res)); ok &= wp
print('FINAL ok' if ok else 'FINAL FAIL')
