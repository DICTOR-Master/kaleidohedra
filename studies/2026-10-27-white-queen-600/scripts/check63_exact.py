"""Exact checks for paper #63 new parts, self-contained (Fractions, Q(sqrt5) as pairs). Reads only the study's JSON data."""
import json, math, sys
from fractions import Fraction as Fr
from itertools import combinations

SRC = sys.argv[1]; ATLAS = sys.argv[2]
S = json.load(open(SRC)); A = json.load(open(ATLAS))

class Q:
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * o.inv()
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        if s.a == 0 and s.b == 0: return 0
        if s.a == 0: return 1 if s.b > 0 else -1
        if s.b == 0: return 1 if s.a > 0 else -1
        if (s.a > 0) == (s.b > 0): return 1 if s.a > 0 else -1
        return (1 if s.a > 0 else -1) if s.a * s.a > 5 * s.b * s.b else (1 if s.b > 0 else -1)
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(5)
    def __repr__(s): return f"{s.a}+{s.b}r5"

def q(p): return Q(Fr(p[0]), Fr(p[1]))
V = [tuple(q(c) for c in v) for v in S["vertices_exact"]]
cells = S["cells"]; edges = S["edges"]
dirs = {k: tuple(q(c) for c in v["d_exact"]) for k, v in S["directions"].items()}
Z = Q(0)
def dot(x, y): return sum((a * b for a, b in zip(x, y)), Z)
def sub(x, y): return tuple(a - b for a, b in zip(x, y))
def sq(x): return dot(x, x)
def parallel(u, w):  # all 2x2 minors zero
    return all((u[i] * w[j] - u[j] * w[i]) == Z for i, j in combinations(range(4), 2))

print("atlas entries:", len(A), "keys:", sorted(A[0].keys()))
for o in A:
    if "face_sizes" not in o: print("  no face_sizes:", {k: o[k] for k in o if k in ("direction", "at_vertex_layer", "h", "V", "F", "note", "kind")})

# ---- 1. quads and squares at every atlas height ----
tot = {}; totq = 0; mism = []
for lab, d in dirs.items():
    h = [dot(v, d) for v in V]
    hs = sorted(set(h), key=float)
    samples = [(x, True) for x in hs if x.sign() >= 0]
    for a, b in zip(hs, hs[1:]):
        if (a + b).sign() >= 0: samples.append(((a + b) / Q(2), False))
    for hv, atv in samples:
        cls = {}; nq = 0
        for c in cells:
            below = [i for i in c if (h[i] - hv).sign() < 0]; above = [i for i in c if (h[i] - hv).sign() > 0]
            if len(below) == 2 and len(above) == 2:
                nq += 1
                def pt(bi, ai):
                    t = (hv - h[bi]) / (h[ai] - h[bi])
                    return tuple(V[bi][k] + t * (V[ai][k] - V[bi][k]) for k in range(4))
                P00, P01, P10, P11 = pt(below[0], above[0]), pt(below[0], above[1]), pt(below[1], above[0]), pt(below[1], above[1])
                # cycle P00-P10-P11-P01
                s = [sq(sub(P10, P00)), sq(sub(P11, P10)), sq(sub(P01, P11)), sq(sub(P00, P01))]
                dg = [sq(sub(P11, P00)), sq(sub(P10, P01))]
                par1 = parallel(sub(P10, P00), sub(P11, P01))  # sides 0 and 2
                par2 = parallel(sub(P11, P10), sub(P00, P01))  # sides 1 and 3
                eqd = dg[0] == dg[1]
                allsides = s[0] == s[1] == s[2] == s[3]
                opp = s[0] == s[2] and s[1] == s[3]
                if allsides and eqd: k = "square"
                elif opp and eqd: k = "rectangle"
                elif (par1 or par2) and eqd and not (par1 and par2): k = "isosceles trapezium"
                elif par1 and par2: k = "parallelogram"
                elif par1 or par2: k = "trapezium (not isosceles)"
                elif allsides: k = "rhombus"
                elif (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]): k = "kite"
                elif eqd: k = "general, equal diagonals"
                elif len(set(s)) < 4: k = "general, some equal sides"
                else: k = "general"
                # mid-cut test as in squares_midcuts.py
                mid = h[below[0]] == h[below[1]] and h[above[0]] == h[above[1]] and (h[below[0]] + h[above[0]]) == hv + hv
                if mid != (k == "square"): print("  MISMATCH midcut vs square", lab, float(hv), k, mid)
                cls[k] = cls.get(k, 0) + 1
        rec = [o for o in A if o["direction"] == lab and bool(o.get("at_vertex_layer")) == atv and abs(o["h"] - float(hv)) < 1e-9]
        at4 = rec[0].get("face_sizes", {}).get("4", 0) if rec else None
        if at4 != nq: mism.append((lab, atv, float(hv), nq, at4, len(rec)))
        totq += nq
        for k, n in cls.items(): tot[k] = tot.get(k, 0) + n
        if nq: print(f"{lab:>12} {'vertex' if atv else 'gap   '} h={float(hv):8.5f} quads {nq:3d} atlas {at4}  {cls}")
