# og_silences.py, DICTO 11 Nov 2026 ("can we use resonance or spherical wave tech" -> "og family has icosahedral so listen for silences").
# The icosahedral symmetry fixes which spherical waves (degrees l) may sound at all: l = 0, 6, 10, 12, 15, 16, 18, 20, 21, 22, 24, ...
# Those are no news. Listen for SILENCES: degrees the symmetry ALLOWS that the OG family leaves (nearly) empty, at one level or at every
# level, and moments when an allowed wave passes through zero between hops. f_k = log rho_k - mean (rho = distance O -> boundary of D_k
# along a ray), real spherical harmonics to degree 40 on 30 000 rays. Silence score of an allowed degree = its energy / the median energy
# of the allowed degrees at that level. Control: energy at forbidden degrees ~ 0 (symmetry + quadrature).
# usage: python -u og_silences.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0])
from scipy.special import sph_harm_y
LMAX = 40; N = 30000; i = np.arange(N) + .5; z = 1 - 2 * i / N; az = np.pi * (1 + 5 ** .5) * i
U = np.stack([np.sqrt(1 - z * z) * np.cos(az), np.sqrt(1 - z * z) * np.sin(az), z], 1); TH = np.arccos(z); PH = np.mod(az, 2 * np.pi)
cols = []; LS = []
for l in range(LMAX + 1):
    for m in range(0, l + 1):
        y = sph_harm_y(l, m, TH, PH)
        cols.append(y.real); LS.append(l)
        if m: cols.append(y.imag); LS.append(l)
B = np.array(cols).T; LS = np.array(LS)
# allowed degrees for the rotation group I: multiplicity of the trivial rep = (1/60) sum_g chi_l(g)
def mult(l):
    tot = 0
    for g in Gf:
        a = np.arccos(np.clip((np.trace(g) - 1) / 2, -1, 1))
        tot += (2 * l + 1) if a < 1e-9 else np.sin((l + .5) * a) / np.sin(a / 2)
    return int(round(tot / 60))
MULT = {l: mult(l) for l in range(LMAX + 1)}; ALLOWED = [l for l in range(1, LMAX + 1) if MULT[l] > 0]
print('allowed degrees (multiplicity):', {l: MULT[l] for l in ALLOWED}, flush=True)
def rho(M, Dd, dirs):
    P = dirs @ M.T; P = np.where(P > 1e-12, P, np.nan); return np.nanmin(Dd[None, :] / P, axis=1)
rows = []; ok = True; V = OGf; FF = faces(V); prevc = None
for k in range(KM + 1):
    M, Dd, cor = FF
    f = np.log(rho(M, Dd, U)); f -= f.mean()
    c, *_ = np.linalg.lstsq(B, f, rcond=None)
    E = np.array([float((c[LS == l] ** 2).sum()) for l in range(LMAX + 1)])
    forb = E[[l for l in range(1, LMAX + 1) if MULT[l] == 0]].sum(); allw = E[ALLOWED].sum()
    ok &= forb < 1e-4 * allw
    med = np.median(E[ALLOWED]); score = {l: E[l] / med for l in ALLOWED}
    silent = [l for l in ALLOWED if score[l] < 1e-3]
    zero_cross = []
    if prevc is not None:
        for l in ALLOWED:
            a, b = prevc[LS == l], c[LS == l]
            if np.linalg.norm(a) > 0 and np.linalg.norm(b) > 0 and (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)) < -0.9: zero_cross.append(l)
    rows.append(dict(k=k, E={l: float(E[l]) for l in ALLOWED}, score={l: float(score[l]) for l in ALLOWED}, silent=silent, flips=zero_cross, forbidden=float(forb), allowed=float(allw)))
    quiet = sorted(ALLOWED, key=lambda l: score[l])[:4]
    print(f"k {k:2d}: SILENT (allowed, < 1e-3 of median) {silent} | quietest {[(l, f'{score[l]:.1e}') for l in quiet]} | waves flipping sign since last hop {zero_cross} | forbidden energy {forb / allw:.1e}", flush=True)
    prevc = c; W = symmetrise(M * Dd[:, None]); FF = faces(W)
json.dump(rows, open(OUTJ, 'w'), indent=1)
always = [l for l in ALLOWED if all(l in r['silent'] for r in rows[1:])]
often = {l: sum(1 for r in rows if l in r['silent']) for l in ALLOWED}
print('silent at EVERY level k >= 1:', always)
print('levels silent per degree:', {l: v for l, v in often.items() if v})
print('FINAL ok' if ok else 'FINAL FAIL: energy at forbidden degrees (symmetry or quadrature error)')
