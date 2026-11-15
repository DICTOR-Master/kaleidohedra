#!/usr/bin/env python3
"""Write orthogonal slices of a uint8 .npy (z, y, x) as greyscale PNGs (pure zlib, no imaging library). Usage: pngview.py VOL.npy OUTPREFIX [z y x]"""
import sys, zlib, struct, numpy as np
def png(path, A):
    A = np.ascontiguousarray(A.astype(np.uint8)); h, w = A.shape
    raw = b''.join(b'\x00' + A[i].tobytes() for i in range(h))
    ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
def stretch(A):
    lo, hi = np.percentile(A, [1, 99.5]); return np.clip((A.astype(float) - lo) / max(hi - lo, 1) * 255, 0, 255)
V = np.load(sys.argv[1], mmap_mode='r'); pre = sys.argv[2]
z, y, x = [int(v) for v in sys.argv[3:6]] if len(sys.argv) > 5 else [s // 2 for s in V.shape]
png(pre + f'_z{z}.png', stretch(V[z])); png(pre + f'_y{y}.png', stretch(V[:, y, :])); png(pre + f'_x{x}.png', stretch(V[:, :, x]))
print('shape', V.shape, 'PNG ok')
