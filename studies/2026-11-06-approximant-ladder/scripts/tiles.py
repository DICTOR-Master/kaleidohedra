"""Rung tiles (DICTO 11-06 ladder; "can we grow golden skin inside"): the golden rhombohedra of an approximant n/m. From the cut-and-
project points (cutproject.py), a rhombohedron with corner x and edges e_i, e_j, e_k exists when all 8 corners are points (Z^6 labels).
Per periodic cell: prolate and oblate counts, total volume = cell volume (check: a true tiling), and the clusters: around each point with
the full icosahedral star, the 20 prolate rhombohedra that close into a rhombic triacontahedron (RT). Usage: tiles.py qn qd R"""
import itertools, sys, numpy as np
exec(open('cutproject.py').read().split('print("FINAL ok")')[0].replace('print(', '(lambda *a, **k: None)('))
lab = {tuple(v): x for v, x in zip(map(tuple, V), X)}
I6 = np.eye(6, dtype=int); tiles = []
for v in V:
    for i, j, k in itertools.combinations(range(6), 3):
        cs = [tuple(v + a * I6[i] + b * I6[j] + c * I6[k]) for a, b, c in itertools.product((0, 1), repeat=3)]
        if all(c in lab for c in cs):
            E = Epar[[i, j, k]]; tv = abs(np.linalg.det(E))
            tiles.append((lab[tuple(v)], (i, j, k), tv))
vols = sorted({round(t[2], 6) for t in tiles}); print("tile volumes:", vols, "(prolate = larger)")
f = lambda Y: np.all((Y @ Binv.T >= -1e-9) & (Y @ Binv.T < 1 - 1e-9), axis=1)
cen = np.array([t[0] + Epar[list(t[1])].sum(0) / 2 for t in tiles])
inc = f(cen); vin = sum(t[2] for t, m in zip(tiles, inc) if m)
npro = sum(1 for t, m in zip(tiles, inc) if m and abs(t[2] - vols[-1]) < 1e-6); nobl = sum(1 for t, m in zip(tiles, inc) if m and abs(t[2] - vols[0]) < 1e-6)
print(f"per cell: {npro} prolate + {nobl} oblate rhombohedra, volume {vin:.4f} vs cell {vol:.4f} -> {'TILING OK' if abs(vin - vol) < 1e-6 else 'MISMATCH'}")
# clusters: stars in the cell, each with 20 prolate tiles having the star point as a corner
starc = [s for s in star if f(np.array([s]))[0]]
sp = {tuple(np.round(s, 6)) for s in starc}; around = {k: 0 for k in sp}
for t in tiles:
    if abs(t[2] - vols[-1]) > 1e-6: continue
    corners = [t[0] + np.array(b) @ Epar[list(t[1])] for b in itertools.product((0, 1), repeat=3)]   # fixed 11-06 (Fable review): combination of the three edge vectors
    for c in corners:
        key = tuple(np.round(c, 6))
        if key in around: around[key] += 1
print(f"cluster centres per cell: {len(starc)}; prolate rhombohedra at each: {sorted(around.values())}")
rt = sum(1 for n_ in around.values() if n_ == 20)
print(f"full rhombic triacontahedra (20 prolate round the centre): {rt}; their share of the cell: {rt * 20 * vols[-1] / vol:.4f}")
print("FINAL ok")
