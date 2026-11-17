"""Protocol steps 15-17 for the fair 14-face die.
15 Vacuus (DICTO's definition, studies/2026-11-02-dicto-vacuus, #87): one fin O-A-B per edge AB, one strut O->corner; isofin?;
   rational-pi apex angles, decided EXACTLY: if theta = p pi/q then 2cos(theta) is an algebraic integer (it is z + 1/z for a root of
   unity z), so a non-integral minimal polynomial of 2cos(theta) proves theta/pi irrational. Kind (heart / inherited heart / non-heart,
   DICTO 16 Nov): 3D heart = centre strictly inside every face plane and centrally symmetric.
16 Origami (studies/2026-11-02-vacuus-origami): one open fan per face, fan angle = sum of the face's fin apex angles; folds if < 360 deg.
17 Centre pyramids (Concordance row "Centre pyramids T, C6, R12, RT"; #44, #77, #92, #93): 6 square and 8 hexagon pyramids; volumes,
   solid angles; Dehn of each pyramid (dehn.py of studies/2026-11-04-dehn-screen, recalibrated); the three 'equal share' points of the
   line (equal solid angle = fair, equal pyramid volume, equal face area), exact. Control: Kelvin's TO."""
import math, json, sys, os, importlib.util
import numpy as np, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fdlib import *
C = Checks(); R = {}
print("STEP 15. Vacuus")
cosSH = 1/(1 + y**2)          # fin over a square-hexagon edge: A = (1, b, 0), B = (1, 0, b)
cosHH = 2*y/(1 + y**2)       # fin over a hexagon-hexagon edge: A = (1, 0, b), B = (b, 0, 1)
Vx = corners(MUF); F, N, H = faces(Vx)
E = {}
for fi, f in enumerate(F):
    for i in range(len(f)): E.setdefault(tuple(sorted((f[i], f[(i + 1) % len(f)]))), []).append(len(f))
ang = {}
for (i, j), ks in E.items():
    a = math.degrees(math.acos(np.dot(Vx[i], Vx[j])/np.linalg.norm(Vx[i])/np.linalg.norm(Vx[j]))); ang.setdefault(tuple(sorted(ks)), set()).add(round(a, 9))
print(f"  fins: {len(E)}; kinds by apex angle: { {k: sorted(v) for k, v in ang.items()} }")
C("two fin kinds (24 square-hexagon, 12 hexagon-hexagon): not isofin", len({x for v in ang.values() for x in v}) == 2)
C("one strut length (all corners on one sphere)", len({round(float(np.linalg.norm(v)), 10) for v in Vx}) == 1)
for name, cexpr in (("square-hexagon fin", cosSH), ("hexagon-hexagon fin", cosHH)):
    p, val = minpoly_of(2*cexpr)
    integral = p.LC() == 1
    print(f"  {name}: apex {math.degrees(math.acos(float(val)/2)):.9f} deg; 2cos(apex) minimal polynomial {p.as_expr()}")
    C(f"{name}: 2cos(apex) is not an algebraic integer -> apex/pi irrational (exact)", not integral)
mpo = lambda c: sp.Poly(sp.minimal_polynomial(2*c, z), z)
C("control: cuboctahedron fin (corners (1,1,0),(1,0,1), apex 60 deg) has integral 2cos (minimal polynomial z - 1)", mpo(sp.Rational(1, 2)).LC() == 1)
C("control: cube fin (corners (1,1,1),(1,1,-1), apex arccos(1/3), irrational) has non-integral 2cos (3z - 2)", mpo(sp.Rational(1, 3)).LC() != 1)
inside = all(e[3] < -1e-9 for e in H.equations)
key = lambda p: tuple(np.round(p, 9)); csym = {key(v) for v in Vx} == {key(-v) for v in Vx}
C("heart kind: centre strictly inside every face plane and centrally symmetric", inside and csym)
print("\nSTEP 16. Origami fans (open centre pyramid of each face)")
fan = {}
for f in F:
    s = sum(math.degrees(math.acos(np.dot(Vx[f[i]], Vx[f[(i + 1) % len(f)]])/np.linalg.norm(Vx[f[i]])**2)) for i in range(len(f)))
    fan.setdefault(len(f), set()).add(round(s, 8))
