# Step 2b: inside one antiprism, does each top-edge tetrahedron X join a bottom-edge one Y (sharing a face) into one convex piece Z, so
# that the antiprism = Cleo-Ico + 3 congruent Z? Both turning senses tried.
import itertools, json, sys, numpy as np
from scipy.spatial import ConvexHull
exec(open('core_step2.py').read().split("sA = sum")[0].replace("S = json.load(open(sys.argv[1])); KIT = json.load(open(sys.argv[2]))", "S = json.load(open(sys.argv[1]))"))
X0, Y0, Cl = X[:3], Y[:3], C[0]
def shared(P, Q): return sum(1 for p in P for q in Q if np.linalg.norm(p - q) < 1e-9)
out = []
for sense in (0, 1):
    Zs = []
    for x in X0:
        ys = [y for y in Y0 if shared(x, y) == 3]
        y = sorted(ys, key=lambda y: tuple(np.round(y[2], 6)))[sense % len(ys)]
        Zs.append(np.unique(np.round(np.vstack([x, y]), 9), axis=0))
    conv = [abs(vol(z) - vol(x) - vol(yy)) < 1e-9 for z, x, yy in zip(Zs, X0, [None] * 3)] if False else None
    ok = []
    for z, x in zip(Zs, X0):
        ys = [y for y in Y0 if shared(x, y) == 3]
        ok.append(any(abs(vol(z) - vol(x) - vol(y)) < 1e-9 for y in ys))
    used = len({tuple(np.round(z[-1], 6)) for z in Zs})
    L = sorted(round(np.linalg.norm(a - b), 6) for a, b in itertools.combinations(Zs[0], 2))
    out.append(f'sense {sense}: Z convex {sum(ok)} of 3; Z has {len(Zs[0])} vertices, vol {vol(Zs[0]):.6f}, distances {L}')
print('\n'.join(out))
