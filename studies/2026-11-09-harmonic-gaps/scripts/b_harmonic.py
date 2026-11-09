# DICTO 2026-11-09 harmonic-gaps study, part B harmonic half. DICTO proposed solving these by 3D waves (harmonics).
# r_G(u): great stellated dodecahedron of CORE (63 cells); r_S(u): the small Sunstar (CORE + 6 Dogstars of the 1/phi^3 lattice).
# Real spherical-harmonic coefficients, l <= 30, of r_G, r_S, their difference Δ = r_G - r_S, and the gap's angular mass
# m(u) = (r_G^3 - r_S^3)/3 (so ∫ m dΩ = gap volume). Checks: solid angle, volumes against the exact values (this also proves both
# solids star-shaped about the centre: a ray leaving and re-entering would make ∫ r^3/3 exceed the volume), convergence between two
# quadratures, and the symmetry of each series (icosahedral / pyritohedral) by rotating sample points.
import os, sys, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from radial import *
from scipy.spatial import ConvexHull
DATA = os.path.join(HERE, '..', 'data'); phi = (1 + 5 ** .5) / 2; s = phi ** -3; fails = []; log = {'mark': 'DICTO harmonic gaps, part B harmonic, 2026-11-09'}
def check(c, m):
    print(('PASS ' if c else 'FAIL ') + m, flush=True); log.setdefault('checks', []).append(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)
J = json.load(open(os.path.join(DATA, 'sunstar-exact.json')))
cells = [np.array(c) for c in J['gsd_cells_float']]; dog = [cells[i] for i in J['dogstar_cells']]
def cell_faces(P):
    h = ConvexHull(P); g = {}
    for simp, eq in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(eq, 9)), set()).update(simp)
    out = []
    for eq, idx in g.items():
        F = P[list(idx)]; c = F.mean(0); n = np.array(eq[:3]); u = F[0] - c; w = np.cross(n, u)
        out.append(F[np.argsort(np.arctan2((F - c) @ w, (F - c) @ u))])
    return out
GSDf = [f for c in cells for f in cell_faces(c)]
E6 = [np.array(v, float) for v in ([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])]
SUNf = cell_faces(cells[0]) + [f for e in E6 for c in dog for f in cell_faces(c * s + 2 * s * e)]
V_exact = {'GSD': 70 - 30 * 5 ** .5, 'Sunstar': -2598 + 1162 * 5 ** .5}
res = {}; series = {}
for name, F, CF in (('GSD', GSDf, [cell_faces(c) for c in cells]), ('Sunstar', SUNf, [cell_faces(cells[0])] + [cell_faces(c * s + 2 * s * e) for e in E6 for c in dog])):
    vis = visible(F); bnd = union_boundary(CF)
    out = []
    for order, ma in ((24, 0.3), (32, 0.22)):
        X, W = quad_points(vis, order, ma); r = np.linalg.norm(X, axis=1)
        a1, P1 = coeffs(X, W, r)
        (a3, P3), om3, vol3, n3 = signed_mass_coeffs(bnd, order=order, maxang=ma)
        out.append((a1, a3, W.sum(), (W * r ** 3).sum() / 3, len(W), om3, vol3))
    (a1, a3, om, vhull, n, om3, vol3), (b1, b3, _, _, _, _, _) = out
    conv = max(max(np.abs(a1[l] - b1[l]).max(), np.abs(a3[l] - b3[l]).max()) for l in range(LMAX + 1))
    series[name] = (a1, a3, vis, bnd)
    res[name] = {'cell_faces': len(F), 'visible_faces': len(vis), 'boundary_faces': len(bnd), 'solid_angle_visible': om, 'solid_angle_signed': om3,
                 'volume_signed_mass': vol3, 'volume_star_hull': vhull, 'volume_exact': V_exact[name], 'conv': conv}
    check(abs(om - 4 * np.pi) < 1e-8 and abs(om3 - 4 * np.pi) < 1e-8 and abs(vol3 - V_exact[name]) < 1e-8 and conv < 1e-8,
          f'{name}: {len(CF)} cells; boundary {len(bnd)} faces; signed solid angle 4π ({om3 - 4 * np.pi:+.1e}); ∫ m dΩ = {vol3:.12f} = exact {V_exact[name]:.12f}; '
          f'coefficients stable to {conv:.1e}')
    print(f'   {name}: volume of its star hull (outer radial function) {vhull:.12f}; excess over the solid {vhull - V_exact[name]:.3e}', flush=True)
