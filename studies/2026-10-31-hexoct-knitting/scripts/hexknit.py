#!/usr/bin/env python3
"""hexknit: knitting chart of any close-packed stacking, from the exact HexOct slice (DICTO's idea, 31 Oct 2026).

Input: a stacking as a c/h word (repeated) or as an A/B/C word (repeated), and the number of layers.
Output (in <outdir>/<name>/): slice.png (exact slice), chart.png (swatch chart), rows.json, rows.md, section.html
(a swatch section for a paper) and paper.html (a stand-alone swatch sheet, printable with papers/print.mjs).

Conventions (same as the 4H swatch): slice plane x = 0 ({11-20}); repeat 12 stitches, 7 rows per layer, stitch 5:4;
4 bias rows per gap (gap rows 2, 3, 5, 6), bias right = decrease at the left edge, increase at the right (seen from the
RS); colours by Rule-of-Halves piece halves: c layer gold, h layer blue, tetrahedral dark, octahedral light; each cell
takes the colour covering most of it (4 x 4 samples), exact ties go to the dark shade; ball stitches = bobbles; the
24-stitch window starts half a repeat after a ball so the bobbles sit at stitches 7 and 19.

Usage (dicto-big-brother):
  ~/geom/bin/python hexknit.py --ch hchc --layers 9 --name 4H
  ~/geom/bin/python hexknit.py --abc ABC --layers 7 --name 3C
  ~/geom/bin/python hexknit.py --ch chcchchcchcch --layers 13 --name Fibonacci
Options: --outdir DIR (default ../gen), --stitches N (multiple of 12, default 24).
"""
import os, sys, json, argparse
import knit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
THIRD = {frozenset('AB'): 'C', frozenset('BC'): 'A', frozenset('AC'): 'B'}
ABBR = {knit.GOLD_D: 'DG', knit.GOLD_L: 'LG', knit.BLUE_D: 'DB', knit.BLUE_L: 'LB'}
NAME = {'DG': 'dark gold', 'LG': 'light gold', 'DB': 'dark blue', 'LB': 'light blue'}
HEX = {v: k for k, v in ABBR.items()}
PH = 6


def from_ch(word, n):
    t = [word[k % len(word)] for k in range(n)]
    seq = ['A', 'B']
    for k in range(1, n - 1):
        seq.append(seq[k - 1] if t[k] == 'h' else THIRD[frozenset(seq[k - 1] + seq[k])])
    return ''.join(seq[:n]), ''.join(t)


def from_abc(word, n):
    p = len(word)
    seq = ''.join(word[k % p] for k in range(n))
    t = ''.join('h' if word[(k - 1) % p] == word[(k + 1) % p] else 'c' for k in range(n))
    return seq, t


def runs(cells):
    out = []
    for c in cells:
        if out and out[-1][1] == c: out[-1][0] += 1
        else: out.append([1, c])
    return out


