# Step 23 (DICTO: "run the radius 8-10 boundary vacancy test"; Fable's top recommendation). Reads the exact chorus runs
# (data/chorus-exact-r{8,10}.json and the radius-5 run) and measures the silenced copies (vacancies) against the five wedge
# boundary half-planes: (1) does the vacancy count grow like boundary AREA (R^2, constant density) or like the axis length (R)?
# (2) in each half-plane, coordinates (z along the axis, rho out from the axis): are the distinct spacings in golden ratios?
# Positions are float readouts of the exactly verified sites (labels: float measurement on an exact structure).
import json, sys, numpy as np
phi = (1 + 5 ** .5) / 2
runs = [('5', 'data/chorus-exact-big.json'), ('8', 'data/chorus-exact-r8.json'), ('10', 'data/chorus-exact-r10.json')]
out = []
for tag, fn in runs:
    try: D = json.load(open(fn))
    except FileNotFoundError: continue
    S = np.array(D['silenced']); A = np.array(D.get('all', [])); a5 = np.array(D['a5']); R = D['RAD']
    if 'e1' in D: e1, e2, th0 = np.array(D['e1']), np.array(D['e2']), D['th0']
    else:
        e1 = np.cross(a5, [1, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(a5, e1); th0 = np.radians(59.0)
    def halfplane(X):
        z = X @ a5; th = np.arctan2(X @ e2, X @ e1); rho = np.hypot(X @ e1, X @ e2)
        k = np.round(((th - th0) % (2 * np.pi)) / (2 * np.pi / 5)) % 5          # nearest boundary
        dth = ((th - th0 - k * 2 * np.pi / 5 + np.pi) % (2 * np.pi)) - np.pi
        return z, rho * np.cos(dth), rho * np.sin(dth), k                     # z, distance out along the half-plane, offset off it
    z, u, off, k = halfplane(S)
    out.append(f'--- radius {R}: {len(S)} silenced of {len(A) if len(A) else "?"} sites')
    out.append(f'  offset from nearest boundary half-plane: max {np.abs(off).max():.3f}, median {np.median(np.abs(off)):.3f}')
    core = np.hypot(u, off) < 1.05
    out.append(f'  in the core (within 1.05 of the axis): {int(core.sum())}; on the boundaries outside it: {int((~core).sum())}')
    # growth: count boundary vacancies inside balls of radius r, compare with r^2 (area) and r (line)
    r_all = np.linalg.norm(S, axis=1)
    for r in [x for x in (3, 4, 5, 6, 7, 8, 9, 10) if x <= R - 1]:
        n = int(((r_all < r) & ~core).sum())
        out.append(f'  r<{r}: boundary vacancies {n:4d}   per boundary area (5 half-discs, 5*pi*r^2/2) {n / (5 * np.pi * r * r / 2):.4f}   per r {n / r:.2f}')
    # the pattern in one half-plane (orbits make the five identical): take k == 0 outside the core
    sel = (k == 0) & ~core
    zz, uu = z[sel], u[sel]
    out.append(f'  half-plane 0: {int(sel.sum())} vacancies')
    for name, v in (('z (along the axis)', zz), ('distance out from the axis', uu)):
        vals = np.unique(np.round(v, 4)); gaps = np.unique(np.round(np.diff(vals), 4)); gaps = gaps[gaps > 1e-3]
        out.append(f'  distinct {name}: {len(vals)}; distinct gaps: {list(gaps[:12])}{" ..." if len(gaps) > 12 else ""}')
        if len(gaps) > 1:
            g0 = gaps.min(); rat = gaps / g0
            hits = [f'{x:.4f}' for x in rat if min(abs(x - phi ** n) for n in range(0, 7)) < 2e-3]
            out.append(f'    gap ratios to the smallest: {[round(x, 4) for x in rat[:12]]}; matching powers of phi: {len(hits)}/{len(rat)}')
print('\n'.join(out)); open('data/chorus-boundary.txt', 'w').write('\n'.join(out) + '\n')
