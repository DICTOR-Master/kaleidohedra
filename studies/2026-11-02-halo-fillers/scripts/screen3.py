# Third screen (DICTO 2026-11-02), for pairs passing screen2; used on each halo face whose edges cannot be crossed by a neighbour's face
# (pi - a not a sum of dihedral angles of the set): such a face is exactly covered by coplanar faces of neighbours.
# Balance lemma: if a convex polygon R is tiled by convex polygons, then for every direction u the total length of tile edges with
# outward normal u minus that with normal -u, summed over the tiles, equals the same quantity for R (inner edge pieces cancel).
# A centrally symmetric polygon has zero balance. So a halo face F that is not centrally symmetric, covered (screen2) by coplanar
# faces of neighbours, must contain a halo face when every partner face is centrally symmetric. If the only halo faces that fit in F
# are congruent to F (all other halo faces have larger area or smaller inradius... we use area and the largest-edge test), the cover is
# a copy of F itself: a halo copy meets the halo face to face on F. Then for every way the copy can sit on F (every congruence of F,
# with each congruent face of the copy), every edge e of F needs 2 pi - a(e) - a'(e) to be a sum of dihedral angles of the set
# (or pi plus one). If no placement works for one such F, the pair cannot fill.  Usage: screen3.py <screen2.json> <out>
import json, sys, math, itertools, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import screen as S, screen2 as S2
TOL = 1e-7
def area(Pf):
    n = np.zeros(3)
    for k in range(len(Pf)): n += np.cross(Pf[k], Pf[(k + 1) % len(Pf)])
    return np.linalg.norm(n) / 2
def symmetric(Pf):
    m = len(Pf)
    if m % 2: return False
    c = Pf.mean(0); return all(np.linalg.norm(Pf[k] + Pf[(k + m // 2) % m] - 2 * c) < 1e-7 for k in range(m))
def edge_dihedrals(P, F):
    P = np.asarray(P, float); N = []
    c = P.mean(0)
    for f in F:
        n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); n /= np.linalg.norm(n); N.append(n if n @ (P[f[0]] - c) > 0 else -n)
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): E.setdefault(frozenset((f[k], f[(k + 1) % len(f)])), []).append(i)
    return {e: math.pi - math.acos(max(-1, min(1, N[l[0]] @ N[l[1]]))) for e, l in E.items() if len(l) == 2}
def sig(P, f):           # cyclic sequence (edge length, corner angle) of a face
    return [(float(np.linalg.norm(P[f[(k + 1) % len(f)]] - P[f[k]])), float(S2.corner_angles(P, [f])[k])) for k in range(len(f))]
def congruences(s1, s2):  # ways face 2 can cover face 1 (as point sets): cyclic shifts and reversals matching lengths and angles
    m = len(s1); out = []
    if len(s2) != m: return out
    for rev in (False, True):
        for sh in range(m):
            ok = True; mp = []
            for k in range(m):
                j = (sh - k) % m if rev else (sh + k) % m
                # edge k of face 1 (corner k -> k+1) maps to edge j (rev: j-1 -> j) of face 2
                L2 = s2[(j - 1) % m][0] if rev else s2[j][0]
                if abs(s1[k][0] - L2) > 1e-7 or abs(s1[k][1] - s2[j][1]) > 1e-7: ok = False; break
                mp.append((j - 1) % m if rev else j)
            if ok: out.append(mp)
    return out
if __name__ == '__main__':
    S2J, OUT = sys.argv[1:3]; s2 = json.load(open(S2J)); H = S.load_halos(); out = {}
    for key, r in s2.items():
        if not r['passes']: out[key] = dict(applies=False, note='screen2 failed'); continue
        hk, kn = key.split(' | '); P = np.asarray(H[hk]['P'], float); F = S2.hull_faces(P); ED = edge_dihedrals(P, F)
        partner = [np.asarray(Q, float)[f] for Q, G in S.KNOWN[kn] for f in G]
        if not all(symmetric(Pf) for Pf in partner): out[key] = dict(applies=False, note='a partner face is not centrally symmetric'); continue
        pool = [a for a, n in S.classes(list(ED.values()))] + [a for Q, G in S.KNOWN[kn] for a in S.dihedrals_faces(Q, G)]
        R = S2.sums(pool, 2 * math.pi)
        Rpi = S2.sums(pool, math.pi)
        crossable = lambda a: np.min(np.abs(Rpi - (math.pi - a))) < TOL       # a neighbour's face could run across an edge of angle a
        reach = lambda t: t > -TOL and (abs(t) < TOL or np.min(np.abs(R - t)) < TOL or (t > math.pi - TOL and np.min(np.abs(R - (t - math.pi))) < TOL))
        A = [area(P[f]) for f in F]; Lmax = [max(x[0] for x in sig(P, f)) for f in F]; killed = None; tried = 0
        for i, f in enumerate(F):
            if symmetric(P[f]): continue
            if any(crossable(ED[frozenset((f[k], f[(k + 1) % len(f)]))]) for k in range(len(f))): continue   # cover argument needs every edge of F uncrossable
            si = sig(P, f)
            # halo faces that could lie inside F: area <= area(F) and longest edge <= longest chord of F
            diam = max(np.linalg.norm(P[a] - P[b]) for a in f for b in f)
            fits = [j for j in range(len(F)) if A[j] <= A[i] + 1e-9 and Lmax[j] <= diam + 1e-9]
            if any(not congruences(si, sig(P, F[j])) for j in fits): continue      # a smaller halo face could share the cover
            tried += 1; ok_any = False
            for j in fits:
                for mp in congruences(si, sig(P, F[j])):
                    g = F[j]
                    if all(reach(2 * math.pi - ED[frozenset((f[k], f[(k + 1) % len(f)]))] - ED[frozenset((g[mp[k]], g[(mp[k] + 1) % len(g)]))]) for k in range(len(f))):
                        ok_any = True; break
                if ok_any: break
            if not ok_any: killed = dict(face=i, sides=len(f), corner_angles=[round(math.degrees(x[1]), 3) for x in si]); break
        out[key] = dict(applies=tried > 0, faces_tested=tried, passes=killed is None, killing_face=killed)
        print(key, out[key], flush=True)
    json.dump(out, open(OUT, 'w'), indent=1)
