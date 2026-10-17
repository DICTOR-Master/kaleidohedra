# DICTO 2026-10-18 bcc golden kit, step 4 drawing: two facing five-fold envelope stars (third neighbours) down the axis -> renders/step4-stars.html
import json, os
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'step4-stars.json'))); c = d['checks']
pts_all = [p for P in d['star1'] + d['star2'] for p in P]
x0, x1 = min(p[0] for p in pts_all) - 0.08, max(p[0] for p in pts_all) + 0.08; y0, y1 = min(p[1] for p in pts_all) - 0.08, max(p[1] for p in pts_all) + 0.08
W = 720; s = W / (x1 - x0); Hh = round((y1 - y0) * s)
T = lambda p: ((p[0] - x0) * s, (y1 - p[1]) * s); pts = lambda P: ' '.join('%.2f,%.2f' % T(p) for p in P)
g = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Two facing five-fold stars of golden envelopes">']
g += [f'<polygon points="{pts(P)}" class="k1"/>' for P in d['star1']] + [f'<polygon points="{pts(P)}" class="k2"/>' for P in d['star2']]
X1, Y1 = T((0, 0)); X2, Y2 = T(d['c2'])
g += [f'<line x1="{X1:.1f}" y1="{Y1:.1f}" x2="{X2:.1f}" y2="{Y2:.1f}" class="off"/>', f'<circle cx="{X1:.1f}" cy="{Y1:.1f}" r="5" class="p1"/>', f'<circle cx="{X2:.1f}" cy="{Y2:.1f}" r="5" class="p2"/>',
      f'<text x="{X1+8:.1f}" y="{Y1+18:.1f}" class="lbl">corner 1</text>', f'<text x="{X2+8:.1f}" y="{Y2-10:.1f}" class="lbl">corner 2</text>', '</svg>']
svg = '\n'.join(g)
html = f'''<title>Envelope Stars in bcc</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: one drawing sheet, then exact facts */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--s1:#d9a21b;--s2:#2f7fd8;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:16px}} h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:72ch}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:8px}} svg{{width:100%;height:auto;display:block}} figcaption{{font-size:.85rem;color:var(--muted)}}
.k1{{fill:var(--s1);fill-opacity:.5;stroke:var(--fg);stroke-width:.8}} .k2{{fill:var(--s2);fill-opacity:.4;stroke:var(--fg);stroke-width:.8}} .off{{stroke:var(--fg);stroke-width:1.5;stroke-dasharray:4 3}}
.p1{{fill:var(--s1);stroke:var(--fg)}} .p2{{fill:var(--s2);stroke:var(--fg)}} .lbl{{fill:var(--fg);font:13px var(--f-ui)}}
ul{{margin:0;padding-left:1.2em;max-width:72ch}} .num{{font-family:var(--f-num)}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>Facing five-fold stars of the golden envelopes (bcc)</h1>
<p class="sub">Down one five-fold axis. Gold: the five golden rhombi round a five-fold corner of one envelope (RT). Blue: the facing star of the envelope at a third neighbour, pointing back. Both stars lie in G′, the golden gap.</p>
<figure>{svg}<figcaption>Corner 2 is <span class="num">{c['offset_along']:.4f}</span> nearer along the axis and <span class="num">{c['offset_sideways']:.4f}</span> sideways.</figcaption></figure>
<ul>
<li>Exact: the sideways offset runs <b>along one of corner 1's spokes</b> (and opposite one of its tips).</li>
<li>Exact: its length is <b>2/3 of the tip radius</b>, or 2φ/3 × the spoke (just 8% past the spoke's end).</li>
<li>Exact search: it is <b>not</b> φ-scaled spoke or tip vectors, singly or in pairs, so no thick Penrose rhombus joins the two corners the way it did in the octet. The factor 2/3 (the bcc lattice's thirds) is what breaks it.</li>
<li>The stars are far apart here (gap <span class="num">{(c['offset_along']**2 + c['offset_sideways']**2) ** .5:.4f}</span>, against 0.363 in the octet), so a link would be a longer bridge through G′.</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-bcc-golden-kit step 4</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'step4-stars.html'), 'w').write(html); print('ok')
