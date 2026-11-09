# DICTO 2026-11-09 harmonic-gaps study, part B float exploration (Monte Carlo, to form hypotheses only; every claim is then checked
# exactly in b_exact.py). Frame of #42 (sunstar_exact.py): cells of edge 2 on 2(i,j,k); dodecahedron DOD = cube + 6 roofs; the Dogstar's
# core CORE = DOD/phi^3; GSD = great stellated dodecahedron of CORE (63 stellation cells, corners = DOD's); the small Sunstar = CORE +
# the 6 Dogstars of the 1/phi^3 lattice round it. The gap = GSD - small Sunstar. Which pieces of the 1/phi^3 lattice (dodecahedra on
# even cells, Dogstars on odd cells) and which stellation cells of CORE make up the gap?
import os, sys, json, itertools, numpy as np
from collections import defaultdict
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
phi = (1 + 5 ** .5) / 2; s = phi ** -3
J = json.load(open(os.path.join(DATA, 'sunstar-exact.json')))
cells = [np.array(c) for c in J['gsd_cells_float']]; dog_ids = set(J['dogstar_cells'])
def H(P):
    h = ConvexHull(P); return h.equations[:, :3], -h.equations[:, 3]
CH = [H(c) for c in cells]
layer = []
cen0 = cells[0].mean(0)
for c in cells:                                    # layer by distance of centre (core 0, pyramids, wedges, spikes)
    layer.append(np.linalg.norm(c.mean(0)))
lay_sorted = sorted(set(np.round(layer, 6)))
lay = [lay_sorted.index(round(x, 6)) for x in layer]
C8 = np.array(list(itertools.product((1, -1), repeat=3)), float)
RID = np.array([r for a in (1, -1) for b in (1, -1) for r in ([0, a / phi, b * phi], [a / phi, b * phi, 0], [b * phi, 0, a / phi])], float)
DOD = np.vstack([C8, RID]); DH = H(DOD)
def in_h(X, h, tol=1e-12): n, d = h; return np.all(X @ n.T <= d + tol, axis=1)
def which_cell(X):
    out = np.full(len(X), -1)
    for i, h in enumerate(CH): out[np.where((out < 0) & in_h(X, h))] = i
    return out
rng = np.random.default_rng(7); N = 6_000_000; R = 3 ** .5
X = rng.uniform(-R, R, size=(N, 3)); boxvol = (2 * R) ** 3
gc = which_cell(X); inG = gc >= 0
# small lattice label: cell index k = round(x / 2s); even -> dodecahedron there; odd -> Dogstar unless inside a neighbour's dodecahedron
k = np.round(X / (2 * s)).astype(int); par = k.sum(1) % 2
own = k.copy()
odd = par == 1
for e in [np.array(v) for v in ([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])]:
    nb = k + e; Y = (X - nb * 2 * s) / s; m = odd & in_h(Y, DH)
    own[m] = nb[m]; odd = odd & ~m
even = (own.sum(1) % 2) == 0                                     # True: small dodecahedron, False: small Dogstar
l1 = np.abs(own).sum(1)
sun = (even & (l1 == 0)) | (~even & (l1 == 1))
gap = inG & ~sun
vol = lambda m: m.sum() / N * boxvol
dodv = (10 + 2 * 5 ** .5) * s ** 3; dogv = (6 - 2 * 5 ** .5) * s ** 3
print(f'GSD {vol(inG):.4f} (exact 63 cells {sum(ConvexHull(c).volume for c in cells):.4f}); small Sunstar inside GSD {vol(inG & sun):.4f} '
      f'(exact {dodv + 6 * dogv:.4f}); Sunstar outside GSD {vol(sun & ~inG):.5f}; gap {vol(gap):.4f}', flush=True)
code = (own[:, 0] + 50) * 10000 + (own[:, 1] + 50) * 100 + (own[:, 2] + 50)
u, inv = np.unique(code, return_inverse=True); n_in = np.bincount(inv, weights=inG, minlength=len(u))
pv = lambda ev: dodv if ev else dogv
groups = defaultdict(list)
for c, ni in zip(u, n_in):
    if ni == 0: continue
    o = (c // 10000 - 50, (c // 100) % 100 - 50, c % 100 - 50); ev = sum(o) % 2 == 0
    groups[('D' if ev else 'S', tuple(sorted(map(abs, o))))].append(ni / N * boxvol / pv(ev))
print('small-lattice pieces meeting GSD (orbit, count, mean fraction inside GSD, min, max):')
for (kk, sh), fs in sorted(groups.items(), key=lambda t: (t[0][1], t[0][0])):
    print(f'  {kk} {sh}  n={len(fs):3d}  mean {np.mean(fs):.3f}  min {min(fs):.3f}  max {max(fs):.3f}', flush=True)
# stellation cells: fraction of each in the gap
print('stellation cells of CORE (layer: count, fraction of the layer in the gap, per-cell min/max):')
for L in range(4):
    ids = [i for i in range(63) if lay[i] == L]
    fr = [((gc == i) & gap).sum() / max(1, (gc == i).sum()) for i in ids]
    inD = sum(1 for i in ids if i in dog_ids)
    print(f'  layer {L}: {len(ids)} cells ({inD} in the big Dogstar)  gap fraction mean {np.mean(fr):.3f} min {min(fr):.3f} max {max(fr):.3f}', flush=True)
    for i in ids: pass
res = {'gsd': vol(inG), 'gap': vol(gap), 'groups': {f'{a} {b}': [len(v), float(np.mean(v)), float(min(v)), float(max(v))] for (a, b), v in groups.items()},
       'cells': {i: [int(lay[i]), i in dog_ids, float(((gc == i) & gap).sum() / max(1, (gc == i).sum()))] for i in range(63)}}
json.dump(res, open(os.path.join(DATA, 'b_explore.json'), 'w'), indent=1)
print('FINAL ok' if abs(vol(inG & sun) - (dodv + 6 * dogv)) < 0.02 else 'FINAL FAIL: Sunstar volume inside GSD off')
