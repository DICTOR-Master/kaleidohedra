# Exact edge classes of the ORIGINAL OG (all 102 corners): lengths, dihedrals (cos) in exact form. DICTO 5 Nov 2026 (Pentagons for the Kites, before release).
import json, math, numpy as np, sympy as sp
from fractions import Fraction as F
from scipy.spatial import ConvexHull
s5 = sp.sqrt(5); D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: sp.Rational(F(a)) + sp.Rational(F(b))*s5)(*x.split("|")) if isinstance(x, str) else sp.nsimplify(x)
VE = [[q(x) for x in p] for p in D["V"]]
c = [sum(v[i] for v in VE)/len(VE) for i in range(3)]; VE = [[sp.nsimplify(v[i] - c[i]) for i in range(3)] for v in VE]
Vf = np.array([[float(x) for x in v] for v in VE]); keep = np.linalg.norm(Vf, axis=1) < 99
VE = [v for v, k in zip(VE, keep) if k]; Vf = Vf[keep]; print("corners", len(VE), flush=True)
h = ConvexHull(Vf); planes = {}
for eq, s in zip(h.equations, h.simplices): planes.setdefault(tuple(np.round(eq, 6)), set()).update(s)
faces = list(planes.values()); print("faces", len(faces), sorted({len(f) for f in faces}), flush=True)
def nrm(f):
    f = list(f); a, b, cc = [sp.Matrix(VE[i]) for i in f[:3]]; n = (b - a).cross(cc - a)
    ctr = sum((sp.Matrix(VE[i]) for i in f), sp.zeros(3, 1))
    if float(n.dot(ctr)) < 0: n = -n
    return n
N = [nrm(f) for f in faces]; cls = {}
for i, j in [(i, j) for i in range(len(faces)) for j in range(i + 1, len(faces))]:
    e = faces[i] & faces[j]
    if len(e) != 2: continue
    a, b = list(e); L2 = sp.nsimplify(sp.expand(sum((VE[a][k] - VE[b][k])**2 for k in range(3))))
    cosang = sp.radsimp(sp.expand(N[i].dot(N[j]))/sp.sqrt(sp.expand(N[i].dot(N[i]))*sp.expand(N[j].dot(N[j]))))
    key = (len(faces[i]) if len(faces[i]) <= len(faces[j]) else len(faces[j]), max(len(faces[i]), len(faces[j])))
    k2 = (key, round(float(L2), 9), round(float(cosang), 9)); cls.setdefault(k2, [0, L2, cosang]); cls[k2][0] += 1
for (key, l, cv), (n, L2, cn) in sorted(cls.items()):
    th = math.pi - math.acos(cv)
    print(f"faces {key}: {n} edges, length^2 = {sp.simplify(L2)}, cos(outer normal angle) = {sp.nsimplify(sp.simplify(cn))}, interior dihedral {math.degrees(th):.6f} deg", flush=True)
print("FINAL ok")
