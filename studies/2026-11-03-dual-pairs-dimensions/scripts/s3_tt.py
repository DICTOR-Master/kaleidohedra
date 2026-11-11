"""Step 3: the self-dual pair T x (-T).
A. The tesseract's vertex-first sections are the same family (exact): the section of [-1,1]^4 by x1+x2+x3+x4 = s, 0 < s < 2,
   written in the rational orthonormal frame b1 = (1,1,-1,-1)/2, b2 = (1,-1,1,-1)/2, b3 = (1,-1,-1,1)/2, is similar to
   S(mu) = T cap mu(-T) with mu = (4 + s)/(4 - s) (proof: x_i <= 1 and x_i >= -1 become two opposite tetrahedra of sizes
   1 - s/4 and 1 + s/4). With h = s/2 (#89's height from the central octahedron to the 4-corner layer) the ratio
   corner side / remaining side of the hexagons is (1 - h)/h, so the golden cuts sit at h = 1/phi^2 (Greater) and 1/phi
   (Lesser) and the Archimedean truncated tetrahedron at h = 1/2: #89's heights. Checked exactly at those three heights.
B. Lattice selection (as the 6D study's part E): Z^3 + Z^3 with the diagonal T_d (rational, so the lattice exists), shadow
   of (m, n) on the flat y = x/mu is proportional to w = mu m + n. Section corners: T side (1/3 < ... ) pattern |w| = a(1, t, t),
   t = (mu - 1)/2 (1 < mu < 3); dual side |w| = a(1, s, s), s = (1 - mu)/(2 mu) (1/3 < mu < 1). Each condition is a
   polynomial of degree <= 2 in mu: either a sweep orbit or rational / quadratic mu. Search: all v in {-2..2}^6 up to the
   diagonal signed permutations.
usage (compute-host): python3 s3_tt.py -> ../data/s3-tt.json
"""
from dp_lib import *          # noqa
import sympy as sp
out = {}
P = Pair('tetrahedron', platonic()['tetrahedron'][0])
B = [tuple(K(Fr(a, 2)) for a in b) for b in ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))]
def tess_section(s):
    pts = []
    for p in itertools.permutations(range(4)):
        base = (ONE, ONE, -ONE, s - 1)
        x = tuple(base[p[i]] for i in range(4)); pts.append(tuple(dot(b, x) for b in B))
    return uniq(pts)
rows = []
for h, lab in ((PHI.inv() * PHI.inv(), 'Greater Golden Cut Tetrahedron'), (K(Fr(1, 2)), 'truncated tetrahedron'), (PHI.inv(), 'Lesser Golden Cut Tetrahedron')):
    s = 2 * h; mu = (4 + s) / (4 - s)
    Sx = P.S(mu); T4 = tess_section(s)
    ok = similar(T4, Sx)[0]
    x = (3 - mu) / 4
    ok2 = (x / (1 - 2 * x)) == (1 - h) / h
    check(f'A: tesseract section at height h = {kstr(h)} (s = {kstr(s)}) = S(mu), mu = (4+s)/(4-s) = {kstr(mu)}: the {lab} ({len(T4)} corners); ratio (1-h)/h', ok and ok2)
    rows.append({'h': kstr(h), 's': kstr(s), 'mu': kdesc(mu), 'stage': lab})
out['tesseract_heights'] = rows
check('A: the Mobius map h -> mu = (2 + h)/(2 - h) sends h = 0, 1/2, 1 to the octahedron (1), Archimedean (5/3), tetrahedron (3)',
      (2 + K(0)) / (2 - K(0)) == ONE and (2 + K(Fr(1, 2))) / (2 - K(Fr(1, 2))) == K(Fr(5, 3)) and K(3) == (2 + ONE) / (2 - ONE))

