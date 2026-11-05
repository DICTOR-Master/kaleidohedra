# The Golden Ladder, closing chapter (DICTO 5 Nov 2026). E8 from the icosians (Conway-Sloane SPLAG ch. 8):
# the icosian ring with the norm N(q) = a + b*sqrt5 read as a + b. Its 240 minimal vectors are the 120 unit icosians
# (a 600-cell of radius 1) and the 120 units divided by phi (a 600-cell of radius 1/phi). Check: the 240 vectors, embedded in 8D by
# x -> (sqrt(w1) x, sqrt(w2) sigma(x)) with w1, w2 = (1 +- 1/sqrt5)/2 (sigma: sqrt5 -> -sqrt5), all have norm 1, pairwise
# products in {0, +-1/2, +-1}, each has 56 neighbours at 1/2 -- the E8 root system (unique with these properties in 8D).
import numpy as np, itertools
s5 = 5**0.5; phi = (1 + s5)/2
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: out.append([v[k] for k in p])
    return out
# units as (rational, sqrt5) pairs per coordinate so sigma is exact: phi = 1/2 + sqrt5/2, 1/phi = -1/2 + sqrt5/2
PHI, IPHI, ONE, HALF, ZERO = (0.5, 0.5), (-0.5, 0.5), (1, 0), (0.5, 0), (0, 0)
U = []
for i in range(4):
    for sg in (1, -1):
        v = [ZERO]*4; v[i] = (sg, 0); U.append(v)
for sg in itertools.product((1, -1), repeat=4): U.append([(0.5*x, 0) for x in sg])
for v in even_perms([PHI, ONE, IPHI, ZERO]):
    for sg in itertools.product((1, -1), repeat=3):
        k = 0; w = []
        for c in v:
            if c == ZERO: w.append(ZERO)
            else: w.append((c[0]/2*sg[k], c[1]/2*sg[k])); k += 1
        U.append(w)
U = {tuple(tuple(np.round(c, 12)) for c in u) for u in U}; U = [list(u) for u in U]; print("unit icosians", len(U))
val = lambda u, sgn: np.array([a + sgn*b*s5 for a, b in u])
def times_iphi(u):   # u / phi = u * (sqrt5 - 1)/2 : (a + b r)(-1/2 + r/2) = (-a/2 + 5b/2) + (a/2 - b/2) r
    return [(-a/2 + 5*b/2, a/2 - b/2) for a, b in u]
V = U + [times_iphi(u) for u in U]
w1, w2 = (1 + 1/s5)/2, (1 - 1/s5)/2
X = np.array([np.concatenate([w1**0.5*val(u, 1), w2**0.5*val(u, -1)]) for u in V])
r4 = np.round(np.linalg.norm(np.array([val(u, 1) for u in V]), axis=1), 9)
print("4D radii", sorted(set(r4)), [int((r4 == x).sum()) for x in sorted(set(r4))], "ratio", max(r4)/min(r4))
n8 = np.round(np.linalg.norm(X, axis=1)**2, 9); print("8D norms", sorted(set(n8)))
G = np.round(X @ X.T, 9); vals = sorted(set(G.ravel())); print("inner products", vals)
print("neighbours at 1/2 per vector", sorted(set((G == 0.5).sum(1))))
print("rank", np.linalg.matrix_rank(X))
for name, S in (("radius 1", [val(u, 1) for u in U]), ("radius 1/phi", [val(times_iphi(u), 1) for u in U])):
    S = np.array(S); D = np.linalg.norm(S[:, None] - S[None], axis=2); np.fill_diagonal(D, 9); m = D.min()
    print(f"{name}: 120 points, nearest {m:.6f} = radius/phi: {abs(m - np.linalg.norm(S[0])/phi) < 1e-9}, 12 neighbours each: {set((np.abs(D - m) < 1e-9).sum(1))}, edges {(np.abs(D - m) < 1e-9).sum()//2}")

# ---- figure: the E8 Petrie (Coxeter-plane) picture, each root coloured by its 600-cell (radius 1 gold, radius 1/phi violet)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
g = np.random.default_rng(1).normal(size=8); pos = X[X @ g > 0]
simple = [r for r in pos if not any(np.allclose(r, a + b) for a in pos for b in pos if a is not b)]
simple = []
for r in pos:
    if not any(np.allclose(r - a, b) for a in pos for b in pos): simple.append(r)
print("simple roots", len(simple))
C = np.eye(8)
for a in simple: C = C @ (np.eye(8) - 2*np.outer(a, a)/(a @ a))
w, v = np.linalg.eig(C); k = np.argmin(np.abs(np.angle(w) - 2*np.pi/30)); e1, e2 = np.real(v[:, k]), np.imag(v[:, k])
e1 /= np.linalg.norm(e1); e2 -= (e2 @ e1)*e1; e2 /= np.linalg.norm(e2)
print("Coxeter element order 30:", np.allclose(np.linalg.matrix_power(C, 30), np.eye(8)))
P2 = np.c_[X @ e1, X @ e2]; rad = np.round(np.linalg.norm(P2, axis=1), 6); print("rings", sorted(set(rad)), [int((rad == x).sum()) for x in sorted(set(rad))])
big = r4 > 0.8
fig, ax = plt.subplots(figsize=(7.5, 7.8), facecolor="white")
for i in range(len(X)):
    for j in range(i + 1, len(X)):
        if G[i, j] == 0.5: ax.plot(*np.c_[P2[i], P2[j]], color="#999", lw=0.12, alpha=0.5, zorder=1)
ax.scatter(*P2[big].T, s=38, c="#d4a020", edgecolors="#6b4e00", linewidths=0.5, zorder=3, label="600-cell of radius 1 (120 roots)")
ax.scatter(*P2[~big].T, s=38, c="#7a5fb0", edgecolors="#2e1f55", linewidths=0.5, zorder=3, label="600-cell of radius 1/φ (120 roots)")
ax.set_aspect("equal"); ax.axis("off"); ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.07), ncol=1, frameon=False, fontsize=9)
ax.set_title("E8: 240 roots, two golden 600-cells", fontsize=12)
fig.text(0.5, 0.01, "DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=8, color="#555")
plt.savefig("../e8-two-600-cells.png", dpi=160, bbox_inches="tight"); print("figure ok")
# ---- the 8 ring radii vs Zamolodchikov's E8 masses; which 600-cell each ring belongs to
rs = sorted(set(rad)); m = np.array(rs)/rs[0]
Z = [1, 1.618034, 1.989044, 2.404867, 2.956295, 3.218340, 3.891157, 4.783386]   # Zamolodchikov 1989 masses m_k/m_1
for k, x in enumerate(rs):
    on = rad == x; print(f"ring {k+1}: radius {x:.6f}, ratio to ring 1 {m[k]:.6f} (E8 mass m{k+1}/m1 = {Z[k]}), roots from the radius-1 600-cell {int((on & big).sum())}, from the 1/phi 600-cell {int((on & ~big).sum())}")
