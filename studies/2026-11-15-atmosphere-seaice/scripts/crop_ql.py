"""Quicklook of a crop: crop_ql.py FILE r0 r1 c0 c1 STEP OUT.png (rows/cols in the file's pixel grid); prints centre lat/lon."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, hsd
from PIL import Image
h = hsd.read(sys.argv[1]); r0, r1, c0, c1, s = map(int, sys.argv[2:7])
r = hsd.calibrated(h)[r0:r1:s, c0:c1:s]
lo, hi = np.nanpercentile(r, [1, 99.5]); g = np.nan_to_num(np.clip((r - lo) / (hi - lo), 0, 1))
Image.fromarray((g * 255).astype(np.uint8)).save(sys.argv[7])
for l, c in ((r0, c0), (r1, c1), ((r0 + r1) // 2, (c0 + c1) // 2)):
    la, lo_ = hsd.latlon(h, h['first_line'] + l, 1 + c); print('pix', l, c, 'lat %.2f lon %.2f' % (la, lo_))
