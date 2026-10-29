# The star chain's scaling numbers, exactly (DICTO 10-30: "maybe the scaling numbers represent a new type of series or ratio").
# With t = 1 the chain S0 = TI, S(n+1) = hull of the feet of the perpendiculars to the faces of S(n), is the shape-only chain; for any t the
# chain is t^n times it. Everything stays in Q(sqrt5) (feet of perpendiculars from the origin to planes through Q(sqrt5) points), so the
# squared corner radii and the volumes of every step are exact numbers a + b sqrt5. Report, for 8 steps: R_n^2 (outer corner radius),
# the ratios R_(n+1)^2 / R_n^2, the volume ratios, and the four-step ratio.
import json, numpy as np, sympy as sp
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
r5 = sp.sqrt(5)
raw = json.load(open('data/stations-exact.json'))
V = [sp.Matrix([sp.Rational(a) + sp.Rational(b) * r5 for a, b in v]) for v in raw['TI']]
def facesx(V):
    Vf = np.array([[float(x) for x in v] for v in V]); h = ConvexHull(Vf); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = [i for i, p in enumerate(Vf) if abs(eq[:3] @ p + eq[3]) < 1e-8]
    return [ids for ids in out.values()], h
def foot(P3):
    a, b, c = P3; n = (b - a).cross(c - a); return sp.simplify(n * (n.dot(a)) / n.dot(n))
rows = []; S = V
for k in range(9):
    F, h = facesx(S)
    R2 = max((sp.nsimplify(sp.radsimp(sp.expand(v.dot(v)))) for v in S), key=lambda x: float(x))
    r2 = min((sp.nsimplify(sp.radsimp(sp.expand(v.dot(v)))) for v in S), key=lambda x: float(x))
    rows.append(dict(step=k, corners=len(S), R2=str(sp.radsimp(R2)), R2_num=float(R2), r2_corner_min=str(sp.radsimp(r2)), volume=float(h.volume)))
    if k == 8: break
    S = [sp.Matrix([sp.radsimp(sp.expand(x)) for x in foot([S[i] for i in ids[:3]])]) for ids in F]
for k in range(1, len(rows)):
    q = sp.radsimp(sp.nsimplify(sp.sympify(rows[k]['R2'])) / sp.nsimplify(sp.sympify(rows[k - 1]['R2'])))
    rows[k]['R2_ratio'] = str(sp.nsimplify(q)); rows[k]['R_ratio_num'] = float(sp.sqrt(q)); rows[k]['vol_ratio'] = rows[k]['volume'] / rows[k - 1]['volume']
four = sp.radsimp(sp.sympify(rows[4]['R2']) / sp.sympify(rows[0]['R2']))
out = dict(rows=rows, four_step_R2_ratio=str(sp.nsimplify(four)), four_step_R_ratio=float(sp.sqrt(four)),
           four_step_R_ratio_exact=str(sp.radsimp(sp.sqrt(sp.nsimplify(four)))))
print(json.dumps(out, indent=1)); json.dump(out, open('data/chain-exact.json', 'w'), indent=1)
