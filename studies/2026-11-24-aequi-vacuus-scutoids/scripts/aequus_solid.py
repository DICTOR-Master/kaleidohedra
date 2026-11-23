"""Exact rational stand-in of an Aequus for the amber cell (24 Nov 2026).
Face planes u.x <= D: u = the exact direction vector in Q(phi)^3 (classify.py), D = the rational number nearest to d*|u| with
denominator <= 10^15 (d = the die's 60-digit depth for the unit normal).  Every vertex is then exact in Q(sqrt5).  All planes of one
orbit share u.u and D, so the stand-in keeps the frame symmetry exactly; its depths differ from the fair die's by < 1e-14, and its face
lattice is checked to be the fair die's (face count N, corner count, face side counts from the catalogue record).
build("aequus-<n>") with n = row of data/aequi_classification.csv (1-based app index)."""
import json, os, sys, csv
from collections import Counter
from fractions import Fraction as Fr
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("RESIN_DIR", os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
from resin import Q, polytope, dot
import classify as C
mp.mp.dps = 70
KIND = {3: "tri", 4: "quad", 5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non", 10: "dec"}

MODE = os.environ.get("AEQ_MODE", "stand")
BOX_R = Fr(1, 10**18)
_rand = {}
def depth_value(k, exact_mp):
    """stand: rational stand-in (denominator <= 10^15).  box: centre c (denominator <= 10^22) with the ball [c - r, c + r], r = 1e-18.
    pt:SEED: the exact random point c + r*(2u - 1), u a 64-bit random rational (same for every plane of orbit k)."""
    if MODE == "stand": return Q(Fr(str(mp.nstr(exact_mp, 40))).limit_denominator(10**15))
    c = Fr(str(mp.nstr(exact_mp, 45))).limit_denominator(10**22)
    assert abs(mp.mpf(c.numerator)/c.denominator - exact_mp) < mp.mpf(10)**-20
    if MODE == "box":
        import certify
        from flint import arb, fmpq
        return certify.HQ(c, 0, z=arb(fmpq(c.numerator, c.denominator)) + arb(0, arb(fmpq(1, 10**18))))
    if MODE.startswith("pt:"):
        import random
        if k not in _rand:
            rng = random.Random(f"{MODE}-{k}"); _rand[k] = Fr(2*rng.getrandbits(64) - 2**64 + 1, 2**64)
        return Q(c + BOX_R*_rand[k])
    raise SystemExit("AEQ_MODE")

def build(name):
    n = int(name.split("-")[1])
    D = json.load(open(os.path.join(HERE, "../src/dice.json"))); e = D["dice"][n - 1]
    row = [r for r in csv.DictReader(open(os.path.join(HERE, "../data/aequi_classification.csv"))) if int(r["n"]) == n][0]
    ED = C.exact_dirs(D["dirs"])
    rec = json.load(open(os.path.join(HERE, "../..", "2026-11-19-aequi-complete" if e["s"] == "A" else "2026-11-20-aequi-two-placements", "data/dice", row["record"])))
    d60 = [mp.mpf(x) for x in rec["depths_60_digits"]]
    # orbit order of the record = order of the app's depths (as matched in classify.py)
    dep = []
    for x in e["d"]:
        j = [t for t in range(len(d60)) if abs(d60[t] - x) < 1e-9 and t not in dep]
        dep.append(j[0] if len(j) == 1 else len(dep))
    H = []
    for k, oi in enumerate(e["o"]):
        for i in D["groups"][e["g"]][oi]["dirs"]:
            u = [Q(c.a, c.b) for c in ED[i][0]]
            uu = dot(u, u); nrm = mp.sqrt(mp.mpf(uu.a.numerator)/uu.a.denominator + mp.mpf(uu.b.numerator)/uu.b.denominator*mp.sqrt(5))
            H.append((u, depth_value(k, d60[dep[k]]*nrm), D["groups"][e["g"]][oi]["lab"]))
    P = polytope(H)
    V = P["verts"]; faces, planes = [], []
    import numpy as np, math
    F = np.array([[float(x) for x in v] for v in V])
    for t, vs in P["faces"].items():
        faces.append((vs, KIND.get(len(vs), f"{len(vs)}-gon"))); planes.append((H[t][0], H[t][1]))
    got = sorted(Counter(len(vs) for vs, k in faces).items())
    want = Counter()
    for s in e["f"]:
        c, g = s.split("×"); want[int(g.split("-")[0])] += int(c)
    assert len(faces) == e["N"] and len(V) == e["c"] and got == sorted(want.items()), ("face lattice differs", len(faces), len(V), got, sorted(want.items()))
    # outward orientation of each face cycle
    for q, (vs, k) in enumerate(faces):
        a, b, c = V[vs[0]], V[vs[1]], V[vs[2]]
        from resin import cross, vsub
        if dot(cross(vsub(b, a), vsub(c, a)), planes[q][0]).sign() < 0: faces[q] = (vs[::-1], k)
    return dict(V=V, faces=faces, planes=planes, name=name)

if __name__ == "__main__":
    for nm in sys.argv[1:]:
        S = build(nm); print(nm, len(S["V"]), "vertices", dict(Counter(k for f, k in S["faces"])), "faces: face lattice = the fair die's")
