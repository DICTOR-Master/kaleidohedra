# Interlock study (DICTO, 2026-10-16): the two cycles as one buildable, readable solid. Step 1: both chains in one frame.
# Original: one turn of the Spheres of Dharma, I .. I*phi^3 (exact stations from the polar Dharma study). Flipped: its polar image
# in the toggle sphere rho^2 = phi^2/4 (the ends setting: the cycles share I and D), inner to outer, as a chain for the cone cut.
import sys, io, os, contextlib, json, numpy as np
from scipy.spatial import ConvexHull
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
p = (1 + 5 ** .5) / 2; r2 = p * p / 4
orig = []
for n, V in stations:
    A = np.array([[c.f() for c in v] for v in V]); _, keep = np.unique(np.round(A, 9), axis=0, return_index=True)   # dedupe, keep full precision
    X = A[np.sort(keep)]; orig.append((n, X[ConvexHull(X).vertices]))
def polar(X):
    pl = []
    for e in ConvexHull(X).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    return np.array([r2 * e[:3] / -e[3] for e in pl])
names = ['dodecahedron (inner)', 'rhombic triacontahedron', 'dual of the Hecatodihedron', 'pentakis dodecahedron', 'icosahedron', 'icosidodecahedron', 'dodecahedron (phi^3)']
# polar reverses the order: the flipped chain inner to outer is the polar of the original outer to inner
flip = [(nm, polar(X)) for nm, (n, X) in zip(['dodecahedron (inner)', 'icosidodecahedron', 'dual of the Hecatodihedron', 'pentakis dodecahedron', 'icosahedron', 'rhombic triacontahedron', 'dodecahedron (phi^3)'], orig[::-1])]
json.dump([[n.replace(' (phi^3)', ' (phi^3)'), X.tolist()] for n, X in orig], open('data/orig-chain.json', 'w'))
json.dump([[n, X.tolist()] for n, X in flip], open('data/flip-ends-chain.json', 'w'))
for n, X in flip: print(f'flipped {n:28s} corners {len(X):3d} radius {np.linalg.norm(X, axis=1).min():.4f}..{np.linalg.norm(X, axis=1).max():.4f}')
