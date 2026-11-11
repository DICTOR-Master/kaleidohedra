# One coherent golden grain (DICTO 5 Nov 2026, "keep going"): rhombohedra cut from ONE icosahedral rhombohedral tiling (de Bruijn dual grid,
# star = the cut OG's six five-fold axes), keeping every tile wholly inside the gap of the densest cut-OG lattice packing. No grain
# boundaries by construction. The tiling is not periodic, so rooms differ: fill measured for several rooms. Disjointness of a tile from a
# cut OG: separating plane among the cut OG's faces or the tile's faces (edge-edge cases, rare and tiny, ignored: float screen).
import json, itertools, numpy as np, time, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
t0 = time.time(); R = "~/study-runs/og-pent/cut/data/"
B = np.array(json.load(open(R + "densest.json"))["B"]); O = np.array(json.load(open(R + "network.json"))["ocd"]); O = O - O.mean(0)
H = ConvexHull(O); EQ = []
for e in H.equations:
    if not any(np.allclose(e, q, atol=1e-6) for q in EQ): EQ.append(e)
EQ = np.array(EQ); pl = {}
for eq, s in zip(H.equations, H.simplices): pl.setdefault(tuple(np.round(eq, 4)), set()).update(s)
ax5 = []
for k, v in pl.items():
    if len(v) == 5:
        p = np.array(k[:3]); p /= np.linalg.norm(p)
        if not any(abs(abs(p @ q) - 1) < 1e-3 for q in ax5): ax5.append(p)
E6 = np.array(ax5); assert len(E6) == 6
print("sum e e^T =", np.round(E6.T @ E6, 6).tolist(), flush=True)
cell = abs(np.linalg.det(B)); VOG = H.volume; GAP = cell - VOG
L = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3) if any(m)]
def room(c):
    hs = np.array([np.r_[v, -(v @ (c + v/2))] for v in L]); return hs, HalfspaceIntersection(hs, c).intersections
def tiles(s, gam, lo, hi):
    a = s/2; out = []
    for i, j, k in itertools.combinations(range(6), 3):
        Ei = E6[[i, j, k]]; Minv = np.linalg.inv(Ei)
        corners = np.array(list(itertools.product(*zip(lo, hi))))
        rng = [(int(np.floor((corners @ E6[m]).min()/s - gam[m])) - 1, int(np.ceil((corners @ E6[m]).max()/s - gam[m])) + 1) for m in (i, j, k)]
        n = np.array(list(itertools.product(*[range(r0, r1 + 1) for r0, r1 in rng])), float)
        X = ((n + gam[[i, j, k]])*s) @ Minv.T                       # intersection points of the three grid planes
        inb = np.all((X >= lo - s) & (X <= hi + s), axis=1); X, n = X[inb], n[inb]
        K = np.ceil(X @ E6.T/s - gam)                                # all six indices at the point
        K[:, [i, j, k]] = n
        base = (K @ E6)*a                                             # one corner of the tile
        for b0 in base: out.append((b0, a*Ei))
    return out
def corners(b0, Ev): return np.array([b0 + bits[0]*Ev[0] + bits[1]*Ev[1] + bits[2]*Ev[2] for bits in itertools.product((0, 1), repeat=3)])
def free_of_og(C, shifts):
    for sh in shifts:
        P = C - sh
        if (P @ EQ[:, :3].T + EQ[:, 3]).min(axis=0).max() > 1e-9: continue      # separated by a cut-OG face
        # tile faces as separators
        c0 = C.mean(0); sep = False
        for f in ((0, 1, 2), (0, 1, 4), (0, 2, 4)):
            pass
        Q = O + sh; Ev = np.array([C[4] - C[0], C[2] - C[0], C[1] - C[0]])
        coef = (Q - C[0]) @ np.linalg.inv(Ev)
        if (coef < -1e-9).all(axis=0).any() or (coef > 1 + 1e-9).all(axis=0).any(): continue
        return False
    return True
res = []
s = float(sys.argv[1]) if len(sys.argv) > 1 else 0.12
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
for rm in range(4):
    c = B @ (np.array([0, .5, .5]) + np.array([rm, 0, 0]))
    hs, V = room(c); lo, hi = V.min(0), V.max(0)
    shifts = [B @ np.array(m, float) for m in itertools.product(range(-1 + rm, 2 + rm), range(-1, 3), range(-1, 3))]
    shifts = [x for x in shifts if np.linalg.norm(x - c) < 2.0]
    best = None
    for trial in range(3):
        gam = rng.random(6); T = tiles(s, gam, lo, hi); vol = 0; nk = 0
        for b0, Ev in T:
            C = corners(b0, Ev); cen = C.mean(0)
            if (hs[:, :3] @ cen + hs[:, 3]).max() > 0: continue       # centroid outside this room's cell
            if free_of_og(C, shifts): vol += abs(np.linalg.det(Ev)); nk += 1
        if best is None or vol > best[0]: best = (vol, nk, len(T))
        if time.time() - t0 > 270: break
    res.append(best[0]/GAP); print(f"room {rm + 1}: grid spacing {s}, tile edge {s/2:.4f}, best of trials fills {best[0]/GAP:.3f} with {best[1]} tiles ({time.time() - t0:.0f}s)", flush=True)
    if time.time() - t0 > 270: break
print(f"mean fill {np.mean(res):.3f}; FINAL ok")
