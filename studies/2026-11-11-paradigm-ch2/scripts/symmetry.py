"""Chapter 2 (The Permutohedron Paradigm): the permutohedron of four values v1<v2<v3<v4 always has the 24 symmetries of the tetrahedron
(permuting coordinates); it has the full 48 of the cube (central inversion added) exactly when the values are symmetric about their mean
(v1 + v4 = v2 + v3, gaps g : m : g). Checked by computing the symmetry group of the corner set (all orthogonal maps of the sum-zero
3-space that map corners to corners, found as permutations of corners preserving all distances) for symmetric and non-symmetric values."""
import itertools, sys
from fractions import Fraction as F
import numpy as np
fails = []
def chk(ok, what): print(('PASS ' if ok else 'FAIL ') + what); (None if ok else fails.append(what))
def sym_count(vals):
    P = [tuple(F(v) for v in p) for p in itertools.permutations(vals)]
    m = sum(vals) / F(4); P = [tuple(x - m for x in p) for p in P]
    D = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b))
    # a symmetry is fixed by where it sends 3 affinely independent corners + it must preserve distances to all; count via images of a frame
    base = [P[0]]; 
    for q in P[1:]:
        cand = base + [q]
        M = np.array([[float(x) for x in c] for c in cand]); 
        if np.linalg.matrix_rank(M - M[0]) == len(cand) - 1: base = cand
        if len(base) == 4: break
    count = 0
    for img in itertools.permutations(range(len(P)), 4):
        if any(D(P[img[i]], P[img[j]]) != D(base[i], base[j]) for i in range(4) for j in range(i + 1, 4)): continue
        if any(D(P[img[i]], (0, 0, 0, 0)) != D(base[i], (0, 0, 0, 0)) for i in range(4)): continue
        # extend: each corner's image is the unique corner with the same distances to the frame images
        ok = True
        for c in P:
            d = [D(c, b) for b in base]
            im = [q for q in P if [D(q, P[img[i]]) for i in range(4)] == d]
            if len(im) != 1: ok = False; break
        count += ok
    return count
tau = (1 + 5 ** .5) / 2
for vals, sym in [((1, 2, 3, 4), True), ((1, 2, 4, 5), True), ((-5, -1, 1, 5), True), ((0, 1, 3, 4), True), ((1, 2, 3, 5), False), ((0, 1, 3, 7), False), ((1, 2, 4, 7), False)]:
    n = sym_count(vals)
    chk(n == (48 if sym else 24), f'values {vals}: {n} symmetries (expected {48 if sym else 24}: symmetric about the mean = {sym})')
print('FINAL ok' if not fails else f'FINAL FAIL {fails}')
