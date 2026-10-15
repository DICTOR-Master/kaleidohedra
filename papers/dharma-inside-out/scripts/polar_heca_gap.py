# Step 5c (DICTO's suggestion): does the Hecatodihedron (102 faces, from the original Dharma cycle) fit in the inner gap of the
# reversed chain, between the inner dodecahedron and the icosidodecahedron? Same test for the other original stations, for context.
# Range of scale s with inner D inside s*X and s*X inside ID (convex, so hull radial functions along many directions + all corners).
import json, sys, io, contextlib, numpy as np
from scipy.spatial import ConvexHull
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
CL = json.load(open('data/reversed-chain.json')); C = {n: np.array(V, float) for n, V in CL}
A, B = C['dodecahedron (inner)'], C['icosidodecahedron']
def rad(V, u):
    e = ConvexHull(V).equations; nu = e[:, :3] @ u; m = nu > 1e-12; return np.min(-e[m, 3] / nu[m])
lines = []
for st in stations:
    name, X = st[0], np.unique(np.round(np.array([[c.f() for c in v] for v in st[1]]), 9), axis=0)
    lo = max(np.linalg.norm(v) / rad(X, v / np.linalg.norm(v)) for v in A)   # inner D inside s*X: its corners suffice (both convex)
    hi = min(rad(B, v / np.linalg.norm(v)) / np.linalg.norm(v) for v in X)   # s*X's corners inside ID
    lines.append(f'{name}: {len(X)} corners; fits for scale {lo:.6f} .. {hi:.6f} '
                 + (f'YES, room x{hi / lo:.4f}' if lo <= hi + 1e-9 else 'NO'))
    print(lines[-1], flush=True)
open('data/polar-heca-gap.txt', 'w').write('\n'.join(lines) + '\n')
