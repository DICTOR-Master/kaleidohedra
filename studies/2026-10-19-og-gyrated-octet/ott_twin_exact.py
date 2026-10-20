# DICTO 2026-10-20: the DICTO OTT at a twin layer, exact in Q(sqrt5): its mirror image in an octahedron face x+y+z = R is the OTT
# turned 60 degrees about (1,1,1) (a true twin, as the OG), not a translate; twin OTTs meet on the whole face triangle; and that
# triangle against the OCD Stella's joint triangle on the same face (float, the Stella file is float).
import os, sys, json, itertools, numpy as np
ME = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(ME, '..', '2026-10-18-ocd-octet', 'scripts'))
from q5 import *
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
D = json.load(open(os.path.join(ME, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json'))); R = q(D['R'])
OT = [[q(c) for c in v] for v in json.load(open(os.path.join(ME, 'cut8-exact.json')))['V']]
N1 = [ONE, ONE, ONE]; TH = qr(Fr(2, 3))
def mir(v): s = qm(qs(dot(N1, v), R), TH); return [qs(x, s) for x in v]
t = [qm(R, TH)] * 3
F3 = lambda a: qr(Fr(a, 3)); R60 = [[F3(2), F3(-1), F3(2)], [F3(2), F3(2), F3(-1)], [F3(-1), F3(2), F3(2)]]
rot = lambda v: [dot(R60[i], v) for i in range(3)]
S = {tuple(v) for v in OT}
tw = {tuple(vsub(mir(v), t)) for v in OT}   # the twin brought back to the origin
ok(tw == {tuple(rot(v)) for v in OT}, 'the OTT mirrored in an octahedron face = the OTT turned 60 degrees about the face axis (a true twin)')
ok(tw != S, 'and not the OTT itself: the twin is not a translate')
tri = [v for v in OT if dot(N1, v) == R]
ok(len(tri) == 3 and all(tuple(mir(v)) == tuple(v) for v in tri), 'the face triangle (3 corners on the face) is fixed by the mirror: twin OTTs meet on the whole triangle')
# float: the OCD Stella's joint triangle on the same face
ST = np.array(json.load(open(os.path.join(ME, 'stella-37frame.json')))['V'], float); Rf = qf(R)
st = ST[np.abs(ST.sum(1) - Rf) < 1e-6]; ot = np.array([[qf(x) for x in v] for v in tri])
same = len(st) == 3 and all(np.min(np.linalg.norm(st - p, axis=1)) < 1e-6 for p in ot)
turned = len(st) == 3 and all(np.min(np.linalg.norm((2 * st.mean(0) - st) - p, axis=1)) < 1e-6 for p in ot)
print(f'      Stella joint triangle on the face: {len(st)} corners; same corners as the OTT triangle: {same}; the same triangle turned 180 degrees: {turned}')
