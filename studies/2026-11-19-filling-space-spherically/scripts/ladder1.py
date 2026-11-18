# Filling Space Spherically, step 1 (DICTO 19 Nov 2026: "All from tetrahedron up" ... "But simpler first").
# One score: IQ = 36 pi V^2 / S^3 (sphere = 1). Pieces: the five Platonic solids and the five Fedorov parallelohedra.
# Controls: cube pi/6, tetrahedron pi/(6 sqrt3), octahedron pi/(3 sqrt3) (exact).
import itertools, math, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5**.5) / 2
def ps(t, even=False):
    out = set()
    for p in itertools.permutations(range(3)):
        if even and p not in [(0,1,2),(1,2,0),(2,0,1)]: continue
        for s in itertools.product([1,-1], repeat=3): out.add(tuple(s[i]*t[p[i]] for i in range(3)))
    return np.array(sorted(out), float)
def iq(P):
    h = ConvexHull(P); return 36*math.pi*h.volume**2/h.area**3
cube = ps((1,1,1)); octa = ps((1,0,0)); tet = np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)], float)
dod = np.vstack([cube, ps((0,1/phi,phi), even=True)]); ico = ps((0,1,phi), even=True)
rd = np.vstack([cube, 2*octa])
to = ps((0,1,2))
hexp = np.array([(math.cos(k*math.pi/3), math.sin(k*math.pi/3), z) for k in range(6) for z in (-.5, .5)])   # uniform: all edges 1
e = 3**.5   # elongated dodecahedron with all edges equal (sqrt3): RD cut at its equator, halves moved apart by e
ed = np.array([(x*a, y*b, z) for a in (1,-1) for b in (1,-1) for (x, y, z) in [(1,1,1+e/2),(1,1,-1-e/2)]] + [(s*2,0,t*e/2) for s in (1,-1) for t in (1,-1)] + [(0,s*2,t*e/2) for s in (1,-1) for t in (1,-1)] + [(0,0,2+e/2),(0,0,-2-e/2)], float)
rows = [('tetrahedron', tet, 0), ('cube', cube, 1), ('octahedron', octa, 0), ('dodecahedron', dod, 0), ('icosahedron', ico, 0),
        ('hexagonal prism (all edges equal)', hexp, 1), ('rhombic dodecahedron', rd, 1), ('elongated dodecahedron', ed, 1), ('truncated octahedron', to, 1)]
ctl = {'cube': math.pi/6, 'tetrahedron': math.pi/(6*3**.5), 'octahedron': math.pi/(3*3**.5)}
ok = True
for n, P, f in sorted(rows, key=lambda r: iq(r[1])):
    v = iq(P); c = ctl.get(n)
    if c is not None and abs(v - c) > 1e-12: ok = False
    print('%-38s IQ = %.6f %s%s' % (n, v, '  fills space' if f else '', '  (control %.12f)' % c if c else ''))
print('sphere'.ljust(38), 'IQ = 1')
print('FINAL ok' if ok else 'FINAL FAIL')
