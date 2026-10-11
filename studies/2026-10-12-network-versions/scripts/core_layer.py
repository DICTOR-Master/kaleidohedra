# The possible last missing piece (2026-10-12): the layer between the network's icosidodecahedral core (edge phi/2) and the small
# icosahedron I(1/phi) at the centre (the Lotus seed's centre). If it fills exactly, the network is a full phi^3 cycle:
# I(phi^2) > RT > cage > D > ID > I(1/phi), repeating inward. Natural pieces: over each ID pentagon, a pyramid down to the small
# icosahedron's corner below; over each ID triangle, the solid down to the small icosahedron's face below; what is left at the ID's
# 30 corners (over the small icosahedron's edges). Volumes and a sampled exact-cover check.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def F(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
ID = ref['ID'] * PHI / 2; Ic = ref['I'] / PHI; FID = F(ID); FIc = F(Ic)
inside = np.all(Ic @ FID[:, :3].T + FID[:, 3] <= 1e-9)
gap = ConvexHull(ID).volume - ConvexHull(Ic).volume
print(f'I(1/phi) inside the ID core: {inside}; gap {gap:.6f} ({gap / ConvexHull(ID).volume:.1%} of the core)')
pieces = {}
for f in FID:
    on = ID[np.abs(ID @ f[:3] + f[3]) < 1e-9]; n = f[:3] / np.linalg.norm(f[:3])
    if len(on) == 5:
        pieces.setdefault('pentagonal pyramid (ID pentagon to the small icosahedron corner)', []).append(np.vstack([on, Ic[np.argmax(Ic @ n)]]))
    else:
        g = FIc[np.argmax(FIc[:, :3] @ n)]; tri = Ic[np.abs(Ic @ g[:3] + g[3]) < 1e-9]
        pieces.setdefault('triangular piece (ID triangle to the small icosahedron face)', []).append(np.vstack([on, tri]))
tot = 0
for k, L in pieces.items():
    v = [ConvexHull(P).volume for P in L]; tot += sum(v); print(f'  {len(L)} x {k}: volume each {v[0]:.6f}')
print(f'these {tot:.6f} of gap {gap:.6f}; left {gap - tot:+.6f}')
rng = np.random.default_rng(3); S = rng.uniform(-1.4, 1.4, (300000, 3))
S = S[np.all(S @ FID[:, :3].T + FID[:, 3] < -1e-9, axis=1) & ~np.all(S @ FIc[:, :3].T + FIc[:, 3] <= 1e-9, axis=1)][:30000]
cnt = np.zeros(len(S), int)
for L in pieces.values():
    for P in L:
        E = ConvexHull(P).equations; cnt += np.all(S @ E[:, :3].T + E[:, 3] < 1e-9, axis=1)
print(f'sample points in the gap: once {np.mean(cnt == 1):.2%}, none {np.mean(cnt == 0):.2%}, twice+ {np.mean(cnt > 1):.2%}')
P = pieces['triangular piece (ID triangle to the small icosahedron face)'][0]; H = ConvexHull(P); Fs = []
for e in H.equations:
    if not any(np.linalg.norm(e - q) < 1e-7 for q in Fs): Fs.append(e)
kinds = sorted(int(np.sum(np.abs(P @ e[:3] + e[3]) < 1e-9)) for e in Fs)
ed = sorted({round(float(np.linalg.norm(P[i] - P[j])), 6) for i, j in itertools.combinations(range(6), 2) if any(np.sum(np.abs(P[[i, j]] @ e[:3] + e[3]) < 1e-9) == 2 for e in Fs)})
print(f'triangular piece: {len(Fs)} faces with corner counts {kinds}; edge lengths {ed}')
