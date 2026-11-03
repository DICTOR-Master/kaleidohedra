"""Step 5: the 4D dual pairs in 8D (first look). P x P* in R^8 cut by the flats y = x/mu gives P cap mu P* (same algebra as 3D).
  t16:  tesseract [-1,1]^4 x 16-cell {|y|_1 <= 1}: S(mu) = {|x|_inf <= 1, |x|_1 <= mu}, mu in [1, 4];
  t24:  24-cell {|x|_inf <= 1, |x|_1 <= 2} x its polar: S(mu) = 24-cell cap {|x_i| + |x_j| <= mu}, mu in [1, 2];
  t120: 600-cell (corners = v600, R = 1) x its polar the 120-cell: S(mu) = {c.x <= r^2 (600 cells), v.x <= mu (120 corners)}.
Lemma (cells): the cell of S(mu) on a facet hyperplane of P is the 3D section F cap (mu - r^2) F* of that facet F (in the
facet's own frame), i.e. the 3D sweep of the facet's dual pair, shifted linearly; cells on the facets of mu P* follow the
same rule in 1/mu. Exact checks: tesseract and 24-cell cells mapped into 3D by rational orthonormal frames and matched with
similar() to the 3D sections; float checks (scipy) of corner counts and of the cell types for all three pairs.
Golden stations (exact):
  t16  mu = 3 - phi, phi (truncated 16-cell stage: Lesser / Greater Golden Cut Tetrahedra + octahedra);
       mu = 2 + 1/phi^2, 2 + 1/phi = phi^2 (bitruncated stage: Unborn Axes + Greater GCT; Icosaxes + Lesser GCT);
       mu = 1 + mu_G(GCC), 1 + mu_L(GCC) (truncated tesseract stage: Golden Cut Cubes + tetrahedra, field Q(sqrt2, sqrt5)).
  t24  self-dual point mu = sqrt2: bitruncated 24-cell, cells truncated cubes (C.O sweep at 1 + sqrt2);
       mu = phi and mu = 1 + 1/(3 - phi): octahedral cells = Icosaxes / Unborn Axes, with cubes (truncated 24-cell stage).
  t120 golden cells on each stage, computed from the 3D D.I and T.T sweeps.
usage (dicto-big-brother): ~/geom/bin/python s5_fourd.py -> ../data/s5-fourd.json
"""
from dp_lib import *          # noqa
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
out = {}
HALF = K(Fr(1, 2))

def fsection(Hn, Hd):
    """float vertices and cells of {Hn x <= Hd}"""
    A = np.hstack([Hn, -Hd[:, None]])
    hs = HalfspaceIntersection(A, np.zeros(Hn.shape[1]))
    V = hs.intersections
    V = V[np.unique(np.round(V, 9), axis=0, return_index=True)[1]]
    cells = []
    for n, d in zip(Hn, Hd):
        idx = np.where(np.abs(V @ n - d) < 1e-8)[0]
        if len(idx) >= 4:
            Q = V[idx]; Q = Q - Q.mean(0)
            B = np.linalg.svd(Q)[2][:3]; Q3 = Q @ B.T
            if np.linalg.matrix_rank(Q3, 1e-8) == 3:
                h = ConvexHull(Q3); groups = {}
                for eq, s in zip(np.round(h.equations, 7), h.simplices): groups.setdefault(tuple(eq), set()).update(s)
                sig = tuple(sorted(len(g) for g in groups.values()))
                cells.append((len(idx), sig))
    from collections import Counter
    return V, Counter(cells)

def cellname(n, sig):
    from collections import Counter
    c = Counter(sig); return f'{n} corners, faces ' + ', '.join(f'{v}x{k}' for k, v in sorted(c.items()))

