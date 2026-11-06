"""Football scutoid study, step 2b (DICTO 11-06/11-07: "go ahead with football 2b"). Cut the space of the stacked football crystal
(stack_layers.py: grid layer, gap 0.6, layer spacing h, shift (a, b)) into one cell per ball: every point goes to the nearest body, where a
body is a ball plus the half of each bridge attached to it (nearest-surface cells, Euclidean, from dense surface samples).
Then slice parallel to the layers and record, at each height, which cells touch (shared boundary of at least MINLEN pixels).
A NEIGHBOUR SWAP (the scutoid move) = two cells that both appear in the slices both below and above, touching on one side and not on the
other while a different pair takes over the contact. Cells entering or leaving the slice (the layer above or below) are counted apart.
Numerical (voxels); a first look, not a proof.  Run: python3 tools/runjob.py <this> <data file> [voxel]"""
import itertools, sys, numpy as np
from scipy.spatial import cKDTree, ConvexHull
VOX = float(sys.argv[1]) if len(sys.argv) > 1 else 0.10
MINLEN = 3
sys.argv = [sys.argv[0], '0.6']
exec(open('grid_layer.py').read().split('# overlap test')[0].replace('print(', '(lambda *a, **k: None)('))
from football import F
n = np.cross(e1, e2); n /= np.linalg.norm(n)
P1, P2 = 2 * D * e1, D * (e1 + e2)
h, A, B = 3.6224, 0.0, 0.444                    # data-stack.txt
T = h * n + A * P1 + B * P2
M = np.array([P1, P2, T])                        # rows: cell vectors; two balls per cell: (0,0) X and (1,0) Y
def tri_samples(P, step):
    """dense points on a convex polygon P (k x 3, in order) by fan triangles"""
    out = []
    for t in range(1, len(P) - 1):
        a, b, c = P[0], P[t], P[t + 1]
        m = max(2, int(np.ceil(max(np.linalg.norm(b - a), np.linalg.norm(c - a)) / step)) + 1)
        for i in range(m + 1):
            for j in range(m + 1 - i):
                out.append(a + (b - a) * i / m + (c - a) * j / m)
    return np.array(out)
def order(P):
    c = P.mean(0); nn = np.cross(P[1] - P[0], P[2] - P[0]); nn /= np.linalg.norm(nn)
    u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(nn, u)
    return P[np.argsort(np.arctan2((P - c) @ w, (P - c) @ u))]
step = VOX * 0.7
# one ball's surface samples (orientation X and Y), and its bridges' side samples (half nearest that ball)
def body_samples(i, j):
    Vb, R = ball(i, j); c = centre(i, j)
    pts = [tri_samples(order(Vb[idx]), step) for nrm, hh, idx in F]
    for di, dj, d in ((1, 0, e1), (0, 1, e2), (-1, 0, -e1), (0, -1, -e2)):
        k1, f1 = face_toward(i, j, d); k2, f2 = face_toward(i + di, j + dj, -d)
        hull = ConvexHull(np.vstack([f1, f2])); allp = np.vstack([f1, f2])
        for s in hull.simplices:                  # side triangles of the bridge (skip the two end faces)
            tri = allp[s]
            if np.allclose((tri - c) @ d, ((f1 - c) @ d).mean(), atol=1e-6) or np.allclose((tri - c) @ d, ((f2 - c) @ d).mean(), atol=1e-6): continue
            q = tri_samples(tri, step); mid = c + d * D / 2
            pts.append(q[(q - mid) @ d <= 0])     # this ball's half
    return np.vstack(pts)
S0 = body_samples(0, 0) - centre(0, 0); S1 = body_samples(1, 0) - centre(1, 0)
# all bodies near the analysed region: cells offsets (p, q, r), balls X at p*P1+q*P2+r*T, Y at that + D e1
imgs, pts, lab = [], [], []
for p, q, r in itertools.product(range(-2, 3), range(-2, 3), range(-1, 3)):
    o = p * P1 + q * P2 + r * T
    for kind, (S, c0) in enumerate(((S0, centre(0, 0)), (S1, centre(1, 0)))):
        imgs.append((kind, p, q, r)); pts.append(S + c0 + o); lab.append(np.full(len(S), len(imgs) - 1))
