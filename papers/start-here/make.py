#!/usr/bin/env python3
"""Roadmap step 3: 'Start Here' page draft for dictospheres.com (LOCAL ONLY, not deployed).
Writes paper.html: dark site look on screen, light print look (print.mjs -> PDF for DICTO)."""
import math, itertools
PHI = (1 + 5 ** 0.5) / 2
GOLD = '#e8c25a'

# ---------- the five solids, D·I·C·T·O order ----------
def cyc(p):
    x, y, z = p; return [(x, y, z), (y, z, x), (z, x, y)]
def signs(p):
    out = set()
    for s in itertools.product([1, -1], repeat=3):
        out.add(tuple(a * b for a, b in zip(s, p)))
    return list(out)
def uniq(ps): 
    r = []
    for p in ps:
        if all(sum((a - b) ** 2 for a, b in zip(p, q)) > 1e-9 for q in r): r.append(p)
    return r
cube = signs((1, 1, 1))
octa = uniq([q for p in [(1, 0, 0)] for c in cyc(p) for q in signs(c)])
tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
icosa = uniq([q for c in cyc((0, 1, PHI)) for q in signs(c)])
dodeca = uniq(cube + [q for c in cyc((0, 1 / PHI, PHI)) for q in signs(c)])
SOLIDS = [('Dodecahedron', dodeca, '12 pentagons'), ('Icosahedron', icosa, '20 triangles'),
          ('Cube', cube, '6 squares'), ('Tetrahedron', tetra, '4 triangles'), ('Octahedron', octa, '8 triangles')]
assert [len(s[1]) for s in SOLIDS] == [20, 12, 8, 4, 6]

def edges(V):
    d = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b))
    m = min(d(a, b) for a, b in itertools.combinations(V, 2))
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(d(V[i], V[j]) - m) < 1e-6]
def rot(p, ax, ay):
    x, y, z = p
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    return x, y, z
def solid_svg(V, size=110):
    E = edges(V); R = max(math.sqrt(sum(c * c for c in v)) for v in V)
    P = [rot(v, 0.42, 0.63) for v in V]
    s = size * 0.42 / R; c = size / 2
    out = []
    for i, j in sorted(E, key=lambda e: P[e[0]][2] + P[e[1]][2]):
        z = (P[i][2] + P[j][2]) / 2
        back = z < -1e-6
        out.append(f'<line x1="{c+P[i][0]*s:.1f}" y1="{c-P[i][1]*s:.1f}" x2="{c+P[j][0]*s:.1f}" y2="{c-P[j][1]*s:.1f}" '
                   f'stroke="var(--gold)" stroke-width="{1.1 if back else 2}" opacity="{0.35 if back else 1}"{" stroke-dasharray=\"3 3\"" if back else ""}/>')
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img">{"".join(out)}</svg>'
assert [len(edges(s[1])) for s in SOLIDS] == [30, 30, 12, 6, 12]

five = ''.join(f'<figure>{solid_svg(V)}<figcaption><b>{n}</b><br>{f}</figcaption></figure>' for n, V, f in SOLIDS)

# ---------- rule 2: squares close, pentagons leave a gap ----------
def poly(cx, cy, r, n, a0):
    return ' '.join(f'{cx+r*math.cos(a0+2*math.pi*k/n):.1f},{cy+r*math.sin(a0+2*math.pi*k/n):.1f}' for k in range(n))
sq = ''.join(f'<rect x="{10+i*34}" y="{12+j*34}" width="34" height="34" fill="none" stroke="var(--gold)" stroke-width="1.6"/>' for i in range(4) for j in range(4))
# three regular pentagons sharing one corner at (0,0): each wedge 108 deg
pent = []
side = 46
for k in range(3):
    start = math.radians(-90 + 18 + k * 108)
    pts = [(0.0, 0.0)]; ang = start; x = y = 0.0
    for _ in range(4):
        x += side * math.cos(ang); y += side * math.sin(ang); pts.append((x, y)); ang += math.radians(72)
    pent.append('<polygon points="' + ' '.join(f'{240+px:.1f},{80+py:.1f}' for px, py in pts) + '" fill="rgba(232,194,90,.12)" stroke="var(--gold)" stroke-width="1.6"/>')