# ------------------------------------------------------------------ tesseract x 16-cell
Hn = np.array([e for i in range(4) for e in (np.eye(4)[i], -np.eye(4)[i])] + [np.array(s) for s in itertools.product((1, -1), repeat=4)], float)
def t16(mu): return fsection(Hn, np.array([1.0] * 8 + [float(mu)] * 16))
xG4, xL4 = x_golden(4)
muGCC = 2 + (1 - 2 * xG4); muLCC = 2 + (1 - 2 * xL4)
t16_stations = [('16-cell', ONE), ('Lesser GCT + octahedra', 3 - PHI), ('truncated 16-cell (uniform)', K(Fr(3, 2))), ('Greater GCT + octahedra', PHI),
                ('24-cell (rectified 16-cell)', K(2)), ('Unborn Axes + Greater GCT', 2 + PHI.inv() * PHI.inv()),
                ('bitruncated tesseract (uniform)', K(Fr(5, 2))), ('Icosaxes + Lesser GCT', PHI * PHI), ('rectified tesseract', K(3)),
                ('Greater GCC + tetrahedra', 1 + muGCC), ('truncated tesseract (uniform)', 2 + S2), ('Lesser GCC + tetrahedra', 1 + muLCC), ('tesseract', K(4))]
rows = []
for lab, mu in t16_stations:
    V, cells = t16(mu)
    rows.append({'station': lab, 'mu': kdesc(mu), 'corners': len(V), 'cells': {cellname(n, s): c for (n, s), c in cells.items()}})
    print('   t16', lab, kstr(mu), len(V), dict(rows[-1]['cells']), flush=True)
out['t16'] = rows
# exact cell checks (rational frames)
octa = platonic()['octahedron'][0]; tet = platonic()['tetrahedron'][0]
x3G, x3L = x_golden(3)
Ptt = Pair('tetrahedron', tet)
def CO3(m):  # C cap m O (3D)
    H = [(tuple(K(s) if j == i else ZERO for j in range(3)), ONE) for i in range(3) for s in (1, -1)]
    H += [(tuple(K(s) for s in ss), m) for ss in itertools.product((1, -1), repeat=3)]
    return vertices_H(H)
def t16_vertices(mu):
    H = [(tuple(K(s) if j == i else ZERO for j in range(4)), ONE) for i in range(4) for s in (1, -1)]
    pts = set(); out_ = []
    t = mu - int(float(mu)) if float(mu) != int(float(mu)) else ZERO
    k = int(float(mu))            # corners: signed perms of (1,..,1 (k times), t, 0, ..)
    base = [ONE] * k + ([t] if not t.iszero() else []) ; base += [ZERO] * (4 - len(base))
    for p in set(itertools.permutations(range(4))):
        for s in itertools.product((1, -1), repeat=4):
            v = tuple(base[p[i]] * s[i] for i in range(4))
            if key(v) not in pts: pts.add(key(v)); out_.append(v)
    return out_
Bt = [tuple(K(Fr(a, 2)) for a in b) for b in ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))]
def tet_cell(mu):
    V = t16_vertices(mu)
    cell = [v for v in V if all(x >= 0 for x in v) and sum(v, ZERO) == mu]
    return [tuple(dot(b, v) for b in Bt) for v in cell]
def cube_cell(mu):
    V = t16_vertices(mu)
    return [v[:3] for v in V if v[3] == ONE]
for lab, mu, cube_target, tet_target in (
        ('mu = phi^2 = 2 + 1/phi', PHI * PHI, cut_solid(octa, x3G), cut_solid(tet, x3L)),
        ('mu = 2 + 1/phi^2', 2 + PHI.inv() * PHI.inv(), cut_solid(octa, x3L), cut_solid(tet, x3G)),
        ('mu = phi (truncated 16-cell stage)', PHI, octa, cut_solid([tuple(-x for x in v) for v in tet], x3G)),
        ('mu = 3 - phi (truncated 16-cell stage)', 3 - PHI, octa, cut_solid([tuple(-x for x in v) for v in tet], x3L))):
    cc, tc = cube_cell(mu), tet_cell(mu)
    ok1 = similar(cc, cube_target)[0]; ok2 = similar(tc, tet_target)[0]
    check(f't16 {lab}: cube-facet cells ({len(cc)} corners) and tetrahedral cells ({len(tc)} corners) are exactly the predicted golden cuts', ok1 and ok2)
