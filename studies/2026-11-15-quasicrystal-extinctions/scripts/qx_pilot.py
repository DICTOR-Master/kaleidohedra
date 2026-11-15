"""Pilot: do the twisted-silent harmonic degrees of the golden 20-set X show up as extinct Bragg peaks?

Sets (centred in the hyperplane sum = 0 of R^5, all scaled to unit radius):
  X  = permutations of (phi^2, phi^2, phi^2, phi, 0)   kills 1, 2, 5, 7 (twisted class of 2I)
  mX = -X                                               same
  F  = permutations of (phi^2, phi^2, 1, 1, 0)          kills 1, 2, 3, 6
  R  = A4 roots e_i - e_j                               kills 2 and all odd
  G  = permutations of (a, a, a, b, 0), a = 1.7, b = 0.6 (control: same S5 orbit type as X, generic, kills 1, 2 only)

Part 1  degree-n multipole of each set, Z_n(u) = sum_x U_n(u.x), max over 400 random directions u, n = 1..12.
Part 2  odd moments p_m(u) = sum_x (u.x)^m, m = 3, 5, 7: is p_5/p_3 and p_7/p_3 the same in every direction?
        (silence of 5 and 7 with 1 silent forces p_5 and p_7 to be multiples of the degree-3 harmonic Z_3.)
Part 3  Bragg test: wavevectors k = m / (4 phi^2) with m in the Z[phi]-module spanned by X (rank 8 over Z),
        integer coefficients in [-C, C]^8, kept when |m| <= KMAX and the Galois image |m*| <= KSTAR (the bright peaks
        of a cut-and-project pattern sit at small |m*|). Motif form factor F_S(k) = sum_x exp(2 pi i k.x) for each set
        (decorated structure: every quasilattice point carries a copy of S, so its peak = window factor x F_S(k)).
        Extinction = |F_S(k)| < 1e-9 |S|. Do extinctions occur, and do they track the silent degrees (X vs control G)?
Every CHECK line must say OK; ends with FINAL ok only if all checks pass.
"""
import numpy as np, itertools, sys, time
t0 = time.time()
phi = (1 + 5 ** .5) / 2; phic = (1 - 5 ** .5) / 2           # phi and its Galois conjugate
def orbit(v):
    P = np.array(sorted(set(itertools.permutations(v))), float)
    return P - P.mean(axis=1, keepdims=True)
def unit(P): return P / np.linalg.norm(P[0])
sets_raw = {
    'X': orbit((phi**2, phi**2, phi**2, phi, 0)),
    'F': orbit((phi**2, phi**2, 1, 1, 0)),
    'R': np.array([np.eye(5)[i] - np.eye(5)[j] for i in range(5) for j in range(5) if i != j]),
    'G': orbit((1.7, 1.7, 1.7, 0.6, 0)),
}
sets_raw['mX'] = -sets_raw['X']
S = {k: unit(v) for k, v in sets_raw.items()}
for k, v in S.items(): print(f"set {k}: {len(v)} points")
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(f"CHECK {name}: {'OK' if cond else 'FAIL'}")
rng = np.random.default_rng(20261115)
U = rng.normal(size=(400, 5)); U -= U.mean(axis=1, keepdims=True); U /= np.linalg.norm(U, axis=1, keepdims=True)
def cheb_U(n, c):
    u0, u1 = np.ones_like(c), 2 * c
    if n == 0: return u0
    for _ in range(n - 1): u0, u1 = u1, 2 * c * u1 - u0
    return u1
# ---- Part 1
print("\nPart 1: max over directions of |Z_n| / |S| (zero = silent degree)")
expect = {'X': {1, 2, 5, 7}, 'mX': {1, 2, 5, 7}, 'F': {1, 2, 3, 6}, 'R': {2, 1, 3, 5, 7, 9, 11}, 'G': {1, 2}}
for name, P in S.items():
    C = U @ P.T
    row = [np.abs(cheb_U(n, C).sum(axis=1)).max() / len(P) for n in range(1, 13)]
    silent = {n for n, r in zip(range(1, 13), row) if r < 1e-10}
    print(f"  {name:2s} " + " ".join(f"{r:8.1e}" for r in row) + f"   silent {sorted(silent)}")
    check(f"silent degrees of {name} (n <= 12) = expected", silent == {e for e in expect[name] if e <= 12})
