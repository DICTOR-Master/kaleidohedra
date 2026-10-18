# Fable review 5 (2026-10-18), PHASE 1 (picture first): continuous kite pattern over the star-centred W, keyed with itself.
# Draws (a) one seam between two W in the plane z = x with the kite rows crossing it, raised/sunk sides marked; (b) the layout over
# the 8 flat faces of one W as two fans round the OCD centres, bump faces vs dent faces, continuation across the folds.
# Geometry from the exact OCD data (fable-review-3 engine). -> renders/p4-continuous-kites.html (+ data/continuous-kites.json)
import sys, os, json, math, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', '..', 'fable-review-3', 'scripts'))
from fable3_engine import *
from fable3_engine import loadS, f3, qv, hull_poly, Poly
from q5 import *
from scipy.spatial import ConvexHull
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; OCD = hull_poly(V, 'OCD'); Vf = np.array([f3(v) for v in V]); R = qf(q(S1['R']))
idx = {tuple(v): i for i, v in enumerate(V)}
def poly_of(pl):
    on = [idx[tuple(c)] for c in OCD.corners if dot(pl[0], c) == pl[1]]; P = Vf[on]; c0 = P.mean(0); nf = f3(pl[0]); a = P[0] - c0; a -= nf * (a @ nf) / (nf @ nf); b = np.cross(nf, a)
    return [on[i] for i in np.argsort(np.arctan2((P - c0) @ b, (P - c0) @ a))]
polys = [poly_of(pl) for pl in OCD.planes]
r = np.linalg.norm(Vf, axis=1); i1 = [i for i in range(len(V)) if abs(r[i] - r.max()) < 1e-9 and abs(Vf[i, 0]) < 1e-9 and Vf[i, 1] > 0 and Vf[i, 2] > 0][0]
star = [p for p in polys if i1 in p]; p = star[0]; k = p.index(i1); P = Vf[[p[k], p[(k + 1) % 4], p[(k + 2) % 4], p[(k + 3) % 4]]]
b = np.linalg.norm(P[1] - P[0]); a = np.linalg.norm(P[2] - P[1]); D = np.linalg.norm(P[2] - P[0])          # short edge (at the star centre), long edge, long diagonal
alpha = 2 * math.degrees(math.asin(np.linalg.norm(P[1] - P[3]) / 2 / a)); beta = 2 * math.degrees(math.asin(np.linalg.norm(P[1] - P[3]) / 2 / b))
s = np.linalg.norm(P[1] - P[3]) / 2; xs = math.sqrt(b * b - s * s)                                       # half short diagonal; tail-to-side-corner along the axis
# face 1 frame
U = np.array([0, 1, 0.]); Wv = np.array([1, 0, 1.]) / np.sqrt(2); N = np.array([1, 0, -1.]) / np.sqrt(2); uv = lambda X: np.array([X @ U, X @ Wv])
E0, Tp = np.array([0, R, 0]), np.array([R / 2, R / 2, R / 2]); tri = np.array([[0, 0], uv(E0), uv(Tp)]); tri_m = tri * np.array([1, -1])
sec = Poly(OCD.planes + [([ONE, Z, qn(ONE)], Z), ([qn(ONE), Z, ONE], Z)], name='sec'); S = np.array([uv(f3(c)) for c in sec.corners]); S = S[ConvexHull(S).vertices]
Sh = np.array([uv(v) for v in Vf]); Sh = Sh[ConvexHull(Sh).vertices]
# the two star rim edges piercing face 1 (for the drawing: where the socket's star reaches the flat face)
star_edges = {(min(x, y), max(x, y)) for q_ in star for kk in range(4) for x, y in [(q_[kk], q_[(kk + 1) % 4])]}
pierce = []
for x, y in star_edges:
    za, zb = Vf[x] @ N, Vf[y] @ N
    if za * zb < 0:
        t = za / (za - zb); Q = Vf[x] + t * (Vf[y] - Vf[x]); d = Vf[y] - Vf[x]; d = d if zb < 0 else -d; din = d - (d @ N) * N; din /= np.linalg.norm(din)
        pierce.append((uv(Q), uv(din)))