# B. lattice selection
m = sp.Symbol('mu', positive=True)
def conditions(v):
    w = [sp.Integer(v[k]) * m + v[k + 3] for k in range(3)]
    found = set(); sweep = set()
    for i, j, k in itertools.permutations(range(3)):
        if j > k: continue
        for sj, sk in itertools.product((1, -1), repeat=2):
            for side, eqs, lo, hi in (('T', [2 * w[j] - sj * (m - 1) * w[i], 2 * w[k] - sk * (m - 1) * w[i]], 1, 3),
                                      ('dual', [2 * m * w[j] - sj * (1 - m) * w[i], 2 * m * w[k] - sk * (1 - m) * w[i]], sp.Rational(1, 3), 1)):
                eqs = [sp.expand(e) for e in eqs]
                if all(e == 0 for e in eqs): sweep.add(side); continue
                nz = [e for e in eqs if e != 0]; g = nz[0]
                for e in nz[1:]: g = sp.gcd(g, e)
                if sp.degree(g, m) < 1: continue
                for r in sp.Poly(g, m).all_roots():
                    if not r.is_real: continue
                    rf = float(r)
                    if not (float(lo) + 1e-12 < rf < float(hi) - 1e-12): continue
                    a = sorted([abs(float(x.subs(m, r))) for x in w], reverse=True)
                    t = (rf - 1) / 2 if side == 'T' else (1 - rf) / (2 * rf)
                    if a[0] > 1e-12 and all(abs(a[q] / a[0] - [1, t, t][q]) < 1e-9 for q in range(3)):
                        found.add((side, sp.nsimplify(r) if r.is_rational else sp.simplify(r)))
    return sweep, found
reps = {}
for v in itertools.product(range(-2, 3), repeat=6):
    if not any(v): continue
    pairs = [(v[k], v[k + 3]) for k in range(3)]
    pairs = [p if (p[0] > 0 or (p[0] == 0 and p[1] >= 0)) else (-p[0], -p[1]) for p in pairs]
    reps.setdefault(tuple(sorted(pairs)), v)
print(f'   {len(reps)} orbit representatives', flush=True)
sel = {}; sweeps = []
for c, v in reps.items():
    sw, fd = conditions(v); nrm = sum(x * x for x in v)
    if sw: sweeps.append({'v': v, 'norm': nrm, 'sides': sorted(sw)})
    for side, r in fd:
        k = (side, str(r))
        if k not in sel or sel[k]['norm'] > nrm:
            sel[k] = {'side': side, 'mu': str(r), 'mu_float': float(r),
                      'degree': int(sp.degree(sp.minimal_polynomial(r, sp.Symbol('z')))), 'v': v, 'norm': nrm}
out['selected_mu'] = sorted(sel.values(), key=lambda d: d['mu_float'])
out['sweep_orbits_min'] = sorted(sweeps, key=lambda d: d['norm'])[:6]
for d in out['selected_mu']: print('   ', d, flush=True)
check(f'B: {len(sel)} isolated mu, all of degree <= 2', all(d['degree'] <= 2 for d in sel.values()))
targets = {'Greater GCT (T side) 2sqrt5 - 3': 2 * 5 ** .5 - 3, 'Lesser GCT (T side) 1 + 2/sqrt5': 1 + 2 / 5 ** .5,
           'Greater GCT (dual side)': 1 / (2 * 5 ** .5 - 3), 'Lesser GCT (dual side) 5 - 2sqrt5': 5 - 2 * 5 ** .5,
           'truncated tetrahedron 5/3': 5 / 3, 'truncated tetrahedron (dual) 3/5': 3 / 5}
hits = {}
for lab, f in targets.items():
    if f > 3 or f < 1 / 3: hits[lab] = 'outside'; continue
    d = [x for x in sel.values() if abs(x['mu_float'] - f) < 1e-9]
    hits[lab] = min((x['norm'] for x in d), default=None)
out['target_min_norm_in_box'] = hits
print('   targets:', hits, flush=True)
check(f'B: smallest selecting norms in the box recorded for the golden and Archimedean stages: {hits}', True)
check(f'B: sweep orbits exist? {bool(sweeps)} (smallest norm {min((s["norm"] for s in sweeps), default=None)})', True)

