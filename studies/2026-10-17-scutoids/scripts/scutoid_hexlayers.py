# DICTO 2026-10-17: "grow some in a circle and then cut them into a hexagon across as many straight edges as you can, and those that get
# damaged you replace with a whole one; should still tile space" — "tile stacked in layers". Within the whole brief (scutoid-bundle-brief):
# bundles (core TI + strict scutoid layer, sweep continuing outward) on a hexagonal-prism lattice: in-layer neighbours across the RD
# directions perpendicular to the diagonal (1,1,1), layers stacked along it. All grow together until they meet (x goes to the bundle that
# reaches it first, inside a bundle to the plane that reaches it last). Every cell of the result is a whole piece of one repeating pattern, so
# it tiles space. A piece cut by a meeting surface (a "damaged" one) is measured on its own AND joined whole with the piece facing it across
# the surface (one whole piece crossing the tile boundary). Voxel prototype on dicto-node; ψ calibrated as in scutoid_interlock.py.
# -> data/scutoid-hexlayers.txt
import sys, json, numpy as np
from scipy import ndimage
exec(open('scripts/scutoid_interlock.py').read().rsplit("\nif __name__", 1)[0])
def run_hex(gP, gHd, gHo, af, cf, n=150):
    dB = np.array([dA[i] * {'P': gP, 'Hd': gHd, 'Ho': gHo}[G[i]] for i in range(32)]); D = dB - dA; rB = max(dB / np.linalg.norm(N, axis=1))
    a, c = af * 2 * rB, cf * 2 * rB
    A1 = a * np.array([1, -1, 0]) / 2 ** .5; A2 = a * np.array([1, 0, -1]) / 2 ** .5; A3 = c * np.ones(3) / 3 ** .5
    half = 1.6 * max(a, c)
    imgs = [i * A1 + j * A2 + k * A3 for i in range(-4, 5) for j in range(-4, 5) for k in range(-4, 5)]
    imgs = np.array([p for p in imgs if np.linalg.norm(p) < half * 1.75 + 2 * rB]); o0 = int(np.argmin(np.linalg.norm(imgs, axis=1)))
    gx = np.linspace(-half, half, n); h = gx[1] - gx[0]
    P = np.stack(np.meshgrid(gx, gx, gx, indexing='ij'), -1).reshape(-1, 3)
    code = np.empty(len(P), np.int32); T0own = np.empty(len(P))
    for s in range(0, len(P), 400000):
        Q = P[s:s + 400000]; best = np.full(len(Q), np.inf); who = np.zeros(len(Q), int); jj = np.zeros(len(Q), int)
        for b, c0 in enumerate(imgs):
            tau = ((Q - c0) @ N.T - dA) / D; T = tau.max(1); m = T < best; best[m] = T[m]; who[m] = b; jj[m] = tau.argmax(1)[m]
        zone = np.where(best <= 0, 0, np.where(best <= 1, 1, 2)); code[s:s + 400000] = who * 128 + zone * 32 + jj; T0own[s:s + 400000] = best
    C = code.reshape(n, n, n); own0 = (C // 128) == o0
    region = own0.sum() * h ** 3; cell = abs(np.dot(A1, np.cross(A2, A3)))
    # scutoid-layer voxels of bundle 0's own layer taken by a neighbour
    tau0 = ((P - imgs[o0]) @ N.T - dA) / D; lost = int(((tau0.max(1) <= 1).reshape(n, n, n) & ~own0).sum())
    border = np.zeros((n, n, n), bool); border[[0, -1], :, :] = border[:, [0, -1], :] = border[:, :, [0, -1]] = True
    per = {}; merged = {}; pairs = {}
    for z in (1, 2):
        for j in range(32):
            m = C == o0 * 128 + z * 32 + j
            if m.sum() < 30: continue
            name = ('scutoid ' if z == 1 else 'outer ') + G[j]; per[name] = min(per.get(name, 9), psi_of(m, h))
            if z == 2:
                # the piece facing it across the meeting surface: the neighbour's outer piece with the largest contact
                cnt = {}
                for ax in range(3):
                    for sh in (1, -1):
                        nb = np.roll(C, sh, axis=ax)[m]; nb = nb[(nb // 128 != o0) & ((nb // 32) % 4 == 2)]
                        for v, k in zip(*np.unique(nb, return_counts=True)): cnt[v] = cnt.get(v, 0) + k
                if not cnt: continue
                v = max(cnt, key=cnt.get); mm = m | (C == v)
                if (mm & border).any(): continue
                merged['joined ' + G[j] + '+' + G[v % 32]] = min(merged.get('joined ' + G[j] + '+' + G[v % 32], 9), psi_of(mm, h))
                pairs[G[j] + str(j)] = (G[v % 32] + str(v % 32))
    sep = min(per.values()) if per else 0
    outer_sep = min([v for k, v in per.items() if k.startswith('outer')] or [9]); joined = min(merged.values()) if merged else None
    return dict(gP=gP, gHd=gHd, gHo=gHo, af=af, cf=cf, lost=lost, region_vs_cell=region / cell, least_layer=min(v for k, v in per.items() if k.startswith('scutoid')),
                least_outer=outer_sep, least_joined=joined, per={k: round(v, 3) for k, v in sorted(per.items())}, joined={k: round(v, 3) for k, v in sorted(merged.items())})
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    cube, ball = calib(n // 2)
    out = ['DICTO · dictospheres.com', f'Hexagonal-prism tiles stacked in layers: bundles grow together until they meet; damaged pieces joined whole across the meeting surface (voxel prototype, {n}³)',
           f'  calibration (at {n // 2}³): cube ψ {cube:.3f} (exact 0.806), ball {ball:.3f}']
    R = []
    for gP, gHd, gHo in ((1.85, 1.95, 2.10), (1.6, 1.7, 1.85)):
        for af in (0.95, 1.1, 1.25, 1.4):
            for cf in (0.85, 1.0, 1.2):
                try: b = run_hex(gP, gHd, gHo, af, cf, n)
                except Exception as e: print('fail', gP, af, cf, repr(e), flush=True); continue
                R.append(b); print(json.dumps(b), flush=True)
    ok = [b for b in R if b['lost'] < 50 and abs(b['region_vs_cell'] - 1) < 0.04]
    out.append(f'  arrangements kept (scutoid layer intact, region = one prism cell): {len(ok)} of {len(R)}')
    for key in ('least_outer', 'least_joined'):
        L = sorted([b for b in ok if b[key] is not None], key=lambda b: -min(b[key], b['least_layer']))
        for b in L[:3]: out.append(f"  best by {key}: {b[key]:.3f}, scutoids {b['least_layer']:.3f} (gP {b['gP']}, in-layer spacing {b['af']}×, layer height {b['cf']}× B's diameter); {b['per']}; joined {b['joined']}")
    out.append('  comparison (exact): rhombic dodecahedron closing 0.578, hexagonal prism closing 0.586; target about cube level (≈0.75-0.85)')
    print('\n'.join(out)); open('data/scutoid-hexlayers.txt', 'w').write('\n'.join(out) + '\n')
