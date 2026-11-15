"""Job A: exact sweep census. (1) Simple uniform 4-polytopes by Wythoff construction + Qhull: f-vector, simplicity,
h1, h2, h2/h1. (2) Generic linear sweeps of periodic Poisson-Voronoi tessellations in 3D and 4D (= 2D / 3D power
diagrams with linearly changing weights): index census, exact identities, swaps per birth. (3) Random simple 4-polytopes
(polars of random points on S^3). (4) Static tissue statistics: 2D Poisson-Voronoi (plane, sphere) and planar sections
of 3D Poisson-Voronoi. Usage: sweeps.py [--pilot] OUT.json"""
import sys, json, time, itertools
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nulllib import sweep_indices, periodic_delaunay, circumcentres, polygon_area, tissue_stats, replicate

PILOT = '--pilot' in sys.argv
OUT = sys.argv[-1]
rng = np.random.default_rng(20261115)
R = {}
CHECKS = []


def check(name, ok, info=''):
    CHECKS.append((name, bool(ok), str(info)))
    print(('X PASS ' if ok else 'X FAIL ') + name + ' ' + str(info), flush=True)


def save():
    R['checks'] = CHECKS
    json.dump(R, open(OUT, 'w'), indent=1)


t0 = time.time()
# ---------------------------------------------------------------- (1) polytopes
def wythoff(m, ring):
    """Coxeter diagram as matrix m (m[i][j] = branch order, 2 = no branch), ring = ringed nodes. Orbit of the seed point."""
    k = len(ring)
    G = np.array([[1.0 if i == j else -np.cos(np.pi / m[i][j]) for j in range(k)] for i in range(k)])
    Rt = np.linalg.cholesky(G)  # rows = simple roots, r_i . r_j = G_ij
    x = np.linalg.solve(Rt, np.array([1.0 if r else 0.0 for r in ring]))
    pts = {tuple(np.round(x, 6)): x}
    front = [x]
    while front:
        nf = []
        for p in front:
            for r in Rt:
                q = p - 2 * (r @ p) * r
                key = tuple(np.round(q, 6))
                if key not in pts:
                    pts[key] = q; nf.append(q)
        front = nf
    V = np.array(list(pts.values()))
    from scipy.spatial import cKDTree
    pairs = cKDTree(V).query_pairs(1e-5 * np.abs(V).max())
    drop = {j for i, j in pairs}
    return V[[k for k in range(len(V)) if k not in drop]]


def fvec_simple(V):
    V = V / np.linalg.norm(V, axis=1).max()
    h = ConvexHull(V)
    eq = np.round(h.equations, 6)
    _, fac = np.unique(eq, axis=0, return_inverse=True)
    fac = fac.ravel()
    F3 = fac.max() + 1
    inc = {}
    for s, f in zip(h.simplices, fac):
        for v in s:
            inc.setdefault(v, set()).add(f)
    if len(inc) != len(V):
        print('WARN hull vertices', len(inc), 'of', len(V), flush=True)
    deg = np.array([len(inc.get(v, ())) for v in range(len(V))])
    return len(V), int(F3), deg


def lin(a, b, c):  # linear 4-node diagram with branches a, b, c
    m = [[2] * 4 for _ in range(4)]
    m[0][1] = m[1][0] = a; m[1][2] = m[2][1] = b; m[2][3] = m[3][2] = c
    for i in range(4):
        m[i][i] = 1
    return m


fams = {'A4': lin(3, 3, 3), 'B4': lin(4, 3, 3), 'F4': lin(3, 4, 3), 'H4': lin(5, 3, 3)}
poly = []
rings = [r for r in itertools.product((0, 1), repeat=4) if any(r)]
for fam, m in fams.items():
    if PILOT and fam in ('H4',):
        rs = [(1, 0, 0, 0), (1, 1, 0, 0), (0, 1, 1, 0)]  # 120-cell, truncated 120-cell, bitruncated 600-cell
    elif PILOT:
        continue
    else:
        rs = rings
    for r in rs:
        V = wythoff(m, r)
        f0, F3, deg = fvec_simple(V)
        simple = bool((deg == 4).all())
        row = {'family': fam, 'rings': ''.join(map(str, r)), 'f0': f0, 'f3': F3, 'simple': simple,
               'corner_degree_max': int(deg.max())}
        if simple:
            row['h1'] = F3 - 4; row['h2'] = f0 - 2 * F3 + 6; row['h2_over_h1'] = row['h2'] / row['h1']
        poly.append(row)
        print('POLY', row, flush=True)
