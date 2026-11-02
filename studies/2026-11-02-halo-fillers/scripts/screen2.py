# Second screen for the pairs that pass screen.py (DICTO 2026-11-02). If pi - a is not a sum of available dihedral angles for every edge
# of the halo, no neighbour's face can cross a halo edge, so every halo face is exactly covered by coplanar faces of neighbours
# (halo copies or partner pieces), and every corner angle of every halo face must be a sum of face corner angles of the set
# (non-negative integer combination; corners of the covering faces lie at the halo corner, since an edge through it would need pi).
# Usage: screen2.py <screen.json> <out>
import json, sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import screen as S
TOL = 1e-7
def corner_angles(P, F):
    P = np.asarray(P, float); out = []
    for f in F:
        for k in range(len(f)):
            a, b, c = P[f[k - 1]], P[f[k]], P[f[(k + 1) % len(f)]]; u, v = a - b, c - b
            th = math.acos(max(-1, min(1, u @ v / np.linalg.norm(u) / np.linalg.norm(v))))
            out.append(th)                 # convex faces only are tested; non-convex partner faces contribute their convex corners
    return out
def hull_faces(P):
    from scipy.spatial import ConvexHull
    import itertools
    P = np.asarray(P, float); H = ConvexHull(P); g = {}
    for sm, eq in zip(H.simplices, H.equations): g.setdefault(tuple(np.round(eq / np.linalg.norm(eq[:3]), 8)), eq / np.linalg.norm(eq[:3]))
    F = []
    for eq in g.values():
        ids = [i for i in range(len(P)) if abs(eq[:3] @ P[i] + eq[3]) < 1e-9 * max(1, np.abs(P).max())]
        c = P[ids].mean(0); n = eq[:3]; u = P[ids[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        ids.sort(key=lambda i: math.atan2((P[i] - c) @ w, (P[i] - c) @ u))
        # drop points on an edge (straight angle)
        ids = [i for k, i in enumerate(ids) if np.linalg.norm(np.cross(P[i] - P[ids[k - 1]], P[ids[(k + 1) % len(ids)]] - P[i])) > 1e-9]
        F.append(ids)
    return F
def sums(A, top):
    A = sorted(set(round(a, 10) for a in A if a < top + TOL)); R = {0.0}
    for a in A:
        new = set(R)
        for s in R:
            m = 1
            while s + m * a <= top + TOL: new.add(round(s + m * a, 9)); m += 1
        R = new
    return np.array(sorted(R))
if __name__ == '__main__':
    SJ, OUT = sys.argv[1:3]; H = S.load_halos(); res = json.load(open(SJ)); out = {}
    for key in res['with_known']:
        hk, kn = key.split(' | ')
        hp = H[hk]['P']; hf = hull_faces(hp)
        da_h = [a for a, n in S.classes(S.dihedrals(hp))]; da_k = [a for P, F in S.KNOWN[kn] for a in S.dihedrals_faces(P, F)]
        pool_d = sums(da_h + da_k, math.pi)
        crossable = [a for a in da_h if np.min(np.abs(pool_d - (math.pi - a))) < TOL]
        fa_h = corner_angles(hp, hf); fa_k = [a for P, F in S.KNOWN[kn] for a in corner_angles(P, F)]
        R = sums(fa_h + fa_k, math.pi)
        bad = sorted({round(math.degrees(t), 4) for t in fa_h if np.min(np.abs(R - t)) > TOL})
        applies = not crossable
        out[key] = dict(edges_crossable=[math.degrees(a) for a in crossable], applies=applies, failing_corner_angles=bad,
                        partner_corner_angles=sorted({round(math.degrees(a), 4) for a in fa_k}), halo_corner_angles=sorted({round(math.degrees(a), 4) for a in fa_h}),
                        passes=(not applies) or not bad)
        print(key, out[key], flush=True)
    json.dump(out, open(OUT, 'w'), indent=1)
