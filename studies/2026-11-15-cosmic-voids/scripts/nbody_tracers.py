"""Rerun of an N-body run of nbody_pm.py (same code pmwd, same arguments, same seed) that also saves the positions of a FIXED random subset
of particles (tracers, the same particles at every snapshot) for the grid-free basins (test 2 of the grid-or-physics follow-up).
pmwd: Li, Lanusse, Modi et al. 2022, arXiv:2211.09958, BSD-3-Clause; we call its functions and copy none of its code.
Saves tracers_KKKK.npy (float32, n x 3, Mpc/h, wrapped into [0, L)) and the cloud-in-cell density contrast delta_KKKK.npy (G^3, all
particles) at every step with a >= a_save; the tracer order is random, so the first n/m rows are themselves a random 1/m subset.
Control: every 32nd saved density is compared with the earlier run's delta_KKKK.npy (same code and seed; must agree to 5% of the std,
the exact deviation is printed; floating-point order in the threaded scatter may differ).
Usage: nbody_tracers.py OUT N L G a_save da seed subsample REF_DIR [a_stop]"""
import sys, os, json, time
import numpy as np
import jax, jax.numpy as jnp
jax.config.update('jax_enable_x64', False)
from pmwd import Configuration, Planck18, boltzmann, white_noise, linear_modes, lpt, scatter
from pmwd.nbody import nbody_init, nbody_step
out, N, L, G, a_save, da, seed, sub, ref = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), \
    float(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), sys.argv[9]
a_stop = float(sys.argv[10]) if len(sys.argv) > 10 else 1.0
os.makedirs(out, exist_ok=True)
t0 = time.time()
conf = Configuration(L / N, (N,) * 3, mesh_shape=2, a_start=1/32, a_stop=1.0, a_nbody_maxstep=da)
cosmo = boltzmann(Planck18(conf), conf)
modes = linear_modes(white_noise(seed, conf), cosmo, conf)
ptcl, obsvbl = lpt(modes, cosmo, conf)
a_list = np.asarray(conf.a_nbody)
ptcl, obsvbl = nbody_init(a_list[0], ptcl, obsvbl, cosmo, conf)
pick = np.random.default_rng(12345).permutation(N ** 3)[:N ** 3 // sub]
saved = []; ctrl = []


def cic(ptcl):
    mesh = scatter(ptcl, conf, mesh=jnp.zeros((G,) * 3, dtype=jnp.float32), val=1.0, cell_size=L / G)
    rho = np.asarray(mesh, dtype=np.float64); return (rho / rho.mean() - 1).astype(np.float32)


nsteps = len(a_list) - 1
for i, (ap, an) in enumerate(zip(a_list[:-1], a_list[1:])):
    if an > a_stop + 1e-9: break
    ptcl, obsvbl = nbody_step(ap, an, ptcl, obsvbl, cosmo, conf)
    if an >= a_save - 1e-9:
        k = len(saved)
        pos = np.asarray(ptcl.pos(dtype=jnp.float32, wrap=True))[pick] % L
        np.save(f'{out}/tracers_{k:04d}.npy', pos.astype(np.float32)); saved.append(dict(k=k, a=float(an)))
        d = cic(ptcl); np.save(f'{out}/delta_{k:04d}.npy', d)
        rp = f'{ref}/delta_{k:04d}.npy'
        if k % 32 == 0 and os.path.exists(rp):
            r = np.load(rp); dev = float(np.abs(d - r).max() / r.std()); ctrl.append(dict(k=k, a=float(an), max_dev_over_std=dev))
            print(f'control k={k} a={an:.4f} max |delta - earlier run| / std = {dev:.2e}', flush=True)
    print(f'PROGRESS {(i + 1) / nsteps:.3f} step {i + 1}/{nsteps} a={an:.4f} t={time.time() - t0:.0f}s', flush=True)
json.dump(dict(code='pmwd (arXiv:2211.09958)', N=N, L_Mpc_h=L, grid=G, da=da, seed=seed, subsample=sub, n_tracers=len(pick),
               tracer_rng_seed=12345, snapshots=saved, control=ctrl, ref=os.path.basename(ref.rstrip('/'))), open(f'{out}/meta.json', 'w'), indent=1)
ok = len(saved) > 1 and all(c['max_dev_over_std'] < 0.05 for c in ctrl)
print('snapshots', len(saved), 'controls', ctrl, 'ok', ok)
print('WALL', time.time() - t0)
sys.exit(0 if ok else 1)
