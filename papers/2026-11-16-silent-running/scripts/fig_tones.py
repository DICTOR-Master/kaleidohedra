#!/usr/bin/env python3
"""Tones T_1 .. T_20 of the point sets drawn in the lofargram (Figure 1) and the silence-signature chart (Figure 6).
No new sets: every set is one already in the paper, the golden-A4 study, the law-giving census (its Wythoff members and
their t = 2 neighbours) or the twisted-silence groups study. Tones are computed in floating point (drawing only); every
zero pattern is asserted against the exact signatures stated in those studies, so a wrong set or a wrong dimension fails.

T_k(S) = |S|^-2 sum_{x,y} G_k(<x,y>) / G_k(1), G_k the Gegenbauer polynomial of the sphere S^(n-1), n = dimension spanned.
Usage: fig_tones.py out.json    (ends FINAL ok / FINAL FAIL)
"""
import sys, json, itertools
import numpy as np
from scipy.special import eval_gegenbauer, eval_legendre

KMAX = 20; ZERO = 1e-10
PHI = (1 + 5 ** 0.5) / 2
fails = []
def check(ok, msg):
    print(('CHECK ok   ' if ok else 'CHECK FAIL ') + msg, flush=True)
    if not ok: fails.append(msg)

def uniq(P, d=9):
    seen, out = set(), []
    for p in P:
        key = tuple(np.round(p, d) + 0.0)
        if key not in seen: seen.add(key); out.append(p)
    return np.array(out)

def centred_unit(P):
    P = np.array(P, float); P = P - P.mean(0) if P.shape[1] == 5 else P
    return P / np.linalg.norm(P, axis=1)[:, None]

def tones(P, n=None):
    P = np.array(P, float)
    if n is None: n = np.linalg.matrix_rank(P, tol=1e-9)   # the sphere's dimension: spanned (4 for the sum-zero 5-cell sets), or given (S^3 for 2I classes)
    G = np.clip(P @ P.T, -1, 1); out = []
    for k in range(1, KMAX + 1):
        if n == 3: g = eval_legendre(k, G); g1 = 1.0
        else: lam = (n - 2) / 2; g = eval_gegenbauer(k, lam, G); g1 = eval_gegenbauer(k, lam, 1.0)
        out.append(float(g.sum() / g1 / len(P) ** 2))
    return n, out

def silent(T): return [k + 1 for k, t in enumerate(T) if abs(t) < ZERO]

def perms(v): return uniq([np.array(p, float) for p in itertools.permutations(v)])

def signed_perms(v):
    out = []
    for p in itertools.permutations(v):
        for s in itertools.product((1, -1), repeat=len(v)): out.append(np.array(p, float) * s)
    return uniq(out)

def wythoff(roots, c):
    """orbit of v = sum c_j w_j (w dual to the UNIT simple roots, so edge lengths are 2 c_j, as in the census) under the reflections"""
    A = np.array([r / np.linalg.norm(r) for r in roots]); v = np.linalg.lstsq(A, np.array(c, float), rcond=None)[0]   # minimal-norm: v in the span of the roots
    orb, frontier = [v], [v]
    seen = {tuple(np.round(v, 9))}
    while frontier:
        new = []
        for p in frontier:
            for a in A:
                q = p - 2 * (p @ a) * a; key = tuple(np.round(q, 9) + 0.0)
                if key not in seen: seen.add(key); orb.append(q); new.append(q)
        frontier = new
    return np.array(orb)

e = np.eye(5)
A4 = [e[0] - e[1], e[1] - e[2], e[2] - e[3], e[3] - e[4]]
E3 = np.eye(3); B3 = [E3[0] - E3[1], E3[1] - E3[2], E3[2]]
E4 = np.eye(4); F4 = [E4[1] - E4[2], E4[2] - E4[3], E4[3], 0.5 * (E4[0] - E4[1] - E4[2] - E4[3])]
D4 = [E4[0] - E4[1], E4[1] - E4[2], E4[2] - E4[3], E4[2] + E4[3]]     # a, b (centre), c, d
A3 = [e[0][:4] - e[1][:4], e[1][:4] - e[2][:4], e[2][:4] - e[3][:4]]

