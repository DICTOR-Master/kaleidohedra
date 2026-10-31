#!/usr/bin/env python3
"""4H swatch sheet: one period (A B C B A), 24 stitches x 29 rows, from the chart of knit.py.

Crop: chart rows 1-29, columns taken half a repeat (6 stitches) later than in chart-4H.png so the ball stitches sit in
columns 7 and 19, away from the edges (the pattern repeats every 12 stitches, so this is the same fabric).
Writes ../swatch/fig/chart.png, ../swatch/fig/slice.png, ../swatch/paper.html, ../out/swatch-rows.json.
Usage (dicto-big-brother): LOGO=~/kres-tmp/dicto-logo.png ~/geom/bin/python swatch.py
"""
import os, json
import knit
from knit import *  # noqa
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle, Rectangle

SW = os.path.join(HERE, '../swatch')
NR = 29
PH = 6                                 # column phase (stitches)
NAME = {GOLD_D: 'dark gold', GOLD_L: 'light gold', BLUE_D: 'dark blue', BLUE_L: 'light blue'}
ABBR = {GOLD_D: 'DG', GOLD_L: 'LG', BLUE_D: 'DB', BLUE_L: 'LB'}


def runs(cells):
    out = []
    for c in cells:
        if out and out[-1][1] == c: out[-1][0] += 1
        else: out.append([1, c])
    return out


