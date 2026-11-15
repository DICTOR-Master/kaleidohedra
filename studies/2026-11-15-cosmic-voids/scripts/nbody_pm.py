"""Small particle-mesh N-body run with the public code pmwd (Li, Lanusse, Modi et al. 2022, arXiv:2211.09958; BSD-3-Clause).
We call pmwd's functions (2LPT initial conditions, leapfrog PM steps, cloud-in-cell scatter) and copy none of its code.
Planck 2018 cosmology as packaged in pmwd (arXiv:1807.06209, Table 2 last column).
Saves the cloud-in-cell density contrast on a G^3 grid at every PM step with a >= a_save (float32 .npy) plus meta.json.
Usage: nbody_pm.py OUT N L G a_save da seed"""
import sys, os, json, time
import numpy as np
import jax, jax.numpy as jnp
jax.config.update('jax_enable_x64', False)
from pmwd import linear_power, Configuration, Planck18, boltzmann, white_noise, linear_modes, lpt, scatter
from pmwd.nbody import nbody_init, nbody_step
out, N, L, G, a_save, da, seed = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
os.makedirs(out, exist_ok=True)
t0 = time.time()
conf = Configuration(L / N, (N,) * 3, mesh_shape=2, a_start=1/32, a_stop=1.0, a_nbody_maxstep=da)
cosmo = boltzmann(Planck18(conf), conf)
modes = linear_modes(white_noise(seed, conf), cosmo, conf)
ptcl, obsvbl = lpt(modes, cosmo, conf)
a_list = np.asarray(conf.a_nbody)
print('a steps', len(a_list), a_list[:3], a_list[-3:], flush=True)
ptcl, obsvbl = nbody_init(a_list[0], ptcl, obsvbl, cosmo, conf)
saved = []
def save(a, ptcl, k):
    mesh = scatter(ptcl, conf, mesh=jnp.zeros((G,) * 3, dtype=jnp.float32), val=1.0, cell_size=L / G)
    rho = np.asarray(mesh, dtype=np.float64)
    delta = (rho / rho.mean() - 1).astype(np.float32)
    assert abs(rho.sum() - N ** 3) < 1e-3 * N ** 3, ('mass not conserved', rho.sum())
    np.save(f'{out}/delta_{k:04d}.npy', delta); saved.append(dict(k=k, a=float(a), z=float(1 / a - 1), std=float(delta.std()), min=float(delta.min())))
nsteps = len(a_list) - 1
for i, (ap, an) in enumerate(zip(a_list[:-1], a_list[1:])):
    ptcl, obsvbl = nbody_step(ap, an, ptcl, obsvbl, cosmo, conf)
    if an >= a_save - 1e-9: save(an, ptcl, len(saved))
    print(f'PROGRESS {(i + 1) / nsteps:.3f} step {i + 1}/{nsteps} a={an:.4f} t={time.time() - t0:.0f}s', flush=True)
# control: large-scale power of the final density against pmwd's linear power at a = 1 (k < 0.06 h/Mpc, ratio should be near 1)
d = np.load(f'{out}/delta_{len(saved) - 1:04d}.npy').astype(np.float64)
dk = np.fft.rfftn(d) * (L / G) ** 3
kf = 2 * np.pi / L; kx = np.fft.fftfreq(G, 1 / G) * kf; kz = np.fft.rfftfreq(G, 1 / G) * kf
kk = np.sqrt(kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2)
P = np.abs(dk) ** 2 / L ** 3
sel = (kk > 0) & (kk < 0.06)
kb = kk[sel]; Pb = P[sel]
Plin = np.asarray(linear_power(jnp.asarray(kb), 1.0, cosmo, conf))
ratio = float(Pb.sum() / Plin.sum()); print('P(k<0.06)/P_lin =', ratio, 'modes', int(sel.sum()))
json.dump(dict(code='pmwd (arXiv:2211.09958)', cosmology='Planck18 (pmwd)', N=N, L_Mpc_h=L, grid=G, a_start=1 / 32, da=da, seed=seed,
               mesh='2x particle grid', Pk_ratio_k_lt_006=ratio, snapshots=saved), open(f'{out}/meta.json', 'w'), indent=1)
std = [s['std'] for s in saved]
ok = len(saved) > 1 and all(b > a for a, b in zip(std, std[1:])) and 0.5 < ratio < 2
print('snapshots', len(saved), 'delta std first/last', std[0], std[-1], 'growing', ok)
print('WALL', time.time() - t0)
sys.exit(0 if ok else 1)
