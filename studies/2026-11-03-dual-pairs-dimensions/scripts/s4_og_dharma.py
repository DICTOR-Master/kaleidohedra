"""Step 4 (DICTO's question: "Is there a connection with OG and the interactions of dodeca and icosa at interdimensional points?").
D = the dodecahedron with corners (+-1,+-1,+-1), (0, +-1/phi, +-phi) cyclic (R^2 = 3, the cube's sphere); D* its polar (icosahedron).
Families: sections S(mu) = D cap mu D* (6D product cut by y = x/mu) and hulls H(mu) = conv(D cup mu D*) = mu polar(S(mu)).
Two-parameter family Q(mu, lam) = H(mu) cap lam D*  (hull cut again by icosahedron planes), polar family conv(S(mu)/mu cup D/lam).
A. OG (DICTO Ogdoecontahedron, #31) = Q(mu_TI, rho^2): the pentakis dodecahedron H(mu_TI) (polar of the truncated icosahedron)
   cut by the icosahedron planes through D's edge midpoints (the rectification level rho^2 = phi^2). Checked: 102 corners,
   80 faces (60 kites + 20 regular hexagons), and corner-for-corner equal to the polar-Dharma chain's OG after one scale.
B. Every station of the polar Dharma cycle located exactly: c D, S(phi^2), Q(mu_TI, phi^2), H(mu_TI), H(3) = 3 D*,
   (3/phi^2) H(phi^2), phi^3 c D; nesting, touching and tight factors exact; closure phi^3.
C. (moved to s4c_relatives.py) Golden relatives Q(mu, phi^2) at the golden mu of the icosahedron side (neutral labels, face signatures).
D. (moved to s4b_og_lattice.py) Lattice: the ideal {lam in Q(sqrt5): lam * OG corners in the icosahedral module M = Z-span(0, +-1, +-phi) cyclic}; its
   generator and the smallest integer scale, in our frame and in the chain frame (the bridge study found 171 there).
usage (dicto-big-brother): ~/geom/bin/python s4_og_dharma.py -> ../data/s4-og-dharma.json
"""
from dp_lib import *          # noqa
import numpy as np, sympy as sp
out = {}
P = Pair('dodecahedron', platonic()['dodecahedron'][0])
D, N = P.V, P.N
muTI = P.mu_Ps(ONE / 3); rho2 = P.rho2
check(f'rho^2 = {kstr(rho2)} = phi^2, mu_TI = {kstr(muTI)}', rho2 == PHI * PHI)
PD = P.Hull(muTI)
C_PD, F_PD, Pl_PD = planes_of(PD)
check(f'A: H(mu_TI) is the pentakis dodecahedron: {len(C_PD)} corners, faces {signature(F_PD)}', len(C_PD) == 32 and signature(F_PD) == {3: 60})
OG = vertices_H(Pl_PD + [(v, rho2) for v in D])
C_OG, F_OG = hull3(OG)
sig = signature(F_OG)
# hexagons regular? kites?
def sides(f): return [d2(C_OG[f[i]], C_OG[f[(i + 1) % len(f)]]) for i in range(len(f))]
def ordered(f):
    pts = [C_OG[i] for i in f]; c = tuple(sum((p[k] for p in pts), ZERO) / len(pts) for k in range(3))
    import math
    fp = np.array([[float(x) for x in p] for p in pts]); fc = fp.mean(0); n = np.cross(fp[1] - fp[0], fp[2] - fp[0])
    u = fp[0] - fc; u /= np.linalg.norm(u); w = np.cross(n / np.linalg.norm(n), u)
    return [f[i] for i in sorted(range(len(f)), key=lambda i: math.atan2((fp[i] - fc) @ w, (fp[i] - fc) @ u))]
hexes = [ordered(f) for f in F_OG if len(f) == 6]; quads = [ordered(f) for f in F_OG if len(f) == 4]
reg = all(len({s.v for s in sides(f)}) == 1 for f in hexes)
kite = all((lambda s: (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]))(sides(f)) for f in quads)
check(f'A: OG = Q(mu_TI, phi^2) = H(mu_TI) cap phi^2 D*: {len(C_OG)} corners, faces {sig}; hexagons regular {reg}, quadrilaterals kites {kite}',
      len(C_OG) == 102 and sig == {4: 60, 6: 20} and reg and kite)
S_rect = P.S(rho2)
check('A: the 30 corners of the icosidodecahedron S(phi^2) are corners... on the hexagon planes of OG (OG contains S(phi^2), touching)',
      all(any(dot(v, x) == rho2 for v in D) for x in S_rect) and all(all(dot(n, x) <= d for n, d in planes_of(C_OG)[2]) for x in S_rect))
# B. the polar Dharma chain, matched to the chain data (floats of its exact corners)
chain = json.load(open(os.path.join(DATA, 'reversed-chain.json')))
def fl_set(V): return np.array([[float(x) for x in v] for v in V])
def match(A, Bf):
    """scale s (float) with s A = B as point sets (1e-9); returns s or None"""
    Af = fl_set(A); s = np.linalg.norm(Bf, axis=1).max() / np.linalg.norm(Af, axis=1).max()
    from scipy.spatial import cKDTree
    d, _ = cKDTree(Bf).query(Af * s)
    return s if len(Af) == len(Bf) and d.max() < 1e-9 else None
