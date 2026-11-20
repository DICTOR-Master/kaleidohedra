# Quanta of Space I, Version 3.0 cover (DICTO, 20 Nov 2026): the same cover, only the series line changed to
# "The Five Orders of Space · Book One, Volume I", with no ring word and no kanji, the whole line in the cube's green
# (series_line.ON_DARK['Earth'], as in v4). Same rule, LED letters, size, gap and placement as series_covers.py (mode full);
# runs() and caps_of() copied from there (that script has no import guard).
# Run: python quanta_cover_v5.py PAPERS_DIR   -> book-quanta-of-space/figures/cover/quanta-cover-front-series-v5.png
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ledtext as L
P = os.path.abspath(sys.argv[1]); os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(P, 'series-five-orders'))
from series_line import ON_DARK
GAP, MIN_ABOVE = 87, 50
TEXT = 'The Five Orders of Space · Book One, Volume I'
GREEN = ON_DARK['Earth']
def runs(a, ground):
    d = (np.abs(a - ground).sum(2) > 30).any(1); out = []; s = None
    for y, v in enumerate(d):
        if v and s is None: s = y
        if not v and s is not None: out.append([s, y]); s = None
    if s is not None: out.append([s, len(d)])
    m = []
    for r in out:
        if m and r[0] - m[-1][1] < 8: m[-1][1] = r[1]
        else: m.append(r)
    return [r for r in m if r[1] - r[0] > 3]
def caps_of(text):
    return text.upper(), tuple(i for i, ch in enumerate(text) if ch.isupper() and (i == 0 or text[i - 1] == ' '))
src = os.path.join(P, 'book-quanta-of-space/figures/cover/quanta-cover-front.png'); nlet = 3
v4 = os.path.join(P, 'book-quanta-of-space/figures/cover/quanta-cover-front-series-v4.png')
out = os.path.join(P, 'book-quanta-of-space/figures/cover/quanta-cover-front-series-v5.png')
im = Image.open(src).convert('RGB'); W, H = im.size; s = W / 2400
a = np.array(im, float); ground = a[-3, 3].copy(); R = runs(a, ground)
pic_bottom, let_top = R[-nlet - 1][1], R[-nlet][0]
t, big = caps_of(TEXT); size = int(W * 0.030)
while True:
    w_ = L.word(t, size, lambda ch: GREEN, big=big, colour_at=lambda i, ch: GREEN)
    if w_[1].shape[1] <= W - 360 * s: break
    size = int(size * 0.96)
rgb, al = w_; comp = rgb * al[..., None] + ground * (1 - al[..., None])
ink = np.where((np.abs(comp - ground).sum(2) > 30).any(1))[0]; ink0, ink1 = ink.min(), ink.max() + 1
need = (ink1 - ink0) + GAP * s + MIN_ABOVE * s
shift = int(np.ceil(max(0, need - (let_top - pic_bottom))))
new = a.copy()
if shift: new[let_top + shift:] = a[let_top:H - shift]
new[pic_bottom:let_top + shift] = ground
y_ink_bottom = let_top + shift - int(round(GAP * s)); y0 = y_ink_bottom - ink1
L.paste(new, w_, W / 2, y0)
Image.fromarray(np.clip(np.rint(new), 0, 255).astype(np.uint8)).save(out)
R2 = runs(new, ground); margin = H - R2[-1][1]
b4 = np.array(Image.open(v4).convert('RGB'), float)
same_pic = np.array_equal(new[:pic_bottom], a[:pic_bottom])
rows = np.where((np.abs(new - b4).sum(2) > 0).any(1))[0]
ok = Image.open(out).size == (W, H) and margin >= 60 * s and same_pic
print(f'{"ok " if ok else "BAD"} {os.path.basename(out)} | {TEXT} | {GREEN} | size {size} | lettering moved {shift} px | bottom margin {margin} px | '
      f'picture unchanged {same_pic} | rows differing from v4: {rows.min() if len(rows) else "-"}..{rows.max() if len(rows) else "-"} of {H}')
