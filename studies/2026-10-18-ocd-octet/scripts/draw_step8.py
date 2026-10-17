# DICTO 2026-10-18 octet study, step 8 drawing: the trimmed middle piece in 2D -- slices across the shared octahedron edge
# (plane perpendicular to the edge) at the edge midpoint m and stepping along the edge. -> renders/step8-trimmed.html
import json, os, itertools, numpy as np
from scipy.spatial import ConvexHull
from q5 import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
V = np.array([[qf(q(x)) for x in v] for v in S1['V']]); R = qf(q(S1['R'])); E_o = ConvexHull(V).equations
o = np.array([0, R, R]); m = o / 2; ed = np.array([0, 1, -1]) / 2 ** .5; e1 = np.array([1., 0, 0]); e2 = np.array([0, 1, 1]) / 2 ** .5
r = np.linalg.norm(V, axis=1); i1 = [i for i in range(len(V)) if r[i] > r.max() - 1e-9 and abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
star = V[sorted({j for f in S1['faces'] if i1 in f for j in f})]; E_h = ConvexHull(np.vstack([star, o - star])).equations
keys = [ConvexHull(np.array([[qf(q(x)) for x in p] for p in K])).equations for K in S5['keys'].values()]
Tp = np.array([[qf(q(x)) for x in v] for v in S2['Tplus']]); Lf = np.array([[qf(q(x)) for x in v] for v in S2['lattice']])
tets = []
for ijk in itertools.product(range(-2, 3), repeat=3):
    s_ = np.array(ijk) @ Lf
    for T in (Tp, -Tp):
        X = T + s_
        if sum(any(np.allclose(x, p) for x in X) for p in ([0, R, 0], [0, 0, R])) == 2: tets.append(ConvexHull(X).equations)
octa = np.array([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)]); E_oct = ConvexHull(octa).equations
def sect(Eq, shift, base):
    poly = [np.array(c) for c in [(-.45, -.45), (.45, -.45), (.45, .45), (-.45, .45)]]   # the view window
    for e in Eq:
        n = e[:3]; a = np.array([n @ e1, n @ e2]); d = e[3] + n @ (base - shift); out = []
        for i in range(len(poly)):
            A, B = poly[i], poly[(i + 1) % len(poly)]; da, db = a @ A + d, a @ B + d
            if da <= 0: out.append(A)
            if da * db < 0: out.append(A + (B - A) * da / (da - db))
        poly = out
        if len(poly) < 3: return None
    return poly
H = os.path.dirname(os.path.abspath(__file__))
def panel(t):
    base = m + t * ed; x0, x1, y0, y1 = -0.42, 0.42, -0.42, 0.42; W = 340; s = W / (x1 - x0)
    T = lambda p: ((p[0] - x0) * s, (y1 - p[1]) * s); pts = lambda P: ' '.join('%.2f,%.2f' % T(p) for p in P)
    g = [f'<svg viewBox="0 0 {W} {W}" role="img">', f'<rect width="{W}" height="{W}" class="bg"/>']
    for sh in (np.zeros(3), o):
        P = sect(E_oct, sh, base); g += [f'<polygon points="{pts(P)}" class="cap"/>'] if P else []
    for Eq in tets:
        P = sect(Eq, np.zeros(3), base); g += [f'<polygon points="{pts(P)}" class="tet"/>'] if P else []
    P = sect(E_h, np.zeros(3), base); g += [f'<polygon points="{pts(P)}" class="mid"/>'] if P else []
    nk = 0
    for sh in (np.zeros(3), o):
        for Eq in keys:
            P = sect(Eq, sh, base)
            if P: g.append(f'<polygon points="{pts(P)}" class="key"/>'); nk += 1
    for sh in (np.zeros(3), o):
        P = sect(E_o, sh, base); g += [f'<polygon points="{pts(P)}" class="ocd"/>'] if P else []
    X, Y = T((0, 0)); g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="3.5" class="edge"/>')
    g.append('</svg>'); return '\n'.join(g), nk
ts = [0.0, 0.06, 0.12, 0.18]; panels = [panel(t) for t in ts]
figs = '\n'.join(f'<figure>{svg}<figcaption><b>{"At the edge midpoint m" if t == 0 else f"{t:.2f} along the edge"}</b>{"; key cut here" if nk else ""}</figcaption></figure>' for t, (svg, nk) in zip(ts, panels))
html = f'''<title>Trimmed Middle Piece</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: legend strip, then a wrapping row of slice panels, then notes */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--ocd:#e3c45a;--cap:#cfe0f2;--tet:#d6ecd9;--mid:#c8382f;--key:#7a3fa0;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--ocd:#b8962f;--cap:#24384f;--tet:#21402a;--mid:#e0564c;--key:#b07ad6;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--ocd:#b8962f;--cap:#24384f;--tet:#21402a;--mid:#e0564c;--key:#b07ad6;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:72ch}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:10px;display:flex;flex-direction:column;gap:6px;min-width:0}}
svg{{width:100%;height:auto;display:block}} figcaption{{font-size:.85rem;color:var(--muted)}}
.bg{{fill:var(--sheet)}} .cap{{fill:var(--cap);stroke:var(--line)}} .tet{{fill:var(--tet);stroke:var(--line)}} .mid{{fill:var(--mid);fill-opacity:.85}}
.key{{fill:var(--key);stroke:var(--fg);stroke-width:.8}} .ocd{{fill:var(--ocd);stroke:var(--fg);stroke-width:1}} .edge{{fill:var(--fg)}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.9rem}} .legend span{{display:flex;align-items:center;gap:6px}}
.sw{{width:16px;height:12px;border-radius:2px;display:inline-block;border:1px solid var(--line)}}
ul{{margin:0;padding-left:1.2em;max-width:72ch}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>The trimmed middle piece, slice by slice</h1>
<p class="sub">Slices straight across the octahedron edge two OCDs share (the black dot is the edge). Left and right of the dot: the two octahedra (their caps); above and below: the two tetrahedra on that edge. The red middle piece is what is left after the gold OCDs and purple keys are taken out; where red sits on blue or green it notches that cap or tetrahedron. Symmetric: the slices on the other side of m are these turned half a turn.</p>
<div class="legend"><span><i class="sw" style="background:var(--ocd)"></i>OCD</span><span><i class="sw" style="background:var(--key)"></i>Key (stays with its OCD)</span><span><i class="sw" style="background:var(--mid)"></i>Middle piece</span><span><i class="sw" style="background:var(--cap)"></i>Cap, notched by red</span><span><i class="sw" style="background:var(--tet)"></i>Tetrahedron, notched by red</span></div>
<div class="row">{figs}</div>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-ocd-octet step 8 (float)</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'step8-trimmed.html'), 'w').write(html); print('ok', [nk for _, nk in panels])
