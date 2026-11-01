# DICTO's sloping-base rule (Kuwagata) at the sharp valleys of the six convex eccentric pieces (DICTO 2026-11-01, for paper D v2).
# Sharp edges of the solid: the edges the valley law keeps open through step two: delta <= 120 deg at t = 2, delta <= 142.0786 deg at
# t = phi (equal-sided golden bound). At every step k = 1..3, at a sharp edge e = (a, b) whose two current valley faces still both
# contain e: if their two full spikes (tips T, T' of the valley rule) overlap, they are NOT cut back; instead each keeps a pyramid over
# its whole face with apex X moved along the line from the face's far corner x (mean of the corners farthest from the line of e; the
# corner c for a triangle, as for Kuwagata) towards T until it meets the valley's bisecting plane (n - n').(p - a) = 0, so that the two
# pyramids meet face to face on (a, b, X). Used only when X = X' (to 1e-9) and the two pyramids clear every old piece; otherwise the
# valley rule as before (counted). All other spikes: the valley rule of star_valley.py, against the old pieces and the sloping pieces.
# Output: data/sloping-six/<D>-<t>.json: per step volume over the step before, closed surface, Euler, volume check, full/cut/flat,
# sloping pairs used / refused. Usage: sloping_six.py <dataset dir> <star-cores.json> <out dir> <D> <t: 2|phi>
import json, os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-10-30-star-cores/scripts'))
DS, SC, OUT, DN, TN = sys.argv[1:6]; sys.argv = sys.argv[:4]          # star_valley reads argv[4] as a job count
from star_core import faces_info, polyvol, vol, load
from star_valley import clash, geo
phi = (1 + 5 ** .5) / 2; t = phi if TN == 'phi' else 2.0
BOUND = 142.0786 if TN == 'phi' else 120.0

def edges_of(F):
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): E.setdefault(tuple(sorted((f[k], f[(k + 1) % len(f)]))), []).append(i)
    return E

