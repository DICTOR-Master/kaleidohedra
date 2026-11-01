# Kagemusha (D86): two variants for its five reflex notches, where the valley rule flattens both crossing notch spikes (DICTO 2026-11-01).
# At a notch e = (a, b) with notch faces f = (a, b, c), f' = (a, b, c') and their full step-1 tips T, T' (tip = t x the foot of O):
#  (a) CONJOINED: the two crossing spikes are replaced by one piece H = hull(a, b, c, c', T, T'), bridging the notch (it must stay
#      outside the solid: checked against the centre pyramids, no clipping needed if none meets it);
#  (b) SLOPING BASES (DICTO's rule of sloping_bases.py, pyramids whose sides meet at shared points, read for a notch): each notch face
#      keeps a pyramid, but its apex is moved down the line c -> T to the point X where that line meets the notch's mirror plane (the plane
#      through e and O); the two pyramids (a, b, c, X), (a, b, c', X') then meet face to face on (a, b, X) (X = X' checked).
# The 20 other faces get the valley rule's step-1 spikes against the centre pyramids and the notch pieces. Steps 2-3: the valley rule of
# star_valley.py on the new surface (pieces beneath = the spikes / notch pieces). Reported per step: volume over the step before, the
# surface's corners / edges / faces (and planes after merging coplanar neighbours), closed and oriented, volume check, full/cut/flat.
# Usage: kagemusha_variants.py <dataset dir> <star-cores.json> <out dir>
import json, os, sys, math, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-10-30-star-cores/scripts'))
from star_core import faces_info, polyvol, vol, load
from star_valley import clash, geo
DS, SC, OUT = sys.argv[1:4]; phi = (1 + 5 ** .5) / 2

class Mesh:
    def __init__(s, V): s.V = [np.array(v, float) for v in V]
    def idx(s, p):
        for i, q in enumerate(s.V):
            if np.linalg.norm(q - p) < 1e-9: return i
        s.V.append(np.array(p, float)); return len(s.V) - 1
def hull_faces(Q):
    """Faces of hull(Q) as point lists, coplanar triangles merged, ccw seen from outside."""
    h = ConvexHull(Q); groups = {}
    for sm, eq in zip(h.simplices, h.equations): groups.setdefault(tuple(np.round(eq, 7)), (eq, set()))[1].update(sm.tolist())
    out = []
    for eq, ids in groups.values():
        P = Q[sorted(ids)]; c = P.mean(0); n = eq[:3]; u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        P = P[np.argsort([math.atan2((p - c) @ w, (p - c) @ u) for p in P])]; out.append((P, n))
    return out
def same(P, pts): return len(P) == len(pts) and all(min(np.linalg.norm(p - q) for q in pts) < 1e-9 for p in P)

