# DICTO · dictospheres.com — the Sun data of Figure 6: three faces of a space-time block of granulation, cut from the vertical
# velocity 0.1 Mm below the mean tau = 1 height of the Bifrost run en024048_hion (Carlsson et al. 2016; Hinode SDC Europe), as
# stored by studies/2026-11-15-sun-granulation (data/bifrost/en024048_hion_uz_dz0.1.npy: 242 frames, 10 s apart, 504 × 504,
# 0.047619 Mm per pixel). Run once on the host that holds the study's data; writes data/sun-faces.npz (float16, in the units
# of the study's file; the figure uses only the sign and the ranking of values):
# top = the last frame, mid = the middle frame, front = the x–t section at the near y edge, side = the y–t section at the far x edge.
# Usage: python3 sun_extract.py STUDY_NPY STUDY_META OUT.npz
import sys, json
import numpy as np

src, meta, out = sys.argv[1:4]
M = json.load(open(meta)); F = np.load(src, mmap_mode='r')
assert F.shape == (242, 504, 504) and M['n'] == 242 and M['dtsnap_s'] == 10.0 and abs(M['dx_Mm'] - 0.047619) < 1e-9, F.shape
N = 252                                    # 12.0 Mm square
x0, y0 = 126, 126                          # the middle of the box
B = np.asarray(F[:, y0:y0 + N, x0:x0 + N], dtype=np.float32)
up = np.sign(np.median(B))                 # granules (upflows) cover most of the area: their sign is the median's
np.savez_compressed(out, top=B[-1].astype(np.float16), mid=B[len(B) // 2].astype(np.float16), front=B[:, 0, :].astype(np.float16),
                    side=B[:, :, -1].astype(np.float16), up=np.float16(up), dx=np.float32(M['dx_Mm']), dt=np.float32(M['dtsnap_s']),
                    crop=np.array([x0, y0, N]))
print('frames', len(B), 'crop', x0, y0, N, 'Mm', N * M['dx_Mm'], 'minutes', (len(B) - 1) * M['dtsnap_s'] / 60, 'upflow sign', up,
      'range', float(B.min()), float(B.max()))
print('FINAL ok')
