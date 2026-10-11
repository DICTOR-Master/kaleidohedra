# Octahedral variant (2026-10-12), layers around the Pacioli icosahedron I(1): (A) between I(1/phi) and I(1); (B) between I(1) and the
# icosidodecahedral core ID(phi/2). Natural pieces tried: (A) over each face of I(1), the frustum down to the parallel face of
# I(1/phi), and what is left at edges and corners; (B) over each ID pentagon a pyramid to the I(1) corner below, over each ID triangle
# the twisted frustum to the I(1) face below. Volumes and a sampled exact cover.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def F(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
def cover(outer, inner, pieces, n=30000):
    FO, FI = F(outer), F(inner); R = np.linalg.norm(outer, axis=1).max()
    rng = np.random.default_rng(5); S = rng.uniform(-R, R, (n * 20, 3))
    S = S[np.all(S @ FO[:, :3].T + FO[:, 3] < -1e-9, axis=1) & ~np.all(S @ FI[:, :3].T + FI[:, 3] <= 1e-9, axis=1)][:n]
    c = np.zeros(len(S), int)
    for P in pieces: E = ConvexHull(P).equations; c += np.all(S @ E[:, :3].T + E[:, 3] < 1e-9, axis=1)
    return np.mean(c == 1), np.mean(c == 0), np.mean(c > 1)
Ic, I1, ID = ref['I'] / PHI, ref['I'], ref['ID'] * PHI / 2
# (A)
FI1, FIc = F(I1), F(Ic); A = []
for f in FI1:
    n = f[:3] / np.linalg.norm(f[:3]); g = FIc[np.argmax(FIc[:, :3] @ n)]
    A.append(np.vstack([I1[np.abs(I1 @ f[:3] + f[3]) < 1e-9], Ic[np.abs(Ic @ g[:3] + g[3]) < 1e-9]]))
gapA = ConvexHull(I1).volume - ConvexHull(Ic).volume; vA = sum(ConvexHull(P).volume for P in A)
print(f'(A) I(1) minus I(1/phi): gap {gapA:.6f}; 20 face frusta {vA:.6f}; left {gapA - vA:+.6f}; cover once/none/twice {cover(I1, Ic, A)}')
# (B)
FID = F(ID); B = []
for f in FID:
    on = ID[np.abs(ID @ f[:3] + f[3]) < 1e-9]; n = f[:3] / np.linalg.norm(f[:3])
    if len(on) == 5: B.append(np.vstack([on, I1[np.argmax(I1 @ n)]]))
    else:
        g = FI1[np.argmax(FI1[:, :3] @ n)]; B.append(np.vstack([on, I1[np.abs(I1 @ g[:3] + g[3]) < 1e-9]]))
gapB = ConvexHull(ID).volume - ConvexHull(I1).volume; vB = sum(ConvexHull(P).volume for P in B)
print(f'(B) ID(phi/2) minus I(1): gap {gapB:.6f}; 12 pyramids + 20 frusta {vB:.6f}; left {gapB - vB:+.6f}; cover once/none/twice {cover(ID, I1, B)}')
