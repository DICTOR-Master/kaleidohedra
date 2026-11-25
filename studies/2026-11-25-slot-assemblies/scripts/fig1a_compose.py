"""Panel for Figure 1(a): the assembled model large, the four pieces pulled apart as an inset at lower right, labelled A, B, C1, C2.
Usage: python fig1a_compose.py <shots dir> <labels.json> <out.jpg>"""
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
SH, LJ, OUT = sys.argv[1:4]; BG = (20, 22, 28)
def frame(i):
    fr = Image.open(f'{SH}/p{i}.png').convert('RGBA'); return Image.alpha_composite(Image.new('RGBA', fr.size, BG + (255,)), fr).convert('RGB')
A = frame(0); W = A.size[0]; k = 0.40; T = int(W * k)
ins = frame(1).resize((T, T), Image.LANCZOS)
d = ImageDraw.Draw(ins); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 46)
for nm, x, y in json.load(open(LJ)): d.text((x * k, y * k - 42), nm, font=f, fill=(250, 246, 236), anchor='mm', stroke_width=3, stroke_fill=(40, 30, 20))
# the assembled model is shrunk (from 1.00 in steps of 0.02) and set at the top left until no model pixel lies under the inset box
for sc in np.arange(1.0, 0.5, -0.02):
    m = int(W * sc); S = Image.new('RGB', (W, W), BG); S.paste(A.resize((m, m), Image.LANCZOS), (0, 0))
    a = np.asarray(S).astype(int); covered = int((np.abs(a[W - T - 22:, W - T - 22:] - np.array(BG)).sum(2) > 24).sum())
    if covered == 0: break
print('assembled scale %.2f' % sc)
S.paste(ins, (W - T - 10, W - T - 10)); ImageDraw.Draw(S).rectangle([W - T - 10, W - T - 10, W - 11, W - 11], outline=(90, 84, 74), width=3)   # 10 px clear of the frame edge (figure bounds check)
S.save(OUT, quality=92); print('model pixels under the inset:', covered); print('FINAL ok' if covered == 0 else 'FINAL FAIL')
