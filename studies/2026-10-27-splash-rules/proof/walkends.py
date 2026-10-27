# Swap Rule proof, lemma W: the walk range (DICTO 2026-10-27). Exact (sympy), symbolic in q = s*2/3 and lam.
# A power cell C_i = {p : pow_i(p) <= pow_j(p) for all j}. For sites j_1..j_m and weights y_k > 0 with sum y_k (c_jk - c_i) = 0,
# summing y_k (pow_jk(p) - pow_i(p)) >= 0 removes p:  sum y_k (|c_jk - c_i|^2 - w_jk + w_i) >= 0. If that constant is < 0 the cell is empty.
# (1) octahedral hole, its 6 tetrahedral neighbours in its own gap:            empty for lam > 1/3 + q/16      (every stacking)
# (2) octahedral hole with tetrahedral holes straight above AND below (both layers of its gap c, as in the cubic stacking):
#                                                                              empty for lam > 9q/16
# (3) tetrahedral hole next to a layer of type h (3 octahedral holes of its gap, 3 of the next gap): empty for lam < -1/3 - 3q/16
# (4) tetrahedral hole next to a layer of type c (3 of its gap, 1 straight over it in the next gap):  empty for lam < -1/4 - 3q/16
import sympy as sp
from swapgeom import POS, Qf
q, lam = sp.symbols('q lam', positive=True)
def d2(ci, cj): return sp.Rational(Qf((cj[0] - ci[0], cj[1] - ci[1]))) + q * (cj[2] - ci[2]) ** 2
def comb(name, ci, wi, J, want):
    mom = [sum(y * (cj[r] - ci[r]) for cj, wj, y in J) for r in range(3)]
    tot = sum(y for _, _, y in J)
    const = sp.expand(sum(y * (d2(ci, cj) - wj + wi) for cj, wj, y in J) / tot)
    ok = all(m == 0 for m in mom) and sp.simplify(const - want) == 0
    print(f'{"PASS" if ok else "FAIL"} {name}: moments {mom}, condition {const} >= 0', flush=True); return ok
R = sp.Rational
A, B, C = [(sp.Rational(x[0]), sp.Rational(x[1])) for x in (POS['A'], POS['B'], POS['C'])]
def pt(xy, dx, dy, z): return (xy[0] + dx, xy[1] + dy, z)
oc = pt(C, 0, 0, R(1, 2))
tX = [pt(A, 1, 1, R(3, 4)), pt(A, 1, 0, R(3, 4)), pt(A, 0, 1, R(3, 4))]          # A points round C=(2/3,2/3): (1,1),(1,0),(0,1)
tY = [pt(B, 0, 0, R(1, 4)), pt(B, 1, 0, R(1, 4)), pt(B, 0, 1, R(1, 4))]          # B points round C: (1/3,1/3),(4/3,1/3),(1/3,4/3)
res = [comb('(1) oct vs its 6 tets', oc, 0, [(c, lam, 1) for c in tX + tY], R(1, 3) + q / 16 - lam)]
res.append(comb('(2) oct vs tets straight above/below', oc, 0, [(pt(C, 0, 0, R(5, 4)), lam, 1), (pt(C, 0, 0, R(-1, 4)), lam, 1)], R(9, 16) * q - lam))
tt = pt(A, 0, 0, R(3, 4))                                                          # tet over layer 0 (A), next to layer 1 (B)
octs0 = [pt(C, -1, -1, R(1, 2)), pt(C, 0, -1, R(1, 2)), pt(C, -1, 0, R(1, 2))]   # C points round A: (-1/3,-1/3),(2/3,-1/3),(-1/3,2/3)
octs1h = [pt(C, -1, -1, R(3, 2)), pt(C, 0, -1, R(3, 2)), pt(C, -1, 0, R(3, 2))]  # layer 2 = A (h at layer 1): octs of gap 1 over C
res.append(comb('(3) tet next to an h layer', tt, lam, [(c, 0, 3) for c in octs0] + [(c, 0, 1) for c in octs1h], R(1, 3) + R(3, 16) * q + lam))
res.append(comb('(4) tet next to a c layer', tt, lam, [(c, 0, 1) for c in octs0] + [(pt(A, 0, 0, R(3, 2)), 0, 1)], R(1, 4) + R(3, 16) * q + lam))
print(f'TOTAL {sum(res)} PASS, {len(res) - sum(res)} FAIL')
