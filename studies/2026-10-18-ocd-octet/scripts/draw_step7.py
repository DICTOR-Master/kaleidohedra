# DICTO 2026-10-18 octet study, step 7 drawing: the shared middle piece in the mirror plane x = 0 -> renders/step7-middle.html
import json, os
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'step7-middle.json'))); S = d['section_x0']; n = d['numbers']
x0, x1, y0, y1 = -0.45, 1.55, -0.45, 1.55; W = 640; s = W / (x1 - x0)
T = lambda p: ((p[0] - x0) * s, (y1 - p[1]) * s); pts = lambda P: ' '.join('%.2f,%.2f' % T(p) for p in P)
g = [f'<svg viewBox="0 0 {W} {W}" role="img" aria-label="Section x=0 through two OCDs and the middle piece">']
g += [f'<polygon points="{pts(S["octa1"])}" class="oct"/>', f'<polygon points="{pts(S["octa2"])}" class="oct"/>']
g += [f'<polygon points="{pts(S["hull"])}" class="mid"/>']
g += [f'<polygon points="{pts(S["ocd1"])}" class="ocd"/>', f'<polygon points="{pts(S["ocd2"])}" class="ocd"/>']
g += [f'<polygon points="{pts(S["octa1"])}" class="octl"/>', f'<polygon points="{pts(S["octa2"])}" class="octl"/>']
for k, cls in (('c1', 'c'), ('c2', 'c'), ('m', 'mpt')):
    X, Y = T(S[k]); g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="5" class="{cls}"/>')
lab = lambda p, t, dx=8, dy=-8, a='start': (lambda X, Y: f'<text x="{X+dx:.1f}" y="{Y+dy:.1f}" class="lbl" text-anchor="{a}">{t}</text>')(*T(p))
g += [lab(S['c1'], 'c1', -10, 18, 'end'), lab(S['c2'], 'c2', 10, -6), lab(S['m'], 'm', 10, 4), lab([0, 0], 'OCD 1', 0, 4, 'middle'), lab([1.0787, 1.0787], 'OCD 2', 0, 4, 'middle')]
g.append('</svg>'); svg = '\n'.join(g); w = n['where_samples']; tot = sum(w.values())
html = f'''<title>Shared Middle Piece</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: one drawing, then measured facts and the open question */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--ocd:#e3c45a;--oct:#e8eef5;--octl:#2b4a6f;--mid:#c8382f;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--ocd:#b8962f;--oct:#1f2a36;--octl:#9cc0ea;--mid:#e0564c;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--ocd:#b8962f;--oct:#1f2a36;--octl:#9cc0ea;--mid:#e0564c;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:70ch}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:8px}}
svg{{width:100%;height:auto;display:block}} figcaption{{font-size:.85rem;color:var(--muted)}}
.oct{{fill:var(--oct)}} .octl{{fill:none;stroke:var(--octl);stroke-width:1.5}} .ocd{{fill:var(--ocd);stroke:var(--fg);stroke-width:1}}
.mid{{fill:var(--mid);fill-opacity:.8;stroke:var(--fg);stroke-width:1}} .c{{fill:var(--fg)}} .mpt{{fill:var(--sheet);stroke:var(--fg);stroke-width:2}}
.lbl{{fill:var(--fg);font:13px var(--f-ui)}} ul{{margin:0;padding-left:1.2em;max-width:72ch}} .num{{font-family:var(--f-num)}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>Shared middle piece between two facing stars</h1>
<p class="sub">Cut through the mirror plane x = 0, which holds both facing five-fold corners (c1, c2), their axis and the octahedron edge the two OCDs share. Blue outlines: the two octahedra, touching along that edge. Gold: the OCDs. Red: the candidate middle piece, the hull of the two five-kite stars minus the OCDs. Floating-point first look.</p>
<figure>{svg}<figcaption>m, the midpoint of the shared edge, is the centre: the red piece is the same seen from either OCD (inversion through m, checked).</figcaption></figure>
<ul>
<li>Middle piece volume ≈ <span class="num">{n["middle_piece_volume"]:.4f}</span> (hull of the stars <span class="num">{n["hull_volume"]:.4f}</span>, of which {100*n["share_of_hull_in_OCDs"]:.0f}% is inside the OCDs).</li>
<li>It straddles the octet pieces: about {100*(w["cap_octa1"]+w["cap_octa2"])/tot:.0f}% lies in the two caps (half each) and {100*(w["tet1"]+w["tet2"])/tot:.0f}% in the two tetrahedra on the shared edge (half each).</li>
<li><b>Clash:</b> 4 of the step-5 keys (2 from each OCD, on the faces beside the shared edge) reach into it, about {100*sum(n["key_samples_inside_middle"].values())/n["middle_piece_samples"]:.0f}% of its volume. Their base corners sit on the octahedron edges near m.</li>
<li>Open for DICTO: should the middle piece swallow those key tips, or should it be trimmed round them? And should it be cut from the caps and tetrahedra (giving them notches) or replace parts of them?</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-ocd-octet step 7</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'step7-middle.html'), 'w').write(html); print('ok')
