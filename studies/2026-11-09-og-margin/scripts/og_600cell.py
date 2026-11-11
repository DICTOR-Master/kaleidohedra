# og_600cell.py, DICTO 11 Nov 2026 ("I thought every 4D was identified" -> "yes test it against the 600-cell").
# The 600-cell's symmetry H4 contains our icosahedral group as the stabiliser of a vertex axis. Put that axis along the slider (lam),
# match the icosahedral orientation (our 5-fold axes -> the standard ones, Kabsch over the matched axis sets), and compare the hop sweep's
# cell (facet) normals a_i = (R X_i, -1/s) with the 600-cell's directions: its 120 vertices, its 600 cell normals (= 120-cell vertices),
# edge directions (720) and 2-face normals are NOT used (too dense to be informative).
# FAIR TEST: one slider scale s per level for all cells (s scanned, plus every s that makes some orbit match exactly); score = number of
# orbit classes whose normal lies within TOL of a 600-cell direction. Axis orbits match for free at a suitable s, so the score is compared
# with a BASELINE: same directions, radii |X| of each orbit multiplied by random factors in [0.8, 1.25] (50 draws), same s search.
# usage: python -u og_600cell.py <five-fold-octet dir> <kmin> <kmax> <out.json>
import sys, os, json, itertools, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); K1, K2, OUTJ = int(sys.argv[2]), int(sys.argv[3]), os.path.abspath(sys.argv[4])
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0])
from scipy.spatial import cKDTree
phi = (1 + 5 ** .5) / 2
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b])
        if inv % 2 == 0: out.append([v[p[q]] for q in range(4)])
    return out
V600 = [list(v) for v in itertools.product([0], [0], [0], [1, -1])] + [list(v) for v in set(itertools.permutations([1, 0, 0, 0]))] + [list(v) for v in set(itertools.permutations([-1, 0, 0, 0]))]
V600 = [v for v in V600 if sum(abs(x) for x in v) == 1]
V600 += [list(s) for s in itertools.product([.5, -.5], repeat=4)]
for sg in itertools.product([1, -1], repeat=3):
    V600 += even_perms([sg[0] * phi / 2, sg[1] * .5, sg[2] / (2 * phi), 0])
V600 = np.unique(np.round(np.array(V600), 12), axis=0); assert len(V600) == 120, len(V600)
# 600-cell cell normals = centroids of its 600 tetrahedra: 4 mutually adjacent vertices (edge length 1/phi for circumradius 1)
E = np.abs(np.linalg.norm(V600[:, None] - V600[None], axis=2) - 1 / phi) < 1e-9
cells = set()
for a in range(120):
    nb = np.where(E[a])[0]
    for b, c, d in itertools.combinations(nb, 3):
        if E[b, c] and E[b, d] and E[c, d]: cells.add(tuple(sorted((a, b, c, d))))
assert len(cells) == 600, len(cells)
C600 = np.array([V600[list(c)].mean(0) for c in cells]); C600 /= np.linalg.norm(C600, axis=1)[:, None]
DIRS = {'vertices': V600, 'cell normals': C600}
# vertex axis = (0,0,0,1); its H3 acts on the first three coordinates; standard 5-fold axes there: neighbours of (0,0,0,1) projected
nbr = V600[E[np.where((V600 == [0, 0, 0, 1]).all(1))[0][0]]][:, :3]; std5 = nbr / np.linalg.norm(nbr, axis=1)[:, None]   # 12 icosahedron dirs
def axes5():
    out = []
    for g in Gf:
        if abs(np.trace(g) - (1 + 2 * np.cos(2 * np.pi / 5))) < 1e-9:
            w, v = np.linalg.eig(g); a = np.real(v[:, np.argmin(abs(w - 1))]); out += [a / np.linalg.norm(a), -a / np.linalg.norm(a)]
    return np.unique(np.round(np.array(out), 10), axis=0)
our5 = axes5(); assert len(our5) == 12, len(our5)
best = None
for i0 in range(12):
    for j0 in range(12):
        a1, b1 = our5[0], std5[i0]
        cand = [j for j in range(12) if abs(our5[1] @ our5[0] - std5[j] @ b1) < 1e-9]
        for j in cand:
            P = np.stack([our5[0], our5[1], np.cross(our5[0], our5[1])]); Q = np.stack([b1, std5[j], np.cross(b1, std5[j])])
            U, S, Vt = np.linalg.svd(Q.T @ P); R = U @ Vt
            if np.linalg.det(R) < 0: continue
            err = cKDTree(std5).query(our5 @ R.T)[0].max()
            if best is None or err < best[0]: best = (err, R)
        break
assert best[0] < 1e-9, best[0]; R = best[1]
def score(X, s, D, tol):
    a = np.hstack([X @ R.T, -np.ones((len(X), 1)) / s]); a /= np.linalg.norm(a, axis=1)[:, None]
    t = cKDTree(np.vstack([D, -D])); d = t.query(a)[0]; return d < tol
rng = np.random.default_rng(0); rows = []; ok = True
V = OGf; FF = faces(V)
for k in range(K2 + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W)
    if k >= K1:
        X = W / np.einsum('ij,ij->i', W, W)[:, None]; X /= np.linalg.norm(X, axis=1).max(); n = len(X)
        tree = cKDTree(X); perms = [tree.query(X @ g.T)[1] for g in Gf]; orb = -np.ones(n, int); nrep = 0
        for i in range(n):
            if orb[i] < 0:
                for p_ in perms: orb[p_[i]] = nrep
                nrep += 1
        row = dict(k=k, cells=n, orbits=nrep)
        for name, D in DIRS.items():
            def best_s(Xx):
                # candidate s: every s making some (orbit, direction) pair exact: a || D  <=>  RX/|RX| = D3/|D3| and (1/s)/|RX| = -D4/|D3|
                Dn = np.vstack([D, -D]); D3 = Dn[:, :3]; n3 = np.linalg.norm(D3, axis=1); okd = (n3 > 1e-9) & (Dn[:, 3] < -1e-9)
                u = Xx @ R.T; nu = np.linalg.norm(u, axis=1); dirs = u / nu[:, None]
                tD = cKDTree(D3[okd] / n3[okd][:, None]); dd, jj = tD.query(dirs)
                ss = []
                for i in np.where(dd < 1e-6)[0]:
                    d4 = Dn[okd][jj[i]]; ss.append(-np.linalg.norm(d4[:3]) / (d4[3] * nu[i]))
                ss = sorted(set(np.round(ss, 9))) + list(np.geomspace(0.05, 20, 400))
                bestv = (-1, None)
                for s in ss:
                    hit = score(Xx, s, D, 1e-6); m = len(set(orb[hit].tolist()))
                    if m > bestv[0]: bestv = (m, s)
                return bestv
            m, s = best_s(X)
            base = []
            for _ in range(50):
                f = rng.uniform(0.8, 1.25, nrep)[orb]; base.append(best_s(X * f[:, None])[0])
            row[name] = dict(best_s=s, orbits_matched=m, baseline_mean=float(np.mean(base)), baseline_max=int(max(base)))
            print(f'k {k:2d} {name:13s}: best slider scale s {s:.6f}: {m}/{nrep} orbit classes along 600-cell directions | baseline (random radii) mean {np.mean(base):.2f} max {max(base)}', flush=True)
        rows.append(row)
    V, FF = W, FN
json.dump(dict(rotation=R.tolist(), rows=rows), open(OUTJ, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL')
