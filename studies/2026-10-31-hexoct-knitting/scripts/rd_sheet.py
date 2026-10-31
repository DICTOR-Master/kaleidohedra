#!/usr/bin/env python3
"""rd/rd.json + rd/*.png -> rd/paper.html (the rhombic dodecahedron cushion pattern sheet)."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.join(HERE, '../rd')
d = json.load(open(os.path.join(RD, 'rd.json')))
T = d['tables']

# assumptions
ST_CM = 10 / 22                     # stitch width (22 sts to 10 cm)
NN_CM = 12 / math.sqrt(3) * ST_CM   # ball spacing in cm (12 stitches = sqrt(3) ball spacings)
ROW_CM = math.sqrt(2 / 3) * NN_CM / 7
YARN_PER_ST = 1.2                   # cm of yarn per stockinette stitch at this gauge (estimate)
BOBBLE_ST = 12                      # a bobble uses about as much yarn as 12 stitches (estimate)
EXTRA = 1.2                         # +20 % for seams, ends and swatching
M_PER_50G = 120                     # DK: about 120 m per 50 g (assumption)


def sizes(n):
    m = 4 * n
    face = m * NN_CM; vtx4 = math.sqrt(2) * m * NN_CM; edge = math.sqrt(3 / 8) * m * NN_CM
    vol = 16 * math.sqrt(3) / 9 * edge ** 3 / 1000
    return face, vtx4, edge, vol


def yarn(n):
    t = T[str(n)]
    dg = (t['counts']['DG'] + t['bobbles'] * BOBBLE_ST) * 12 * YARN_PER_ST / 100 * EXTRA
    lg = t['counts']['LG'] * 12 * YARN_PER_ST / 100 * EXTRA
    return dg, lg


NAMES = {1: 'small', 2: 'medium', 3: 'large'}
rows_html = []
for n in (1, 2, 3):
    t = T[str(n)]; face, v4, edge, vol = sizes(n); dg, lg = yarn(n)
    rows_html.append(f"<tr><td>{NAMES[n]} (n = {n})</td><td class=n>{t['ncol']} × {t['nrows']}</td><td class=n>{t['counts']['DG']} / {t['counts']['LG']}</td>"
                     f"<td class=n>{t['bobbles']}</td><td class=n>{edge:.1f}</td><td class=n>{face:.1f}</td><td class=n>{v4:.1f}</td>"
                     f"<td class=n>{dg:.0f} m ({dg / M_PER_50G * 50:.0f} g)</td><td class=n>{lg:.0f} m ({lg / M_PER_50G * 50:.0f} g)</td><td class=n>{vol:.1f} L</td></tr>")


def shaping_table(n, full=False):
    t = T[str(n)]; out = []
    for r in t['rows']:
        if not full and not r['shaping'] and not r['bobbles'] and r['row'] != 1: continue
        bob = ', '.join(str(b + r['first']) for b in r['bobbles'])
        runs = ', '.join(f"{k} {c}" for k, c in r['runs']) if full else ''
        out.append(f"<tr><td class=n>{r['row']}</td><td>{r['side']}</td><td class=n>{r['sts']}</td><td>{r['shaping']}</td>"
                   + (f"<td>{runs}</td>" if full else '') + f"<td>{bob}</td></tr>")
    head = "<tr><th class=n>Row</th><th>Side</th><th class=n>Sts</th><th>Shaping</th>" + ("<th>Colour runs (working order)</th>" if full else '') + "<th>Bobble (chart col.)</th></tr>"
    return f"<table class=rows>{head}{''.join(out)}</table>"


html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HexOct knitting: the rhombic dodecahedron cushion</title>
<link rel="stylesheet" href="../paper.css">
<style>body{{font-size:9.6pt}} h2{{margin:9pt 0 3pt}} p{{margin:3pt 0}} figure{{margin:4pt 0}} figure img{{width:100%;display:block}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:3%;align-items:start}} .three{{display:grid;grid-template-columns:30% 34% 34%;gap:1%;align-items:end}}
table{{border-collapse:collapse;font:8pt/1.25 "DejaVu Sans",sans-serif;width:100%;margin:2mm 0}} td,th{{border-bottom:1px solid #ddd;padding:0.6mm 1.2mm;text-align:left;vertical-align:top}} td.n,th.n{{text-align:right}}
table.rows{{font-size:7.6pt}} ul{{margin:2pt 0 2pt 14pt;padding:0}} li{{margin:1pt 0}} .chk{{border-left:3px solid #b8962e;padding-left:3mm;margin:3mm 0}}
.app{{break-before:page}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>HexOct knitting: the rhombic dodecahedron cushion</h1>
<p class="sub">Twelve knitted faces of the cubic crystal 3C, sewn into its own Voronoi cell</p>
<div class="meta"><b>DICTO</b> · pattern of 31 October 2026<br>
The idea is DICTO's: the rhombic dodecahedron (RD) is the cell of one ball in the cubic stacking 3C, its faces lie in the
planes of the knitted slice, so twelve 3C faces sewn together make a cushion whose surface is its own crystal. Geometry
checked exactly with Claude (Anthropic).</div>

<h2>1. What was checked</h2>
<div class="chk">
<p><b>(a) The slice plane is a {{110}} plane: true.</b> In cubic terms the close-packed layers of 3C are (111) planes and a
row of touching balls runs along [1-10]. The knitted slice is perpendicular to that row, so its normal is [1-10]: it is the
(1-10) plane, a {{110}} plane (the {{11-20}} plane of the hexagonal setting), and it contains the stacking direction [111].</p>
<p><b>(b) Every RD face lies in a {{110}} plane and carries the same pattern: true.</b> The RD is the Voronoi cell of a ball of
3C; its 12 faces are perpendicular to the 12 directions to the touching neighbours, the &lt;110&gt; directions, and each lies
in a {{110}} plane full of ball centres. In 3C every layer is c, so the whole cushion is gold, and the colours are only dark
(tetrahedra) and light (octahedra): they do not depend on which stacking direction is used. Each {{110}} plane contains two
&lt;111&gt; directions, 70.53° apart, and the <b>RD edges run exactly along these two directions</b>. Knitting with the rows across
one of them, two edges of the rhombus run straight up the stitch columns and the other two climb at 19.47° to the rows,
16 stitches for every 7 rows. The long diagonal of the face is a row of touching balls, the short diagonal runs along
[001]. When the edge is n × 3 layers long (n = 1, 2, 3), all four corners are ball centres and the corners of the face fall
exactly on stitch and row points of the 12-stitch, 7-row gauge: (0, 0), (16n, 7n), (16n, 28n), (0, 21n) in stitches and rows.
Exact check: the sections of the pieces cover each face exactly (n = 1: 12 triangles and 6 rhombi, whole or cut).</p>
<p><b>The face shape and the octahedron's cut: same shape, not the same piece.</b> The RD face is a rhombus with angles
70.53° / 109.47°, the same shape as the octahedron's section in the chart, but turned a quarter turn (the octahedron's
rhombus has two sides along the rows, the RD face has two sides across them) and larger: at n = 1 its edge is 2.449 ball
spacings against 0.866, 2√2 times.</p>
<p><b>(c) The pattern runs on across the seams: true.</b> All twelve faces are sections of the same crystal, so next to every
seam both faces show the same piece. Exact check at all three sizes: on all 24 seams, no point where the two faces show
different pieces. The face pattern is symmetric under both diagonals of the rhombus (exact), so <b>all 12 faces are knitted
from one chart</b>; each face is sewn with its acute corners (70.53°) at the four-edged corners of the cushion. With 12 identical
pieces right side out, the direction of the rows on each face is fixed by the geometry (arrows on the net, Section 4).
Balls on the edges and corners lie on the seams; only the inner balls are bobbles.</p>
<p><b>(d) Knitted directly, with stepped shaping; the bias is not used.</b> The left edge runs straight up the columns from
row 1 to row 21n + 1, the right edge from row 7n + 1 to the top; the slanted edges are made by adding stitches at the right
(bottom part) and removing them at the left (top part), 16n stitches over 7n rows. The bias of the swatches moves the edge
one stitch per row, which at this gauge is 51° from the columns; the RD edges lie at 0° and 70.53°, so the bias does not
make them. (In true geometry a 3C bias edge, 4 stitches per 7 rows, leans 35.26°: along the rows of touching balls, the
long diagonal of the face.) The gauge keeps the true proportions: the corners land exactly on the grid.</p>
</div>

<h2>2. Sizes</h2>
<p>Assumed gauge: 22 stitches and 27 rows to 10 cm in stockinette (DK or light worsted), which is the 5:4 stitch of the
charts; then one ball spacing is {NN_CM:.2f} cm. Yarn: about {YARN_PER_ST} cm per stitch, a bobble as much as {BOBBLE_ST}
stitches, +20 % for seams and ends, DK at about {M_PER_50G} m per 50 g (all estimates; swatch first). Bobbles in dark gold.</p>
<table><tr><th>Size</th><th class=n>Face (sts × rows)</th><th class=n>Per face DG / LG sts</th><th class=n>Bobbles per face</th><th class=n>Edge cm</th><th class=n>Face to face cm</th><th class=n>Corner to corner cm</th><th class=n>Dark gold</th><th class=n>Light gold</th><th class=n>Stuffing volume</th></tr>
{''.join(rows_html)}</table>
<p>Corner to corner: between opposite four-edged corners. For a bigger cushion at the same chart, use thicker yarn: at 15
stitches to 10 cm every length grows by 22/15 ≈ 1.47. Two colours are enough: dark gold and light gold.</p>

<div class="three">
<figure><img src="fig/face-exact-n1.png" alt="exact face n=1"><figcaption><b>The exact face</b> (small size): sections of
tetrahedra (dark) and octahedra (light), ball centres as dots; rows run across.</figcaption></figure>
<figure><img src="fig/rd-3d-n2.png" alt="cushion"><figcaption><b>The medium cushion</b> (exact): the pattern runs on over every
seam; dots are ball centres.</figcaption></figure>
<figure><img src="fig/chart-n1.png" alt="chart small"><figcaption><b>Small face chart</b>, 17 sts × 29 rows. Red: the exact
rhombus; black dots: bobbles; open dots: balls on the seams.</figcaption></figure>
</div>

<h2>3. Knitting one face</h2>
<ul>
<li>Stockinette, intarsia with bobbins; colour runs are given in working order (RS rows from the right, WS rows from the left).</li>
<li>Row 1 (RS): cast on the stitches of row 1 in dark gold. <b>Adding at the right edge</b>: cable cast-on at the start of a RS
row, backward-loop cast-on at the end of a WS row. <b>Removing at the left edge</b>: bind off at the start of a WS row; on a RS
row leave the stitches unworked at the end and bind them off at the start of the next WS row.</li>
<li>Bobble (MB) as in the swatch sheets, in dark gold. Bind off the last stitch; leave a long tail for seaming.</li>
<li>Knit 12 faces from the same chart. Block each to the rhombus (edge {sizes(1)[2]:.1f} / {sizes(2)[2]:.1f} / {sizes(3)[2]:.1f} cm, acute angle 70.5°).</li>
</ul>
<h3 style="font:600 10.5pt 'DejaVu Sans',sans-serif;color:#6b5310">Small face, row by row</h3>
{shaping_table(1, full=True)}

<div class="app"><h2>4. The net, orientation and sewing</h2>
<figure><img src="fig/net.png" alt="net"><figcaption><b>The net</b> (small size shown): faces 1–6 form the belt, 7–9 the top, 10–12
the bottom. Each arrow points up the chart (from row 1 to the last row) when the face is seen from outside. The odd belt
faces 1, 3, 5 have their rows along the true layers of the crystal around the [111] axis.</figcaption></figure>
<ul>
<li><b>Orientation.</b> Every face goes right side out with its acute corners (rows 1 and 29 for the small size) at four-edged
corners of the cushion. Turned half a turn a face shows the same pattern, so only the acute corners matter; the arrows show the
row direction that results.</li>
<li><b>Sewing order.</b> (1) Join the belt 1–2–3–4–5–6 into a ring along its six edges, matching the ball points (open dots)
on the seams. (2) Sew the top faces 7, 8, 9 to the belt and to each other, so their three obtuse corners meet at the top.
(3) Sew the bottom faces 10, 11, 12 the same way, leaving the last two seams open. Mattress stitch on the right side, one
stitch in from the edge, keeps the pattern running on.</li>
<li><b>Stuffing.</b> Polyester fibrefill or a sewn inner cushion of the same net in plain fabric; stuff firmly into the corners
with a blunt stick before closing the last seams. The volumes in the table are those of the exact RD.</li>
<li><b>Optional.</b> To have all six belt faces show the true layers, knit faces 2, 4, 6 from the mirror image of the chart.</li>
</ul></div>

<h2>5. Medium and large face charts</h2>
<div class="two">
<figure><img src="fig/chart-n2.png" alt="chart medium"><figcaption><b>Medium</b>: 33 sts × 57 rows, corners at (0,0), (32,14),
(32,56), (0,42).</figcaption></figure>
<figure><img src="fig/chart-n3.png" alt="chart large"><figcaption><b>Large</b>: 49 sts × 85 rows, corners at (0,0), (48,21),
(48,84), (0,63).</figcaption></figure></div>
<p class=small>Shaping and bobbles (rows not listed are worked straight with no bobble):</p>
<div class="two"><div><b>Medium</b>{shaping_table(2)}</div><div><b>Large</b>{shaping_table(3)}</div></div>

<h2>6. The hexagonal cousin (2H)</h2>
<p>The cell of one ball in the hexagonal stacking 2H is the trapezo-rhombic dodecahedron: 6 rhombi and 6 trapezoids (exact
check from the Voronoi cell of 2H). The 6 trapezoids are the vertical faces toward the six neighbours in the ball's own layer;
they lie in slice planes ({{11-20}}, through ball centres) and carry exactly the knitted 2H pattern, layers as rows, blue,
with the two parallel sides of the trapezoid (h and h/2 high at unit size) running up the columns. The 6 rhombi face the
three neighbours above and the three below; their planes are tilted to the layers, so they are oblique sections of the
crystal, not the knitted slice, and their pattern is a different one. A 2H cushion is therefore possible but mixes two kinds
of face; its pattern is left for later.</p>

<h2>7. Assumptions and open points</h2>
<ul>
<li>Gauge, yarn use per stitch and yarn per 50 g are assumptions; knit a gauge swatch and scale.</li>
<li>The colour of each stitch follows the same rule as the swatches (majority of the stitch's area; exact ties dark).</li>
<li>Stepped cast-on and bind-off edges are approximations of the straight slanted edges; blocking and seaming smooth them.</li>
<li>Not knitted yet.</li>
</ul>
</body></html>'''
open(os.path.join(RD, 'paper.html'), 'w').write(html)
print('written', [(n, sizes(n), yarn(n)) for n in (1, 2, 3)])
