# DICTO · dictospheres.com — every solid drawn in the Dehn Canon figures, from exact corners or exact half-spaces, with the
# exact checks that tie each drawing to the paper: edge counts, edge lengths squared and edge angles (named exactly, exact3d.ANG),
# volumes and heights where the paper states them. Any mismatch stops the script.
import json, os
from fractions import Fraction as Fr
from exact3d import Q5, R5, PHI, G, q, dot, sub, cross, det3, from_vertices, from_halfspaces, perms3, signs, uniq

HERE = os.path.dirname(os.path.abspath(__file__))
E3 = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
DIAG = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
RDN = [(a, b, 0) for a in (1, -1) for b in (1, -1)] + [(a, 0, b) for a in (1, -1) for b in (1, -1)] + \
      [(0, a, b) for a in (1, -1) for b in (1, -1)]


def cube(): return from_halfspaces(E3, [1] * 6)
def rd(): return from_halfspaces(RDN, [2] * 12)
def cube_rd(s, c): return from_halfspaces(E3 + RDN, [s] * 6 + [c] * 12)
def cube_oct(t): return from_halfspaces(E3 + DIAG, [1] * 6 + [t] * 8)
def octa(): return from_halfspaces(DIAG, [1] * 8)
def tetra(): return from_vertices([(-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)])


def rt():                                   # the 30 two-fold directions of the Lean file Dehn7Gold.lean (rtZ), offset 16
    Z = [(4, 0, 0), (-4, 0, 0), (0, 4, 0), (0, -4, 0), (0, 0, 4), (0, 0, -4)]
    a, b = R5 - 1, R5 + 1
    for sa in (1, -1):
        for sb in (1, -1):
            for sc in (1, -1): Z += perms3((a * sa, b * sb, Q5(2 * sc)))
    Z = uniq([q(*z) for z in Z]); assert len(Z) == 30 and all(dot(z, z) == 16 for z in Z)
    return from_halfspaces(Z, [16] * 30)


def rhombohedron(U, V, W):                  # the parallelepiped on three edge vectors (goldProlateSet_eq, goldOblateSet_eq)
    U, V, W = q(*U), q(*V), q(*W); P = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1): P.append(tuple(a * x + b * y + c * z for x, y, z in zip(U, V, W)))
    return from_vertices(P)


def prolate(): return rhombohedron((0, 1, PHI), (0, -1, PHI), (PHI, 0, 1))
def oblate(): return rhombohedron((0, 1, PHI), (0, -1, PHI), (1, PHI, 0))


def dodeca():                               # Theorem 8 (i): (±2, ±2, ±2) and cyclic (0, ±(1 + √5), ±(√5 − 1))
    P = signs(q(2, 2, 2))
    for v in signs(q(0, 1 + R5, R5 - 1)): P += perms3(v)
    return from_vertices(uniq(P))


def icosa():                                # Theorem 8 (ii): cyclic (0, ±2, ±(1 + √5))
    P = []
    for v in signs(q(0, 2, 1 + R5)): P += perms3(v)
    return from_vertices(uniq(P))


def snap(x):                                # a float corner coordinate of pieces.json as p/4 + r√5/4, checked to 5e-9
    best = min(((p, r) for p in range(-40, 41) for r in range(-20, 21)), key=lambda pr: abs(pr[0] / 4 + pr[1] * 5 ** .5 / 4 - x))
    assert abs(best[0] / 4 + best[1] * 5 ** .5 / 4 - x) < 5e-9, x
    return Q5(Fr(best[0], 4), Fr(best[1], 4))


def word(name):                             # CLEO, AXE, FUJI: corners of [11] (study 2026-10-14-axe-cleo-fuji), made exact
    D = json.load(open(os.path.join(HERE, 'pieces.json')))[name]
    return from_vertices([tuple(snap(x) for x in v) for v in D['vertices']])


A0, B0, C0, D0, D1 = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)     # Theorem 1 (h)
def hilbert_T(): return from_vertices([A0, B0, C0, D0])
def hilbert_T2(): return from_vertices([A0, B0, C0, D1])


def vol_tet(P):
    a, b, c, d = [q(*p) for p in P]
    v = det3([sub(b, a), sub(c, a), sub(d, a)]); return Fr(abs(v.a), 6) if v.b == 0 else None


