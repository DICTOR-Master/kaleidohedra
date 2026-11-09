# DICTO 2026-11-09 harmonic-gaps study, step 0: sanity checks of the harmonic tools before any use.
#  (1) Steinhardt Q_l, W6-hat of the icosahedron's and dodecahedron's corners (classical: icosahedron Q6 = 0.663, W6^ = -0.169754;
#      dodecahedron Q6 0.368, W6^ +0.1698 as in studies/2026-11-04-harmonic-fingerprint), Q4 = Q8 = 0 for both;
#  (2) the quadrature as a sphere rule (f = 1 and Y_lm Y_l'm' orthonormality, l <= 30) on the cube's visible boundary;
#  (3) the radial function of a sphere (r = 1: a00 = sqrt(4 pi), all else 0) and of the cube [-1,1]^3 (solid angle 4 pi, volume 8,
#      only cubic degrees 0, 4, 6, 8, ...), convergence between two quadrature settings, and a brute-force grid cross-check.
import itertools, math, json, os, numpy as np
from sympy.physics.wigner import wigner_3j
from radial import *
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
phi = (1 + 5 ** .5) / 2; res = {}; fails = []
def check(c, m):
    print(('PASS ' if c else 'FAIL ') + m, flush=True)
    if not c: fails.append(m)
def cycp(v):
    out = set()
    for k in range(3):
        p = v[k:] + v[:k]
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(round(a * b, 12) for a, b in zip(p, s)))
    return np.array(sorted(out))
ICO = cycp([0, 1, phi]); DOD = np.vstack([np.array(list(itertools.product((1, -1), repeat=3)), float), cycp([0, 1 / phi, phi])])
W3J = {}
def QW(Pts, l):
    U = Pts / np.linalg.norm(Pts, axis=1)[:, None]; th = np.arccos(U[:, 2]); ph = np.arctan2(U[:, 1], U[:, 0])
    q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l + 1)]); s = np.sum(abs(q) ** 2)
    if l not in W3J: W3J[l] = [(a, b, -a - b, float(wigner_3j(l, l, l, a, b, -a - b))) for a in range(-l, l + 1) for b in range(-l, l + 1) if abs(a + b) <= l]
    w = sum(c * q[a + l] * q[b + l] * q[cc + l] for a, b, cc, c in W3J[l])
    return math.sqrt(4 * math.pi / (2 * l + 1) * s), (float(np.real(w)) / s ** 1.5 if s > 1e-14 else 0.0)
for name, Pts, q6, w6 in (('icosahedron', ICO, 0.6633, -0.169754), ('dodecahedron', DOD, 0.3685, 0.169754)):
    Q4, _ = QW(Pts, 4); Q6, W6 = QW(Pts, 6); Q8, _ = QW(Pts, 8)
    res[name] = {'Q4': Q4, 'Q6': Q6, 'W6hat': W6, 'Q8': Q8}
    check(abs(Q4) < 1e-12 and abs(Q8) < 1e-12 and abs(Q6 - q6) < 5e-4 and abs(W6 - w6) < 1e-5, f'{name}: Q4 {Q4:.1e} Q6 {Q6:.4f} W6^ {W6:+.6f} Q8 {Q8:.1e}')
# cube faces
C = np.array(list(itertools.product((1, -1), repeat=3)), float)
cube_faces = []
for k in range(3):
    for s in (1, -1):
        F = C[C[:, k] == s]; c = F.mean(0); n = np.zeros(3); n[k] = s; u = F[0] - c; w = np.cross(n, u)
        cube_faces.append(F[np.argsort(np.arctan2((F - c) @ w, (F - c) @ u))])
vis = visible(cube_faces)
runs = {}
for tag, order, ma in (('A', 20, 0.4), ('B', 28, 0.4)):
    X, W = quad_points(vis, order, ma); U = X / np.linalg.norm(X, axis=1)[:, None]; Y = real_Y(U); r = np.linalg.norm(X, axis=1)
    runs[tag] = (X, W, Y, r)
    print(f'quadrature {tag}: {len(W)} points', flush=True)
