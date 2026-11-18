# Filling Space Spherically, step 2: tie-in with earlier work (DICTO 19 Nov: "Tying in with our earlier work").
# Second score: Mahler volume M = vol(P) vol(P polar) about the centre, divided by the sphere's (4pi/3)^2
# (Blaschke-Santalo: the ball is the maximum, so sphere = 1; aim 2: vol(polar) = canonical form at the point).
# Every piece here has its Santalo point at the centre by symmetry.
# New rungs from earlier work: the cube-octahedron line at mu = sqrt3 (flat counterpart of the DICTOsphere,
# best IQ on that line, studies/2026-11-18-fair-die-sphere) and Lucky 7 (fair 14-face die, mu_f = 1.7565821359).
# Controls: cube M = 32/3, octahedron 32/3, tetrahedron 128/9? -> computed as check of duality: M(P) = M(polar P).
import math, numpy as np
exec(open('ladder1.py').read().split('rows =')[0])
def polar(P):
    h = ConvexHull(P); pl = {}
    for eq in h.equations: pl[tuple(np.round(eq, 9))] = eq
    return np.array([eq[:3] / -eq[3] for eq in pl.values()])
def mahler(P): return ConvexHull(P).volume * ConvexHull(polar(P)).volume / (4*math.pi/3)**2
def co(mu):   # cube faces at distance 1 (normals axes), octahedron |x|+|y|+|z| <= mu (normals (+-1,+-1,+-1)/sqrt3): vertices = polar of the normals/d
    N = [np.array(v, float) for v in ps((1,0,0))] + [np.array(v, float)/mu for v in ps((1,1,1))]
    return polar(np.array(N))
rows = [('tetrahedron', tet, 0), ('cube', cube, 1), ('octahedron', octa, 0), ('dodecahedron', dod, 0), ('icosahedron', ico, 0),
        ('hexagonal prism (all edges equal)', hexp, 1), ('rhombic dodecahedron', rd, 1), ('elongated dodecahedron', ed, 1), ('truncated octahedron', to, 1),
        ('cube-octahedron line, mu = sqrt3 (flat DICTOsphere)', co(3**.5), 0), ('Lucky 7 (fair 14-face die)', co(1.7565821359), 0)]
ok = abs(mahler(cube) - 32/3/(4*math.pi/3)**2) < 1e-9 and abs(mahler(cube) - mahler(octa)) < 1e-9 and abs(mahler(dod) - mahler(ico)) < 1e-9 \
     and abs(mahler(rd) - mahler(polar(rd))) < 1e-9 and abs(iq(co(3**.5)) - 0.781639) < 1e-6 and abs(iq(co(1.7565821359)) - 0.781306) < 1e-6
for n, P, f in sorted(rows, key=lambda r: iq(r[1])):
    print('%-52s IQ = %.4f  Mahler/sphere = %.4f%s' % (n, iq(P), mahler(P), '  fills space' if f else ''))
print('%-52s IQ = 1       Mahler/sphere = 1' % 'sphere')
print('controls: cube M = 32/3, M(P) = M(polar) for cube/octa, dodeca/icosa, RD; IQ of mu = sqrt3 and Lucky 7 as in 2026-11-18')
print('FINAL ok' if ok else 'FINAL FAIL')
