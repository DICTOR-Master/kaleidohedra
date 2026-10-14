# Tetrapods of one polyhedron (DICTO 2026-10-14: "same polyhedron, that's why I gave you two examples"). Four round one: a space-filling
# shape with four congruent faces in tetrahedral positions; for a parallelohedron (lattice tiling, face to face) the copy across each face
# is the translate taking the opposite face onto it, so the five are part of its tiling. Checked: each face has an opposite parallel
# congruent face, and the four translates do not overlap each other or the centre. DICTO · dictospheres.com
import itertools, json, sys
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
S = json.load(open(sys.argv[1]))
def faces(V, F):
    out = []
    for f in F:
        P = V[f]; n = np.zeros(3)
        for k in range(len(f)): n += np.cross(P[k], P[(k + 1) % len(f)])
        out.append((f, n / np.linalg.norm(n), P.mean(0)))
    return out
def overlap(P, Q):
    A = np.r_[ConvexHull(P).equations, ConvexHull(Q).equations]
    r = linprog(c=[0, 0, 0, -1], A_ub=np.c_[A[:, :3], np.ones(len(A))], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(None, 1)])
    return r.status == 0 and r.x[3] > 1e-7
out = []
for sid in ['TRUNCATED_OCTAHEDRON', 'BAIN_RD', 'BAIN_ED', 'RHOMBIC_DODECAHEDRON', 'REGULAR_HEX_ED', 'ELONGATED_DODECAHEDRON', 'CUBE', 'HEXAGONAL_PRISM', 'DICTO_SKEWED_RD', 'TRUNCATED_TETRAHEDRON']:
    if sid not in S: continue
    V = np.array(S[sid]['v'], float); V -= V.mean(0); Fs = faces(V, S[sid]['f'])
    vol = ConvexHull(V).volume
    sign = 1 if sum(n @ c for _, n, c in Fs) > 0 else -1
    Fs = [(f, sign * n, c) for f, n, c in Fs]
    found = None
    for quad in itertools.combinations(range(len(Fs)), 4):
        ns = [Fs[q][1] for q in quad]
        if not all(abs(ns[a] @ ns[b] + 1 / 3) < 1e-6 for a, b in itertools.combinations(range(4), 2)): continue
        trans = []
        for q in quad:
            f, n, c = Fs[q]
            opp = [c2 for f2, n2, c2 in Fs if np.allclose(n2, -n, atol=1e-6) and len(f2) == len(f)]
            if not opp: trans = None; break
            trans.append(c - opp[0])
        if trans is None: continue
        copies = [V + t for t in trans]
        ok = not any(overlap(a, b) for a, b in itertools.combinations(copies, 2)) and not any(overlap(V, c) for c in copies)
        found = dict(shape=sid, four_faces=len(Fs[quad[0]][0]), translates_fit=ok); break
    out.append(found or dict(shape=sid, four_faces=None, translates_fit=None))
for o in out: print(o)
json.dump(out, open('same-shape-four-round-one.json', 'w'), indent=1)