def main():
    r = [x for x in json.load(open(SC)) if x['D'] == DN][0]
    d, V, F = load(r['file']); V = V - V.mean(0); F = [list(f) for f in F]; VOL0 = polyvol(V, F)
    FI = faces_info(V, F); E0 = edges_of(F); sharp = []
    for e, (i, j) in E0.items():
        dih = 180 - math.degrees(math.acos(np.clip(FI[i][1] @ FI[j][1], -1, 1)))
        if dih <= BOUND + 1e-9: sharp.append(e)
    old = [np.vstack([V[f], np.zeros(3)]) for f in F]; OG = [geo(Q) for Q in old]; below = list(old)
    steps = []; vols = [VOL0]
    for k in (1, 2, 3):
        FI = faces_info(V, F); base = []
        for (f, n, c), Pc in zip(FI, below):
            h = (Pc - V[f[0]]) @ n; A = Pc[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
        spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
        # sloping pairs at sharp edges
        E = edges_of(F); slope = {}; sedge = {}; used = refused = 0
        for e in sharp:
            fs = E.get(e)
            if not fs or len(fs) != 2: continue
            i, j = fs; Qi, Qj = spike(i, t), spike(j, t)
            if not clash(Qi, geo(Qi), Qj, geo(Qj)): continue
            a, b = V[e[0]], V[e[1]]; u = (b - a) / np.linalg.norm(b - a); m = FI[i][1] - FI[j][1]; m /= np.linalg.norm(m)
            X = []
            for q, Q in ((i, Qi), (j, Qj)):
                f = F[q]; off = [v for v in f if v not in e]
                dist = np.array([np.linalg.norm((V[v] - a) - ((V[v] - a) @ u) * u) for v in off])
                x = V[[v for v, dd in zip(off, dist) if dd > dist.max() - 1e-9]].mean(0); T = Q[-1]
                den = (T - x) @ m; X.append(x + ((a - x) @ m) / den * (T - x) if abs(den) > 1e-12 else None)
            ok = X[0] is not None and X[1] is not None and np.linalg.norm(X[0] - X[1]) < 1e-9
            if ok:
                Pi, Pj = np.vstack([V[F[i]], X[0]]), np.vstack([V[F[j]], X[0]])
                ok = not any(clash(P, geo(P), Q, G) for P in (Pi, Pj) for Q, G in zip(old, OG)) and i not in slope and j not in slope
            if ok:
                slope[i] = Pi; slope[j] = Pj; sedge[i] = sedge[j] = set(e); used += 1
            else: refused += 1
        oldS = old + list(slope.values()); OGS = OG + [geo(Q) for Q in slope.values()]
        def free_old(i, s): Q = spike(i, s); g = geo(Q); return not any(clash(Q, g, P, G) for P, G in zip(oldS, OGS))
        S = []
        for i in range(len(base)):
            if i in slope: S.append(None); continue
            if free_old(i, t): S.append(t); continue
            lo, hi = 1.0, t
            for _ in range(30):
                mid = (lo + hi) / 2
                if free_old(i, mid): lo = mid
                else: hi = mid
            S.append(lo)
        free = [i for i in range(len(S)) if S[i] is not None]
        for _ in range(12):
            Qs = {i: spike(i, S[i]) for i in free}; Gs = {i: geo(Qs[i]) if S[i] > 1 + 1e-9 else None for i in free}
            pairs = [(i, j) for x_, i in enumerate(free) for j in free[x_ + 1:] if Gs[i] and Gs[j] and clash(Qs[i], Gs[i], Qs[j], Gs[j])]
            if not pairs: break
            for i, j in pairs:
                lo, hi = 1.0, min(S[i], S[j])
                for _ in range(30):
                    mid = (lo + hi) / 2; A_, B_ = spike(i, min(S[i], mid)), spike(j, min(S[j], mid))
                    if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                    else: lo = mid
                S[i] = min(S[i], lo); S[j] = min(S[j], lo)
        V2 = list(V); F2 = []; B2 = []; added = 0.0; Xidx = {}
        for i, (f, A, foot) in enumerate(base):
            if i in slope:
                P = slope[i]; key = tuple(np.round(P[-1], 9))
                if key not in Xidx: Xidx[key] = len(V2); V2.append(P[-1])
                xi = Xidx[key]; old.append(P); OG.append(geo(P)); added += vol(P)
                for a_ in range(len(f)):
                    u_, w_ = f[a_], f[(a_ + 1) % len(f)]
                    if {u_, w_} == sedge[i]: continue                  # the shared face (a, b, X) lies inside
                    F2.append([u_, w_, xi]); B2.append(P)
                continue
            if S[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); continue
            tp = A + S[i] * (foot - A); ti = len(V2); V2.append(tp); Q = np.vstack([V[f], tp]); old.append(Q); OG.append(geo(Q)); added += vol(Q)
            for a_ in range(len(f)): F2.append([f[a_], f[(a_ + 1) % len(f)], ti]); B2.append(Q)
        V, F, below = np.array(V2), F2, B2; vols.append(polyvol(V, F))
        E2 = edges_of(F); closed = all(len(x) == 2 for x in E2.values()); usedv = {v for f in F for v in f}
        fr = [(s - 1) / (t - 1) for s in S if s is not None]
        steps.append(dict(step=k, volume_over_last=vols[-1] / vols[-2], volume_over_solid=vols[-1] / VOL0, closed=closed,
                          euler=len(usedv) - len(E2) + len(F), corners=len(usedv), faces=len(F), volume_check=added - (vols[-1] - vols[-2]),
                          sloping_pairs=used, refused=refused, full=sum(x > 1 - 1e-9 for x in fr), cut=sum(1e-9 <= x <= 1 - 1e-9 for x in fr),
                          flat=sum(x < 1e-9 for x in fr)))
        print(DN, TN, steps[-1], flush=True)
    os.makedirs(os.path.join(OUT, 'sloping-six'), exist_ok=True)
    json.dump(dict(D=DN, name=r['name'], t=TN, sharp_edges=len(sharp), bound=BOUND, steps=steps),
              open(os.path.join(OUT, 'sloping-six', f'{DN}-{TN}.json'), 'w'), indent=1, default=float)
main()
