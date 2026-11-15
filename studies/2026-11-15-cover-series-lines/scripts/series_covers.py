# Put the series line of THE FIVE ORDERS OF SPACE on every front cover of the series (DICTO, 15 Nov 2026: "the orders of
# space labels aren't on all book front covers in the series"). The reference is the Platonic Solids cover
# (studies/2026-11-15-platonic-cover-circle/scripts/compose.py): series line white, LED letters (ledtext.py, DSEG14 by keshikan,
# SIL OFL; kanji from Noto Sans CJK at the LED letter height), size int(0.030 W), fitted to W - 360 s, s = W / 2400.
#
# ONE RULE FOR ALL COVERS: the series line is the top line of the lettering, centred, 87 s below its own ink (the Platonic
# gap from series line to title); below it comes, unchanged, whatever the cover already had: a sub-series line ("Cycles of
# Growth Part I/II"), then title, subtitle and the DICTO mark. The picture stays where it is; the lettering block (pixels
# copied, nothing redrawn) moves down only as far as needed to keep at least 50 s of ground between picture and series line.
# Canvas size, picture, title, subtitle and mark are unchanged. Wording from papers/series-five-orders/series_line.py.
#
# Run: python series_covers.py PAPERS_DIR    (writes <cover>-series-v2.png beside each cover; prints one line per cover)
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ledtext as L
P = os.path.abspath(sys.argv[1]); os.chdir(os.path.dirname(os.path.abspath(__file__)))   # ledtext opens the LED font by name
sys.path.insert(0, os.path.join(P, 'series-five-orders'))
from series_line import series_text
WHITE = (255, 255, 255)
GAP, MIN_ABOVE = 87, 50            # at the 2400-wide scale
from series_covers_list import COVERS
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
bad = 0
for rel, book, part, nlet in COVERS:
    if book == 8: continue   # the Platonic Solids cover is the reference
    path = os.path.join(P, rel); im = Image.open(path).convert('RGB'); W, H = im.size; s = W / 2400
    a = np.array(im, float); ground = a[-3, 3].copy(); R = runs(a, ground)
    pic_bottom, let_top = R[-nlet - 1][1], R[-nlet][0]
    text = series_text(book, part); t, big = caps_of(text); size = int(W * 0.030)
    while True:
        w_ = L.word(t, size, lambda ch: WHITE, big=big)
        if w_[1].shape[1] <= W - 360 * s: break
        size = int(size * 0.96)
    rgb, al = w_; comp = rgb * al[..., None] + ground * (1 - al[..., None])
    ink = np.where((np.abs(comp - ground).sum(2) > 30).any(1))[0]; ink0, ink1 = ink.min(), ink.max() + 1
    need = (ink1 - ink0) + GAP * s + MIN_ABOVE * s
    shift = int(np.ceil(max(0, need - (let_top - pic_bottom))))
    assert not (np.abs(a[H - shift:] - ground).sum(2) > 30).any() if shift else True, rel + ': lettering would leave the canvas'
    new = a.copy()
    if shift:
        new[let_top + shift:] = a[let_top:H - shift]
    new[pic_bottom:let_top + shift] = ground
    y_ink_bottom = let_top + shift - int(round(GAP * s)); y0 = y_ink_bottom - ink1
    L.paste(new, w_, W / 2, y0)
    d_, b_ = os.path.split(path); out = os.path.join(d_, b_[:-4].replace('-series', '') + '-series-v2.png')
    Image.fromarray(np.clip(np.rint(new), 0, 255).astype(np.uint8)).save(out)
    R2 = runs(new, ground); margin = H - R2[-1][1]
    ok = Image.open(out).size == (W, H) and margin >= 60 * s and np.array_equal(new[:pic_bottom], a[:pic_bottom])
    bad += not ok
    print(f'{"ok " if ok else "BAD"} {rel} -> {os.path.basename(out)} | {text} | size {size} | picture bottom {pic_bottom} | '
          f'lettering moved {shift} px | bottom margin {margin} px (was {H - R[-1][1]})', flush=True)
print('FINAL ok' if not bad else f'FINAL FAIL: {bad} covers')
