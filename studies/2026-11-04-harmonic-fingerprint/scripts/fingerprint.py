#!/usr/bin/env python3
"""Harmonic fingerprint (Concordance 5.5 test, DICTO 4 Nov 2026): Steinhardt-Nelson-Ronchetti bond-orientational invariants of a solid's
corner directions, Q_l = sqrt(4pi/(2l+1) sum_m |mean Y_lm|^2) and W_l-hat, for l = 4, 6, 8, 10, 12.
Validation: fcc (CO) Q4 .191 Q6 .575; hcp (J27) .097/.485; bcc (14) .036/.511; icosahedron Q4 0, Q6 .663 (classical values).
Then the sweep P_mu = C ∩ mu C* (C = [-1,1]^3) from the octahedron (mu = 1) to the cube (mu = 3), with its named stations,
looking for where Q4 vanishes or Q6 peaks. Run with ~/geom/bin/python on dicto-big-brother. Output data/fingerprint.json + log."""
import itertools, json, math, os
import numpy as np
from scipy.special import sph_harm_y
from sympy.physics.wigner import wigner_3j

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'); os.makedirs(OUT, exist_ok=True)
phi = (1 + 5**.5) / 2
LS = (4, 6, 8, 10, 12)

def perms(v, signs=True):
    out = set()
    for p in itertools.permutations(v):
        for s in itertools.product((1, -1), repeat=3):
            out.add(tuple(round(a*b, 12) for a, b in zip(p, s)))
    return np.array(sorted(out))
def cyc(v):
    out = set()
    for k in range(3):
        p = v[k:] + v[:k]
        for s in itertools.product((1, -1), repeat=3):
            out.add(tuple(round(a*b, 12) for a, b in zip(p, s)))
    return np.array(sorted(out))

W3J = {}
def fingerprint(P):
    P = np.array(P, float); P = P[np.linalg.norm(P, axis=1) > 1e-12]
    u = P / np.linalg.norm(P, axis=1)[:, None]
    th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    out = {}
    for l in LS:
        q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l+1)])
        s = np.sum(np.abs(q)**2)
        Q = math.sqrt(4*math.pi/(2*l+1) * s)
        if l not in W3J:
            W3J[l] = [(m1, m2, -m1-m2, float(wigner_3j(l, l, l, m1, m2, -m1-m2))) for m1 in range(-l, l+1) for m2 in range(-l, l+1) if abs(m1+m2) <= l]
        w = sum(c * q[m1+l] * q[m2+l] * q[m3+l] for m1, m2, m3, c in W3J[l])
        out[l] = (round(Q, 4), round(float(np.real(w)) / s**1.5, 4) if s > 1e-14 else 0.0)
    return out

def sweep(mu):
    if mu <= 2: return perms((1, mu - 1, 0)) if mu > 1 else perms((1, 0, 0))
    return perms((1, 1, mu - 2))

J27 = []  # hcp shell: 6 in plane, 3 above, 3 directly below
for k in range(6): J27.append((math.cos(k*math.pi/3), math.sin(k*math.pi/3), 0))
for k in range(3):
    a = math.pi/6 + k*2*math.pi/3; e = math.atan(math.sqrt(2))
    for s in (1, -1): J27.append((math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), s*math.sin(e)))
solids = {
    'Dodecahedron': np.vstack([perms((1, 1, 1)), cyc([0, 1/phi, phi])]),
    'Icosahedron': cyc([0, 1, phi]),
    'Cube': perms((1, 1, 1)),
    'Tetrahedron': np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]),
    'Octahedron': perms((1, 0, 0)),
    'Cuboctahedron (fcc shell)': perms((1, 1, 0)),
    'Anticuboctahedron J27 (hcp shell)': np.array(J27),
    'bcc shell (cube + octahedron, 14)': np.vstack([perms((1, 1, 1)) / math.sqrt(3), perms((1, 0, 0)) * 2/math.sqrt(3)]),
    'Rhombic dodecahedron': np.vstack([perms((1, 1, 1)), perms((2, 0, 0))]),
    'Icosidodecahedron': np.vstack([perms((phi, 0, 0)), cyc([0.5, phi/2, phi**2/2])]),
    'Rhombic triacontahedron': np.vstack([perms((1, 1, 1)), cyc([0, 1/phi, phi]), cyc([0, 1, phi])]),
}
mu_G = 4 + 1.5*2**.5 - 5**.5 - 0.5*10**.5
mu_L = 4 - 1.5*2**.5 + 5**.5 - 0.5*10**.5
stations = {'Unborn Axes (3 − φ)': 3 - phi, 'Kelvin (3/2)': 1.5, 'Icosaxes (φ)': phi, 'cuboctahedron (2)': 2.0,
            'Greater Golden Cut Cube (μ_G)': mu_G, 'Lesser Golden Cut Cube (μ_L)': mu_L, 'truncated cube (2 + 1/(1+√2)·…)': 2 + (2**.5 - 1)}
log = []
def show(name, f):
    s = f'{name:42s} ' + '  '.join(f'Q{l} {f[l][0]:.3f}' for l in LS) + f'   W6^ {f[6][1]:+.4f}'
    print(s); log.append(s)
res = {'solids': {}, 'stations': {}, 'sweep': []}
for n, P in solids.items():
    f = fingerprint(P); res['solids'][n] = f; show(n, f)
print(); log.append('')
for n, mu in stations.items():
    f = fingerprint(sweep(mu)); res['stations'][n] = {'mu': mu, 'fp': f}; show(f'{n} μ={mu:.4f}', f)
# fine sweep: zeros of Q4 and extremes of Q6
grid = np.linspace(1.0005, 2.9995, 4001)
vals = [(mu, fingerprint(sweep(mu))) for mu in grid]
res['sweep'] = [(round(mu, 4), f[4][0], f[6][0]) for mu, f in vals[::40]]
q4 = np.array([f[4][0] for _, f in vals]); q6 = np.array([f[6][0] for _, f in vals])
i4 = np.argsort(q4)[:3]; i6 = np.argmax(q6)
print(); print('smallest Q4 along the sweep:', [(round(grid[i], 4), round(q4[i], 4)) for i in sorted(i4)])
print('largest Q6 along the sweep:', round(grid[i6], 4), round(q6[i6], 4))
log += ['smallest Q4: ' + str([(round(grid[i], 4), round(q4[i], 4)) for i in sorted(i4)]), f'largest Q6: {grid[i6]:.4f} {q6[i6]:.4f}']
json.dump(res, open(os.path.join(OUT, 'fingerprint.json'), 'w'), indent=1, default=str)
open(os.path.join(OUT, 'fingerprint.log'), 'w').write('\n'.join(log) + '\n')
