# cut_lemma.py (from float_family.py), DICTO 10 Nov 2026 ("go ahead with both"): the CUT LEMMA for #43 step (A).
# Polar picture: X_k = polar(D_k), corners v = m/d (faces (m, d) of D_k). Candidate v is ACTIVE (a face of X_{k+1}) iff its foot point
# v/|v|^2 is a corner of D_{k+1}. A cut candidate's plane is excluded by some cutter w: w.v > |w|^2. Per level: cut fraction; are the
# cutters themselves active (never cut)?; maximum matching cut -> distinct cutter (Hopcroft-Karp): matching = #cut proves #cut <= #active.
# Original header: DICTO #43 Conjecture 1 (the OG's margin), study 2026-11-09: float exploration of the OG's downward family far beyond k = 8.
# D_0 = OG (exact, from the five-fold-octet tools, then float), D_k = P(D_{k-1}) = hull of the foot points of D_{k-1}'s face planes.
# t_min(D_k) = max over corners v of D_k and faces (m, d) of D_{k+1} of m.v/d (D_k inside t.D_{k+1}).
# Records per k: corners, faces, R, r, H, t_min, (R/r)^2, the argmax, and the normalised radial profile (for shape convergence).
# Sanity: t_min for k = 0..8 must match Table 7 of #43 to 1e-9; corner/face counts must match the exact counts (k <= 11).
# usage: python -u float_family.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull
OUT = os.path.abspath(sys.argv[3])                      # resolved before the chdir below
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])   # OG (exact), G (60 exact rotations)
KMAX = int(sys.argv[2])
OGf = np.array([[x.f() for x in v] for v in OG]); Gf = np.array([[[x.f() for x in row] for row in M] for M in G])

def faces(V, tol=1e-9):
    """distinct face planes of hull(V): unit normals m, distances d, and the hull's corners. Coplanar hull triangles are merged
    by joining neighbouring triangles whose planes agree within tol (union-find over hull adjacency; memory O(n))."""
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    roots = np.array([find(i) for i in range(n)]); u, inv = np.unique(roots, return_inverse=True)
    M = np.zeros((len(u), 3)); Dd = np.zeros(len(u)); cnt = np.bincount(inv)
    np.add.at(M, inv, E[:, :3]); np.add.at(Dd, inv, -E[:, 3]); M /= np.linalg.norm(M, axis=1)[:, None]; Dd /= cnt
    return M, Dd, np.unique(h.vertices)

def cover_radius(M):
    """covering radius (rad) of the unit normal set M: arccos of the smallest facet distance of hull(M)."""
    return float(np.arccos((-ConvexHull(M).equations[:, 3]).min()))

def symmetrise(W):
    """orbit closure under the 60 rotations, then merge points closer than 1e-9 (kills float drift of the symmetry)."""
    X = np.vstack([W @ g.T for g in Gf]); X = X[np.lexsort(X.T[::-1])]
    from scipy.spatial import cKDTree
    t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)):
        groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])

def sym_err(V):
    from scipy.spatial import cKDTree
    t = cKDTree(V); return max(t.query(V @ g.T)[0].max() for g in Gf)

TABLE7 = [1.133581, 1.117382, 1.103147, 1.145898, 1.042441, 1.086902, 1.025657, 1.059516, 1.138077]
EXACT_COUNTS = {0: (102, 80), 1: (80, 132), 2: (132, 140), 3: (140, 162), 4: (162, 200), 5: (200, 252), 6: (192, 320), 7: (260, 402),
                8: (312, 500), 9: (500, 732)}
TARGET = 3 / ((1 + 5 ** .5) / 2) ** 2
res = {'mark': 'DICTO #43 Conjecture 1, float downward family, 2026-11-09 · DICTO · dictospheres.com', 'k': []}
V = OGf; FF = faces(V); t0 = time.time(); ok_all = True
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
rows_out = []; ok_all = True
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None])                             # listed points of D_{k+1} = foot points of D_k's faces
    FN = faces(W); M2, D2, cor2 = FN
    act = np.zeros(len(W), bool); act[cor2] = True               # candidate i active iff W[i] is a corner of D_{k+1}
    X = W / np.einsum('ij,ij->i', W, W)[:, None]                  # polar candidates v_i = W_i / |W_i|^2 (corners of X_k)
    nX = np.linalg.norm(X, axis=1); U = X / nX[:, None]; tree = cKDTree(U)
    cut = np.where(~act)[0]; rows, cols = [], []; cutters_active = True; ncut_by = {}
    for i in cut:
        v = X[i]; cand = tree.query_ball_point(U[i], 0.6)       # chord 0.6 = angle ~35 deg: far more than any cutter needs
        cand = np.array([j for j in cand if j != i])
        if len(cand) == 0: continue
        viol = cand[(X[cand] @ v) > np.einsum('ij,ij->i', X[cand], X[cand]) * (1 + 1e-12)]
        for j in viol: rows.append(i); cols.append(j)
        if len(viol) and not act[viol].any(): cutters_active = False
    nc = len(cut); na = int(act.sum())
    if nc:
        A = csr_matrix((np.ones(len(rows)), (np.searchsorted(cut, rows), cols)), shape=(nc, len(W)))
        mt = maximum_bipartite_matching(A, perm_type='column'); matched = int((mt >= 0).sum())
        # matching to ACTIVE cutters only
        keep = act[np.array(cols)] if cols else np.zeros(0, bool)
        Aa = csr_matrix((np.ones(int(keep.sum())), (np.searchsorted(cut, np.array(rows)[keep]), np.array(cols)[keep])), shape=(nc, len(W)))
        ma = int((maximum_bipartite_matching(Aa, perm_type='column') >= 0).sum())
        uncut = len(set(rows)) == nc
        # capacity 2: each active cutter may take two cut candidates (columns doubled)
        ra = np.array(rows)[keep]; ca = np.array(cols)[keep]
        A2 = csr_matrix((np.ones(2 * len(ra)), (np.concatenate([np.searchsorted(cut, ra)] * 2), np.concatenate([ca, ca + len(W)]))), shape=(nc, 2 * len(W)))
        m2 = int((maximum_bipartite_matching(A2, perm_type='column') >= 0).sum())
    else: matched = ma = m2 = 0; uncut = True
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f} level {k}', flush=True)
    print(f'k {k:3d}: candidates {len(W):6d} active {na:6d} cut {nc:6d} ({nc / len(W):.3f}) | every cut has a cutter: {uncut} | cutters always include an active one: {cutters_active} | matching cut->distinct cutter {matched}/{nc}, ->distinct ACTIVE cutter {ma}/{nc}, with each active cutter taking up to two {m2}/{nc}', flush=True)
    rows_out.append(dict(k=k, cand=len(W), active=na, cut=nc, matched=matched, matched_active=ma, matched_cap2=m2, has_cutter=uncut))
    ok_all &= uncut
    V, FF = W, FN
json.dump(rows_out, open(OUT, 'w'))
full = all(r['matched_active'] == r['cut'] for r in rows_out)
print('every level: each cut candidate matched to its own ACTIVE cutter (=> cut <= active, i.e. at most half cut):', full)
print('FINAL ok' if ok_all else 'FINAL FAIL: a cut candidate without a cutter (geometry or tolerance error)')
