"""Near-miss sequences from the EKP / Kaleidohedra / golden-cycle papers, each computed two ways (exact integers).
A: closed form as printed (or as implied by the printed rule); B: independent simulation / enumeration."""
from fractions import Fraction
from itertools import combinations_with_replacement
N = 25
ok = True
def check(name, a, b):
    global ok
    same = a == b
    ok &= same
    print(f"{name}: {'agree' if same else 'DISAGREE'}")
    print("  ", ", ".join(map(str, a)))

# 1. Chain of Karma (Golden Cycle book ch. 1 s.2): pieces after n steps.
#    A: printed closed form 13^n icosahedra + 100(13^n - 1)/12 gap pieces.
A = [13**n + Fraction(100 * (13**n - 1), 12) for n in range(N)]
assert all(x.denominator == 1 for x in A); A = [int(x) for x in A]
#    B: substitution: every icosahedron -> Lotus seed = 12 I(1) + I(1/phi) + 60 AXE + 20 FUJI + 20 CLEO; gaps kept whole.
B = []; ico, axe, fuji, cleo = 1, 0, 0, 0
for n in range(N):
    B.append(ico + axe + fuji + cleo)
    ico, axe, fuji, cleo = 13 * ico, axe + 60 * ico, fuji + 20 * ico, cleo + 20 * ico
check("Chain of Karma total pieces, n>=0", A, B)
assert A[1:4] == [113, 1569, 20497], A[1:4]   # printed check values
check("Chain of Karma gap pieces, n>=0", [100 * (13**n - 1) // 12 for n in range(N)], [b - 13**m for m, b in enumerate(B)])

# 2. Dodecahedral Chain (ch. 1 s.5): D(phi^(2n)) = Chain-filled I(phi^(2n-1)) + 12 J2 + 30 AXE + 20 CLEO.
A2 = [(28 * 13**n + 161) // 3 for n in range(N)]
assert all((28 * 13**n + 161) % 3 == 0 for n in range(N))
B2 = [B[n] + 62 for n in range(N)]
check("Dodecahedral Chain pieces, n>=0", A2, B2)
assert A2[:3] == [63, 175, 1631], A2[:3]

# 3. Dehn-zero integer truncations of T(n) (Space-Fillers book ch. 2 s.3): cuts k_i>=0, sum k_i = n, k_i + k_j <= n,
#    up to order, not the whole tetrahedron removed. A: brute enumeration; B: A001400(n) - 1 via partitions into <= 4 parts.
def brute(n):
    c = 0
    for k in combinations_with_replacement(range(n + 1), 4):
        if sum(k) == n and all(k[i] + k[j] <= n for i in range(4) for j in range(i + 1, 4)) and sorted(k)[-1] < n:
            c += 1
    return c
def parts_le4(n):  # coefficient of x^n in 1/((1-x)(1-x^2)(1-x^3)(1-x^4))
    p = [1] + [0] * n
    for m in (1, 2, 3, 4):
        for i in range(m, n + 1): p[i] += p[i - m]
    return p[n]
A3 = [brute(n) for n in range(1, N + 1)]; B3 = [parts_le4(n) - 1 for n in range(1, N + 1)]
check("Dehn-zero integer truncations of T(n), n>=1", A3, B3)
assert A3[1:5] == [1, 2, 4, 5]   # printed: 1, 2, 4, 5 pieces at n = 2..5

print("FINAL ok" if ok else "FINAL FAIL")