# gap wedge: remaining 36 deg
g0 = math.radians(-90 + 18 + 3 * 108); g1 = g0 + math.radians(36)
gap = f'<path d="M240,80 L{240+side*math.cos(g0):.1f},{80+side*math.sin(g0):.1f} L{240+side*math.cos(g1):.1f},{80+side*math.sin(g1):.1f} Z" fill="#c0392b" opacity=".75"/>'
rule2 = (f'<svg viewBox="0 0 330 190" width="100%" style="max-width:420px" role="img" aria-label="Squares cover a floor; three pentagons round a corner leave a gap">'
         f'{sq}<text x="78" y="182" fill="var(--muted)" font-size="11" text-anchor="middle">4 × 90° = 360°: closed</text>'
         f'{"".join(pent)}{gap}<text x="240" y="182" fill="var(--muted)" font-size="11" text-anchor="middle">3 × 108° = 324°: 36° gap</text></svg>')

# ---------- rule 3: layers A, B, C seen from the side ----------
def layers(seq, x0, label):
    out = []; r = 6; pitch = 2 * r
    off = {'A': 0, 'B': pitch / 3, 'C': 2 * pitch / 3}
    for row, L in enumerate(seq):
        y = 160 - row * 2 * r * 0.9
        for k in range(5):
            out.append(f'<circle cx="{x0+off[L]+k*pitch:.1f}" cy="{y:.1f}" r="{r-0.6}" fill="rgba(232,194,90,.18)" stroke="var(--gold)" stroke-width="1.1"/>')
        out.append(f'<text x="{x0-12}" y="{y+4:.1f}" fill="var(--text)" font-size="11" text-anchor="middle">{L}</text>')
    for row in range(1, len(seq) - 1):
        y = 160 - row * 2 * r * 0.9
        ch = 'h' if seq[row - 1] == seq[row + 1] else 'c'
        out.append(f'<text x="{x0+5*pitch+14:.1f}" y="{y+4:.1f}" fill="{GOLD if ch=="h" else "var(--muted)"}" font-size="11" font-weight="bold">{ch}</text>')
    out.append(f'<text x="{x0+40}" y="190" fill="var(--muted)" font-size="11" text-anchor="middle">{label}</text>')
    return ''.join(out)
rule3 = ('<svg viewBox="0 82 400 116" width="100%" style="max-width:600px" role="img" aria-label="Three stacks of layers: ABCABC, ABABAB and a mixed order">'
         + layers('ABCABCA', 22, 'ABCABC…: all c') + layers('ABABABA', 158, 'ABABAB…: all h') + layers('ABCBCAB', 294, 'any order: c and h mixed') + '</svg>')

# ---------- printable nets: unfolded from the real solids (nets.py), same edge ----------
import nets as N
def net_svg(tri, tb, label, rotate=False, E=60):
    if rotate:
        tri = {f: {v: (-p[1], p[0]) for v, p in t.items()} for f, t in tri.items()}
        tb = [tuple((-p[1], p[0]) for p in x) for x in tb]
    x0, y0, x1, y1 = N.bbox(tri); W, H = x1 - x0 + 30, y1 - y0 + 40
    body = N.svg(tri, tb, 15 - x0, 15 - y0)
    return (f'<svg class="net" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}mm" height="{H:.0f}mm" style="max-width:100%;height:auto;background:#fff" role="img" aria-label="Cut-out net: {label}">'
            + body + f'<text x="15" y="{H-13:.0f}" font-size="4.2" fill="#555">{label} · DICTO · dictospheres.com</text><text x="15" y="{H-7:.0f}" font-size="4.2" fill="#555">edge {E} mm · print at 100% · grey = glue tabs</text></svg>')
