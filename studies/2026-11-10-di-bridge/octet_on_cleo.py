"""D–I bridge B, step 3 (DICTO 10 Nov: "go on with the octet above the CLEOs"). Exact construction:
- a CLEO: apex A = the lowest corner of a crossed Dogstar cube (a dodecahedron corner); its base corners = the dodecahedron corners at
  distance 1 from A (dodecahedron edges) inside that cube; they must lie in the plane n.x = c = phi/(2 sqrt3);
- the octet of edge phi/sqrt2 has its octahedra axis-parallel; an octahedron with its bottom face (normal -n) centred on the CLEO base
  has centre O = B + (phi/6)(1,1,1); Pacioli's icosahedron in it = O + (1/(2 phi)) x cyclic(0, ±1, ±phi) (or the mirror cyclic(0, ±phi, ±1)).
Test: is the icosahedron's face in the plane exactly the CLEO's base? Usage: python octet_on_cleo.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import phi, CUBE, DOD
n = np.ones(3) / 3 ** .5; c = phi / (2 * 3 ** .5); e = 1 / phi; h = phi / 2
ctr = phi * np.array([1., 0, 0]); A = ctr - h * np.ones(3)                 # Dogstar cell (odd), its lowest corner
Dverts = np.vstack([DOD + phi * np.array(p) for p in itertools.product(range(-1, 3), repeat=3) if sum(p) % 2 == 0])
Dverts = np.unique(np.round(Dverts, 12), axis=0)
nb = [v for v in Dverts if abs(np.linalg.norm(v - A) - 1) < 1e-9 and np.all(np.abs(v - ctr) <= h + 1e-9)]
print(f'dodecahedron corners one edge from A inside the Dogstar cube: {len(nb)}; their levels {np.round([v @ n for v in nb], 9)} (plane {c:.9f})')
base = np.array(nb)
be = sorted(np.linalg.norm(base[a] - base[b]) for a, b in itertools.combinations(range(len(base)), 2))
print(f'base edges {np.round(be, 9)} (1/phi = {e:.9f}); apex height {c - A @ n:.9f}')
B = base.mean(0); O = B + phi / 6 * np.ones(3)
def cyc(v): return [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]
res = []
for name, base_v in (('cyclic(0,±1,±φ)', (0, 1, phi)), ('mirror cyclic(0,±φ,±1)', (0, phi, 1))):
    I = np.array([O + (1 / (2 * phi)) * np.array(w) * np.array(sg) for w in cyc(base_v) for sg in itertools.product((1, -1), repeat=3)])   # 11-10 fix: signs on every coordinate
    I = np.unique(np.round(I, 12), axis=0)
    ed = sorted({round(float(np.linalg.norm(p - q)), 9) for p, q in itertools.combinations(I, 2)})[0]
    onO = all(abs(np.abs(p - O).sum() - h * 1.0) < 1e-9 for p in I)                  # corners on the octahedron |x|+|y|+|z| = phi/2
    inpl = I[np.abs(I @ n - c) < 1e-9]
    d = max(min(np.linalg.norm(q - b) for q in inpl) for b in base) if len(inpl) == 3 else float('inf')
    print(f'{name}: icosahedron edge {ed:.9f} (1/phi), corners on the octahedron {onO}, corners in the plane {len(inpl)}, max distance to the CLEO base corners {d:.2e}')
    res.append(d)
ok = len(base) == 3 and all(len(np.unique(np.round(np.array([O + (1 / (2 * phi)) * np.array(w) * np.array(sg) for w in cyc((0, 1, phi)) for sg in itertools.product((1, -1), repeat=3)]), 9), axis=0)) == 12 for _ in [0]) and abs(be[0] - e) < 1e-9 and abs(be[-1] - e) < 1e-9
match = ok and min(res) < 1e-9
print('RESULT:', 'icosahedron face = CLEO base EXACTLY (true face-to-face meeting)' if match else 'no exact face match', '| CLEO base exact:', ok)
print('FINAL ok' if ok else 'FINAL FAIL: CLEO base not as expected')