def make(seq, types, name, outdir, nst=24):
    knit.configure(seq, types)
    knit.NCOL = nst
    knit.NREP = nst // 12
    od = os.path.join(outdir, name); os.makedirs(od, exist_ok=True)
    NL = len(seq); NR = knit.RW * (NL - 1) + 1; NC = nst
    halves = knit.build()
    grid, balls, S, bias, ties = knit.chart(halves)
    G = [[grid[j][(c - PH) % NC] for c in range(NC)] for j in range(NR)]
    B = sorted({(j, (c + PH) % NC) for j, c in balls})
    assert {c for j, c in B} == set(range(PH, NC, 12)) and len(B) == NL * NC // 12
    rows = []
    for j in range(NR):
        rs = j % 2 == 0
        order = range(NC - 1, -1, -1) if rs else range(NC)
        rows.append(dict(row=j + 1, side='RS' if rs else 'WS', runs=[(n, ABBR[c]) for n, c in runs([G[j][c] for c in order])],
                         bias=bias[j], shift=S[j], bobbles=[c + 1 for jj, c in B if jj == j]))
    counts = {}
    for r in G:
        for c in r: counts[ABBR[c]] = counts.get(ABBR[c], 0) + 1
    info = dict(name=name, layers=seq, types=types, rows=NR, stitches=NC, ties=ties, counts=counts,
                hexagonality=f"{types[1:-1].count('h')}/{NL - 2} inner layers h", final_shift=S[-1])
    json.dump(dict(info=info, rows=rows), open(os.path.join(od, 'rows.json'), 'w'), indent=1)
    # chart
    stw, sth = 1.25, 1.0
    W = NC * stw + 13.4; H = NR * sth + 1.9
    fig = plt.figure(figsize=(7.0, 7.0 * H / W), dpi=240)
    ax = fig.add_axes([0, 0, 1, 1])
    for j in range(NR):
        for c in range(NC):
            ax.add_patch(Rectangle((c * stw, j * sth), stw, sth, fc=G[j][c], ec='#3a3a3a', lw=0.4))
    for j, c in B:
        ax.plot((c + 0.5) * stw, (j + 0.5) * sth, 'o', ms=7.5, mfc='#1d1d24', mec='white', mew=1.0)
    for j in range(NR):
        ax.text(-0.35, (j + 0.5) * sth, str(j + 1), ha='right', va='center', fontsize=6.5)
        ax.text(NC * stw + 0.35, (j + 0.5) * sth, str(j + 1), ha='left', va='center', fontsize=6.5)
        if bias[j]:
            dl = bias[j] > 0
            ax.text(-2.6, (j + 0.5) * sth, 'dec' if dl else 'inc', ha='right', va='center', fontsize=5.8, color='#b00020')
            ax.text(NC * stw + 2.6, (j + 0.5) * sth, 'inc' if dl else 'dec', ha='left', va='center', fontsize=5.8, color='#b00020')
    for c in range(NC):
        ax.text((c + 0.5) * stw, -0.55, str(c + 1), ha='center', va='top', fontsize=5.2)
    for k, L in enumerate(seq):
        ax.text(-5.4, (k * knit.RW + 0.5) * sth, f'{L} {types[k]}', ha='right', va='center', fontsize=8, weight='bold',
                color=knit.GOLD_D if types[k] == 'c' else knit.BLUE_D)
    ax.set_xlim(-8.2, NC * stw + 5.2); ax.set_ylim(-1.6, NR * sth + 0.3); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(os.path.join(od, 'chart.png')); plt.close(fig)
    # slice (same window as the chart's row 1)
    S0 = -PH // 2; S1 = S0 + NC // 2
    hv = knit.build(S0, S1)
    Wt, Ht = (S1 - S0) * knit.SQ3_6, (NL - 1) * knit.H
    fig = plt.figure(figsize=(4.0, 4.0 * (Ht + 0.3) / (Wt + 0.7)), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1])
    tr = lambda v: ((float(v[0]) - S0) * knit.SQ3_6, float(v[1]) * knit.H)
    for h in hv:
        ax.add_patch(MPoly([tr(v) for v in h['poly']], closed=True, fc=knit.colour(h), ec=knit.EDGE, lw=1.1, joinstyle='miter'))
    for k in range(NL - 1):
        ax.plot([0, Wt], [(k + 0.5) * knit.H] * 2, ls=(0, (3, 3)), lw=0.5, color='#555')
    for k, L in enumerate(seq):
        for r in range(-2, 4):
            s = knit.SOFF[L] + r * knit.REP
            if S0 <= s <= S1:
                ax.plot((s - S0) * knit.SQ3_6, k * knit.H, 'o', ms=4.5, mfc='#1d1d24', mec='white', mew=0.7, zorder=5)
        ax.text(-0.06, k * knit.H, L, ha='right', va='center', fontsize=8, weight='bold')
        ax.text(Wt + 0.06, k * knit.H, types[k], ha='left', va='center', fontsize=8, weight='bold',
                color=knit.GOLD_D if types[k] == 'c' else knit.BLUE_D)
    ax.set_xlim(-0.3, Wt + 0.3); ax.set_ylim(-0.12, Ht + 0.12); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(os.path.join(od, 'slice.png')); plt.close(fig)
    # rows.md
    with open(os.path.join(od, 'rows.md'), 'w') as f:
        f.write(f'# {name}: {seq} ({types}), {NC} stitches x {NR} rows\n\n| Row | Side | Colour runs | Bias | Bobbles |\n|---|---|---|---|---|\n')
        for r in rows:
            f.write(f"| {r['row']} | {r['side']} | {', '.join(f'{n} {a}' for n, a in r['runs'])} | "
                    f"{'right' if r['bias'] > 0 else 'left' if r['bias'] < 0 else ''} | {', '.join(map(str, r['bobbles']))} |\n")
    write_html(od, info, rows, B)
    print(name, seq, types, f'{NC} sts x {NR} rows', counts, 'ties', ties, 'final shift', S[-1])
    return info


