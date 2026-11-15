# Compose the Platonic Solids series cover (third design, DICTO 15 Nov 2026: the five solids plain in a circle): the picture
# (circle_scene.py) on the cover ground, lettering exactly as the previous design (ledtext.py, DSEG14 by keshikan, SIL OFL): series
# line white, title in the series gold, subtitle in SUBCOL (a colour of the picture), and the ◆ DICTO ◆ mark (front and back) in the
# dodecahedron's violet (DICTO, 15 Nov 2026: the mark in the D solid's colour, element colours of the DICTO square).
# Run: python compose.py PICTURE.png OUT.png [BACKMARK.png]
import sys, os
import numpy as np
from PIL import Image
import ledtext as L
pic, out = sys.argv[1], sys.argv[2]; back = sys.argv[3] if len(sys.argv) > 3 else None
GROUND = (20, 15, 11); GOLD = (217, 165, 33); WHITE = (255, 255, 255)
VIOLET = (138, 92, 196)                     # D, the dodecahedron (aether): element colour
SUBCOL = tuple(int(c) for c in os.environ.get('SUBCOL', '58,112,205').split(','))   # default: the icosahedron's blue (element colour)
W, Hc, TOP = 2400, 3394, 2200
def caps_of(text):
    return text.upper(), tuple(i for i, ch in enumerate(text) if ch.isupper() and (i == 0 or text[i - 1] == ' '))
def fit(text, size, col, maxw):
    t, big = caps_of(text)
    while True:
        w_ = L.word(t, size, lambda ch: col, big=big)
        if w_[1].shape[1] <= maxw: return w_, size
        size = int(size * 0.96)
SERIES = 'Book Eight · Wind 風 · The Five Orders of Space'
TITLE = 'The Platonic Solids'
SUB = 'Inside the Five, Filling Space & Where They Live'
MARK_BIG = (0, 2, 3, 4, 5, 6, 8)
can = np.ones((Hc, W, 3)) * np.array(GROUND, float)
P = np.array(Image.open(pic).convert('RGB'), float); assert P.shape[:2] == (TOP, W), P.shape
can[:TOP] = P
N = W
ser, s1 = fit(SERIES, int(N * 0.030), WHITE, W - 360)
t1, s2 = fit(TITLE, int(N * 0.064), GOLD, W - 160)
sub, s3 = fit(SUB, int(N * 0.0225), SUBCOL, W - 200)
by = L.word('* DICTO *', int(N * 0.040), lambda ch: VIOLET, big=MARK_BIG)
y = L.paste(can, ser, N / 2, TOP + 40); y = L.paste(can, t1, N / 2, y + 60); y = L.paste(can, sub, N / 2, y + 75); y = L.paste(can, by, N / 2, y + 85)
print('lettering sizes: series', s1, 'title', s2, 'subtitle', s3, '; bottom of lettering', y, flush=True)
ok = y < Hc - 60
Image.fromarray(np.clip(can, 0, 255).astype(np.uint8)).save(out)
if back:
    mk = L.word('* DICTO *', int(W * 0.06), lambda ch: VIOLET, big=MARK_BIG)
    Image.fromarray(np.dstack([np.clip(mk[0], 0, 255), mk[1] * 255]).astype(np.uint8), 'RGBA').save(back)
print('PROGRESS 0.95 composed', out, flush=True)
print('FINAL ok' if ok and Image.open(out).size == (W, Hc) else 'FINAL FAIL: lettering past the bottom or wrong size')
