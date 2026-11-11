# Complete one room exactly (DICTO 5 Nov 2026: "we need to complete so we know it is really possible"). Room = the room adaptor of the
# densest cut-OG lattice packing (Voronoi cell of the room centres minus the cut OGs). Golden rhombohedra from ONE icosahedral tiling
# (de Bruijn dual grid on the cut OG's six five-fold axes), in phi-steps coarse to fine (same phases); a tile is kept only if it lies wholly
# in the room and clear of all kept tiles (exact manifold booleans, after a voxel pre-screen). Leftover = room − tiles, decomposed.
# Completeness check: kept tiles + leftover pieces = room volume; tiles overlap 0; leftover overlaps tiles 0. Float booleans.
import json, itertools, numpy as np, time, sys, manifold3d as m3
from scipy.spatial import ConvexHull, HalfspaceIntersection
t0 = time.time(); R = "~/study-runs/og-pent/cut/data/"
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 2; S0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2; LIM = float(sys.argv[3]) if len(sys.argv) > 3 else 280
B = np.array(json.load(open(R + "densest.json"))["B"]); O = np.array(json.load(open(R + "network.json"))["ocd"]); O = O - O.mean(0)
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float).tolist())
H = ConvexHull(O); pl = {}
for eq, s in zip(H.equations, H.simplices): pl.setdefault(tuple(np.round(eq, 4)), set()).update(s)
ax5 = []
for k, v in pl.items():
    if len(v) == 5:
        p = np.array(k[:3]); p /= np.linalg.norm(p)
        if not any(abs(abs(p @ q) - 1) < 1e-3 for q in ax5): ax5.append(p)
E6 = np.array(ax5)
c = B @ np.array([0, .5, .5]); L = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3) if any(m)]
hs = np.array([np.r_[v, -(v @ (c + v/2))] for v in L]); V = HalfspaceIntersection(hs, c).intersections; Vor = hull(V)
OG = hull(O); cops = [OG.translate(list(B @ np.array(m, float))) for m in itertools.product(range(-3, 4), repeat=3)]
cops = [x for x in cops if np.linalg.norm((np.array(x.bounding_box()[:3]) + np.array(x.bounding_box()[3:]))/2 - c) < 2.4]
Room = Vor - m3.Manifold.batch_boolean(cops, m3.OpType.Add); RV = Room.volume(); lo, hi = V.min(0), V.max(0)
print(f"room volume {RV:.6f}", flush=True)
gam = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 0).random(6); phi = (1 + 5**0.5)/2
kept = []; KM = []; KLO = []; KHI = []; tile_vol = 0.0; per = []
for st in range(STEPS):
    s = S0/phi**st; a = s/2; n_try = n_keep = 0
    for i, j, k in itertools.combinations(range(6), 3):
        Ei = E6[[i, j, k]]; Mi = np.linalg.inv(Ei); corn = np.array(list(itertools.product(*zip(lo, hi))))
        rg = [(int(np.floor((corn @ E6[m]).min()/s - gam[m])) - 1, int(np.ceil((corn @ E6[m]).max()/s - gam[m])) + 1) for m in (i, j, k)]
        nn = np.array(list(itertools.product(*[range(r0, r1 + 1) for r0, r1 in rg])), float)
        X = ((nn + gam[[i, j, k]])*s) @ Mi.T; ok = np.all((X >= lo - s) & (X <= hi + s), axis=1); X, nn = X[ok], nn[ok]
        K = np.ceil(X @ E6.T/s - gam); K[:, [i, j, k]] = nn; base = (K @ E6)*a; Ev = a*Ei
        for b0 in base:
            C = np.array([b0 + b[0]*Ev[0] + b[1]*Ev[1] + b[2]*Ev[2] for b in itertools.product((0, 1), repeat=3)])
            if (hs[:, :3] @ C.mean(0) + hs[:, 3]).max() > 0: continue
            if (C @ hs[:, :3].T + hs[:, 3]).max() > 1e-12: continue          # must lie in the room's cell
            n_try += 1; T = hull(C); vT = T.volume()
            if (T - Room).volume() > 1e-10*vT: continue                       # wholly inside the room
            clo, chi = C.min(0), C.max(0); clash = False
            for M_, l_, h_ in zip(KM, KLO, KHI):
                if np.any(clo > h_ - 1e-12) or np.any(l_ > chi - 1e-12): continue
                if (T ^ M_).volume() > 1e-10*vT: clash = True; break
            if clash: continue
            KM.append(T); KLO.append(clo); KHI.append(chi); kept.append((st, C)); tile_vol += vT; n_keep += 1
        if time.time() - t0 > LIM: break
    per.append((st, s/2, n_keep)); print(f"HEARTBEAT step {st + 1}: tile edge {s/2:.4f}, tried {n_try}, kept {n_keep}; rhombi fill {tile_vol/RV:.4f} of the room ({time.time() - t0:.0f}s)", flush=True)
    if time.time() - t0 > LIM: print("time limit reached", flush=True); break
placed = m3.Manifold.batch_boolean(KM, m3.OpType.Add); Left = Room - placed; comps = Left.decompose(); parts = sorted([p.volume() for p in comps if p.volume() > 1e-13], reverse=True); voids = sum(1 for p in comps if p.volume() < -1e-13)
print(f"COMPLETENESS: rhombi {tile_vol:.9f} + leftover {Left.volume():.9f} = {tile_vol + Left.volume():.9f} vs room {RV:.9f} (diff {tile_vol + Left.volume() - RV:.1e})", flush=True)
print(f"overlaps: tiles with tiles {tile_vol - placed.volume():.1e}; leftover with tiles {(Left ^ placed).volume():.1e}", flush=True)
print(f"leftover: {len(parts)} solid piece(s), {voids} hollow(s) where tiles sit; pieces; biggest {[round(x, 6) for x in parts[:6]]}; pieces under 1e-6: {sum(1 for x in parts if x < 1e-6)}", flush=True)
np.save("complete-room-tiles.npy", np.array([np.r_[[st], C.ravel()] for st, C in kept]))
mm = Left.to_mesh(); np.savez("complete-room-left.npz", v=np.array(mm.vert_properties)[:, :3], t=np.array(mm.tri_verts), c=c)
print(f"FINAL ok {time.time() - t0:.0f}s")