# C. exact: for a target mu in Q(sqrt5) the vectors v whose shadow is the corner (1, t, t) pattern (w1 = t w0, w2 = t w0)
#    form a rank-2 lattice containing the sweep vector s0 = (0,1,1 | 2,-1,-1); the shortest vector NOT parallel to s0 is the
#    shortest "isolated" selector (exact 2D reduction).
r = sp.Symbol('r'); ms = sp.symbols('m0:3'); ns = sp.symbols('n0:3')
def lattice_selector(mu_expr, side, B=6):
    """shortest v in {-B..B}^6 whose shadow w = mu m + n has the corner pattern (w1 = t w0, w2 = t w0, w0 != 0) and is
    not parallel to the side's sweep vector; float search, every hit re-verified exactly (sympy)"""
    import numpy as np
    s0 = np.array((0, 1, 1, 2, -1, -1) if side == 'T' else (-2, 1, 1, 0, -1, -1))
    mu = float(mu_expr.subs(r, sp.sqrt(5))); t = (mu - 1) / 2 if side == 'T' else (1 - mu) / (2 * mu)
    rng = np.arange(-B, B + 1)
    g = np.stack(np.meshgrid(*([rng] * 6), indexing='ij'), -1).reshape(-1, 6)
    w = mu * g[:, :3] + g[:, 3:]
    ok = (np.abs(w[:, 1] - t * w[:, 0]) < 1e-9) & (np.abs(w[:, 2] - t * w[:, 0]) < 1e-9) & (np.abs(w[:, 0]) > 1e-9)
    G = g[ok]
    par = np.all(np.abs(np.cross(G[:, :3], s0[:3])) == 0, 1) & np.all(np.abs(np.cross(G[:, 3:], s0[3:])) == 0, 1) & \
          (G[:, :3] @ s0[3:] == G[:, 3:] @ s0[:3]) if len(G) else np.zeros(0, bool)
    # parallel test exactly: v = c s0
    par = np.array([np.linalg.matrix_rank(np.stack([v, s0])) == 1 for v in G], bool) if len(G) else par
    G = G[~par]
    if not len(G): return None
    nr = (G * G).sum(1); v = tuple(int(x) for x in G[np.argmin(nr)])
    me = mu_expr.subs(r, sp.sqrt(5)); te = (me - 1) / 2 if side == 'T' else (1 - me) / (2 * me)
    we = [me * v[k] + v[k + 3] for k in range(3)]
    assert sp.simplify(we[1] - te * we[0]) == 0 and sp.simplify(we[2] - te * we[0]) == 0
    return (int(nr.min()), v)
mus = {'Greater GCT (T side)': (-3 + 2 * r, 'T'), 'Lesser GCT (T side)': (1 + 2 * r / 5, 'T'),
       'Lesser GCT (dual side)': (5 - 2 * r, 'dual'), 'Greater GCT (dual side)': (sp.Rational(3, 11) + sp.Rational(2, 11) * r, 'dual')}
sl = {}
for lab, (mu_, side) in mus.items():
    res = lattice_selector(mu_, side); sl[lab] = res; print('   C:', lab, res, flush=True)
out['shortest_isolated_selector'] = {k: (None if v is None else {'norm': v[0], 'v': v[1]}) for k, v in sl.items()}
wT = [0 * m + 2, m - 1, m - 1]; wD = [-2 * m, m - 1, m - 1]
check('C: sweep vectors (0,1,1 | 2,-1,-1) and (-2,1,1 | 0,-1,-1) (norm 8) cast the corners of T cap mu(-T) at every mu on the T side and the dual side (identically)',
      sp.simplify(2 * wT[1] - (m - 1) * wT[0]) == 0 and sp.simplify(2 * m * wD[1] - (1 - m) * wD[0]) == 0)
check(f'C: shortest isolated selectors of the golden cut tetrahedra have norm {[ (v[0] if v else None) for k, v in sl.items() if "GCT" in k]}, '
      f'against 3 (mu = 2), 4 (sqrt3, 1 + sqrt2), 6 (phi) and 11 (Archimedean 5/3)',
      all(v is not None and v[0] > 11 for k, v in sl.items() if 'GCT' in k))
save('s3-tt.json', out)
