# Print faces (sides, corner angles, edge lengths) of a few solids / halos, for the construction step.
import json, sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import screen as S, screen2 as S2
def desc(name, P, F):
    P = np.asarray(P, float); print('==', name, len(P), 'corners', len(F), 'faces')
    seen = {}
    for f in F:
        L = tuple(round(float(np.linalg.norm(P[f[k]] - P[f[(k + 1) % len(f)]])), 6) for k in range(len(f)))
        A = tuple(round(math.degrees(a), 3) for a in S2.corner_angles(P, [f]))
        n = np.zeros(3)
        for k in range(len(f)): n += np.cross(P[f[k]], P[f[(k + 1) % len(f)]])
        d = abs(n / np.linalg.norm(n) @ (P[f[0]] - P.mean(0)))
        key = (len(f), tuple(sorted(L)), tuple(sorted(A)), round(d, 6)); seen[key] = seen.get(key, 0) + 1
    for k, v in sorted(seen.items()): print('  ', v, 'x', k[0], 'sides; lengths', k[1], 'angles', k[2], 'dist', k[3])
if __name__ == '__main__':
    import os
    H = S.load_halos()
    for k in sys.argv[1:]:
        if k in H: desc(k, H[k]['P'], S2.hull_faces(H[k]['P']))
        else:
            for P, F in S.KNOWN[k]: desc(k, P, F)
