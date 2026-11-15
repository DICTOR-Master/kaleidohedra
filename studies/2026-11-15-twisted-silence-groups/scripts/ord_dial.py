"""Control for 'Turning the dial': ORDINARY (untwisted) classes of 2I on S^3 as the base point moves.
The conjugation action fixes the real part w, so orbits are latitude slices x = (w, sqrt(1-w^2) n), n on S^2, with the icosahedral
orbit of n.  Dial: w in [-1, 1] (fine grid) for n on the three special axes (vertex, face, edge directions: 12, 20, 30 points)
and for 3 generic n; each degree k <= KMAX: F_k(w) = sum_g U_k(<g x g^-1, x>) >= 0; zeros located as near-zero local minima,
refined by golden-section search, and a degree is called silent there if F_k / |O| < TOL.  Numerical (floats), a control only.
Expected: single silences along the dial (latitude zeros), several degrees together only at w = 0 (equator, antipodal slice:
all odd degrees) and at the group points themselves."""
import sys, itertools
import numpy as np
KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
TOL = 1e-9
phi = (1 + 5 ** 0.5) / 2
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0: out.append([v[p[i]] for i in range(4)])
    return out
G = set()
for i in range(4):
    for s in (1, -1):
        e = [0.0] * 4; e[i] = s; G.add(tuple(e))
for sg in itertools.product((1, -1), repeat=4): G.add(tuple(0.5 * t for t in sg))
for v in even_perms([phi / 2, 0.5, 1 / (2 * phi), 0.0]):
    for sg in itertools.product((1, -1), repeat=4): G.add(tuple(round(a * b, 12) + 0.0 for a, b in zip(v, sg)))
G = np.array(sorted(G)); assert len(G) == 120, len(G)
def rot(q):                                   # matrix of v -> q v q^-1 on pure quaternions
    w, x, y, z = q
    return np.array([[1 - 2*(y*y + z*z), 2*(x*y - w*z), 2*(x*z + w*y)], [2*(x*y + w*z), 1 - 2*(x*x + z*z), 2*(y*z - w*x)],
                     [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*(x*x + y*y)]])
R = np.array([rot(q) for q in G])
def F(w, n, k):
    c = w * w + (1 - w * w) * (R @ n) @ n           # <g x g^-1, x> for all 120 g
    u0, u1 = np.ones_like(c), 2 * c
    for _ in range(k - 1): u0, u1 = u1, 2 * c * u1 - u0
    return (u1 if k >= 1 else u0).sum() / 120
axes = {'vertex axis (12)': np.array([0, 1, phi]), 'face axis (20)': np.array([1, 1, 1]), 'edge axis (30)': np.array([0, 0, 1.0])}
rng = np.random.default_rng(3)
for i in range(3): axes[f'generic n #{i+1}'] = rng.normal(size=3)
ws = np.linspace(-1, 1, 4001)
print(f'PROGRESS 0.00 ordinary dial, k <= {KMAX}', flush=True)
for ai, (nm, n) in enumerate(axes.items()):
    n = n / np.linalg.norm(n)
    hits = {}
    for k in range(1, KMAX + 1):
        f = np.array([F(w, n, k) for w in ws])
        if np.all(np.abs(f) < TOL):
            hits.setdefault('ALL w', []).append(k); continue
        for j in range(1, len(ws) - 1):
            if f[j] <= f[j - 1] and f[j] <= f[j + 1] and f[j] < 1e-2:
                a, b = ws[j - 1], ws[j + 1]
                for _ in range(80):
                    m1, m2 = a + (b - a) * 0.382, a + (b - a) * 0.618
                    if F(m1, n, k) < F(m2, n, k): b = m2
                    else: a = m1
                wz = (a + b) / 2
                if F(wz, n, k) < TOL: hits.setdefault(round(wz, 6), []).append(k)
    multi = {w: ks for w, ks in hits.items() if w != 'ALL w' and len(ks) >= 2}
    single = sum(1 for w, ks in hits.items() if w != 'ALL w' and len(ks) == 1)
    print(f'{nm}: degrees silent for every w: {hits.get("ALL w", [])}; {single} single-silent latitudes; multi-silent latitudes: '
          + '; '.join(f'w={w}: {ks}' for w, ks in sorted(multi.items())), flush=True)
    print(f'PROGRESS {(ai+1)/len(axes):.2f} {nm}', flush=True)
# control: the ordinary 12-class (vertex axis, w = phi/2) kills exactly degree 4 among k <= KMAX (golden A4 study, section 3C)
ctl = [k for k in range(1, KMAX + 1) if F(phi / 2, axes['vertex axis (12)'] / np.linalg.norm(axes['vertex axis (12)']), k) < TOL]
print('control: 12-class at w = phi/2 kills', ctl)
print('FINAL ok' if ctl == [4] else 'FINAL FAIL')
