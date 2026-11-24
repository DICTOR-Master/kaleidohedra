# Exact check of the Aequi silences that are not composite (accidental), of every near miss (1e-11 < e_k < 1e-5), and of the
# grey case (triakis tetrahedron, k = 17). E_k = sum_{f,g} P_k(n_f.n_g) is computed exactly: n_f = q_f/|q_f| with q_f in Q(sqrt5)^3,
# |q_f|^2 = u_f^2 s_f with s_f in {1, 2, 3, phi+2} (or 11 for the triakis tetrahedron). Odd powers of t = q_f.q_g/(|q_f||q_g|) carry
# sqrt(s_f s_g); the numbers sqrt(product of a subset of {2, 3, phi+2}) are linearly independent over Q(sqrt5) (Q(sqrt2, sqrt3, sqrt5)
# is multiquadratic and cannot contain the cyclic quartic field Q(sqrt(phi+2))), so E_k = 0 iff every radical coefficient is 0.
# E_k >= 0 with equality iff silent (Delsarte-Goethals-Seidel). Usage: python exact_check.py post.json OUT.json
import os, sys, json, itertools, importlib.util
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tacitus as T

class Q5:
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = o if isinstance(o, Q5) else Q5(o); d = o.a * o.a - 5 * o.b * o.b; return s * Q5(o.a / d, -o.b / d)
    def __pow__(s, m):
        r = Q5(1)
        for _ in range(m): r = r * s
        return r
    def iszero(s): return s.a == 0 and s.b == 0
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s): return "%s + %s*sqrt5" % (s.a, s.b)
PHI = Q5(Fr(1, 2), Fr(1, 2)); IPHI = Q5(Fr(-1, 2), Fr(1, 2))
SQ = {"2": Q5(2), "3": Q5(3), "s": PHI + 2, "11": Q5(11)}

def legendre(k):
    """coefficients a_m of P_k(t) = sum a_m t^m."""
    P = [[Fr(1)], [Fr(0), Fr(1)]]
    for j in range(1, k):
        a = [Fr(0)] + [Fr(2 * j + 1) * c for c in P[j]]; b = [Fr(j) * c for c in P[j - 1]] + [Fr(0)] * 2
        P.append([(x - y) / (j + 1) for x, y in zip(a, b)])
    return P[k]

def norm_split(N):
    """|q|^2 = u^2 * s; returns (u, radical key)."""
    for u, key in ((Q5(1), ()), (Q5(2), ()), (Q5(1), ("2",)), (Q5(1), ("3",)), (Q5(1), ("s",)), (Q5(1), ("11",))):
        s = Q5(1)
        for r in key: s = s * SQ[r]
        if ((u * u) * s + (N * -1)).iszero(): return u, key
    raise ValueError(N)