g2 = G * G                                  # g² = (3 − √5)/2
EXPECT = {
    'cube': {('π/2', Q5(4)): 12},
    'tetrahedron': {('arccos(1/3)', Q5(8)): 6},                                  # 6 · 2√2 ⊗ arccos(1/3) = 12√2
    'octahedron': {('π − arccos(1/3)', Q5(2)): 12},                              # 12 · √2 ⊗ (π − arccos(1/3)) = −12√2
    'dodecahedron': {('π − α', (2 * R5 - 2) * (2 * R5 - 2)): 30},               # 30 · (2√5 − 2) ⊗ (π − α)
    'icosahedron': {('π − γ', Q5(16)): 30},                                      # 30 · 4 ⊗ (π − γ) = −120 ⊗ γ
    'CLEO': {('α', Q5(1)): 3, ('β', g2): 3},                                    # Table 2
    'AXE': {('α', g2): 1, ('β', Q5(1)): 4, ('γ', Q5(1)): 1},
    'FUJI': {('π − ε', Q5(1)): 6, ('γ', Q5(1)): 3, ('ε', g2): 3},
    'T': {('π/2', Q5(1)): 3, ('arccos(1/√3)', Q5(2)): 3},                        # Theorem 6′ proof
    "T'": {('π/4', Q5(1)): 2, ('π/2', Q5(1)): 1, ('π/2', Q5(2)): 2, ('π/3', Q5(3)): 1},
}


def check(name, S):
    got = S.classes(); exp = EXPECT[name]
    assert got == exp, (name, got, exp)
    return f'{name}: {len(S.V)} corners, {len(S.F)} faces, {len(S.E)} edges, edge classes as in the paper'


def check_zero(name, S, nf=None):          # every dihedral angle a rational multiple of π (Theorem 7 (i))
    assert all(e[4] for e in S.E), (name, {e[3] for e in S.E})
    if nf: assert len(S.F) == nf, (name, len(S.F))
    return f'{name}: {len(S.V)} corners, {len(S.F)} faces, every edge angle in ℚπ ({sorted({e[3] for e in S.E})})'


def check_co(t, S):                         # cube ∩ octahedron at t: edges and the coefficient 12√2(2t − 3) (Theorem 8 (iii))
    t = Fr(t); got = S.classes()
    if t == 1: assert got == EXPECT['octahedron']; return 'cube ∩ octahedron t = 1: the octahedron'
    exp = {('π − arccos(1/√3)', Q5(2 * (t - 1) ** 2)): 24, ('π − arccos(1/3)', Q5(2 * (2 - t) ** 2)): 12}
    assert got == exp, (t, got); assert len(S.F) == 14, len(S.F)
    # π − arccos(1/√3) ≡ ½ arccos(1/3) and π − arccos(1/3) ≡ −arccos(1/3) mod ℚπ, since 2 arccos(1/√3) = π − arccos(1/3)
    coef = 24 * (t - 1) / 2 - 12 * (2 - t)           # in units of √2 ⊗ arccos(1/3)
    assert coef == 12 * (2 * t - 3)
    return f'cube ∩ octahedron t = {t}: 14 faces, coefficient 12√2(2t − 3) = {coef}√2'


if __name__ == '__main__':
    print(check('cube', cube())); print(check('tetrahedron', tetra())); print(check('octahedron', octa()))
    print(check('dodecahedron', dodeca())); print(check('icosahedron', icosa()))
    for w in ['CLEO', 'AXE', 'FUJI']: print(check(w, word(w)))
    print(check_zero('rhombic dodecahedron', rd(), 12)); print(check_zero('cube ∩ RD', cube_rd(1, Fr(3, 2)), 18))
    print(check_zero('rhombic triacontahedron', rt(), 30)); print(check_zero('prolate', prolate(), 6)); print(check_zero('oblate', oblate(), 6))
    for t in [1, Fr(9, 8), Fr(3, 2), Fr(8783, 5000)]: print(check_co(t, cube_oct(t)))
    print(check('T', hilbert_T()), vol_tet([A0, B0, C0, D0])); print(check("T'", hilbert_T2()), vol_tet([A0, B0, C0, D1]))
