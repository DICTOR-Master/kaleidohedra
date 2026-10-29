# Amazon KDP paperback wrap cover for "HexOct: The Laws of Stacking" (DICTO 10-29). A4 trim 8.27 x 11.69 in, 80 pages,
# standard colour on white paper: spine = 80 x 0.002252 in = 0.180 in (KDP's figure for white paper; check against KDP's
# cover calculator before upload); bleed 0.125 in on the outer edges; 300 dpi. Left to right: back, spine, front.
# Front: hexoct-cover-front.png on the dark ground. Spine: HEXOCT · DICTO, top to bottom. Back: text in Nimbus Sans, the
# barcode area (2 x 1.2 in, bottom right, 0.25 in from the trim) left empty for KDP's ISBN barcode.
import numpy as np
from PIL import Image, ImageDraw, ImageFont
DPI = 300; TW, TH, BLEED, PAGES = 8.27, 11.69, 0.125, 80; SPINE = PAGES * 0.002252
W_in, H_in = 2 * BLEED + 2 * TW + SPINE, 2 * BLEED + TH
px = lambda v: int(round(v * DPI)); W, H = px(W_in), px(H_in)
GROUND = (20, 15, 11); WHITE = (240, 240, 240); GOLD = (217, 165, 33)
im = Image.new('RGB', (W, H), GROUND); d = ImageDraw.Draw(im)
xb0, xs0 = BLEED, BLEED + TW; xf0 = xs0 + SPINE           # back trim left, spine left, front trim left (inches)
# front
fr = Image.open('../hexoct-cover-front.png').convert('RGB'); sh = TH - 0.5; sw = sh * fr.width / fr.height
fr = fr.resize((px(sw), px(sh)), Image.LANCZOS); im.paste(fr, (px(xf0 + (TW - sw) / 2), px(BLEED + 0.25)))
# spine: text reads top to bottom
fs = ImageFont.truetype('NimbusSans-Bold.otf', px(SPINE - 0.125) + 6)
t = 'HEXOCT  ·  THE LAWS OF STACKING  ·  DICTO'; tw = d.textlength(t, font=fs)
lab = Image.new('RGB', (int(tw) + 20, px(SPINE)), GROUND); ImageDraw.Draw(lab).text((10, px(SPINE) / 2), t, font=fs, fill=WHITE, anchor='lm')
lab = lab.rotate(-90, expand=True); im.paste(lab, (px(xs0), px(BLEED + TH / 2) - lab.height // 2))
# back
F = lambda name, pt: ImageFont.truetype(name, int(pt * DPI / 72))
def para(x, y, text, font, width, fill=WHITE, lead=1.42):
    words, line = text.split(), ''
    for w in words:
        if d.textlength(line + ' ' + w if line else w, font=font) > width:
            d.text((x, y), line, font=font, fill=fill); y += font.size * lead; line = w
        else: line = line + ' ' + w if line else w
    if line: d.text((x, y), line, font=font, fill=fill); y += font.size * lead
    return y
x = px(xb0 + 0.85); wid = px(TW - 1.7); y = px(BLEED + 1.0)
d.text((x, y), 'HexOct', font=F('NimbusSans-Bold.otf', 30), fill=GOLD); y += px(0.62)
d.text((x, y), 'The Laws of Stacking', font=F('NimbusSans-Regular.otf', 16), fill=WHITE); y += px(0.6)
body = F('NimbusSans-Regular.otf', 11.5)
y = para(x, y, 'Stack equal balls in close-packed layers, each new layer in the hollows of the one below, and the space between them '
         'is shared out into a few kinds of piece. This book follows three laws found in this one setting. The Rule of Halves: the gaps of '
         'any stacking are built from the gaps of the two pure stackings, whole or in halves. The Swap Rule: when the layers are squashed '
         'or stretched, the two mixed pieces always add up to the two pure ones. The Hexagonality Law: every count and every volume of the '
         'pieces is a straight line in one number, the share of hexagonal layers.', body, wid) + px(0.12)
y = para(x, y, 'The laws are tested on real materials, from silicon carbide, ice and battery oxides to spin ice and kagome magnets. The '
         'book ends with HexOct: only two tiles, one cubic and one hexagonal, build every close-packed stacking, any tile on any tile; '
         'and keyed tiles, HexOct-K, that compute.', body, wid) + px(0.3)
y = para(x, y, 'The Law gave the pieces, / The pieces prove the law.', F('NimbusSans-Italic.otf', 13), wid, fill=GOLD) + px(0.35)
y = para(x, y, 'DICTO is an artist in Osaka, Japan, with a background in architectural sculpture, stonecarving and Buddhist statuary. '
         'He builds geometric sculpture from recycled PET bottles with his own modular systems, B1NR and DICTOspheres.', F('NimbusSans-Regular.otf', 10.5), wid)
# ◆ DICTO ◆ in the cover's LED letters, centred in the free space between the text and the emblem (DICTO 10-29)
mk = Image.open('dicto-mark.png'); mw = px(3.2); mk = mk.resize((mw, int(mk.height * mw / mk.width)), Image.LANCZOS)
gap_top, gap_bot = y, px(BLEED + TH - 1.25) - px(0.75) - px(0.1)
im.paste(mk, (px(xb0 + TW / 2) - mw // 2, int((gap_top + gap_bot) / 2) - mk.height // 2), mk)
small = F('NimbusSans-Regular.otf', 9)
d.text((x, px(BLEED + TH - 1.05)), 'Open access edition: DICTO DOI 10.5281/zenodo.23731359', font=small, fill=WHITE)
d.text((x, px(BLEED + TH - 0.85)), 'Licence CC BY-SA 4.0  ·  dictospheres.com', font=small, fill=WHITE)
logo = Image.open('dicto-logo.png').convert('RGBA'); L = px(0.75); logo = logo.resize((L, L), Image.LANCZOS)
im.paste(logo, (x, px(BLEED + TH - 1.25) - L - px(0.1)), logo)
# barcode area kept clear (KDP prints the ISBN barcode here)
bx0, by0 = px(xs0 - 0.25 - 2.0), px(BLEED + TH - 0.25 - 1.2)
GUIDE = __import__('os').environ.get('GUIDES') == '1'
if GUIDE:
    for xx in (xb0, xs0, xf0, xf0 + TW): d.line([(px(xx), 0), (px(xx), H)], fill=(255, 0, 0), width=2)
    d.rectangle([bx0, by0, bx0 + px(2.0), by0 + px(1.2)], outline=(255, 0, 0), width=3)
im.save('kdp-cover-hexoct%s.pdf' % ('-guides' if GUIDE else ''), resolution=DPI, quality=95)
im.save('kdp-cover-hexoct%s.png' % ('-guides' if GUIDE else '')); print('ok', W, H, round(W_in, 4), round(H_in, 4), 'spine', round(SPINE, 4))
