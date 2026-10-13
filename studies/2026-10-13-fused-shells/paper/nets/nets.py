# Cut-out-and-glue paper nets for DICTO Transitional Shells (paper "Capturing the In-betweens", DICTO, 2026-10-13).
# Input: the fused solids of krp-core transitional.js (the same shapes as Polyhedraverse's group), passed as trans.json.
# Each solid is unfolded into as few pieces as fit an A4 page (greedy, compact), checked for overlaps (faces and tabs),
# glue tabs numbered in pairs, folds marked mountain (dashed) or valley (dash-dot) from the 3D dihedral, then packed onto
# A4 pages as SVG. Writes nets.html (print with print_pdf.mjs) and nets-checks.json. Run on dicto-node (shapely).
# DICTO · dictospheres.com
import json, math, sys, os, itertools
import numpy as np
from shapely.geometry import Polygon, box
from shapely import affinity
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'trans.json')))
PAGE_W, PAGE_H, MARGIN, HEAD = 210.0, 297.0, 12.0, 30.0
AREA_W, AREA_H = PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN - HEAD - 8
EPS = 1e-6
CHOSEN = [  # id, title, mm per unit, what it is
    ('TRANS_LOTUS_2', 'Lotus seed, stage 2', 44, 'Icosahedron + 20 CLEO, fused: the great stellated dodecahedron (Kepler 1619) as a solid: 60 golden triangles, 32 corners.'),
    ('TRANS_LOTUS_3', 'Lotus seed, stage 3', 40, '+ 30 AXE: the excavated dodecahedron (Coxeter et al. 1938, Ef1g1): 60 equilateral triangles on the same 32 corners.'),
    ('TRANS_BODHI_B2', 'Bodhi Seed Kit B, stage 2', 30, 'Triacontahedron + 60 Vajra (fine), fused: the rhombic hexecontahedron (Unkelbach 1940): 60 golden rhombi.'),
    ('TRANS_DHARMA_80', 'Spheres of Dharma, the 80-corner stage', 46, 'Convex: 12 regular pentagons, 30 rhombi, 60 isosceles triangles; the hull of the truncated icosahedron and a dodecahedron.'),
]


def frame(P3, n):
    u = P3[1] - P3[0]; u /= np.linalg.norm(u); v = np.cross(n, u)
    return np.array([[(p - P3[0]) @ u, (p - P3[0]) @ v] for p in P3])


