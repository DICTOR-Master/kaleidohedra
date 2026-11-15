"""Register consecutive Ni states by orientation fingerprints: for each grain of state i, the grain of state i+1 with the smallest
misorientation (cubic symmetry, both quaternion conventions tried); pairs below 0.5 deg vote for the centroid translation."""
import sys, h5py, numpy as np, itertools
sys.path.insert(0, sys.argv[2]); from ni_probe import OPS, load
D = sys.argv[1]; G = 'DataContainers/ImageDataContainer/'
def mats(q, wfirst):
    if wfirst: w, x, y, z = q.T
    else: x, y, z, w = q.T
    return np.stack([np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], -1),
                     np.stack([2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], -1),
                     np.stack([2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)], -1)], -2)
def feat(i):
    f = h5py.File(f'{D}/An{i}new6.dream3d', 'r')
    return f[G + 'CellFeatureData/AvgQuats'][:], f[G + 'CellFeatureData/Centroids'][:], f[G + 'CellFeatureData/EquivalentDiameters'][:, 0]
for i in range(5):
    qa, ca, da = feat(i); qb, cb, db = feat(i + 1)
    for wf in (False, True):
        Ma, Mb = mats(qa[1:], wf), mats(qb[1:], wf)
        big = np.argsort(-da[1:])[:300]
        best = []
        for a in big:
            R = np.einsum('ij,bkj->bik', Ma[a], Mb)               # A_a B_b^T
            tr = np.einsum('sij,bji->bs', OPS, R).max(1)
            ang = np.degrees(np.arccos(np.clip((tr - 1) / 2, -1, 1)))
            b = ang.argmin(); best.append((a + 1, b + 1, ang[b]))
        best = np.array(best); good = best[best[:, 2] < 0.5]
        if len(good) < 5: print(i, 'wfirst', wf, 'pairs < 0.5 deg', len(good)); continue
        dc = cb[good[:, 1].astype(int)] - ca[good[:, 0].astype(int)]
        med = np.median(dc, 0); spread = np.median(np.abs(dc - med), 0)
        print(i, 'wfirst', wf, 'pairs < 0.5 deg', len(good), 'of 300; centroid shift median', med.round(1), 'MAD', spread.round(1))