# ---------------------------------------------------------------- the kite tiling: rows parallel to the seam A0E0 (u axis), a row axis on the seam
K0 = np.array([[D, 0], [xs, s], [0, 0], [xs, -s]])          # nose (alpha), upper side, tail (beta), lower side; points +u
def kite(j, kk):
    """row j (axis at w = j s), kite kk along the row; even rows point +u, odd rows -u"""
    if j % 2 == 0: return K0 + np.array([kk * D, j * s])
    return np.array([kk * D + xs, j * s]) - K0
D_RIM, D_FAR, RHO_RIM, RHO_FAR = 2.0, 1.1, 0.667, 0.95       # mm at the socket rim / far out; fade between these distances (units) from the OCD centre
def depth_mm(pt):
    rho = math.hypot(pt[0], pt[1]); f = min(1.0, max(0.0, (rho - RHO_RIM) / (RHO_FAR - RHO_RIM))); return D_RIM + (D_FAR - D_RIM) * f
def heights(j):
    """axis height of row j: 0 on the seam, then alternating +d/2, -d/2 ... (anti-symmetric in w)"""
    if j == 0: return 0.0
    return (1 if j % 2 == 1 else -1) * (1 if j > 0 else -1) * 0.5
# clip to a convex polygon (Sutherland-Hodgman)
def clip(poly, conv):
    out = [tuple(pp) for pp in poly]
    for i in range(len(conv)):
        A, B = conv[i], conv[(i + 1) % len(conv)]; inp = out; out = []
        if not inp: break
        def side(pt): return (B[0] - A[0]) * (pt[1] - A[1]) - (B[1] - A[1]) * (pt[0] - A[0])
        for n_ in range(len(inp)):
            cur, prev = inp[n_], inp[n_ - 1]; sc, sp = side(cur), side(prev)
            if sc >= 0:
                if sp < 0: t = sp / (sp - sc); out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
                out.append(cur)
            elif sp >= 0: t = sp / (sp - sc); out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
    return out
def ccw(poly):
    poly = np.array(poly); a_, b_ = poly[1] - poly[0], poly[2] - poly[0]; return poly if a_[0] * b_[1] - a_[1] * b_[0] > 0 else poly[::-1]
tri_c = ccw(tri); trim_c = ccw(tri_m)
tiles = []                                                   # (row j, polygon clipped to face 1, class)
for j in range(-8, 9):
    for kk in range(-2, 5):
        Kj = kite(j, kk)
        for face, conv in (('face1', tri_c), ('mirror', trim_c)):
            c = clip(Kj, conv)
            if len(c) >= 3 and abs(sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c))) / 2) > 1e-6:
                cen = np.mean(np.array(c), axis=0)
                tiles.append(dict(row=j, face=face, poly=[list(map(float, pt)) for pt in c], h=heights(j), depth_mm=depth_mm(cen), whole=len(c) == 4 and np.allclose(sorted(map(tuple, np.round(c, 9))), sorted(map(tuple, np.round(Kj, 9))))))
scale_mm = 60.0 / (R * math.sqrt(2))
geo = dict(mark='DICTO · dictospheres.com', R=R, kite=dict(long_edge=a, short_edge=b, long_diagonal=D, half_short_diagonal=s, apex_alpha_deg=alpha, apex_beta_deg=beta, row_spacing=s),
           tri_uv=tri.tolist(), section_uv=S.tolist(), shadow_uv=Sh.tolist(), pierce=[[q_.tolist(), d_.tolist()] for q_, d_ in pierce], tiles=tiles,
           mm=dict(scale=scale_mm, row_spacing=s * scale_mm, kite_long_edge=a * scale_mm, kite_short_edge=b * scale_mm, kite_length=D * scale_mm, face_A0E0=R * scale_mm, face_A0T=R * math.sqrt(3) / 2 * scale_mm),
           depth_options={str(dmm): dict(depth_mm=dmm, slope_deg=math.degrees(math.atan(dmm / (s * scale_mm))), crease_fold_deg=2 * math.degrees(math.atan(0.5 * dmm / (xs * scale_mm)))) for dmm in (1.1, 1.5, 2.0, 2.5)})