def unfold(V, F, scale, forced_cuts=None):
    V = np.array(V, float) * scale; V -= V.mean(0)
    nF = len(F)
    normals, local = [], []
    for f in F:
        P3 = V[f]; c = P3.mean(0); n = np.zeros(3)
        for i in range(len(f)): n += np.cross(P3[i] - c, P3[(i + 1) % len(f)] - c)
        n /= np.linalg.norm(n); normals.append(n); local.append(frame(P3, n))
    edges = {}
    for fi, f in enumerate(F):
        for i in range(len(f)):
            edges.setdefault(tuple(sorted((f[i], f[(i + 1) % len(f)]))), []).append(fi)
    assert all(len(x) == 2 for x in edges.values()), 'not closed'
    # convex (mountain) or reflex (valley) per edge
    kind = {}
    for e, (f1, f2) in edges.items():
        c2 = V[F[f2]].mean(0)
        kind[e] = 'mountain' if normals[f1] @ (c2 - V[e[0]]) < -1e-9 else ('valley' if normals[f1] @ (c2 - V[e[0]]) > 1e-9 else 'flat')
    vfaces = {}
    for fi, f in enumerate(F):
        for v in f: vfaces.setdefault(v, set()).add(fi)
    defect = {}
    for v, fs in vfaces.items():
        tot = 0.0
        for fi in fs:
            f = F[fi]; i = f.index(v); a, b = V[f[i - 1]] - V[v], V[f[(i + 1) % len(f)]] - V[v]
            tot += math.acos(np.clip(a @ b / np.linalg.norm(a) / np.linalg.norm(b), -1, 1))
        defect[v] = math.degrees(2 * math.pi - tot)
    placed = {}  # face -> (piece, 2D coords array aligned with F[face])
    pieces = []
    unplaced = set(range(nF))

    def place_across(fi, gi, e):
        """2D coords of face gi unfolded across edge e from placed face fi."""
        a, b = e
        Pf = placed[fi][1]; f = F[fi]; g = F[gi]
        A2, B2 = Pf[f.index(a)], Pf[f.index(b)]
        L = local[gi]; a_l, b_l = L[g.index(a)], L[g.index(b)]
        ang = math.atan2(*(B2 - A2)[::-1]) - math.atan2(*(b_l - a_l)[::-1])
        R = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
        Q = (L - a_l) @ R.T + A2
        return Q

    def fits(polys):
        U = unary_union(polys)
        best = None
        for t in range(0, 180, 6):
            r = affinity.rotate(U, t, origin='centroid')
            x0, y0, x1, y1 = r.bounds
            w, h = x1 - x0, y1 - y0
            if (w <= AREA_W - 16 and h <= AREA_H - 16) or (h <= AREA_W - 16 and w <= AREA_H - 16):
                return True
        return False

    while unplaced:
        root = min(unplaced)
        pid = len(pieces); placed[root] = (pid, local[root].copy()); unplaced.discard(root)
        polys = {root: Polygon(placed[root][1])}
        piece = [root]
        while True:
            cands = []
            for fi in piece:
                for i in range(len(F[fi])):
                    e = tuple(sorted((F[fi][i], F[fi][(i + 1) % len(F[fi])])))
                    gi = [x for x in edges[e] if x != fi][0]
                    if gi in unplaced and not (forced_cuts and e in forced_cuts): cands.append((fi, gi, e))
            if not cands: break
            cen = np.mean([np.array(p.centroid.coords[0]) for p in polys.values()], axis=0)
            scored = []
            for fi, gi, e in cands:
                Q = place_across(fi, gi, e)
                scored.append((np.linalg.norm(Q.mean(0) - cen), fi, gi, e, Q))
            scored.sort(key=lambda s: s[0])
            added = False
            for _, fi, gi, e, Q in scored:
                pg = Polygon(Q)
                inpiece = set(piece) | {gi}
                # never close the ring of faces round a corner: the leftover slit (the angle defect) is too narrow for a tab
                if not forced_cuts and any(vfaces[v] <= inpiece and 0 < defect[v] < 40 for v in F[gi]): continue
                if any(pg.intersection(p).area > 1e-9 * scale * scale for p in polys.values()): continue
                if not fits(list(polys.values()) + [pg]): continue
                placed[gi] = (pid, Q); polys[gi] = pg; piece.append(gi); unplaced.discard(gi)
                placed[gi] = (pid, Q, fi, e) if False else (pid, Q)
                added = True; break
            if not added: break
        pieces.append(piece)
    # folds: an edge whose two faces are in one piece and whose 2D copies coincide
    folds, cuts = [], []
    for e, (f1, f2) in edges.items():
        p1, Q1 = placed[f1]; p2, Q2 = placed[f2]
        if p1 == p2:
            a1, b1 = Q1[F[f1].index(e[0])], Q1[F[f1].index(e[1])]
            a2, b2 = Q2[F[f2].index(e[0])], Q2[F[f2].index(e[1])]
            if np.linalg.norm(a1 - a2) < 1e-6 and np.linalg.norm(b1 - b2) < 1e-6:
                folds.append((e, p1, a1, b1)); continue
        cuts.append((e, f1, f2))
    return V, F, edges, kind, placed, pieces, folds, cuts


def steepest_unfold(Vraw, Fraw, scale, tries=120, seed=7):
    """Steepest-edge cut tree (convex solids): for a direction d, every corner but the top cuts its steepest upward edge;
    all other edges fold. Tries random d until the one-piece net has no overlap."""
    V = np.array(Vraw, float) * scale; V -= V.mean(0); F = [list(f) for f in Fraw]
    edges = {}
    for fi, f in enumerate(F):
        for i in range(len(f)): edges.setdefault(tuple(sorted((f[i], f[(i + 1) % len(f)]))), []).append(fi)
    nbr = {}
    for a, b in edges: nbr.setdefault(a, []).append(b); nbr.setdefault(b, []).append(a)
    rng = np.random.default_rng(seed); best = None
    for t in range(tries):
        d = rng.normal(size=3); d /= np.linalg.norm(d)
        top = int(np.argmax(V @ d)); cut = set()
        for v in range(len(V)):
            if v == top: continue
            w = max(nbr[v], key=lambda u: (V[u] - V[v]) @ d / np.linalg.norm(V[u] - V[v]))
            cut.add(tuple(sorted((v, w))))
        res = unfold(Vraw, Fraw, scale, forced_cuts=cut)
        if best is None or len(res[5]) < len(best[5]): best = res
        if len(res[5]) <= 2: break
    return best


