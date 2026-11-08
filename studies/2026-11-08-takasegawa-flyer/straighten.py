"""Straighten DICTO's photo of the Takasegawa Art Festival flyer: find the sheet's corners (bright paper on a dark table),
undo the perspective to a flat A4 sheet. Usage: straighten.py in.jpg out.png"""
import sys, numpy as np
from PIL import Image, ImageOps, ImageFilter
im = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert('RGB'); a = np.asarray(im).astype(float)
lum = a.mean(2); sat = a.max(2) - a.min(2)
mask = (lum > 120)  # paper (white/blue/yellow print) vs black table
m = Image.fromarray((mask * 255).astype('uint8')).filter(ImageFilter.MedianFilter(15)); mask = np.asarray(m) > 128
ys, xs = np.nonzero(mask)
s, d = xs + ys, xs - ys
tl = (xs[s.argmin()], ys[s.argmin()]); br = (xs[s.argmax()], ys[s.argmax()])
tr = (xs[d.argmax()], ys[d.argmax()]); bl = (xs[d.argmin()], ys[d.argmin()])
if len(sys.argv) > 3:  # manual corners x,y x,y x,y x,y (tl tr br bl), read off a gridded crop; glare fools the mask
    tl, tr, br, bl = [tuple(map(float, p.split(','))) for p in sys.argv[3:7]]
print('corners', tl, tr, br, bl)
W, H = 1414, 2000
def coeffs(dst, src):
    A = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float))
c = coeffs([(0, 0), (W, 0), (W, H), (0, H)], [tl, tr, br, bl])
out = im.transform((W, H), Image.PERSPECTIVE, tuple(c), Image.BICUBIC)
out.save(sys.argv[2]); print('saved', out.size)
