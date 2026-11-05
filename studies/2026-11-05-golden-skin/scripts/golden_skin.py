# A complete, nearly golden fill around the ORIGINAL OG (DICTO 5 Nov 2026: "use the original OG with actual rhombi ... to try for a completely
# golden solution"; "this new combination of technologies"). Exact Dehn (proved today): golden rhombohedra alone can never close around the OG;
# the obstruction sits on its edges. Construction: OGs on a lattice t*Z{e1,e2,e3} built from three of its own five-fold axes (a scaled prolate
# golden rhombohedral lattice, smallest t without overlap); space tiled by the prolate golden rhombohedron of edge a = t/m (same lattice,
# m^3 bricks per period). Skin = (bricks meeting an OG) − OG. Complete fill per period: OG + skin + whole bricks; counted exactly, checked by
# booleans. Float.
import json, itertools, numpy as np, time, sys, manifold3d as m3
from scipy.spatial import ConvexHull
t0 = time.time()
O = np.array(json.load(open("/home/dicto/study-runs/og-pent/og/data/network.json"))["ocd"]); O = O - O.mean(0)
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float).tolist()); OG = hull(O); VOG = OG.volume()
r = np.linalg.norm(O, axis=1); tips = O[r > r.max() - 1e-6]; ax = []
for p in tips/np.linalg.norm(tips, axis=1)[:, None]:
    if not any(abs(abs(p @ q) - 1) < 1e-6 for q in ax): ax.append(p)
ax = np.array(ax); print("OG corners", len(O), "five-fold tips", len(tips), "axes", len(ax), flush=True)
tri = next(q for q in itertools.combinations(range(6), 3) if all(abs(ax[i] @ ax[j] - 1/5**0.5) < 1e-6 for i, j in itertools.combinations(q, 2)) or
           all(abs(abs(ax[i] @ ax[j]) - 1/5**0.5) < 1e-6 for i, j in itertools.combinations(q, 2)))
E = np.array([ax[k] for k in tri])
for k in (1, 2):
    if E[0] @ E[k] < 0: E[k] = -E[k]
print("edge directions pairwise cos", np.round([E[0] @ E[1], E[0] @ E[2], E[1] @ E[2]], 6), "(1/sqrt5 = 0.447214: prolate)", flush=True)
def overlaps(t):
    for n in itertools.product(range(-2, 3), repeat=3):
        if not any(n): continue
        v = t*(np.array(n, float) @ E)
        if np.linalg.norm(v) > 2*r.max() + 1e-9: continue
        if (OG ^ OG.translate(list(v))).volume() > 1e-12: return True
    return False
lo_, hi_ = 0.5, 4.0
for _ in range(40):
    mid = (lo_ + hi_)/2
    if overlaps(mid): lo_ = mid
    else: hi_ = mid
t = hi_; cellV = abs(np.linalg.det(t*E)); print(f"smallest lattice scale t = {t:.6f}; OG packing density {VOG/cellV:.4f}", flush=True)
for m in [int(x) for x in (sys.argv[1:] or ["3", "5", "8"])]:
    a = t/m; vb = abs(np.linalg.det(a*E))
    # bricks meeting the OG at the origin (and its neighbours): brick (i,j,k) = a*((i,j,k) + [0,1]^3) @ E
    Ei = np.linalg.inv(a*E); cf = O @ Ei; lo, hi = np.floor(cf.min(0)).astype(int) - 1, np.ceil(cf.max(0)).astype(int) + 1
    env = []
    for idx in itertools.product(*[range(l, h + 1) for l, h in zip(lo, hi)]):
        C = (np.array(idx, float) + np.array(list(itertools.product((0, 1), repeat=3)), float)) @ (a*E)
        if (hull(C) ^ OG).volume() > 1e-13: env.append(idx)
    env = set(env); touch = {tuple(np.array(b) % m) for b in env}      # brick places per period meeting some OG (each counted once)
    shared = len(env) - len(touch)
    nper = m**3; skinV = len(touch)*vb - VOG
    print(f"m = {m}: brick edge {a:.4f}; per period {nper} brick places; {len(touch)} meet an OG -> OG + skin; {nper - len(touch)} whole golden bricks; bricks touching two OGs {shared}", flush=True)
    pos = ['(skin joined across touching OGs: one network piece per period)']
    print(f"   skin volume {skinV:.6f} {pos[0]}; share of space: OG {VOG/cellV:.4f}, skin {skinV/cellV:.4f}, golden bricks {(nper - len(touch))*vb/cellV:.4f}; sum {(VOG + skinV + (nper - len(touch))*vb)/cellV:.9f}", flush=True)
    np.save(f"touch-m{m}.npy", np.array(sorted(env)))
    if time.time() - t0 > 250: break
print(f"FINAL ok {time.time() - t0:.0f}s")