def tab_poly(a, b, inside_pt, h):
    d = b - a; L = np.linalg.norm(d); t = d / L; n = np.array([-t[1], t[0]])
    if n @ (inside_pt - a) > 0: n = -n
    ins = min(h / math.tan(math.radians(45)), 0.3 * L)
    return Polygon([a, b, b + n * h - t * ins, a + n * h + t * ins])


def build(sid, title, scale, note):
    res = steepest_unfold(RAW[sid]['vertices'], RAW[sid]['faces'], scale) if sid == 'TRANS_DHARMA_80' else None
    if res is None: res = unfold(RAW[sid]['vertices'], RAW[sid]['faces'], scale)
    V, F, edges, kind, placed, pieces, folds, cuts = res
    piece_polys = {p: {fi: Polygon(placed[fi][1]) for fi in fl} for p, fl in enumerate(pieces)}
    tabs, labels, notab = {p: [] for p in range(len(pieces))}, [], []
    for k, (e, f1, f2) in enumerate(cuts, 1):
        L = np.linalg.norm(V[e[0]] - V[e[1]])
        done = False
        best = None
        for h in (min(7.0, 0.42 * L), min(4.0, 0.3 * L), 2.5):
            for (fa, fb) in ((f1, f2), (f2, f1)):
                p, Q = placed[fa]; f = F[fa]
                a, b = Q[f.index(e[0])], Q[f.index(e[1])]
                tp = tab_poly(a, b, Q.mean(0), h)
                block = unary_union(list(piece_polys[p].values()) + [t for t, _ in tabs[p]]).buffer(0.4, join_style=2)
                clipped = tp.difference(block)
                if clipped.geom_type != 'Polygon':
                    parts = [g for g in getattr(clipped, 'geoms', []) if g.geom_type == 'Polygon']
                    clipped = max(parts, key=lambda g: g.area) if parts else Polygon()
                if clipped.is_empty: continue
                from shapely.geometry import LineString
                along = clipped.buffer(0.45).intersection(LineString([a, b])).length / L
                score = clipped.area / tp.area * min(1.0, along / 0.6)
                if along >= 0.45 and clipped.area >= 0.25 * tp.area and (best is None or score > best[0]):
                    best = (score, p, clipped)
            if best is not None: break
        if best is not None:
            tabs[best[1]].append((best[2], k)); done = True
        if not done: notab.append(k)
        for fa in (f1, f2):
            p, Q = placed[fa]; f = F[fa]
            a, b = Q[f.index(e[0])], Q[f.index(e[1])]
            m = (a + b) / 2; inward = Q.mean(0) - m; inward /= np.linalg.norm(inward)
            labels.append((p, m + inward * 3.2, k, math.degrees(math.atan2(*(b - a)[::-1]))))
    # checks
    chk = {}
    chk['faces'] = len(F); chk['facesPlaced'] = sum(len(p) for p in pieces); chk['pieces'] = len(pieces)
    worst = 0.0
    for fi, f in enumerate(F):
        Q = placed[fi][1]
        for i in range(len(f)):
            worst = max(worst, abs(np.linalg.norm(Q[i] - Q[(i + 1) % len(f)]) - np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])))
        # angles too (congruence, not just side lengths)
        for i in range(len(f)):
            u3, w3 = V[f[i - 1]] - V[f[i]], V[f[(i + 1) % len(f)]] - V[f[i]]
            u2, w2 = Q[i - 1] - Q[i], Q[(i + 1) % len(f)] - Q[i]
            worst = max(worst, abs(math.acos(np.clip(u3 @ w3 / np.linalg.norm(u3) / np.linalg.norm(w3), -1, 1)) - math.acos(np.clip(u2 @ w2 / np.linalg.norm(u2) / np.linalg.norm(w2), -1, 1))) * 10)
    chk['worstCongruenceErrorMm'] = worst
    chk['edges'] = len(edges); chk['folds'] = len(folds); chk['cutPairs'] = len(cuts)
    chk['everyEdgeFoldOrPair'] = len(folds) + len(cuts) == len(edges)
    ov = 0.0
    for p, polys in piece_polys.items():
        items = list(polys.values()) + [t for t, _ in tabs[p]]
        for x, y in itertools.combinations(items, 2): ov = max(ov, x.intersection(y).area)
    chk['worstOverlapMm2'] = ov
    chk['tabsMissing'] = notab
    chk['valleyFolds'] = sum(1 for e, *_ in folds if kind[e] == 'valley'); chk['mountainFolds'] = sum(1 for e, *_ in folds if kind[e] == 'mountain')
    chk['valleyCuts'] = sum(1 for e, *_ in cuts if kind[e] == 'valley')
    chk['ok'] = chk['facesPlaced'] == chk['faces'] and chk['everyEdgeFoldOrPair'] and ov < 1e-6 and worst < 1e-6 and not notab
    return dict(sid=sid, title=title, scale=scale, note=note, F=F, placed=placed, pieces=pieces, folds=folds, kind=kind,
                tabs=tabs, labels=labels, piece_polys=piece_polys, checks=chk, colours=RAW[sid].get('faceColours'))


