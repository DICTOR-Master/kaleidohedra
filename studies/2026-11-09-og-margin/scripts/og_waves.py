# og_waves.py, DICTO 11 Nov 2026 ("can we use resonance or spherical wave tech"): spherical-wave (spherical harmonic) analysis of the
# OG family. f_k(u) = log rho_k(u) (rho = distance O -> boundary of D_k along u), minus its mean; expanded in real spherical harmonics
# up to degree LMAX on 20 000 quasi-uniform rays. Per level: energy E_l = sum_m c_lm^2 per degree, the sign and size of the single
# icosahedral wave at degree 6 (projection onto the I-invariant direction), the decay per hop of each degree, and RESONANCE tests:
# sign flip per hop (corner <-> face swap) and non-decaying degrees. Control: energy outside the icosahedral degrees must be ~0.
# usage: python -u og_waves.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0])
try:
    from scipy.special import sph_harm_y as SH; Y = lambda l, m, th, ph: SH(l, m, th, ph)
except ImportError:
    from scipy.special import sph_harm as SH0; Y = lambda l, m, th, ph: SH0(m, l, ph, th)
LMAX = 30; N = 20000; i = np.arange(N) + .5; z = 1 - 2 * i / N; az = np.pi * (1 + 5 ** .5) * i
U = np.stack([np.sqrt(1 - z * z) * np.cos(az), np.sqrt(1 - z * z) * np.sin(az), z], 1); TH = np.arccos(z); PH = np.mod(az, 2 * np.pi)
B = []; LM = []
for l in range(LMAX + 1):
    for m in range(-l, l + 1):
        y = Y(l, abs(m), TH, PH)
        B.append(np.sqrt(2) * (y.real if m > 0 else y.imag) if m != 0 else y.real) if m != 0 else B.append(y.real); LM.append((l, m))
B = np.array(B).T * np.sqrt(4 * np.pi / N)                              # equal-weight quadrature, orthonormal columns approx
ICO = {0, 6, 10, 12, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30}     # degrees carrying icosahedral (I) invariants
def rho(M, Dd, dirs):
    P = dirs @ M.T; P = np.where(P > 1e-12, P, np.nan); return np.nanmin(Dd[None, :] / P, axis=1)
# icosahedral invariant at degree 6: average the rotated harmonic over the 60 rotations (computed on the rays by symmetrising f)
rows = []; ok = True; prev = None
V = OGf; FF = faces(V)
for k in range(KM + 1):
    M, Dd, cor = FF
    f = np.log(rho(M, Dd, U)); f -= f.mean()
    c, *_ = np.linalg.lstsq(B, f * np.sqrt(4 * np.pi / N), rcond=None)
    E = np.zeros(LMAX + 1)
    for (l, m), cc in zip(LM, c): E[l] += cc * cc
    off = E[[l for l in range(1, LMAX + 1) if l not in ICO]].sum(); tot = E[1:].sum()
    ok &= off < 1e-3 * tot + 1e-14
    c6 = np.array([cc for (l, m), cc in zip(LM, c) if l == 6])
    if k == 0: d6 = c6 / np.linalg.norm(c6)                             # the icosahedral direction at degree 6 (fixed by D_0)
    a6 = float(c6 @ d6)
    row = dict(k=k, E={l: float(E[l]) for l in sorted(ICO) if l}, off_ico=float(off), total=float(tot), a6=a6)
    rows.append(row)
    print(f"k {k:2d}: total wave energy {tot:.3e} | a6 {a6:+.4e} | E6 {E[6]:.2e} E10 {E[10]:.2e} E12 {E[12]:.2e} E15 {E[15]:.2e} E16 {E[16]:.2e} E18 {E[18]:.2e} E20 {E[20]:.2e} | off-icosahedral {off:.1e}", flush=True)
    W = symmetrise(M * Dd[:, None]); FF = faces(W)
json.dump(rows, open(OUTJ, 'w'), indent=1)
a6 = [r['a6'] for r in rows]; flips = sum(1 for a, b in zip(a6, a6[1:]) if a * b < 0)
print('degree-6 wave a6 by level:', [f'{x:+.2e}' for x in a6])
print(f'sign flips of a6 per hop: {flips} of {len(a6) - 1}')
for l in (6, 10, 12, 15, 16, 18):
    e = [r['E'][l] for r in rows]; q = [(e[i + 1] / e[i]) ** .5 for i in range(len(e) - 1) if e[i] > 0]
    print(f'degree {l:2d}: amplitude ratio per hop, last 8: {[round(x, 3) for x in q[-8:]]}')
print('FINAL ok' if ok else 'FINAL FAIL: energy outside the icosahedral degrees (symmetry or quadrature error)')