def section_html(info, rows, imgpre='', h='h2', sec=''):
    name, seq, types, NR, NC = info['name'], info['layers'], info['types'], info['rows'], info['stitches']
    br = [r['row'] for r in rows if r['bias'] > 0]; bl = [r['row'] for r in rows if r['bias'] < 0]
    bob = [r for r in rows if r['bobbles']]
    bob_rs = [r['row'] for r in bob if r['side'] == 'RS']; bob_ws = [r['row'] for r in bob if r['side'] == 'WS']
    c0 = rows[0]['runs'][0][1]; cl = rows[-1]['runs'][0][1]
    trs = []
    for r in rows:
        how = ''
        if r['bias']:
            right = r['bias'] > 0
            how = ('k1, M1, … k2tog, k1' if right else 'k1, ssk, … M1, k1') if r['side'] == 'RS' else \
                  ('p1, p2tog, … M1P, p1' if right else 'p1, M1P, … ssp, p1')
            how = ('<b>bias right</b>: ' if right else '<b>bias left</b>: ') + how
        mb = ('MB at st ' + ', '.join(map(str, r['bobbles']))) if r['bobbles'] else ''
        trs.append(f"<tr><td class=n>{r['row']}</td><td>{r['side']}</td><td>{', '.join(f'{n} {a}' for n, a in r['runs'])}</td><td>{how}</td><td>{mb}</td></tr>")
    cnt = ' · '.join(f'<span class=sw style="background:{HEX[a]}"></span> {a} {NAME[a]}: {info["counts"].get(a, 0)} sts'
                     for a in ('DG', 'LG', 'DB', 'LB') if info['counts'].get(a, 0))
    lst = lambda v: ', '.join(map(str, v)) if v else 'none'
    return f'''<{h}>{sec}{name}: {seq} ({types}), {NC} stitches × {NR} rows</{h}>
<div class="top">
<figure><img src="{imgpre}chart.png" alt="{name} chart"><figcaption><b>Chart.</b> Seen from the RS, row 1 at the bottom;
RS rows read right to left, WS rows left to right. Dots = bobbles. <i>dec</i>/<i>inc</i>: which edge of a bias row gets
the decrease and which the increase.</figcaption></figure>
<div><figure><img src="{imgpre}slice.png" alt="{name} exact slice"><figcaption><b>The exact slice</b> for this window
(dots = ball centres; letters = layers; c gold, h blue; dark = tetrahedral, light = octahedral pieces).</figcaption></figure>
<p class=small>{cnt}. Total {NC * NR} stitches.</p></div></div>
<p class=small><b>Cast on</b> {NC} sts in {c0}; row 1 is a RS row. <b>Bias right</b> (decrease at the left edge, increase
at the right, seen from the RS): rows {lst(br)}. <b>Bias left</b>: rows {lst(bl)}. Net shift at the top: {info["final_shift"]:+d}
stitches. <b>Bobbles</b> on RS rows {lst(bob_rs)}; on WS rows {lst(bob_ws)}. Bind off in {cl} on the WS after row {NR}.</p>
<table class=rows><tr><th class=n>Row</th><th>Side</th><th>Colour runs (working order)</th><th>Bias (edge stitches)</th><th>Bobble</th></tr>
{chr(10).join(trs)}
</table>'''