def layout(net):
    """Rotate each piece to its smallest bounding box and give it a translation; returns per-piece transforms."""
    out = []
    for p in range(len(net['pieces'])):
        items = list(net['piece_polys'][p].values()) + [t for t, _ in net['tabs'][p]]
        U = unary_union(items)
        best = None
        for t in range(0, 180, 3):
            r = affinity.rotate(U, t, origin=(0, 0)); x0, y0, x1, y1 = r.bounds
            w, h = x1 - x0, y1 - y0
            fit = (w <= AREA_W and h <= AREA_H) or (h <= AREA_W and w <= AREA_H)
            key = (0 if fit else 1, w * h)
            if best is None or key < best[0]: best = (key, t, x0, y0, w, h)
        _, t, x0, y0, w, h = best
        if w > AREA_W or h > AREA_H: t += 90; r = affinity.rotate(U, t, origin=(0, 0)); x0, y0, x1, y1 = r.bounds; w, h = x1 - x0, y1 - y0
        assert w <= AREA_W + 1e-6 and h <= AREA_H + 1e-6, 'piece larger than the page'
        out.append(dict(rot=t, x0=x0, y0=y0, w=w, h=h, U=U))
    return out


def svg_pages(nets):
    """Nest each net's pieces onto A4 pages: largest first, bottom-left, 4 turns, 2.5 mm gaps (shapely collision tests)."""
    from shapely.prepared import prep
    pages = []
    for net in nets:
        L = layout(net); net['layout'] = L
        order = sorted(range(len(L)), key=lambda i: -L[i]['U'].area)
        npages = []  # [(items, occupied geometry)]
        for i in order:
            T = L[i]; done = False
            for turn in (0, 90, 180, 270):
                G = affinity.rotate(T['U'], T['rot'] + turn, origin=(0, 0))
                x0, y0, x1, y1 = G.bounds; w, h = x1 - x0, y1 - y0
                if w > AREA_W or h > AREA_H: continue
                Gb = affinity.translate(G, -x0, -y0).buffer(1.25)
                for pg in npages:
                    occ = prep(pg[1]) if not pg[1].is_empty else None
                    for yy in np.arange(0, AREA_H - h + 1e-9, 3.0):
                        for xx in np.arange(0, AREA_W - w + 1e-9, 3.0):
                            cand = affinity.translate(Gb, xx, yy)
                            if occ is None or not occ.intersects(cand):
                                pg[0].append((i, turn, xx, yy)); pg[1] = pg[1].union(cand); done = True; break
                        if done: break
                    if done: break
                if done: break
            if not done:
                turn = 0
                G = affinity.rotate(T['U'], T['rot'] + turn, origin=(0, 0)); x0, y0, x1, y1 = G.bounds
                npages.append([[(i, turn, 0.0, 0.0)], affinity.translate(G, -x0, -y0).buffer(1.25)])
        for items, _ in npages: pages.append((net, items))
    svgs = []
    total = len(pages)
    for pno, (net, items) in enumerate(pages, 1):
        L = net['layout']
        g = []
        placed_boxes = []
        for i, turn, ox, oy in items:
            T = L[i]; rot = T['rot'] + turn
            G = affinity.rotate(T['U'], rot, origin=(0, 0)); gx0, gy0, gx1, gy1 = G.bounds
            tx, ty = MARGIN + ox - gx0, MARGIN + HEAD + oy - gy0
            placed_boxes.append(affinity.translate(G, tx, ty))
            ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            tf = lambda q: (q[0] * ca - q[1] * sa + tx, q[0] * sa + q[1] * ca + ty)
            pts = lambda poly: ' '.join(f'{a:.2f},{b:.2f}' for a, b in (tf(c) for c in list(poly.exterior.coords)[:-1]))
            for t, k in net['tabs'][i]:
                g.append(f'<polygon points="{pts(t)}" fill="#eef1f4" stroke="#222" stroke-width="0.25"/>')
            for fi in net['pieces'][i]:
                col = net['colours'][fi] if net['colours'] else 0xdddddd
                hexc = '#%06x' % col
                g.append(f'<polygon points="{pts(net["piece_polys"][i][fi])}" fill="{hexc}" fill-opacity="0.28" stroke="#222" stroke-width="0.3"/>')
            for e, p, a, b in net['folds']:
                if p != i: continue
                (x1, y1), (x2, y2) = tf(a), tf(b)
                dash = '2.2,1.2' if net['kind'][e] == 'mountain' else '3,1,0.6,1'
                colr = '#1b4fa0' if net['kind'][e] == 'mountain' else '#b3261e'
                g.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{colr}" stroke-width="0.35" stroke-dasharray="{dash}"/>')
            for p, m, k, ang in net['labels']:
                if p != i: continue
                X, Y = tf(m)
                g.append(f'<text x="{X:.2f}" y="{Y:.2f}" font-size="2.6" text-anchor="middle" dominant-baseline="middle" transform="rotate({ang + rot:.1f} {X:.2f} {Y:.2f})">{k}</text>')
            cx, cy = tf(np.array(net['piece_polys'][i][net['pieces'][i][0]].centroid.coords[0]))
            g.append(f'<text x="{cx:.2f}" y="{cy:.2f}" font-size="4" font-weight="700" fill="#555" text-anchor="middle" dominant-baseline="middle">{chr(65 + i)}</text>')
        # pieces must not overlap on the page
        for a, b in itertools.combinations(placed_boxes, 2):
            assert a.intersection(b).area < 1e-6, 'page overlap'
        for a in placed_boxes:
            x0, y0, x1, y1 = a.bounds
            assert x0 >= MARGIN - 1e-6 and y0 >= MARGIN + HEAD - 1e-6 and x1 <= PAGE_W - MARGIN + 1e-6 and y1 <= PAGE_H - MARGIN - 8 + 1e-6, 'off page'
        c = net['checks']
        head = (f'<text x="{MARGIN}" y="{MARGIN + 6}" font-size="6" font-weight="700">{net["title"]}</text>'
                f'<text x="{MARGIN}" y="{MARGIN + 12}" font-size="3.1">{net["note"]}</text>'
                f'<text x="{MARGIN}" y="{MARGIN + 17}" font-size="3.1">Cut on solid lines. Fold: <tspan fill="#1b4fa0">dashed = mountain</tspan> (crease away from you), '
                f'<tspan fill="#b3261e">dash-dot = valley</tspan> (crease towards you); printed side out.</text>'
                f'<text x="{MARGIN}" y="{MARGIN + 21.5}" font-size="3.1">Glue each grey tab under the edge with the same number. Pieces are lettered A, B, ...</text>'
                f'<text x="{MARGIN}" y="{MARGIN + 26}" font-size="3.1">{c["faces"]} faces in {c["pieces"]} piece{"s" if c["pieces"] > 1 else ""} ({", ".join(chr(65 + j) for j in range(c["pieces"]))}); '
                f'{c["cutPairs"]} glue pairs; scale {net["scale"]} mm per unit. Checked: no overlaps, every edge folded or paired.</text>')
        foot = (f'<text x="{MARGIN}" y="{PAGE_H - 7}" font-size="3">DICTO · dictospheres.com · Capturing the In-betweens: cut-out nets, draft 2026-10-13</text>'
                f'<text x="{PAGE_W - MARGIN}" y="{PAGE_H - 7}" font-size="3" text-anchor="end">page {pno} / {total}</text>')
        svgs.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297" font-family="Noto Sans, DejaVu Sans, sans-serif">{head}{"".join(g)}{foot}</svg>')
    return svgs


if __name__ == '__main__':
    nets, report = [], {}
    for sid, title, scale, note in CHOSEN:
        n = build(sid, title, scale, note); nets.append(n); report[sid] = n['checks']
        print(sid, json.dumps(n['checks']), flush=True)
    svgs = svg_pages(nets)
    html = ('<!doctype html><html><head><meta charset="utf-8"><title>Transitional shells: cut-out nets (DICTO)</title>'
            '<style>@page{size:A4;margin:0}body{margin:0}svg{display:block;page-break-after:always}</style></head><body>'
            + ''.join(svgs) + '</body></html>')
    open(os.path.join(HERE, 'nets.html'), 'w').write(html)
    json.dump({'credit': 'DICTO · dictospheres.com', 'pages': len(svgs), 'nets': report}, open(os.path.join(HERE, 'nets-checks.json'), 'w'), indent=1)
    print('pages', len(svgs))
