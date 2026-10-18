# DICTO 2026-10-18 keyed Penrose pattern on the star-centred W, one piece type kept -- 2D drawing (picture first).
# Face 0 of W (corners: OCD centre A, edge end E, tetrahedron centre T) carries raised Penrose keys; its partner faces carry the same
# pattern sunk (data/p4-key-pairing.json: bump faces {0,1,6,7}, dent faces {2,3,4,5}). The OCD imprint near A is cut away in the face.
# A Penrose "sun" (5 thick rhombi) + 5 thin rhombi ring, sized to fit the free part of the face. -> renders/p4-penrose-keys.html
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data', 'step10-input.json')))
R = D['R']; V = np.array(D['V'])
from scipy.spatial import ConvexHull
E = ConvexHull(V).equations
A, Ee, T = np.zeros(3), np.array([0, R, 0]), np.array([-R / 2, R / 2, R / 2])
u = (Ee - A) / np.linalg.norm(Ee - A); n = np.cross(Ee - A, T - A); n /= np.linalg.norm(n); w = np.cross(n, u)
f2 = lambda p: [float((p - A) @ u), float((p - A) @ w)]
tri = [f2(A), f2(Ee), f2(T)]
# OCD section in the face plane (OCD centred at A): clip a big square in plane coords by the OCD's planes
poly = [np.array(c) for c in [(-2, -2), (2, -2), (2, 2), (-2, 2)]]
for e in E:
    a2 = np.array([e[:3] @ u, e[:3] @ w]); d = e[3]; out = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]; dp, dq = a2 @ P + d, a2 @ Q + d
        if dp <= 0: out.append(P)
        if dp * dq < 0: out.append(P + (Q - P) * dp / (dp - dq))
    poly = out
ocd = [p.tolist() for p in poly]
# Penrose sun + ring: thick rhombi (72 deg) round a centre, thin rhombi (36 deg) between their outer tips
# centre of the largest free disc: inside the face, outside the OCD imprint (grid search)
def segdist(p, a, b):
    a, b = np.array(a), np.array(b); t = np.clip((p - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); return np.linalg.norm(p - a - t * (b - a))
def in_poly(p, P):
    P = np.array(P); ins = False
    for i in range(len(P)):
        a, b = P[i], P[i - 1]
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]: ins = not ins
    return ins
best, c = -1, None
for x in np.linspace(min(q[0] for q in tri), max(q[0] for q in tri), 120):
    for y in np.linspace(min(q[1] for q in tri), max(q[1] for q in tri), 120):
        p = np.array([x, y])
        if not in_poly(p, tri) or in_poly(p, ocd): continue
        dd = min([segdist(p, tri[i], tri[i - 1]) for i in range(3)] + [segdist(p, ocd[i], ocd[i - 1]) for i in range(len(ocd))])
        if dd > best: best, c = dd, p
s = best / 2.75; ang = np.radians(np.arange(5) * 72 + 90); uv = lambda t: np.array([np.cos(t), np.sin(t)])
thick, thin = [], []
for k in range(5):
    a0, a1 = ang[k] - np.radians(36), ang[k] + np.radians(36)
    p0 = c; p1 = c + s * uv(a0); p3 = c + s * uv(a1); p2 = p1 + s * uv(a1); thick.append([p0, p1, p2, p3])
for k in range(5):
    tipA = thick[k][2]; tipB = thick[(k + 1) % 5][2]; mid = thick[k][3]
    thin.append([mid, tipA, tipA + (tipB - mid), tipB])
def inside(P):
    a, b, cc = map(np.array, tri)
    def side(p, q, r): d1, d2 = q - p, r - p; return d1[0] * d2[1] - d1[1] * d2[0]
    return all(side(a, b, P) * side(a, b, cc) >= 0 and side(b, cc, P) * side(b, cc, a) >= 0 and side(cc, a, P) * side(cc, a, b) >= 0 for _ in [0])
fits = all(inside(p) for r in thick + thin for p in r)
res = dict(free_disc_radius=float(best), face_corners=dict(A='OCD centre', E='edge end (octet vertex)', T='tetrahedron centre'), edge_AE=R, edge_AT=R * 3 ** .5 / 2, rhombus_edge=s, keys_fit_inside_face=fits,
           tri=tri, ocd=ocd, thick=[[q.tolist() for q in r] for r in thick], thin=[[q.tolist() for q in r] for r in thin])