os.makedirs(os.path.join(H, '..', 'data'), exist_ok=True); json.dump(geo, open(os.path.join(H, '..', 'data', 'continuous-kites.json'), 'w'), indent=1)
# ---------------------------------------------------------------- SVG
def svg_poly(pts, cls, extra=''): return f'<polygon class="{cls}" points="{" ".join(f"{x:.4f},{y:.4f}" for x, y in pts)}" {extra}/>'
def panel_a():
    # plane z = x round the seam: face 1 above (w > 0), the mirror face below; u to the right, w up (SVG y flipped)
    T = lambda pt: (pt[0] * 100, -pt[1] * 100)
    out = []
    for t_ in tiles:
        cls = 'kite ' + ('raised' if t_['h'] > 0 else 'sunk' if t_['h'] < 0 else 'seam'); out.append(svg_poly([T(pt) for pt in t_['poly']], cls, f'style="fill-opacity:{0.12 + 0.4 * t_["depth_mm"] / D_RIM:.2f}"'))
    # seam kites: split colouring by the sign of w
    for t_ in tiles:
        if t_['row'] == 0:
            up = clip(t_['poly'], ccw([[-1, 0], [3, 0], [3, 2], [-1, 2]])); dn = clip(t_['poly'], ccw([[-1, -2], [3, -2], [3, 0], [-1, 0]]))
            op = f'style="fill-opacity:{0.12 + 0.4 * t_["depth_mm"] / D_RIM:.2f}"'
            if len(up) >= 3: out.append(svg_poly([T(pt) for pt in up], 'kite raised half', op))
            if len(dn) >= 3: out.append(svg_poly([T(pt) for pt in dn], 'kite sunk half', op))
    out.append(svg_poly([T(pt) for pt in tri], 'face')); out.append(svg_poly([T(pt) for pt in tri_m], 'face'))
    out.append(svg_poly([T(pt) for pt in Sh], 'shadow')); out.append(svg_poly([T(pt) for pt in S], 'socket'))
    for q_, d_ in pierce:
        q2 = q_ + 0.12 * d_; out.append(f'<line class="star" x1="{T(q_)[0]:.3f}" y1="{T(q_)[1]:.3f}" x2="{T(q2)[0]:.3f}" y2="{T(q2)[1]:.3f}"/>')
    out.append(f'<line class="seam" x1="0" y1="0" x2="{R * 100:.2f}" y2="0"/>')
    lab = lambda pt, txt, cls='lab', anchor='start': f'<text class="{cls}" x="{T(pt)[0]:.2f}" y="{T(pt)[1]:.2f}" text-anchor="{anchor}">{txt}</text>'
    out += [lab((0.02, 0.04), 'A0 (OCD centre, inside the socket)'), lab((R + 0.02, 0.0), 'E0 (edge end)'), lab((tri[2][0], tri[2][1] + 0.05), 'T+ (tetrahedron centre)', anchor='middle'),
            lab((tri_m[2][0], tri_m[2][1] - 0.04), 'T− (tetrahedron centre)', anchor='middle'),
            lab((0.72, 0.70), 'face 1 of W(m): raised rows = bumps of W(m)', 'lab strong'), lab((0.72, -0.70), 'mirror face of W(ρm): the same rows, sign reversed', 'lab strong'),
            lab((0.5, -0.03), 'seam A0E0: a row axis — these kites are half raised, half sunk', 'lab', 'start'), lab((0.75, 0.06), 'socket rim (OCD section); grey = OCD shadow', 'lab small')]
    return '\n'.join(out)
