# DICTO 2026-10-18 picture first: the 12 star-centred W round one OCD, with all their meeting seams drawn as ONE continuous keyed Penrose
# pattern (lobes at the star's scale). DICTO: "star centred W the set - the single piece meeting with itself around OCD locking together
# with keyed penrose pattern" / "they all have to show because they are all keying joints, I don't need the star on the edges just a lobe
# or two, same scale as star though" / "the pattern seems continuous across the whole piece".
# Geometry (exact facts used): every W-W face next to the OCD passes through the OCD centre, and all 12 edge midpoints are at the same
# distance R/sqrt2, so round the OCD the 12 W divide directions like the spherical rhombic dodecahedron of the 12 directions (0,+-1,+-1):
# 12 four-sided regions, each holding one five-fold star; seams = 24 arcs from a 4-way corner (+-1,0,0) to a 3-way corner (+-1,+-1,+-1).
# Each seam gets two lobes (thick Penrose rhombi, edge = the star's link rhombus edge 0.2166), one each way, so all W stay identical.
# Drawn on a sphere of radius 0.72 round the OCD (just outside it), orthographic, looking along a two-fold axis; the OCD's own five-kite
# stars are drawn underneath. -> data/p4-lobed-map.json, renders/p4-lobed-map.html
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data', 'step10-input.json')))
V = np.array(D['V']); faces = D['faces']; RS = 0.72; S = 0.2166
dirs = [np.array(p, float) / np.sqrt(2) for p in set(itertools.permutations((0, 1, 1))) | set(itertools.permutations((0, 1, -1))) | set(itertools.permutations((0, -1, -1)))]
dirs = [d for d in dirs]
corner4 = [s * e for e in np.eye(3) for s in (1, -1)]; corner3 = [np.array(s) / np.sqrt(3) for s in itertools.product((1, -1), repeat=3)]
seams = []
for a in corner4:
    for b in corner3:
        if abs(a @ b - 1 / np.sqrt(3)) < 1e-9:
            mid = (a + b) / np.linalg.norm(a + b); near = sorted(range(len(dirs)), key=lambda k: -dirs[k] @ mid)[:2]
            seams.append((a, b, near))
def slerp(a, b, t):
    w = np.arccos(np.clip(a @ b, -1, 1)); return (np.sin((1 - t) * w) * a + np.sin(t * w) * b) / np.sin(w)
lobes = []; seamlines = []
for a, b, (j, k) in seams:
    pts = [slerp(a, b, t) * RS for t in np.linspace(0, 1, 40)]; seamlines.append(pts)
    for t, owner, into in ((1 / 3, j, k), (2 / 3, k, j)):        # two lobes per seam, one each way
        p = slerp(a, b, t); tan = slerp(a, b, t + 1e-3) - slerp(a, b, t - 1e-3); tan /= np.linalg.norm(tan)
        out = dirs[into] - (dirs[into] @ p) * p; out -= (out @ tan) * tan; out /= np.linalg.norm(out)
        half = np.radians(36); dl = 2 * S * np.cos(half); ds = 2 * S * np.sin(half)          # thick rhombus diagonals
        q0 = p * RS; q2 = q0 + out * dl; qc = (q0 + q2) / 2; q1 = qc + tan * ds / 2; q3 = qc - tan * ds / 2
        lobes.append(dict(owner=int(owner), into=int(into), pts=[q.tolist() for q in (q0, q1, q2, q3)]))
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
kites = [[V[i].tolist() for i in f] for f in faces if len(f) == 4 and any(i in five for i in f)]
view = np.array([0, 1, 1]) / np.sqrt(2); ux = np.array([1.0, 0, 0]); uy = np.cross(view, ux)
proj = lambda q: [float(np.array(q) @ ux), float(np.array(q) @ uy)]; front = lambda q: float(np.array(q) @ view) > 0
data = dict(seams=[[proj(q) for q in L if front(q)] for L in seamlines], lobes=[dict(owner=l['owner'], into=l['into'], pts=[proj(q) for q in l['pts']])
            for l in lobes if all(front(q) for q in l['pts'])], kites=[[proj(q) for q in K] for K in kites if all(front(q) for q in K)],
            regions=[dict(k=k, c=proj(d * RS)) for k, d in enumerate(dirs) if front(d)], radius=RS, lobe_edge=S, seams_total=len(seams), lobes_total=len(lobes))
