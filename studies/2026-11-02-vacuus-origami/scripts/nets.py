# Printable A4 nets of the DICTO Vacuus as modular origami (DICTO proposed 2026-11-02), from fan.py's JSON.
# One open-pyramid fan per face (one triangle per face edge, apex = the centre O), at one true scale per solid: the largest net fills
# the printable area of A4. Lines: cut = solid; valley = dashed; mountain = dash-dot (seen from the printed side = the inside of the
# open pyramid). Tabs:
#  - SEAM tab (one per fan): on the free strut edge of the last triangle; it is glued under the first triangle (marked 1), which closes
#    the fan into an open pyramid. Its fold is the strut fold of that corner (valley, dihedral psi).
#  - RIM half-tabs, the tab rule: every fan triangle O-A-B, with A -> B counter-clockwise on the printed side (= counter-clockwise seen
#    from outside the solid), carries a tab on the half of its rim edge AB next to B. The neighbouring pyramid runs the same edge B -> A,
#    so its tab sits on the other half (next to A). Each rim edge thus gets exactly two half-tabs, one from each pyramid of the fin pair;
#    each folds 180 deg over the double rim (mountain) and is glued to the neighbour's printed side. The rule depends only on the
#    orientation, so congruent pyramids (related by rotations) get identical nets.
# Every copy is labelled: net type, copy number, fin letter on each triangle, the neighbouring net type behind it (the double wall),
# the strut class at each rim corner, the fold dihedral psi on every fold, and the target of every tab.
# Page 1 is the assembly guide. Checks: no two pieces of a net overlap (shapely, area < 1e-6 mm^2), each net is one piece, every net
# fits the page, the 50 mm scale bar. Usage: nets.py <fan json> <render png or -> <logo png> <out pdf>
import sys, os, json, math, textwrap, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
from shapely import affinity
from PIL import Image
J, RENDER, LOGO, OUT = sys.argv[1:5]
r = json.load(open(J)); T = r['types']; NAME = r['name']
SHORT = {'Kagemusha': 'Kagemusha (D86)'}.get(NAME, NAME)
PW, PH = 210.0, 297.0; X0, X1, Y0, Y1 = 12.0, 198.0, 23.0, 272.0; W, H = X1 - X0, Y1 - Y0
RIM_T, SEAM_T, GAP = 6.0, 7.0, 4.0
plt.rcParams.update({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42})
LOGO_IM = np.asarray(Image.open(LOGO).convert('RGBA'))
def fan_points(ty):
    phi = [0.0]
    for t in ty['tri']: phi.append(phi[-1] + t['theta'])
    rr = [math.sqrt(t['ra2']) for t in ty['tri']] + [math.sqrt(ty['tri'][0]['ra2'])]
    return np.array([[q * math.cos(p), q * math.sin(p)] for q, p in zip(rr, phi)]), phi