def panel_b():
    # two fans of four faces round A0 and A1; each face drawn in its own frame (A at the fan centre, E along the first edge, T the apex)
    ang = math.degrees(math.atan2(tri[2][1], tri[2][0])); out = []
    def fan(cx, cy, faces, centre_label):
        rot = -ang * 2  # start angle
        for fi, (name, sign, labels) in enumerate(faces):
            th = math.radians(rot + fi * ang); th2 = th + math.radians(ang)
            def T(pt, th=th):
                # face frame: u along the edge A->E at angle th, w toward T (rotate by +ang inside the wedge)
                x = pt[0] * math.cos(th) - pt[1] * math.sin(th); y = pt[0] * math.sin(th) + pt[1] * math.cos(th); return (cx + 95 * x, cy - 95 * y)
            for t_ in tiles:
                if t_['face'] != 'face1': continue
                h = t_['h'] * sign; cls = 'kite ' + ('raised' if h > 0 else 'sunk' if h < 0 else 'seam'); out.append(svg_poly([T(pt) for pt in t_['poly']], cls, f'style="fill-opacity:{0.12 + 0.4 * t_["depth_mm"] / D_RIM:.2f}"'))
            out.append(svg_poly([T(pt) for pt in tri], 'face')); out.append(svg_poly([T(pt) for pt in S], 'socket'))
            mid = T((0.62, 0.42)); out.append(f'<text class="lab strong" x="{mid[0]:.1f}" y="{mid[1]:.1f}" text-anchor="middle">{name}</text>')
            e = T((R * 1.04, -0.02)); out.append(f'<text class="lab small" x="{e[0]:.1f}" y="{e[1]:.1f}" text-anchor="middle">{labels[0]}</text>')
            tt = T((tri[2][0], tri[2][1] + 0.06)); out.append(f'<text class="lab small" x="{tt[0]:.1f}" y="{tt[1]:.1f}" text-anchor="middle">{labels[1]}</text>')
        out.append(f'<text class="lab strong" x="{cx}" y="{cy + 4}" text-anchor="middle">{centre_label}</text>')
    fan(300, 330, [('face 1  bump', +1, ('E0', 'T+')), ('face 3  dent', -1, ('E1', 'T+')), ('face 2  dent', -1, ('E1', 'T−')), ('face 0  bump', +1, ('E0', 'T−'))], 'A0')
    fan(850, 330, [('face 7  bump', +1, ('E1', 'T−')), ('face 5  dent', -1, ('E0', 'T−')), ('face 4  dent', -1, ('E0', 'T+')), ('face 6  bump', +1, ('E1', 'T+'))], 'A1')
    return '\n'.join(out)