json.dump(data, open(os.path.join(H, '..', 'data', 'p4-lobed-map.json'), 'w')); print(len(seams), 'seams', len(lobes), 'lobes')
pal = ['#ec407a', '#7e57c2', '#26a69a', '#ffa726', '#42a5f5', '#9ccc65', '#ef5350', '#ab47bc', '#29b6f6', '#d4e157', '#8d6e63', '#78909c']
W = 640; sc = W / 1.9; T = lambda p: (W / 2 + p[0] * sc, W / 2 - p[1] * sc); pts = lambda P: ' '.join('%.1f,%.1f' % T(p) for p in P)
g = [f'<svg viewBox="0 0 {W} {W}" role="img" aria-label="Lobed Penrose seams round one OCD">', f'<circle cx="{W/2}" cy="{W/2}" r="{RS*sc:.1f}" class="disc"/>']
g += [f'<polygon points="{pts(K)}" class="kite"/>' for K in data['kites']]
g += [f'<polyline points="{pts(L)}" class="seam"/>' for L in data['seams'] if len(L) > 1]
g += [f'<polygon points="{pts(l["pts"])}" style="fill:{pal[l["owner"]]}" class="lobe"/>' for l in data['lobes']]
g += [f'<circle cx="{T(r_["c"])[0]:.1f}" cy="{T(r_["c"])[1]:.1f}" r="7" style="fill:{pal[r_["k"]]}" class="dot"/>' for r_ in data['regions']]
g.append('</svg>'); svg = ''.join(g)
html = f'''<title>Lobed Penrose Seams</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* layout: one drawing, then how to read it */
:root{{--bg:#f4f3ef;--fg:#1f2329;--muted:#5d6470;--line:#c9ccd2;--sheet:#fff;--disc:#f7efe0;--kite:#e3c45a;--f-ui:"IBM Plex Sans",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--disc:#2a2620;--kite:#8a7440;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121418;--fg:#e6e8ec;--muted:#9aa1ad;--line:#2c313a;--sheet:#1a1d23;--disc:#2a2620;--kite:#8a7440;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-ui);line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
main{{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:14px}} h1{{font-size:1.3rem;margin:0;text-wrap:balance}} .sub{{color:var(--muted);margin:0;max-width:72ch}}
figure{{margin:0;background:var(--sheet);border:1px solid var(--line);border-radius:8px;padding:12px}} svg{{width:100%;height:auto;display:block}}
.disc{{fill:var(--disc);stroke:var(--line)}} .kite{{fill:var(--kite);fill-opacity:.55;stroke:var(--fg);stroke-width:.5}} .seam{{fill:none;stroke:var(--fg);stroke-width:2}}
.lobe{{stroke:var(--fg);stroke-width:1.2;fill-opacity:.9}} .dot{{stroke:var(--fg);stroke-width:1}} ul{{margin:0;padding-left:1.2em;max-width:72ch}} .mark{{font-size:.75rem;color:var(--muted)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&display=swap">
<main>
<h1>Keyed Penrose seams round one OCD</h1>
<p class="sub">Picture first. Looking at one OCD (gold: its five-kite stars) with its 12 star-centred W round it, drawn on a sphere just outside the OCD. Black lines: where the W meet. Coloured dots: one W each (its star). Coloured lobes: star-scale thick Penrose rhombi jutting from one W into its neighbour.</p>
<figure>{svg}</figure>
<ul>
<li>Exact: round the OCD, every W–W joint passes through the OCD centre, so the 12 W split the space round it like a rhombic dodecahedron — <b>12 four-sided regions</b> (not five), one star in each; the joints meet 4 at a time (6 places) or 3 at a time (8 places).</li>
<li>Every seam carries <b>two lobes, one each way</b>, so each W gives as many lobes as it takes and all 12 stay the same piece. 24 seams, 48 lobes per OCD; lobe edge 0.2166 = the edge of the Penrose rhombus that links facing stars (≈ 8.5 mm at a 60 mm octahedron edge).</li>
<li>Only the front half is drawn. In 3D each lobe would run through the joint from the OCD outwards (a tenon), so the pattern is continuous over the whole set.</li>
</ul>
<span class="mark">DICTO · dictospheres.com · 2026-10-18 · studies/2026-10-18-p4-golden-octet-adaptor</span>
</main>'''
open(os.path.join(H, '..', 'renders', 'p4-lobed-map.html'), 'w').write(html); print('ok')