R['polytopes'] = poly
d = {(p['family'], p['rings']): p for p in poly}
check('120-cell (116,366)', d[('H4', '1000')].get('h1') == 116 and d[('H4', '1000')].get('h2') == 366)
check('truncated 120-cell (716,966)', d[('H4', '1100')].get('h1') == 716 and d[('H4', '1100')].get('h2') == 966)
check('bitruncated 600-cell (716,2166)', d[('H4', '0110')].get('h1') == 716 and d[('H4', '0110')].get('h2') == 2166)
if not PILOT:
    check('truncated 600-cell is NOT simple (rosette, #104 Lemma 5)', not d[('H4', '0011')]['simple'], d[('H4', '0011')]['corner_degree_max'])
    check('tesseract (4,6)', d[('B4', '1000')].get('h1') == 4 and d[('B4', '1000')].get('h2') == 6)
    check('5-cell (1,1)', d[('A4', '1000')].get('h1') == 1 and d[('A4', '1000')].get('h2') == 1)
print('PROGRESS 0.15 polytopes', flush=True); save()

# ---------------------------------------------------------------- (2) Poisson-Voronoi sweeps
def rand_dir(dim):
    u = rng.normal(size=dim); return u / np.linalg.norm(u)


def pv_sweep(dim, n, reps, ndir):
    rows = []
    for rep in range(reps):
        P = rng.random((n, dim))
        for k in range(ndir):
            u = rand_dir(dim)
            h, V = sweep_indices(P, u)
            rows.append({'n': n, 'V': V, 'h': h.tolist()})
    return rows