check(abs(res['GSD']['volume_star_hull'] - V_exact['GSD']) < 1e-8, 'GSD is star-shaped about its centre (outer radial function encloses exactly its volume)')
excess = res['Sunstar']['volume_star_hull'] - V_exact['Sunstar']; log['sunstar_not_star_shaped_excess'] = excess
check(excess > 1e-3, f'the small Sunstar is NOT star-shaped about its centre: the region under its outer radial function exceeds it by {excess:.6f} '
      f'({excess / V_exact["Sunstar"]:.4f} of its volume): pockets of the gap that no radial function r(u) sees; so the gap is measured by angular mass m(u), not by r_G - r_S')
aG, a3G, visG, bndG = series['GSD']; aS, a3S, visS, bndS = series['Sunstar']
dA = {l: aG[l] - aS[l] for l in range(LMAX + 1)}; mA = {l: a3G[l] - a3S[l] for l in range(LMAX + 1)}
Pw = lambda a: np.array([np.sum(a[l] ** 2) for l in range(LMAX + 1)])
spec = {'r_GSD': Pw(aG), 'r_Sunstar': Pw(aS), 'Delta': Pw(dA), 'm_gap': Pw(mA)}
check(abs(mA[0][0] * np.sqrt(4 * np.pi) - (V_exact['GSD'] - V_exact['Sunstar'])) < 1e-8, f'gap volume from the l = 0 coefficient of m: {mA[0][0] * np.sqrt(4 * np.pi):.12f} (exact 2668 - 1192√5 = {V_exact["GSD"] - V_exact["Sunstar"]:.12f})')
ico_l = [0, 6, 10, 12, 16, 18, 20, 22, 24, 26, 28, 30]
nzG = [l for l in range(LMAX + 1) if spec['r_GSD'][l] > 1e-18]
check(nzG == ico_l, f'r_GSD has only the icosahedral degrees {nzG} (even: the solid is centrally symmetric, so l = 15, 21, 25, 27 of the rotation group do not appear)')
nzS = [l for l in range(LMAX + 1) if spec['r_Sunstar'][l] > 1e-18]
check(2 not in nzS and all(l % 2 == 0 for l in nzS) and 4 in nzS, f'r_Sunstar has the pyritohedral degrees {nzS}: l = 4 (absent from any icosahedral solid) is the cubic signature')
# symmetry by rotating points
def evalser(a, U):
    Y = real_Y(U); return sum(Y[l].T @ a[l] for l in range(LMAX + 1))
