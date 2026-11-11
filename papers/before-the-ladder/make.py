#!/usr/bin/env python3
"""Before the Ladder (DICTO 11-08: "it really needs to start long before the ladder"; "too complicated still").
Six one-page lessons below Rung 0: Looking, Sorting, Counting, Dimensions, Symmetry, Filling.
Each: one idea, one big picture, <= ~70 words, a memory hook, a hands-on try, bridges down and up."""
import math
G = '#b8892a'; INK = '#222'; FILL = 'rgba(184,137,42,.18)'
def svg(body, w=400, h=220): return f'<svg viewBox="-20 0 {w} {h}" width="100%" style="max-width:150mm" role="img">{body}</svg>'
def P(pts, fill='none', stroke=INK, sw=2, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def L(a, b, stroke=INK, sw=2, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def T(x, y, s, size=14, anchor='middle', col=INK, w='normal'): return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{col}" font-weight="{w}">{s}</text>'
def C(x, y, r=5, col=G): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'
def reg(cx, cy, r, n, a0=-90): return [(cx + r * math.cos(math.radians(a0 + 360 * k / n)), cy + r * math.sin(math.radians(a0 + 360 * k / n))) for k in range(n)]
def cube(x, y, s, d):
    f = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]; b = [(px + d, py - d) for px, py in f]
    return f, b

# 1 Looking: a box with one face, one edge, one corner picked out
f, b = cube(110, 70, 110, 45)
pic1 = (P([b[0], b[1], f[1], f[0]], fill='#eee') + P([f[1], b[1], b[2], f[2]], fill='#ddd') + P(f, fill=FILL, stroke=INK)
        + L(f[1], f[2], G, 6) + C(*b[1], 8)
        + T(165, 135, 'face', 16, col=INK, w='bold') + T(f[1][0] + 62, 150, 'edge', 16, 'start', G, 'bold') + L((f[1][0] + 4, 140), (f[1][0] + 58, 146), G, 1.2) + T(b[1][0] + 14, b[1][1] - 10, 'corner', 16, 'start', G, 'bold'))
# 2 Sorting: same shape different size / different shapes
pic2 = (P(reg(60, 110, 26, 3), fill=FILL) + P(reg(130, 105, 50, 3), fill=FILL) + P(reg(230, 110, 30, 4, -45), fill='#ddd') + P(reg(310, 110, 30, 5), fill='#ddd')
        + T(95, 190, 'same shape, two sizes', 13) + T(270, 190, 'different shapes', 13))
# 3 Counting: box and pyramid with their counts
f, b = cube(30, 80, 80, 32)
box = P([b[0], b[1], f[1], f[0]], fill='#eee') + P([f[1], b[1], b[2], f[2]], fill='#ddd') + P(f, fill=FILL)
pyr = P([(220, 170), (330, 170), (275, 60)], fill=FILL) + P([(275, 60), (330, 170), (345, 140)], fill='#ddd') + L((220, 170), (250, 140), INK, 1.4, '4 3') + L((250, 140), (345, 140), INK, 1.4, '4 3') + L((250, 140), (275, 60), INK, 1.4, '4 3')
pic3 = box + pyr + T(80, 200, 'box: 8 − 12 + 6 = 2', 13, w='bold') + T(280, 200, 'pyramid: 5 − 8 + 5 = 2', 13, w='bold')
# 4 Dimensions: point -> line -> square -> cube
pic4 = (C(30, 110, 6, INK) + T(30, 190, '0', 16, w='bold') + T(30, 208, 'point', 12)
        + L((70, 110), (130, 110), INK, 3) + C(70, 110, 4, INK) + C(130, 110, 4, INK) + T(100, 190, '1', 16, w='bold') + T(100, 208, 'line', 12)
        + P([(160, 80), (220, 80), (220, 140), (160, 140)], fill=FILL) + T(190, 190, '2', 16, w='bold') + T(190, 208, 'square', 12))
f, b = cube(258, 90, 55, 25)
pic4 += P([b[0], b[1], f[1], f[0]], fill='#eee') + P([f[1], b[1], b[2], f[2]], fill='#ddd') + P(f, fill=FILL) + T(298, 190, '3', 16, w='bold') + T(298, 208, 'cube', 12)
for x in (50, 140, 238): pic4 += T(x, 115, '→', 18, col=G, w='bold')
# 5 Symmetry: square with its four mirror lines and a turn arrow
sq = [(130, 40), (250, 40), (250, 160), (130, 160)]
pic5 = (P(sq, fill=FILL) + L((190, 25), (190, 175), G, 2, '6 4') + L((115, 100), (265, 100), G, 2, '6 4') + L((120, 30), (260, 170), G, 2, '6 4') + L((260, 30), (120, 170), G, 2, '6 4')
        + f'<path d="M 300 60 A 45 45 0 0 1 300 140" fill="none" stroke="{INK}" stroke-width="2"/>' + P([(300, 140), (292, 128), (308, 130)], fill=INK, sw=1)
        + T(318, 105, '¼ turn', 13, 'start') + T(190, 205, '4 mirror lines, 4 turns', 14, w='bold'))
# 6 Filling: triangles, squares, hexagons tile; pentagons leave a gap
def tri_tiles(x0, y0, s, nx, ny):
    h = s * 3 ** .5 / 2; out = ''
    for j in range(ny):
        for i in range(nx):
            x = x0 + i * s / 2; y = y0 + j * h
            up = (i + j) % 2 == 0
            out += P([(x, y + h), (x + s, y + h), (x + s / 2, y)] if up else [(x, y), (x + s, y), (x + s / 2, y + h)], fill=FILL, sw=1.2)
    return out
tiles = tri_tiles(10, 40, 30, 5, 3)
tiles += ''.join(P([(100 + i * 26, 40 + j * 26), (126 + i * 26, 40 + j * 26), (126 + i * 26, 66 + j * 26), (100 + i * 26, 66 + j * 26)], fill=FILL, sw=1.2) for i in range(3) for j in range(3))
for i in range(3):
    for j in range(3):
        cx = 200 + i * 22.5; cy = 52 + j * 26 + (13 if i % 2 else 0)
        tiles += P(reg(cx, cy, 15, 6, 0), fill=FILL, sw=1.2)
pent = ''.join(P(reg(320 + dx, 85 + dy, 18, 5), fill='#ddd', sw=1.2) for dx, dy in [(0, -16), (-17, 12), (17, 12)])
pic6 = tiles + pent + T(45, 175, '3', 16, w='bold') + T(139, 175, '4', 16, w='bold') + T(222, 175, '6', 16, w='bold') + T(320, 175, '5 ✗', 16, col='#a33', w='bold') + T(180, 205, 'triangles, squares and hexagons close up; pentagons leave gaps', 12)

LESSONS = [
 ('Looking', pic1,
  'Look at a box. It has flat sides, called <b>faces</b>. Where two faces meet there is a line, an <b>edge</b>. Where edges meet there is a point, a <b>corner</b>. Every shape in this course is made of these three.',
  'Face, edge, corner: flat, line, point.', 'Find a box. Touch one face, run a finger along one edge, press one corner.',
  'Nothing: this is the start.', 'Sorting shapes.'),
 ('Sorting', pic2,
  'A small die and a big die have the same <b>shape</b> but different <b>sizes</b>. A die and a pyramid have different shapes. Geometry sorts by shape first: grow or shrink a shape and it stays the same shape.',
  'Shape first, size second.', 'Gather things from the kitchen. Put the same shapes together, whatever their size.',
  'Faces, edges and corners.', 'Counting them.'),
 ('Counting', pic3,
  'Count a box: 8 corners, 12 edges, 6 faces. Now take corners, subtract edges, add faces: 8 − 12 + 6 = <b>2</b>. A pyramid: 5 − 8 + 5 = 2. Every solid without a hole through it comes to 2.',
  'Corners minus edges plus faces: always two.', 'Count a chocolate box with triangle ends: 6 corners, 9 edges, 5 faces. Does it come to 2?',
  'Sorting by shape.', 'Directions: dimensions.'),
 ('Dimensions', pic4,
  'A point has no size. Slide it: a <b>line</b>, one direction. Slide the line sideways: a <b>square</b>, two directions. Lift the square: a <b>cube</b>, three directions. Each step slides the last shape in a new direction. A fourth direction would give a shape we can only draw as a shadow.',
  'Slide in a new direction to go up one.', 'Draw a point, a line, a square. Then draw two squares and join their corners: a cube.',
  'Counting corners, edges, faces.', 'Turning and mirroring: symmetry.'),
 ('Symmetry', pic5,
  'Turn a square a quarter turn: it looks the same. Fold it along a line through its middle: the halves match. Each turn or fold that leaves a shape looking unchanged is a <b>symmetry</b>. A square has 4 turns and 4 mirror lines.',
  "If you can't tell it moved, it's symmetric.", 'Cut a paper square. Fold it in half every way you can so the halves match: you find 4 folds.',
  'Dimensions.', 'Filling a floor.'),
 ('Filling', pic6,
  'Cover a floor with one shape, no gaps, no overlaps. With equal-sided shapes only three work: <b>triangles</b>, <b>squares</b>, <b>hexagons</b>, as in a bees\' comb. Pentagons cannot: three leave a gap. One step up, filling a room with solids, is where DICTO\'s work begins.',
  'Three, four, six: the floor-fillers.', 'Cut out six paper pentagons and try to cover a table with no gaps. Then try squares.',
  'Symmetry.', 'Rung 0 of the Golden Ladder, and the Start Here page.'),
]
pages = []
for i, (name, pic, text, hook, tryit, down, up) in enumerate(LESSONS, 1):
    pages.append(f'''<section class="lesson"><p class="num">Lesson {i} of {len(LESSONS)}</p><h2>{name}</h2>
<div class="pic">{svg(pic)}</div><p class="txt">{text}</p>
<p class="hook">💡 {hook}</p><p class="try">✋ {tryit}</p>
<p class="br"><span>↓ Rests on: {down}</span><span>↑ Next: {up}</span></p></section>''')
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Before the Ladder</title><link rel="stylesheet" href="../paper.css">
<style>.lesson{{page-break-before:always}} .lesson .num{{color:#8a6a1c;font-size:10pt;margin:0}} .lesson h2{{font-size:24pt;margin:1mm 0 4mm}}
.pic{{text-align:center;margin:4mm 0 6mm}} .txt{{font-size:14pt;line-height:1.5}} .hook{{font-size:14pt;border-left:4px solid #b8892a;padding:2mm 4mm;background:#faf4e4}}
.try{{font-size:13pt}} .br{{display:flex;justify-content:space-between;color:#555;font-size:10.5pt;border-top:1px solid #ccc;padding-top:2mm;margin-top:8mm}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Before the Ladder<br><span style="font-size:0.72em;font-weight:normal">Six first lessons, from looking at a box to filling a floor</span></h1>
<div class="meta"><b>DICTO</b> · dictospheres.com · 8 November 2026 · For anyone, from the very beginning. Written by Claude (Anthropic) for DICTO.</div>
<div class="status">DRAFT for DICTO. Starts at "Looking", as proposed; DICTO's answer on the starting point is still open, so the first lesson can move earlier. One idea per page, one picture, one memory hook, one thing to try. Leads into Rung 0 and the Start Here page.</div>
<p style="font-size:13pt">DICTO's Golden Ladder climbs from one triangle to the eighth dimension. These six lessons come before its first rung. Each needs only your eyes, your hands, and things from home.</p>
<ol style="font-size:13pt">{''.join(f'<li>{l[0]}</li>' for l in LESSONS)}</ol>
{''.join(pages)}
</body></html>'''
open('~/k-research/papers/before-the-ladder/paper.html', 'w').write(html)
print('ok', len(LESSONS))
