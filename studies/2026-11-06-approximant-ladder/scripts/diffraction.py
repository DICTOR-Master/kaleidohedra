"""How five-fold is each rung? (DICTO 11-06: "harmonics, other tools".) Bond directions are exactly icosahedral on every rung (the
physical projection is golden), so the rungs differ only in the ARRANGEMENT of points. Tool: diffraction (3D waves): intensity
I(k) = |sum_x exp(i k.x)|^2 / N over the points of one region, on the plane of wave vectors square-on to a five-fold axis. A five-fold
structure gives a ten-fold pattern. Score: correlation between the pattern and itself turned by 36 deg (1.0 = perfectly ten-fold); a
cubic rung scores lower. Also the share of intensity in the brightest spots. Usage: diffraction.py qn qd R [kmax] [grid]"""
import sys, numpy as np
kmax = float(sys.argv[4]) if len(sys.argv) > 4 else 6.0; G = int(sys.argv[5]) if len(sys.argv) > 5 else 161
exec(open('cutproject.py').read().split('# period of the physical set')[0].replace('print(', '(lambda *a, **k: None)('))
phi = (1 + 5 ** .5) / 2
ax = np.array([0, 1, phi]); ax /= np.linalg.norm(ax)                      # a five-fold axis
u = np.cross(ax, [1, 0, 0]); u /= np.linalg.norm(u); w = np.cross(ax, u)
c = X.mean(0); r = np.linalg.norm(X - c, axis=1); Rr = 0.8 * r.max() * 0.6
P = X[r < Rr] - c                                                          # a ball of points round the centre (no box edges)
win = np.exp(-(np.linalg.norm(P, axis=1) / (0.6 * Rr)) ** 2)               # soft edge
g = np.linspace(-kmax, kmax, G); KX, KY = np.meshgrid(g, g)
K = KX.ravel()[:, None] * u + KY.ravel()[:, None] * w
Iimg = np.zeros(len(K))
for s in range(0, len(K), 4000):
    ph = K[s:s + 4000] @ P.T; Iimg[s:s + 4000] = np.abs((np.exp(1j * ph) * win).sum(1)) ** 2
Iimg = (Iimg / win.sum() ** 2).reshape(G, G); Iimg[G // 2, G // 2] = 0          # drop the central peak
def rotate(img, t):
    from scipy.ndimage import map_coordinates
    cy = cx = (G - 1) / 2; yy, xx = np.mgrid[0:G, 0:G]; x0, y0 = xx - cx, yy - cy
    xr = np.cos(t) * x0 - np.sin(t) * y0 + cx; yr = np.sin(t) * x0 + np.cos(t) * y0 + cy
    return map_coordinates(img, [yr, xr], order=1)
mask = (KX ** 2 + KY ** 2) < (0.95 * kmax) ** 2
def corr(a, b): a, b = a[mask], b[mask]; a = a - a.mean(); b = b - b.mean(); return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))
ten = corr(Iimg, rotate(Iimg, np.pi / 5)); four = corr(Iimg, rotate(Iimg, np.pi / 2))
top = np.sort(Iimg[mask])[::-1]; share = top[:50].sum() / top.sum()
print(f"rung {qn}/{qd}: {len(P)} points in the ball; ten-fold score (36 deg) {ten:.4f}, four-fold score (90 deg) {four:.4f}, top-50 spot share {share:.3f}")
np.save(f'../diffraction-{qn}-{qd}.npy', Iimg)
print("FINAL ok")
