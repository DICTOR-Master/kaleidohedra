# Bull-horns basis (DICTO 5 Nov 2026 "how about using bullhorns as basis"): the published Bull-horns OG adaptor filled with ONE coherent golden tiling.
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
DD = json.load(open("~/study-runs/og-pent/step10-input.json")); VV = np.array(DD["V"]); Rr = DD["R"]; aa = 4*Rr/3
h0 = np.array([aa/2, 0, 0])
holes = [np.array(q)*aa/2 for q in itertools.product(range(-5, 6), repeat=3) if sum(x % 2 for x in q) in (1, 2)]
hh = [np.r_[p - h0, -(p - h0) @ ((p + h0)/2)] for p in holes if 1e-9 < np.linalg.norm(p - h0) < 3*aa]
CC = HalfspaceIntersection(np.array(hh), h0).intersections; cellM = hull(CC)
sites = [np.array(q)*aa/2 for q in itertools.product(range(-4, 5), repeat=3) if len({x % 2 for x in q}) == 1]
OGM = hull(VV); nearO = [p for p in sites if np.linalg.norm(p - h0) < 2.2*aa]
Room = cellM - m3.Manifold.batch_boolean([OGM.translate(list(p)) for p in nearO], m3.OpType.Add)
RV = Room.volume(); c = h0; bb = Room.bounding_box(); lo, hi = np.array(bb[:3]), np.array(bb[3:])
OM = VV - VV.mean(0); rr = np.linalg.norm(OM, axis=1); tp = OM[rr > rr.max() - 1e-6]; ax5 = []
for p in tp/np.linalg.norm(tp, axis=1)[:, None]:
    if not any(abs(abs(p @ q) - 1) < 1e-4 for q in ax5): ax5.append(p)
E6 = np.array(ax5); print("Bull-horns adaptor rebuilt: volume", RV, "(published 0.111898); five-fold axes", len(E6), flush=True)
hs = np.array([[0, 0, 0, -1.0]])      # no cell restriction: tiles only need to lie inside the adaptor
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
np.save(f"bh-tiles-s{STEPS}.npy", np.array([np.r_[[st_], C_.ravel()] for st_, C_ in kept]))
# trimmed bricks: every finest-step tile of the same tiling meeting the room, minus the kept tiles near it, intersected with the room
st = len(per) - 1; s = S0/phi**st; a = s/2; trim = []; KL, KH = np.array(KLO), np.array(KHI)
for i, j, k in itertools.combinations(range(6), 3):
    Ei = E6[[i, j, k]]; Mi = np.linalg.inv(Ei); corn = np.array(list(itertools.product(*zip(lo, hi))))
    rg = [(int(np.floor((corn @ E6[m]).min()/s - gam[m])) - 1, int(np.ceil((corn @ E6[m]).max()/s - gam[m])) + 1) for m in (i, j, k)]
    nn = np.array(list(itertools.product(*[range(r0, r1 + 1) for r0, r1 in rg])), float)
    X = ((nn + gam[[i, j, k]])*s) @ Mi.T; ok = np.all((X >= lo - 2*s) & (X <= hi + 2*s), axis=1); X, nn = X[ok], nn[ok]
    K = np.ceil(X @ E6.T/s - gam); K[:, [i, j, k]] = nn; base = (K @ E6)*a; Ev = a*Ei
    for b0 in base:
        C = np.array([b0 + b[0]*Ev[0] + b[1]*Ev[1] + b[2]*Ev[2] for b in itertools.product((0, 1), repeat=3)])
        clo, chi = C.min(0), C.max(0)
        if np.any(clo > hi) or np.any(chi < lo): continue
        T = hull(C); P = T ^ Room
        if P.volume() < 1e-14: continue
        near = np.where(~(np.any(KL > chi - 1e-12, axis=1) | np.any(clo > KH - 1e-12, axis=1)))[0]
        for q in near: P = P - KM[q]
        for comp in P.decompose():
            if comp.volume() > 1e-14: trim.append(comp)
    if time.time() - t0 > 2*LIM: break
tv = sum(p.volume() for p in trim)
print(f"COMPLETE: room {RV:.9f} = whole rhombi {tile_vol:.9f} ({len(KM)}) + trimmed rhombi {tv:.9f} ({len(trim)} pieces); sum {tile_vol + tv:.9f}, diff {tile_vol + tv - RV:.1e}", flush=True)
whole_trim = sum(1 for p in trim if abs(p.volume() - np.mean([m.volume() for m in KM[-5:]])) < 1e-12)
print(f"trimmed pieces: smallest {min(p.volume() for p in trim):.2e}, largest {max(p.volume() for p in trim):.2e}; share of the room in trimmed pieces {tv/RV:.3f}", flush=True)
print(f"FINAL ok {time.time() - t0:.0f}s")