def run(variant, t):
    sc = {r['D']: r for r in json.load(open(SC))}
    d, V0, F0 = load(sc['D86']['file']); V0 = V0 - V0.mean(0); FI = faces_info(V0, F0); VOL0 = polyvol(V0, F0)
    E = {}
    for i, (f, n, c) in enumerate(FI):
        for k in range(3): E.setdefault(tuple(sorted((f[k], f[(k + 1) % 3]))), []).append(i)
    def runs(i, e): f = F0[i]; k = f.index(e[0]); return f[(k + 1) % 3] == e[1]
    notches = [(e, i, j) for e, (i, j) in E.items()
               if np.cross(FI[i][1], FI[j][1]) @ ((V0[e[1]] - V0[e[0]]) if runs(i, e) else (V0[e[0]] - V0[e[1]])) < -1e-12]
    assert len(notches) == 5
    old = [np.vstack([V0[f], np.zeros(3)]) for f in F0]; OG = [geo(Q) for Q in old]
    tip = lambda i: t * FI[i][2] * FI[i][1]
    notchface = {i for _, i, j in notches} | {j for _, i, j in notches}
    pieces, info = [], {}
    for e, i, j in notches:
        a, b = V0[e[0]], V0[e[1]]; c = V0[[v for v in F0[i] if v not in e][0]]; c2 = V0[[v for v in F0[j] if v not in e][0]]
        if variant == 'conjoined':
            Q = np.vstack([a, b, c, c2, tip(i), tip(j)]); pieces.append((Q, [[a, b, c], [a, b, c2]]))
        else:
            m = np.cross(b - a, -a); m /= np.linalg.norm(m)                       # mirror plane through e and O: m.x = 0
            X = []
            for cc, T in ((c, tip(i)), (c2, tip(j))):
                s_ = (cc @ m) / ((cc - T) @ m); X.append(cc + s_ * (T - cc))
            info['X_mismatch'] = max(info.get('X_mismatch', 0), float(np.linalg.norm(X[0] - X[1])))
            pieces.append((np.vstack([a, b, c, X[0]]), [[a, b, c], [a, b, X[0]]])); pieces.append((np.vstack([a, b, c2, X[0]]), [[a, b, c2], [a, b, X[0]]]))
    # notch pieces against the solid (its centre pyramids) and each other
    info['notch_piece_meets_solid'] = sum(1 for Q, _ in pieces for P, G in zip(old, OG) if clash(Q, geo(Q), P, G))
    info['notch_pieces_overlap'] = sum(1 for x in range(len(pieces)) for y in range(x + 1, len(pieces)) if clash(pieces[x][0], geo(pieces[x][0]), pieces[y][0], geo(pieces[y][0])))
    info['notch_piece_volume'] = [round(vol(Q), 12) for Q, _ in pieces[:2]]
    for Q, _ in pieces: old.append(Q); OG.append(geo(Q))
    # step 1 on the 20 other faces: valley rule against the old pieces and each other
    caps = [i for i in range(len(F0)) if i not in notchface]
    sp = lambda i, s: np.vstack([V0[F0[i]], s * FI[i][2] * FI[i][1]])
    def free(i, s): Q = sp(i, s); g = geo(Q); return not any(clash(Q, g, P, G) for P, G in zip(old, OG))
    S = {}
    for i in caps:
        if free(i, t): S[i] = t; continue
        lo, hi = 1.0, t
        for _ in range(30):
            mid = (lo + hi) / 2
            if free(i, mid): lo = mid
            else: hi = mid
        S[i] = lo
    for _ in range(12):
        pairs = [(x, y) for x in caps for y in caps if x < y and S[x] > 1 + 1e-9 and S[y] > 1 + 1e-9 and clash(sp(x, S[x]), geo(sp(x, S[x])), sp(y, S[y]), geo(sp(y, S[y])))]
        if not pairs: break
        for x, y in pairs:
            lo, hi = 1.0, min(S[x], S[y])
            for _ in range(30):
                mid = (lo + hi) / 2; A_, B_ = sp(x, min(S[x], mid)), sp(y, min(S[y], mid))
                if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                else: lo = mid
            S[x] = min(S[x], lo); S[y] = min(S[y], lo)
    info['step1_caps_full'] = sum(1 for i in caps if S[i] > t - 1e-9); info['step1_caps_flat'] = sum(1 for i in caps if S[i] <= 1 + 1e-9)
    # surface after step 1
    M = Mesh(V0); F, below, kind = [], [], []
    for i in caps:
        f = F0[i]
        if S[i] <= 1 + 1e-9: F.append(list(f)); below.append(old[i]); kind.append('solid'); continue
        Q = sp(i, S[i]); ti = M.idx(Q[-1])
        for k in range(3): F.append([f[k], f[(k + 1) % 3], ti]); below.append(Q); kind.append('spike')
    for Q, inner in pieces:
        for P, n in hull_faces(Q):
            if any(same(P, I) for I in inner): continue
            F.append([M.idx(p) for p in P]); below.append(Q); kind.append('notch')
    V = np.array(M.V)
    steps = [describe(V, F, VOL0, VOL0, 1, info)]; vols = [VOL0, polyvol(V, F)]
    snap = dict(V=V.tolist(), F=F, kind=kind)
    # steps 2-3: the valley rule
    for k in (2, 3):
        FI2 = faces_info(V, F); base = []
        for (f, n, c), Pc in zip(FI2, below):
            h = (Pc - V[f[0]]) @ n; A = Pc[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
        spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
        def free_old(i, s): Q = spike(i, s); g = geo(Q); return not any(clash(Q, g, P, G) for P, G in zip(old, OG))
        S2 = []
        for i in range(len(base)):
            if free_old(i, t): S2.append(t); continue
            lo, hi = 1.0, t
            for _ in range(30):
                mid = (lo + hi) / 2
                if free_old(i, mid): lo = mid
                else: hi = mid
            S2.append(lo)
        for _ in range(12):
            Qs = [spike(i, s) for i, s in enumerate(S2)]; Gs = [geo(Q) if s > 1 + 1e-9 else None for Q, s in zip(Qs, S2)]
            pairs = [(i, j) for i in range(len(S2)) for j in range(i + 1, len(S2)) if Gs[i] and Gs[j] and clash(Qs[i], Gs[i], Qs[j], Gs[j])]
            if not pairs: break
            for i, j in pairs:
                lo, hi = 1.0, min(S2[i], S2[j])
                for _ in range(30):
                    mid = (lo + hi) / 2; A_, B_ = spike(i, min(S2[i], mid)), spike(j, min(S2[j], mid))
                    if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                    else: lo = mid
                S2[i] = min(S2[i], lo); S2[j] = min(S2[j], lo)
        V2 = list(V); F2 = []; B2 = []; added = 0.0
        for i, (f, A, foot) in enumerate(base):
            if S2[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); continue
            tp = A + S2[i] * (foot - A); ti = len(V2); V2.append(tp); Q = np.vstack([V[f], tp]); old.append(Q); OG.append(geo(Q)); added += vol(Q)
            for a in range(len(f)): F2.append([f[a], f[(a + 1) % len(f)], ti]); B2.append(Q)
        V, F, below = np.array(V2), F2, B2; vols.append(polyvol(V, F))
        fr = [(s - 1) / (t - 1) for s in S2]
        steps.append(describe(V, F, vols[-2], VOL0, k, dict(full=sum(x > 1 - 1e-9 for x in fr), cut=sum(1e-9 <= x <= 1 - 1e-9 for x in fr),
                                                         flat=sum(x < 1e-9 for x in fr), spikes_vs_gain=added - (vols[-1] - vols[-2]))))
    steps[0]['volume_over_last'] = vols[1] / vols[0]; steps[0]['volume_check'] = vols[1] - VOL0 - sum(vol(Q) for Q, _ in pieces) - sum(vol(sp(i, S[i])) for i in caps if S[i] > 1 + 1e-9)
    return dict(variant=variant, t='phi' if t == phi else '2', steps=steps, step1=snap, final=dict(V=V.tolist(), F=F))

def describe(V, F, vlast, v0, k, extra):
    E = {}
    for f in F:
        for a in range(len(f)): E.setdefault(tuple(sorted((f[a], f[(a + 1) % len(f)]))), []).append(f)
    closed = all(len(x) == 2 for x in E.values())
    FI = faces_info(V, F); planes = len({tuple(np.round(np.append(n, c), 6)) for _, n, c in FI})
    used = {v for f in F for v in f}
    vol_ = polyvol(V, F)
    return dict(step=k, corners=len(used), edges=len(E), faces=len(F), planes=planes, euler=len(used) - len(E) + len(F), closed=closed,
                volume_over_last=vol_ / vlast, volume_over_solid=vol_ / v0, **extra)

if __name__ == '__main__':
    out = [run(v, t) for v in ('conjoined', 'sloping') for t in (2.0, phi)]
    json.dump(out, open(os.path.join(OUT, 'kagemusha-variants.json'), 'w'), indent=1, default=float)
    for r in out:
        for s in r['steps']: print(r['variant'], r['t'], {k: (round(v, 6) if isinstance(v, float) else v) for k, v in s.items()}, flush=True)