json.dump(res, open(os.path.join(H, '..', 'data', 'p4-penrose-keys.json'), 'w')); print('fits', fits)
xs = [p[0] for p in tri]; ys = [p[1] for p in tri]; x0, x1, y0, y1 = min(xs) - .1, max(xs) + .1, min(ys) - .1, max(ys) + .1
W = 420; sc = W / (x1 - x0); Hh = round((y1 - y0) * sc)
Tm = lambda p: ((p[0] - x0) * sc, (y1 - p[1]) * sc); pts = lambda P: ' '.join('%.1f,%.1f' % Tm(p) for p in P)
def panel(raised):
    g = [f'<svg viewBox="0 0 {W} {Hh}" role="img"><defs><clipPath id="t{int(raised)}"><polygon points="{pts(tri)}"/></clipPath></defs>',
         f'<polygon points="{pts(tri)}" class="face"/>', f'<polygon points="{pts(ocd)}" class="ocd" clip-path="url(#t{int(raised)})"/>']
    for r in thick: g.append(f'<polygon points="{pts(r)}" class="{"bthick" if raised else "dthick"}"/>')
    for r in thin: g.append(f'<polygon points="{pts(r)}" class="{"bthin" if raised else "dthin"}"/>')
    for p, l in zip(tri, ('A  OCD centre', 'E  edge end', 'T  tetrahedron centre')):
        X, Y = Tm(p); g.append(f'<text x="{X+6:.1f}" y="{Y-6:.1f}" class="lbl">{l}</text>')
    return ''.join(g) + '</svg>'
html = f'''<title>Penrose Keys on W</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: two face panels side by side, then the rule and the other two options */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--face:#f6d4e2;--ocd:#d9a21b;--k1:#c2185b;--k2:#f48fb1;--f-ui:"IBM Plex Sans",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--face:#4a2433;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--face:#4a2433;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:960px;margin:0 auto;display:flex;flex-direction:column;gap:16px}} h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:75ch}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:6px;min-width:0}} svg{{width:100%;height:auto}} figcaption{{font-size:.85rem;color:var(--muted)}}
.face{{fill:var(--face);stroke:var(--fg);stroke-width:1.2}} .ocd{{fill:var(--ocd);fill-opacity:.7}}
.bthick{{fill:var(--k1);stroke:var(--fg);stroke-width:.8}} .bthin{{fill:var(--k2);stroke:var(--fg);stroke-width:.8}}
.dthick{{fill:none;stroke:var(--k1);stroke-width:1.6;stroke-dasharray:4 2}} .dthin{{fill:none;stroke:var(--k2);stroke-width:1.6;stroke-dasharray:4 2}}
.lbl{{fill:var(--fg);font:11px var(--f-ui)}} ul{{margin:0;padding-left:1.2em;max-width:78ch}} .mark{{font-size:.75rem;color:var(--muted)}} .tag{{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>Penrose keys on the star-centred W — one piece type</h1>
<p class="sub">Picture first (proposal, Claude). Each W has 8 triangular faces where it meets a neighbouring W. Exact pairing check: the faces split into 4 "bump" faces and 4 "dent" faces so that every shared face meets a bump with a dent, and all W stay identical. Gold: where the OCD imprint cuts the face. <span class="tag">Penrose keys: thick rhombi (dark) and thin rhombi (light)</span></p>
<div class="row"><figure>{panel(True)}<figcaption><b>Bump face</b> (faces 0, 1, 6, 7: those holding A with E₁, or B with E₂): the Penrose sun stands out.</figcaption></figure>
<figure>{panel(False)}<figcaption><b>Dent face</b> (faces 2, 3, 4, 5): the same pattern sunk, so the neighbour's bumps sit in it.</figcaption></figure></div>
<ul>
<li>Pairing (exact symmetry check, data/p4-key-pairing.json): no face is paired with itself, and the bump/dent split is consistent, so <b>one W shape carries all the keys</b>.</li>
<li>Free disc on the face (outside the OCD imprint): radius {best:.4f}; rhombus edge {s:.4f} (≈ {s / (R * 2 ** .5) * 60:.1f} mm at a 60 mm octahedron edge); keys fit inside the face: {fits}.</li>
<li>Also possible (as many as possible): <b>the central Penrose prism as a key piece</b> through W (the thick rhombus prism of step 13; with its two flanking prisms), and a <b>Penrose pattern on the exposed outer skin</b> of a chamber. To draw next.</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-p4-golden-octet-adaptor</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'p4-penrose-keys.html'), 'w').write(html); print('ok')
