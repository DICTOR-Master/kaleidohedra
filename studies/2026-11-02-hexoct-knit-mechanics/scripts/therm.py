# Comfort proxies for the Knitted HexOct (DICTO proposed), on the same voxel model as flow.py (members as capsules of
# radius r, periodic 1 x sqrt(3) a cell, sheets 0..11):
#  (1) vapour diffusion through the air: Laplace solve in the fluid voxels (6-neighbour finite volume, periodic in x and y,
#      c = 1 on the bottom plane, c = 0 on the top), D_eff/D_air = flux * H / (cell area); tortuosity factor = porosity / that;
#  (2) conduction along the yarn: the same solve in the solid voxels (yarn conductivity 1, air 0), k_solid_eff/k_yarn;
#  (3) direct radiation: share of rays from the bottom plane (cosine-weighted directions, black members) that reach the
#      top plane without touching a member; ray marching in the voxel grid at h/2 steps, periodic in x and y.
# Usage: therm.py <seq> <h> <r> <out.json> [nrays]
import sys, json, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spl
from flow import segments, voxels, CX, CY
from lattice import SEQ_LABELS, word_from_labels

def laplace_flux(mask, hs):
    nx, ny, nz = mask.shape; idx = -np.ones(mask.shape, np.int64); idx[mask] = np.arange(mask.sum()); n = int(mask.sum())
    rows, cols, vals = [], [], []; diag = np.zeros(n); rhs = np.zeros(n)
    for ax, (d, other) in enumerate(((hs[0], hs[1] * hs[2]), (hs[1], hs[0] * hs[2]))):  # periodic x, y
        g = other / d; nb = np.roll(idx, -1, ax); m = (idx >= 0) & (nb >= 0)
        a, b = idx[m], nb[m]; rows += [a, b]; cols += [b, a]; vals += [np.full(len(a), -g)] * 2
        np.add.at(diag, a, g); np.add.at(diag, b, g)
    g = hs[0] * hs[1] / hs[2]; a, b = idx[:, :, :-1], idx[:, :, 1:]; m = (a >= 0) & (b >= 0)
    rows += [a[m], b[m]]; cols += [b[m], a[m]]; vals += [np.full(m.sum(), -g)] * 2
    np.add.at(diag, a[m], g); np.add.at(diag, b[m], g)
    # Dirichlet planes half a voxel outside: bottom c = 1, top c = 0 (conductance 2g)
    bot = idx[:, :, 0][idx[:, :, 0] >= 0]; top = idx[:, :, -1][idx[:, :, -1] >= 0]
    np.add.at(diag, bot, 2 * g); rhs[bot] += 2 * g; np.add.at(diag, top, 2 * g)
    A = sps.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsr() + sps.diags(diag)
    # unconnected pockets make A singular only if isolated from both planes; regularise them away by a tiny leak
    A = A + sps.identity(n) * 1e-12
    c, info = spl.cg(A, rhs, rtol=1e-10, maxiter=20000, M=sps.diags(1 / A.diagonal()))
    flux = float(np.sum(2 * g * (1 - c[bot])))
    H = nz * hs[2]
    return flux * H / (CX * CY), int(info)

def radiation(solid, hs, nrays, rng):
    nx, ny, nz = solid.shape; H = nz * hs[2]
    u = rng.random(nrays); phi = 2 * np.pi * rng.random(nrays); st = np.sqrt(u); ct = np.sqrt(1 - u)  # cosine-weighted
    d = np.stack([st * np.cos(phi), st * np.sin(phi), ct], 1)
    p = np.stack([rng.random(nrays) * CX, rng.random(nrays) * CY, np.zeros(nrays)], 1)
    alive = np.ones(nrays, bool); step = 0.5 * min(hs); L = H / ct
    for k in range(int(np.ceil(L.max() / step)) + 1):
        s = np.minimum(k * step, L); q = p + d * s[:, None]
        i = np.floor((q[:, 0] % CX) / hs[0]).astype(int) % nx; j = np.floor((q[:, 1] % CY) / hs[1]).astype(int) % ny
        kz = np.clip(np.floor(q[:, 2] / hs[2]).astype(int), 0, nz - 1)
        alive &= ~solid[i, j, kz]
        if (k * step > L).all(): break
    return float(alive.mean())

if __name__ == '__main__':
    seq, h, r, outp = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    nrays = int(sys.argv[5]) if len(sys.argv) > 5 else 200000
    labels = seq[2:] if seq.startswith('L:') else SEQ_LABELS[seq]
    seg, N = segments(labels); solid, hs, H = voxels(seg, N, r, h)
    res = dict(seq=seq, labels=labels, word=word_from_labels(labels), h=h, r=r, voxels=list(solid.shape), H=H,
               porosity=float((~solid).mean()))
    res['D_eff_air'], res['cg_info_air'] = laplace_flux(~solid, hs)
    res['tortuosity_factor'] = res['porosity'] / res['D_eff_air']
    res['k_eff_yarn'], res['cg_info_yarn'] = laplace_flux(solid, hs)
    res['radiation_direct'] = radiation(solid, hs, nrays, np.random.default_rng(1))
    json.dump(res, open(outp, 'w'), indent=1)
    print(seq, h, r, 'D_eff/D_air %.4f  k_yarn %.5f  rad %.4f' % (res['D_eff_air'], res['k_eff_yarn'], res['radiation_direct']))
