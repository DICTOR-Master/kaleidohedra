#!/usr/bin/env python3
"""Controls for the silent-coincidence study.
(1) Independent tone formula: T_k(v) = (1/N) sum_q Z_k(<v, q>)/Z_k(1) over the float orbit (Legendre P_k in 3D, Chebyshev U_k in 4D),
    at a random interior seed of each group: T_k must be ~0 exactly in the degrees with no invariant harmonic and clearly > 0 in the
    others (this checks the list of possible degrees).
(2) The silent zonohedron (B3, c = (1, 1, t)): T_4 = 0 at t = sqrt2 a*, a* = -1 + sqrt(1 + sqrt(5/6)), exact.
(3) The Icosaxes (B3, c = (1, t, 0)): T_4 = T_8 = 0 at t = golden ratio, exact (and which further degrees vanish there).
(4) Zonal cross-check at every point listed in data/three-*.json / data/four-*.json if present: T_k ~ 0 in the zero degrees.
Usage: controls.py -> data/controls.json; prints ok/FAIL lines and FINAL ok/FAIL."""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from numpy.polynomial import legendre as LG
from flint import fmpq, fmpq_poly, arb
import sil, symm, three_d as T
import exact as X
from exact import K, E, positive_roots, same_algebraic
FAILS = []; OUT = {}
def check(c, msg):
    print(('ok   ' if c else 'FAIL ') + msg, flush=True)
    if not c: FAILS.append(msg)

def zonal_float(k, d, x):
    if d == 3: return LG.legval(x, [0]*k + [1])
    U0, U1 = np.ones_like(x), 2*x
    if k == 0: return U0
    for _ in range(k - 1): U0, U1 = U1, 2*x*U1 - U0
    return U1

def tones_float(H, c, kmax):
    P = symm.orbit(H, c); d = H.r
    v = P[0]; x = np.clip(P @ v, -1, 1)
    return {k: float(np.mean(zonal_float(k, d, x))/zonal_float(k, d, np.array([1.0]))[0]) for k in range(1, kmax + 1)}, len(P)

def control_degrees():
    rng = np.random.default_rng(3); res = {}
    for g, kmax in [('A3', 30), ('B3', 30), ('H3', 30), ('A4', 24), ('B4', 24), ('D4', 24), ('F4', 24), ('H4', 40)]:
        H = sil.H(g); c = rng.uniform(0.3, 1.0, H.r)
        Tk, N = tones_float(H, c, kmax)
        zero_ok = all(abs(Tk[k]) < 1e-11 for k in range(1, kmax + 1) if not H.dims.get(k, 0))
        pos_ok = all(Tk[k] > 1e-9 for k in range(1, kmax + 1) if H.dims.get(k, 0))
        check(zero_ok and pos_ok, f'{g}: orbit {N}; zonal tones vanish exactly in the degrees without invariant harmonics and are > 0 in '
              f'the {sum(1 for k in range(1, kmax+1) if H.dims.get(k, 0))} degrees with them (k <= {kmax})')
        res[g] = {'seed': c.tolist(), 'orbit': N, 'nonzero_degrees': [k for k in range(1, kmax + 1) if H.dims.get(k, 0)],
                  'min_tone_nonzero_degrees': min(Tk[k] for k in range(1, kmax + 1) if H.dims.get(k, 0)),
                  'max_abs_tone_other_degrees': max([abs(Tk[k]) for k in range(1, kmax + 1) if not H.dims.get(k, 0)] + [0])}
    OUT['degrees'] = res

def control_zonohedron():
    H = sil.H('B3')
    groups, ident = T.line_roots(H, [K(1), K(1), K(0)], [K(0), K(0), K(1)], 30)
    t0 = arb(2).sqrt()*(-1 + (1 + (arb(5)/6).sqrt()).sqrt())
    # t0 is a root of N(t) = (t^4/4 + 2t^2 - 5/6)^2 - 2 t^6 (norm of (t^2/2 + sqrt2 t)^2 - 5/6)
    tq = fmpq_poly([0, 1]); N = (tq**4/4 + 2*tq**2 - fmpq(5, 6))**2 - 2*tq**6
    hit = [g for g in groups if 4 in g['degrees'] and g['root']['x'].overlaps(t0)]
    ok = False
    if hit:
        mp = fmpq_poly([fmpq(q) for q in hit[0]['root']['minpoly']])
        q, r = divmod(N, mp); ok = r == 0
    check(bool(hit) and ok, f'silent zonohedron: on c = (1, 1, t) the tone T4 vanishes at t = sqrt2 a* = {t0.str(20)} '
          f'(certified root ball overlaps, its minimal polynomial divides the norm polynomial of (t^2/2 + sqrt2 t)^2 = 5/6)')
    OUT['zonohedron'] = {'t': t0.str(30), 'degrees_zero_there': hit[0]['degrees'] if hit else None,
                         'minpoly': hit[0]['root']['minpoly'] if hit else None}

def control_icosaxes():
    H = sil.H('B3')
    groups, ident = T.line_roots(H, [K(1), K(0), K(0)], [K(0), K(1), K(0)], 30)
    g = next((g for g in groups if g['root']['minpoly'] == ['-1', '-1', '1']), None)
    check(g is not None and 4 in g['degrees'] and 8 in g['degrees'] and 6 not in g['degrees'],
          f'Icosaxes: on c = (1, t, 0) the tones vanishing exactly at t = golden ratio: {g["degrees"] if g else None} (T4 and T8, not T6)')
    info = symm.explain(H, [1.0, (1 + 5**0.5)/2, 0.0])
    check(any(s['hidden'] and s['suborbit_symmetry_order'] == 120 for s in info['suborbits']),
          'Icosaxes: a sub-orbit of an index-2 subgroup (12 points) has symmetry of order 120 (a regular icosahedron): explained')
    OUT['icosaxes'] = {'degrees_zero': g['degrees'] if g else None, 'symmetry': info}

def control_points():
    res = []
    for fn in sorted(glob.glob(os.path.join(HERE, '..', 'data', 'three-*.json')) + glob.glob(os.path.join(HERE, '..', 'data', 'four-*.json'))):
        d = json.load(open(fn)); H = sil.H(d['group'])
        pts = [p for p in d.get('interior_points', [])] + [p for e in d.get('edges', []) for p in e['points']] \
              + [p for f in d.get('facets', []) for p in f.get('points', [])]
        bad = 0; n = 0
        for p in pts:
            zd = p.get('zero_degrees_exact', p.get('zero_degrees', p.get('degrees')))
            if zd is None or 'seed_c' not in p: continue
            Tk, N = tones_float(H, p['seed_c'], max(H.degrees(24)) if H.name != 'H4' else 40)
            for k, v in Tk.items():
                if not H.dims.get(k, 0): continue
                if (k in zd) != (abs(v) < 1e-9): bad += 1
            n += 1
        check(bad == 0, f'{d["group"]} ({os.path.basename(fn)}): zonal tones agree with the zero degrees at all {n} listed points')
        res.append({'file': os.path.basename(fn), 'points': n, 'disagreements': bad})
    OUT['points'] = res

if __name__ == '__main__':
    control_degrees(); control_zonohedron(); control_icosaxes(); control_points()
    OUT['fails'] = FAILS
    json.dump(OUT, open(os.path.join(HERE, '..', 'data', 'controls.json'), 'w'), indent=1, default=str)
    print('FINAL ok' if not FAILS else 'FINAL FAIL', flush=True)
