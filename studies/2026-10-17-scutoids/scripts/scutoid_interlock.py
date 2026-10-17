# DICTO 2026-10-17: "or half a cube and the scutoids overlapping the space", "going into the next boundary on all sides"; diagonal half
# (the hexagon cut). Bundles: two per cube, one at the centroid of each diagonal half ({x+y+z >= 0} and its mirror through the cube centre);
# all bundles in the same orientation (the bundle has inversion symmetry, so the two halves' bundles are the same). Each bundle = core
# truncated icosahedron A + the strict scutoid layer A -> B, and its sweep CONTINUES past B at the same plane speeds until it meets its
# neighbours' sweeps: x belongs to the bundle that reaches it first (arrival time T(x) = max_j (n_j·(x-c) - dA_j) / (dB_j - dA_j)), and
# inside a bundle to the plane that reaches it last (the sweep cell). So the outer pieces cross the half-cube boundary on every side and
# interlock with the neighbours'; no closing layer, no container wall. Not convex in general, so this is a VOXEL prototype: volume by count,
# surface by marching cubes, sphericity ψ = π^(1/3)(6V)^(2/3)/A, calibrated on a cube and a ball at the same resolution. Two ways to cut
# the pieces: the scutoid and its outer growth as separate pieces, or as one piece. -> data/scutoid-interlock.txt (run on dicto-node)
import itertools, sys, json, numpy as np
from scipy import ndimage
from skimage.measure import marching_cubes, mesh_surface_area
phi = (1 + 5 ** .5) / 2
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
ICO = np.array([c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1, s2 * phi])], float)
DOD = np.array([[a, b, c] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1 * phi, s2 / phi])], float)
diag = np.array([abs(abs(v[0]) - abs(v[1])) < 1e-9 and abs(abs(v[1]) - abs(v[2])) < 1e-9 for v in DOD])
N = np.vstack([ICO, DOD[diag], DOD[~diag]]); G = ['P'] * 12 + ['Hd'] * 8 + ['Ho'] * 12
TI = []
for b in ([0, 1, 3 * phi], [1, 2 + phi, 2 * phi], [phi, 2, phi ** 3]):
    for c in cyc(b):
        for s in itertools.product((1, -1), repeat=3): TI.append([c[k] * s[k] for k in range(3)])
TI = np.unique(np.round(TI, 9), axis=0); dA = (TI @ N.T).max(0)
# centroid of the diagonal half cube {x+y+z >= 0} of [-1,1]^3 (sampled), along (1,1,1)
g = np.linspace(-1, 1, 201) + 0.005; X = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = X[(np.abs(X) <= 1).all(1) & (X.sum(1) >= 0)]
U0 = X.mean(0).mean()
def psi_of(mask, h):
    m = np.pad(mask, 2).astype(np.float32); m = ndimage.gaussian_filter(m, 0.6)
    v, f, _, _ = marching_cubes(m, 0.5); return np.pi ** (1 / 3) * (6 * mask.sum() * h ** 3) ** (2 / 3) / (mesh_surface_area(v, f) * h ** 2)
