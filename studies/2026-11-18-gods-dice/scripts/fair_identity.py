"""Identity card of the fair 14-face die (DICTO 18 Nov: 'what is its harmonic identity etc').
P(mu) = [-1,1]^3 ∩ {|x|+|y|+|z| <= mu}; corners perms of (±1, ±b, 0), b = mu - 1.
1 corner-direction fingerprint Q_l, W_l-hat (Steinhardt–Nelson–Ronchetti 1983; same formulas as 2026-11-04-harmonic-fingerprint) at mu_f and neighbours
2 landing fingerprint: face normals weighted by solid angle (fair -> equal weights -> bcc 14-shell values)
3 Vacuus (2026-11-02 definition): fins O-A-B per edge, apex angles, strut lengths
4 field of mu_f (sympy minimal polynomials), volume, IQ, Mahler, Dehn. Controls: fcc/bcc/icosahedron classical values. FINAL ok/FAIL."""
import itertools, math, json
import numpy as np, sympy as sp
from scipy.special import sph_harm_y
from scipy.spatial import ConvexHull
from sympy.physics.wigner import wigner_3j
LS = (4, 6, 8, 10, 12, 14, 16); W3J = {}
def fp(P, w=None):
    P = np.array(P, float); u = P/np.linalg.norm(P, axis=1)[:, None]
    w = np.ones(len(u))/len(u) if w is None else np.array(w)/sum(w)
    th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0]); out = {}
    for l in LS:
        q = np.array([(w*sph_harm_y(l, m, th, ph)).sum() for m in range(-l, l+1)]); s = np.sum(abs(q)**2)
        if l not in W3J: W3J[l] = [(a, b_, -a-b_, float(wigner_3j(l, l, l, a, b_, -a-b_))) for a in range(-l, l+1) for b_ in range(-l, l+1) if abs(a+b_) <= l]
        W = sum(c*q[a+l]*q[b_+l]*q[c3+l] for a, b_, c3, c in W3J[l])
        out[l] = (math.sqrt(4*math.pi/(2*l+1)*s), float(np.real(W))/s**1.5 if s > 1e-14 else 0.0)
    return out
def perms(v):
    return np.array(sorted({tuple(a*s for a, s in zip(p, sg)) for p in itertools.permutations(v) for sg in itertools.product((1, -1), repeat=3)}))
ok = True; R = {}
# controls
bcc = np.vstack([perms((1, 1, 1))/math.sqrt(3), perms((1, 0, 0))])
for name, P, q4, q6 in [("fcc shell", perms((1, 1, 0)), .191, .575), ("bcc 14 shell", bcc, .036, .511)]:
    f = fp(P); good = abs(f[4][0]-q4) < 6e-4 and abs(f[6][0]-q6) < 6e-4; ok &= good
    print(f"control {name}: Q4 {f[4][0]:.4f} Q6 {f[6][0]:.4f} {'ok' if good else 'FAIL'}")
phi = (1+5**.5)/2; ico = np.array([(s1*a, s2*b, s3*c) for (a, b, c) in [(0, 1, phi), (1, phi, 0), (phi, 0, 1)] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]); ico = np.unique(ico, axis=0); f = fp(ico); good = f[4][0] < 1e-9 and abs(f[6][0]-.663) < 6e-4; ok &= good
print(f"control icosahedron: Q4 {f[4][0]:.1e} Q6 {f[6][0]:.4f} {'ok' if good else 'FAIL'}")
muf = 1 + math.sqrt(2*math.tan(math.pi/14)*math.tan(2*math.pi/7))
def solid(mu):
    b = mu-1; V = perms((1, b, 0)); return V, ConvexHull(V)
def sa(tri):
    a, b, c = tri; la, lb, lc = map(np.linalg.norm, (a, b, c))
    return 2*math.atan2(abs(np.dot(a, np.cross(b, c))), la*lb*lc+np.dot(a, b)*lc+np.dot(a, c)*lb+np.dot(b, c)*la)
def faces(V, H):
    F = {}
    for s, e in zip(H.simplices, H.equations): F.setdefault(tuple(np.round(e, 9)), []).append(s)
    return F
print("\n1-2. corner fingerprint (C) and landing fingerprint (L, face normals weighted by solid angle)")
rows = [("Kelvin TO 3/2", 1.5), ("insphere point √3", 3**.5), ("FAIR DIE mu_f", muf), ("cuboctahedron 2", 2.0)]
for name, mu in rows:
    V, H = solid(mu); F = faces(V, H)
    N = [k[:3] for k in F]; W = [sum(sa(V[t]) for t in F[k]) for k in F]
    c, L = fp(V), fp(N, W)
    print(f"  {name:20s} C: " + " ".join(f"Q{l} {c[l][0]:.4f}" for l in LS) + f"  W4^ {c[4][1]:+.4f} W6^ {c[6][1]:+.4f}")
    print(f"  {'':20s} L: " + " ".join(f"Q{l} {L[l][0]:.4f}" for l in LS) + f"  W4^ {L[4][1]:+.4f} W6^ {L[6][1]:+.4f}")
    R[name] = {"mu": mu, "corner": {l: c[l] for l in LS}, "landing": {l: L[l] for l in LS}}
