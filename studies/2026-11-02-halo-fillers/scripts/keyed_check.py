# Keyed-bond check (DICTO 2026-11-02) for the two pairs left by screen3: DBT Polar Halo and OTT Polar Halo with the keyed bond
# (Lotus Jewel Axes + Dodecaxes). Lists, for every face of the two keyed pieces, the dihedral angle at each edge next to each corner,
# and for the halo: the dihedral angles at the edges of its triangles, and every way 2 pi - a (a = halo angle) is a sum of the set's angles.
import json, sys, math, itertools, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import screen as S, screen2 as S2, screen3 as S3
def signed_edges(P, F):
    P = np.asarray(P, float); N = []
    for f in F:
        n = np.zeros(3)
        for k in range(len(f)): n += np.cross(P[f[k]], P[f[(k + 1) % len(f)]])
        N.append(n / np.linalg.norm(n))
    vol = sum(np.dot(P[f[0]], np.cross(P[f[k]], P[f[k + 1]])) for f in F for k in range(1, len(f) - 1))
    if vol < 0: N = [-n for n in N]
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): E[(f[k], f[(k + 1) % len(f)])] = i
    D = {}
    for (a, b), i in E.items():
        j = E[(b, a)]; e = P[b] - P[a]; e /= np.linalg.norm(e)
        th = math.atan2(float(np.cross(N[i], N[j]) @ e), float(N[i] @ N[j])); D[(a, b)] = math.degrees(math.pi - th)
    return D
def combos(target, pool, tol=1e-6):
    pool = sorted(set(round(p, 6) for p in pool)); out = []
    def rec(i, left, cur):
        if abs(left) < tol: out.append(tuple(cur)); return
        for j in range(i, len(pool)):
            if pool[j] <= left + tol: rec(j, left - pool[j], cur + [pool[j]])
    rec(0, target, []); return out
if __name__ == '__main__':
    pieces = S.KNOWN['Lotus Jewel Axes + Dodecaxes (keyed bond)']; kpool = []
    for name, (P, F) in zip(['Lotus Jewel Axes', 'Dodecaxes'], pieces):
        P = np.asarray(P, float); D = signed_edges(P, F); kpool += list(D.values()); rows = {}
        for f in F:
            for k in range(len(f)):
                ang = S2.corner_angles(P, [f])[k]
                e_in = D[(f[k - 1], f[k])]; e_out = D[(f[k], f[(k + 1) % len(f)])]
                key = (len(f), round(math.degrees(ang), 3), tuple(sorted((round(e_in, 3), round(e_out, 3)))))
                rows[key] = rows.get(key, 0) + 1
        print('==', name)
        for k, v in sorted(rows.items()): print('   face', k[0], 'sides; corner', k[1], 'deg; dihedrals at its two edges', k[2], 'x', v)
    H = S.load_halos()
    for hk in ['Belted Triacontahedron (DBT) Polar Halo', 'OTT (Octahedrally Truncated Triacontahedron) Polar Halo']:
        P = np.asarray(H[hk]['P'], float); F = S2.hull_faces(P); ED = S3.edge_dihedrals(P, F)
        hp = sorted({round(math.degrees(a), 6) for a in ED.values()}); pool = hp + [round(x, 6) for x in kpool]
        print('==', hk, 'dihedrals', hp)
        for a in hp: print('   2pi -', a, '=', combos(360 - a, pool), '| pi -', a, '=', combos(180 - a, pool))
        tri = [f for f in F if len(f) == 3]
        print('   triangle edge dihedrals:', sorted({tuple(sorted(round(math.degrees(ED[frozenset((f[k], f[(k + 1) % 3]))]), 3) for k in range(3))) for f in tri}))