def exact_energy(Q, k):
    """E_k as {radical key: Q5}, Q a list of exact vectors."""
    a = legendre(k); dot = lambda x, y: x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
    info = [norm_split(dot(q, q)) for q in Q]
    out = {}
    for f, g in itertools.product(range(len(Q)), repeat=2):
        uf, kf = info[f]; ug, kg = info[g]; d = dot(Q[f], Q[g])
        key = tuple(sorted(set(kf) ^ set(kg))); com = Q5(1)
        for r in set(kf) & set(kg): com = com * SQ[r]       # sqrt(s_f s_g) = com * sqrt(key)
        Nf = (uf * uf) * Q5(1); Ng = (ug * ug) * Q5(1)
        for r in kf: Nf = Nf * SQ[r]
        for r in kg: Ng = Ng * SQ[r]
        NN = Nf * Ng; tot = Q5(0); totodd = Q5(0)
        for m, c in enumerate(a):
            if c == 0: continue
            if m % 2 == 0: tot = tot + Q5(c) * (d ** m) / (NN ** (m // 2))
            else: totodd = totodd + Q5(c) * (d ** m) / ((NN ** (m // 2)) * (uf * ug) * com)   # times 1/sqrt(key)
        out[()] = out.get((), Q5(0)) + tot
        if not totodd.iszero():
            kk = key
            if kk == (): out[()] = out[()] + totodd
            else:
                # 1/sqrt(key) = sqrt(key)/prod(key): store as coefficient of sqrt(key)
                p = Q5(1)
                for r in kk: p = p * SQ[r]
                out[kk] = out.get(kk, Q5(0)) + totodd / p
    return out

def exact_dirs():
    spec = importlib.util.spec_from_file_location("g", os.path.join(T.ST, "2026-11-24-aequi-certify-extend/scripts/groups.py"))
    gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
    cand = []
    for t in [(Q5(1), Q5(0), Q5(0)), (Q5(1), Q5(1), Q5(1)), (Q5(1), Q5(1), Q5(0)), (Q5(0), PHI, Q5(1)), (Q5(0), IPHI, PHI),
              (Q5(1), PHI, IPHI), (Q5(0), Q5(1), PHI), (Q5(0), PHI, IPHI), (PHI, Q5(1), IPHI)]:
        for s in itertools.product((1, -1), repeat=3):
            q = [x * c for x, c in zip(t, s)]
            for r in range(3): cand.append(q[r:] + q[:r])
    out = []
    for v in gm.DIRS:
        for q in cand:
            f = np.array([float(x) for x in q]); f /= np.linalg.norm(f)
            if np.abs(f - v).max() < 1e-9: out.append(q); break
    assert len(out) == len(gm.DIRS)
    return out

def is_zero(E): return all(v.iszero() for v in E.values())
def approx(E):
    return sum(float(v) * float(np.sqrt(float(np.prod([float(SQ[r]) for r in key])) if key else 1.0)) for key, v in E.items())

if __name__ == "__main__":
    post = json.load(open(sys.argv[1])); X = exact_dirs(); out = []; bad = 0
    for o in post:
        Q = [X[i] for i in o["idx"]]; N = len(Q)
        for k, c in o["covers"].items():
            if c is None:
                E = exact_energy(Q, int(k)); z = is_zero(E); bad += not z
                out.append(dict(name=o["name"], label=o["label"], k=int(k), kind="accidental silence", exact_zero=z))
        for k, e in o["small"]:
            E = exact_energy(Q, k); z = is_zero(E); bad += z
            out.append(dict(name=o["name"], label=o["label"], k=k, kind="near miss", e=e, exact_zero=z, exact_e=approx(E) / N ** 2))
    # grey case: triakis tetrahedron normals = corners of the truncated tetrahedron, (3,1,1) with an even number of minus signs
    tt = [p for p in set(itertools.permutations((3, 1, 1))) ]
    Qt = []
    for p in tt:
        for s in itertools.product((1, -1), repeat=3):
            if s.count(-1) % 2 == 0: Qt.append([Q5(a * b) for a, b in zip(p, s)])
    assert len(Qt) == 12
    E = exact_energy(Qt, 17); out.append(dict(name="triakis tetrahedron", k=17, kind="grey", exact_zero=is_zero(E), exact_e=approx(E) / 144)); bad += is_zero(E)
    tri = [r for r in map(json.loads, open(os.path.join(HERE, "../data/poly.jsonl"))) if r["name"] == "triakis tetrahedron"][0]
    json.dump(out, open(sys.argv[2], "w"), indent=0)
    acc = [r for r in out if r["kind"] == "accidental silence"]; nm = [r for r in out if r["kind"] == "near miss"]
    print("accidental silences checked exactly:", len(acc), "zero:", sum(r["exact_zero"] for r in acc))
    print("near misses checked exactly:", len(nm), "nonzero:", sum(not r["exact_zero"] for r in nm),
          "| smallest exact e: %.4g" % min(r["exact_e"] for r in nm))
    print("triakis tetrahedron k=17:", out[-1])
    print("FINAL ok" if bad == 0 else "FINAL FAIL %d mismatches" % bad)
