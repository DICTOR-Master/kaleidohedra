# DICTO 2026-10-18 octet study, step 4 drawing: the two facing five-kite stars down the five-fold axis -> renders/step4-stars.html
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'step4-stars.json')))
x0, x1, y0, y1 = -0.62, 0.95, -0.62, 0.62; W = 720; s = W / (x1 - x0); Hh = round((y1 - y0) * s)
T = lambda p: ((p[0] - x0) * s, (y1 - p[1]) * s); pts = lambda P: ' '.join('%.2f,%.2f' % T(p) for p in P)
o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Two five-kite stars seen down the five-fold axis">']
for P in d['ring1']: o.append(f'<polygon points="{pts(P)}" class="ring r1"/>')
for P in d['ring2']: o.append(f'<polygon points="{pts(P)}" class="ring r2"/>')
for P in d['kites1']: o.append(f'<polygon points="{pts(P)}" class="k1"/>')
for P in d['kites2']: o.append(f'<polygon points="{pts(P)}" class="k2"/>')
r = d['checks']['star_radius']; cx, cy = T((0, 0))
o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*s:.1f}" class="circ"/>')
c2 = T(d['c2']); o.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{c2[0]:.1f}" y2="{c2[1]:.1f}" class="off"/>')
o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" class="p1"/><circle cx="{c2[0]:.1f}" cy="{c2[1]:.1f}" r="6" class="p2"/>')
o.append(f'<text x="{cx+10:.1f}" y="{cy+20:.1f}" class="lbl">corner 1</text><text x="{c2[0]-12:.1f}" y="{c2[1]+20:.1f}" class="lbl" text-anchor="end">corner 2 (neighbour), 0.094 nearer</text>')
mx = (cx + c2[0]) / 2; o.append(f'<text x="{mx:.1f}" y="{cy-10:.1f}" class="lbl small" text-anchor="middle">0.3505</text>')
o.append('</svg>'); svg = '\n'.join(o)
c = d['checks']
html = f'''<title>Facing Five-fold Stars</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: one drawing sheet, caption and facts below */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--s1:#d9a21b;--s2:#2f7fd8;--ring:#e9e4d4;--ring2:#dbe6f3;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--ring:#3a3524;--ring2:#22324a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--ring:#3a3524;--ring2:#22324a;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:70ch}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:8px}}
svg{{width:100%;height:auto;display:block}} figcaption{{font-size:.85rem;color:var(--muted)}}
.k1{{fill:var(--s1);fill-opacity:.75;stroke:var(--fg);stroke-width:1}} .k2{{fill:var(--s2);fill-opacity:.55;stroke:var(--fg);stroke-width:1}}
.ring.r1{{fill:var(--ring);stroke:var(--line)}} .ring.r2{{fill:var(--ring2);fill-opacity:.6;stroke:var(--line)}}
.circ{{fill:none;stroke:var(--muted);stroke-dasharray:5 4}} .off{{stroke:var(--fg);stroke-width:1.5;stroke-dasharray:3 3}}
.p1{{fill:var(--s1);stroke:var(--fg)}} .p2{{fill:var(--s2);stroke:var(--fg)}}
.lbl{{fill:var(--fg);font:13px var(--f-ui)}} .lbl.small{{font:12px var(--f-num)}}
ul{{margin:0;padding-left:1.2em;max-width:72ch}} .num{{font-family:var(--f-num)}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>Two facing five-fold stars in the OCD octet</h1>
<p class="sub">Looking straight down one five-fold axis. Gold: the five kites round a corner of one OCD. Blue: the five kites round the facing corner of the neighbouring OCD (across the shared octahedron edge), which points straight back. Pale: the next ring of faces of each.</p>
<figure>{svg}<figcaption>Dashed circle: the tips of the gold star (radius <span class="num">0.3505</span>). The blue star's centre lies exactly on that circle, but between two gold tips, in line with a gold inner corner (180°), not on a tip. It is <span class="num">0.094</span> nearer the viewer along the axis.</figcaption></figure>
<ul>
<li>Exact: the sideways offset between the two corners equals the star's tip radius (both <span class="num">{c['offset_sideways']:.6f}</span>).</li>
<li>Exact: the neighbour's corner is <b>not</b> over a gold tip (my earlier guess was wrong); it sits at 180°, where the gold star has an inner corner.</li>
<li>The two stars are turned 36° against each other: a half turn, which for a five-fold star is the same as 36°.</li>
<li>Gold star surface: inner corners 0.056 and tips 0.128 below its centre; the blue star slopes the other way.</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-ocd-octet step 4</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'step4-stars.html'), 'w').write(html); print('ok')
