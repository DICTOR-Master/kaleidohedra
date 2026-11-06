# DICTO 11-06: "dodgy rough blackout lines" on the photos of his work (Figure 1 of #20; Figure 3A.0 of The Golden Ladder).
# Panel (c), the dictosphere design, was cut from its background with a jagged white halo. Its outline is a circle: fit the circle
# to the silhouette (least squares on the edge points), then repaint a ring round it with the ground colour and an anti-aliased edge,
# inset past the halo. Nothing inside the sphere and nothing outside the ring (the DICTO mark) is touched. Source kept as -orig.
import numpy as np
from PIL import Image
from scipy import ndimage
src = 'paper/figures/fig0-dicto-work-orig.jpg'; out = 'paper/figures/fig0-dicto-work.jpg'
A = np.array(Image.open(src).convert('RGB'), float); H, W, _ = A.shape
G = A[5, 5].copy()
x0 = 1740                                            # panel (c) starts here
sub = A[:, x0:]
fg = np.abs(sub - G).sum(2) > 60
fg = ndimage.binary_opening(fg, iterations=2)
lab, n = ndimage.label(fg); big = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)
big = ndimage.binary_fill_holes(big)
edge = big ^ ndimage.binary_erosion(big)
ys, xs = np.nonzero(edge)
# algebraic circle fit x^2+y^2+Dx+Ey+F=0
M = np.c_[xs, ys, np.ones_like(xs)]; b = -(xs ** 2 + ys ** 2)
D, E, F = np.linalg.lstsq(M, b, rcond=None)[0]; cx, cy = -D / 2, -E / 2; R = np.sqrt(cx ** 2 + cy ** 2 - F)
d = np.hypot(*np.meshgrid(np.arange(sub.shape[1]) - cx, np.arange(H) - cy))
res = np.abs(np.hypot(xs - cx, ys - cy) - R)
print(f'circle centre ({cx + x0:.1f}, {cy:.1f}) R {R:.1f}; edge residual median {np.median(res):.2f} px, 90% {np.percentile(res, 90):.2f} px')
inset = 9.0                                          # past the halo (measured 6-10 px)
r0 = R - inset
alpha = np.clip(r0 + 0.75 - d, 0, 1.5) / 1.5          # 1 inside, 0 outside, ~1.5 px soft edge
ring = (d > r0 - 2) & (d < R + 18)                   # repaint only this ring
new = sub * alpha[..., None] + G * (1 - alpha[..., None])
sub2 = np.where(ring[..., None], new, sub)
A[:, x0:] = sub2
# DICTO 11-06: "there was a bit of brown floor or table on the deltahedrons photo": panel (a), the brown patch under the DeltaZips
# (box x 60-300, y 280-460): brownish pixels (red > green >= blue, not bright), components > 300 px, grown 2 px, painted with the ground.
y0, y1, x1_, x0_ = 280, 460, 300, 60
S = A[y0:y1, x0_:x1_]; r, g, b_ = S[..., 0], S[..., 1], S[..., 2]; mx = S.max(2); mn = S.min(2)
brown = (r > g + 8) & (g >= b_ - 5) & (mx < 170) & (mx > 35) & ((mx - mn) > 18)
brown = ndimage.binary_closing(ndimage.binary_opening(brown, iterations=1), iterations=2)
lab, n = ndimage.label(brown); sz = np.bincount(lab.ravel())
keep = ndimage.binary_dilation(np.isin(lab, [i for i in range(1, n + 1) if sz[i] > 300]), iterations=2)
soft = ndimage.gaussian_filter(keep.astype(float), 1.0)
A[y0:y1, x0_:x1_] = S * (1 - soft[..., None]) + G * soft[..., None]
print('panel (a) brown patch px', int(keep.sum()))
Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)).save(out, quality=93)
print('saved', out)