def build(ty, s):
    """the net of one type at scale s (mm per unit): pieces (polygons), fold lines, labels; overlaps checked"""
    P, phi = fan_points(ty); P = P * s; m = len(ty['tri']); O = np.zeros(2)
    tris = [Polygon([O, P[j], P[j + 1]]) for j in range(m)]
    folds = []; labels = []; rim = []
    for j in range(1, m):
        folds.append(('valley' if ty['psi'][j] < math.pi else 'mountain', O, P[j], f"{math.degrees(ty['psi'][j]):.1f}°"))
    # rim half-tabs (next to the leading corner P[j+1])
    for j in range(m):
        A, B = P[j], P[j + 1]; L = np.linalg.norm(B - A); u = (B - A) / L; nrm = np.array([u[1], -u[0]])
        if nrm @ ((A + B) / 2) < 0: nrm = -nrm
        g = 0.6; half = L / 2 - 2 * g; t = min(RIM_T, 0.42 * half)
        Q0 = (A + B) / 2 + u * g; Q1 = B - u * g; Q2 = Q1 - u * t + nrm * t; Q3 = Q0 + u * t + nrm * t
        rim.append(Polygon([Q0, Q1, Q2, Q3])); folds.append(('mountain', Q0, Q1, None))
        t0 = ty['tri'][j]; labels.append(('tab', (Q0 + Q1 + Q2 + Q3) / 4, math.degrees(math.atan2(u[1], u[0])), f"→ {T[t0['nbr_type']]['name']} {t0['fin']}", t))
    # seam tab on the free strut edge O-P[m] of the last triangle, pointing into the gap (angles beyond phi[m])
    a = P[m] / np.linalg.norm(P[m]); Lm = np.linalg.norm(P[m]); nrm = np.array([-a[1], a[0]])  # ccw normal: into the gap
    body = unary_union(tris + rim)
    seam = None
    for frac0, t in [(0.18, SEAM_T), (0.25, SEAM_T), (0.3, 5.0), (0.35, 4.0), (0.4, 3.0), (0.45, 2.5)]:
        d0, d1 = frac0 * Lm, 0.90 * Lm; tt = min(t, 0.3 * (d1 - d0))
        cand = Polygon([d0 * a, d1 * a, (d1 - tt) * a + nrm * tt, (d0 + tt) * a + nrm * tt])
        if cand.intersection(body).area < 1e-6: seam = (cand, d0, d1); break
    assert seam is not None, 'no room for the seam tab'
    folds.append(('valley' if ty['psi'][0] < math.pi else 'mountain', seam[1] * a, seam[2] * a, f"{math.degrees(ty['psi'][0]):.1f}°"))
    labels.append(('seam', (seam[1] + seam[2]) / 2 * a + nrm * min(SEAM_T, 0.3 * (seam[2] - seam[1])) / 2,
                   math.degrees(math.atan2(a[1], a[0])), 'glue under 1', None))
    pieces = tris + rim + [seam[0]]
    for i in range(len(pieces)):
        for k in range(i + 1, len(pieces)):
            assert pieces[i].intersection(pieces[k]).area < 1e-6, ('overlap', NAME, ty['name'], i, k)
    outline = unary_union([Polygon(np.vstack([O, P]))] + [p.buffer(1e-5, join_style=2) for p in rim + [seam[0]]]).buffer(-1e-5, join_style=2)
    outline = outline.simplify(1e-6); assert outline.geom_type == 'Polygon', 'net not in one piece'
    for j, t0 in enumerate(ty['tri']):
        c = (O + P[j] + P[j + 1]) / 3 * 0.55 + (P[j] + P[j + 1]) / 2 * 0.45
        labels.append(('tri', c, None, (t0['fin'], T[t0['nbr_type']]['name'], j == 0, t0['disc']), tris[j]))
        labels.append(('strut', P[j] * (1 - min(0.12, 9.0 / np.linalg.norm(P[j]))), None, str(t0['strut_a']), None))
    return dict(outline=outline, folds=folds, labels=labels, P=P)
def best_angle(poly):
    best = None
    for ang in np.arange(0, 180, 0.5):
        q = affinity.rotate(poly, ang, origin=(0, 0)); x0, y0, x1, y1 = q.bounds; w, h = x1 - x0, y1 - y0
        sc = min(W / w, H / h)
        if best is None or sc > best[0]: best = (sc, ang, w, h)
    return best
# scale: the largest net (fan + tab allowance) fits the printable area; then rounded down so the longest strut is whole mm
s = 1e9
for ty in T:
    P, _ = fan_points(ty); poly = Polygon(np.vstack([[0, 0], P])).convex_hull
    for ang in np.arange(0, 180, 0.5):
        q = affinity.rotate(poly, ang, origin=(0, 0)); x0, y0, x1, y1 = q.bounds
        pass
    sc = max(min((W - 2 * RIM_T - 2) / (q.bounds[2] - q.bounds[0]), (H - 2 * RIM_T - 2) / (q.bounds[3] - q.bounds[1]))
             for q in (affinity.rotate(poly, a_, origin=(0, 0)) for a_ in np.arange(0, 180, 0.5)))
    s = min(s, sc)
