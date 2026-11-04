import json, numpy as np, math, os
from fractions import Fraction as F
from scipy.spatial import ConvexHull
s5 = math.sqrt(5); D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: float(F(a)) + float(F(b))*s5)(*x.split("|")) if isinstance(x, str) else float(x)
V = np.array([[q(x) for x in p] for p in D["V"]]); V -= V.mean(0); C = V[np.linalg.norm(V, axis=1) < .69]
for nm, P in (("og", V), ("cut", C)):
    os.makedirs(f"{nm}/data", exist_ok=True); json.dump({"ocd": P.tolist(), "T": [0, 0, 0]}, open(f"{nm}/data/network.json", "w"))
# Dehn input: faces as cyclic vertex lists
sol = {}
for nm, P in (("OG", V), ("cut OG (rectified truncated icosahedron)", C)):
    h = ConvexHull(P); pl = {}
    for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 6)), (eq, set()))[1].update(s)
    fs = []
    for eq, f in pl.values():
        f = list(f); c = P[f].mean(0); e1 = P[f[0]] - c; e2 = np.cross(eq[:3], e1)
        f.sort(key=lambda i: math.atan2((P[i] - c) @ e2, (P[i] - c) @ e1)); fs.append([int(i) for i in f])
    sol[nm] = {"v": P.tolist(), "f": fs}
json.dump({"order": list(sol), "solids": sol}, open("dehn-input.json", "w")); print("prepared")
