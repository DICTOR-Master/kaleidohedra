"""Probe the public Ni HEDM grain maps (Bhattacharya et al., Science 374 (2021) 189; data archive of G. S. Rohrer, CMU):
align consecutive states by their stated origins (arrays are z, y, x; spacing x, y, z) and match grains by largest voxel overlap;
check the match by misorientation with cubic symmetry."""
import sys, h5py, numpy as np, itertools
D = sys.argv[1]
G = 'DataContainers/ImageDataContainer/'
def cubic_ops():
    ops = []
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3)); M[range(3), p] = s
            if np.linalg.det(M) > 0: ops.append(M)
    return np.array(ops)
OPS = cubic_ops()
def qmat(q):          # dream3d quats stored x, y, z, w
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
def misor(qa, qb):
    A, B = qmat(qa), qmat(qb); R = A @ B.T
    tr = np.einsum('kij,ji->k', OPS, R)
    return np.degrees(np.arccos(np.clip((tr.max() - 1) / 2, -1, 1)))
def load(i):
    f = h5py.File(f'{D}/An{i}new6.dream3d', 'r')
    return f[G + 'CellData/FeatureIds'][..., 0], f[G + 'CellFeatureData/AvgQuats'][:], f[G + '_SIMPL_GEOMETRY/ORIGIN'][:], f[G + '_SIMPL_GEOMETRY/SPACING'][:]
def common(a, oa, b, ob, sp):
    off = np.round((ob - oa) / sp).astype(int)[::-1]        # b index + off = a index (z, y, x)
    sl_a, sl_b = [], []
    for k in range(3):
        lo = max(0, off[k]); hi = min(a.shape[k], b.shape[k] + off[k])
        sl_a.append(slice(lo, hi)); sl_b.append(slice(lo - off[k], hi - off[k]))
    return a[tuple(sl_a)], b[tuple(sl_b)], off
if __name__ == '__main__':
    S = [load(i) for i in range(6)]
    for i in range(5):
        a, qa, oa, sp = S[i]; b, qb, ob, _ = S[i + 1]
        A, B, off = common(a, oa, b, ob, sp)
        m = (A > 0) & (B > 0)
        key = A[m].astype(np.int64) * 100000 + B[m]; u, c = np.unique(key, return_counts=True)
        best = {}
        for x, y, n in zip(u // 100000, u % 100000, c):
            if n > best.get(x, (0, 0))[1]: best[x] = (y, n)
        mis = np.array([misor(qa[x], qb[y]) for x, (y, n) in list(best.items())[:400]])
        print(i, 'offset zyx', off, 'overlap voxels', int(m.sum()), 'matched', len(best), 'misorientation median', np.median(mis).round(2),
              'frac <2 deg', (mis < 2).mean().round(3))
