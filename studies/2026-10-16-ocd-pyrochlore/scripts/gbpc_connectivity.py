# Fable, FLOAT check (2026-10-16): is G' (space minus the union of uncut RTs on the bcc sites) one connected periodic region? Voxel flood fill of one cell with periodic wrap.
import sys, io, os, contextlib, numpy as np
os.chdir('/home/dicto/kaleidohedra/studies/2026-10-16-ocd-pyrochlore')
src = open('scripts/golden_fill.py').read().split('# ---- all bodies')[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
Nn = np.array([fl(n) for n, d in RT['H']]); Dd = np.array([d.f() for n, d in RT['H']])
L = np.array([fl(b) for b in LB]).T
n = 72
g = (np.arange(n) + 0.5) / n
F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
X = F @ L.T
free = np.ones(len(X), bool)
for m in np.array(np.meshgrid(*[range(-2, 3)] * 3, indexing='ij')).reshape(3, -1).T:
    s = L @ m
    free &= ~np.all((X - s) @ Nn.T <= Dd + 1e-12, axis=1)
print('free fraction FLOAT', free.mean())
fr = free.reshape(n, n, n)
# BFS with lattice offsets
lab = -np.ones((n, n, n), int); off = np.zeros((n, n, n, 3), int); comps = []; perc = []
idx = np.argwhere(fr)
for start in map(tuple, idx):
    if lab[start] >= 0: continue
    k = len(comps); lab[start] = k; stack = [start]; cnt = 0; wraps = False
    while stack:
        p = stack.pop(); cnt += 1
        for ax in range(3):
            for dlt in (-1, 1):
                q = list(p); o = off[p].copy(); q[ax] += dlt
                if q[ax] < 0: q[ax] += n; o[ax] -= 1
                elif q[ax] >= n: q[ax] -= n; o[ax] += 1
                q = tuple(q)
                if not fr[q]: continue
                if lab[q] < 0: lab[q] = k; off[q] = o; stack.append(q)
                elif lab[q] == k and np.any(off[q] != o): wraps = True
    comps.append(cnt); perc.append(wraps)
cv = abs(np.linalg.det(L))
print('components per cell', len(comps), 'percolating', sum(perc))
big = max(comps); txt = f"DICTO · dictospheres.com\nFLOAT voxel flood fill, {n}^3 voxels per cell: free fraction {free.mean():.4f}; largest component {big} voxels = {big / free.sum():.2%} of the free voxels, percolating (wraps the cell): {perc[comps.index(big)]}; other components: {len(comps) - 1}, each at most {sorted(comps)[-2] if len(comps) > 1 else 0} voxels (slivers in the 36-degree wedges cut off by the voxel grid)\n"; print(txt); open("data/gbpc-connectivity.txt", "w").write(txt)
