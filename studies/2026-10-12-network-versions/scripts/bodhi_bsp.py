# Bodhi seed gap, exact (2026-10-12): cut one fundamental domain of the full icosahedral group (the cone on a 5-, 3- and 2-fold
# axis) inside the outer RT(phi^2) by every face plane of the 13 inner solids; keep the cells outside all solids; split them into
# the two pockets (cells joined across shared faces) and by nearest axis; then rebuild each piece as the union of its cells' images
# under the axis' stabiliser, and report whether it is convex (union volume = hull volume), its corners and faces.
import os, itertools, numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'lotus_analogs.py')).read()
exec(src[:src.index('def lotus(')].replace("__file__.replace('lotus_analogs.py', 'network_screen.py')", repr(os.path.join(HERE, 'network_screen.py'))))
V = ref['RT']; outer = V * PHI ** 2; centre = V / PHI
FO = planes_of(outer); I = ref['I']; U5 = I / np.linalg.norm(I, axis=1)[:, None]; copies = []
for u in U5:
    t = min((-f[3] - (V @ f[:3]).max()) / (f[:3] @ u) for f in FO if f[:3] @ u > 1e-9); copies.append(V + t * u)
solids = [planes_of(c) for c in copies] + [planes_of(centre)]
# fundamental cone
u5 = U5[0]; D = ref['D']; u3 = D[np.argmax(D @ u5)]; u3 = u3 / np.linalg.norm(u3)
ID = ref['ID'] / np.linalg.norm(ref['ID'], axis=1)[:, None]; c2 = ID[np.argsort(-(ID @ u5))]; u2 = [w for w in c2 if w @ u3 > 0.9][0] if any(w @ u3 > 0.9 for w in c2) else c2[0]
cand = sorted(ID, key=lambda w: -(w @ u5 + w @ u3)); u2 = cand[0]
def cone_plane(a, b, c):
    n = np.cross(a, b); n = n / np.linalg.norm(n)
    if n @ c > 0: n = -n                     # plane n.x <= 0 keeps c
    return np.r_[n, 0.0]
cone = [cone_plane(u5, u3, u2), cone_plane(u3, u2, u5), cone_plane(u2, u5, u3)]
cut = []
for P in solids:
    for e in P:
        if not any(np.linalg.norm(e - q) < 1e-7 or np.linalg.norm(e + q) < 1e-7 for q in cut): cut.append(e)
cells = [list(FO) + cone]
for e in cut:
    nxt = []
    for H in cells:
        lo, hi = side_range(H, e)
        if lo < -1e-7 and hi > 1e-7: nxt += [H + [e], H + [-e]]
        else: nxt.append(H)
    cells = nxt
gap = []
for H in cells:
    x, r = interior(H)
    if x is None or r < 1e-9: continue
    if any(inside_poly(x, P) for P in solids): continue
    W = verts(H)
    if W is not None: gap.append(W)
tot = sum(ConvexHull(W).volume for W in gap)
print(f'cells {len(cells)}, gap cells {len(gap)}, volume {tot:.9f} x 120 = {120 * tot:.6f} (gap 70.272181)', flush=True)
# pockets: join cells sharing >= 3 corners
key = lambda v: tuple(np.round(v, 6)); ks = [set(map(key, W)) for W in gap]
par = list(range(len(gap)))
def f(i):
    while par[i] != i: par[i] = par[par[i]]; i = par[i]
    return i
for i, j in itertools.combinations(range(len(gap)), 2):
    if len(ks[i] & ks[j]) >= 3: par[f(i)] = f(j)
G = GROUP
for root in sorted(set(f(i) for i in range(len(gap)))):
    mem = [gap[i] for i in range(len(gap)) if f(i) == root]
    vol = sum(ConvexHull(W).volume for W in mem)
    print(f'\npocket part in the cone: {len(mem)} cells, volume x120 = {120 * vol:.6f}', flush=True)
    for nm, ax, cnt in (('5-fold', u5, 12), ('3-fold', u3, 20), ('2-fold', u2, 30)):
        sel = [W for W in mem if max(((W.mean(0) / np.linalg.norm(W.mean(0))) @ a for a in (u5, u3, u2))) == (W.mean(0) / np.linalg.norm(W.mean(0))) @ ax]
        if not sel: continue
        stab = [g for g in G if np.linalg.norm(g @ ax - ax) < 1e-9]
        pts = np.unique(np.round(np.vstack([W @ g.T for W in sel for g in stab]), 9), axis=0)
        uv = sum(ConvexHull(W).volume for W in sel) * len(stab)
        H = ConvexHull(pts); hv = H.volume; cv = pts[H.vertices]
        fp = planes_of(cv); fs = []
        for e in fp: fs.append(int(np.sum(np.abs(cv @ e[:3] + e[3]) < 1e-7)))
        print(f'  {nm} piece (x{cnt}): volume {uv:.6f}, hull {hv:.6f}, convex {abs(uv - hv) < 1e-6}; {len(cv)} corners, faces {sorted(fs)}', flush=True)
        np.save(os.path.join(HERE, f'../data/bodhi-{root}-{nm}.npy'), cv)
