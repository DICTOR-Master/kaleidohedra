# The Golden Ladder, closing chapter (DICTO 5 Nov 2026): E8's 240 roots folded to 4D by the golden (icosian) projection.
# Checks: the 240 images lie on two spheres in ratio phi, 120 on each; each shell is a 600-cell (120 vertices, 12 nearest
# neighbours each at distance radius/phi, 720 edges); the Galois-conjugate projection swaps the two shells.
import numpy as np, itertools
phi = (1 + 5**0.5)/2
R = []
for i, j in itertools.combinations(range(8), 2):
    for si, sj in itertools.product((1, -1), repeat=2):
        v = np.zeros(8); v[i], v[j] = si, sj; R.append(v)
for s in itertools.product((0.5, -0.5), repeat=8):
    if sum(1 for x in s if x < 0) % 2 == 0: R.append(np.array(s))
R = np.array(R); print("E8 roots", len(R), "norms", sorted(set(np.round(np.linalg.norm(R, axis=1)**2, 9))))
# Moody-Patera / Elser-Sloane style folding: x (8D) -> (x_L + phi x_R) in 4D with a fixed 4x4 orthogonal pairing; here the
# standard H4 folding matrix (Dechant 2016, Koca et al.): rows built from (phi, 1, 1/phi, 0) patterns.
a, b, c = phi, 1.0, 1/phi
P = np.array([[a, 0, 0, 0, c, 0, 0, 0],
              [0, b, c, 0, 0, -b, c, 0],
              [0, c, 0, b, 0, c, 0, -b],
              [0, 0, b, c, 0, 0, -b, c]])
def test(P, name):
    X = R @ P.T; r = np.round(np.linalg.norm(X, axis=1), 6); rs = sorted(set(r)); print(name, "radii", rs, [int((r == x).sum()) for x in rs])
    for x in rs:
        S = X[r == x]; D = np.linalg.norm(S[:, None] - S[None], axis=2); np.fill_diagonal(D, 9e9); m = D.min()
        nn = (np.abs(D - m) < 1e-6).sum(1)
        print(f"   shell r={x}: {len(S)} points, nearest distance {m:.6f} = r/{x/m:.6f}, neighbours each {sorted(set(nn))}, edges {int((np.abs(D - m) < 1e-6).sum()//2)}")
    if len(rs) == 2: print(f"   ratio of radii {rs[1]/rs[0]:.9f} (phi = {phi:.9f})")
    return X
test(P, "golden projection")
phi2 = (1 - 5**0.5)/2; a2, c2 = phi2, 1/phi2
P2 = np.array([[a2, 0, 0, 0, c2, 0, 0, 0], [0, b, c2, 0, 0, -b, c2, 0], [0, c2, 0, b, 0, c2, 0, -b], [0, 0, b, c2, 0, 0, -b, c2]])
test(P2, "conjugate projection")
