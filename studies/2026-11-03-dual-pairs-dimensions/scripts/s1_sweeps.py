"""Step 1: the 6D sweeps S(mu) = P cap mu P* (sections of P x P* by the flats y = x/mu) and their polars, the hulls
H(mu) = conv(P cup mu P*), for the three dual pairs, exact.
  co: cube x octahedron (SANITY: must reproduce studies/2026-11-03-6d-golden-cubes s3 part C: octahedron 1, Unborn Axes 3 - phi,
      truncated octahedron 3/2, Icosaxes phi, cuboctahedron 2, Greater GCC, truncated cube 1 + sqrt2, Lesser GCC, cube 3)
  di: dodecahedron x icosahedron;  tt: tetrahedron x (-tetrahedron).
For each pair: r^2, rho^2, R^2; every named stage (the two ends, the Archimedean truncations, the rectified stage, the #88 golden
cuts on both sides) located at its exact mu (Lemma: a corner cut at edge fraction x is S(mu) with mu = R^2 - x e^2/2, on the dual
side 1/mu = R*^2 - x e*^2/2); each section built exactly and matched corner to corner (similar()) with the cut solid; the hull at
the same mu checked to be mu times the polar of the section (exact). Numbers reported: mu, nu = mu/r^2, kappa = mu/rho^2,
layer height h = 1 - 2x, ratio (corner side / remaining side), phi-power test and field norm.
usage (dicto-big-brother): ~/geom/bin/python s1_sweeps.py co|di|tt  -> ../data/s1-sweep-<pair>.json
"""
from dp_lib import *          # noqa
import sys
which = sys.argv[1]
pl = platonic()
C_N = {3: ONE, 4: S2, 5: PHI}
if which == 'co':   P, nP, nS, names = Pair('cube', pl['cube'][0]), 4, 3, ('cube', 'octahedron')
elif which == 'di': P, nP, nS, names = Pair('dodecahedron', pl['dodecahedron'][0]), 5, 3, ('dodecahedron', 'icosahedron')
else:               P, nP, nS, names = Pair('tetrahedron', pl['tetrahedron'][0]), 3, 3, ('tetrahedron', 'tetrahedron (polar)')
out = {'pair': names, 'r2': kdesc(P.r2), 'rho2': kdesc(P.rho2), 'R2': kdesc(P.R2),
       'nu_rect': kdesc(P.rho2 / P.r2), 'nu_P_end': kdesc(P.R2 / P.r2)}
print(names, 'r2', kstr(P.r2), 'rho2', kstr(P.rho2), 'R2', kstr(P.R2), flush=True)
check(f'{which}: polar P* = conv(N) has {len(P.N)} corners, midradii multiply to 1 (rho^2 rho*^2 = 1)',
      (P.Rs2 - P.es2 / 4) * P.rho2 == ONE)
stages = []
def stage(label, side, x):
    if side == 'P':
        mu = P.mu_P(x); target = cut_solid(P.V, x) if x != ZERO else P.V; c = C_N[nP]
    else:
        mu = P.mu_Ps(x); target = cut_solid(P.N, x) if x != ZERO else P.N; c = C_N[nS]
    stages.append((label, side, x, mu, target, c))
xg, xl = x_golden(nP); xgs, xls = x_golden(nS)
stage(names[1] + ' (dual end)', 'S', ZERO)
stage('Lesser Golden Cut ' + ('Octahedron = Unborn Axes' if which == 'co' else names[1].split(' ')[0].capitalize() + ' (dual side)'), 'S', xls)
stage('truncated ' + names[1].split(' ')[0] + ' (Archimedean, dual side)', 'S', ONE / (C_N[nS] + 2))
stage('Greater Golden Cut ' + ('Octahedron = Icosaxes' if which == 'co' else names[1].split(' ')[0].capitalize() + ' (dual side)'), 'S', xgs)
stage('rectified (' + {'co': 'cuboctahedron', 'di': 'icosidodecahedron', 'tt': 'octahedron'}[which] + ')', 'P', K(Fr(1, 2)))
stage('Greater Golden Cut ' + names[0].capitalize(), 'P', xg)
stage('truncated ' + names[0] + ' (Archimedean)', 'P', ONE / (C_N[nP] + 2))
stage('Lesser Golden Cut ' + names[0].capitalize(), 'P', xl)
stage(names[0] + ' (P end)', 'P', ZERO)
rows = []
for label, side, x, mu, target, c in stages:
    Sx = P.S(mu)
    ok, lam = similar(Sx, target)
    check(f'{which}: S(mu) at mu = {kstr(mu)} (~{float(mu):.6f}) is the {label} ({len(Sx)} corners)', ok)
    Hm = P.Hull(mu); pol = [vscale(mu, p) for p in polar_pts(Sx)]
    ok2 = {key(p) for p in Hm} == {key(p) for p in pol}
    check(f'{which}:   H(mu) = conv(P cup mu P*) = mu * polar(S(mu)) ({len(Hm)} corners)', ok2)
    ratio = (x * c / (1 - 2 * x)) if x != ZERO and x != K(Fr(1, 2)) else None
    rows.append({'stage': label, 'side': side, 'x': kstr(x), 'mu': kdesc(mu), 'nu': kdesc(P.nu(mu)), 'kappa': kdesc(mu / P.rho2),
                 'h_layer': kstr(1 - 2 * x), 'ratio_corner_over_remaining': kstr(ratio) if ratio is not None else None,
                 'corners': len(Sx), 'hull_corners': len(Hm)})
    print('   ', label, '| mu', kstr(mu), f'~{float(mu):.6f}', '| nu', kstr(P.nu(mu)), f'~{float(P.nu(mu)):.6f}', flush=True)
out['stages'] = rows
mus = [s[3] for s in stages]
check(f'{which}: the stages are in increasing mu order (dual end -> P end), sweep monotone', all(a < b for a, b in zip(mus, mus[1:])))
if which == 'co':
    exp = {'Unborn': 3 - PHI, 'Icosaxes': PHI, 'tO': K(Fr(3, 2)), 'tC': 1 + S2}
    check('SANITY (6D study): Unborn Axes at 3 - phi, truncated octahedron 3/2, Icosaxes phi, truncated cube 1 + sqrt2, ends 1 and 3',
          mus[1] == exp['Unborn'] and mus[2] == exp['tO'] and mus[3] == exp['Icosaxes'] and mus[6] == exp['tC']
          and mus[0] == ONE and mus[-1] == K(3) and mus[4] == K(2))
    s3 = json.load(open(os.path.join(HERE, '..', '..', '2026-11-03-6d-golden-cubes', 'data', 's3-six-d.json')))
    old = {d['name']: d['mu'] for d in s3['sections']}
    check('SANITY: Greater/Lesser GCC mu identical to the 6D study (exact strings)',
          old['Greater Golden Cut Cube'] == kstr(mus[5]) and old['Lesser Golden Cut Cube'] == kstr(mus[7]))
# golden mu: in which field, phi powers?
gold = [r for r in rows if 'Golden' in r['stage']]
out['golden_mu_fields'] = {r['stage']: ('Q(sqrt5)' if 'norm' in r['mu'] else 'Q(sqrt2, sqrt5)') for r in gold}
out['golden_mu_phi_powers'] = {r['stage']: r['mu'].get('phi_power') for r in gold}
# layer formula: ratio as a function of mu (Mobius) -- record
save(f's1-sweep-{which}.json', out)
