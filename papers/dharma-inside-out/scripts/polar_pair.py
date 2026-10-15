# Step 8 (DICTO's choice): the inner gap filled by the truncated icosidodecahedron pair instead of the Hecatodihedron. In the
# reversed chain the pair goes in reverse order too (DICTO): the disdyakis triacontahedron (DT) inside the truncated
# icosidodecahedron (TID). DT grows until it touches the inner dodecahedron, TID until it touches the icosidodecahedron; the
# play (x1.052) stays between the pair. Writes the chain, then the cone cut (polar_pieces.py) and render data.
import json, subprocess, sys, numpy as np
WHICH = sys.argv[1] if len(sys.argv) > 1 else 'tid'          # step 9 (DICTO): 'rid' = rhombicosidodecahedron inside deltoidal hexecontahedron
from scipy.spatial import ConvexHull
_argv = sys.argv; sys.argv = ['x']; exec(open('scripts/polar_round.py').read().split('def rad(V, u):')[0]); sys.argv = _argv
CL = json.load(open('data/reversed-chain.json')); D, ID = C['dodecahedron (inner)'], C['icosidodecahedron']
def grow(A, B): return min(-e[3] / max(A @ e[:3]) for e in ConvexHull(B).equations)
NX, NY = {'tid': ('disdyakis triacontahedron', 'truncated icosidodecahedron'), 'rid': ('rhombicosidodecahedron', 'deltoidal hexecontahedron')}[WHICH]
X, Y = SOL[NX], SOL[NY]; TAG = '' if WHICH == 'tid' else '-rid'
X = X / grow(D, X); Y = Y * grow(Y, ID)
lines = [f'{NX} scaled to touch the dodecahedron, {NY} to touch the icosidodecahedron; play between them x{grow(X, Y):.6f}',
         f'radii: D {np.linalg.norm(D, axis=1).max():.6f}, inner {np.linalg.norm(X, axis=1).min():.6f}-{np.linalg.norm(X, axis=1).max():.6f} '
         f'(inradius {min(-ConvexHull(X).equations[:, 3]):.6f}), outer inradius {min(-ConvexHull(Y).equations[:, 3]):.6f}, '
         f'ID inradius {min(-ConvexHull(ID).equations[:, 3]):.6f}']
print('\n'.join(lines)); open(f'data/polar-pair{TAG}.txt', 'w').write('\n'.join(lines) + '\n')
chain = [CL[0], [NX, X.tolist()], [NY, Y.tolist()]] + CL[1:]
json.dump(chain, open(f'data/reversed-chain-pair{TAG}.json', 'w'))
subprocess.run(['python3', 'scripts/polar_pieces.py', f'data/reversed-chain-pair{TAG}.json', f'data/polar-pair{TAG}-pieces.txt', f'data/polar-pair{TAG}-pieces.json'], check=True)
PC = json.load(open(f'data/polar-pair{TAG}-pieces.json'))
def solid(V):
    V = np.array(V); h = ConvexHull(V); F = []
    for e in h.equations:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(f) for f in F): continue
        Qp = V[idx]; c = Qp.mean(0); a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        F.append([idx[i] for i in np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a))])
    return {'v': V.tolist(), 'f': F, 'c': V.mean(0).tolist()}
R = {'layers': [{'name': k, 'pieces': [solid(V) for V in L]} for k, L in PC.items()], 'core': solid(chain[0][1]), 'outer': solid(chain[-1][1])}
json.dump(R, open(f'data/polar-pair{TAG}-render.json', 'w'))
