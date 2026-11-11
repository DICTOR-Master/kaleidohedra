"""Step 3: six dimensions. Exact in K = Q(sqrt2, sqrt5) unless marked.
A. Face directions. A truncated cube has 14 faces in 7 parallel pairs (3 octagon pairs + 4 triangle pairs), checked
   exactly on both Golden Cut Cubes. A section of the 6-cube {|y_i| <= 1} by any 3-flat x -> y = Lx + b is
   {x : |l_i.x + b_i| <= 1}: at most 6 face directions. So no section of the 6-cube, or tile of a section of its honeycomb,
   is a truncated cube (any depth), in any embedding. Projections of the 6-cube are zonotopes (all faces centrally
   symmetric), and a truncated cube has triangles. (Proofs; the script checks the 7 directions.)
B. Cube x cube. R^6 = R^3 + R^3 with the diagonal cube group (g, g). The flats carrying the vector representation are
   F_mu = {(x, x/mu)}. Graph sections of C x C (C = [-1,1]^3) are C cap A^-1 C: at most 6 directions (part A).
   Example A = 5-fold icosahedral rotation (entries in Q(sqrt5)): C cap A^-1 C, exact faces and cube symmetries.
C. Cube x octahedron C x C* (C* = {|y|_1 <= 1}, the dual octahedron), a 6D polytope with symmetry B3 x B3.
   Its section by F_mu is C cap mu C* = {|x|_inf <= 1, |x|_1 <= mu}: octahedron (mu = 1), corner-cut octahedra
   (1 < mu < 2), cuboctahedron (2), corner-cut cubes (2 < mu < 3), cube (3). Exact sections at the named mu and
   matches: Unborn Axes (mu = 3 - phi), Icosaxes (phi), Lesser/Greater Golden Cut Cube (mu_L, mu_G), Archimedean
   truncated octahedron (3/2), truncated cube (1 + sqrt2), and the cut cubes at the golden heights 2 + 1/phi^2, 2 + 1/phi.
D. Shadows of Z^6 on F_mu: (m, n) -> m + n/mu (up to the factor 1/(1 + 1/mu^2)). D6 roots: orbits under the diagonal
   group; the 24 mixed roots e_a + -f_b (a != b) cast (1, +-1/mu, 0) and its images. Section corners = shadows exactly
   when mu - 1 = 1/mu, i.e. mu = phi: Icosaxes.
E. Selection by lattice orbits (exact, sympy): every v in {-2..2}^6 (up to the diagonal group); find all mu in (1, 3),
   mu != 2, at which the shadow orbit of v equals (up to scale) the corner set of C cap mu C*. Each condition is a
   polynomial of degree <= 2 in mu with integer coefficients, so it holds identically ("sweep orbit") or at rational or
   quadratic mu only. Expected: mu_G, mu_L (degree 4) never isolated.
F. Golden heights in mu between the layers octahedron (1), cuboctahedron (2), cube (3), and mu_G, mu_L written as
   golden heights a + (b - a)/phi^2 with a, b in Q(sqrt2) (unique).
usage (compute-host): python3 s3_six_d.py -> ../data/s3-six-d.json
"""
from sixd_lib import *          # noqa
from collections import Counter
import sympy as sp

out = {}
xG, xL = x_golden(4)
GCC = {'Greater': cut_cube(xG), 'Lesser': cut_cube(xL)}

