# DICTO 2026-10-21 (follow-up to #43): B. the polar of the OG upward family (#39). Upward family U_k = T^k(OG): OG, KRE, PHE, TPP,
# DPHP. By Lemma 3 (polar(P X) = T(polar X), so P(polar X) = polar(T X)) its polar is the downward foot-point family of the DICTO
# Hecatodihedron H = polar(OG): polar(U_k) = P^k(H). EXACT in Q(sqrt5), frame of #39, unit sphere, k <= 4: corners, faces, exact face
# kinds, all 60 rotations; nesting of every pair (polarity reverses inclusion: P^k H inside P^j H <=> U_j inside U_k), checked on both
# sides; the nested shells cut into towers on the faces of the inner solid (one volume per orbit, sum = shell exactly).
# Computed in the phi^4 frame (the small inner solids trip the float guessing otherwise, as in polar_turned.py).
# usage: python3 og_up_polar.py <studies/2026-10-19-five-fold-octet>
import sys, os
FIVE = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'nc_common.py')).read())
NM = ['OG', 'KRE', 'PHE', 'TPP', 'DPHP']; PN = ['H (Hecatodihedron)', 'P H', 'P^2 H', 'P^3 H', 'P^4 H']
res = {'mark': 'DICTO polar of the OG upward family, exact, 2026-10-21 · DICTO · dictospheres.com', 'frame': 'phi^4 x polar (unit sphere)', 'solids': {}, 'nesting': {}, 'upward_nesting': {}, 'shells': []}
t0 = time.time(); U = [OG]
for _ in range(4): U.append(step(U[-1])[0])
H = polar(OG); C, F, K = kinds(H)
ok(len(C) == 80 and len(F) == 102, f'polar(OG) = the DICTO Hecatodihedron: {len(C)} corners, {len(F)} faces ({kind_str(K)})')
P = [H]
for _ in range(4): P.append(rev(P[-1]))
for k in range(5):
    ok(set(corners(P[k])) == set(polar(U[k])), f'P^{k}(H) = polar({NM[k]}) exactly (Lemma 3), {len(P[k])} listed foot points, {len(set(corners(P[k])))} corners')
Q = [scale(pw(4), corners(p)) for p in P]
for k in range(5):
    info, C, F, K = describe(Q[k]); info['symmetric_60'] = symmetric(Q[k], G); info['polar_of'] = NM[k]; res['solids'][PN[k]] = info
    ok(info['symmetric_60'], f"{PN[k]} = polar({NM[k]}): {len(C)} corners, {len(F)} faces ({kind_str(K)}), {len(K)} exact face kinds, all 60 rotations")
print(f'solids done ({time.time() - t0:.0f} s)', flush=True)
for j in range(5):
    for k in range(j + 1, 5):
        o, nb, w = inside(Q[k], Q[j]); ou, nbu, wu = inside(U[j], U[k])
        res['nesting'][f'{PN[k]} inside {PN[j]}'] = {'nested': o, 'corners_outside': nb, 'largest_excess_float': w}
        res['upward_nesting'][f'{NM[j]} inside {NM[k]}'] = {'nested': ou, 'corners_outside': nbu}
        ok(o == ou, f"{PN[k]} inside {PN[j]}: {'YES' if o else 'NO'} (corners outside {nb}{'' if o else f', largest excess {w:.3g}'});  {NM[j]} inside {NM[k]}: {'YES' if ou else 'NO'} (corners outside {nbu}) -- polarity agrees")
for k in range(1, 5):
    j = max((j for j in range(k) if res['nesting'][f'{PN[k]} inside {PN[j]}']['nested']), default=None)
    if j is None: print(f'NOTE {PN[k]} lies inside none of the solids before it: no shell'); continue
    t = time.time(); out = shell_orbits(Q[k], Q[j], G, f'shell {PN[k]} -> {PN[j]} (inward)'); out['outer'] = PN[j]; out['inner'] = PN[k]; res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_orbit'], shell_line(out) + f' ({time.time() - t:.0f} s)')
res['boundaries_float'] = {PN[k]: fl(Q[k]) for k in range(5)}
json.dump(res, open(os.path.join(HERE, 'og-up-polar.json'), 'w'), indent=1)
print(f'done ({time.time() - t0:.0f} s)')
