# Amazon KDP paperback wrap cover for "DICTONIC Bonds: from the Octet to the Rule of Halves" (2026-11-03), copied from Star Cores'
# (DICTO 10-31: "back cover same"; after The Golden Cycle's and HexOct's, DICTO 10-29). A4 trim 8.27 x 11.69 in, PAGES interior pages
# (env, default 105: DRAFT-bonds-book.pdf of 3 Nov), standard colour on white paper: spine = PAGES x 0.002252 in (KDP's figure for white
# paper; check against KDP's cover calculator before upload); bleed 0.125 in on the outer edges; 300 dpi. Left to right: back, spine, front.
# Front: bonds-cover-front.png on the dark ground. Spine (only above 79 pages, KDP's rule, as the Alicia cover): title · subtitle · DICTO,
# top to bottom. Back: text in Nimbus Sans, the barcode area (2 x 1.2 in, bottom right, 0.25 in from the trim) left empty for KDP's ISBN
# barcode. Not part of a series: no series line.
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
DPI = 300; TW, TH, BLEED = 8.27, 11.69, 0.125; PAGES = int(os.environ.get('PAGES', 105)); SPINE = PAGES * 0.002252   # 105 = the draft of 3 Nov; rerun with PAGES= if it changes
W_in, H_in = 2 * BLEED + 2 * TW + SPINE, 2 * BLEED + TH
px = lambda v: int(round(v * DPI)); W, H = px(W_in), px(H_in)
GROUND = (20, 15, 11); WHITE = (240, 240, 240); GOLD = (217, 165, 33); TEAL = (72, 206, 188)
im = Image.new('RGB', (W, H), GROUND); d = ImageDraw.Draw(im)
xb0, xs0 = BLEED, BLEED + TW; xf0 = xs0 + SPINE           # back trim left, spine left, front trim left (inches)
# front
fr = Image.open(os.environ.get('FRONT', '../bonds-cover-front.png')).convert('RGB'); sh = TH - 0.5; sw = sh * fr.width / fr.height
fr = fr.resize((px(sw), px(sh)), Image.LANCZOS); im.paste(fr, (px(xf0 + (TW - sw) / 2), px(BLEED + 0.25)))
# spine: text reads top to bottom
if PAGES > 79:   # KDP allows spine text only on books of more than 79 pages
    fs = ImageFont.truetype('NimbusSans-Bold.otf', px(SPINE - 0.125) + 6)
    t = 'DICTONIC BONDS  ·  FROM THE OCTET TO THE RULE OF HALVES  ·  DICTO'; tw = d.textlength(t, font=fs)
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
d.text((x, y), 'DICTONIC Bonds', font=F('NimbusSans-Bold.otf', 30), fill=GOLD); y += px(0.62)
d.text((x, y), 'from the Octet to the Rule of Halves', font=F('NimbusSans-Regular.otf', 16), fill=TEAL); y += px(0.6)   # teal, as on the front
body = F('NimbusSans-Regular.otf', 11.5)
# blurb from the book's preface (front.html); claims only from the book
y = para(x, y, 'A space-filler is a solid whose copies pack together with no gaps, like bricks. Most solids cannot do this alone, but '
         'some can in pairs. DICTO calls such a pair a DICTONIC bond, and there are four: the Golden bond, Icosaxes and Unborn Axes; '
         'the Keyed bond, Lotus Jewel Axes and Dodecaxes; the Delian bond, Samson and Delilah; and the Twinned Delian bond, Sonsam '
         'and Lahdeli. Their eight solids make the square on the cover.', body, wid) + px(0.12)
y = para(x, y, 'DICTO proposed that the bond papers are one series building to the Rule of Halves, and this book follows that path. '
         'Every mix of the five Platonic solids fills space, with a kit of seven connectors. Cutting the gaps of a filling at the right '
         'place finds the first pairs: the golden point of the icosahedra, and the cut through the octet where Samson and Delilah have '
         'equal volume. The golden and the Delian families are each one set of points of two kinds with one weight slid between the '
         'kinds; the book follows which faces are shared as the weight slides, there and in ten more crystal networks. Turned on every way of stacking balls at once, the same weight gives the Rule of Halves: every '
         'piece is borrowed, whole or in half, from the two pure stackings. Eleven chapters, each one published paper kept word for word '
         'with its DICTO DOI.', body, wid) + px(0.35)
y = para(x, y, 'DICTO is an artist in Osaka, Japan, with a background in architectural sculpture, stonecarving and Buddhist statuary. '
         'He builds geometric sculpture from recycled PET bottles with his own modular systems, B1NR and DICTOspheres. He is also the author of '
         'HexOct: The Hexagonality Law, Alicia in Wonderland, The Golden Cycle, Star Cores and Quanta of Space: A Manifesto.', F('NimbusSans-Regular.otf', 10.5), wid)
# ◆ DICTO ◆ in the cover's LED letters, centred in the free space between the text and the emblem (DICTO 10-29)
mk = Image.open('../dicto-mark.png'); mw = px(3.2); mk = mk.resize((mw, int(mk.height * mw / mk.width)), Image.LANCZOS)
gap_top, gap_bot = y, px(BLEED + TH - 1.25) - px(0.75) - px(0.1)
im.paste(mk, (px(xb0 + TW / 2) - mw // 2, int((gap_top + gap_bot) / 2) - mk.height // 2), mk)
small = F('NimbusSans-Regular.otf', 9)
d.text((x, px(BLEED + TH - 1.05)), 'Open access edition: DICTO DOI ' + os.environ.get('DOI', '(to come)'), font=small, fill=WHITE)
d.text((x, px(BLEED + TH - 0.85)), 'Licence CC BY-SA 4.0  ·  dictospheres.com', font=small, fill=WHITE)
logo = Image.open('dicto-logo.png').convert('RGBA'); L = px(0.75); logo = logo.resize((L, L), Image.LANCZOS)
im.paste(logo, (x, px(BLEED + TH - 1.25) - L - px(0.1)), logo)
# barcode area kept clear (KDP prints the ISBN barcode here)
bx0, by0 = px(xs0 - 0.25 - 2.0), px(BLEED + TH - 0.25 - 1.2)
GUIDE = __import__('os').environ.get('GUIDES') == '1'
if GUIDE:
    for xx in (xb0, xs0, xf0, xf0 + TW): d.line([(px(xx), 0), (px(xx), H)], fill=(255, 0, 0), width=2)
    d.rectangle([bx0, by0, bx0 + px(2.0), by0 + px(1.2)], outline=(255, 0, 0), width=3)
im.save('../kdp-cover-bonds%s.pdf' % ('-guides' if GUIDE else ''), resolution=DPI, quality=95)
im.save('../kdp-cover-bonds%s.png' % ('-guides' if GUIDE else '')); print('ok', W, H, round(W_in, 4), round(H_in, 4), 'spine', round(SPINE, 4))
