# projection_body.py: independent exact computation (our own code) for OpenAI, "A product counterexample to the simplex maximum for
# projection-body volume" (aiXiv 2610.00950, ai-authored; openai/math result 088). Claim (Theorem 1): K = T10 x T10 in R^20 has
# R(K) / R(T20) = 22 355 476 / 22 020 096 > 1, where R(K) = |Pi K| / |K|^(d-1).
# Method: by Cauchy's formula (paper Lemma 2) Pi P is the zonotope sum over facets of the segments [-g_F/2, g_F/2], g_F = (facet area)
# x (outward unit normal) = the facet's area-normal vector; a zonotope with generators g_i has volume = sum over d-subsets |det|.
# Area-normal vectors of a simplex conv(v_0..v_d): for the facet opposite v_i, g_i = -(1/(d-1)!) * (cofactor normal) computed exactly
# from the facet's vertices (signed (d-1)-volume vector = generalized cross product / (d-1)!). Exact rationals throughout.
# Controls: R(T2) must be 6 (triangle: Pi of a triangle is a hexagon; affine invariant value 6 = 3*2^2/2) and R(T3) = 18 (tetrahedra
# attain 18 = c3, Chen-Feng-Li-Xi-Xu); R is affine invariant (a sheared simplex gives the same value).
import itertools, math
from fractions import Fraction as F
def det(M):
    M = [[F(x) for x in r] for r in M]; n = len(M); d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f: M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return d
def simplex_area_normals(V):
    """outward area-normal vectors of the facets of the simplex with vertices V (d+1 points in R^d)"""
    d = len(V[0]); out = []; cen = [sum(F(v[k]) for v in V) / (d + 1) for k in range(d)]
    for i in range(d + 1):
        W = [V[j] for j in range(d + 1) if j != i]; E = [[F(W[k][c]) - F(W[0][c]) for c in range(d)] for k in range(1, d)]
        n = [(-1) ** c * det([[row[cc] for cc in range(d) if cc != c] for row in E]) for c in range(d)]   # generalized cross product
        g = [x / math.factorial(d - 1) for x in n]
        if sum(gc * (F(W[0][c]) - cen[c]) for c, gc in enumerate(g)) < 0: g = [-x for x in g]
        out.append(g)
    return out
def simplex_volume(V):
    d = len(V[0]); return abs(det([[F(V[k][c]) - F(V[0][c]) for c in range(d)] for k in range(1, d + 1)])) / math.factorial(d)
def zonotope_volume(G):
    d = len(G[0]); return sum(abs(det([G[i] for i in S])) for S in itertools.combinations(range(len(G)), d))
def R_simplex(V):
    G = simplex_area_normals(V); return zonotope_volume(G) / simplex_volume(V) ** (len(V[0]) - 1)
def T(d): return [tuple(0 for _ in range(d))] + [tuple(1 if c == k else 0 for c in range(d)) for k in range(d)]
r2, r3 = R_simplex(T(2)), R_simplex(T(3))
shear = [(0, 0, 0), (2, 1, 0), (1, 3, 1), (0, 1, 5)]
print(f'controls: R(T2) = {r2} (expect 6), R(T3) = {r3} (expect 18), R(sheared tetrahedron) = {R_simplex(shear)} (expect 18)', flush=True)
# K = T10 x T10: facets F x T10 and T10 x G; area-normal of F x T10 = (g_F, 0) * |T10|, and symmetrically
V10 = T(10); G10 = simplex_area_normals(V10); vol10 = simplex_volume(V10)
GK = [g + [F(0)] * 10 for g in G10] + [[F(0)] * 10 + g for g in G10]
GK = [[x * vol10 for x in g] for g in GK]
volK = vol10 ** 2
RK = zonotope_volume(GK) / volK ** 19
R20 = R_simplex(T(20))
ratio = RK / R20
print(f'R(T10 x T10) / R(T20) = {ratio} = {float(ratio):.9f}; claim 22355476/22020096 = {22355476/22020096:.9f}', flush=True)
ok = r2 == 6 and r3 == 18 and R_simplex(shear) == 18 and ratio == F(22355476, 22020096) and ratio > 1
print('FINAL ok: Theorem 1 confirmed exactly' if ok else 'FINAL FAIL')
