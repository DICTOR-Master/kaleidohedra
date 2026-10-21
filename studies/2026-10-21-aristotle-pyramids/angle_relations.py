# DICTO 2026-10-21, "what could Aristotle have meant": the face pyramids of the Platonic solids (cone from the centre over one face).
# Side edge = line from the centre to a corner; the pyramids round it are the solid's faces at that corner (3, 3, 4, 3, 5).
# Step 1: their dihedral angles, and integer relations among the irrational ones (PSLQ, 80 digits; evidence, the proof of independence
# is the Conway-Radin-Sadun theorem on angles with rational squared cosines, cited in the write-up).
from mpmath import mp, acos, sqrt, pi, pslq, mpf, degrees
mp.dps = 80
a = acos(mpf(1) / 3); tD = acos(-1 / sqrt(5)); tI = acos(-sqrt(5) / 3)
P = {'cube pyramid': {'base edge': pi / 4, 'side edge': 2 * pi / 3},
     'tetrahedron pyramid': {'base edge': a / 2, 'side edge': 2 * pi / 3},
     'octahedron pyramid': {'base edge': (pi - a) / 2, 'side edge': pi / 2},
     'dodecahedron pyramid': {'base edge': tD / 2, 'side edge': 2 * pi / 3},
     'icosahedron pyramid (Cleo-Icos)': {'base edge': tI / 2, 'side edge': 2 * pi / 5}}
for k, v in P.items(): print(f'{k:32s}', {e: round(float(degrees(x)), 4) for e, x in v.items()})
for name, vec in [('a, tD, tI, pi', [a, tD, tI, pi]), ('tD, tI, pi', [tD, tI, pi]), ('a, tD, pi', [a, tD, pi]), ('a, tI, pi', [a, tI, pi])]:
    print(name, '-> integer relation:', pslq(vec, maxcoeff=10 ** 9, maxsteps=10 ** 7))