Lb = fp(np.vstack([perms((1, 1, 1)), perms((1, 0, 0))]))  # equal weights on the 14 directions
Lf = R["FAIR DIE mu_f"]["landing"]; same = all(abs(Lf[l][0]-Lb[l][0]) < 1e-9 and abs(Lf[l][1]-Lb[l][1]) < 1e-9 for l in LS); ok &= same
print(f"  landing fingerprint of the fair die = equal-weight bcc 14 directions (all l, Q and W): {same}")
print("\n3. Vacuus of the fair die (fins O-A-B per edge; struts O->corner)")
V, H = solid(muf); F = faces(V, H)
edges = {}
for k, tris in F.items():
    pts = sorted({i for t in tris for i in t}); n = np.array(k[:3]); c = V[pts].mean(0)
    u = V[pts[0]]-c; u /= np.linalg.norm(u); w = np.cross(n, u)
    pts.sort(key=lambda i: math.atan2(np.dot(V[i]-c, w), np.dot(V[i]-c, u)))
    kind = 'S' if max(abs(n)) > .99 else 'H'
    for i in range(len(pts)):
        e = tuple(sorted((pts[i], pts[(i+1) % len(pts)]))); edges.setdefault(e, []).append(kind)
cls = {}
for e, ks in edges.items():
    A, B = V[e[0]], V[e[1]]; ang = math.degrees(math.acos(np.dot(A, B)/np.linalg.norm(A)/np.linalg.norm(B)))
    cls.setdefault("-".join(sorted(ks)), []).append((ang, np.linalg.norm(A-B)))
struts = sorted({round(float(np.linalg.norm(v)), 12) for v in V})
print(f"  corners {len(V)}, edges {len(edges)}, faces {len(F)}; strut lengths {struts}")
for k, L in cls.items():
    a = sorted({round(x[0], 9) for x in L}); el = sorted({round(x[1], 9) for x in L})
    rat = [(p, q) for q in range(1, 721) for p in range(1, q) if math.gcd(p, q) == 1 and abs(a[0] - 180*p/q) < 1e-7]
    print(f"  fins between {k}: {len(L)}, apex angle {a} deg, edge {el}; rational multiple of pi (q<=720): {rat[:1] or 'none'}")
print("\n4. numbers")
x = sp.symbols('x'); T = sp.tan(sp.pi/14)*sp.tan(2*sp.pi/7)
mT = sp.minimal_polynomial(T, x); mmu = sp.minimal_polynomial(1+sp.sqrt(2*T), x)
print(f"  tan(pi/14)tan(2pi/7) = {float(T):.15f}, minimal polynomial {mT}")
print(f"  mu_f minimal polynomial {mmu}")
c7 = sp.minimal_polynomial(sp.cos(2*sp.pi/7), x); print(f"  (heptagon: cos(2pi/7) has {c7})")
disc = sp.discriminant(mT, x); print(f"  discriminant of the cubic: {disc} = {sp.factorint(disc)}")
try:
    a = sp.to_number_field(T, sp.cos(2*sp.pi/7)); print(f"  T lies in Q(cos 2pi/7): T = {a.as_expr()} with c = cos(2pi/7)  (check {float(a.as_expr().subs(sp.Symbol('theta'), sp.cos(2*sp.pi/7))) if a.as_expr().free_symbols else ''})")
    R_field = "Q(cos 2pi/7)"
except Exception as ex:
    print(f"  T not shown in Q(cos 2pi/7): {ex}"); R_field = "unknown"
vol = H.volume; area = H.area; IQ = 36*math.pi*vol**2/area**3
dual = ConvexHull(np.array([k[:3] for k in F])/np.array([-k[3] for k in F])[:, None]); M = vol*dual.volume
D = 24*2**.5*(3-2*muf)
print(f"  volume {vol:.10f}  surface {area:.10f}  IQ {IQ:.6f}  Mahler {M:.6f}  Dehn coefficient 24√2(3-2mu) = {D:.6f} (nonzero)")
R["numbers"] = {"mu_f": muf, "volume": vol, "IQ": IQ, "Mahler": M, "Dehn": D, "minpoly_T": str(mT), "minpoly_mu": str(mmu)}
import os; os.makedirs("../data", exist_ok=True); json.dump(R, open("../data/fair-identity.json", "w"), indent=1, default=str)
print("FINAL ok" if ok else "FINAL FAIL")