X, W, Y, r = runs['B']
check(abs(W.sum() - 4 * math.pi) < 1e-11, f'solid angle 4 pi: {W.sum():.15f}')
check(abs((W * r ** 3).sum() / 3 - 8) < 1e-11, f'cube volume by ∫ r^3/3 dΩ = {(W * r ** 3).sum() / 3:.15f}')
XA, WA, YA, rA = runs['A']; Ym = np.vstack([YA[l] for l in range(LMAX + 1)]); G = (Ym * WA) @ Ym.T; del Ym; err = np.abs(G - np.eye(len(G))).max()
check(err < 1e-10, f'orthonormality of the {len(G)} real Y_lm (l <= 30) under the quadrature: max error {err:.1e}')
a1, P1 = coeffs(X, W, np.ones(len(W)), Y=Y)
check(abs(a1[0][0] - math.sqrt(4 * math.pi)) < 1e-12 and P1[1:].max() < 1e-22, f'sphere r = 1: a00 = {a1[0][0]:.12f} (sqrt(4pi) {math.sqrt(4*math.pi):.12f}), max P_l (l>0) {P1[1:].max():.1e}')
aA, PA = coeffs(*runs['A'][:2], runs['A'][3], Y=runs['A'][2]); aB, PB = coeffs(X, W, r, Y=Y)
conv = max(np.abs(aA[l] - aB[l]).max() for l in range(LMAX + 1))
check(conv < 1e-10, f'cube r(u): coefficients agree between quadratures A and B to {conv:.1e}')
nz = [l for l in range(LMAX + 1) if PB[l] > 1e-20]
cubic = [l for l in range(LMAX + 1) if l % 2 == 0 and l not in (2,)]
check(set(nz) <= set(cubic) and 2 not in nz and all(l % 2 == 0 for l in nz), f'cube r(u): nonzero degrees {nz} (cubic only: no l = 2, no odd l)')
# brute-force grid cross-check of the leading coefficients (r sampled by ray casting; non-smooth, so only ~1e-5 expected)
Nt = 600; xg, wg = np.polynomial.legendre.leggauss(Nt); th = np.arccos(xg); ph = (np.arange(2 * Nt) + .5) * np.pi / Nt
TH, PH = np.meshgrid(th, ph, indexing='ij'); Ug = np.c_[(np.sin(TH) * np.cos(PH)).ravel(), (np.sin(TH) * np.sin(PH)).ravel(), np.cos(TH).ravel()]
Wg = np.repeat(wg, 2 * Nt) * (np.pi / Nt); rg = 1 / np.abs(Ug).max(1)
Yg = real_Y(Ug, 8); ag = {l: Yg[l] @ (Wg * rg) for l in (0, 4, 6, 8)}
gd = max(np.abs(ag[l] - aB[l]).max() for l in (0, 4, 6, 8))
check(gd < 1e-4, f'cube: independent grid ({len(Wg)} rays) agrees on l = 0, 4, 6, 8 to {gd:.1e}')
U0 = np.random.default_rng(1).normal(size=(500, 3)); U0 /= np.linalg.norm(U0, axis=1)[:, None]
Ya, Yb = real_Y(U0), real_Y_slow(U0); ydiff = max(np.abs(np.abs(Ya[l]) - np.abs(Yb[l])).max() for l in range(LMAX + 1))
check(ydiff < 1e-11, f'fast real Y_lm recurrence = scipy sph_harm_y up to sign convention: {ydiff:.1e}')
res['cube'] = {'a00': aB[0][0], 'P': PB.tolist(), 'conv': conv, 'grid_diff': gd, 'orth_err': err}
json.dump(res, open(os.path.join(DATA, 'sanity.json'), 'w'), indent=1)
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