# ---------------------------------------------------------------- the 600-cell and its five S5-orbits (sum-zero R^5)
X = centred_unit(perms((PHI**2, PHI**2, PHI**2, PHI, 0)))
F = centred_unit(perms((PHI**2, PHI**2, 1, 1, 0)))
R = centred_unit(perms((1, -1, 0, 0, 0)))
P600 = np.vstack([X, -X, R, F, -F])
G = P600 @ P600.T
check(len(X) == 20 and len(F) == 30 and len(R) == 20 and len(uniq(P600)) == 120, '120 distinct corners: 20 + 20 + 20 + 30 + 30')
allowed = np.array([0, .5, -.5, PHI / 2, -PHI / 2, 1 / (2 * PHI), -1 / (2 * PHI), 1, -1])
check(np.abs(G[..., None] - allowed).min(-1).max() < 1e-12, 'every cosine is a 600-cell cosine {0, ±1/2, ±φ/2, ±1/(2φ), ±1}')
check(all(np.sum(np.abs(G[i] - PHI / 2) < 1e-9) == 12 for i in range(120)), 'every corner has 12 nearest neighbours (cosine φ/2)')

sets = {}
def add(key, P, expect=None, note='', n=None):
    n, T = tones(P, n); s = silent(T); sets[key] = {'n_points': len(P), 'dim': int(n), 'T': T, 'silent': s, 'note': note}
    if expect is not None: check(s == expect, f'{key}: silent {s} (expected {expect})')
    else: print(f'INFO {key}: {len(P)} points, silent {s}', flush=True)
    return s

odd = [k for k in range(1, KMAX + 1) if k % 2]
# lofargram rows
add('ctrl-X (3,3,3,2,0)', centred_unit(perms((3, 3, 3, 2, 0))), [1, 2], 'X family at t = 2')
add('ctrl-F (3,3,2,2,0)', centred_unit(perms((3, 3, 2, 2, 0))), [1, 2], 'F family at t = 2')
add('X', X, [1, 2, 5, 7]); add('-X', -X, [1, 2, 5, 7])
add('F', F, [1, 2, 3, 6]); add('-F', -F, [1, 2, 3, 6])
add('R', R, sorted(set(odd) | {2}))
add('600-cell', P600, [k for k in range(1, 20) if k != 12])

# census members (law-giving census table, section 4) and their t = 2 neighbours on the same family
def both(key, roots, c_member, c_nb, expect=None):
    s = add(key, centred_unit(wythoff(roots, c_member)), expect)
    sn = add(key + ' | t=2', centred_unit(wythoff(roots, c_nb)))
    sets[key]['neighbour_silent'] = sn
both('cuboctahedron (A3 x3o3t, t=1)', A3, (1, 0, 1), (1, 0, 2), sorted(set(odd) | {2}))
both('bitruncated 5-cell (A4 o3x3t3o, t=1)', A4, (0, 1, 1, 0), (0, 1, 2, 0), sorted(set(odd) | {2}))
both('runcinated 5-cell = R (A4 x3o3o3t, t=1)', A4, (1, 0, 0, 1), (1, 0, 0, 2), sorted(set(odd) | {2}))
both('omnitruncated 5-cell (A4 x3x3x3t, t=1)', A4, (1, 1, 1, 1), (1, 1, 1, 2))
both('bitruncated 24-cell (F4 o3x4t3o, t=1)', F4, (0, 1, 1, 0), (0, 1, 2, 0))
both('runcinated 24-cell (F4 x3o4o3t, t=1)', F4, (1, 0, 0, 1), (1, 0, 0, 2))
both('omnitruncated 24-cell (F4 x3x4x3t, t=1)', F4, (1, 1, 1, 1), (1, 1, 1, 2))
both('Icosaxes (B3 x3t4o, t=φ)', B3, (1, PHI, 0), (1, 2, 0))
both('Kelvin truncated octahedron (B3 x3t4o, t=1)', B3, (1, 1, 0), (1, 2, 0))
both('D4 o3o3x *b3x (t=1)', D4, (0, 0, 1, 1), (0, 0, 1, 2))
for k in ['bitruncated 24-cell (F4 o3x4t3o, t=1)', 'runcinated 24-cell (F4 x3o4o3t, t=1)', 'omnitruncated 24-cell (F4 x3x4x3t, t=1)']:
    check(6 in sets[k]['silent'] and 14 in sets[k]['silent'], f'{k}: T6 = T14 = 0 (census rows 7-10)')
