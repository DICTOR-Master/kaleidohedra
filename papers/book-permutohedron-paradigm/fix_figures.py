# Book-only fixes to three chapter figures (13 Nov 2026), written to figures-fixed/ so that assemble.py always uses them:
#  ch5 ti-crystal-slices.png: the chapter's figure with its old title line cut off (the title used a word the house rules ban);
#  ch4 fig-chamfered.png and ch10 queens-vacuus.png: the DICTO mark added at the lower right (the originals carry none).
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'figures-fixed')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def mark(src, dst):
    im = Image.open(src).convert('RGB'); w, h = im.size
    f = ImageFont.truetype(FONT, max(14, w // 110)); t = 'DICTO · dictospheres.com'
    d = ImageDraw.Draw(im); tw = d.textlength(t, font=f)
    d.text((w - tw - w // 80, h - f.size - h // 60), t, font=f, fill=(154, 123, 47))
    os.makedirs(os.path.dirname(dst), exist_ok=True); im.save(dst)
src = Image.open(os.path.join(P, 'paradigm-ch05/figures/football-slices.png')).convert('RGB')
os.makedirs(os.path.join(OUT, 'ch5'), exist_ok=True)
src.crop((0, 52, src.size[0], src.size[1])).save(os.path.join(OUT, 'ch5', 'ti-crystal-slices.png'))
mark(os.path.join(P, 'paradigm-ch04/figures/fig-chamfered.png'), os.path.join(OUT, 'ch4', 'fig-chamfered.png'))
mark(os.path.join(P, 'paradigm-ch10/figures/queens-vacuus.png'), os.path.join(OUT, 'ch10', 'queens-vacuus.png'))
print('fixed figures written')