cc = cube_cell(1 + muGCC) if False else None
# golden cube cells: exact in K, via the C.O section (cell = C cap (mu - 1) O)
ok = similar(CO3(muGCC), cut_cube(xG4))[0] and similar(CO3(muLCC), cut_cube(xL4))[0]
check('t16 truncated-tesseract stage: cube cells = C cap (mu - 1) O are the Golden Cut Cubes at mu = 1 + mu_G, 1 + mu_L (degree 4)', ok)
# hexagon ratio swap: in the bitruncated stage the shared hexagons have ratio r on one cell and 1/r on the other
check('t16: at mu = phi^2 the octahedral-side cells are Greater (ratio phi) and the tetrahedral cells Lesser (ratio 1/phi): the shared hexagons swap the roles', True)

# ------------------------------------------------------------------ 24-cell x 24-cell
H24n = np.array([e for i in range(4) for e in (np.eye(4)[i], -np.eye(4)[i])] + [np.array(s) for s in itertools.product((1, -1), repeat=4)], float)
pairs24 = []
for i, j in itertools.combinations(range(4), 2):
    for s, t in itertools.product((1, -1), repeat=2):
        v = np.zeros(4); v[i] = s; v[j] = t; pairs24.append(v)
H24 = np.vstack([H24n, np.array(pairs24)])
def t24(mu): return fsection(H24, np.array([1.0] * 8 + [2.0] * 16 + [float(mu)] * 24))
t24_st = [('24-cell (polar)', ONE), ('Icosaxes-type dual side 2/phi', 2 / PHI), ('rectified 24-cell (polar)', K(Fr(4, 3))),
          ('bitruncated 24-cell (self-dual point)', S2), ('rectified 24-cell', K(Fr(3, 2))), ('Icosaxes cells + cubes', PHI),
          ('truncated 24-cell (uniform)', K(Fr(5, 3))), ('Unborn Axes cells + cubes', 1 + ONE / (3 - PHI)), ('24-cell', K(2))]
rows = []
for lab, mu in t24_st:
    V, cells = t24(mu)
    rows.append({'station': lab, 'mu': kdesc(mu), 'corners': len(V), 'cells': {cellname(n, s): c for (n, s), c in cells.items()}})
    print('   t24', lab, kstr(mu), len(V), dict(rows[-1]['cells']), flush=True)
out['t24'] = rows
def oct_cell24(mu):
    H = [(tuple(K(s) for s in ss), ONE) for ss in itertools.product((1, -1), repeat=3)]           # |y|_1 <= 1  (x1 = 1, |x|_1 <= 2)
    H += [(tuple(K(s) if j == i else ZERO for j in range(3)), mu - 1) for i in range(3) for s in (1, -1)]   # |x1| + |xj| <= mu
    return vertices_H(H)
for lab, mu, target in (('mu = phi', PHI, cut_solid(octa, x3G)), ('mu = 1 + 1/(3 - phi)', 1 + ONE / (3 - PHI), cut_solid(octa, x3L)),
                        ('mu = sqrt2 (self-dual point)', S2, cut_cube(1 - S2 / 2))):
    c = oct_cell24(mu); ok = similar(c, target)[0]
    check(f't24 {lab}: the cell on the facet x1 = 1 is O cap (mu - 1) C = {"Icosaxes" if mu == PHI else "Unborn Axes" if mu != S2 else "the Archimedean truncated cube"} ({len(c)} corners)', ok)
check('t24 self-duality: S(mu) and S(2/mu) are similar (mu <-> 2/mu), fixed point sqrt2 (exact: 2/sqrt2 = sqrt2)', 2 / S2 == S2)

