# Airflow proxy for the Knitted HexOct (DICTO proposed): members (links and in-sheet members) as capsules of radius r
# (cylinders with rounded ends) on the periodic rectangular cell 1 x sqrt(3) a, sheets 0..11, fluid domain between the
# centre planes of the bottom and top sheets.
#  (1) open fraction along the stacking axis: share of the cell area through which a straight line along z misses every
#      member (exact for capsules: the line misses a capsule iff its plan point is > r from the capsule's plan segment);
#  (2) tortuosity: shortest open path from each open voxel of the top plane to the bottom plane (26-neighbour voxel
#      graph, periodic in x and y, multi-source Dijkstra from the bottom), divided by the thickness.
# Usage: flow.py <seq> <h> <r> <out.json>     (seq = a SEQ_LABELS key, or 'L:<labels>')
import sys, json, numpy as np, scipy.sparse as sps
from scipy.sparse.csgraph import dijkstra
from lattice import build, word_from_labels, SEQ_LABELS, D, R3
CX, CY = 1.0, R3

def segments(labels):
    lat = build(word_from_labels(labels)); X = lat['X']; seg = []
    # each member once per orbit of the 1 x sqrt(3) translations: from its 'lower' end (v up, or in-sheet with v
    # pointing to +y, or along +x), when that end lies inside the rectangular cell
    for a, b, s, kind in lat['members']:
        for p, v in ((a, X[b] + s - X[a]), (b, X[a] - s - X[b])):
            pos = v[2] > 1e-9 or (abs(v[2]) < 1e-9 and (v[1] > 1e-9 or (abs(v[1]) < 1e-9 and v[0] > 0)))
            if pos and X[p, 0] < CX - 1e-9 and X[p, 1] < CY - 1e-9: seg.append((X[p].copy(), X[p] + v, kind))
    assert len(seg) == 2 * lat['N'] * 3 + 2 * (lat['N'] - 1) * 3, len(seg)  # 2 nodes/sheet: 3 sheet members + 3 up-links each
    return seg, lat['N']

def dist_seg(P, a, b):
    ab = b - a; t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1); return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)

def open_fraction(seg, r, h2=0.002):
    xs = (np.arange(int(round(CX / h2))) + 0.5) * h2; ys = (np.arange(int(round(CY / h2))) + 0.5) * h2
    gx, gy = np.meshgrid(xs, ys, indexing='ij'); P = np.stack([gx.ravel(), gy.ravel()], 1); cov = np.zeros(len(P), bool)
    for a, b, _ in seg:
        for ox in (-CX, 0, CX):
            for oy in (-CY, 0, CY):
                o = np.array([ox, oy]); cov |= dist_seg(P, a[:2] + o, b[:2] + o) <= r
    return 1 - cov.mean(), (~cov).reshape(gx.shape)

def voxels(seg, N, r, h):
    nx, ny = int(round(CX / h)), int(round(CY / h)); H = (N - 1) * D; nz = int(round(H / h)) + 1
    hx, hy, hz = CX / nx, CY / ny, H / (nz - 1)
    solid = np.zeros((nx, ny, nz), bool)
    for a, b, _ in seg:
        lo = np.minimum(a, b) - r; hi = np.maximum(a, b) + r
        ix = np.arange(int(np.floor(lo[0] / hx)) - 1, int(np.ceil(hi[0] / hx)) + 2)
        iy = np.arange(int(np.floor(lo[1] / hy)) - 1, int(np.ceil(hi[1] / hy)) + 2)
        iz = np.arange(max(0, int(np.floor(lo[2] / hz)) - 1), min(nz, int(np.ceil(hi[2] / hz)) + 2))
        GX, GY, GZ = np.meshgrid((ix + 0.5) * hx, (iy + 0.5) * hy, iz * hz, indexing='ij')
        P = np.stack([GX.ravel(), GY.ravel(), GZ.ravel()], 1); m = dist_seg(P, a, b) <= r
        I, Jy, K = np.meshgrid(ix % nx, iy % ny, iz, indexing='ij'); solid[I.ravel()[m], Jy.ravel()[m], K.ravel()[m]] = True
    return solid, (hx, hy, hz), H

def tortuosity(solid, hs, H):
    nx, ny, nz = solid.shape; idx = -np.ones(solid.shape, np.int64); fl = ~solid; idx[fl] = np.arange(fl.sum())
    rows, cols, w = [], [], []
    offs = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) > (0, 0, 0)]
    for dx, dy, dz in offs:
        rl = np.roll(np.roll(idx, -dx, 0), -dy, 1)
        a = idx[:, :, max(0, -dz):nz - max(0, dz)]; b = rl[:, :, max(0, dz):nz - max(0, -dz)]
        m = (a >= 0) & (b >= 0); rows.append(a[m]); cols.append(b[m])
        w.append(np.full(m.sum(), np.sqrt((dx * hs[0]) ** 2 + (dy * hs[1]) ** 2 + (dz * hs[2]) ** 2)))
    n = fl.sum(); G = sps.coo_matrix((np.concatenate(w), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsr()
    src = idx[:, :, 0][idx[:, :, 0] >= 0]; dist = dijkstra(G, directed=False, indices=src, min_only=True)
    top = idx[:, :, -1][idx[:, :, -1] >= 0]; dt = dist[top]; ok = np.isfinite(dt)
    tau = dt[ok] / H
    return dict(porosity=float(fl.mean()), top_open=int(len(top)), top_connected=int(ok.sum()),
                tau_min=float(tau.min()), tau_mean=float(tau.mean()), tau_median=float(np.median(tau)),
                tau_p90=float(np.percentile(tau, 90)), frac_tau_1=float(np.mean(tau < 1 + 1e-9)),
                hist=np.histogram(tau, bins=40, range=(1, 1.4))[0].tolist())

if __name__ == '__main__':
    seq, h, r, outp = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    labels = seq[2:] if seq.startswith('L:') else SEQ_LABELS[seq]
    seg, N = segments(labels)
    res = dict(seq=seq, labels=labels, word=word_from_labels(labels), h=h, r=r, n_segments=len(seg))
    of, mask = open_fraction(seg, r); res['open_fraction_z'] = float(of)
    np.save(outp.replace('.json', '_openmask.npy'), mask)
    for rr in (0.03, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2): res.setdefault('open_fraction_vs_r', {})[str(rr)] = float(open_fraction(seg, rr, 0.004)[0])
    solid, hs, H = voxels(seg, N, r, h); res['voxels'] = list(solid.shape); res['H'] = H
    res['voxel_open_columns'] = float((~solid.any(2)).mean())
    res.update(tortuosity(solid, hs, H))
    json.dump(res, open(outp, 'w'), indent=1); print(seq, h, r, 'done', res['open_fraction_z'], res['tau_mean'])
