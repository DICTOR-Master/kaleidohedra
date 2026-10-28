# Measured polytypes (DICTO 10-28): is the volume per Si-C pair of the SiC polytypes a straight line in the hexagonality h,
# as the Hexagonality Law (#66) would have it if each layer kept its own share? Data: Kawanishi and Mizoguchi, arXiv 1512.04626,
# Table I (experimental a, c/p with their sources; and their three DFT sets, each self-consistent). Volume per pair = (sqrt3/2) a^2 (c/p).
import numpy as np, json
H = {'2H': 1.0, '4H': 0.5, '15R': 0.4, '6H': 1 / 3, '3C': 0.0}
EXP = {  # (a, c/p) pairs as listed; several sources where given
 '2H': [(3.079, 2.527), (3.076, 2.524)], '4H': [(3.073, 2.513), (3.079, 2.520)], '15R': [(3.080, 2.513)],
 '6H': [(3.080, 2.520), (3.081, 2.520)], '3C': [(3.083, 2.517)]}
DFT = {'GGA': {'2H': (3.091, 2.537), '4H': (3.095, 2.532), '15R': (3.094, 2.532), '6H': (3.095, 2.531), '3C': (3.097, 2.529)},
       'LDA': {'2H': (3.058, 2.509), '4H': (3.061, 2.504), '15R': (3.060, 2.504), '6H': (3.061, 2.504), '3C': (3.063, 2.501)},
       'GGA(vdW)': {'2H': (3.074, 2.529), '4H': (3.076, 2.521), '15R': (3.076, 2.520), '6H': (3.077, 2.519), '3C': (3.079, 2.514)}}
vol = lambda a, cp: np.sqrt(3) / 2 * a * a * cp
def fit(points, label):
    h = np.array([p[0] for p in points]); v = np.array([p[1] for p in points])
    A = np.c_[np.ones_like(h), h]; coef, *_ = np.linalg.lstsq(A, v, rcond=None); res = v - A @ coef
    # rounding of the data: a to 0.001, c/p to 0.001 -> volume uncertainty ~ V*(2*0.0005/a + 0.0005/cp)
    unc = np.array([p[1] * (2 * 0.0005 / p[2] + 0.0005 / p[3]) for p in points])
    print(f'{label:10s} V(h) = {coef[0]:.4f} + {coef[1]:+.4f} h  (A^3 per Si-C pair); residuals {np.round(res, 4)}; max |res| {np.abs(res).max():.4f}; rounding uncertainty ~{unc.mean():.4f}')
    return {'intercept': coef[0], 'slope': coef[1], 'residuals': res.tolist(), 'max_abs_res': float(np.abs(res).max()), 'rounding_unc': float(unc.mean())}
out = {}
pts = [(H[k], vol(a, cp), a, cp) for k, L in EXP.items() for a, cp in L]
out['experiment'] = fit(pts, 'Exp.')
for m, d in DFT.items():
    out[m] = fit([(H[k], vol(a, cp), a, cp) for k, (a, cp) in d.items()], m)
# separately: c/p (layer spacing) and a, which DFT shows move in opposite directions
for m, d in DFT.items():
    hs = np.array([H[k] for k in d]); cp = np.array([d[k][1] for k in d]); a = np.array([d[k][0] for k in d])
    for nm, y in (('c/p', cp), ('a', a)):
        c = np.polyfit(hs, y, 1); r = y - np.polyval(c, hs); print(f'   {m:9s} {nm:3s}: slope {c[0]:+.4f}, max |res| {np.abs(r).max():.4f}')
json.dump(out, open('sic_linear.json', 'w'), indent=1)