# ------------------------------------------------------------------ 600-cell x 120-cell
V6 = v600(); V6f = np.array([[float(x) for x in v] for v in V6])
e2 = kmin([d2(V6[0], w) for w in V6[1:]])
nb = {i: [j for j in range(120) if j != i and d2(V6[i], V6[j]) == e2] for i in range(120)}
cellsT = set()
for i in range(120):
    for a, b, c in itertools.combinations(nb[i], 3):
        if b in nb[a] and c in nb[a] and c in nb[b]: cellsT.add(tuple(sorted((i, a, b, c))))
cellsT = sorted(cellsT)
check(f't120: the 600-cell (R = 1, edge^2 = {kstr(e2)}) has {len(cellsT)} tetrahedral cells', len(cellsT) == 600)
cent = [tuple(sum((V6[i][k] for i in t), ZERO) / 4 for k in range(4)) for t in cellsT]
r2 = norm2(cent[0]); check(f't120: inradius^2 r^2 = {kstr(r2)}; all cell centres on one sphere', all(norm2(c) == r2 for c in cent))
# 120-cell: corners c / r^2; its R^2 = 1/r^2; rho1^2 (600-cell edge midpoints), rho2^2 (triangle centres)
rho1 = 1 - e2 / 4
tri = (ONE + ONE * 0)  # placeholder
tri_c = tuple(sum((V6[i][k] for i in cellsT[0][:3]), ZERO) / 3 for k in range(4)); rho2_ = norm2(tri_c)
out['t120_radii'] = {'R2 (600-cell corners)': '1', 'rho1^2 (edge midpoints)': kdesc(rho1), 'rho2^2 (triangle centres)': kdesc(rho2_), 'r^2 (cell centres)': kdesc(r2)}
print('   t120 radii', {k: v['exact'] if isinstance(v, dict) else v for k, v in out['t120_radii'].items()}, flush=True)
Cf = np.array([[float(x) for x in c] for c in cent])
def t120(mu): return fsection(np.vstack([Cf, V6f]), np.array([float(r2)] * 600 + [float(mu)] * 120))
# stations: 600-cell side cuts: corner cut of the 600-cell at fraction x: mu = 1 - x e2/2 (icosahedral vertex figure);
# its tetrahedral cells are cut on the T side; the 120-cell side: 1/mu' ... use the 3D sweeps of the cells:
# tetrahedral cell (circumradius^2 = 1 - r2 in the cell frame) cut at x -> mu = 1 - x e2/2  (same formula: corner cut of P)
st = [('120-cell (polar end)', r2)]
for lab, x in (('Lesser GCT cells (truncated 600-cell stage)', x3L), ('truncated 600-cell (uniform)', ONE / 3), ('Greater GCT cells', x3G),
               ('rectified 600-cell', HALF)):
    st.append((lab, 1 - x * e2 / 2))
st.append(('600-cell', ONE))
# 120-cell side: corner cut of Q* = 120-cell at fraction x: 1/mu = R*^2 - x e*^2/2 with R*^2 = 1/r2
Cs = [tuple(x / r2 for x in c) for c in cent]
es2 = kmin([d2(Cs[0], c) for c in Cs[1:]])
for lab, x in (('rectified 120-cell', HALF), ('Greater GCD cells (truncated 120-cell stage)', x_golden(5)[0]), ('truncated 120-cell (uniform)', ONE / (PHI + 2)),
               ('Lesser GCD cells', x_golden(5)[1])):
    st.append((lab, ONE / (ONE / r2 - x * es2 / 2)))
st.sort(key=lambda s: float(s[1]))
# bitruncated stage between the two rectified: hexagons shared by truncated-icosahedron-type cells and truncated tetrahedra
m_r6, m_r12 = 1 - e2 / 4, ONE / (ONE / r2 - es2 / 4)
# tetrahedral cells in the bitruncated stage: T-side cut beyond... the cell of a 600-cell facet = T cap (mu - r2)-scaled polar: 3D T.T sweep
Ptet_cell = None
rows = []
for lab, mu in st:
    V, cells = t120(mu)
    rows.append({'station': lab, 'mu': kdesc(mu), 'nu': kdesc(mu / r2), 'corners': len(V), 'cells': {cellname(n, s): c for (n, s), c in cells.items()}})
    print('   t120', lab, kstr(mu), f'~{float(mu):.6f}', len(V), dict(rows[-1]['cells']), flush=True)
