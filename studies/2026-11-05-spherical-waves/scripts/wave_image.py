# Spherical-wave imaging (DICTO 5 Nov 2026: "spherical wave patterns to help with imaging and reveal or close gaps"; first test on the
# pyrochlore cell). Every point of solid sends out a spherical wave j0(k r) = sin(kr)/(kr); the field F = (solid) * j0 is computed on one
# periodic cubic cell of the diamond network of regular-triangle cut OGs (8 copies) by FFT. Dark (low F) should mark gaps. Score: how well
# "F below its median" picks out empty space, at several wavelengths. Float; grid N^3.
import numpy as np, itertools, math, time
from scipy.spatial import ConvexHull
t0 = time.time()
V = np.load("../../../study-runs-link/equilateral.npy") if False else np.load("equilateral.npy"); V = V - V.mean(0)
H = ConvexHull(V); A, b = H.equations[:, :3], H.equations[:, 3]
pl = {}
for eq, s in zip(H.equations, H.simplices): pl.setdefault(tuple(np.round(eq, 5)), set()).update(s)
HEX = [sorted(f) for f in pl.values() if len(f) == 6]; cen = [V[f].mean(0) for f in HEX]; u = [c/np.linalg.norm(c) for c in cen]
tet = next(q for q in itertools.combinations(range(len(HEX)), 4) if all(abs(u[i] @ u[j] + 1/3) < 1e-5 for i, j in itertools.combinations(q, 2)))
tu = [u[i] for i in tet]; M = np.linalg.norm(cen[tet[0]])
SQ = [(tu[0] + tu[j])/np.linalg.norm(tu[0] + tu[j]) for j in (1, 2, 3)]; Q = np.array(SQ)   # rows: cube axes
a = 8*M/math.sqrt(3)
B = Q @ (2*M*tu[0]); print("cell side", round(a, 4), "B in cube frame / (a/4):", np.round(B/(a/4), 4))
fcc = [np.zeros(3), a*np.array([0, .5, .5]), a*np.array([.5, 0, .5]), a*np.array([.5, .5, 0])]
nodes = fcc + [p + B for p in fcc]
Vc = V @ Q.T; Hc = ConvexHull(Vc); Ac, bc = Hc.equations[:, :3], Hc.equations[:, 3]
N = 96; g = (np.arange(N) + 0.5)/N*a; X = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1).reshape(-1, 3)
solid = np.zeros(len(X), bool)
for c in nodes:
    d = X - c; d -= a*np.round(d/a)
    solid |= np.all(d @ Ac.T + bc <= 0, axis=1)
S = solid.reshape(N, N, N).astype(float); print(f"solid fraction {S.mean():.4f} (cut OG fills 75.43% of its TO, half the TOs empty -> expect {0.7543/2:.4f})", flush=True)
f = np.fft.fftfreq(N, d=a/N)*2*np.pi; KX, KY, KZ = np.meshgrid(f, f, f, indexing="ij"); Kn = np.sqrt(KX**2 + KY**2 + KZ**2)
Sf = np.fft.fftn(S)
out = {}
for name, lam in (("long", a/2), ("medium", a/4), ("short", a/8)):
    k = 2*np.pi/lam
    # kernel j0(k r) truncated smoothly at r = a/2, built in real space on the periodic grid
    d = (np.arange(N) + 0.0)/N*a; d = np.minimum(d, a - d); R = np.sqrt(d[:, None, None]**2 + d[None, :, None]**2 + d[None, None, :]**2)
    Kr = np.sinc(k*R/np.pi)*np.clip(1 - (R/(a/2))**2, 0, 1)**2
    F = np.real(np.fft.ifftn(Sf*np.fft.fftn(Kr))).ravel()
    dark = F < np.median(F); emp = ~solid
    hit = (dark & emp).sum()/emp.sum(); false = (dark & solid).sum()/solid.sum()
    print(f"{name} wavelength {lam:.3f}: dark covers {hit:.3f} of the gaps and {false:.3f} of the solid", flush=True)
    out[name] = F.reshape(N, N, N)
np.savez_compressed("wave-fields.npz", S=S, a=a, N=N, **out)
print(f"FINAL ok {time.time() - t0:.0f}s")
