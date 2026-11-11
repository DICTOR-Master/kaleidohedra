# Spherical waves on a packing with unknown gaps (DICTO 5 Nov 2026): the densest lattice packing of the cut OG (density 0.776244).
# Field F = solid * j0(k r) on one lattice cell (fractional grid, FFT). Its critical points, read as in chemistry's electron density:
# maxima = atoms, saddles with 2 falling directions = bonds, with 1 = rings (windows), minima = cages (gap rooms). Morse check for a
# periodic field: atoms - bonds + rings - cages = 0. Then a view inside the cell through every cage. Float.
import json, itertools, numpy as np, time, sys
from scipy.spatial import ConvexHull
from scipy import ndimage, optimize
t0 = time.time(); R = "~/study-runs/og-pent/cut/data/"
B = np.array(json.load(open(R + "densest.json"))["B"]); O = np.array(json.load(open(R + "network.json"))["ocd"]); O = O - O.mean(0)
H = ConvexHull(O); A, b = H.equations[:, :3], H.equations[:, 3]; VOL = H.volume
N = int(sys.argv[1]) if len(sys.argv) > 1 else 64
u = (np.arange(N) + 0.5)/N; U = np.stack(np.meshgrid(u, u, u, indexing="ij"), -1).reshape(-1, 3); X = U @ B.T
sh = np.array(list(itertools.product(range(-2, 3), repeat=3)), float) @ B.T
solid = np.zeros(len(X), bool)
for s in sh: solid |= np.all((X - s) @ A.T + b <= 1e-12, axis=1)
S = solid.reshape(N, N, N).astype(float); det = abs(np.linalg.det(B))
print(f"cell volume {det:.6f}, solid fraction {S.mean():.4f} (density {VOL/det:.6f})", flush=True)
L = sorted(np.linalg.norm(np.array(list(itertools.product(range(-2, 3), repeat=3)), float) @ B.T, axis=1))[1]
d = np.arange(N)/N; d = np.where(d > 0.5, d - 1, d)
DU = np.stack(np.meshgrid(d, d, d, indexing="ij"), -1).reshape(-1, 3)
img = np.array(list(itertools.product(range(-1, 2), repeat=3)), float)
Rr = np.min(np.linalg.norm((DU[:, None, :] + img[None]) @ B.T, axis=2), axis=1).reshape(N, N, N)
rc = 0.5*min(np.linalg.norm(B, axis=0))*1.6
Sf = np.fft.fftn(S); res = {}
for fac in (1.0, 0.8, 1.25):
    lam = fac*L; k = 2*np.pi/lam; Kr = np.sinc(k*Rr/np.pi)*np.clip(1 - (Rr/rc)**2, 0, 1)**2
    F = np.real(np.fft.ifftn(Sf*np.fft.fftn(Kr))); thr = np.quantile(F, 1 - S.mean())
    dark = F < thr; prec = (dark & (S == 0)).sum()/dark.sum()
    print(f"wavelength {fac:.2f} x nearest-neighbour distance {L:.4f}: of the darkest {100*(1-S.mean()):.1f}% of space, {100*prec:.1f}% is gap", flush=True)
    res[fac] = F
F = res[1.0]
# critical points: start from grid points where |grad F|^2 is a local minimum, refine by Newton on a periodic cubic spline
gx = [(np.roll(F, -1, axis=i) - np.roll(F, 1, axis=i))/2 for i in range(3)]
G2 = gx[0]**2 + gx[1]**2 + gx[2]**2
cand = np.argwhere(G2 == ndimage.minimum_filter(G2, size=3, mode="wrap"))
coef = ndimage.spline_filter(F, order=3, mode="grid-wrap")
def f(p): return ndimage.map_coordinates(coef, (np.asarray(p) % N)[:, None], order=3, mode="grid-wrap", prefilter=False)[0]
def grad(p, h=0.05): return np.array([(f(p + h*e) - f(p - h*e))/(2*h) for e in np.eye(3)])
def hess(p, h=0.25): return np.array([[(f(p + h*ei + h*ej) - f(p + h*ei - h*ej) - f(p - h*ei + h*ej) + f(p - h*ei - h*ej))/(4*h*h) for ej in np.eye(3)] for ei in np.eye(3)])
pts = []
for c in cand:
    p = c.astype(float)
    for _ in range(30):
        Hm = hess(p); g = grad(p)
        try: step = np.linalg.solve(Hm, g)
        except np.linalg.LinAlgError: break
        if np.linalg.norm(step) > 1.5: step *= 1.5/np.linalg.norm(step)
        p = p - step
        if np.linalg.norm(step) < 1e-6: break
    if np.linalg.norm(grad(p)) < 1e-6*np.abs(F).max()*N:
        q = (p % N)
        if not any(np.linalg.norm(((q - r + N/2) % N) - N/2) < 0.3 for r, _, _ in pts):
            ev = np.linalg.eigvalsh(hess(q)); pts.append((q, int((ev < 0).sum()), f(q)))
kind = {3: "atom (maximum)", 2: "bond (saddle)", 1: "ring (window)", 0: "cage (gap room)"}
cnt = {kk: sum(1 for _, n, _ in pts if n == kk) for kk in (3, 2, 1, 0)}
print("critical points per cell:", {kind[kk]: cnt[kk] for kk in cnt}, " Morse sum atoms - bonds + rings - cages =", cnt[3] - cnt[2] + cnt[1] - cnt[0], flush=True)
for q, n, v in sorted(pts, key=lambda t: (-t[1], -t[2])):
    x = (q/N) @ B.T; ins = bool(np.any([np.all((x - s) @ A.T + b <= 0) for s in sh]))
    print(f"   {kind[n]:16s} at fractional {np.round(q/N, 3)}, field {v:+.4f}, {'inside a piece' if ins else 'in the gap'}")
np.savez_compressed("lattice-wave.npz", S=S, F=F, B=B, pts=np.array([list(q) + [n, v] for q, n, v in pts]))
print(f"FINAL ok {time.time() - t0:.0f}s")
