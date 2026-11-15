"""Quicklook PNG of one HSD file (downsampled), with a lat/lon grid printed for choosing a scene box. Usage: quicklook.py FILE OUT.png STEP"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, hsd
from PIL import Image
h = hsd.read(sys.argv[1]); s = int(sys.argv[3])
r = hsd.calibrated(h)[::s, ::s]
lo, hi = np.nanpercentile(r, [1, 99.5])
g = np.clip((r - lo) / (hi - lo), 0, 1); g = np.nan_to_num(g)
if h['band'] >= 7: g = 1 - g
Image.fromarray((g * 255).astype(np.uint8)).save(sys.argv[2])
L0 = h['first_line']
for fl in (0, .25, .5, .75, 1):
    for fc in (0, .25, .5, .75, 1):
        l = L0 + fl * (h['nlin'] - 1); c = 1 + fc * (h['ncol'] - 1)
        la, lo_ = hsd.latlon(h, l, c)
        print(f'row {fl:.2f} col {fc:.2f}  lat {float(la):.2f} lon {float(lo_):.2f}')
print('shape', h['counts'].shape, 'band', h['band'])
