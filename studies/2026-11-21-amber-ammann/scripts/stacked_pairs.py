"""Stacked same-type pairs never occur in the cut-and-project tilings (24 Nov 2026; reproduces the referee report of 24 Nov, section 5).
Exact in Q(sqrt5) with sympy (independent of the study's own Q class).

Rule of tiling.py: the tile n + C_A (A a triple of the six star vectors) is present iff gamma lies in the OPEN parallelepiped
W(n, A) = pi'(n + 1_A/2) + sum_{b not in A} (-1/2, 1/2) e_b'.
Two translates of one cell A stacked across a face (the face spanned by A minus {l}) differ by +-e_l in space.  Because
Z^6 -> R^3, m -> sum m_i e_i is injective (checked: the 6x6 matrix [e_i ; e_i'] has nonzero determinant, and a lattice vector with
sum m_i e_i = 0 also has sum m_i e_i' = 0 by Galois conjugation), the two tiles are n + C_A and n + e_l + C_A (up to naming).
Both are present only if gamma is in W(n, A) and in W(n, A) + e_l', i.e. only if e_l' is in sum_{b not in A} (-1, 1) e_b'.
Check: for all 20 triples A and all 3 choices of l in A, write e_l' = sum_{b not in A} t_b e_b' exactly; the absolute values {|t_b|}
are (1, phi, phi) or (1/phi, 1/phi, 1), so some |t_b| = 1 exactly, e_l' lies outside the open set, and the two open windows are
disjoint for every shift gamma.
Control: data/patch.json (the paper's patch) has no shared face between two tiles of the same triple.
Last line FINAL ok only if every check holds."""
import itertools, json, os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
r5 = sp.sqrt(5); phi = (1 + r5)/2
E = [(0, 1, phi), (0, -1, phi), (1, phi, 0), (-1, phi, 0), (phi, 0, 1), (-phi, 0, 1)]   # as tiling.py
conj = lambda x: sp.expand(sp.sympify(x).subs(r5, -r5))
EP = [tuple(conj(x) for x in v) for v in E]
ok = True
M6 = sp.Matrix([list(E[i]) + list(EP[i]) for i in range(6)])
d6 = sp.simplify(M6.det())
print(f"det [e_i | e_i'] (6x6) = {d6}; nonzero: {d6 != 0} -> Z^6 -> R^3 injective")
ok &= d6 != 0
# sanity: sum e_i e_i'^T = 0 (parallel and perpendicular spaces orthogonal), as tiling.py
S = sp.zeros(3, 3)
for i in range(6): S += sp.Matrix(E[i]) * sp.Matrix(EP[i]).T
ok &= all(sp.simplify(x) == 0 for x in S); print(f"sum e_i e_i'^T = 0: {all(sp.simplify(x) == 0 for x in S)}")
T1 = sorted([1, phi, phi], key=float); T2 = sorted([1/phi, 1/phi, 1], key=float)
seen = {}; n_cases = 0; n_one = 0
for A in itertools.combinations(range(6), 3):
    B = [b for b in range(6) if b not in A]
    MB = sp.Matrix([list(EP[b]) for b in B]).T          # columns e_b'
    for l in A:
        t = MB.LUsolve(sp.Matrix(EP[l]))
        t = [sp.nsimplify(sp.radsimp(sp.simplify(x)), [r5]) for x in t]
        assert all(sp.simplify(MB*sp.Matrix(t) - sp.Matrix(EP[l])) == sp.zeros(3, 1) for _ in [0])
        av = sorted([sp.Abs(x) for x in t], key=float)
        is1 = sp.simplify(av[0] - T1[0]) == 0 and sp.simplify(av[1] - T1[1]) == 0 and sp.simplify(av[2] - T1[2]) == 0
        is2 = sp.simplify(av[0] - T2[0]) == 0 and sp.simplify(av[1] - T2[1]) == 0 and sp.simplify(av[2] - T2[2]) == 0
        has1 = any(sp.simplify(sp.Abs(x) - 1) == 0 for x in t)
        inside = all(sp.simplify(sp.Abs(x) - 1).is_negative for x in t)   # open set test, exact
        n_cases += 1; n_one += has1
        key = "(1, phi, phi)" if is1 else "(1/phi, 1/phi, 1)" if is2 else "OTHER"
        seen[key] = seen.get(key, 0) + 1
        print(f"A={A} l={l}: e_l' = " + " + ".join(f"({sp.simplify(x)}) e{b}'" for x, b in zip(t, B)) + f"  |t| {key}; inside open set: {inside}")
        ok &= (is1 or is2) and has1 and not inside
print(f"cases {n_cases} (20 triples x 3); |t| patterns {seen}; a coefficient exactly 1 in {n_one}/{n_cases}")
ok &= n_cases == 60 and n_one == 60 and "OTHER" not in seen
P = json.load(open(os.path.join(HERE, "../data/patch.json"))); tiles = P["tiles"]
same = sum(1 for t1, t2, _ in P["shared"] if tiles[t1]["A"] == tiles[t2]["A"])
print(f"control: patch walls {len(P['shared'])}, between two tiles of one triple (stacked): {same}")
ok &= len(P["shared"]) == 998 and same == 0
print("RESULT: stacked same-type pairs never occur in the cut-and-project tilings, for every gamma" if ok else "RESULT: check failed")
print("FINAL ok" if ok else "FINAL FAILED")