def main():
    os.makedirs(os.path.join(SW, 'fig'), exist_ok=True)
    halves = build()
    grid, balls, S, bias, ties = chart(halves)
    G = [[grid[j][(c - PH) % NCOL] for c in range(NCOL)] for j in range(NR)]
    B = sorted({(j, (c + PH) % NCOL) for j, c in balls if j < NR})
    assert {c for j, c in B} == {6, 18}
    # rows
    rows = []
    for j in range(NR):
        rs = (j % 2 == 0)                      # row 1 (j=0) is a RS row
        order = list(range(NCOL - 1, -1, -1)) if rs else list(range(NCOL))
        rr = runs([G[j][c] for c in order])
        b = bias[j]                             # +1: row moves right (seen from RS), -1: left
        rows.append(dict(row=j + 1, side='RS' if rs else 'WS', runs=[(n, ABBR[c]) for n, c in rr], bias=b,
                         shift=S[j], balls=[c + 1 for jj, c in B if jj == j]))
    json.dump(rows, open(os.path.join(HERE, '../out/swatch-rows.json'), 'w'), indent=1)
    counts = {}
    for row in G:
        for c in row: counts[c] = counts.get(c, 0) + 1
    # ---- chart figure
    stw, sth = 1.25, 1.0
    fig = plt.figure(figsize=(7.0, 5.05), dpi=240)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    for j in range(NR):
        for c in range(NCOL):
            ax.add_patch(Rectangle((c * stw, j * sth), stw, sth, fc=G[j][c], ec='#3a3a3a', lw=0.4))
    for j, c in B:
        ax.plot((c + 0.5) * stw, (j + 0.5) * sth, 'o', ms=7.5, mfc='#1d1d24', mec='white', mew=1.0)
    for j in range(NR):
        ax.text(-0.35, (j + 0.5) * sth, str(j + 1), ha='right', va='center', fontsize=6.5)
        ax.text(NCOL * stw + 0.35, (j + 0.5) * sth, str(j + 1), ha='left', va='center', fontsize=6.5)
        if bias[j]:
            # decrease edge / increase edge marks, seen from the RS
            dec_left = bias[j] > 0
            ax.text(-2.6, (j + 0.5) * sth, 'dec' if dec_left else 'inc', ha='right', va='center', fontsize=5.8, color='#b00020')
            ax.text(NCOL * stw + 2.6, (j + 0.5) * sth, 'inc' if dec_left else 'dec', ha='left', va='center', fontsize=5.8, color='#b00020')
    for c in range(NCOL):
        ax.text((c + 0.5) * stw, -0.55, str(c + 1), ha='center', va='top', fontsize=5.2)
    for k, L in enumerate(SEQ[:5]):
        ax.text(-5.4, (k * RW + 0.5) * sth, f'{L} {ltype(k)}', ha='right', va='center', fontsize=8, weight='bold',
                color=GOLD_D if ltype(k) == 'c' else BLUE_D)
    ax.set_xlim(-8.2, NCOL * stw + 5.2); ax.set_ylim(-1.6, NR * sth + 0.3); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(os.path.join(SW, 'fig/chart.png')); plt.close(fig)
    # ---- slice figure: one period, same 24-stitch window (true lateral position of fabric column 1 in row 1 = -PH)
    S0, S1 = -PH * REP // (3 * K), NCOL * REP // (3 * K) - PH * REP // (3 * K)
    hv = build(S0, S1, ngap=4)
    W, Ht = (S1 - S0) * SQ3_6, 4 * H
    fig = plt.figure(figsize=(4.0, 4.0 * (Ht + 0.5) / (W + 0.7)), dpi=220)
    ax = fig.add_axes([0.0, 0.0, 1, 1])
    tr = lambda v: ((float(v[0]) - S0) * SQ3_6, float(v[1]) * H)
    for h in hv:
        ax.add_patch(MPoly([tr(v) for v in h['poly']], closed=True, fc=colour(h), ec=EDGE, lw=1.1, joinstyle='miter'))
    for k in range(4):
        ax.plot([0, W], [(k + 0.5) * H] * 2, ls=(0, (3, 3)), lw=0.5, color='#555')
    for k, L in enumerate(SEQ[:5]):
        for r in range(-1, 3):
            s = SOFF[L] + r * REP
            if S0 <= s <= S1:
                ax.plot((s - S0) * SQ3_6, k * H, 'o', ms=4.5, mfc='#1d1d24', mec='white', mew=0.7, zorder=5)
        ax.text(-0.06, k * H, L, ha='right', va='center', fontsize=8, weight='bold')
        ax.text(W + 0.06, k * H, ltype(k), ha='left', va='center', fontsize=8, weight='bold', color=GOLD_D if ltype(k) == 'c' else BLUE_D)
    ax.set_xlim(-0.3, W + 0.3); ax.set_ylim(-0.12, Ht + 0.12); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(os.path.join(SW, 'fig/slice.png')); plt.close(fig)
    # ---- html
    def rowtxt(r):
        seq = ', '.join(f'{n} {ABBR_NAME[a]}' for n, a in r['runs'])
        return seq
    ABBR_NAME = {'DG': 'DG', 'LG': 'LG', 'DB': 'DB', 'LB': 'LB'}
    trs = []
    for r in rows:
        if r['bias'] == 0:
            how = ''
        else:
            right = r['bias'] > 0
            if r['side'] == 'RS':
                how = ('k1, M1, … k2tog, k1' if right else 'k1, ssk, … M1, k1')
            else:
                how = ('p1, p2tog, … M1P, p1' if right else 'p1, M1P, … ssp, p1')
            how = ('<b>bias right</b>: ' if right else '<b>bias left</b>: ') + how
        mb = (f"MB at st {', '.join(str(c) for c in r['balls'])}" if r['balls'] else '')
        trs.append(f"<tr><td class=n>{r['row']}</td><td>{r['side']}</td><td>{rowtxt(r)}</td><td>{how}</td><td>{mb}</td></tr>")
    cnt = ' · '.join(f'<span class=sw style="background:{c}"></span> {ABBR[c]} {NAME[c]}: {counts[c]} sts' for c in (GOLD_D, GOLD_L, BLUE_D, BLUE_L))
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HexOct knitting: the 4H swatch</title>
<link rel="stylesheet" href="../paper.css">
<style>
body{{font-size:9.6pt}} h2{{margin:8pt 0 3pt}} p{{margin:3pt 0}}
.top{{display:grid;grid-template-columns:62% 36%;gap:2%;align-items:start}}
.top img{{width:100%;display:block}}
table{{border-collapse:collapse;font:7.9pt/1.25 "DejaVu Sans",sans-serif;width:100%}}
td,th{{border-bottom:1px solid #ddd;padding:0.55mm 1.2mm;text-align:left;vertical-align:top}} td.n{{text-align:right}}
span.sw{{display:inline-block;width:9pt;height:9pt;border:1px solid #333;vertical-align:-1pt}}
ul{{margin:2pt 0 2pt 14pt;padding:0}} li{{margin:1pt 0}}
</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>HexOct knitting: the 4H swatch</h1>
<p class="sub">One period of the stacking A B C B A, 24 stitches by 29 rows</p>
<div class="meta"><b>DICTO</b> · knitting swatch of 31 October 2026<br>
The idea is DICTO's: the knitted fabric is an exact edge-on slice through a stacking of balls, coloured by the pieces
between the balls. Chart computed exactly with Claude (Anthropic).</div>
<p><b>What the swatch tests:</b> whether the bias rows place the fabric where the chart assumes (each band of colour
sits one third of a repeat further over, to the right going up from A to C, back to the left from C to A), and how the
four colours read at this size.</p>
<div class="top">
<figure><img src="fig/chart.png" alt="Swatch chart"><figcaption><b>Chart.</b> Seen from the right side, row 1 at the
bottom; RS rows read right to left, WS rows left to right. Dots = bobbles (ball stitches). <i>dec</i>/<i>inc</i> at the
sides of a row: which edge gets the decrease and which the increase.</figcaption></figure>
<div><figure><img src="fig/slice.png" alt="Exact slice"><figcaption><b>What you are making.</b> The exact slice through
the stacked balls (dots = ball centres, letters = layers). Gold bands belong to the c layers (B), blue to the h layers
(A, C); dark = tetrahedral pieces, light = octahedral pieces. Knitted, the bias rows give the sideways steps.</figcaption></figure>
<h2>Colours (4)</h2><p>{cnt}</p>
<p>Total {NCOL * NR} stitches. Any yarn of one weight; four shades with clear contrast between gold and blue and between dark and light.</p></div>
</div>
<h2>1. Cast on and edges</h2>
<ul>
<li>Cast on <b>24 stitches</b> in DB (long-tail). Row 1 is the first row after the cast-on, a right-side (RS) row.</li>
<li>Stockinette throughout. Stitch 1 and stitch 24 are edge stitches: knit them (RS) and purl them (WS) in the colour of
the chart; do not slip them, so the edges show the bias steps.</li>
<li>Colour changes: intarsia with small bobbins, twisting the yarns at every change; carry a colour along the back only
where its next block is 1–2 stitches away.</li>
<li>Every bias row keeps <b>24 stitches</b>: one decrease at one edge and one increase at the other, each worked one
stitch in from the edge. <i>Bias right</i> (rows 3, 4, 6, 7, 10, 11, 13, 14): decrease at the left edge, increase at the
right edge (as seen from the RS), so the row sits one stitch further right. <i>Bias left</i> (rows 17, 18, 20, 21, 24,
25, 27, 28): decrease at the right edge, increase at the left.</li>
<li>In the colour runs below, the increased and decreased stitches are already counted as they finish (24 stitches per
row); work each in the colour of its run.</li>
<li>After row 29, bind off loosely in DB on the WS.</li>
</ul>
<h2>2. Bobble (MB)</h2>
<p>In the colour of the stitch: (k1, yo, k1) into the stitch, turn, p3, turn, k3, turn, p3, turn, sl1-k2tog-psso.
Rows 1, 15 and 29 are RS rows. Rows 8 and 22 are WS rows: work the bobble the same way with knit and purl exchanged
((p1, yo, p1) into the stitch, turn, k3, turn, p3, turn, k3, turn, p3tog) and push it to the RS; if it sits badly,
purl these two stitches plain and sew a bobble or French knot there afterwards.</p>
<h2>3. Row by row</h2>
<p>DG dark gold, LG light gold, DB dark blue, LB light blue. Runs in working order (RS from stitch 24 to stitch 1, WS from
stitch 1 to stitch 24); stitch numbers as on the chart.</p>
<table><tr><th class=n>Row</th><th>Side</th><th>Colour runs</th><th>Bias (edge stitches)</th><th>Bobble</th></tr>
{chr(10).join(trs)}
</table>
<p style="font-size:8.4pt;color:#444;margin-top:5pt">Gauge of the design: 12 stitches per repeat, 7 rows per layer of balls,
stitches about 5 wide to 4 tall (e.g. 22 stitches and 28 rows to 10 cm). Note your own gauge on the swatch; the true
proportions need stitch width : row height ≈ 1.24.</p>
</body></html>'''
    open(os.path.join(SW, 'paper.html'), 'w').write(html)
    print('counts', {NAME[c]: n for c, n in counts.items()}, 'balls', [(j + 1, c + 1) for j, c in B])
    for r in rows: print(r['row'], r['side'], r['bias'], r['runs'], r['balls'])


if __name__ == '__main__':
    main()
