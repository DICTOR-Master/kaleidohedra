# DICTO 2026-10-21 (follow-up to #43): C. the DICTO OTT cycle outward. The golden turned-out step on the DICTO OTT (the rhombic
# triacontahedron cut by its octahedron at all 8 key sites, #37a; exact corners from studies/2026-10-20-ott-rays, cut8-exact.json):
# S_k = phi^k P^k(OTT). The OTT is not icosahedral, so Theorem B does not apply: nesting S_{k-1} inside S_k is checked exactly, and
# t_min(D) (least t with D inside t P(D), nesting-proof study) is computed EXACTLY for every D_k = P^k(OTT) and compared with phi by exact
# sign. The rotation group of the OTT is found exactly (all signed permutation matrices and all 60 icosahedral rotations tested on the
# corner set); towers are grouped by its orbits, and also by the orbits of the full group with the central inversion added.
# Polar (Lemma 3): polar(S_k) = phi^-k T^k(polar OTT); inward nesting and towers (computed in the phi^KMAX frame).
# usage: python3 ott_turned.py <studies/2026-10-19-five-fold-octet> <cut8-exact.json> [KMAX]
import sys, os
FIVE = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); CUT = os.path.abspath(sys.argv[2]); KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 7
exec(open(os.path.join(HERE, 'nc_common.py')).read())
from fractions import Fraction as Fr
q = lambda s: Q5(Fr(s.split('|')[0]), Fr(s.split('|')[1]))
OTT = [tuple(q(x) for x in p) for p in json.load(open(CUT))['V']]
res = {'mark': 'DICTO OTT turned out, golden step, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}, 'tmin': {}, 'shells': [], 'polar': {'solids': {}, 'shells': []}}
t0 = time.time()
# --- the symmetry group, exactly
one, zero = Q5(1), Q5(0)
SP = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        SP.append(tuple(tuple(Q5(sg[i]) if perm[i] == j else zero for j in range(3)) for i in range(3)))
det = lambda M: X.det3v(*M)
cand = SP + X.rotations()
fix = [M for M in cand if symmetric(OTT, [M])]
fix = list({tuple(tuple(repr(x) for x in r) for r in M): M for M in fix}.values())
GR = [M for M in fix if det(M) == one]; GI = fix
ok(True, f'OTT: {len(OTT)} corners. Exact symmetry (tested: 48 signed permutations + 60 icosahedral rotations): {len(GR)} rotations, {len(GI)} symmetries in all (with reflections)')
res['group'] = {'rotations': len(GR), 'all_symmetries': len(GI), 'central_inversion': any(all(M[i][j] == (-one if i == j else zero) for i in range(3) for j in range(3)) for M in GI),
                'rotations_are_signed_permutations': all(M in SP for M in GR)}
print(f"NOTE rotation group order {len(GR)} ({'T, tetrahedral: not O, the RT has no 4-fold axes' if len(GR) == 12 else 'see json'}); central inversion {res['group']['central_inversion']}; full group {len(GI)} elements ({'T_h, pyritohedral' if len(GI) == 24 and res['group']['central_inversion'] else 'see json'})", flush=True)
info, C, F, K = describe(OTT); res['solids']['OTT'] = info
ok(len(C) == len(OTT), f"OTT: {len(C)} corners, {len(F)} faces ({kind_str(K)}), {len(K)} exact face kinds, volume {info['volume']}")
# --- the turned-out family
D = [OTT]
for k in range(1, KMAX + 1):
    t = time.time(); nxt = rev(D[-1]); cc = corners(nxt)
    if len(cc) != len(nxt): print(f'  NOTE: P^{k}(OTT) lists {len(nxt)} foot points, {len(nxt) - len(cc)} of them not corners', flush=True)
    D.append(cc); print(f'built D_{k} = P^{k}(OTT): {len(cc)} corners ({time.time() - t:.0f} s)', flush=True)
    if time.time() - t0 > 900: print(f'NOTE time: stopping the family at k = {k}', flush=True); KMAX = k; break
S = [scale(pw(k), D[k]) for k in range(KMAX + 1)]
for k in range(KMAX + 1):
    info, C, F, K = describe(S[k]); info['symmetric_T'] = symmetric(S[k], GR); info['symmetric_Th'] = symmetric(S[k], GI); res['solids'][f'S{k}'] = info
    ok(info['symmetric_Th'], f"S_{k} = phi^{k} P^{k}(OTT): {len(C)} corners, {len(F)} faces ({kind_str(K)}), {len(K)} exact face kinds, radii {info['corner_radii_float'][0]:.4f}..{info['corner_radii_float'][-1]:.4f}, all {len(GI)} symmetries of T_h")
for k in range(KMAX):
    tm = tmin(D[k], D[k + 1]); le = (tm - PHI).sign() <= 0
    o, nb, w = inside(S[k], S[k + 1])
    Rk = max(dot(v, v).f() for v in D[k]) ** .5; rk = min((d * d / dot(n, n)).f() for n, d in solid(D[k])) ** .5; rk1 = min((d * d / dot(n, n)).f() for n, d in solid(D[k + 1])) ** .5
    res['tmin'][f'D{k}'] = {'t_min': tm.f(), 't_min_exact': repr(tm), 'le_phi_exact': le, 'phi_minus_t_min': PHI.f() - tm.f(), 'R': Rk, 'r': rk, 'r_next': rk1,
                           'upper_R_over_r_next': Rk / rk1, 'upper_R_over_r_sq': (Rk / rk) ** 2, 'S_k_inside_S_k+1': o, 'corners_outside': nb}
    ok(le == o, f"t_min(D_{k}) = {tm!r} = {tm.f():.9f}, phi - t_min = {PHI.f() - tm.f():+.6f} [{'<= phi' if le else '> phi'} exactly]; bounds t_min <= R/r_next {Rk / rk1:.6f} <= (R/r)^2 {(Rk / rk) ** 2:.6f}; "
       f"S_{k} inside S_{k + 1}: {'YES' if o else 'NO'} (corners outside {nb}) -- agrees with t_min")
print(f'solids done ({time.time() - t0:.0f} s)', flush=True)
# DICTO-relevant surprise, checked exactly: after ONE beat the family is icosahedral. P(OTT) drops the 8 foot points of the octahedral
# cuts (strictly inside) and the other 30 are an icosidodecahedron; from there it is the CLEO turned-out family of A, one beat behind.
GI60 = X.rotations()
exec(open('exact_cycle.py').read().split("if __name__ == '__main__':")[1].split("    log = {")[0].replace('\n    ', '\n'))   # ID of radius phi (Cleo Towers)
res['icosahedral_from_beat'] = None
for k in range(KMAX + 1):
    s60 = symmetric(S[k], GI60); res['solids'][f'S{k}']['symmetric_60'] = s60
    if s60 and res['icosahedral_from_beat'] is None: res['icosahedral_from_beat'] = k
ok(res['icosahedral_from_beat'] == 1 and all(res['solids'][f'S{k}']['symmetric_60'] for k in range(1, KMAX + 1)),
   f"S_0 (the OTT) has only T_h; S_1 .. S_{KMAX} are fixed by all 60 icosahedral rotations exactly (icosahedral from beat {res['icosahedral_from_beat']})")
r2 = {dot(v, v) for v in D[1]}; c = None
if len(r2) == 1:
    c2 = next(iter(r2)) / (PHI * PHI); c = next((x for x in [D[1][0][i] / ID[j][i] for j in range(30) for i in range(3) if ID[j][i] != Q5(0)] if x * x == c2 and x.sign() > 0), None)
same1 = c is not None and set(D[1]) == set(scale(c, ID))
ok(same1, f'P(OTT) = c x ID (the CLEO sphere core) exactly, c = {c!r} = {c.f() if c else 0:.6f}; so S_k = phi c x (CLEO turned out S_(k-1)) for every k >= 1')
res['P_OTT_equals_c_ID'] = {'c': repr(c), 'c_float': c.f() if c else None, 'exact': same1}
if same1:
    DC = [ID]
    for _ in range(KMAX - 1): DC.append(rev(DC[-1]))
    ok(all(set(S[k]) == set(scale(PHI * c, scale(pw(k - 1), DC[k - 1]))) for k in range(1, KMAX + 1)), f'S_k = (phi c) x phi^(k-1) P^(k-1)(ID) exactly for k = 1..{KMAX}: the OTT cycle is the CLEO cycle one beat behind')
edges = [e for e in (0, 1, 2, 4, 7) if e <= KMAX]
for a, b in zip(edges, edges[1:]):
    o, nb, _ = inside(S[a], S[b])
    if not o: print(f'NOTE shell S{a} -> S{b}: not nested ({nb} corners outside), not cut'); continue
    t = time.time(); out = shell_orbits(S[a], S[b], GR, f'shell S{a} -> S{b} ({b - a} beat{"s" if b - a > 1 else ""})'); outI = shell_orbits(S[a], S[b], GI, 'with reflections')
    o60 = shell_orbits(S[a], S[b], GI60, 'icosahedral') if a >= 1 else None; out['orbits_I'] = len(o60['orbits']) if o60 else None; out['orbits_Th'] = len(outI['orbits']); out['distinct_shapes_up_to_mirror'] = outI['distinct_volumes']; res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_orbit'] and outI['one_volume_per_orbit'], shell_line(out) + f"; under T_h: {len(outI['orbits'])} orbits" + (f"; under the 60 icosahedral rotations: {len(o60['orbits'])} orbit(s)" if o60 else '') + f" ({time.time() - t:.0f} s)")
# --- polar
Q0 = polar(OTT); TQ = [Q0]
info, C, F, K = describe(Q0); res['polar']['polar OTT'] = info
ok(True, f"polar(OTT): {len(C)} corners, {len(F)} faces ({kind_str(K)})")
for _ in range(KMAX): TQ.append(step(TQ[-1])[0])
Qp = [scale(pw(KMAX), polar(s)) for s in S]
for k in range(KMAX + 1):
    same = set(Qp[k]) == set(scale(pw(KMAX - k), TQ[k]))
    info, C, F, K = describe(Qp[k]); info['symmetric_Th'] = symmetric(Qp[k], GI); res['polar']['solids'][f'polar S{k}'] = info
    ok(same and info['symmetric_Th'], f'polar(S_{k}) = phi^-{k} T^{k}(polar OTT) exactly: {len(C)} corners, {len(F)} faces ({kind_str(K)}), all {len(GI)} symmetries')
    if k: o, nb, _ = inside(Qp[k], Qp[k - 1]); ok(o == res['tmin'][f'D{k - 1}']['S_k_inside_S_k+1'], f"polar(S_{k}) inside polar(S_{k - 1}): {'YES' if o else 'NO'} (corners outside {nb}) -- polarity agrees")
for a, b in zip(edges, edges[1:]):
    o, nb, _ = inside(Qp[b], Qp[a])
    if not o: print(f'NOTE polar shell: polar S{b} not inside polar S{a}, not cut'); continue
    t = time.time(); out = shell_orbits(Qp[b], Qp[a], GR, f'polar shell polar S{b} -> polar S{a} (inward)'); res['polar']['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_orbit'], shell_line(out) + f' ({time.time() - t:.0f} s)')
res['kmax'] = KMAX; res['polar']['frame'] = f'phi^{KMAX} x polar (unit sphere)'
res['boundaries_float'] = {f'S{k}': fl(S[k]) for k in range(KMAX + 1)}
res['polar']['boundaries_float'] = {f'polar S{k}': fl(Qp[k]) for k in range(KMAX + 1)}
json.dump(res, open(os.path.join(HERE, 'ott-turned.json'), 'w'), indent=1)
print(f'done ({time.time() - t0:.0f} s)')
