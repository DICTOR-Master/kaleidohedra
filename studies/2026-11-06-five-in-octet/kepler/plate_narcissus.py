# Site tiles in the plate style (DICTO 11-06 "into queue and do a nice cover"): #97 Narcissus (one piece, and a stack of layers) and
# #98 Narcissus and Covenant (two Narcissi on their hexagons: straight = twisted cube; turned 60 deg = Covenant).
import sys, numpy as np
sys.path.insert(0, '/home/dicto/k-research/studies/2026-11-05-one-piece-any-stacking/scripts')
from n_slabs import narc, SITE, H, build
from davinci import Plate, look, PARCH
from PIL import Image
N = narc(SITE['A'], H, 0, 'C'); c = N[:6].mean(0)
GOLD = (214, 172, 70); VIO = (140, 104, 176)
def mirror_turn(P, turn):
    Q = P.copy(); Q[:, 2] = 2 * H - Q[:, 2]
    if turn:
        t = np.pi / 3; R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]); Q[:, :2] = (Q[:, :2] - c[:2]) @ R.T + c[:2]
    return Q
def save_tile(pl, out):
    pl.save('/tmp/_t.png', ''); im = Image.open('/tmp/_t.png').convert('RGB'); w, h = im.size
    im.crop((0, int(h * 0.125), w, int(h * 0.875))).resize((1200, 900), Image.LANCZOS).save(out, quality=88, optimize=True)
# 97: one Narcissus large on the left, three layers of a stacking on the right
pl = Plate(look((0.55, -0.75, 0.45), (0, 0, 1)), W=2400, scale=2400 * 0.13, centre=c + np.array([2.1, 0.5, 0.9]))
pl.solid(N - np.array([0, 0, 0]), GOLD, w=4)
P = build('ST', n=1); top = max(p[:, 2].mean() for p in P)
for k, Q in sorted(enumerate(P), key=lambda t: pl.z(t[1].mean(0) + np.array([3.2, 0.8, 0.0]))):
    sh = np.array([3.4, 0.8, 0.0]) + np.array([0, 0, 0.25 * int(Q[:, 2].mean() / H)])
    if np.linalg.norm(Q[:, :2].mean(0) - c[:2]) > 1.3: continue
    pl.solid(Q + sh, GOLD if (k % 2 == 0) else VIO, w=2)
save_tile(pl, '/home/dicto/dictospheres/papers/narcissus-keyed.jpg')
# 98: straight pair (twisted cube) and turned pair (Covenant), pulled slightly apart
pl = Plate(look((0.5, -0.8, 0.35), (0, 0, 1)), W=2400, scale=2400 * 0.21, centre=c + np.array([1.2, 0, 0.6]))
gap = np.array([0, 0, 0.12])
for dx, turn in ((0.0, False), (2.4, True)):
    a = N + np.array([dx, 0, 0]); b = mirror_turn(N, turn) + np.array([dx, 0, 0]) + gap
    for Q, col in sorted([(a, GOLD), (b, VIO)], key=lambda t: pl.z(t[0].mean(0))): pl.solid(Q, col, w=3)
save_tile(pl, '/home/dicto/dictospheres/papers/narcissus-and-covenant.jpg'); print('ok')
