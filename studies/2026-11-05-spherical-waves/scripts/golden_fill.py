# Grow rhombohedra into the gap room of the densest cut-OG lattice packing (DICTO 5 Nov 2026: "use [waves] together with harmonics with
# growing golden or regular rhombi to fill gaps"). (1) Harmonics of the room (radius function from the room centre to the adaptor surface):
# power in l = 4 (cubic tone; zero for icosahedral shapes), l = 6, l = 10. (2) Greedy growth on the gap voxels, darkest wave points first:
# golden rhombohedra (edges along 3 of the cut OG's 6 five-fold axes: prolate and oblate) or regular-rhombus rhombohedra (edges along 3 of
# the 4 body diagonals of one inscribed cube: RD rhombi). Score: share of the gap filled. Float, voxels. Rhombi alone cannot fill it exactly
# (their Dehn invariant is zero, the gap's is not), so the leftover is the true adaptor.
import json, itertools, numpy as np, time, sys
from scipy.special import sph_harm_y
t0 = time.time(); R = "~/study-runs/og-pent/cut/data/"
B = np.array(json.load(open(R + "densest.json"))["B"]); O = np.array(json.load(open(R + "network.json"))["ocd"]); O = O - O.mean(0)
W = np.load("lattice-wave.npz"); S, F = W["S"], W["F"]; N = S.shape[0]; Bi = np.linalg.inv(B)
c = B @ np.array([0, .5, .5])
# --- harmonics of the room: radius from c to the nearest solid along each direction (march on the voxel grid)
def solid_at(X):
    q = (np.floor(((X @ Bi.T) % 1.0)*N).astype(int)) % N; return S[q[..., 0], q[..., 1], q[..., 2]] > 0.5
n = 1500; i = np.arange(n) + 0.5; th = np.arccos(1 - 2*i/n); ph = np.pi*(1 + 5**0.5)*i
D = np.c_[np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th)]; ts = np.linspace(0, 1.0, 400)
hit = solid_at(c + ts[None, :, None]*D[:, None, :]); r = np.array([ts[np.argmax(h)] if h.any() else 1.0 for h in hit])
P = {}
for l in range(0, 13):
    a = [np.mean(r*np.conj(sph_harm_y(l, m, th, ph)))*4*np.pi for m in range(-l, l + 1)]; P[l] = float(np.sum(np.abs(a)**2))
tot = sum(P[l] for l in range(1, 13)); print("room harmonics (share of the non-round part): " + ", ".join(f"l={l} {P[l]/tot:.3f}" for l in range(1, 13)), flush=True)
# --- directions in the frame of the cut OG
from scipy.spatial import ConvexHull
H = ConvexHull(O); pl = {}
for eq, s in zip(H.equations, H.simplices): pl.setdefault(tuple(np.round(eq, 5)), set()).update(s)
pent = [np.array(k[:3]) for k, v in pl.items() if len(v) == 5]; ax5 = []
for p in pent:
    if not any(abs(abs(p @ q) - 1) < 1e-3 for q in ax5): ax5.append(p)
hexn = [np.array(k[:3]) for k, v in pl.items() if len(v) == 6]; ax3 = []
for p in hexn:
    if not any(abs(abs(p @ q) - 1) < 1e-3 for q in ax3): ax3.append(p)
cube = next(q for q in itertools.combinations(range(len(ax3)), 4) if all(abs(abs(ax3[a] @ ax3[b]) - 1/3) < 1e-3 for a, b in itertools.combinations(q, 2)))
print("five-fold axes", len(ax5), " three-fold axes", len(ax3), flush=True)
def rhombs(axes):
    out = []
    for tri in itertools.combinations(range(len(axes)), 3):
        for sg in itertools.product((1, -1), repeat=2):
            E = np.array([axes[tri[0]], sg[0]*axes[tri[1]], sg[1]*axes[tri[2]]]); out.append(E)
    return out
