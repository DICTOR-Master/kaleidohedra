#!/usr/bin/env python3
"""Resample the 600 nm volume of butterfly eye gw05 (Paukner et al. 2024, BossDB paukner2024) onto concentric shells about
the fitted cornea sphere. Chart: azimuthal-equidistant angles (a, b) about a patch axis, step DA rad, so a column that runs
towards the sphere centre keeps its chart position at every depth. Output: stack (depth, a, b) kept on the compute machine
(derived from unlicensed data, never put in git).
Patch axes are given as (A, B) angles in the coarse frame (u0, e1, e2) found on the 2.4 um volume (sphere_iso.npy, frame_iso.npy).
Usage: eyeshells.py OUT.npy A B [DEPTH_STEP_UM N D0_UM D1_UM]"""
import sys, numpy as np, time
from scipy import ndimage as ndi
E = '/home/dicto/eye-data/'
DA = 0.001


def frame():
    s = np.load(E + 'sphere_iso.npy'); c = s[:3] * 4 + 1.5; R = s[3] * 4                # 600-voxel units, full volume (z, y, x)
    f = np.load(E + 'frame_iso.npy'); return c, R, f[:3], f[3:6], f[6:]


def patch_axes(A0, B0):
    c, R, u0, e1, e2 = frame()
    t = np.hypot(A0, B0)
    uc = u0 if t == 0 else np.cos(t) * u0 + np.sin(t) * (A0 * e1 + B0 * e2) / t
    uc /= np.linalg.norm(uc); f1 = np.cross(uc, e2); f1 /= np.linalg.norm(f1); f2 = np.cross(uc, f1)
    return c, R, uc, f1, f2


def chart_dirs(uc, f1, f2, N):
    a = (np.arange(N) - (N - 1) / 2) * DA
    Aa, Bb = np.meshgrid(a, a, indexing='ij'); th = np.hypot(Aa, Bb) + 1e-15
    return np.cos(th)[..., None] * uc + np.sin(th)[..., None] * (Aa[..., None] * f1 + Bb[..., None] * f2) / th[..., None]


def make_stack(V, A0, B0, depths, N=400, log=None):
    c, R, uc, f1, f2 = patch_axes(A0, B0); D = chart_dirs(uc, f1, f2, N)
    S = np.zeros((len(depths), N, N), np.float32); t0 = time.time()
    for k, d in enumerate(depths):
        S[k] = ndi.map_coordinates(V, (c + (R - d / 0.6) * D).reshape(-1, 3).T, order=1, cval=-1, output=np.float32).reshape(N, N)
        if log and k % max(1, len(depths) // 10) == 0: log(f'shell {k}/{len(depths)} depth {d:.0f} um {time.time() - t0:.0f} s')
    meta = np.r_[depths[0], depths[1] - depths[0], DA, R * 0.6, uc, f1, f2, c]
    return S, meta


def fibre_dir(V, p, h=50, ref=None):
    """Mean fibre direction in a cube of half-size h voxels at p: eigenvector of the smallest eigenvalue of the
    gradient structure tensor (intensity varies least along the columns). Returns (direction, eigenvalue ratios)."""
    p = np.round(p).astype(int)
    B = np.asarray(V[p[0] - h:p[0] + h, p[1] - h:p[1] + h, p[2] - h:p[2] + h], np.float32)
    g = np.gradient(ndi.gaussian_filter(B, 1.5))
    T = np.array([[np.mean(g[i] * g[j]) for j in range(3)] for i in range(3)])
    w, v = np.linalg.eigh(T); d = v[:, 0]
    if ref is not None and d @ ref < 0: d = -d
    return d, (w[0] / w[2], w[1] / w[2])


def make_fibre_stack(V, p0, inward, length_um, N=500, px_um=0.3, step_um=1.0, every_um=10.0, log=None):
    """Planes perpendicular to the measured local column direction, stepped along it (a straightened frame that follows
    bending columns). The direction is re-measured every every_um and interpolated; in-plane axes are parallel-transported."""
    nsteps = int(round(length_um / step_um)) + 1
    p = np.array(p0, float); n, rat = fibre_dir(V, p, ref=inward); e1 = np.cross(n, [1.0, 0, 0]); e1 /= np.linalg.norm(e1)
    g = (np.arange(N) - (N - 1) / 2) * px_um / 0.6                                  # voxels
    G1, G2 = np.meshgrid(g, g, indexing='ij')
    S = np.zeros((nsteps, N, N), np.float32); path = []; dirs = []; ratios = [rat]; e1s = []
    n_next, last = n, 0.0
    for k in range(nsteps):
        t = k * step_um
        if t - last >= every_um - 1e-9:
            n_new, rat = fibre_dir(V, p, ref=n); ratios.append(rat); n_next = n_new; last = t
        n = n + (n_next - n) * min(1.0, step_um / every_um); n /= np.linalg.norm(n)   # smooth turn towards the new direction
        e1 = e1 - (e1 @ n) * n; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        P = p[None, None] + G1[..., None] * e1 + G2[..., None] * e2
        S[k] = ndi.map_coordinates(V, P.reshape(-1, 3).T, order=1, cval=-1, output=np.float32).reshape(N, N)
        path.append(p.copy()); dirs.append(n.copy()); e1s.append(e1.copy())
        p = p + n * step_um / 0.6
        if log and k % max(1, nsteps // 10) == 0: log(f'plane {k}/{nsteps}')
    return S, np.array(path), np.array(dirs), np.array(ratios), np.array(e1s)


if __name__ == '__main__':
    out, A0, B0 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    dstep = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0; N = int(sys.argv[5]) if len(sys.argv) > 5 else 400
    d0, d1 = (float(sys.argv[6]), float(sys.argv[7])) if len(sys.argv) > 7 else (-10.0, 560.0)
    V = np.load(E + 'gw05-s600.npy', mmap_mode='r')
    S, meta = make_stack(V, A0, B0, np.arange(d0, d1 + 1e-9, dstep), N, log=lambda m: print('PROGRESS', m, flush=True))
    np.save(out, S); np.save(out.replace('.npy', '_meta.npy'), meta)
    print('outside-volume share', float((S < 0).mean()), 'shape', S.shape); print('SHELLS ok')
