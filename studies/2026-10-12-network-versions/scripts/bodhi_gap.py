# Bodhi seed (DICTO 2026-10-12): RT(phi^2) holding 12 RT(1) on its 5-fold axes (each pushed out to touch) and RT(1/phi) at the
# centre. Survey of the gap: contacts between the solids (shared face area), then the gap on a voxel grid split into connected
# pockets; each pocket kind is reported with its count, volume, the axis it sits on, and how convex it is (pocket / its hull).
import itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
exec(open(__file__.replace('bodhi_gap.py', 'network_screen.py')).read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
V = ref['RT']; outer = V * PHI ** 2; centre = V / PHI
def faces(W):
    E = []
    for e in ConvexHull(W).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
FO = faces(outer); I = ref['I']; U5 = I / np.linalg.norm(I, axis=1)[:, None]
copies = []
for u in U5:
    t = min((-f[3] - (V @ f[:3]).max()) / (f[:3] @ u) for f in FO if f[:3] @ u > 1e-9); copies.append(V + t * u)
solids = copies + [centre]; SE = [faces(W) for W in solids]
print(f'copy offset {np.linalg.norm(copies[0].mean(0)):.6f}; volumes: outer {ConvexHull(outer).volume:.6f}, copies {12 * ConvexHull(V).volume:.6f}, centre {ConvexHull(centre).volume:.6f}')
gap = ConvexHull(outer).volume - 12 * ConvexHull(V).volume - ConvexHull(centre).volume; print(f'gap {gap:.6f}')
def contact(A, EA, B):            # number of A's faces that B's points lie flat on (shared plane, B outside)
    n = 0
    for e in EA:
        on = np.abs(B @ e[:3] + e[3]) < 1e-7
        if on.sum() >= 3 and np.all(B @ e[:3] + e[3] >= -1e-7): n += 1
    return n
nb = [contact(copies[0], SE[0], copies[j]) for j in range(1, 12)]
print('copy 0 shares face planes with neighbours:', nb, '; with centre:', contact(copies[0], SE[0], centre), '; corners on outer faces:',
      int(sum(np.any(np.abs(FO[:, :3] @ v + FO[:, 3]) < 1e-7) for v in copies[0])))
R = np.linalg.norm(outer, axis=1).max(); n = 260
g = np.linspace(-R, R, n); h = g[1] - g[0]
X = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
m = np.all(X @ FO[:, :3].T + FO[:, 3] < 0, axis=1)
for E in SE: m &= ~np.all(X @ E[:, :3].T + E[:, 3] <= 0, axis=1)
lab, k = ndimage.label(m.reshape(n, n, n))
print(f'gap on grid {m.sum() * h ** 3:.3f}; pockets {k}')
L = lab.reshape(-1); kinds = {}
I5, D3, ID2 = U5, ref['D'] / np.linalg.norm(ref['D'], axis=1)[:, None], ref['ID'] / np.linalg.norm(ref['ID'], axis=1)[:, None]
for i in range(1, k + 1):
    P = X[L == i]
    if len(P) < 20: continue
    c = P.mean(0); d = c / (np.linalg.norm(c) + 1e-12)
    ax = max((('5-fold', (I5 @ d).max()), ('3-fold', (D3 @ d).max()), ('2-fold', (ID2 @ d).max())), key=lambda t: t[1])
    vol = len(P) * h ** 3; hv = ConvexHull(P).volume if len(P) > 4 else 0
    key = (round(vol, 1), ax[0] if ax[1] > 0.999 else 'off-axis', round(np.linalg.norm(c), 2))
    kinds.setdefault(key, []).append(vol / hv if hv else 0)
for (vol, ax, r), L_ in sorted(kinds.items(), key=lambda t: t[0][2]):
    print(f'  {len(L_):3d} pockets, volume ~{vol}, on the {ax} axis at radius {r}, filled share of own hull {np.mean(L_):.2f}')
