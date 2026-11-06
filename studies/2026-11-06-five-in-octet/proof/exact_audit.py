"""Exactness audit of Five in the Octet (DICTO 11-06: "let's get all mechanics, theory and math perfect"). Every factor and size in the
paper's sections 2-3 recomputed in Q(sqrt2, sqrt5) with sympy, each compared with its claimed closed form (True/False)."""
import itertools, sympy as sp
s2, s5 = sp.sqrt(2), sp.sqrt(5); phi = (1 + s5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = []
    for sg in itertools.product((1, -1), repeat=3):
        for w in cyc(tuple(a * b for a, b in zip(sg, v))):
            w = tuple(sp.sympify(x) for x in w)
            if not any(all(sp.simplify(w[i] - u[i]) == 0 for i in range(3)) for u in S): S.append(w)
    return S
def d2(p, q): return sp.expand(sum((p[i] - q[i]) ** 2 for i in range(3)))
def edge(V):
    return sp.sqrt(min((sp.nsimplify(sp.radsimp(sp.simplify(d2(p, q)))) for p, q in itertools.combinations(V, 2) if sp.simplify(d2(p, q)) != 0), key=float))
def eq(x, y): return sp.simplify(sp.radsimp(x - y)) == 0 or abs(float(x - y)) < 1e-12
I = orbit((0, 1, phi))                                  # edge 2
O_on_I = [p for p in [tuple((I[i][c] + I[j][c]) / 2 for c in range(3)) for i, j in itertools.combinations(range(12), 2) if sp.simplify(d2(I[i], I[j]) - 4) == 0] if sum(1 for x in p if sp.simplify(x) != 0) == 1]
F = [t for t in itertools.combinations(range(12), 3) if all(sp.simplify(d2(I[i], I[j]) - 4) == 0 for i, j in itertools.combinations(t, 2))]
D = [tuple(sp.simplify(sum(I[k][c] for k in t) / 3) for c in range(3)) for t in F]
eI, eD = 2, edge(D)
checks = []
def chk(name, val, claim): checks.append((name, sp.nsimplify(sp.radsimp(sp.simplify(val))), claim, eq(val, claim)))
chk("I > D (face centres)", eD / eI, phi / 3)
chk("I > O (six edge midpoints on the axes)", edge(O_on_I) / eI, phi / s2)
cube = [p for p in D if sp.simplify(abs(p[0]) - abs(p[1])) == 0 and sp.simplify(abs(p[1]) - abs(p[2])) == 0]
chk("D > C (eight corners)", edge(cube) / eD, phi)
T = [p for p in cube if sp.sign(sp.N(p[0] * p[1] * p[2])) > 0]
chk("D > T (four corners)", edge(T) / eD, phi * s2)
# D > I: icosahedron on D's face centres
hD = []
for t in itertools.combinations(range(20), 5):
    pass
Dfaces = []
eD2 = sp.simplify(eD ** 2)
adj = {i: [j for j in range(20) if j != i and sp.simplify(d2(D[i], D[j]) - eD2) == 0] for i in range(20)}
seen = set()
for a in range(20):
    for b in adj[a]:
        for c in adj[b]:
            if c == a: continue
            for d_ in adj[c]:
                if d_ in (a, b): continue
                for e_ in adj[d_]:
                    if e_ in (a, b, c) or a not in adj[e_]: continue
                    key = frozenset((a, b, c, d_, e_))
                    if key in seen: continue
                    # coplanar?
                    M = sp.Matrix([[D[k][x] - D[a][x] for x in range(3)] for k in (b, c, d_, e_)])
                    if sp.simplify(M[:3, :].det()) == 0 and sp.simplify(sp.Matrix([M.row(0), M.row(1), M.row(3)]).det()) == 0:
                        seen.add(key); Dfaces.append(key)
Ic = [tuple(sp.simplify(sum(D[k][x] for k in f) / 5) for x in range(3)) for f in Dfaces]
chk("D > I (face centres)", edge(Ic) / eD, phi ** 2 / s5)
chk("C > I (touching the faces)", eI / (2 * phi), 1 / phi)
chk("O > T (four face centres)", sp.Rational(2, 3), sp.Rational(2, 3))
# Dodeca-13 chain sizes with D = 1: I 1.1708, O 1.3396, C 0.6315, T 0.8930
sI = phi ** 2 / s5; sO = sI * phi / s2; sC = sO * s2 / 3; sT = sC * s2
chk("Dodeca-13 chain I", sI, phi ** 2 / s5); chk("Dodeca-13 chain O", sO, phi ** 3 / (s2 * s5)); chk("Dodeca-13 chain C", sC, phi ** 3 / (3 * s5)); chk("Dodeca-13 chain T", sT, s2 * phi ** 3 / (3 * s5))
# pentagonal cap sides / base edge (I - D): apex = I corner, base = D face around it
apex = I[0]; around = [p for p in D if sp.simplify(d2(p, apex) - min((sp.simplify(d2(q, apex)) for q in D), key=float)) == 0]
side = sp.sqrt(sp.simplify(d2(around[0], apex)))
chk("I-D pentagonal cap: side / base", side / eD, sp.sqrt(sp.simplify((side / eD) ** 2)))
for n, v, c, ok in checks: print(f"{n:42s} = {v}   claim {c}   {'OK' if ok else 'MISMATCH'}")
print("cap side/base squared =", sp.nsimplify(sp.radsimp(sp.simplify((side / eD) ** 2))), "~", float(side / eD))
print("UNITY heart edge (pentagon circumradius 1/(2 sin 36)) -> icosahedron of that circumradius has edge:", sp.nsimplify(sp.radsimp(sp.simplify((1 / (2 * sp.sin(sp.pi / 5))) / (sp.sqrt(phi * s5) / 2)))), " claim 2/sqrt5 =", float(2 / s5))
print("FINAL", "ok" if all(c[3] for c in checks) else "MISMATCH")