rng = np.random.default_rng(3); U = rng.normal(size=(4000, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
def rot(axis, ang):
    k = np.array(axis, float); k /= np.linalg.norm(k); K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
DODf = np.array(list(itertools.product((1, -1), repeat=3)), float)
RIDf = np.array([r for a in (1, -1) for b in (1, -1) for r in ([0, a / phi, b * phi], [a / phi, b * phi, 0], [b * phi, 0, a / phi])], float)
hD = ConvexHull(np.vstack([DODf, RIDf])); c5 = hD.equations[0, :3]                # a face normal of the dodecahedron = a 5-fold axis
ops = {'C3 (1,1,1)': rot([1, 1, 1], 2 * np.pi / 3), 'C2 z': rot([0, 0, 1], np.pi), 'inversion': -np.eye(3), 'C4 z': rot([0, 0, 1], np.pi / 2),
       'C5 face axis': rot(c5, 2 * np.pi / 5), 'mirror x': np.diag([-1., 1, 1])}
sym = {}
for name, a in (('r_GSD', aG), ('r_Sunstar', aS), ('Delta', dA)):
    f0 = evalser(a, U); sym[name] = {o: float(np.abs(evalser(a, U @ R.T) - f0).max()) for o, R in ops.items()}
    print(f'   {name:10s} invariance error under ' + ', '.join(f'{o}: {e:.1e}' for o, e in sym[name].items()), flush=True)
inv = lambda n, o: sym[n][o] < 1e-7
check(all(inv('r_GSD', o) for o in ('C3 (1,1,1)', 'C2 z', 'inversion', 'C5 face axis', 'mirror x')) and not inv('r_GSD', 'C4 z'), 'r_GSD: full icosahedral symmetry I_h (C5 yes, C4 no)')
check(all(inv('Delta', o) for o in ('C3 (1,1,1)', 'C2 z', 'inversion', 'mirror x')) and not inv('Delta', 'C4 z') and not inv('Delta', 'C5 face axis'),
      'Δ = r_GSD - r_Sunstar (outer radial functions): pyritohedral T_h exactly (C3, C2, inversion, mirrors; no C4, no C5): a filler of the gap can have at most T_h, so no icosahedral solid fills it alone')
# how much of the gap is icosahedral and how much cubic: power of the l = 4 and the non-icosahedral part of each degree
# (the I_h-invariant part of degree l is the projection of a_l onto the I_h invariants; computed by averaging over the 120 elements)
def ih_group():
    gens = [ops['C5 face axis'], ops['C3 (1,1,1)'], -np.eye(3)]; G = [np.eye(3)]
    while True:
        new = [g @ h for g in G for h in gens]; added = False
        for M in new:
            if not any(np.abs(M - X).max() < 1e-9 for X in G): G.append(M); added = True
        if not added: break
    return G
G = ih_group(); check(len(G) == 120, f'the icosahedral group I_h generated: {len(G)} elements')
Uq = U[:1500]
def ih_part(a):
    """coefficients of the I_h average of the series (fit by least squares on sample points, per degree)"""
    Y = real_Y(Uq); f = np.mean([sum(real_Y(Uq @ R.T)[l].T @ a[l] for l in range(LMAX + 1)) for R in G], axis=0)
    M = np.hstack([Y[l].T for l in range(LMAX + 1)]); c = np.linalg.lstsq(M, f, rcond=None)[0]; out = {}; i = 0
    for l in range(LMAX + 1): out[l] = c[i:i + 2 * l + 1]; i += 2 * l + 1
    return out
ihm = ih_part(mA); P_ih = Pw(ihm); P_tot = spec['m_gap']
frac_cubic = {l: float(1 - P_ih[l] / P_tot[l]) for l in range(1, LMAX + 1) if P_tot[l] > 1e-18}
tot_nonzero = P_tot[1:].sum(); tot_cubic = (P_tot[1:] - P_ih[1:]).sum()
check(P_ih[4] < 1e-12 * P_tot[4], 'the gap mass has no icosahedral l = 4 part (all of its l = 4 is the Sunstar\'s cube)')
print('   gap angular mass m(u): power by degree (l: total, share that is not icosahedral)')
for l in range(0, 17, 2): print(f'     l = {l:2d}: {P_tot[l]:.6e}   non-icosahedral {frac_cubic.get(l, 0):.4f}', flush=True)
log['gap_mass_anisotropy'] = {'non_icosahedral_share_of_l>0_power': float(tot_cubic / tot_nonzero), 'a00_share': float(P_tot[0] / P_tot.sum())}
print(f'   of the gap mass\'s angular variation (l > 0), {tot_cubic / tot_nonzero:.4f} of the power is pyritohedral, {1 - tot_cubic / tot_nonzero:.4f} icosahedral', flush=True)
log['results'] = res; log['spectra'] = {k: v.tolist() for k, v in spec.items()}; log['symmetry_errors'] = sym; log['m_nonicosahedral_share'] = frac_cubic
np.savez(os.path.join(DATA, 'b_series.npz'), **{f'{k}_{l}': v[l] for k, v in (('aG', aG), ('aS', aS), ('a3G', a3G), ('a3S', a3S)) for l in range(LMAX + 1)})
import pickle; pickle.dump({'visG': visG, 'visS': visS, 'bndG': bndG, 'bndS': bndS}, open(os.path.join(DATA, 'b_visible.pkl'), 'wb'))
json.dump(log, open(os.path.join(DATA, 'b_harmonic.json'), 'w'), indent=1)
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
