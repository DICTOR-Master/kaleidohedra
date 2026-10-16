# Line-up C, step 2a: both chains in one frame and their cone-cut pieces (float; the exact check rebuilds every corner).
# Original: I ⊂ ID ⊂ D ⊂ TI ⊂ 3·I ⊂ RT ⊂ I·φ³ (true corners only). Reversed: its polar in the toggle sphere rho² = φ²/4 (ends setting), inner to
# outer. Cone cut (the Kion construction of Theaetetus, as in Inverted Shells and P4): each layer A → B is cut by the cones from the centre over the
# faces of the inner solid A; a face whose cone holds no volume of the layer (it lies in B's boundary) gives no piece.
# -> data/orig-chain.json, flip-ends-chain.json, orig-pieces.json, flip-ends-pieces.json (same formats as studies/2026-10-16-interlock)
import os, io, sys, contextlib, json, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
LINEUP = sys.argv[1] if len(sys.argv) > 1 else 'C'            # 'B': P4's line-up (the Hecatodihedron), a known-case check that must give 174 and 154 pieces
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
p = (1 + 5 ** .5) / 2; r2 = p * p / 4
st = {n: np.array([[x.f() for x in v] for v in V]) for n, V in stations}
def true_corners(X):
    h = ConvexHull(X); keep = [i for i in range(len(X)) if np.linalg.matrix_rank(np.array([e[:3] for e in h.equations if abs(X[i] @ e[:3] + e[3]) < 1e-7]), tol=1e-6) == 3]
    return X[keep]
names = ['icosahedron', 'icosidodecahedron', 'dodecahedron', 'truncated icosahedron', '3·icosahedron', 'rhombic triacontahedron', 'icosahedron (phi^3)']
if LINEUP == 'B': names[4] = 'Hecatodihedron'
orig = [(n, true_corners(st[n] if n != '3·icosahedron' else 3 * st['icosahedron'])) for n in names]
def planes(X):
    pl = []
    for e in ConvexHull(X).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    return np.array(pl)
def polar(X): return np.array([r2 * e[:3] / -e[3] for e in planes(X)])
fnames = ['dodecahedron (inner)', 'icosidodecahedron', 'dodecahedron (third)', 'pentakis dodecahedron', 'icosahedron', 'rhombic triacontahedron', 'dodecahedron (phi^3)']
flip = [(nm, true_corners(polar(X))) for nm, (n, X) in zip(fnames, orig[::-1])]
def cone_pieces(chain):
    out = {}
    for (na, A), (nb, B) in zip(chain, chain[1:]):
        L = []; HB = planes(B)
        for e in planes(A):                                  # a face of A: n.x + d = 0, A inside n.x + d <= 0
            idx = [i for i in range(len(A)) if abs(A[i] @ e[:3] + e[3]) < 1e-7]; F = A[idx]; c = F.mean(0)
            a = F - c; ang = np.arctan2(a @ np.cross(e[:3], a[0] / np.linalg.norm(a[0])), a @ (a[0] / np.linalg.norm(a[0]))); F = F[np.argsort(ang)]
            H = [np.r_[-e[:3], -e[3]]]                       # outside A's face plane
            for i in range(len(F)):                          # cone sides through the centre and each edge of the face, the face's centre inside
                n = np.cross(F[i], F[(i + 1) % len(F)]); n = n if n @ c < 0 else -n; H.append(np.r_[n, 0.0])
            H = np.vstack([np.array(H), HB]); nrm = np.linalg.norm(H[:, :3], axis=1)
            r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
            if r.status != 0 or r.x[3] < 1e-7: continue
            V = HalfspaceIntersection(H, r.x[:3]).intersections; V = np.unique(np.round(V, 10), axis=0)
            if len(V) >= 4 and ConvexHull(V).volume > 1e-11: L.append(V.tolist())
        out[f'{na} -> {nb}'] = L
    return out
OP, FP = cone_pieces(orig), cone_pieces(flip)
for (na, A), (nb, B) in zip(orig, orig[1:]):                 # each layer's pieces fill it
    s = sum(ConvexHull(np.array(V)).volume for V in OP[f'{na} -> {nb}']); assert abs(s - (ConvexHull(B).volume - ConvexHull(A).volume)) < 1e-9, (na, nb)
for (na, A), (nb, B) in zip(flip, flip[1:]):
    s = sum(ConvexHull(np.array(V)).volume for V in FP[f'{na} -> {nb}']); assert abs(s - (ConvexHull(B).volume - ConvexHull(A).volume)) < 1e-9, (na, nb)
if LINEUP == 'B': print('B check:', sum(len(v) for v in OP.values()), 'original,', sum(len(v) for v in FP.values()), 'reversed (P4: 174, 154)'); sys.exit()
json.dump([[n, X.tolist()] for n, X in orig], open('data/orig-chain.json', 'w')); json.dump([[n, X.tolist()] for n, X in flip], open('data/flip-ends-chain.json', 'w'))
json.dump(OP, open('data/orig-pieces.json', 'w')); json.dump(FP, open('data/flip-ends-pieces.json', 'w'))
out = ['DICTO · dictospheres.com', 'Line-up C: chains and cone-cut pieces (float; layers filled to 1e-9)']
out += [f'  original {k}: {len(v)} pieces' for k, v in OP.items()] + [f'  original turn: {sum(len(v) for v in OP.values())} pieces']
out += [f'  reversed {k}: {len(v)} pieces' for k, v in FP.items()] + [f'  reversed turn: {sum(len(v) for v in FP.values())} pieces']
print('\n'.join(out)); open('data/lineup-c-pieces.txt', 'w').write('\n'.join(out) + '\n')