def calib(n):
    a = np.zeros((n, n, n), bool); a[n // 4: 3 * n // 4, n // 4: 3 * n // 4, n // 4: 3 * n // 4] = True
    gg = np.arange(n) - n / 2 + .5; R = np.sqrt(sum(x ** 2 for x in np.meshgrid(gg, gg, gg, indexing='ij'))); return psi_of(a, 1), psi_of(R < n / 4, 1)
def run(gP, gHd, gHo, Lf, n=120):
    dB = np.array([dA[i] * {'P': gP, 'Hd': gHd, 'Ho': gHo}[G[i]] for i in range(32)]); D = dB - dA
    rB = max(dB / np.linalg.norm(N, axis=1))   # B's largest face distance (its rough radius)
    L = Lf * 2 * rB   # cube edge, as a multiple of B's outer diameter
    c0 = np.full(3, U0 * L / 2)
    cs = [np.array(k) * L + s * c0 for k in itertools.product((-1, 0, 1, 2, -2), repeat=3) for s in (1, -1)]
    cs = [c for c in cs if np.linalg.norm(c - c0) < 2.2 * L and np.linalg.norm(c - c0) > 1e-9]
    half = 1.05 * L; gx = np.linspace(-half, half, n); h = gx[1] - gx[0]
    P = np.stack(np.meshgrid(gx, gx, gx, indexing='ij'), -1).reshape(-1, 3) + c0
    Nn = N / 1.0
    tau0 = ((P - c0) @ Nn.T - dA) / D; T0 = tau0.max(1); J = tau0.argmax(1)
    own = np.ones(len(P), bool)
    for c in cs:
        Tc = (((P - c) @ Nn.T - dA) / D).max(1); own &= T0 <= Tc + 1e-12
    shape = (n, n, n)
    lost = int(((T0 <= 1) & ~own).sum())   # scutoid-layer voxels taken by a neighbour (should be 0)
    vol_region = own.sum() * h ** 3; vol_half = L ** 3 / 2
    res = {'core': psi_of((own & (T0 <= 0)).reshape(shape), h)}; per = {}; parts = {}
    for j in range(32):
        lay = (own & (T0 > 0) & (T0 <= 1) & (J == j)).reshape(shape); out = (own & (T0 > 1) & (J == j)).reshape(shape)
        for name, m in (('scutoid ' + G[j], lay), ('outer ' + G[j], out), ('merged ' + G[j], lay | out)):
            if m.sum() < 30: continue
            k = ndimage.label(m)[1]; parts[name] = max(parts.get(name, 0), k)
            per[name] = min(per.get(name, 9), psi_of(m, h))
    sep = min(v for k, v in per.items() if not k.startswith('merged')); mer = min(v for k, v in per.items() if k.startswith('merged'))
    return dict(gP=gP, gHd=gHd, gHo=gHo, Lf=Lf, lost=lost, region_vs_half=vol_region / vol_half, worst_separate=sep, worst_merged=mer,
                per={k: round(v, 3) for k, v in sorted(per.items())}, parts=parts, core_psi=round(res['core'], 3))
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    cube, ball = calib(n); out = ['DICTO · dictospheres.com', 'Interlocking scutoid bundles in diagonal half-cubes: the sweep continues past B until it meets the neighbours (voxel prototype, %d³)' % n,
        f'  calibration at this resolution: cube ψ {cube:.3f} (exact 0.806), ball ψ {ball:.3f} (exact 1)']
    R = []
    for gP, gHd, gHo in ((1.85, 1.95, 2.10), (1.6, 1.7, 1.85), (2.3, 2.46, 2.64), (1.4, 1.45, 1.6)):
        for Lf in (0.9, 1.0, 1.1, 1.25, 1.4):
            try: b = run(gP, gHd, gHo, Lf, n)
            except Exception as e: print('fail', gP, Lf, e, flush=True); continue
            R.append(b); print(json.dumps(b), flush=True)
    ok = [b for b in R if b['lost'] == 0 and abs(b['region_vs_half'] - 1) < 0.03]
    for key in ('worst_separate', 'worst_merged'):
        ok.sort(key=lambda b: -b[key])
        for b in ok[:3]: out.append(f"  best by {key}: {b[key]:.3f} (gP {b['gP']} gHd {b['gHd']} gHo {b['gHo']}, cube edge {b['Lf']}× B's diameter); core ψ {b['core_psi']}; {b['per']}; pieces in >1 part: {[k for k, v in b['parts'].items() if v > 1]}")
    out.append(f'  bundles kept (no scutoid lost, region = half a cube): {len(ok)} of {len(R)}')
    out.append('  for comparison, closed by a rhombic dodecahedron: least ψ 0.578; by a hexagonal prism: 0.586 (exact polyhedra, not voxels)')
    print('\n'.join(out)); open('data/scutoid-interlock.txt', 'w').write('\n'.join(out) + '\n')
