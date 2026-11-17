"""Protocol steps 6-9 for the fair 14-face die: volume, area, isoperimetric quotient, Mahler product, canonical form at the centre,
Dehn invariant (exact closed forms on chamber I, each checked against the hull at sample points, then evaluated exactly at mu_f);
harmonic fingerprint (exact Q4 by the cubic invariant, Q_l l = 4..16 float with the Steinhardt–Nelson–Ronchetti 1983 formulas as in
studies/2026-11-04-harmonic-fingerprint and 2026-11-18-gods-dice/scripts/fair_identity.py); independent Dehn screen with
studies/2026-11-04-dehn-screen/scripts/dehn.py (calibrated there 11/11; recalibrated here). Control: Kelvin's TO (mu = 3/2)."""
import math, json, sys, os, importlib.util
import numpy as np, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fdlib import *
C = Checks(); R = {}
mu = sp.Symbol('mu'); b = mu - 1
Vf = sp.Rational(4, 3)*mu**3 - 4*b**3                       # octahedron minus 6 corner pyramids
Af = 12*b**2 + 4*sp.sqrt(3)*(mu**2 - 3*b**2)                 # 6 squares 2b^2 + 8 hexagons (sqrt3/2)(mu^2 - 3b^2)
Pf = 8/mu**2                                                 # polar = conv(C*, C/mu): volume 8/mu^2 on chamber I (mahler-sweep)
Om = 6*Pf                                                    # canonical form at the centre = 3!·vol(polar) (canonical-sweep)
Dc = 24*sp.sqrt(2)*(3 - 2*mu)                                # Dehn = Dc ⊗ arccos(1/sqrt3) mod Q·pi (God's Dice)
print("STEP 6. Closed forms on chamber I checked against the hull (5 sample points + Kelvin)")
from scipy.spatial import ConvexHull
for s in (1.1, 1.3, 1.5, 1.7, MUF, 1.9):
    V = corners(s); H = ConvexHull(V)
    eqs = list({tuple(np.round(e, 9)): e for e in H.equations}.values())
    dualpts = np.array([np.array(e[:3])/(-e[3]) for e in eqs]); vp = ConvexHull(dualpts).volume
    ok = abs(H.volume - float(Vf.subs(mu, s))) < 1e-9 and abs(H.area - float(Af.subs(mu, s))) < 1e-9 and abs(vp - float(Pf.subs(mu, s))) < 1e-9
    C(f"mu = {s:.6f}: volume, area, polar volume match the closed forms", ok)
print("\nexact values at mu_f (minimal polynomials over Q) and at Kelvin 3/2")
def ex(name, f, sq3=False):
    g = sp.simplify(f.subs(mu, 1 + y))
    if sq3:   # f = P + Q sqrt3: minimal polynomial of the square-free part via (z - P)^2 = 3 Q^2
        P_, Q_ = sp.expand(g).as_independent(sp.sqrt(3)); Q_ = sp.simplify(Q_/sp.sqrt(3))
        p1, v1 = minpoly_of(P_); p2, v2 = minpoly_of(Q_); val = v1 + mp.sqrt(3)*v2
        # resultant elimination: z = P + sqrt3 Q  ->  z with (z-P)^2 - 3Q^2 = 0
        e = sp.together((z - P_)**2 - 3*Q_**2); n_, d_ = sp.fraction(e)
        res = sp.resultant(sp.Poly(n_, y), sp.Poly(M_B, y)); best = None
        for fct, _ in sp.factor_list(sp.Poly(res, z))[1]:
            cs = [mp.mpf(sp.Rational(c).p)/sp.Rational(c).q for c in sp.Poly(fct, z).all_coeffs()]
            r = abs(mp.polyval(cs, val))/max(abs(c) for c in cs)
            if best is None or r < best[0]: best = (r, fct)
        assert best[0] < mp.mpf(10)**-25
        p = sp.Poly(best[1], z).primitive()[1]; p = -p if p.LC() < 0 else p
    else:
        p, val = minpoly_of(g)
    kv = f.subs(mu, sp.Rational(3, 2))
    print(f"  {name:28s} mu_f: {mp.nstr(val, 15):>18s}  minpoly degree {p.degree()}: {p.as_expr()}")
    print(f"  {'':28s} Kelvin: {sp.nsimplify(sp.simplify(kv))} = {float(kv):.10f}")
    R[name] = {'mu_f': mp.nstr(val, 25), 'minpoly': str(p.as_expr()), 'kelvin': str(sp.simplify(kv))}
    return val, p
v, _ = ex("volume (half-width 1)", Vf); a, _ = ex("surface area", Af, sq3=True)
iq = 36*mp.pi*v**2/a**3; print(f"  isoperimetric quotient 36 pi V^2/A^3   mu_f {mp.nstr(iq, 12)}; line max at sqrt3 (Lindelof) 0.781640; Kelvin {36*math.pi*16/float(Af.subs(mu, 1.5))**3:.6f}")
R['IQ'] = mp.nstr(iq, 15)
C("IQ(mu_f) < IQ(sqrt3) (the line's maximum)", iq < 36*mp.pi*float(Vf.subs(mu, sp.sqrt(3)))**2/float(Af.subs(mu, sp.sqrt(3)))**3)
mah, _ = ex("Mahler product V·V(polar)", Vf*Pf); om, _ = ex("Omega(S;0) = 3!·vol(polar)", Om)
C("Mahler(mu_f) below the line's maximum 14.37509 and above the cube/octahedron minimum 32/3", 32/3 < mah < 14.37509)
dval = 24*mp.sqrt(2)*(3 - 2*MU_HP); print(f"  Dehn invariant: 24 sqrt2 (3 - 2 mu_f) ⊗ arccos(1/sqrt3) = {mp.nstr(dval, 15)} ⊗ arccos(1/sqrt3); zero only at 3/2 on chamber I")
C("Dehn coefficient nonzero at mu_f (|value| > 1; exactly nonzero since mu_f != 3/2, step 4)", abs(dval) > 1); R['Dehn_coefficient'] = mp.nstr(dval, 20)

