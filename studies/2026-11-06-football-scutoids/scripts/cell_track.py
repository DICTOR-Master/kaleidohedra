"""Football scutoid study, step 2b, part 2: follow ONE cell (ball X and ball Y of the base layer, each with its half bridges; nearest-
surface cells from cut_cells.py) from its bottom to its top, slicing parallel to the layers. At each height: the cell's neighbours (shared
boundary >= MINLEN pixels). An event = a neighbour gained or lost. It is a SWAP (the scutoid move: a Y-junction inside the cell's side) when
the cell is present on both sides of the event and the neighbour gained/lost is present in the slice on both sides too (so the change is
not a cell of another layer appearing or ending). Numerical, voxels.  Run: python3 tools/runjob.py <this> <data file> [voxel]"""
import sys, numpy as np
exec(open('cut_cells.py').read().split('# slices')[0])
ref = {imgs.index((0, 0, 0, 0)): 'X', imgs.index((1, 0, 0, 0)): 'Y'}
NS = int(2 * h / VOX)
U = np.linspace(-0.9, 1.9, int(2.8 * np.linalg.norm(P1) / VOX)); Vv = np.linspace(-0.9, 1.9, int(2.8 * np.linalg.norm(P2) / VOX))
uu, vv = np.meshgrid(U, Vv, indexing='ij')
name = lambda b: f"{'XY'[imgs[b][0]]}({imgs[b][1]:+d},{imgs[b][2]:+d},{imgs[b][3]:+d})"
hist = {r: [] for r in ref}; pres = []
for k in range(NS):
    w = -1 + (k + 0.5) * 2 / NS
    X = uu[..., None] * P1 + vv[..., None] * P2 + w * T
    _, idx = tree.query(X.reshape(-1, 3), workers=-1); L = lab[idx].reshape(uu.shape)
    core = L[2:-2, 2:-2]; pres.append(set(np.unique(core)))
    for r in ref:
        nb = {}
        for a1, a2 in ((L[1:], L[:-1]), (L[:, 1:], L[:, :-1])):
            for s, t in ((a1, a2), (a2, a1)):
                m = (s == r) & (t != r)
                for x in t[m]: nb[x] = nb.get(x, 0) + 1
        hist[r].append({x for x, c in nb.items() if c >= MINLEN})
    if k % 10 == 0: print(f"  slice {k + 1}/{NS}", flush=True)
print(f"voxel {VOX}: {NS} slices over two layer periods (w = -1..1, height {2 * h:.3f}), one slice {2 * h / NS:.3f}")
swaps_total = 0
for r, nm in ref.items():
    ks = [k for k in range(NS) if r in pres[k]]
    print(f"cell {nm}: present in slices {ks[0]}..{ks[-1]} (height {(ks[-1] - ks[0] + 1) * 2 * h / NS:.2f}); neighbours per slice: "
          + " ".join(str(len(hist[r][k])) for k in ks))
    for k in ks[1:]:
        if k - 1 not in ks: continue
        gain, lost = hist[r][k] - hist[r][k - 1], hist[r][k - 1] - hist[r][k]
        if not (gain or lost): continue
        kind = []
        for x in gain: kind.append(('SWAP-gain' if x in pres[k - 1] else 'enters') + ' ' + name(x))
        for x in lost: kind.append(('SWAP-lose' if x in pres[k] else 'ends') + ' ' + name(x))
        swaps_total += sum(1 for s in kind if s.startswith('SWAP'))
        print(f"   slice {k} (w {-1 + (k + 0.5) * 2 / NS:+.3f}): " + "; ".join(sorted(kind)))
print(f"SWAP events (neighbour changes among cells present on both sides): {swaps_total}")
print("FINAL ok" if all(len(hist[r][k]) >= 3 for r in ref for k in range(NS) if r in pres[k]) and swaps_total > 0 else "FINAL FAIL (a cell section with fewer than 3 neighbours, or no events)")