GOLD = rhombs(ax5); REG = rhombs([ax3[k] for k in cube])
def template(E, e):
    # voxel index offsets (relative to the anchor voxel) of the rhombohedron with edge vectors e*E rows, corner at the anchor
    Ev = e*E; corners = np.array([sum(Ev[k]*b for k, b in enumerate(bits)) for bits in itertools.product((0, 1), repeat=3)])
    lo, hi = corners.min(0), corners.max(0); h = (B/N)
    ext = np.ceil(np.abs((np.array(list(itertools.product(*zip(lo, hi)))) @ Bi.T)*N)).max(0).astype(int) + 1
    g = np.array(list(itertools.product(*[range(-x, x + 1) for x in ext])))
    X = (g + 0.0) @ (B/N).T; coef = X @ np.linalg.inv(Ev)
    ok = np.all((coef >= 0) & (coef < 1), axis=1); return g[ok]
gap = S < 0.5; order = np.argsort(F[gap])
idx = np.argwhere(gap)[order]
phi = (1 + 5**0.5)/2
from scipy import ndimage
e0 = 0.16; free = gap.copy(); PL = []
for k in range(5):
    e = e0/phi**k; TT = [(E, template(E, e)) for E in GOLD]; TT = [x for x in TT if len(x[1]) > 3]
    for a in idx[: 80000]:
        if not free[tuple(a)]: continue
        for E, t in TT:
            q = (a + t) % N
            if free[q[:, 0], q[:, 1], q[:, 2]].all():
                free[q[:, 0], q[:, 1], q[:, 2]] = False; PL.append((k, ((a + 0.5)/N) @ B.T, e*E)); break
    print(f"step {k+1} edge {e:.3f}: filled {1 - free.sum()/gap.sum():.3f}", flush=True)
# slivers: connected leftover pieces on the periodic grid (merge labels across the faces)
lab, n = ndimage.label(free, structure=np.ones((3, 3, 3)))
par = list(range(n + 1))
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for ax in range(3):
    A1 = np.take(lab, 0, axis=ax); A2 = np.take(lab, N - 1, axis=ax)
    for x, y in zip(A1.ravel(), A2.ravel()):
        if x and y: par[find(x)] = find(y)
root = np.vectorize(find)(lab); root[lab == 0] = 0
ids, cnt = np.unique(root[root > 0], return_counts=True); vox = abs(np.linalg.det(B))/N**3
order = np.argsort(-cnt); cnt = cnt[order]; ids = ids[order]
print(f"leftover {free.sum()*vox:.5f} of the gap {gap.sum()*vox:.5f}; slivers {len(cnt)}; biggest ten (share of leftover): {[round(x/cnt.sum(), 3) for x in cnt[:10]]}", flush=True)
print(f"slivers of 1-2 voxels (grid dust): {int((cnt <= 2).sum())}, holding {cnt[cnt <= 2].sum()/cnt.sum():.3f} of the leftover", flush=True)
# where the big slivers sit: distance from the room centre, nearest window, nearest contact (bond saddles)
Pc = W["pts"]; real = lambda q: ((q + 0.5)/N) @ B.T
img = np.array(list(itertools.product(range(-1, 2), repeat=3)), float) @ B.T
def dmin(x, pts): return min(np.linalg.norm(x - (p + s)) for p in pts for s in img)
wins = [real(p[:3]) for p in Pc if p[3] == 1]; bonds = [real(p[:3]) for p in Pc if p[3] == 2]
big = []
for j in range(min(12, len(ids))):
    vv = np.argwhere(root == ids[j]); X = real(vv.astype(float))
    ref = X[0]; Xu = np.array([min((x + s for s in img), key=lambda y: np.linalg.norm(y - ref)) for x in X]); cen = Xu.mean(0)
    big.append(cen); print(f"   sliver {j+1}: volume {cnt[j]*vox:.5f}, {cnt[j]} voxels; from room centre {dmin(cen, [c]):.3f}, nearest window {dmin(cen, wins):.3f}, nearest contact {dmin(cen, bonds):.3f}", flush=True)
np.savez_compressed("golden-fill.npz", free=free, root=root, ids=ids[:12], c=c, B=B, PL_k=np.array([p[0] for p in PL]), PL_o=np.array([p[1] for p in PL]), PL_E=np.array([p[2] for p in PL]))
print(f"placed {len(PL)}; FINAL ok {time.time() - t0:.0f}s")