_t, _tt, _o, _ot = N.make(60)
nets = '<h3>Tetrahedron (make two)</h3>' + net_svg(_t, _tt, 'tetrahedron') + '</section><section class="netpage"><h3>Octahedron (make one)</h3>' + net_svg(_o, _ot, 'octahedron', rotate=True)
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Start Here · DICTO</title>
<style>
:root{{--bg:#0a0b10;--text:#eef0f6;--muted:#9aa0b4;--gold:#e8c25a;--line:rgba(255,255,255,.12)}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:17px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:760px;margin:0 auto;padding:24px 16px 64px}}
.status{{border:2px solid #c0392b;color:#ffb3a8;padding:10px 14px;border-radius:8px;font-size:14px;margin:0 0 24px}}
.logo{{width:64px;height:64px}} h1{{font-size:40px;line-height:1.15;margin:8px 0 4px;color:var(--gold)}}
.lead{{font-size:20px;color:var(--text)}} h2{{color:var(--gold);font-size:26px;margin:44px 0 6px}} h2 .n{{display:inline-block;width:38px;height:38px;border:2px solid var(--gold);border-radius:50%;text-align:center;line-height:34px;margin-right:10px;font-size:20px}}
.photo{{border:2px dashed var(--line);border-radius:12px;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;color:var(--muted);text-align:center;padding:16px;margin:18px 0}}
.five{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:12px 0}} .five figure{{margin:0;text-align:center;width:128px}} figcaption{{font-size:13px;color:var(--muted)}} figcaption b{{color:var(--text)}}
.pic{{text-align:center;margin:14px 0}} figure.ph{{margin:18px 0}} figure.ph img{{width:100%;height:auto;border-radius:12px;display:block}} figure.ph figcaption{{color:var(--muted);font-size:14px;margin-top:6px}} .try{{border-left:4px solid var(--gold);padding:6px 14px;margin:14px 0;background:rgba(232,194,90,.06)}}
.word{{color:var(--muted);font-size:15px}} a{{color:var(--gold)}} .next li{{margin:6px 0}} .small{{font-size:14px;color:var(--muted)}}
@media print{{
 :root{{--bg:#fff;--text:#111;--muted:#555;--gold:#8a6a1c;--line:#bbb}} body{{font-size:11pt}} h1{{font-size:26pt}} h2{{font-size:16pt;margin-top:22px}} .lead{{font-size:13pt}}
 .status{{color:#a01f12}} section{{page-break-inside:avoid}} .netpage{{page-break-before:always}} main{{padding:0}}
}}
</style></head><body><main>
<div class="status">DRAFT for DICTO, local only, not on the site. Title: "Start Here" (DICTO, 8 November). Photos: DICTO, 8 November. The three rules are a proposal for DICTO to keep, change or replace.</div>
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Start Here</h1>
<p class="lead">DICTO is a sculptor in Osaka. He builds from recycled PET bottles, and the shapes he builds lead into questions nobody had answered. You need no mathematics to follow. Three rules carry the whole project.</p>
<figure class="ph"><img src="sculpture-stream-1.jpg" width="1050" height="1400" alt="A tall open frame of clear PET bottles joined at white nodes, standing in the shallow Takasegawa river in Kyoto under autumn leaves" loading="lazy"><figcaption>DICTO's PET-bottle sculpture standing in the Takasegawa river, Kyoto: The 3rd Kyoto Takasegawa Art Festival, 7–23 November 2026, open 24 hours, between Sanjo and Shijo streets</figcaption></figure>
<p>Before the bottles there was stone and wood. DICTO trained as a stonemason, a Buddhist statue wood-carver and a restoration technician. In 2012 he was one of the Buddhist sculptors who restored a wooden statue attributed to Kōbō Daishi (Kūkai), in the restoration led by the master carver Hōju Hase; his name is written in kanji beneath the statue.</p>
<figure class="ph"><img src="fudo-myoo-statue.jpg" width="791" height="1200" alt="A Buddhist figure carved in wood, Fudō Myōō, holding an upright sword before a flame halo, photographed close in black and white" loading="lazy"><figcaption>Fudō Myōō, the wisdom king with the sword, carved in wood</figcaption></figure>

<section>
<h2 id="rule-1"><span class="n">1</span>There are five perfect shapes</h2>
<p>Take one flat shape, the same every time, and build a closed solid where every corner looks the same. It can be done in exactly five ways, and no more. They are the five dice in a role-playing set. DICTO's name carries them, one letter each: <b>D</b>odecahedron, <b>I</b>cosahedron, <b>C</b>ube, <b>T</b>etrahedron, <b>O</b>ctahedron.</p>
<div class="five">{five}</div>
<p class="word">The word: <i>Platonic solids</i>. Plato wrote about them around 360 BC; the proof that there are only five is in Euclid.</p>
<div class="try">✋ Pick up a die. Count its corners, its edges and its faces: 8, 12 and 6. Now 8 − 12 + 6 = 2. Try the same sum on any of the five, and it always comes to 2.</div>
</section>

<section>
<h2 id="rule-2"><span class="n">2</span>Fill space with no gaps</h2>
<p>Squares cover a bathroom floor: four meet at every corner and close up. Pentagons cannot: three leave a gap, four overlap. The same holds one step up. Pack a car boot so perfectly that no air is left between the boxes, and you have filled space. Of the five perfect shapes, only the cube does it alone. Tetrahedra and octahedra do it together, two to one, the frame of many roofs and climbing frames.</p>
<div class="pic">{rule2}</div>
<p>Most shapes cannot fill space. DICTO hunts for the ones that can, and has found new ones: the HexOct pieces, and Narcissus, a single piece that fills space all by itself.</p>
<figure class="ph"><img src="block-corbel-balance.jpg" width="900" height="1200" alt="Wooden blocks stacked on one upright block, each course reaching out past the one below, held by weight alone" loading="lazy"><figcaption>DICTO's block corbel: each course reaches out past the one below, held by weight alone, with no keystone. Corbelled openings come to a point, like a lancet arch</figcaption></figure>
<p class="word">The words: <i>tiling</i> (a floor), <i>space-filling</i> (a room), <i>octet</i> (tetrahedra and octahedra together).</p>
<figure class="ph"><img src="sculpture-stream-2.jpg" width="1400" height="1050" alt="The same PET-bottle sculpture seen from upstream, its bottles and nodes forming triangles over the water" loading="lazy"><figcaption>The same sculpture from upstream</figcaption></figure>
</section>

<section>
<h2 id="rule-3"><span class="n">3</span>Layers can stack in any order</h2>
<p>Stack oranges on a market stall: each new layer sits in the dips of the one below. There are only three places a layer can sit, A, B and C. Look at any layer and its two neighbours. If they match (…A B A…) the layer turns back: call it <b>h</b>. If they differ (…A B C…) it carries straight on: call it <b>c</b>.</p>
<div class="pic">{rule3}</div>
<p>Every string of c's and h's is a stacking that can be built, and real crystals use many of them. DICTO found what stays the same whatever the order. One example: in the diamond-like network built on any stacking, every atom sits on exactly the same number of closed loops of each length (the Loop Equality, paper #102). And DICTO turned the rule into cloth: in Knitting Crystals (#83) the knitted sheets are the layers, and the linking yarns run straight on at a c layer and turn back at an h layer, so the fabric is the crystal.</p>
<p class="word">The words: <i>close-packed layers</i>, <i>stacking</i>, <i>hexagonality</i> (the share of h layers).</p>
</section>

<section>
<h2>Try it with your hands</h2>
<p>Print the sheet below at 100%, cut, fold and glue, or download <a href="build-the-five.pdf">Build the Five</a>, a kit of all five perfect shapes and the rhombic dodecahedron, one A4 page each. You get a tetrahedron and an octahedron with the same edge. Make two tetrahedra and one octahedron, and you hold rule 2: they fit face to face with no gaps, and the pattern goes on for ever.</p>
</section>

<section>
<h2>Where next</h2>
<ul class="next">
<li><b>Before the Ladder</b>: short lessons from the very beginning, one idea each, with a picture, a memory hook and something to try. <span class="small">(in preparation)</span></li>
<li><b>Play</b>: <a href="https://rhombiverse.dictospheres.com/rhombis.html">RHOMBIS</a>, the puzzle app, and the three apps on the home page.</li>
<li><b>Read</b>: <a href="../#books">the books</a>, each with its own cover on the home page, in seven languages.</li>
<li><b>Words</b>: an everyday glossary of the geometry words used on this site. <span class="small">(in preparation)</span></li>
</ul>
<p class="small">DICTO · dictospheres.com</p>
</section>

<section class="netpage">
<h2>Cut-out sheets</h2>
{nets}
</section>
</main></body></html>'''
open('/home/dicto/k-research/papers/start-here/paper.html', 'w').write(page)
import re as _re
live = _re.sub(r'<div class="status">.*?</div>\n', '', page, flags=_re.S)
live = _re.sub(r'<div class="photo">.*?</div>\n', '', live, flags=_re.S)
live = _re.sub(r'<li>[^\n]*\(in preparation\)</span></li>\n', '', live)
live = live.replace('<title>Start Here · DICTO</title>', '<title>Start Here · DICTO</title>\n<meta name="description" content="Start here: DICTO\'s geometry in three rules, five perfect shapes, filling space with no gaps, and layers that stack in any order, with nets to print and build.">\n<link rel="canonical" href="https://dictospheres.com/start-here/">\n<link rel="icon" href="../favicon.png">')
live = live.replace('src="../dicto-logo.png"', 'src="../dicto-logo.png?v=2"').replace('<p class="small">DICTO · dictospheres.com</p>', '<p class="small"><a href="../">DICTO · dictospheres.com</a></p>')
assert 'status' not in live.split('</style>')[1] and 'class="photo"' not in live.split('</style>')[1] and 'in preparation' not in live
open('/home/dicto/k-research/papers/start-here/live-index.html', 'w').write(live)
print('ok', len(page))