def profile():
    """section across the rows (w direction) at u = 0.80, from the E0T+ side of face 1 down through the seam into the mirror face: zig-zag heights
    +-d(rho)/2 in mm; and the depth law d(rho) in mm against the distance from the OCD centre"""
    out = []; u0 = 0.80
    T = lambda w, hmm: (380 + w * 420, 70 - hmm * 18)
    pts = []
    for j in range(-6, 7):
        w = j * s
        if abs(w) > 0.62: continue
        dmm = depth_mm((u0, w)); pts.append((w, heights(j) * dmm))
    out.append('<polyline class="prof" points="' + ' '.join(f'{T(w, h)[0]:.1f},{T(w, h)[1]:.1f}' for w, h in pts) + '"/>')
    out.append(f'<line class="seam" x1="{T(-0.62, 0)[0]:.1f}" y1="{T(0, 0)[1]:.1f}" x2="{T(0.62, 0)[0]:.1f}" y2="{T(0, 0)[1]:.1f}"/>')
    out.append(f'<line class="axis" x1="{T(0, 0)[0]:.1f}" y1="{T(0, 1.4)[1]:.1f}" x2="{T(0, 0)[0]:.1f}" y2="{T(0, -1.4)[1]:.1f}"/>')
    for w, h in pts:
        if abs(h) > 0.05: out.append(f'<text class="lab small" x="{T(w, h)[0]:.1f}" y="{T(w, h)[1] + (14 if h < 0 else -6):.1f}" text-anchor="middle">{abs(2 * h):.1f}</text>')
    out.append(f'<text class="lab" x="{T(-0.62, 0)[0]:.1f}" y="{T(0, 1.4)[1] - 22:.1f}">section across the rows at u = {u0 * scale_mm:.0f} mm from A0, through the seam (centre); numbers = ridge-to-valley depth in mm; heights x3</text>')
    out.append(f'<text class="lab small" x="{T(0, 0)[0] + 4:.1f}" y="{T(0, -1.4)[1] + 4:.1f}">seam A0E0</text>')
    out.append(f'<text class="lab small" x="{T(0.62, 0)[0]:.1f}" y="{T(0, 0)[1] + 28:.1f}" text-anchor="end">face 1 (W(m)) →</text>')
    out.append(f'<text class="lab small" x="{T(-0.62, 0)[0]:.1f}" y="{T(0, 0)[1] + 28:.1f}">← mirror face (W(ρm))</text>')
    # depth law graph: x = distance from the OCD centre in mm (rim .. corner E0), y = depth in mm
    G = lambda rmm, dmm: (120 + (rmm - 20) * 22, 190 - dmm * 30)
    xs_ = np.linspace(RHO_RIM * scale_mm, R * scale_mm, 60); out.append('<polyline class="prof" points="' + ' '.join(f'{G(x, depth_mm((x / scale_mm, 0)))[0]:.1f},{G(x, depth_mm((x / scale_mm, 0)))[1]:.1f}' for x in xs_) + '"/>')
    for x, lab in ((RHO_RIM * scale_mm, 'socket rim'), (RHO_FAR * scale_mm, 'fade end'), (R * math.sqrt(3) / 2 * scale_mm, 'T (corner)'), (R * scale_mm, 'E (corner)')):
        out.append(f'<line class="axis" x1="{G(x, 0)[0]:.1f}" y1="{G(x, 0)[1]:.1f}" x2="{G(x, 2.3)[0]:.1f}" y2="{G(x, 2.3)[1]:.1f}"/><text class="lab small" x="{G(x, 0)[0]:.1f}" y="{G(x, 0)[1] + 12:.1f}" text-anchor="middle">{lab} {x:.0f} mm</text>')
    for dmm in (1.1, 2.0): out.append(f'<text class="lab small" x="{G(20, dmm)[0] - 4:.1f}" y="{G(20, dmm)[1] + 3:.1f}" text-anchor="end">{dmm} mm</text>')
    out.append(f'<text class="lab" x="{G(20, 2.3)[0]:.1f}" y="{G(20, 2.3)[1] - 8:.1f}">depth law d(distance from the OCD centre): {D_RIM} mm at the rim → {D_FAR} mm from {RHO_FAR * scale_mm:.0f} mm on (both sockets; the two fields meet on the bisector E0T+, where they are equal)</text>')
    return '\n'.join(out)