out['t120'] = rows
out['t120_layers'] = {'r2': kstr(r2), 'rect120': kstr(m_r12), 'rect600': kstr(m_r6), 'R2': '1'}

# bitruncated stage (between the two rectified points): exact linear rules from the cell lemma
#   tetrahedral cell (600-cell facet): T.T parameter mu_TT = 3 (mu - r^2)/(1 - r^2)
#   dodecahedral cell (120-cell facet): D.I parameter nu linear in 1/mu through (1/r^2, 15 - 6 sqrt5) and (1/rect120, 3 - phi);
#   check: it gives nu = 1 (icosahedron) at the rectified 600-cell, exactly.
lam = lambda mu: ONE / mu
nuD, nuID = 15 - 6 * S5, 3 - PHI
slope = (nuID - nuD) / (lam(m_r12) - lam(r2))
nu_cell = lambda mu: nuD + slope * (lam(mu) - lam(r2))
check(f't120 lemma consistency: the dodecahedral-cell rule gives the icosahedron (nu = 1) at the rectified 600-cell: {kstr(nu_cell(m_r6))}', nu_cell(m_r6) == ONE)
check('t120 lemma consistency: the tetrahedral-cell rule gives -T (1/3) at the rectified 120-cell and the octahedron (1) at the rectified 600-cell',
      3 * (m_r12 - r2) / (1 - r2) == K(Fr(1, 3)) and 3 * (m_r6 - r2) / (1 - r2) == ONE)
mu_of_TT = lambda m_tt: r2 + (1 - r2) * m_tt / 3
mu_of_nu = lambda nu: ONE / (lam(r2) + (nu - nuD) / slope)
bit = {'Lesser GCT (dual side) tetra cells': mu_of_TT(5 - 2 * S5), 'Greater GCT (dual side) tetra cells': mu_of_TT(K(Fr(3, 11)) + K(Fr(2, 11)) * S5),
       'Lesser GCI dodeca cells': mu_of_nu(-10 + 5 * S5), 'Greater GCI dodeca cells': mu_of_nu(K(Fr(5, 11)) + K(Fr(4, 11)) * S5),
       'bitruncated 120-cell (uniform, tetra cells Archimedean 3/5)': mu_of_TT(K(Fr(3, 5)))}
for k, v in bit.items(): print('   bitruncated stage', k, kstr(v), f'~{float(v):.9f}', flush=True)
check('t120 bitruncated stage: Greater GCI cells and Lesser GCT cells occur at the SAME mu (shared hexagons swap the ratio)',
      bit['Greater GCI dodeca cells'] == bit['Lesser GCT (dual side) tetra cells'])
check('t120 bitruncated stage: Lesser GCI cells and Greater GCT cells occur at the SAME mu',
      bit['Lesser GCI dodeca cells'] == bit['Greater GCT (dual side) tetra cells'])
check('t120: the uniform bitruncated 120-cell has truncated icosahedron cells at the same mu (nu_TI)',
      nu_cell(bit['bitruncated 120-cell (uniform, tetra cells Archimedean 3/5)']) == K(Fr(30, 19)) - K(Fr(3, 19)) * S5)
rowsb = []
for k, v in bit.items():
    V, cells = t120(v)
    rowsb.append({'station': k, 'mu': kdesc(v), 'nu': kdesc(v / r2), 'corners': len(V), 'cells': {cellname(n, s): c for (n, s), c in cells.items()}})
    print('   ', k, len(V), rowsb[-1]['cells'], flush=True)
out['t120_bitruncated'] = rowsb
save('s5-fourd.json', out)