print("PROGRESS 0.33 part 1 done")
# ---- Part 2
print("\nPart 2: odd moments p_m(u); spread of p_5/p_3 and p_7/p_3 over directions (relative)")
for name in ['X', 'G', 'F']:
    C = U @ S[name].T; p3, p5, p7 = (C ** 3).sum(1), (C ** 5).sum(1), (C ** 7).sum(1)
    keep = np.abs(p3) > 1e-3
    if keep.sum() < 50:
        print(f"  {name}: p_3 vanishes in every direction (max |p_3| = {np.abs(p3).max():.1e})"); continue
    r5, r7 = p5[keep] / p3[keep], p7[keep] / p3[keep]
    s5, s7 = np.ptp(r5) / abs(r5.mean()), np.ptp(r7) / abs(r7.mean())
    print(f"  {name}: p5/p3 mean {r5.mean():.6f} rel.spread {s5:.1e};  p7/p3 mean {r7.mean():.6f} rel.spread {s7:.1e}")
    if name == 'X': check("X: p5 and p7 are fixed multiples of p3 in every direction", s5 < 1e-9 and s7 < 1e-9)
    if name == 'G': check("control G: p5/p3 not constant", s5 > 1e-3)
print("PROGRESS 0.5 part 2 done")
# ---- Part 3
C_RANGE, KMAX, KSTAR = 3, 6.0, 1.5
base = orbit((phi**2, phi**2, phi**2, phi, 0)); basec = orbit((phic**2, phic**2, phic**2, phic, 0))
# pick 4 points of X independent over R (hence over Q(sqrt5)); Z-basis b_i, phi*b_i
idx = []
for i in range(len(base)):
    if np.linalg.matrix_rank(base[idx + [i]]) == len(idx) + 1: idx.append(i)
    if len(idx) == 4: break
B = np.vstack([base[idx], phi * base[idx]]); Bc = np.vstack([basec[idx], phic * basec[idx]])   # physical / internal images
check("Z-basis is independent in R^5 x R^5 (rank 8)", np.linalg.matrix_rank(np.hstack([B, Bc])) == 8)
scale = 4 * phi ** 2
rawX = sets_raw  # unnormalised motifs at the module's own scale (X has |x|^2 = 2 phi^2)
motifs = {k: v for k, v in sets_raw.items()}
rng_vals = np.arange(-C_RANGE, C_RANGE + 1)
grid = np.array(list(itertools.product(rng_vals, repeat=4)))
nk, zeros, near = 0, {k: 0 for k in motifs}, {k: np.inf for k in motifs}
zero_examples = {k: [] for k in motifs}
for j, g1 in enumerate(grid):                       # coefficients of b_i
    coef = np.hstack([np.repeat(g1[None], len(grid), 0), grid])
    m, mc = coef @ B, coef @ Bc
    keep = (np.linalg.norm(m, axis=1) <= KMAX) & (np.linalg.norm(mc, axis=1) <= KSTAR) & (np.abs(coef).sum(1) > 0)
    if not keep.any(): continue
    k = m[keep] / scale; nk += len(k)
    for name, P in motifs.items():
        Fk = np.exp(2j * np.pi * (k @ P.T)).sum(1); a = np.abs(Fk) / len(P)
        z = a < 1e-9; zeros[name] += int(z.sum()); near[name] = min(near[name], a[~z].min() if (~z).any() else np.inf)
        if z.any() and len(zero_examples[name]) < 3: zero_examples[name] += [tuple(c) for c in coef[keep][z][:3]]
    if j % 240 == 0: print(f"PROGRESS {0.5 + 0.5 * j / len(grid):.3f} bragg block {j}/{len(grid)}")
print(f"\nPart 3: {nk} Bragg vectors (|m| <= {KMAX}, |m*| <= {KSTAR}, coefficients in [-{C_RANGE},{C_RANGE}])")
for name in motifs: print(f"  {name:2s}: exact-zero peaks {zeros[name]:6d}   smallest nonzero |F|/|S| {near[name]:.2e}   examples {zero_examples[name][:2]}")
check("enough Bragg vectors tested (> 1000)", nk > 1000)
print(f"\nelapsed {time.time() - t0:.1f} s")
print("FINAL ok" if ok else "FINAL FAIL")