dep = geo['depth_options']
style = '''
:root{--bg:#f3f4f6;--fg:#1d2230;--muted:#5b6275;--line:#d5d8e0;--panel:#fff;--raise:#e4593b;--sink:#3b6fd1;--seamc:#8e6bb8;--sock:#d9a21b;--f-ui:"IBM Plex Sans",system-ui,sans-serif;--f-num:"IBM Plex Mono",ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11141b;--fg:#e6e8ee;--muted:#9aa1b2;--line:#2a2f3c;--panel:#181c25;--raise:#f07a5e;--sink:#6f9bea;--seamc:#b394dd;--sock:#e8c56a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11141b;--fg:#e6e8ee;--muted:#9aa1b2;--line:#2a2f3c;--panel:#181c25;--raise:#f07a5e;--sink:#6f9bea;--seamc:#b394dd;--sock:#e8c56a;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--f-ui);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:12px;display:flex;flex-direction:column;gap:14px}
h1{font-size:1.15rem;margin:0;font-weight:600;text-wrap:balance} h2{font-size:1rem;margin:0;font-weight:600} p,li{font-size:.9rem;max-width:80ch;line-height:1.45} .meta{color:var(--muted);margin:0}
.panel{border:1px solid var(--line);border-radius:8px;background:var(--panel);padding:10px;overflow-x:auto} svg{display:block;max-width:100%;height:auto}
.kite{stroke:var(--fg);stroke-width:.6;fill:none} .raised{fill:var(--raise);fill-opacity:.55} .sunk{fill:var(--sink);fill-opacity:.55} .seam{stroke:var(--seamc);stroke-width:1.6} .kite.seam{fill:var(--seamc);fill-opacity:.25;stroke:var(--fg)}
.half{stroke:none} .face{fill:none;stroke:var(--fg);stroke-width:1.4} .socket{fill:var(--sock);fill-opacity:.9;stroke:var(--fg);stroke-width:.8} .shadow{fill:var(--fg);fill-opacity:.12;stroke:none}
.star{stroke:var(--fg);stroke-width:1.8;stroke-dasharray:3 2} .prof{fill:none;stroke:var(--fg);stroke-width:2} .axis{stroke:var(--muted);stroke-width:.8;stroke-dasharray:2 2}
.lab{font-size:9px;fill:var(--fg);font-family:var(--f-num)} .strong{font-weight:600;font-size:10px} .small{font-size:8px;fill:var(--muted)}
table{border-collapse:collapse;font-size:.88rem;font-variant-numeric:tabular-nums} td,th{border:1px solid var(--line);padding:4px 8px;text-align:right} th:first-child,td:first-child{text-align:left}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:.85rem} .sw{display:inline-block;width:12px;height:12px;border-radius:2px;vertical-align:-2px;margin-right:4px}
'''
html = f'''<title>Continuous Kite Keys</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>{style}</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;600&display=swap">
<h1>Continuous kite keys on the star-centred W — phase 1 drawing</h1>
<p class="meta">DICTO 2026-10-18: "the keys to provide a continuous decorative pattern as well as key … transition is what I mean" — the OCD's star kites at exact star scale, one pattern over the whole assembly, kites running across the seams, every W identical, the relief deepest at the sockets and fading outward so the star grows out of its socket into the surface pattern. Drawing only; no 3D yet. Colour strength = local depth. DICTO · dictospheres.com · fable-review-5</p>
<div class="legend"><span><span class="sw" style="background:var(--raise)"></span>raised (ridge +d/2 toward the viewer of this face)</span><span><span class="sw" style="background:var(--sink)"></span>sunk (valley −d/2)</span><span><span class="sw" style="background:var(--seamc)"></span>seam kites: half raised, half sunk</span><span><span class="sw" style="background:var(--sock)"></span>socket (OCD)</span><span>dashed = the socket star's two rim edges reaching the face</span></div>
<div class="panel"><h2>(a) One seam, in the plane of the flat faces</h2>
<svg viewBox="-12 -92 160 184" width="1100" height="1265" role="img" aria-label="Kite rows crossing the seam between two W faces">{panel_a()}</svg></div>
<div class="panel"><h2>Depth transition: section across the seam, and the depth law</h2><svg viewBox="0 0 760 215" width="760" height="215" role="img" aria-label="height profile and depth law">{profile()}</svg>
<p>Measured on the OCD itself: its kites fold by 23.8° (dihedral 156.2°) and the star centre rises {(0.6951994790452729 - 2 / 3) * scale_mm:.2f} mm above the ring of its neighbours — the imprint's own relief is about 1.1 mm, i.e. DICTO's number. A kite roof folding like the OCD's facets (23.8°) over one row spacing is 0.9 mm deep. So "imprint depth fading to 1.1 mm" would be flat; for a visible transition the rows nearest the socket must be deeper than the imprint. Drawn: <strong>{D_RIM} mm at the socket rim fading linearly to {D_FAR} mm at {RHO_FAR * scale_mm:.0f} mm from the OCD centre</strong> (the fade spans the inner {(RHO_FAR - RHO_RIM) * scale_mm:.0f} mm of each face; the far corners stay at 1.1 mm). Alternative if the far surface should be fainter: 1.1 mm at the rim fading to 0.5 mm. The depth field depends only on the distance from the nearer OCD centre, so it is continuous across every seam and fold (the piece's E0T-type edges lie on the bisector of the two centres).</p></div>
<div class="panel"><h2>(b) The 8 flat faces of one W (each drawn in its own frame: A at the fan centre, E along the edge, T at the apex)</h2>
<svg viewBox="80 60 1000 440" width="1100" height="484" role="img" aria-label="layout over the eight faces">{panel_b()}</svg>
<p>All eight faces carry the <em>same</em> picture in their own (A, E, T) frame; the four bump faces (A0E0T±, A1E1T±) with the signs shown, the four dent faces (A0E1T±, A1E0T±) with every sign reversed. Across the fold A0T+ (faces 1 and 3) the two pictures are related by the 3-fold turn about that edge, across A0E0 (faces 1 and 0) by the mirror x = 0, across E0T+ (faces 1 and 4) by the 3-fold turn about that edge, across the piece (faces 1 and 7) by the inversion through the edge midpoint — each fixes the shared edge point by point, so every kite line that reaches a fold continues on the next face.</p></div>
<div class="panel"><h2>How the pattern is derived, and what it does</h2>
<ul>
<li><strong>Tile.</strong> The OCD's star kite itself: long edge {geo["mm"]["kite_long_edge"]:.1f} mm, short edge {geo["mm"]["kite_short_edge"]:.1f} mm, length {geo["mm"]["kite_length"]:.1f} mm, apex angles {alpha:.1f}° / {beta:.1f}° (60 mm octahedron edge). Same scale as the star in the socket.</li>
<li><strong>Tiling.</strong> The only way congruent kites tile a plane edge to edge: rows of kites nose to tail, neighbouring rows pointing the opposite way and sitting in each other's notches (row spacing {geo["mm"]["row_spacing"]:.1f} mm). The rows run parallel to the piece's seam edge A0E0 and one row axis lies <em>on</em> the seam.</li>
<li><strong>Why that orientation is forced.</strong> Across the seam A0E0 the next face in the same plane belongs to another W, placed by the half-turn about the A0E0 axis. That turn reverses the face normal, so the height field must be anti-symmetric across the seam (zero on it) and the kite lines must be mirror-symmetric about it. The kite tiling's only mirror lines are its row axes, hence rows parallel to A0E0 with an axis on the seam. The seam kites are then split exactly in half: the upper half rises as a bump of one W, the lower half sinks as the dent of the W behind — DICTO's "kite split between neighbouring W".</li>
<li><strong>Heights.</strong> Row axes alternate: seam 0, then +d/2, −d/2, +d/2 … outward (anti-symmetric on the other side), with d the local depth of the transition law above (deepest at the socket, 1.1 mm far out). Each kite becomes a shallow roof (ridge along its long diagonal) or trough; every raised kite row on a bump face faces a sunk row on the neighbour. Within one face the rows alternate raised / sunk, so the pattern is decorative on its own and the whole face is a key.</li>
<li><strong>One identical piece.</strong> The eight faces pair bipartitely across the structure (bump faces A0E0T±, A1E1T±; dent faces A0E1T±, A1E0T±; the neighbour across any face presents a face of the other class). The pattern on one face is carried to the other seven by the piece's own 2/m symmetry and by the 3-fold turns about the OCD centres, as in the first keyed W, so every W is the same solid and every bump meets a dent. This is exact, not approximate.</li>
</ul></div>
<div class="panel"><h2>Depth and slope (per row spacing of {geo["mm"]["row_spacing"]:.1f} mm)</h2>
<table><tr><th>pattern depth d (ridge to valley)</th><th>slope of the kite roofs</th><th>crease along the kite's long diagonal</th><th>reads as</th></tr>
{''.join(f"<tr><td>{v['depth_mm']:.1f} mm</td><td>{v['slope_deg']:.0f}°</td><td>{v['crease_fold_deg']:.0f}°</td><td>{'far corners (DICTO´s 1.1 mm = the imprint´s own relief)' if k == '1.1' else 'at the socket rim (drawn)' if k == '2.0' else 'deeper option at the rim' if k == '2.5' else 'between'}</td></tr>" for k, v in dep.items())}
</table>
<p>With the transition the keys are firmest where they matter most, next to the sockets (2 mm, {dep['2.0']['slope_deg']:.0f}° slopes), and decorative-depth (1.1 mm, {dep['1.1']['slope_deg']:.0f}°) at the far corners. The piece's 7.5 mm waist is unaffected.</p></div>
<div class="panel"><h2>Problems, stated plainly</h2>
<ul>
<li><strong>Flat tilted kites are impossible.</strong> A periodic plane tiling by one flat tilted kite is a tilted plane: there is no non-trivial way to give every kite a flat facet. The kites here are creased along their long diagonal (two triangles, fold of {dep['1.1']['crease_fold_deg']:.0f}° at 1.1 mm); at that depth the crease reads as a soft ridge, not a break, but it is not the OCD's flat facet.</li>
<li><strong>The star does not continue into the rows.</strong> Five-fold order cannot run into a periodic row tiling. The socket rim is a visible join, as on the OCD where the W planes cut its faces. Of the two star edges reaching each face (dashed), one lies within 1° of a row direction but aligning it would tilt the rows off the seam and break the mirror; the rows stay parallel to A0E0.</li>
<li><strong>The piece's oblique edges.</strong> Along A0T, E0T (and their A1 twins) the relief must return to the face plane so that the faces meet in a closed solid: a fade band about one row wide along those edges (not drawn as such; the clipped kites there will be flattened in 3D). Along the seam edges A0E0, A1E1 nothing fades — the zero line is the seam itself.</li>
<li><strong>Corners.</strong> The piece corner E0 falls at 2.9 kite lengths from A0, not on a kite vertex; the pattern is simply cut there, and beyond E0 the next W's rows run the other way (inversion through E0). Pattern lines meet at E0 but the kites do not continue straight through it.</li>
<li><strong>The transition and the sockets.</strong> The deepest rows sit next to the socket rim, exactly where the OCD's shadow (grey) overhangs the face plane: raised rows there must stay clear of the OCD (the first keyed W kept 1.3 mm). The transition may need to start a few mm outside the rim; to be checked in 3D.</li>
<li><strong>Not yet checked</strong> (phase 1): the 3D closure at the fade bands, print tolerance, the socket shadow margin for the deep rows.</li>
</ul></div>
'''
os.makedirs(os.path.join(H, '..', 'renders'), exist_ok=True); open(os.path.join(H, '..', 'renders', 'p4-continuous-kites.html'), 'w').write(html)
print('tiles', len(tiles), 'whole kites in face 1', sum(1 for t_ in tiles if t_['face'] == 'face1' and t_['whole']), 'depth', json.dumps(dep))