print("TOTAL quads", totq, "by kind", tot)
print("quad-count mismatches vs atlas:", mism)

# ---- 2. events along the six turnings: cells per event ----
N = [tuple(sum((V[i][k] for i in c), Z) for k in range(4)) for c in cells]
tot_ev = 0
for (An, a), (Bn, b) in combinations(dirs.items(), 2):
    ev = {}; flat = 0
    for n in N:
        al, be = dot(n, b), -dot(n, a); sa, sb = al.sign(), be.sign()
        if sa == 0 and sb == 0: flat += 1; continue
        if sa != 0 and sa == sb:
            if sa < 0: al, be = -al, -be
            key = next((k for k in ev if al * k[1] == k[0] * be), None)
            if key is None: key = (al, be); ev[key] = 0
            ev[key] += 1
    c2 = dot(a, b) * dot(a, b) / (dot(a, a) * dot(b, b))
    ang = math.degrees(math.acos(math.sqrt(float(c2))))
    evs = sorted(ev.items(), key=lambda kv: float(kv[0][1] / kv[0][0]))
    out = []
    for (al, be), cnt in evs:
        u = tuple(al * x + be * y for x, y in zip(a, b)); cc = dot(u, a) * dot(u, a) / (dot(u, u) * dot(a, a))
        front = sum(1 for n in N if dot(n, u).sign() > 0)
        out.append((round(math.degrees(math.acos(math.sqrt(float(cc)))), 4), cnt, cc, front))
    tot_ev += len(evs)
    print(f"{An} -> {Bn}: turn {ang:.6f} deg, events {len(evs)}, all-along side-on {flat}; (deg, cells side-on at event, cos2, front cells AT event) = {out}")
print("total events", tot_ev)

# ---- 3. dihedral and the (1+3r5)/8 claim ----
cosd = (1 + 3 * math.sqrt(5)) / 8
print("arccos(-(1+3r5)/8) =", math.degrees(math.acos(-cosd)), "; 180 - that =", 180 - math.degrees(math.acos(-cosd)),
      "; cos^2 =", (23 + 3 * math.sqrt(5)) / 32, "vs ((1+3r5)/8)^2 =", cosd ** 2)
# true dihedral of 600-cell from two adjacent cells: normals = cell centres sharing a triangle
c0 = cells[0]; t = set(c0[:3])
c1 = next(c for c in cells if c != c0 and t <= set(c))
n0, n1 = N[cells.index(c0)], N[cells.index(c1)]
cosang = float(dot(n0, n1)) / math.sqrt(float(sq(n0)) * float(sq(n1)))
print("angle between adjacent cell normals:", math.degrees(math.acos(cosang)), "dihedral = 180 - that =", 180 - math.degrees(math.acos(cosang)))

# ---- 4. Cleo core: neighbours of the top vertex at one height; octahedron edge ----
d = dirs["vertex-first"]; h = [dot(v, d) for v in V]
top = max(range(120), key=lambda i: float(h[i]))
nb = sorted({j for e in edges for j in e if top in e} - {top})
print("top vertex", top, "neighbours", len(nb), "heights", {repr(h[j]) for j in nb}, "edge^2", {repr(sq(sub(V[e[0]], V[e[1]]))) for e in edges[:50]})
print("1/phi =", (math.sqrt(5) - 1) / 2, "= half edge", (math.sqrt(5) - 1) / 2)
# shells by cell-centre height along the vertex direction (height of vertex = 2 scaling)
from collections import Counter
hc = Counter()
for n in N:
    hc[dot(n, d) / dot(d, d) * Q(2) / Q(4)] += 1
for k in sorted(hc, key=float, reverse=True): print("shell height", repr(k), float(k), hc[k])
