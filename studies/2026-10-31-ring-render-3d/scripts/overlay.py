# Check of a camera fit: draws the bipyramid's edges (red), apices A/B and the equator vertices E1-E3 on the photo.
# Output is photo-derived: write it outside the repository.  Usage: ~/geom/bin/python overlay.py photo.jpg cam.json out.jpg
import sys, json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, __import__('os').path.dirname(__file__))
import ringmesh as RM
photo, camp, out = sys.argv[1:4]
J = json.load(open(camp)); x = np.array(J['x'])
im = Image.open(photo).convert('RGB'); W0, H0 = im.size; d = ImageDraw.Draw(im)
rings, verts = RM.bipyramid()
# the fit centred the model on the mean of ring-mesh vertices; recompute that centre from the OBJ used
V = []
name = None
for line in open(sys.argv[4] if len(sys.argv) > 4 else 'bip.obj'):
    if line.startswith('o '): name = line[2:].strip()
    if line.startswith('v ') and name == 'Rings': V.append([float(v) for v in line.split()[1:4]])
ctr = np.array(V)[::7].mean(0)
L = np.linalg.norm(np.asarray(rings[0]['T'][1]) - rings[0]['T'][0]); sc = RM.S_M / L
Rm = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:6]; f = math.exp(x[6])
def pj(p):
    q = Rm @ (np.asarray(p) * sc - ctr) + t; return (f * q[0] / q[2] + W0 / 2, f * q[1] / q[2] + H0 / 2)
names = ['E1', 'E2', 'E3', 'A', 'B']
for i in range(5):
    for j in range(i + 1, 5):
        if {i, j} == {3, 4}: continue
        d.line([pj(verts[i]), pj(verts[j])], fill=(255, 0, 0), width=5)
for i, v in enumerate(verts):
    u = pj(v); d.ellipse([u[0] - 14, u[1] - 14, u[0] + 14, u[1] + 14], fill=(255, 255, 0)); d.text((u[0] + 16, u[1] - 10), names[i], fill=(255, 255, 0))
for r in rings:
    if r['central']:
        P = [pj(p) for p in r['T']]; d.line(P + [P[0]], fill=(0, 200, 255), width=3)
im.resize((W0 // 2, H0 // 2)).save(out, quality=85)
