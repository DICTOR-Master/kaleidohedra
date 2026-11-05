# Grow rhombohedra into the gap room of the densest cut-OG lattice packing (DICTO 5 Nov 2026: "use [waves] together with harmonics with
# growing golden or regular rhombi to fill gaps"). (1) Harmonics of the room (radius function from the room centre to the adaptor surface):
# power in l = 4 (cubic tone; zero for icosahedral shapes), l = 6, l = 10. (2) Greedy growth on the gap voxels, darkest wave points first:
# golden rhombohedra (edges along 3 of the cut OG's 6 five-fold axes: prolate and oblate) or regular-rhombus rhombohedra (edges along 3 of
# the 4 body diagonals of one inscribed cube: RD rhombi). Score: share of the gap filled. Float, voxels. Rhombi alone cannot fill it exactly
# (their Dehn invariant is zero, the gap's is not), so the leftover is the true adaptor.
import json, itertools, numpy as np, time, sys
from scipy.special import sph_harm_y
t0 = time.time(); R = "/home/dicto/study-runs/og-pent/cut/data/"
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
def grow(steps, label):
    free = gap.copy(); tally = []
    for fam, shapes, e in steps:
        T = [t for t in (template(E, e) for E in shapes) if len(t) > 3]; placed = 0
        for a in idx[: 80000]:
            if not free[tuple(a)]: continue
            for t in T:
                q = (a + t) % N
                if free[q[:, 0], q[:, 1], q[:, 2]].all(): free[q[:, 0], q[:, 1], q[:, 2]] = False; placed += 1; break
        tally.append(f"{fam[0]}{e:.3f}:{placed}")
        print(f"  {label}: after {fam} edge {e:.3f} -> filled {1 - free.sum()/gap.sum():.3f} ({time.time() - t0:.0f}s)", flush=True)
        if time.time() - t0 > 280: break
    return free
e0 = 0.16
grow([("golden", GOLD, e0/phi**k) for k in range(5)], "golden, growing in phi-steps")
grow([("regular", REG, e0/phi**k) for k in range(5)], "regular, growing in phi-steps")
mix = []
for k in range(5): mix += [("golden", GOLD, e0/phi**k), ("regular", REG, e0/phi**k)]
grow(mix, "golden + regular, phi-steps")
print("FINAL ok")