c_scale_sq = None
stations = [('D (inner)', 'c D', D), ('icosidodecahedron', 'S(phi^2)', S_rect), ('OG', 'Q(mu_TI, phi^2)', C_OG),
            ('pentakis dodecahedron', 'H(mu_TI)', C_PD), ('icosahedron', 'H(3) = 3 D*', P.Hull(K(3))),
            ('rhombic triacontahedron', '(3/phi^2) H(phi^2)', [vscale(3 / rho2, p) for p in P.Hull(rho2)]),
            ('D (phi^3)', 'phi^3 c D', D)]
scales = []
for (lab, form, X), (cn, cv) in zip(stations, chain):
    s = match(X, np.array(cv)); scales.append(s)
    check(f'B: chain station "{cn}" = {form} up to one common chain scale (float match 1e-9)', s is not None)
k0 = scales[1]
rel = [s / k0 for s in scales]
print('   scales relative to the middle stations:', [f'{r:.12f}' for r in rel], flush=True)
check('B: the four middle stations S(phi^2), OG, H(mu_TI), 3D* (and RT as (3/phi^2) H(phi^2)) share ONE scale: they are the 6D sections/hulls themselves',
      all(abs(r - 1) < 1e-12 for r in rel[1:6]))
cf = rel[0] ** 2
c2 = sp.nsimplify(cf, [sp.sqrt(5)], tolerance=1e-12)
print('   c^2 =', c2, flush=True)
# exact c: c^2 in Q(sqrt5); c itself?
a_, b_ = [sp.Rational(x) for x in (sp.Poly(sp.expand(c2), sp.sqrt(5)).all_coeffs()[::-1] + [0])[:2]] if c2.has(sp.sqrt(5)) else (sp.Rational(c2), 0)
cK2 = K(Fr(int(a_.p), int(a_.q)), 0, Fr(int(b_.p), int(b_.q)))
# try c in Q(sqrt5)
cK = None
for den in range(1, 200):
    for A in range(-400, 401):
        Bf = (float(rel[0]) * den - A) / 5 ** .5
        Bn = round(Bf)
        if abs(Bf - Bn) < 1e-9:
            cand = K(Fr(A, den), 0, Fr(Bn, den))
            if cand * cand == cK2: cK = cand; break
    if cK is not None: break
out['inner_scale_c'] = {'c^2': kstr(cK2), 'c': kstr(cK) if cK is not None else 'not in Q(sqrt5)', 'c_float': rel[0]}
check(f'B: inner dodecahedron = c D with c^2 = {kstr(cK2)}, c = {kstr(cK) if cK is not None else "?"} (~{rel[0]:.9f}); outer = phi^3 c D',
      cK is not None and abs(rel[6] / rel[0] - float(PHI) ** 3) < 1e-12)
Ks = [cK * 1, ONE, ONE, ONE, ONE, ONE, cK * PHI * PHI * PHI]
St = [[vscale(k, p) for p in X] for k, (_, _, X) in zip(Ks, stations)]
links = []; TT = []
for k in range(6):
    A, B_ = St[k], St[k + 1]
    t = tight(A, B_); TT.append(t); inside = t <= ONE
    tch = touches(A, B_)
    _, _, PlA = planes_of(A)
    thru = sum(1 for b in hull3(B_)[0] if any(dot(n, b) == d for n, d in PlA))
    links.append({'from': stations[k][0], 'to': stations[k + 1][0], 'inside': inside, 'tight_factor': kdesc(t),
                  'inner_corners_on_outer_faces': tch})
    check(f'B: {stations[k][0]} inside {stations[k + 1][0]}: {inside}; tight factor {kstr(t)} (~{float(t):.6f}); '
          f'{tch} inner corners on outer faces', inside)
out['chain_links'] = links
tprod = ONE
for t in TT: tprod = tprod * t
cl = PHI * PHI * PHI * tprod   # closure after tightening every link (each station rescaled to touch the next)
check(f'B: closure of the given cycle = phi^3 (exact); closure if every link is tightened = product of tight factors = {kstr(cl)} (~{float(cl):.6f})',
      Ks[6] / Ks[0] == PHI * PHI * PHI)
out['closure_given'] = 'phi^3'; out['closure_all_tight'] = kdesc(cl)
out['all_tight_note'] = 'closure_all_tight = phi^3 x product of the tight factors of the given links'
check('B: sanity vs polar-Dharma step 4 (tight nest closure 1.814635): our all-tight product agrees to 1e-6', abs(float(cl) - 1.814635) < 1e-6)
out['path'] = [{'station': s[0], 'form': s[1]} for s in stations]
out['parameters'] = {'mu_TI': kdesc(muTI), 'nu_TI': kdesc(muTI / P.r2), 'rho2': kdesc(rho2), 'nu_rect': kdesc(rho2 / P.r2)}
save('s4-og-dharma.json', out)
