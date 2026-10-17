# DICTO 2026-10-18 octet study, step 13 drawing: the Penrose-rhombus cut between the two facing stars -> renders/step13-penrose.html
import json, os
H = os.path.dirname(os.path.abspath(__file__)); D = lambda n: json.load(open(os.path.join(H, '..', 'data', n)))
st = D('step4-stars.json'); pe = D('step13-penrose.json'); c = pe['checks']
x0, x1, y0, y1 = -0.62, 0.42, -0.5, 0.5; W = 720; s = W / (x1 - x0); Hh = round((y1 - y0) * s)
T = lambda p: ((p[0] - x0) * s, (y1 - p[1]) * s); pts = lambda P: ' '.join('%.2f,%.2f' % T(p) for p in P)
g = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Penrose rhombi between two facing five-fold stars">']
for P in st['kites1']: g.append(f'<polygon points="{pts(P)}" class="k1"/>')
for P in st['kites2']: g.append(f'<polygon points="{pts(P)}" class="k2"/>')
g.append(f'<polygon points="{pts(pe["patch"]["central"])}" class="pc"/>')
for k in ('flank1', 'flank2'):
    if k in pe['patch']: g.append(f'<polygon points="{pts(pe["patch"][k])}" class="pf"/>')
for p, lab, dx, dy, an in ((st['c1'], 'c1', 10, 18, 'start'), (st['c2'], 'c2', -10, 18, 'end')):
    X, Y = T(p); g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="5" class="pt"/><text x="{X+dx:.1f}" y="{Y+dy:.1f}" class="lbl" text-anchor="{an}">{lab}</text>')
cx, cy = T([sum(p[0] for p in pe['patch']['central']) / 4, sum(p[1] for p in pe['patch']['central']) / 4])
g.append(f'<text x="{cx:.1f}" y="{cy+4:.1f}" class="lbl b" text-anchor="middle">72°</text>')
g.append('</svg>'); svg = '\n'.join(g)
html = f'''<title>Penrose Cut Between Stars</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: one drawing sheet, then exact facts and the open question */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--s1:#d9a21b;--s2:#2f7fd8;--pc:#c8382f;--pf:#7a3fa0;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--pc:#e0564c;--pf:#b07ad6;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--pc:#e0564c;--pf:#b07ad6;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:72ch}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:8px}}
svg{{width:100%;height:auto;display:block}} figcaption{{font-size:.85rem;color:var(--muted)}}
.k1{{fill:var(--s1);fill-opacity:.45;stroke:var(--fg);stroke-width:.8}} .k2{{fill:var(--s2);fill-opacity:.35;stroke:var(--fg);stroke-width:.8}}
.pc{{fill:var(--pc);fill-opacity:.75;stroke:var(--fg);stroke-width:2}} .pf{{fill:var(--pf);fill-opacity:.7;stroke:var(--fg);stroke-width:2}}
.pt{{fill:var(--fg)}} .lbl{{fill:var(--fg);font:13px var(--f-ui)}} .lbl.b{{font-weight:600;fill:var(--sheet)}}
ul{{margin:0;padding-left:1.2em;max-width:72ch}} .num{{font-family:var(--f-num)}} .tag{{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>A Penrose cut between the two facing stars</h1>
<p class="sub">Looking down the five-fold axis, as in step 4. Gold and blue: the two facing five-kite stars. Red: one thick Penrose rhombus from corner c1 to corner c2. Purple: two smaller thick Penrose rhombi, each reaching one tip of each star. <span class="tag">Proposal by Claude, for DICTO</span></p>
<figure>{svg}<figcaption>Each rhombus would become a Penrose prism: run along the five-fold axis, closed above and below by the two OCD surfaces.</figcaption></figure>
<ul>
<li>Exact: the line c1 → c2 is the long diagonal of a <b>thick Penrose rhombus</b> (72° at c1 and c2, 108° at the sides), edge <span class="num">{c['edge_central']:.4f}</span> = tip radius ÷ φ.</li>
<li>Exact: its four edges run <b>along the stars' own spokes</b>, towards a gold tip from c1 and a blue tip from c2.</li>
<li>Exact: at each side corner a <b>thick Penrose rhombus one φ-step smaller</b> (edge <span class="num">{c['edge_flank']:.4f}</span>, 108° at the side corner) reaches one gold tip and one blue tip.</li>
<li>So three Penrose rhombi in φ-scaled sizes join the two stars, tip to tip, symmetric about the middle point.</li>
<li>Open: in 3D, do these prisms fit inside the middle region (between the OCDs, clear of the keys)? To check next, after your read.</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-ocd-octet step 13</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'step13-penrose.html'), 'w').write(html); print('ok')