check({4, 8, 14} <= set(sets['Icosaxes (B3 x3t4o, t=φ)']['silent']) and not {6, 10, 12} & set(sets['Icosaxes (B3 x3t4o, t=φ)']['silent']),
      'Icosaxes: T4 = T8 = T14 = 0, T6, T10, T12 nonzero (census row 13)')
check(len(wythoff(B3, (1, PHI, 0))) == 24, 'Icosaxes has 24 corners')
# the 24-cell on the tesseract-16-cell line (mu = 2) and a neighbour (mu = 2.5); the turn's fixed point on the cube-octahedron line
s24 = add('24-cell (tesseract-16-cell line, μ=2)', centred_unit(signed_perms((1, 1, 0, 0))))
sets['24-cell (tesseract-16-cell line, μ=2)']['neighbour_silent'] = add('24-cell | μ=2.5', centred_unit(signed_perms((1, 1, .5, 0))))
check(s24[:5] == [1, 2, 3, 4, 5], '24-cell is a 5-design')
m = 3 ** 0.5
add('turn fixed point (cube-octahedron line, μ=√3)', centred_unit(signed_perms((1, m - 1, 0))))
sets['turn fixed point (cube-octahedron line, μ=√3)']['neighbour_silent'] = add('turn | μ=1.5', centred_unit(signed_perms((1, .5, 0))))
check(len(signed_perms((1, m - 1, 0))) == 24, 'turn member: 24 corners (truncated octahedron)')
# ordinary classes of 2I (latitude slices of the 600-cell as the group 2I, quaternion order w, x, y, z)
def quat_600():
    Q = [np.array(v, float) for v in itertools.product(*[(1, -1)] * 4)]; Q = [q / 2 for q in Q]
    for i in range(4):
        for s in (1, -1): v = np.zeros(4); v[i] = s; Q.append(v)
    base = (0, 1, 1 / PHI, PHI)
    for p in itertools.permutations(range(4)):
        if np.linalg.det(np.eye(4)[list(p)]) < 0: continue
        for s in itertools.product((1, -1), repeat=4):
            v = np.array([base[p[i]] for i in range(4)]) * s / 2; Q.append(v)
    return uniq(Q)
Q = quat_600(); check(len(Q) == 120 and np.allclose(np.linalg.norm(Q, axis=1), 1), 'unit icosians: 120')
w = Q[:, 0]
add('2I 12-point class (w = φ/2)', Q[np.abs(w - PHI / 2) < 1e-9], [4], n=4)
add('2I 20-point class (w = 1/2)', Q[np.abs(w - .5) < 1e-9], [2, 5], n=4)
add('2I 30-point class (w = 0)', Q[np.abs(w) < 1e-9], odd, n=4)
json.dump({'kmax': KMAX, 'zero': ZERO, 'sets': sets}, open(sys.argv[1], 'w'), indent=1, ensure_ascii=False)
print(f'{len(sets)} sets; {len(fails)} checks failed', flush=True)
print('FINAL ok' if not fails else 'FINAL FAIL', flush=True)