SW = {}
for dim, n, reps, ndir, pred, label in [(3, 2000 if PILOT else 200000, 2 if PILOT else 10, 2, 24 * np.pi ** 2 / 35 - 2, '24pi^2/35 - 2'),
                                         (4, 1000 if PILOT else 40000, 2 if PILOT else 8, 2, 286 / 9 - 2, '286/9 - 2')]:
    rows = pv_sweep(dim, n, reps, ndir)
    ok_id = True
    ratios = []
    for r in rows:
        h = r['h']; N = r['n']; V = r['V']
        if dim == 3:
            ok_id &= (h[0] == 0 and h[4] == 0 and h[1] == N and h[3] == N and h[2] == V - 2 * N)
            ratios.append(h[2] / h[1])
        else:
            ok_id &= (h[0] == 0 and h[5] == 0 and h[1] == N and h[4] == N and h[2] == h[3] == V // 2 - N and V % 2 == 0)
            ratios.append((h[2] + h[3]) / h[1])
    ratios = np.array(ratios)
    # per-sample ratio = V/N - 2 is the same for all directions of one sample -> error from samples
    per_sample = ratios.reshape(reps, ndir)[:, 0]
    mean, err = per_sample.mean(), per_sample.std(ddof=1) / np.sqrt(reps)
    SW[f'PV{dim}D'] = {'rows': rows, 'contact_changes_per_birth': mean, 'err': err, 'prediction': pred, 'prediction_formula': label}
    check(f'PV {dim}D sweep identities exact (births = deaths = cells, i=0 and i=d+1 absent' + (', i2 = i3' if dim == 4 else '') + ')', ok_id)
    check(f'PV {dim}D contact changes per birth {mean:.4f} +- {err:.4f} vs {label} = {pred:.4f}', abs(mean - pred) < 4 * err + (0.05 if PILOT else 0))
    print(f'PROGRESS {0.15 + 0.2 * (dim - 2):.2f} PV{dim}D sweep', flush=True); save()

# positive control with known exact value: perturbed bcc lattice (Voronoi cells = truncated octahedra, 14 faces) -> k/2 - 3 = 4
m = 6 if PILOT else 20
g = np.array(list(itertools.product(range(m), repeat=3)), float)
B = np.vstack([g, g + 0.5]) / m
B = (B + 1e-4 / m * rng.normal(size=B.shape)) % 1.0
hB, VB = sweep_indices(B, rand_dir(3), margin_cells=2.5)
check('control bcc (truncated octahedra) swaps per birth = 4 exactly', hB[2] == 4 * hB[1] and hB[1] == len(B), hB.tolist())
check('negative control: PV 3D value differs from the bcc value 4', abs(SW['PV3D']['contact_changes_per_birth'] - 4) > 0.5)
# perturbed fcc lattice: rhombic dodecahedra are NOT simple (degree-4 vertices at the 6 four-fold corners) -> perturbation splits them
F = np.vstack([g, g + [0.5, 0.5, 0], g + [0.5, 0, 0.5], g + [0, 0.5, 0.5]]) / m
F = (F + 1e-4 / m * rng.normal(size=F.shape)) % 1.0
hF, VF = sweep_indices(F, rand_dir(3), margin_cells=2.5)
SW['fcc_perturbed'] = {'h': hF.tolist(), 'V_per_cell': VF / len(F), 'swaps_per_birth': hF[2] / hF[1]}
print('fcc perturbed', SW['fcc_perturbed'], flush=True)
R['sweeps'] = SW
print('PROGRESS 0.6 controls', flush=True); save()

# ---------------------------------------------------------------- (3) random simple 4-polytopes: polar of random points on S^3
RP = []
for n in ([200, 1000] if PILOT else [100, 1000, 10000, 100000, 300000]):
    reps = 3 if PILOT else (20 if n <= 10000 else (4 if n <= 100000 else 2))
    vals = []
    for _ in range(reps):
        X = rng.normal(size=(n, 4)); X /= np.linalg.norm(X, axis=1)[:, None]
        T = len(ConvexHull(X).simplices)  # facets of the simplicial hull = corners of the simple polar
        h1, h2 = n - 4, T - 2 * n + 6
        vals.append(h2 / h1)
    vals = np.array(vals)
    RP.append({'cells': n, 'h2_over_h1': vals.mean(), 'err': vals.std(ddof=1) / np.sqrt(reps), 'reps': reps})
    print('RANDPOLY', RP[-1], flush=True)
R['random_simple_polytopes'] = RP
pv3 = 24 * np.pi ** 2 / 35 - 2
defi = np.array([pv3 - r['h2_over_h1'] for r in RP]); cells = np.array([r['cells'] for r in RP], float)
p_fit = -np.polyfit(np.log(cells[1:]), np.log(defi[1:]), 1)[0]
R['random_polytope_deficit_exponent'] = p_fit
check('random simple 4-polytopes: deficit from the PV value shrinks with every size step', bool(np.all(np.diff(defi) < 0)), defi.tolist())
check('random simple 4-polytopes: largest size within 0.03 of 24pi^2/35 - 2', abs(defi[-1]) < (0.3 if PILOT else 0.03), f'{RP[-1]} deficit exponent {p_fit:.3f}')
print('PROGRESS 0.75 random polytopes', flush=True); save()

# ---------------------------------------------------------------- (4) static tissue statistics
def pv2d_stats(n):
    P = rng.random((n, 2))
    X, orig, tri = periodic_delaunay(P)
    S = tri.simplices
    C = circumcentres(X, S)
    cell = S.ravel(); pts = np.repeat(C, 3, axis=0)
    keep = cell < n
    ids, area = polygon_area(cell[keep], pts[keep])
    nside = np.bincount(cell[keep], minlength=n)
    E = np.vstack([S[:, [0, 1]], S[:, [1, 2]], S[:, [0, 2]]])
    E = np.sort(orig[E], axis=1); E = np.unique(E, axis=0)
    st = tissue_stats(nside, E, area)
    st['area_sum'] = float(area.sum())
    return st


def sphere_stats(n):
    X = rng.normal(size=(n, 3)); X /= np.linalg.norm(X, axis=1)[:, None]
    S = ConvexHull(X).simplices
    nside = np.bincount(S.ravel(), minlength=n)
    E = np.unique(np.sort(np.vstack([S[:, [0, 1]], S[:, [1, 2]], S[:, [0, 2]]]), axis=1), axis=0)
    return tissue_stats(nside, E), nside.sum() / n


def section_stats(n):
    """Planar section z = 1/2 of the periodic 3D Poisson-Voronoi tessellation (a 2D power diagram)."""
    P = rng.random((n, 3))
    X, orig, tri = periodic_delaunay(P)
    S = tri.simplices
    C = circumcentres(X, S)
    z0 = 0.5
    # Voronoi edges dual to Delaunay triangles: pairs of adjacent tets
    nb = tri.neighbors
    a = np.repeat(np.arange(len(S)), 4); b = nb.ravel(); j = np.tile(np.arange(4), len(S))
    ok = (b > a)
    a, b, j = a[ok], b[ok], j[ok]
    za, zb = C[a, 2], C[b, 2]
    cross = (za - z0) * (zb - z0) < 0
    a, b, j = a[cross], b[cross], j[cross]
    t = (z0 - C[a, 2]) / (C[b, 2] - C[a, 2])
    Q = C[a, :2] + t[:, None] * (C[b, :2] - C[a, :2])
    inbox = np.all((Q >= 0) & (Q < 1), axis=1)
    # the triangle shared by tets a, b = tet a without vertex j: its three seeds are the three cells meeting at Q
    tri3 = np.array([np.delete(S[a_], j_) for a_, j_ in zip(a, j)])
    cells = orig[tri3]
    # polygon of each section cell: all crossing points of its edges (take points with Q in an enlarged box, cells counted once by original id
    # restricted to cells whose section polygon lies within the box via their centroid)
    cid = cells.ravel(); qp = np.repeat(Q, 3, axis=0)
    # use extended ids (X index) to avoid merging images
    xid = tri3.ravel()
    ids, area = polygon_area(xid, qp)
    nside = np.bincount(xid)[ids]
    sel = ids < n
    nside_o = np.zeros(n, int); nside_o[ids[sel]] = nside[sel]
    area_o = np.zeros(n); area_o[ids[sel]] = area[sel]
    present = nside_o > 0
    pr = np.vstack([cells[:, [0, 1]], cells[:, [1, 2]], cells[:, [0, 2]]])
    pr = np.unique(np.sort(pr, axis=1), axis=0)
    pr = pr[present[pr[:, 0]] & present[pr[:, 1]]]
    lab = -np.ones(n, int); lab[present] = np.arange(present.sum())
    st = tissue_stats(nside_o[present], lab[pr], area_o[present])
    st['area_sum'] = float(area[sel].sum())
    st['cells_per_unit_area_over_n23'] = float(sel.sum() / n ** (2 / 3))
    return st


ST = {}
st2 = pv2d_stats(20000 if PILOT else 2000000)
ST['PV2D_plane'] = st2
check('PV 2D plane mean sides = 6 exactly (torus Euler)', abs(st2['mean_n'] - 6) < 1e-9, st2['mean_n'])
check('PV 2D plane areas tile the torus', abs(st2['area_sum'] - 1) < 1e-6, st2['area_sum'])
check('PV 2D mu2 vs Hinde-Miles 1.781', abs(st2['mu2'] - 1.781) < (0.05 if PILOT else 0.01), st2['mu2'])
print('PV2D', {k: st2[k] for k in ('mean_n', 'mu2', 'aboav_a', 'lewis_slope')}, flush=True)
ns = 1000
sp, mean_sp = sphere_stats(ns)
ST['PV2D_sphere_1000'] = sp
check('PV on the sphere: mean sides = 6 - 12/N exactly', abs(mean_sp - (6 - 12 / ns)) < 1e-12, mean_sp)
print('PROGRESS 0.85 PV2D', flush=True); save()
sec = section_stats(20000 if PILOT else 1000000)
ST['PV3D_section'] = sec
check('section of PV 3D: mean sides = 6 (planar section of a normal tessellation)', abs(sec['mean_n'] - 6) < (0.05 if PILOT else 0.01), sec['mean_n'])
check('section areas tile the plane section', abs(sec['area_sum'] - 1) < 0.02, sec['area_sum'])
print('SECTION', {k: sec[k] for k in ('mean_n', 'mu2', 'aboav_a', 'lewis_slope')}, flush=True)
R['static'] = ST
R['wall_s'] = time.time() - t0
save()
nf = sum(not c[1] for c in CHECKS)
print(f'{len(CHECKS)} checks, {nf} failed', flush=True)
print('PROGRESS 1.0 done', flush=True)
print('FINAL ok' if nf == 0 else 'FINAL FAIL', flush=True)
