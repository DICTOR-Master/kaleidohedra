# DICTO 2026-10-18 "construct an octet truss system from pieces available" -- STEP 1: the OCD exactly, and its octahedron.
# Takes the OCD (dual of the Hecatodihedron) exactly from the polar-dharma study; proves: the 8 joint hexagons lie on |x|+|y|+|z| = R,
# R = 2*phi/3 exactly; every OCD corner satisfies |x|+|y|+|z| <= R. -> data/step1-ocd-exact.json
import sys, io, os, contextlib, itertools, numpy as np
from scipy.spatial import ConvexHull
from q5 import *
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD); sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()): exec(open('scripts/polar.py').read())
os.chdir(here)
V = [[(x.a, x.b) for x in v] for v in dict(rev)['dual of the Hecatodihedron']]
Vf = np.array([[qf(x) for x in v] for v in V]); h = ConvexHull(Vf)
faces = []
for e in h.equations:
    idx = sorted(i for i in range(len(V)) if abs(Vf[i] @ e[:3] + e[3]) < 1e-7)
    if idx not in faces: faces.append(idx)
R = qm(qr(Fr(2, 3)), PHI)
l1 = lambda v: qa(qa(v[0] if sgn(v[0]) >= 0 else qn(v[0]), v[1] if sgn(v[1]) >= 0 else qn(v[1])), v[2] if sgn(v[2]) >= 0 else qn(v[2]))
on = [i for i, v in enumerate(V) if l1(v) == R]
inside = all(sgn(qs(R, l1(v))) >= 0 for v in V)
hexes = [f for f in faces if len(f) == 6]
joint = [f for f in hexes if all(i in on for i in f) and len({tuple(sgn(V[i][k]) for k in range(3)) for i in f}) == 1]
checks = dict(faces=len(faces), corners=len(V), hexagons=len(hexes), joint_hexagons_on_octa_faces=len(joint), corners_on_octa_surface=len(on),
              all_corners_inside_octa=inside, R_exact='2*phi/3', R=qf(R), octa_edge=qf(R) * 2 ** .5,
              octa_volume=4 / 3 * qf(R) ** 3, ocd_volume=h.volume, fill=h.volume / (4 / 3 * qf(R) ** 3))
print(checks); assert len(joint) == 8 and inside
save('step1-ocd-exact.json', dict(mark=MARK, step=1, note='OCD corners exact a|b (a + b*sqrt5); faces as corner indices; joint = the 8 hexagons on the octahedron |x|+|y|+|z| = 2phi/3',
     V=[[qs_(x) for x in v] for v in V], faces=faces, joint=joint, R=qs_(R), checks=checks))
