# The DICTO mark on figures (DICTO 2026-10-13: "everything made bears our mark"): the gold emblem and "DICTO · dictospheres.com",
# bottom right, sized to the image. Marks in place; skips images already marked (a small sidecar list keeps track).
# Usage: python3 scripts/dicto-mark.py image.png [more.png ...]
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
EMBLEM = os.path.join(HERE, '..', 'assets', 'brand', 'dicto-emblem.png')
GOLD = (232, 194, 90, 235)
def font(px):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans.ttf']:
        try: return ImageFont.truetype(f, px)
        except OSError: pass
    return ImageFont.load_default()
for path in sys.argv[1:]:
    log = os.path.join(os.path.dirname(path) or '.', '.dicto-marked.json')
    done = json.load(open(log)) if os.path.exists(log) else []
    if os.path.basename(path) in done: continue
    im = Image.open(path).convert('RGBA'); W, H = im.size
    e = max(28, int(min(W, H) * 0.07))
    em = Image.open(EMBLEM).convert('RGBA').resize((e, e), Image.LANCZOS)
    f = font(max(11, int(e * 0.32))); text = 'DICTO · dictospheres.com'
    d = ImageDraw.Draw(im); tw = d.textlength(text, font=f)
    pad = int(e * 0.35)
    x0 = int(W - pad - e - pad // 2 - tw); y = H - pad - e
    im.alpha_composite(em, (W - pad - e, y))
    d.text((x0, y + e / 2), text, font=f, fill=GOLD, anchor='lm')
    im.convert('RGB').save(path) if path.lower().endswith(('.jpg', '.jpeg')) else im.save(path)
    done.append(os.path.basename(path)); json.dump(done, open(log, 'w'))
    print('marked', path)
