#!/usr/bin/env python3
"""Does the Dehn-zero member of the tetrahedron sweep, S(2) = T(4) minus its four corner T(1), tile space alone?
S(2) is a union of 30 cells of the octet honeycomb (16 up + 4 down tetrahedra, 10 octahedra: ratio 2:1 as in the honeycomb — true for T(n) minus corners only at n = 4,
the same condition as Dehn zero). Search: exact cover of the octet cells on periodic tori fcc/L for every sublattice L of index N (Hermite normal form), by the piece's
orientations under O_h (signed permutations). Finding a cover proves a tiling; failure on all tori up to N is evidence only (cell-aligned, periodic).
Controls: the rhombohedron (1 O + 2 T) tiles at N = 1; a single tetrahedron never tiles."""
import itertools, sys, json, numpy as np
from scipy.spatial import Delaunay
B = np.array([(1,1,0),(1,0,1),(0,1,1)], float).T   # fcc basis (columns)
def cells(R):
    out = []
    for p in itertools.product(range(-R, R+1), repeat=3):
        if sum(p) % 2: out.append(('O', p))
    for p in itertools.product([x + .5 for x in range(-R, R)], repeat=3): out.append(('T', p))
    return out
def inside(verts, R=10):
    d = Delaunay(np.array(verts, float)); return [c for c in cells(R) if d.find_simplex(np.array(c[1])) >= 0 and all(abs(c[1][k]) < R for k in range(3))]
PIECES = {
 'S2': lambda: [c for c in inside([(0,0,0),(4,4,0),(4,0,4),(0,4,4)]) if not any(np.allclose(c[1], v + (np.array((2,2,2)) - v)/4) for v in np.array([(0,0,0),(4,4,0),(4,0,4),(0,4,4)], float))],
 'rhombohedron': lambda: inside([(0,0,0),(1,1,0),(1,0,1),(0,1,1),(2,1,1),(1,2,1),(1,1,2),(2,2,2)]),
 'tetra': lambda: inside([(0,0,0),(1,1,0),(1,0,1),(0,1,1)]),
}
def orientations(cl):
    pts = np.array([c[1] for c in cl]); seen = []; res = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3)); [M.__setitem__((i, perm[i]), sg[i]) for i in range(3)]
            Q = pts @ M.T; Q = Q - Q.min(0); Q = Q - (np.floor(Q.min(0)))  # normalise later by lattice shift
            key = frozenset(map(tuple, np.round(Q - Q[np.lexsort(Q.T[::-1])][0], 6)))
            if key not in seen: seen.append(key); res.append(pts @ M.T)
    return res
def hnf(N):
    for a in range(1, N+1):
        if N % a: continue
        for b in range(1, N//a + 1):
            if (N//a) % b: continue
            c = N//a//b
            for d, e, f in itertools.product(range(a), range(a), range(b)): yield np.array([[a, d, e], [0, b, f], [0, 0, c]], float)
def solve(rows, ncols):
    X = {j: set() for j in range(ncols)}
    for i, r in enumerate(rows):
        for j in r: X[j].add(i)
    sol = []
    def sel(i):
        cols = []
        for j in rows[i]:
            for k in X[j]:
                for l in rows[k]:
                    if l != j: X[l].discard(k)
            cols.append(X.pop(j))
        return cols
    def desel(i, cols):
        for j in reversed(rows[i]):
            X[j] = cols.pop()
            for k in X[j]:
                for l in rows[k]:
                    if l != j: X[l].add(k)
    def rec():
        if not X: return True
        j = min(X, key=lambda c: len(X[c]))
        for i in list(X[j]):
            sol.append(i); cols = sel(i)
            if rec(): return True
            desel(i, cols); sol.pop()
        return False
    return sol if rec() else None
def try_torus(orients, H):
    L = B @ H; Li = np.linalg.inv(L); Bi = np.linalg.inv(B)
    def key(kind, x):
        z = Li @ np.asarray(x, float); z = np.round(z - np.floor(z + 1e-9), 6) % 1; return (kind, tuple(np.round(z, 6)))
    N = int(round(np.linalg.det(H)))
    # all cells of the torus: cells of the fcc unit (1 O + 2 T per lattice point) over coset reps
    reps = [B @ np.array(v, float) for v in itertools.product(*[range(int(H[k, k])) for k in range(3)])]
    base = [('O', (1, 0, 0)), ('T', (.5, .5, .5)), ('T', (-.5, -.5, -.5))]
    allc = {key(k, np.array(p) + r) for r in reps for k, p in base}
    if len(allc) != 3*N: return 'bad torus'
    idx = {c: i for i, c in enumerate(sorted(allc))}
    rows = set()
    for kinds, P in orients:
        for r in reps:
            ks = [idx.get(key(k, p + r)) for k, p in zip(kinds, P)]
            if None in ks or len(set(ks)) != len(ks): continue
            rows.add(tuple(sorted(ks)))
    rows = sorted(rows)
    s = solve(rows, len(idx)); return s
if __name__ == '__main__':
    name = sys.argv[1]; Ns = [int(x) for x in sys.argv[2].split(',')]
    cl = PIECES[name](); kinds = [c[0] for c in cl]
    print(name, 'cells', len(cl), 'O', kinds.count('O'), 'T', kinds.count('T'), flush=True)
    pts = np.array([c[1] for c in cl]); orients = []
    seen = set()
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3))
            for i in range(3): M[i, perm[i]] = sg[i]
            Q = pts @ M.T
            # shift so the piece's cells sit on the same cell lattice: shifts by fcc vectors keep cells; a signed perm already maps cells to cells
            k = frozenset((kd, tuple(np.round(q - Q.min(0), 6))) for kd, q in zip(kinds, Q))
            if k in seen: continue
            seen.add(k); orients.append((kinds, Q))
    print('orientations', len(orients), flush=True)
    res = {}
    for N in Ns:
        if (3*N) % len(cl): print('N', N, 'skip (cell count)'); continue
        n = 0; found = None
        for H in hnf(N):
            n += 1; s = try_torus(orients, H)
            if s and s != 'bad torus': found = H.tolist(); break
        print('N', N, 'tori tried', n, 'FOUND' if found else 'none', found, flush=True); res[N] = found
        if found: break
    json.dump({'piece': name, 'results': res}, open(f'data/tile-{name}.json', 'w'))
