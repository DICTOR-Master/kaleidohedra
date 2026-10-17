# DICTO 2026-10-18 bcc golden kit, step 2 drawing: the slab face tiled by golden pieces, and the two layers side-on -> renders/step2-slab.html
import json, os
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'step2-slab.json'))); D = d['draw']
xs = [p[0] for t in D['tiles'] for p in t['p']]; ys = [p[1] for t in D['tiles'] for p in t['p']]
pad = 0.03; x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad; W = 640; s = W / (x1 - x0); Hh = round((y1 - y0) * s)
T = lambda p: ((p[0] - x0) * s, (y1 - p[1]) * s); pts = lambda P: ' '.join('%.2f,%.2f' % T(p) for p in P)
cls = {'rhombus e': 'ra', 'rhombus e/phi': 'rb', 'parallelogram e x e/phi': 'pc'}
g = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Slab face tiled by golden rhombi and parallelograms">']
g += [f'<polygon points="{pts(t["p"])}" class="{cls[t["kind"]]}"/>' for t in D['tiles']]
g.append('</svg>'); face_svg = '\n'.join(g)
def side_svg(sd):
    a, b = sd['face']; h = sd['h']; sh = sd['shift']; gp = 2 * h
    X0, X1, Y0, Y1 = a - 0.12, b + 0.12, -0.03, gp + 0.03; Wd = 560; sc = Wd / (X1 - X0); Hd = round((Y1 - Y0) * sc)
    Tt = lambda p: ((p[0] - X0) * sc, (Y1 - p[1]) * sc); P = lambda Q: ' '.join('%.2f,%.2f' % Tt(p) for p in Q)
    o = [f'<svg viewBox="0 0 {Wd} {Hd}" role="img" aria-label="Two layers in the slab, side view">']
    o.append(f'<polygon points="{P([(a, 0), (b, 0), (b, gp), (a, gp)])}" class="slab"/>')
    o.append(f'<polygon points="{P([(a, 0), (b, 0), (b + sh, h), (a + sh, h)])}" class="l1"/>')
    o.append(f'<polygon points="{P([(a + sh, h), (b + sh, h), (b, gp), (a, gp)])}" class="l2"/>')
    o.append(f'<polygon points="{P([(b, 0), (b + sh, h), (b, gp)])}" class="spill"/>')
    o.append(f'<polygon points="{P([(a, 0), (a + sh, h), (a, gp)])}" class="hole"/>')
    for yy, lab in ((0, 'own RT face'), (gp, "neighbour's RT face")):
        X, Y = Tt((a, yy)); o.append(f'<line x1="{Tt((X0,yy))[0]:.1f}" y1="{Y:.1f}" x2="{Tt((X1,yy))[0]:.1f}" y2="{Y:.1f}" class="face"/><text x="{Tt((a,yy))[0]+4:.1f}" y="{Y + (14 if yy == 0 else -5):.1f}" class="lbl">{lab}</text>')
    o.append('</svg>'); return '\n'.join(o)
sides = ''.join(f'<figure>{side_svg(sd)}<figcaption><b>Third edge {sd["L"]}</b> (on the e×e tiles: {sd["piece_on_e_tiles"]}): each layer leans sideways by <span class="num">{sd["shift"]:.4f}</span>; the second leans back, so the stack ends exactly on the neighbour\'s face. Red: spill past the slab\'s side into the wedge; hatched white: the matching hollow left inside the slab.</figcaption></figure>' for sd in D['sides'])
c = d['tiling_counts']
html = f'''<title>Golden Slab Cover</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: face tiling and side views in a wrapping row, facts below */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--ra:#d9a21b;--rb:#5b8fd0;--pc:#3f9a5b;--l1:#7fcf9c;--l2:#2e9e5b;--spill:#c8382f;--slab:#eef1f5;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--l1:#3f8a5e;--slab:#1f2a36;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--l1:#3f8a5e;--slab:#1f2a36;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:72ch}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}} .col{{display:flex;flex-direction:column;gap:16px;min-width:0}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:8px;min-width:0}}
svg{{width:100%;height:auto;display:block}} figcaption{{font-size:.85rem;color:var(--muted)}}
.ra{{fill:var(--ra);stroke:var(--fg);stroke-width:.8}} .rb{{fill:var(--rb);stroke:var(--fg);stroke-width:.8}} .pc{{fill:var(--pc);fill-opacity:.8;stroke:var(--fg);stroke-width:.8}}
.slab{{fill:var(--slab);stroke:var(--line)}} .l1{{fill:var(--l1);stroke:var(--fg);stroke-width:.8}} .l2{{fill:var(--l2);stroke:var(--fg);stroke-width:.8}}
.spill{{fill:var(--spill);fill-opacity:.85}} .hole{{fill:var(--sheet);stroke:var(--spill);stroke-dasharray:4 3}}
.face{{stroke:var(--fg);stroke-width:1.5}} .lbl{{fill:var(--fg);font:12px var(--f-ui)}}
ul{{margin:0;padding-left:1.2em;max-width:72ch}} .num{{font-family:var(--f-num)}} .tag{{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>Covering a slab of the golden gap</h1>
<p class="sub">OCDs joined hexagon to hexagon on the bcc lattice, each in its golden envelope (RT). Between second neighbours the gap is a flat slab over one RT face (a golden rhombus, 63.43°), <span class="num">{d["gap"]:.4f}</span> thick. <span class="tag">Picture first, for DICTO</span></p>
<div class="row">
<figure>{face_svg}<figcaption><b>The face, tiled.</b> Its edge is exactly 3φ·e = 3e + 3e/φ (e = edge of the λ/φ rhombohedron, {d["e"]:.4f}). Cutting each edge into three e and three e/φ: <b>{c.get("rhombus e", 0)} golden rhombi e×e</b> (gold), <b>{c.get("rhombus e/phi", 0)} golden rhombi e/φ×e/φ</b> (blue), <b>{c.get("parallelogram e x e/phi", 0)} golden parallelograms e×e/φ</b> (green). Area checked exactly.</figcaption></figure>
<div class="col">{sides}</div>
</div>
<ul>
<li>Each tile becomes a piece by pushing it along a third five-fold axis: rhombohedra on the rhombi, golden bricks (parallelepipeds with edges e and e/φ along five-fold axes) on the rest.</li>
<li>Exact: four choices of that third edge give a layer exactly <b>half the slab</b> (<span class="num">{d["draw"]["layer_h"]:.5f}</span>): two of length e, two of length e/φ.</li>
<li>Exact: in each length the two choices lean opposite ways, so <b>two layers, one leaning each way, end exactly on the neighbour's face</b>. Between them they spill a little past the slab's sides into the wedges (red), leaving an equal hollow on the other side (hatched).</li>
<li>Open: whether the spills and hollows of neighbouring slabs and wedges can meet up; that is the next step.</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-bcc-golden-kit step 2</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'step2-slab.html'), 'w').write(html); print('ok')