pts = np.vstack(pts); lab = np.concatenate(lab); tree = cKDTree(pts)
print(f"voxel {VOX}; bodies {len(imgs)}; surface samples {len(pts)}; cell |P1| {np.linalg.norm(P1):.3f} |P2| {np.linalg.norm(P2):.3f} h {h}")
# slices: fractional w in [0, 1) (one layer period), in-plane window = 1 cell plus margin
N1, N2 = int(np.linalg.norm(P1) / VOX), int(np.linalg.norm(P2) / VOX); N3 = int(h / VOX)
mg = 0.25
U = np.linspace(-mg, 1 + mg, int(N1 * (1 + 2 * mg))); Vv = np.linspace(-mg, 1 + mg, int(N2 * (1 + 2 * mg)))
contacts = {}; present = {}
def canon(a, b):
    ka, pa, qa, ra = imgs[a]; kb, pb, qb, rb = imgs[b]
    x = (ka, kb, pb - pa, qb - qa, rb - ra); y = (kb, ka, pa - pb, qa - qb, ra - rb)
    return min(x, y)
inside = lambda uu, vv: (uu >= 0) & (uu < 1) & (vv >= 0) & (vv < 1)
for k in range(N3):
    w = (k + 0.5) / N3
    uu, vv = np.meshgrid(U, Vv, indexing='ij')
    X = uu[..., None] * P1 + vv[..., None] * P2 + w * T
    _, idx = tree.query(X.reshape(-1, 3), workers=-1); L = lab[idx].reshape(uu.shape)
    pairs = {}
    for a1, a2, m in ((L[1:], L[:-1], inside(uu[1:], vv[1:])), (L[:, 1:], L[:, :-1], inside(uu[:, 1:], vv[:, 1:]))):
        dif = (a1 != a2) & m
        for x, y in zip(a1[dif], a2[dif]): key = canon(x, y); pairs[key] = pairs.get(key, 0) + 1
    for key, c in pairs.items():
        if c >= MINLEN: contacts.setdefault(key, set()).add(k)
    for b in np.unique(L[inside(uu, vv)]):
        kd, p, q, r = imgs[b]; present.setdefault((kd, r), set()).add(k)   # which ball kinds/layers show in the slice
    if k % 5 == 0: print(f"  slice {k + 1}/{N3} done", flush=True)
print(f"slices {N3} (layer period h = {h}, one slice {h / N3:.3f}); contact pairs found {len(contacts)}")
for key in sorted(contacts, key=lambda k: min(contacts[k])):
    ks = sorted(contacts[key]); ka, kb, dp, dq, dr = key
    print(f"  {'XY'[ka]}-{'XY'[kb]} offset ({dp:+d},{dq:+d},{dr:+d}) layers {'same' if dr == 0 else 'next'}: touch in slices {ks[0]}..{ks[-1]} ({len(ks)} of {N3})" + ("" if len(ks) == ks[-1] - ks[0] + 1 else "  [gaps]"))
# neighbour swaps: for each canonical ball kind, the neighbour set at each slice where both cells are present all through
print("ball layers present per slice range:", {f"{'XY'[a]} r={r}": (min(s), max(s)) for (a, r), s in sorted(present.items())})
swaps = []
same = [k for k in contacts if k[4] == 0]
for k1, k2 in itertools.combinations(same, 2):
    s1, s2 = contacts[k1], contacts[k2]
    if s1 and s2 and not (s1 & s2) and len(s1 | s2) >= N3 - 2: swaps.append((k1, k2))
print(f"same-layer contacts that hand over to another pair through the layer (scutoid move candidates): {len(swaps)}")
for k1, k2 in swaps: print(f"  {k1} slices {min(contacts[k1])}..{max(contacts[k1])}  <->  {k2} slices {min(contacts[k2])}..{max(contacts[k2])}")
print("FINAL ok")
