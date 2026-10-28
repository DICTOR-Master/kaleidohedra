# Ti-6Al-4V step (DICTO 10-28): hydrogen sites in a close-packed metal of any stacking, counted from explicit coordinates.
# Balls of diameter a = 1 on layers ABC...; tetrahedral and octahedral holes found as centres of 4 and 6 touching balls.
# Count per ball: tetrahedral sites, face-sharing tetrahedral pairs (centres closer than 2.1 A, Switendick's H-H limit, for
# titanium a = 2.95 A), octahedral sites, face-sharing octahedral pairs; compare with the hexagonality h of the stacking.
import itertools, numpy as np
from fractions import Fraction as F
POS = {'A': np.array([0, 0]), 'B': np.array([1/2, 3**.5/6]), 'C': np.array([1, 3**.5/3])}
DZ = (2/3)**.5; N = 6                                       # in-plane cell N x N balls
def balls(word, reps):
    out = []
    for L in range(len(word) * reps):
        p = POS[word[L % len(word)]]
        for i, j in itertools.product(range(N), repeat=2):
            out.append([p[0] + i + j/2, p[1] + j*3**.5/2, L*DZ])
    return np.array(out)
def count(word, a_ang=2.95):
    n = len(word); reps = 3; B = balls(word, reps)
    cell = np.array([[N, 0], [N/2, N*3**.5/2]]); inv = np.linalg.inv(cell.T); PZ = 1e9
    def disp(P, Q):                                        # minimal-image vector Q - P (periodic in plane)
        dd = Q[:2] - P[:2]; f = dd @ inv.T; f -= np.round(f); dz = Q[2] - P[2]; dz -= PZ * np.round(dz / PZ)
        return np.array([*(f @ cell), dz])
    def d2(P, Q): v = disp(P, Q); return v @ v
    # candidate hole centres: tetra at centroids of 4 mutually touching balls, octa at centres of 6
    tet, octa = [], []
    for L in range(n, 2*n):                                # middle repeat only
        lo = B[np.isclose(B[:, 2], L*DZ)]; up = B[np.isclose(B[:, 2], (L+1)*DZ)]
        for X, Y in ((lo, up), (up, lo)):                  # triangle in X, apex in Y
            for i, p in enumerate(X):
                nb = [q for q in X if abs(d2(p, q) - 1) < 1e-9]
                for q, r in itertools.combinations(nb, 2):
                    if abs(d2(q, r) - 1) > 1e-9: continue
                    c = p + (disp(p, q) + disp(p, r)) / 3
                    ap = [y for y in Y if abs(d2(c, y) - 2/3) < 1e-9]
                    if ap: tet.append(c + disp(c, ap[0]) / 4)
                    else: octa.append(c + np.array([0, 0, DZ/2 if Y is up else -DZ/2]))
    def uniq(S):
        S = np.array(S); keep = []
        for s in S:
            if not any(d2(s, k) < 1e-9 for k in keep): keep.append(s)
        return np.array(keep)
    tet, octa = uniq(tet), uniq(octa); nb = n * N * N; PZ = n * DZ          # now periodic in z too
    # distance classes (a = 1): face-sharing tetra pair DZ/2 = 0.408 (1.20 A in Ti), edge-sharing tetra 1/2 (1.48 A),
    # face-sharing octa pair DZ = 0.816 (2.41 A); all tetra-tetra classes found are listed
    from collections import Counter
    cls = Counter(round(d2(tet[i], tet[j])**.5, 4) for i, j in itertools.combinations(range(len(tet)), 2) if d2(tet[i], tet[j]) < 0.75)
    tp = sum(1 for i, j in itertools.combinations(range(len(tet)), 2) if abs(d2(tet[i], tet[j]) - DZ**2/4) < 1e-9)
    op = sum(1 for i, j in itertools.combinations(range(len(octa)), 2) if abs(d2(octa[i], octa[j]) - DZ**2) < 1e-9)
    print('   ', word, 'tetra-tetra distance classes < 0.75a (per ball):', {k: str(F(v, n*N*N)) for k, v in sorted(cls.items())})
    t = ''.join('h' if word[i-1] == word[(i+1) % n] else 'c' for i in range(n)); h = F(t.count('h'), n)
    return h, F(len(tet), nb), F(len(octa), nb), F(tp, nb), F(op, nb)
print('stacking  h     tetra/ball  octa/ball  face-sharing tetra pairs/ball  face-sharing octa pairs/ball')
for w in ('ABC', 'ABAB', 'ABAC', 'ABCACB', 'ABCBCBACAC', 'ABCBCBCBACACAC'):
    h, T, O, TP, OP = count(w)
    print(f'{w:15s} {str(h):5s} {str(T):10s} {str(O):10s} {str(TP):22s} {OP}   face tetra pairs = h: {TP == h}; octa pairs = h: {OP == h}')
