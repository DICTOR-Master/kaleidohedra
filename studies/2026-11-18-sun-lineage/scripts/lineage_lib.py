"""Lineage net change of neighbours (definition in README.md). Shared by lin_sun.py (granules) and lin_null.py (seeds).

M: sparse (end cells x start cells), M[c, a] = 1 when end cell c descends from start cell a (a in anc(c)).
Lineage contacts: pairs a < b of start cells with some descendant of a touching some descendant of b, or one end cell descending
from both (fused). Net change per cell = (|E0 minus lineage contacts| + |lineage contacts minus E0|) / N0."""
import numpy as np
import scipy.sparse as sp


def lineage_counts(E0, N0, ec, ed, n_end, M):
    """E0: int64 keys a * N0 + b (a < b) of start contacts; ec, ed: end contact pairs (end-cell indices); M: csr (n_end x N0).
    Returns dict lost, made, pairs (lineage contacts), fused (pairs joined in one end cell), size (sum of lineage sizes)."""
    M = sp.csr_matrix(M, dtype=np.int64); M.data[:] = 1
    A = sp.coo_matrix((np.ones(2 * len(ec), np.int64), (np.concatenate([ec, ed]), np.concatenate([ed, ec]))), shape=(n_end, n_end))
    A = (A + sp.identity(n_end, dtype=np.int64, format='coo')).tocsr()
    L = (M.T @ A @ M).tocoo()
    k = L.row < L.col
    keys = np.unique(L.row[k].astype(np.int64) * N0 + L.col[k])
    F = (M.T @ M).tocoo(); kf = F.row < F.col
    fused = int(np.unique(F.row[kf].astype(np.int64) * N0 + F.col[kf]).size)
    lost = int(np.setdiff1d(E0, keys, assume_unique=True).size); made = int(np.setdiff1d(keys, E0, assume_unique=True).size)
    return dict(lost=lost, made=made, pairs=int(keys.size), fused=fused, size=int(M.nnz))


def identity_test(seed=3):
    """With anc(c) = {c} (no births or deaths) the lineage count must equal the plain count |E0 xor E1| exactly."""
    rng = np.random.default_rng(seed); N = 300
    def rnd():
        a = rng.integers(0, N, 1500); b = rng.integers(0, N, 1500); m = a != b
        return np.unique(np.minimum(a[m], b[m]).astype(np.int64) * N + np.maximum(a[m], b[m]))
    E0, E1 = rnd(), rnd()
    M = sp.identity(N, dtype=np.int64, format='csr')
    r = lineage_counts(E0, N, E1 // N, E1 % N, N, M)
    plain = np.setdiff1d(E0, E1).size + np.setdiff1d(E1, E0).size
    return r['lost'] + r['made'] == plain and r['fused'] == 0 and r['pairs'] == E1.size