Lmax = math.floor(s * r['R'])
while True:
    s = Lmax / r['R']; nets = [build(ty, s) for ty in T]; fits = [best_angle(n['outline']) for n in nets]
    if all(f[0] >= 1 for f in fits): break
    Lmax -= 1
EDGE_MM = sorted({round(f['AB'] * s, 1) for f in r['fins']}); STRUT_MM = [(st['no'], st['L'] * s) for st in r['struts']]
# copies per page
layout = []
for ty, net, fit in zip(T, nets, fits):
    q = affinity.rotate(net['outline'], fit[1], origin=(0, 0)); x0, y0, x1, y1 = q.bounds; w, h = x1 - x0, y1 - y0
    cols, rows = int((W + GAP) // (w + GAP)), int((H + GAP) // (h + GAP)); cp = max(1, cols * rows)
    layout.append(dict(ang=fit[1], w=w, h=h, cols=max(cols, 1), rows=max(rows, 1), cp=cp, pages=math.ceil(ty['count'] / cp), off=(-x0, -y0)))
NPAGES = 1 + sum(l['pages'] for l in layout)
DASH = {'valley': (0, (3.2, 1.6)), 'mountain': (0, (4.5, 1.3, 0.8, 1.3))}
def page_frame(fig, ax, pno, sub):
    ax.set_xlim(0, PW); ax.set_ylim(0, PH); ax.set_aspect('equal'); ax.axis('off')
    ax.text(X0, PH - 10, f'DICTO Vacuus origami · {SHORT}', fontsize=11, fontweight='bold', va='center')
    ax.text(X0, PH - 16, sub, fontsize=7.5, va='center', color='#333')
    lh = 12; lw = lh * LOGO_IM.shape[1] / LOGO_IM.shape[0]; ax.imshow(LOGO_IM, extent=(X1 - lw, X1, PH - 19.5, PH - 19.5 + lh), zorder=5)
    # footer: legend, scale bar, mark
    y = 13.5
    for i, (nm, ls) in enumerate([('cut', '-'), ('valley fold', DASH['valley']), ('mountain fold', DASH['mountain'])]):
        x = X0 + i * 33; ax.plot([x, x + 9], [y, y], color='#7a3b00' if nm == 'mountain fold' else 'k', lw=0.8 if nm == 'cut' else 0.6, ls=ls); ax.text(x + 10.5, y, nm, fontsize=6.3, va='center')
    ax.plot([X0 + 103, X0 + 153], [y, y], color='k', lw=1.0); [ax.plot([x, x], [y - 1.2, y + 1.2], color='k', lw=0.8) for x in (X0 + 103, X0 + 153)]
    ax.text(X0 + 128, y + 2.4, '50 mm: print at 100 % (no "fit to page")', fontsize=5.6, ha='center')
    ax.text(X0, 6.5, f'DICTO · dictospheres.com · Vacuus origami, DICTO proposed 2026-11-02 · printed side = inside of the open pyramid · CC BY-SA 4.0',
            fontsize=5.6, color='#444', va='center')
    ax.text(X1, 6.5, f'{pno} / {NPAGES}', fontsize=6.5, ha='right', va='center')
def draw_net(ax, net, ang, off, tag):
    rot = lambda p: np.array(affinity.rotate(LineString([(0, 0), tuple(p)]), ang, origin=(0, 0)).coords[1]) + off
    o = affinity.translate(affinity.rotate(net['outline'], ang, origin=(0, 0)), *off)
    x, y = o.exterior.xy; ax.plot(x, y, color='k', lw=0.75, solid_joinstyle='miter')
    ax.fill(x, y, color='#fbfaf6', zorder=0)
    for kind, a, b, lab in net['folds']:
        A, B = rot(a), rot(b); ax.plot([A[0], B[0]], [A[1], B[1]], color='#222' if kind == 'valley' else '#7a3b00', lw=0.55, ls=DASH[kind])
        if lab:
            M = A + 0.42 * (B - A); d = (B - A) / np.linalg.norm(B - A); deg = math.degrees(math.atan2(d[1], d[0]))
            if deg > 90 or deg < -90: deg += 180
            nn = np.array([-d[1], d[0]]); ax.text(*(M + nn * 1.6), 'ψ ' + lab, fontsize=5.2, rotation=deg, ha='center', va='center', color='#333', rotation_mode='anchor')
    for kind, c, deg, txt, extra in net['labels']:
        C = rot(c)
        if kind == 'tri':
            fl, nb, first, disc = txt; area = extra.area; fs = max(7, min(20, math.sqrt(area) / 3.2))
            ax.text(C[0], C[1] + fs * 0.12, fl + ('  1' if first else ''), fontsize=fs, ha='center', va='center', fontweight='bold', color='#1d1d24')
            ax.text(C[0], C[1] - fs * 0.30, f'back to back with {nb}' + ('\ncentral disc' if disc else ''), fontsize=max(4.6, fs * 0.30), ha='center', va='top', color='#444')
        elif kind == 'strut':
            ax.text(C[0], C[1], txt, fontsize=5.2, ha='center', va='center', color='#2b5fa8',
                    bbox=dict(boxstyle='circle,pad=0.18', fc='white', ec='#2b5fa8', lw=0.4))
        elif kind == 'tab':
            if extra < 2.4: continue
            dd = deg + ang
            while dd > 90: dd -= 180
            while dd < -90: dd += 180
            ax.text(C[0], C[1], txt, fontsize=min(5.2, extra * 1.15), ha='center', va='center', rotation=dd, rotation_mode='anchor', color='#7a3b00')
        elif kind == 'seam':
            dd = deg + ang
            while dd > 90: dd -= 180
            while dd < -90: dd += 180
            ax.text(C[0], C[1], txt, fontsize=4.8, ha='center', va='center', rotation=dd, rotation_mode='anchor', color='#333')
    bx = o.bounds; ax.text(bx[0], bx[3] + 1.2, tag, fontsize=6.4, fontweight='bold', color='#7a5c00')
def guide(pdf):
    fig = plt.figure(figsize=(PW / 25.4, PH / 25.4)); ax = fig.add_axes([0, 0, 1, 1]); page_frame(fig, ax, 1, 'Assembly guide · read first')
    y = PH - 24
    if RENDER != '-':
        im = np.asarray(Image.open(RENDER).convert('RGB')); hh = 88; ww = hh * im.shape[1] / im.shape[0]
        if ww > W: ww = W; hh = ww * im.shape[0] / im.shape[1]
        ax.imshow(im, extent=(X0 + (W - ww) / 2, X0 + (W - ww) / 2 + ww, y - hh, y)); y -= hh + 3
        ax.text(X0 + W / 2, y, 'Left: the folded Vacuus (every fin a double wall). Right: exploded, each open pyramid pulled out along its axis.',
                fontsize=6.3, ha='center', color='#333'); y -= 6
    D = 2 * max(st['L'] for st in r['struts']) * s
    lines = [('b', f'{r["F"]} open pyramids (one per face), {sum(len(t["tri"]) * t["count"] for t in T)} paper triangles, {r["E"]} double-walled fins, '
                   f'{r["V"]} struts. Scale: longest strut {Lmax} mm; rim edges {", ".join(f"{e:g}" for e in EDGE_MM)} mm; finished size ≤ {D:.0f} mm across.')]
    lines.append(('h', 'Nets to print (this file holds every copy: print all pages once, 100 %)'))
    for ty, lo in zip(T, layout):
        fins = ''.join(t['fin'] for t in ty['tri']); nb = sorted({T[t['nbr_type']]['name'] for t in ty['tri']})
        lines.append(('t', f'{ty["name"]}: {ty["face"]} face, {ty["count"]} copies on {lo["pages"]} page(s); fan of {ty["sides"]} triangles (fins {fins}), '
                           f'fan angle {ty["fan_sum_deg"]:.2f}° < 360°; folds ψ = {", ".join(f"{math.degrees(p):.1f}°" for p in ty["psi"])}; neighbours {", ".join(nb)}.'))
    lines.append(('h', 'Lines, labels and the tab rule'))
    for t_ in ['Cut on solid lines. Valley folds (dashed) fold towards you, mountain folds (dash-dot) away, seen from the printed side. '
               'The printed side is the inside of the open pyramid: after assembly you look into it through the open face.',
               'ψ on a fold is the angle between the two triangles once folded (the dihedral inside the pyramid at that strut).',
               'Big letter = the fin (triangles with the same letter are congruent). "back to back with N2" = the neighbouring pyramid that '
               'shares this fin; its triangle carries the same letter. Blue circled numbers = strut class at that rim corner (1 = longest).',
               'Tab rule: each triangle has one half-tab on the rim half next to its leading corner (counter-clockwise on the printed side). '
               'The neighbour runs the same edge the other way, so its half-tab covers the other half: every rim gets two half-tabs, one '
               'from each pyramid. "→ N2 b": fold 180° over the double rim and glue onto the printed side of fin b of the neighbour N2.',
               'Seam tab: glue it under triangle 1 (the one marked "1"); this closes the fan into an open pyramid.']:
        lines.append(('p', t_))
    lines.append(('h', 'Assembly'))
    steps = ['Fold every net and close it with its seam tab. Check one pyramid against the ψ values before folding the rest.',
             'Optional: snip 2 mm off every apex tip, so that the tips can all meet at the centre without bunching.',
             'Glue two neighbouring pyramids back to back along one fin: glue stick over the whole back of the triangle, the same letter '
             'on both sides, apices together. This is one double wall.',
             'Grow the cluster round one strut first: all pyramids that share a corner, fin to fin, closing the ring. Then add rings '
             'round the next corners. The apices all nest at the centre O; the open faces point outwards.',
             'Last, fold every rim half-tab over the double rims and glue it to the neighbour\'s printed side. The last pyramid goes in '
             'with glue on all its fin backs at once; its rim tabs lock it.']
    if NAME == 'Kagemusha':
        steps.append('Kagemusha central pentagon: the five fins marked "central disc" lie in one plane through O and make one flat regular '
                     'pentagon of five 72° fins (double walls, see the diagram below). Build the five pyramids on one side of it first, '
                     'check that the five disc fins lie flat, then add the five on the other side.')
    if r['disc_fins'] and NAME != 'Kagemusha':
        steps.append(f'Central discs: the fins marked "central disc" lie in planes through O and join into flat central polygons '
                     f'({len(r["disc_fins"])} fins). Keep them flat while gluing.')
    for i, t_ in enumerate(steps): lines.append(('p', f'{i + 1}. {t_}'))
    for kind, t_ in lines:
        if kind == 'h': y -= 2; ax.text(X0, y, t_, fontsize=8.2, fontweight='bold', va='top'); y -= 4.6; continue
        wrap = textwrap.wrap(t_, 128 if kind != 'b' else 118)
        for ln in wrap: ax.text(X0 + (3 if kind == 't' else 0), y, ln, fontsize=6.6 if kind != 'b' else 7.0, va='top', fontweight='bold' if kind == 'b' else None); y -= 3.15
        y -= 0.9
    if NAME == 'Kagemusha': disc_diagram(ax, y)
    pdf.savefig(fig); plt.close(fig); return y
def disc_diagram(ax, ytop):
    """Kagemusha: the central pentagon disc seen face on, five fins, with the pyramids above and below"""
    V = np.array(r['points']); ed = [tuple(e) for e in r['disc_fins']]
    n = np.cross(V[ed[0][0]], V[ed[0][1]]); n /= np.linalg.norm(n); e1 = V[ed[0][0]] - (V[ed[0][0]] @ n) * n; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    size = min(ytop - 26, 52); sc = size / 2 / max(np.linalg.norm(V[v]) for e in ed for v in e); cx, cy = X0 + W / 2, ytop - size / 2 - 2
    pr = lambda p: np.array([cx + sc * (p @ e1), cy + sc * (p @ e2)])
    fins = {f['letter']: f for f in r['fins']}
    for a, b in ed:
        A, B = pr(V[a]), pr(V[b]); O = np.array([cx, cy]); ax.fill([O[0], A[0], B[0]], [O[1], A[1], B[1]], color='#f4f1e6', ec='k', lw=0.6)
        # pyramids on the two sides of this fin
        sides = []
        for fc in r['faces']:
            cs = fc['corners']; m = len(cs)
            if any({cs[k], cs[(k + 1) % m]} == {a, b} for k in range(m)):
                cen = V[cs].mean(0); sides.append(('above' if cen @ n > 0 else 'below', T[fc['type']]['name']))
        M = (O + A + B) / 3; ax.text(*M, 'disc', fontsize=5.5, ha='center', va='center')
        M2 = O + 1.34 * ((A + B) / 2 - O); ax.text(*M2, ' / '.join(f'{nm} {sd}' for sd, nm in sorted(sides)), fontsize=5.2, ha='center', va='center', color='#444')
    ax.text(cx, cy - size / 2 - 6.5, 'The Kagemusha central pentagon disc, face on: five fins of apex 72° (exact) in one plane through O. '
            'Each is a double wall between a pyramid above and one below.', fontsize=6.0, ha='center', color='#333')
with PdfPages(OUT) as pdf:
    guide(pdf); pno = 1
    for ty, net, lo in zip(T, nets, layout):
        done = 0
        for pg in range(lo['pages']):
            pno += 1; fig = plt.figure(figsize=(PW / 25.4, PH / 25.4)); ax = fig.add_axes([0, 0, 1, 1])
            k = min(lo['cp'], ty['count'] - done)
            page_frame(fig, ax, pno, f'{ty["name"]}: {ty["face"]} face, open pyramid, {ty["count"]} needed · fold ψ and tabs as labelled · '
                                     f'longest strut {Lmax} mm')
            for i in range(k):
                cx, cy = i % lo['cols'], i // lo['cols']
                gw = lo['cols'] * lo['w'] + (lo['cols'] - 1) * GAP; gh = min(lo['rows'], math.ceil(k / lo['cols'])) * lo['h'] + (min(lo['rows'], math.ceil(k / lo['cols'])) - 1) * GAP
                ox = X0 + (W - gw) / 2 + cx * (lo['w'] + GAP) + lo['off'][0]; oy = Y1 - (H - gh) / 2 - (cy + 1) * lo['h'] - cy * GAP + lo['off'][1]
                draw_net(ax, net, lo['ang'], np.array([ox, oy]), f'{ty["name"]} · copy {done + i + 1} of {ty["count"]}')
            done += k; pdf.savefig(fig); plt.close(fig)
    d = pdf.infodict(); d['Title'] = f'DICTO Vacuus origami nets: {SHORT}'; d['Author'] = 'DICTO'; d['Subject'] = 'Vacuus origami, DICTO proposed 2026-11-02'
info = dict(name=NAME, scale_mm_per_unit=s, longest_strut_mm=Lmax, edges_mm=EDGE_MM, struts_mm=STRUT_MM, pages=NPAGES,
            layout=[dict(type=t['name'], count=t['count'], per_page=l['cp'], pages=l['pages'], w=l['w'], h=l['h']) for t, l in zip(T, layout)])
json.dump(info, open(OUT[:-4] + '.json', 'w'), indent=1); print(json.dumps(info))
