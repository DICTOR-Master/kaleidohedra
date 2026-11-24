"""Square OEIS link card for dictospheres.com (24 Nov 2026): title in Orbitron (SIL OFL, fonts/OFL.txt), the diamond render
(renders/shots/p1.png, exact coordinates) in the middle, entry numbers below. Usage: python card.py <out.jpg>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = 1200; BG = (12, 16, 26); TXT = (232, 238, 245); SUB = (170, 182, 198); GOLD = (224, 184, 74)
def font(px, w):
    f = ImageFont.truetype(os.path.join(R, "fonts/Orbitron.ttf"), px)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
im = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(im)
def spaced(y, text, f, col, sp):
    ws = [d.textlength(c, font=f) for c in text]; W = sum(ws) + sp * (len(text) - 1); x = (S - W) / 2
    for c, w in zip(text, ws): d.text((x, y), c, font=f, fill=col); x += w + sp
def rule(y):
    d.line([(90, y), (S/2 - 40, y)], fill=SUB, width=2); d.line([(S/2 + 40, y), (S - 90, y)], fill=SUB, width=2)
    d.polygon([(S/2, y-9), (S/2+9, y), (S/2, y+9), (S/2-9, y)], fill=GOLD)
spaced(70, "OEIS", font(150, 500), TXT, 34)
rule(262)
net = Image.open(os.path.join(R, "renders/shots/p1.png")).convert("RGBA").resize((760, 760), Image.LANCZOS)
im.paste(net, ((S - 760) // 2, 268), net)
rule(1032)
f40 = font(40, 500); a, b = "JAMES BAKER", "DICTO"; wa = d.textlength(a, font=f40) + 6*(len(a)-1); wb = d.textlength(b, font=f40) + 6*(len(b)-1)
gap = 70; x0 = (S - (wa + gap + wb)) / 2
def put(x, t):
    for c in t: d.text((x, 1058), c, font=f40, fill=TXT); x += d.textlength(c, font=f40) + 6
put(x0, a); put(x0 + wa + gap, b); cx = x0 + wa + gap/2; cy = 1058 + 22
d.polygon([(cx, cy-8), (cx+8, cy), (cx, cy+8), (cx-8, cy)], fill=GOLD)
spaced(1122, "A400949   A402231   A402191", font(30, 400), SUB, 5)
im.save(sys.argv[1], quality=90); print("FINAL ok")
