# DICTO 2026-10-21 (follow-up to #43): A. CLEO turned out. Start from the CLEO sphere core (the icosidodecahedron ID of Cleo Towers,
# radius phi, standard frame of exact_cycle.py) and take the golden turned-out step: S_k = phi^k P^k(ID) (tips = phi x the foot points).
# EXACT in Q(sqrt5): beats 0..7 (corners, faces, exact face kinds, symmetry under all 60 rotations, nesting S_{k-1} inside S_k --
# Theorem B guarantees it, checked anyway); the 4-beat return P^4(ID) = (phi^4/10) ID; shells in Fibonacci beats 1, 1, 2, 3
# (boundaries 0, 1, 2, 4, 7) cut into towers (one volume per orbit, sum = shell exactly). Polar (Lemma 3): polar(S_k) =
# phi^-k T^k(polar ID), polar ID = T(ID)/phi^2 (a rhombic triacontahedron): the UP family of the RT shrinking by phi^-k; inward nesting
# and inward towers as in polar_turned.py (computed in the phi^7 frame).   usage: python3 cleo_turned.py <studies/2026-10-19-five-fold-octet>
import sys, os
FIVE = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'nc_common.py')).read())
exec(open('exact_cycle.py').read().split("if __name__ == '__main__':")[1].split("    log = {")[0].replace('\n    ', '\n'))   # ID of radius phi
GA = X.rotations(); KMAX = 7
res = {'mark': 'DICTO CLEO turned out, golden step, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}, 'shells': [], 'polar': {'solids': {}, 'shells': []}}
ok(len(ID) == 30 and symmetric(ID, GA), 'the CLEO sphere core: ID, 30 corners on radius phi, fixed by all 60 rotations')
D = [ID]; t0 = time.time()
for k in range(1, KMAX + 1): D.append(rev(D[-1]))
S = [scale(pw(k), D[k]) for k in range(KMAX + 1)]
lam = pw(4) / 10
ok(set(D[4]) == set(scale(lam, ID)), 'P^4(ID) = (phi^4/10) ID exactly: the downward family returns to the ID after 4 beats')
ok(all(set(S[k + 4]) == set(scale(pw(8) / 10, S[k])) for k in range(KMAX - 3)), f'S_(k+4) = (phi^8/10) S_k exactly (phi^8/10 = {(pw(8) / 10)!r} = {(pw(8) / 10).f():.6f}; per beat {(pw(8) / 10).f() ** .25:.6f} < phi)')
for k in range(KMAX + 1):
    info, C, F, K = describe(S[k]); info['symmetric_60'] = symmetric(S[k], GA); info['listed_points'] = len(S[k]); res['solids'][f'S{k}'] = info
    ok(info['symmetric_60'] and len(C) == len(S[k]), f"S_{k}: {len(C)} corners, {len(F)} faces ({kind_str(K)}), {len(K)} exact face kinds, radii {info['corner_radii_float']}, all 60 rotations")
    if k:
        o, nb, _ = inside(S[k - 1], S[k]); res['solids'][f'S{k}']['holds_previous'] = o
        ok(o, f'S_{k - 1} lies inside S_{k} exactly (corners outside {nb})')
        ok(set(S[k]) == {tuple(PHI * x for x in v) for v in rev(S[k - 1])}, f'S_{k} corners = phi x the foot points of S_{k - 1} exactly')
# which solids: compare each S_k with the four solids of the UP cycle of Cleo Towers (ID, RT, GTI, FPD = T^j ID), exactly
U = [ID]
for _ in range(3): U.append(step(U[-1])[0])
UN = ['ID', 'RT', 'GTI (golden truncated icosahedron)', 'FPD (pentakis type)']
def similar(A, B):
    for u in B:
        for s in A:
            if all(x == Q5(0) for x in cross(s, u)) and dot(s, s) * dot(u, u) == dot(s, u) * dot(s, u) and dot(s, u).sign() > 0:
                i = next(i for i in range(3) if u[i] != Q5(0)); c = s[i] / u[i]
                if set(scale(c, B)) == set(A): return c
    return None
res['same_as_up_cycle'] = {}
for k in range(4):
    hit = [(j, similar(S[k], U[j])) for j in range(4)]; hit = [(j, c) for j, c in hit if c is not None]
    res['same_as_up_cycle'][f'S{k}'] = [(UN[j], repr(c)) for j, c in hit]
    ok(len(hit) == 1, f'S_{k} = ' + ' / '.join(f'{c!r} x {UN[j]} of the UP cycle' for j, c in hit) + ' exactly' if hit else f'S_{k}: not similar to any UP-cycle solid')
print(f'solids done ({time.time() - t0:.0f} s)', flush=True)
for a, b in [(0, 1), (1, 2), (2, 4), (4, 7)]:
    t = time.time(); out = shell_orbits(S[a], S[b], GA, f'shell S{a} -> S{b} ({b - a} beat{"s" if b - a > 1 else ""})'); res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_orbit'], shell_line(out) + f' ({time.time() - t:.0f} s)')
# polar
Q0 = polar(ID); RTp = step(ID)[0]
ok(set(Q0) == set(scale(Q5(1) / (PHI * PHI), RTp)), 'polar(ID) = T(ID)/phi^2 exactly: the rhombic triacontahedron (32 corners)')
TQ = [Q0]
for _ in range(KMAX): TQ.append(step(TQ[-1])[0])
Q = [scale(pw(KMAX), polar(s)) for s in S]          # phi^7 frame: the small polar solids trip the float guessing otherwise (as polar_turned.py)
for k in range(KMAX + 1):
    same = set(Q[k]) == set(scale(pw(KMAX - k), TQ[k]))
    info, C, F, K = describe(Q[k]); info['symmetric_60'] = symmetric(Q[k], GA); res['polar']['solids'][f'polar S{k}'] = info
    ok(same and info['symmetric_60'], f'polar(S_{k}) = phi^-{k} T^{k}(RT) exactly: {len(C)} corners, {len(F)} faces ({kind_str(K)}), all 60 rotations')
    if k: o, nb, _ = inside(Q[k], Q[k - 1]); ok(o, f'polar(S_{k}) lies inside polar(S_{k - 1}) exactly (corners outside {nb})')
for a, b in [(1, 0), (2, 1), (4, 2), (7, 4)]:
    t = time.time(); out = shell_orbits(Q[a], Q[b], GA, f'polar shell polar S{a} -> polar S{b} (inward, {a - b} beat{"s" if a - b > 1 else ""})'); res['polar']['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_orbit'], shell_line(out) + f' ({time.time() - t:.0f} s)')
res['boundaries_float'] = {f'S{k}': fl(S[k]) for k in range(KMAX + 1)}
res['polar']['boundaries_float'] = {f'polar S{k}': fl(Q[k]) for k in range(KMAX + 1)}; res['polar']['frame'] = 'phi^7 x polar (unit sphere); volumes in that frame'
json.dump(res, open(os.path.join(HERE, 'cleo-turned.json'), 'w'), indent=1)
print(f'done ({time.time() - t0:.0f} s)')