print(f"  fan angles: squares {sorted(fan[4])} deg, hexagons {sorted(fan[6])} deg -> 2 distinct nets")
C("every fan angle < 360 deg (folds as modular origami, one net per face kind)", max(x for v in fan.values() for x in v) < 360)
R['fins'] = {str(k): sorted(v) for k, v in ang.items()}; R['fans'] = {str(k): sorted(v) for k, v in fan.items()}

print("\nSTEP 17. Centre pyramids")
mu = sp.Symbol('mu'); b = mu - 1
volS = 2*b**2/3; volH = (mu**2 - 3*b**2)*mu/6          # square: base 2b^2, height 1; hexagon: base (sqrt3/2)(mu^2-3b^2), height mu/sqrt3
areaS = 2*b**2; areaH = sp.sqrt(3)/2*(mu**2 - 3*b**2)
C("exact: 6 volS + 8 volH = volume (4/3 mu^3 - 4 b^3)", sp.expand(6*volS + 8*volH - (sp.Rational(4, 3)*mu**3 - 4*b**3)) == 0)
for name, m_ in (("Kelvin TO 3/2", 1.5), ("fair die mu_f", MUF)):
    vs, vh = float(volS.subs(mu, m_)), float(volH.subs(mu, m_))
    Vx2 = corners(m_); F2, N2, _ = faces(Vx2); W = sorted({round(solid_angle_face(Vx2, f), 12) for f in F2})
    print(f"  {name:14s} square pyramid volume {vs:.8f}, hexagon pyramid {vh:.8f} (ratio {vh/vs:.6f}); solid angles {W}")
R['pyr_vol_fair'] = (float(volS.subs(mu, MUF)), float(volH.subs(mu, MUF)))
rv = [r for r in sp.Poly(sp.expand(4*b**2 - mu*(mu**2 - 3*b**2)), mu).real_roots() if 1 < r < 2]
ra = [r for r in sp.solve(sp.Eq(2*b**2, sp.sqrt(3)/2*(mu**2 - 3*b**2)), mu) if r.is_real and 1 < float(r) < 2]
print(f"  equal pyramid volume: 4b^2 = mu(mu^2 - 3b^2) -> mu_v = {[ (sp.factor(sp.minimal_polynomial(r, mu)), float(r)) for r in rv]}")
print(f"  equal face area: 2b^2 = (sqrt3/2)(mu^2 - 3b^2) -> mu_a = {[(sp.nsimplify(r), float(r)) for r in ra]}")
print(f"  equal solid angle (fair): mu_f = {MUF:.10f}; insphere (equal face distance) sqrt3 = {math.sqrt(3):.10f}")
C("the three equal-share points are distinct from each other and from sqrt3", len(rv) == 1 and len(ra) == 1 and min(abs(float(rv[0]) - MUF), abs(float(ra[0]) - MUF), abs(float(rv[0]) - float(ra[0])), abs(float(rv[0]) - 3**.5), abs(float(ra[0]) - 3**.5)) > 1e-3)
R['mu_equal_volume'] = float(rv[0]); R['mu_equal_area'] = float(ra[0])
sys.argv = ['dehn', 'x', '10', '300']
spec = importlib.util.spec_from_file_location('dehn', os.path.join(HERE, '..', '..', '2026-11-04-dehn-screen', 'scripts', 'dehn.py'))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
cube = perms((1, 1, 1))
P, Fc = D.hull_faces(np.vstack([np.zeros(3), cube[cube[:, 0] > 0]])); C("Dehn control: cube's centre pyramid is zero (#100)", D.dehn(P, Fc, 'C6')['dehn_zero'])
for name, m_ in (("Kelvin TO 3/2", 1.5), ("fair die mu_f", MUF)):
    Vx2 = corners(m_); F2, N2, _ = faces(Vx2)
    for k in (4, 6):
        f = next(f for f in F2 if len(f) == k); P, Fp = D.hull_faces(np.vstack([np.zeros(3), Vx2[f]])); r = D.dehn(P, Fp, f'{name} {k}-gon pyramid')
        print(f"  Dehn screen, {name} {'square' if k == 4 else 'hexagon'} pyramid: zero = {r['dehn_zero']} ({r['distinct_angles']} angles, basis {r['basis_angles']})")
        R[f'pyr dehn {name} {k}'] = r['dehn_zero']
json.dump(R, open(os.path.join(HERE, '..', 'data', 's04-vacuus-pyramids.json'), 'w'), indent=1, default=str)
C.final()