# ---------------------------------------------------------------- A. seven face directions
def face_lines(P):
    V, F = hull3(P)
    lines = set()
    for f in F:
        a, b, c = V[f[0]], V[f[1]], V[f[2]]
        n = (( b[1]-a[1])*(c[2]-a[2]) - (b[2]-a[2])*(c[1]-a[1]), (b[2]-a[2])*(c[0]-a[0]) - (b[0]-a[0])*(c[2]-a[2]),
             (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
        k = next(i for i in range(3) if not n[i].iszero()); n = tuple(x / n[k] for x in n)   # projective normal
        lines.add(key(n))
    return V, F, lines
for lab, P in GCC.items():
    V, F, L = face_lines(P)
    check(f'{lab} Golden Cut Cube: {len(F)} faces {signature(F)} in {len(L)} directions (3 octagon + 4 triangle pairs) > 6',
          len(F) == 14 and signature(F) == {3: 8, 8: 6} and len(L) == 7)
out['face_directions'] = 7

# ---------------------------------------------------------------- B. cube x cube graph sections
h = Fr(1, 2)
A5 = [[K(h), -PHI * h, PHI.inv() * h], [PHI * h, PHI.inv() * h, K(-h)], [PHI.inv() * h, K(h), PHI * h]]
AT = [[A5[j][i] for j in range(3)] for i in range(3)]
I3 = [[sum((A5[i][k] * AT[k][j] for k in range(3)), ZERO) for j in range(3)] for i in range(3)]
def mul(X, Y): return [[sum((X[i][k] * Y[k][j] for k in range(3)), ZERO) for j in range(3)] for i in range(3)]
Pw = A5
for _ in range(4): Pw = mul(Pw, A5)
check('A (icosahedral 5-fold rotation) is orthogonal, det 1, A^5 = I, entries in Q(sqrt5)',
      all(I3[i][j] == (ONE if i == j else ZERO) for i in range(3) for j in range(3)) and det3(*A5) == 1
      and all(Pw[i][j] == (ONE if i == j else ZERO) for i in range(3) for j in range(3)))
Hc = [(tuple(K(s) if j == i else ZERO for j in range(3)), ONE) for i in range(3) for s in (1, -1)]
Ha = [(tuple(A5[i][j] * s for j in range(3)), ONE) for i in range(3) for s in (1, -1)]   # |(A x)_i| <= 1
Vx = vertices_H(Hc + Ha)
V, F, L = face_lines(Vx)
sym = sum(1 for g in signed_perms(3) if {key(act(g, v)) for v in V} == {key(v) for v in V})
check(f'C cap A^-1 C (two cubes of the compound of five): {len(V)} corners, faces {signature(F)}, {len(L)} directions '
      f'(<= 6), {sym} of the 48 cube symmetries', len(L) <= 6 and sym < 48)
out['cube_x_cube_example'] = {'corners': len(V), 'faces': signature(F), 'directions': len(L), 'cube_symmetries_kept': sym}

# ---------------------------------------------------------------- C. sections of cube x octahedron
def CO(mu):
    H = [(tuple(K(s) if j == i else ZERO for j in range(3)), ONE) for i in range(3) for s in (1, -1)]
    H += [(tuple(K(s) for s in ss), mu) for ss in itertools.product((1, -1), repeat=3)]
    return vertices_H(H)
def muc(t): return 2 + t          # cube side: corners (1, 1, t) <-> mu = 2 + t
tG, tL = 1 - 2 * xG, 1 - 2 * xL
muG, muL = muc(tG), muc(tL)
octa = platonic()['octahedron'][0]
x3G, x3L = x_golden(3)
named = [('octahedron', ONE, octa), ('Unborn Axes', 3 - PHI, cut_solid(octa, x3L)),
         ('truncated octahedron (Archimedean)', K(Fr(3, 2)), cut_solid(octa, K(Fr(1, 3)))),
         ('Icosaxes', PHI, cut_solid(octa, x3G)), ('cuboctahedron', K(2), None),
         ('cut cube at golden height 2 + 1/phi^2', 2 + PHI.inv() * PHI.inv(), None),
         ('Lesser Golden Cut Cube', muL, GCC['Lesser']), ('Greater Golden Cut Cube', muG, GCC['Greater']),
         ('truncated cube (Archimedean)', 1 + S2, cut_cube(1 - S2 / 2)),
         ('cut cube at golden height 2 + 1/phi', 2 + PHI.inv(), None), ('cube', K(3), None)]
out['sections'] = []
for name, mu, target in named:
    V = CO(mu)
    rec = {'name': name, 'mu': kstr(mu), 'mu_float': float(mu), 'slope_1_over_mu': kstr(1 / mu), 'corners': len(V),
           'mu_field': 'Q' if in_q(mu) else 'Q(sqrt5)' if in_q5(mu) else ('Q(sqrt2)' if mu.v[2] == 0 and mu.v[3] == 0 else 'Q(sqrt2, sqrt5)')}
    if mu > 2 and mu < 3:
        t = mu - 2; r = (1 - t) / (S2 * t)            # octagon corner side / original side
        rec['octagon_ratio'] = kstr(r); rec['octagon_ratio_over_sqrt2'] = kstr(r / S2)
    if target is not None:
        ok, lam = similar(V, target)
        check(f'section of cube x octahedron at mu = {kstr(mu)} (~{float(mu):.6f}) is the {name} ({len(V)} corners)', ok)
    out['sections'].append(rec); print('   ', rec, flush=True)
check('octahedron pair at mu in Q(sqrt5), Archimedean truncated cube at mu in Q(sqrt2), Golden Cut Cubes at mu of degree 4',
      in_q5(3 - PHI) and in_q5(PHI) and not in_q5(muG) and not in_q5(muL) and (muG.v[2] != 0 or muG.v[3] != 0))
u1, u2 = PHI.inv() * PHI.inv(), PHI.inv()                 # t = mu - 2 at the golden heights
r1, r2 = (1 - u1) / (S2 * u1), (1 - u2) / (S2 * u2)
check(f'golden heights on the cube side give octagon ratios {kstr(r1)} = phi/sqrt2 and {kstr(r2)} = 1/(sqrt2 phi), not phi^+-1',
      r1 == PHI / S2 and r2 == ONE / (S2 * PHI))

# ---------------------------------------------------------------- D. D6 roots on F_mu
D6 = []
for i, j in itertools.combinations(range(6), 2):
    for s, u in itertools.product((1, -1), repeat=2):
        v = [0] * 6; v[i] = s; v[j] = u; D6.append(tuple(v))
def shadow(v, mu): return tuple(K(v[k]) + K(v[k + 3]) / mu for k in range(3))
def kind(v):
    a = [k for k in range(3) if v[k]]; b = [k for k in range(3) if v[k + 3]]
    if len(a) == 2: return 'e_a +- e_b (first cube)'
    if len(b) == 2: return 'f_a +- f_b (second factor)'
    return 'e_a +- f_a (same index)' if a == b else 'e_a +- f_b, a != b (mixed)'
groups = {}
for v in D6: groups.setdefault(kind(v), []).append(v)
check('D6: 60 roots in four orbits of the diagonal cube group: 12 + 12 + 12 + 24',
      sorted(len(g) for g in groups.values()) == [12, 12, 12, 24])
mixed = groups['e_a +- f_b, a != b (mixed)']
for mu, lab in ((PHI, 'phi'), (3 - PHI, '3 - phi'), (K(Fr(3, 2)), '3/2')):
    sh = uniq([shadow(v, mu) for v in mixed]); sec = CO(mu)
    ok = similar(sh, sec)[0]
    check(f'mixed D6 roots on F_mu, mu = {lab}: shadows similar to the section corners: {ok}', ok == (lab == 'phi'))
ok = similar(uniq([shadow(v, PHI) for v in mixed]), cut_solid(octa, x3G))[0]
check('on the golden flat F_phi the 24 mixed roots cast Icosaxes, and the section of C x C* there is Icosaxes: the same corners '
      '(section corner (1, 1/phi, 0) = shadow of e_1 + f_2)', ok and {key(p) for p in CO(PHI)} == {key(p) for p in uniq([shadow(v, PHI) for v in mixed])})

# ---------------------------------------------------------------- E. selection by lattice orbits (sympy)
m = sp.Symbol('mu', positive=True)
def conditions(v):
    """all mu in (1,3)\\{2} where |shadow| multiset = scaled corner pattern; returns (sweep_side or None, set of roots)"""
    w = [sp.Integer(v[k]) * m + v[k + 3] for k in range(3)]          # mu * shadow
    found = set(); sweep = set()
    for i, j, k in itertools.permutations(range(3)):
        for sj, sk in itertools.product((1, -1), repeat=2):
            # cube side: |w_i| = |w_j| (two largest), |w_k| = (mu - 2)|w_i|
            # octahedron side: |w_j| = (mu - 1)|w_i|, w_k = 0
            for side, eqs in (('cube', [w[i] - sj * w[j], w[k] - sk * (m - 2) * w[i]]),
                              ('octa', [w[j] - sj * (m - 1) * w[i], w[k]])):
                eqs = [sp.expand(e) for e in eqs]
                if all(e == 0 for e in eqs):
                    sweep.add(side); continue
                nz = [e for e in eqs if e != 0]
                g = nz[0]
                for e in nz[1:]: g = sp.gcd(g, e)
                if sp.degree(g, m) < 1: continue
                for r in sp.Poly(g, m).all_roots():
                    if not r.is_real: continue
                    rf = float(r)
                    lo, hi = (2, 3) if side == 'cube' else (1, 2)
                    if not (lo + 1e-12 < rf < hi - 1e-12): continue
                    # full check: |w(mu)| sorted equals the pattern (s, s, s(mu-2)) or (s, s(mu-1), 0), s > 0
                    a = sorted([abs(float(x.subs(m, r))) for x in w], reverse=True)
                    pat = [1, 1, rf - 2] if side == 'cube' else [1, rf - 1, 0]
                    if a[0] > 1e-12 and all(abs(a[q] / a[0] - pat[q]) < 1e-9 for q in range(3)):
                        found.add((side, sp.nsimplify(sp.simplify(r)) if r.is_rational else sp.simplify(r)))
    return sweep, found
reps = {}
for v in itertools.product(range(-2, 3), repeat=6):
    if not any(v): continue
    # canonical rep under the diagonal group: sort pairs (|a|,|b| with joint sign) -- use orbit min
    pairs = [(v[k], v[k + 3]) for k in range(3)]
    pairs = [p if (p[0], p[1]) >= (0, 0) and (p[0] > 0 or (p[0] == 0 and p[1] >= 0)) else (-p[0], -p[1]) for p in pairs]
    c = tuple(sorted(pairs))
    reps.setdefault(c, v)
print(f'   {len(reps)} orbit representatives of {{-2..2}}^6 under the diagonal cube group', flush=True)
sel = {}; sweeps = []
for c, v in reps.items():
    sw, fd = conditions(v)
    nrm = sum(x * x for x in v)
    if sw: sweeps.append({'v': v, 'norm': nrm, 'sides': sorted(sw)})
    for side, r in fd:
        k = (side, str(r))
        if k not in sel or sel[k]['norm'] > nrm:
            sel[k] = {'side': side, 'mu': str(r), 'mu_float': float(r), 'degree': int(sp.degree(sp.minimal_polynomial(r, sp.Symbol('z')))),
                      'v': v, 'norm': nrm}
out['selected_mu'] = sorted(sel.values(), key=lambda d: (d['side'], d['mu_float']))
out['sweep_orbits_min'] = sorted(sweeps, key=lambda d: d['norm'])[:6]
for d in out['selected_mu']: print('   ', d, flush=True)
fG, fL = float(muG), float(muL)
check(f'{len(sel)} isolated mu found, all of degree <= 2; neither Golden Cut Cube (mu_G ~ {fG:.6f}, mu_L ~ {fL:.6f}) is among them',
      all(d['degree'] <= 2 for d in sel.values()) and not any(abs(d['mu_float'] - f) < 1e-9 for d in sel.values() for f in (fG, fL)))
phi_sel = [d for d in sel.values() if abs(d['mu_float'] - float(PHI)) < 1e-12]
check(f'mu = phi (Icosaxes) is selected by a root (norm 2): smallest selecting norm {phi_sel[0]["norm"] if phi_sel else None}',
      bool(phi_sel) and phi_sel[0]['norm'] == 2)
mins = min(d['norm'] for d in sel.values())
check(f'among roots (norm 2) the only isolated mu is phi', sorted(d['mu'] for d in sel.values() if d['norm'] == 2) == [str(sp.nsimplify((1 + sp.sqrt(5)) / 2))]
      or all(abs(d['mu_float'] - float(PHI)) < 1e-12 for d in sel.values() if d['norm'] == 2))
check(f'sweep orbits exist (shadow = section for every mu); smallest norm {min(s["norm"] for s in sweeps)}', len(sweeps) > 0)

# ---------------------------------------------------------------- F. golden heights
def gh(x):
    """x = alpha + beta phi with alpha, beta in Q(sqrt2): x = a + (b - a)/phi^2 with a = alpha + 2 beta, b = a - beta"""
    a, b, c, d = x.v       # x = a + b r2 + c r5 + d r10 ; r5 = 2 phi - 1
    beta = K(0) + K(2 * c, 2 * d) ; alpha = K(a - c, b - d)
    A = alpha + 2 * beta; B = A - beta
    assert A + (B - A) * (PHI.inv() * PHI.inv()) == x
    return A, B
out['golden_height_form'] = {}
for lab, mu in (('Greater', muG), ('Lesser', muL)):
    A, B = gh(mu)
    out['golden_height_form'][lab] = {'mu': kstr(mu), 'a': kstr(A), 'b': kstr(B)}
    check(f'mu_{lab[0]} = {kstr(mu)} = a + (b - a)/phi^2 with a = {kstr(A)} (~{float(A):.4f}), b = {kstr(B)} (~{float(B):.4f}); '
          f'not two of the layers 1, 2, 3', not ({kstr(A), kstr(B)} <= {'1', '2', '3'}))
dump('s3-six-d.json', out)
