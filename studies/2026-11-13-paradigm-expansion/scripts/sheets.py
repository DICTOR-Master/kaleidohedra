# contact sheets and page zooms of a PDF, for looking at every page (run on the compute host).
# usage: sheets.py PDF OUTDIR [zoom pages, comma separated]   -> OUTDIR/sheet-NN.png (4 x 3 pages each), OUTDIR/page-NNN.png
import sys, os, subprocess, glob
from PIL import Image, ImageDraw
pdf, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*.png')): os.remove(f)
tmp = os.path.join(out, 'tmp'); os.makedirs(tmp, exist_ok=True)
import shutil
if shutil.which('pdftoppm'): subprocess.run(['pdftoppm', '-r', '38', '-png', pdf, os.path.join(tmp, 'p')], check=True)
else: subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=png16m', '-r38', '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', '-o', os.path.join(tmp, 'p-%03d.png'), pdf], check=True)
pages = sorted(glob.glob(os.path.join(tmp, 'p-*.png'))); W, H = Image.open(pages[0]).size
per = 12
for s in range(0, len(pages), per):
    sheet = Image.new('RGB', (4 * W + 50, 3 * (H + 18) + 10), 'white'); d = ImageDraw.Draw(sheet)
    for k, p in enumerate(pages[s:s + per]):
        x = 10 + (k % 4) * (W + 10); y = 5 + (k // 4) * (H + 18)
        sheet.paste(Image.open(p), (x, y + 14)); d.rectangle([x, y + 14, x + W - 1, y + 14 + H - 1], outline='#888'); d.text((x, y), f'p. {s + k + 1}', fill='black')
    sheet.save(os.path.join(out, f'sheet-{s // per + 1:02d}.png'))
for f in pages: os.remove(f)
if len(sys.argv) > 3 and sys.argv[3]:
    for n in [int(x) for x in sys.argv[3].split(',')]:
        subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=png16m', '-r90', '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', f'-dFirstPage={n}', f'-dLastPage={n}', '-o', os.path.join(out, f'page-{n:03d}.png'), pdf], check=True)
print('sheets', (len(pages) + per - 1) // per, 'pages', len(pages)); print('FINAL ok')
