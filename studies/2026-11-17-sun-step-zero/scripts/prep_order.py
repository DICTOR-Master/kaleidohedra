"""Frame-order controls for the step calibration (section "Swap rate at step 0", 16 Nov 2026).
Writes a copy of one field with its frames time-reversed ("rev") or shuffled by a fixed permutation ("shuf"), under a new run name
RUN-MODE, with the ORIGINAL increasing time stamps, so census.py reads it as an ordinary sequence. For a control sequence (an
*_exact.json beside it) the exact Delaunay pair sets are reordered the same way, so the exact count of the new sequence is known.
Usage: stepcal_prep.py DATA RUN VAR DZ OUTDIR MODE(rev|shuf) SEED"""
import sys, os, json, shutil
import numpy as np

data, run, var, dz, out, mode, seed = sys.argv[1:8]
os.makedirs(out, exist_ok=True)
F = np.load(f'{data}/{run}_{var}_dz{dz}.npy', mmap_mode='r')
n = F.shape[0]
order = np.arange(n)[::-1] if mode == 'rev' else np.random.default_rng(int(seed)).permutation(n)
new = f'{run}-{mode}'
G = np.lib.format.open_memmap(f'{out}/{new}_{var}_dz{dz}.npy', mode='w+', dtype=F.dtype, shape=F.shape)
for i, k in enumerate(order):
    G[i] = F[k]
    if i % 20 == 0: print(f'PROGRESS {(i + 1) / n:.4f} frame {i + 1}/{n}', flush=True)
G.flush()
shutil.copy(f'{data}/{run}_times.npy', f'{out}/{new}_times.npy')
if os.path.exists(f'{data}/{run}_meta.json'): shutil.copy(f'{data}/{run}_meta.json', f'{out}/{new}_meta.json')
ex = f'{data}/{run}_exact.json'
if os.path.exists(ex):
    E = json.load(open(ex))
    E['frame_pairs'] = [E['frame_pairs'][k] for k in order]; E['name'] = new; E['order'] = order.tolist()
    E['exact_swaps_total'] = None; E['exact_per_frame'] = None          # substep counts do not survive reordering
    json.dump(E, open(f'{out}/{new}_exact.json', 'w'))
ok = G.shape == F.shape and np.array_equal(np.asarray(G[0]), np.asarray(F[order[0]])) and np.array_equal(np.asarray(G[-1]), np.asarray(F[order[-1]]))
print('PREP', new, 'frames', n, 'first source frame', int(order[0]), flush=True)
print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
