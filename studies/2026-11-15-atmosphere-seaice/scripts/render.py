"""Figure: one frame's albedo with the cell boundaries of the census rule (red) and the box. Usage: render.py DATA MODE SIGMA H BOX R0 C0 OUT.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import cellcensus as CC
d, mode, sigma, h, box, r0, c0, out = sys.argv[1:9]
box, r0, c0 = int(box), int(r0), int(c0)
F = np.load(os.path.join(d, 'frames.npy'), mmap_mode='r'); a = np.asarray(F[0, r0:r0 + box, c0:c0 + box])
lab = CC.segment(a, mode, float(sigma), float(h))
lo, hi = np.nanpercentile(a, [1, 99.5]); g = np.nan_to_num(np.clip((a - lo) / (hi - lo), 0, 1))
rgb = np.stack([g, g, g], -1)
edge = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1)); edge[0, :] = edge[:, 0] = False
rgb[edge] = [1, 0.15, 0.1]
im = Image.fromarray((rgb * 255).astype(np.uint8)); im = im.resize((im.width * 2, im.height * 2), Image.NEAREST); im.save(out)
print('RENDER_OK cells', lab.max())