CSS = '''body{font-size:9.6pt} h2{margin:8pt 0 3pt} p{margin:3pt 0}
.top{display:grid;grid-template-columns:62% 36%;gap:2%;align-items:start}
.top img{width:100%;display:block}
table.rows{border-collapse:collapse;font:7.9pt/1.25 "DejaVu Sans",sans-serif;width:100%}
table.rows td,table.rows th{border-bottom:1px solid #ddd;padding:0.55mm 1.2mm;text-align:left;vertical-align:top} table.rows td.n{text-align:right}
span.sw{display:inline-block;width:9pt;height:9pt;border:1px solid #333;vertical-align:-1pt}
p.small{font-size:8.8pt} ul{margin:2pt 0 2pt 14pt;padding:0} li{margin:1pt 0}'''

COMMON = '''<h2>How to knit every swatch</h2>
<ul>
<li>Stockinette. Stitches 1 and the last are edge stitches, worked in the chart colour, not slipped, so the edges show the
bias steps.</li>
<li>Colour changes: intarsia with small bobbins, twisting at every change; carry a colour along the back only where its next
block is 1–2 stitches away.</li>
<li>Every bias row keeps the stitch count: one decrease and one increase, each one stitch in from its edge. In the colour
runs the increased and decreased stitches are counted as they finish; work each in the colour of its run.</li>
<li>Bobble (MB), in the colour of the stitch. RS rows: (k1, yo, k1) into the stitch, turn, p3, turn, k3, turn, p3, turn,
sl1-k2tog-psso. WS rows: (p1, yo, p1) into the stitch, turn, k3, turn, p3, turn, k3, turn, p3tog, and push it to the RS;
if it sits badly, purl the stitch plain and sew a bobble or French knot there afterwards.</li>
<li>Abbreviations: DG dark gold, LG light gold, DB dark blue, LB light blue. Runs are given in working order (RS from the
last stitch to stitch 1, WS from stitch 1 to the last).</li>
</ul>'''


def write_html(od, info, rows, B):
    name = info['name']
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HexOct knitting: the {name} swatch</title>
<link rel="stylesheet" href="../paper.css"><style>{CSS}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>HexOct knitting: the {name} swatch</h1>
<p class="sub">Stacking {info['layers']}, {info['stitches']} stitches by {info['rows']} rows</p>
<div class="meta"><b>DICTO</b> · knitting swatch of 31 October 2026<br>
The idea is DICTO's: the knitted fabric is an exact edge-on slice through a stacking of balls, coloured by the pieces
between the balls. Chart computed exactly with Claude (Anthropic), generator hexknit.</div>
{COMMON}
{section_html(info, rows, 'fig/')}
</body></html>'''
    open(os.path.join(od, 'paper.html'), 'w').write(html)
    open(os.path.join(od, 'section.html'), 'w').write(section_html(info, rows, f'fig/{name}/', 'h3'))


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--ch'); g.add_argument('--abc')
    ap.add_argument('--layers', type=int, required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--outdir', default=os.path.join(HERE, '../gen'))
    ap.add_argument('--stitches', type=int, default=24)
    a = ap.parse_args()
    seq, types = from_ch(a.ch, a.layers) if a.ch else from_abc(a.abc, a.layers)
    make(seq, types, a.name, a.outdir, a.stitches)


if __name__ == '__main__':
    main()
