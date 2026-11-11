# Dense exact check of the main theorem's computed part: the fixed shift of one c-tower (connect.py's best choice) keeps the c-tile
# one face-connected solid with a clean surface (every side in exactly two faces) at every weight of a grid of step 1/480 over the
# walk -11/24 <= λ <= 3/8 (401 weights; every break point of the ring-build scan is a multiple of 1/96, so all are included), plus
# 1/10. Also records the least contact area between the towers (unit triangles) and the h-tile's connectivity with no shift.
# Usage: python3 dense.py <k0> <k1>  (grid indices k: λ = -11/24 + k/480) -> data/dense_<k0>.jsonl
import json, os, sys, itertools
from fractions import Fraction as Fr
from tiles import tile
import exactfaces as E
import connect as K

def check(lam, t):
    w, L = {'c': ('ABC', 1), 'h': ('AB', 0)}[t]
    T = tile(w, L, lam)[0]; n = len(T)
    sh = [(0, 1) if (t == 'c' and k[2][0] < 0) else (0, 0) for k in T]       # c: move the tower whose sites sit at (-1/3, -1/3)
    P = [K.shift(p[3], s) for p, s in zip(T, sh)]; F = [E.facets(X) for X in P]
    cont = {}
    for i, j in itertools.combinations(range(n), 2):
        a = K.contact(F[i], F[j], (0, 0))
        if a > 0: cont[(i, j)] = cont[(j, i)] = a
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in range(n):
            if y not in seen and (x, y) in cont: seen.add(y); st.append(y)
    faces = E.union_faces(P); segs, bad = E.edge_multiplicity(faces)
    neck = min(sum(cont.get((i, j), 0) for i in S for j in range(n) if j not in S)
               for r in range(1, n) for S in itertools.combinations(range(n), r) if 0 in S)
    return dict(lam=str(lam), tile=t, pieces=n, shift=sh, connected=len(seen) == n, manifold=not bad, faces=len(faces), neck=neck)

if __name__ == '__main__':
    k0, k1 = int(sys.argv[1]), int(sys.argv[2]); os.makedirs(os.path.join(K.HERE, 'data'), exist_ok=True)
    out = open(os.path.join(K.HERE, f'data/dense_{k0:03d}.jsonl'), 'w')
    lams = [Fr(-11, 24) + Fr(k, 480) for k in range(k0, k1)] + ([Fr(1, 10)] if k0 == 0 else [])
    for lam in lams:
        for t in 'ch': out.write(json.dumps(check(lam, t)) + '\n'); out.flush()