print("\nSTEP 7. Independent Dehn screen (dehn.py of studies/2026-11-04-dehn-screen, PSLQ basis, tol 1e-10, coefficients <= 300)")
sys.argv = ['dehn', 'x', '10', '300']
spec = importlib.util.spec_from_file_location('dehn', os.path.join(HERE, '..', '..', '2026-11-04-dehn-screen', 'scripts', 'dehn.py'))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
cube = perms((1, 1, 1)); octa = perms((1, 0, 0))
for name, P, want in (("cube (control, zero)", cube, True), ("Kelvin TO (control, zero)", corners(1.5), True), ("octahedron (control, nonzero)", octa, False),
                      ("fair die", corners(MUF), False)):
    Pp, F = D.hull_faces(P); r = D.dehn(Pp, F, name)
    C(f"Dehn screen: {name}: zero = {r['dehn_zero']}", r['dehn_zero'] == want, f"{r['distinct_angles']} angles, basis {r['basis_angles']}")
    if name == "fair die": R['dehn_screen'] = r

print("\nSTEP 8. Harmonic fingerprint (corners C; landing L = face normals weighted by solid angle)")
s = (1 + BF**4)/(1 + BF**2)**2
q4c = 2.5*math.sqrt(7/12)*abs(s - 0.6)
print(f"  exact Q4 by the cubic invariant: Q4 = (5/2) sqrt(7/12) |<x^4+y^4+z^4> - 3/5|; zero iff b = 1/tau (Icosaxes)")
pq, vq = minpoly_of((1 + y**4)/(1 + y**2)**2 - sp.Rational(3, 5))
print(f"  corners: <x^4+y^4+z^4> - 3/5 = {mp.nstr(vq, 15)} (minpoly {pq.as_expr()}), Q4 = {q4c:.10f}")
print(f"  landing: equal weights on the 14 bcc directions, <x^4+y^4+z^4> = 13/21 exactly, Q4 = sqrt(7/12)/21 = {math.sqrt(7/12)/21:.10f}")
# reuse the fingerprint function only: copy of fp() from fair_identity.py (same formulas)
from scipy.special import sph_harm_y
from sympy.physics.wigner import wigner_3j
LS = (4, 6, 8, 10, 12, 14, 16); W3J = {}
def fp(P, w=None):
    P = np.array(P, float); u = P/np.linalg.norm(P, axis=1)[:, None]
    w = np.ones(len(u))/len(u) if w is None else np.array(w)/sum(w)
    th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0]); out = {}
    for l in LS:
        q = np.array([(w*sph_harm_y(l, mm, th, ph)).sum() for mm in range(-l, l+1)]); ss = np.sum(abs(q)**2)
        if l not in W3J: W3J[l] = [(a_, b_, -a_-b_, float(wigner_3j(l, l, l, a_, b_, -a_-b_))) for a_ in range(-l, l+1) for b_ in range(-l, l+1) if abs(a_+b_) <= l]
        W = sum(c*q[a_+l]*q[b_+l]*q[c3+l] for a_, b_, c3, c in W3J[l])
        out[l] = (math.sqrt(4*math.pi/(2*l+1)*ss), float(np.real(W))/ss**1.5 if ss > 1e-14 else 0.0)
    return out
bcc = np.vstack([perms((1, 1, 1))/math.sqrt(3), perms((1, 0, 0))])
for name, P, q4, q6 in (("fcc shell", perms((1, 1, 0)), .1909, .5745), ("bcc 14 shell", bcc, .0364, .5107)):
    f = fp(P); C(f"control {name}: Q4 {f[4][0]:.4f} Q6 {f[6][0]:.4f} (classical)", abs(f[4][0] - q4) < 2e-4 and abs(f[6][0] - q6) < 2e-4)
for name, m_ in (("Kelvin TO 3/2", 1.5), ("fair die mu_f", MUF)):
    V = corners(m_); F, N, H = faces(V); W = [solid_angle_face(V, f) for f in F]
    c, L = fp(V), fp(N, W)
    print(f"  {name:14s} C: " + " ".join(f"Q{l} {c[l][0]:.4f}" for l in LS) + f"  W4^ {c[4][1]:+.4f} W6^ {c[6][1]:+.4f}")
    print(f"  {'':14s} L: " + " ".join(f"Q{l} {L[l][0]:.4f}" for l in LS))
    R[f'fingerprint {name}'] = {'corner': {l: c[l] for l in LS}, 'landing': {l: L[l] for l in LS}}
    if name.startswith('fair'):
        C("exact corner Q4 equals the float fingerprint", abs(c[4][0] - q4c) < 1e-10)
        C("landing fingerprint = bcc 14 shell (all l)", all(abs(L[l][0] - fp(bcc)[l][0]) < 1e-9 for l in LS))
        C("no corner Q_l vanishes, l = 4..16", min(c[l][0] for l in LS) > 0.05)
        C("total solid angle 4 pi and each face 4 pi/14", abs(sum(W) - 4*math.pi) < 1e-12 and max(abs(x - 4*math.pi/14) for x in W) < 1e-12)
json.dump(R, open(os.path.join(HERE, '..', 'data', 's02-measures.json'), 'w'), indent=1, default=str)
C.final()
