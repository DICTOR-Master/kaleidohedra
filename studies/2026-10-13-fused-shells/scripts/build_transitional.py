# DICTO Transitional Shells for Polyhedraverse (DICTO 2026-10-13: each stage as ONE fused solid, coloured as in the app's views;
# the group fills from Fable's selection, a handful to start). For each chosen stage: the outside of the fused pieces, face by face
# (on every plane, the faces pointing out minus those pointing in, split by piece kind so each face keeps its piece's colour), welded
# into one polyhedron with outward faces and a colour per face. Writes src/krp-core/src/polyhedra/transitional.js (generated).
# Checks per shape: every face simple (no holes), the volume equals the fused pieces' volume.
import os, sys, json
import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA
from steps import plane, GAP

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
REPO = os.path.join(HERE, '..', '..')
ROLE = json.load(open(os.path.join(HERE, 'role-colours.json')))

# (id, name, view, how the stage is chosen): 'app': the app's Top shell levels up to k (1-based); 'route': main-route steps up to k.
CHOSEN = [
    # The Dodecahedral Chain, the clearest teaching route (DICTO 2026-10-13): icosahedron -> great stellated dodecahedron ->
    # excavated dodecahedron -> dodecahedron (identifications checked in the paper, CHECKS.md). Its stages 2 and 3 are the Lotus
    # seed's stages 2 and 3.
    ('TRANS_LOTUS_2', 'Great stellated dodecahedron: icosahedron + 20 CLEO (Lotus seed and Dodecahedral Chain, stage 2)', 'karma.lotus', 'app', 2),
    ('TRANS_LOTUS_3', 'Excavated dodecahedron: + 30 AXE (Lotus seed and Dodecahedral Chain, stage 3)', 'karma.lotus', 'app', 3),
    ('TRANS_DCHAIN_4', 'Dodecahedron: + 12 caps (Dodecahedral Chain, stage 4)', 'karma.dodeca', 'app', 4),
    ('TRANS_LOTUS_4', 'Lotus seed, stage 4: + 12 icosahedra', 'karma.lotus', 'app', 4),
    ('TRANS_LOTUS_5', 'Lotus seed, stage 5: + 30 AXE', 'karma.lotus', 'app', 5),
    ('TRANS_BODHI_B2', 'Rhombic hexecontahedron: triacontahedron + 60 Vajras (Bodhi Seed Kit B, stage 2)', 'bodhi.kitB', 'app', 2),
    ('TRANS_DHARMA_80', 'DICTO Truncated-Icosahedral Hecatodihedron: truncated icosahedron + 20 Shields (Spheres of Dharma, stage 7)', 'dharma.cycle', 'route', 7),
]


def stage_pieces(view, how, k):
    pieces = DATA[view]
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    P = [(r, np.array(V, float) - c0, F) for r, V, F in pieces]
    dist = [float(np.linalg.norm(Q.mean(0))) for _, Q, _ in P]
    if how == 'app':  # exactly as world-chains.js groups them
        radius = np.linalg.norm(allP - c0, axis=1).max()
        levels = []
        for d in sorted(dist):
            if not levels or d - levels[-1] >= radius * 0.06: levels.append(d)
        shell = [min(range(len(levels)), key=lambda i: abs(levels[i] - d)) for d in dist]
        return [P[i] for i in range(len(P)) if shell[i] < k]
    steps = json.load(open(os.path.join(HERE, 'steps.json')))[view]
    keep = {s['added'].split(' ')[0] for s in steps[:k]}
    return [P[i] for i in range(len(P)) if f"{P[i][0]}@{dist[i]:.2f}" in keep]


def fused_polyhedron(pcs):
    planes = []  # [n, d, {role: [plus faces]}, [minus faces]]
    for role, Q, F in pcs:
        pc = Q.mean(0)
        for f in F:
            n, d = plane(Q, f, pc)
            for q in planes:
                if np.allclose(q[0], n, atol=1e-4) and abs(q[1] - d) < 1e-4: q[2].setdefault(role, []).append(Q[f]); break
                if np.allclose(q[0], -n, atol=1e-4) and abs(q[1] + d) < 1e-4: q[3].append(Q[f]); break
            else: planes.append([n, d, {role: [Q[f]]}, []])
    close = lambda polys: unary_union([p.buffer(GAP, join_style=2) for p in polys]).buffer(-GAP, join_style=2)
    verts.clear(); faces.clear(); colours.clear(); split[0] = 0; holes = 0
    for n, d, plus, minus in planes:
        u = np.cross(n, [1, 0, 0] if abs(n[0]) < 0.9 else [0, 1, 0]); u /= np.linalg.norm(u); v = np.cross(n, u)
        to2 = lambda poly: Polygon([(float(p @ u), float(p @ v)) for p in poly]).buffer(0)
        allplus = close([to2(x) for fs in plus.values() for x in fs]); B = close([to2(x) for x in minus]) if minus else Polygon()
        # each piece face's visible part, then neighbours of one kind merged while the merge stays convex (no star or bow-tie faces)
        def convex_merge(polys):
            polys = [g for p in polys for g in getattr(p, 'geoms', [p]) if g.geom_type == 'Polygon' and g.area > 1e-6]
            merged = True
            while merged:
                merged = False
                for a in range(len(polys)):
                    for c in range(a + 1, len(polys)):
                        if polys[a].distance(polys[c]) > GAP * 2: continue
                        m = close([polys[a], polys[c]])
                        if m.geom_type == 'Polygon' and abs(m.convex_hull.area - m.area) < 1e-6 and abs(m.area - polys[a].area - polys[c].area) < 1e-5:
                            polys[a] = m; polys.pop(c); merged = True; break
                    if merged: break
            # second pass: pieces joined along edges (not just at a corner) that together make one convex shape become one face
            n = len(polys)
            joined = [[a] for a in range(n)]
            near = lambda a, c: polys[a].buffer(GAP).intersection(polys[c].buffer(GAP)).area > 1e-6
            comp, seen = [], set()
            for a in range(n):
                if a in seen: continue
                stack, cur = [a], []
                seen.add(a)
                while stack:
                    x = stack.pop(); cur.append(x)
                    for c in range(n):
                        if c not in seen and near(x, c): seen.add(c); stack.append(c)
                comp.append(cur)
            out = []
            for cur in comp:
                if len(cur) > 1:
                    m = close([polys[x] for x in cur])
                    if m.geom_type == 'Polygon' and abs(m.convex_hull.area - m.area) < 1e-6 and abs(m.area - sum(polys[x].area for x in cur)) < 1e-5:
                        out.append(m); continue
                out += [polys[x] for x in cur]
            return out
        visible = {r: convex_merge([to2(x).difference(B) for x in fs]) for r, fs in plus.items()}
        for sign, regions in ((1, visible), (-1, {'inner': [B.difference(allplus)]})):
            for role, reg in regions.items():
                # parts that only touch at a corner (a ring through the same point twice) become separate faces
                parts = []
                for g0 in [y for x in reg for y in getattr(x, 'geoms', [x])]:
                    if g0.geom_type != 'Polygon' or g0.is_empty: continue
                    for h in getattr(make_valid(Polygon(g0.exterior.coords, [i.coords for i in g0.interiors])), 'geoms', None) or [make_valid(g0)]:
                        parts += [x for x in getattr(h, 'geoms', [h]) if x.geom_type == 'Polygon']
                for g in parts:
                    if g.is_empty or g.area < 1e-4 or g.geom_type != 'Polygon': continue
                    if sign < 0 and d < 0: continue  # facing the centre: rounding only (none of these is hollow)
                    holes += len(g.interiors)
                    ring = [np.array(c) for c in g.exterior.coords[:-1]]
                    ring = [p for i, p in enumerate(ring) if np.linalg.norm(p - ring[i - 1]) > 1e-4]
                    keep = []  # true corners only
                    for i, p in enumerate(ring):
                        a, c = ring[i - 1], ring[(i + 1) % len(ring)]
                        w1, w2 = p - a, c - p
                        if abs(w1[0] * w2[1] - w1[1] * w2[0]) > 2e-3 * np.linalg.norm(w1) * np.linalg.norm(w2): keep.append(p)
                    if len(keep) < 3: continue
                    if sign < 0: keep = keep[::-1]
                    for part in convex_parts(keep):
                        add_face([x * u + y * v + d * n for x, y in part], n * sign, role)
    V = np.array(verts)
    vol = sum(np.dot(V[f[0]], np.cross(V[f[m]], V[f[m + 1]])) for f in faces for m in range(1, len(f) - 1)) / 6
    return V, faces, colours, holes, vol, split[0]


def convex_parts(poly):
    """A simple 2D polygon as few convex polygons: ear-clip into triangles.
    A convex polygon comes back whole; a non-convex one as triangles."""
    P = [np.array(p, float) for p in poly]
    area = sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))
    if area < 0: P = P[::-1]
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    if all(cross(P[i - 1], P[i], P[(i + 1) % len(P)]) > -1e-9 for i in range(len(P))): return [P]
    split[0] += 1
    idx, tris = list(range(len(P))), []
    while len(idx) > 3:
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            if cross(P[i0], P[i1], P[i2]) <= 1e-12: continue
            if any(cross(P[i0], P[i1], P[j]) >= 0 and cross(P[i1], P[i2], P[j]) >= 0 and cross(P[i2], P[i0], P[j]) >= 0 for j in idx if j not in (i0, i1, i2)): continue
            tris.append([i0, i1, i2]); idx.pop(k); break
        else: break
    tris.append(idx)
    polys = tris  # plain triangles (a merge into larger convex parts is left out: it must be proved not to overlap first)
    return [[P[i] for i in q] for q in polys]


split = [0]
verts, faces, colours = [], [], []


def vid(p):
    for i, q in enumerate(verts):
        if np.linalg.norm(q - p) < 1e-4: return i
    verts.append(p); return len(verts) - 1


def add_face(P3, nn, role):
    idx = [vid(p) for p in P3]
    c3 = np.mean(P3, axis=0)
    s = sum(np.dot(np.cross(P3[i] - c3, P3[(i + 1) % len(P3)] - c3), nn) for i in range(len(P3)))
    if s < 0: idx = idx[::-1]
    faces.append(idx); colours.append(ROLE.get(role, 0xb8c4bd) if role != 'inner' else 0xb8c4bd)


if __name__ == '__main__':
    raw, report = {}, []
    for sid, name, view, how, k in CHOSEN:
        pcs = stage_pieces(view, how, k)
        V, F, C, holes, vol, nsplit = fused_polyhedron(pcs)
        F, C = [list(map(int, f)) for f in F], list(C)
        want = sum(ConvexHull(Q).volume for _, Q, _ in pcs)
        ok = holes == 0 and abs(vol - want) < 1e-3 * want
        report.append(f"{sid}: {len(pcs)} pieces -> {len(V)} corners, {len(F)} faces, holes {holes}, non-convex faces split {nsplit}, volume {vol:.5f} vs {want:.5f} {'OK' if ok else 'CHECK'}")
        print(report[-1], flush=True)
        if ok: raw[sid] = {'name': name, 'source': f'{view} {how} {k}', 'vertices': np.round(V, 6).tolist(), 'faces': F, 'faceColours': C}
    out = os.path.join(REPO, 'src', 'krp-core', 'src', 'polyhedra', 'transitional.js')
    with open(out, 'w') as fh:
        fh.write("// Generated by studies/2026-10-13-fused-shells/scripts/build_transitional.py (DICTO Transitional Shells). Do not edit.\n")
        fh.write("// Each: one stage of DICTO's Chain of Karma, Spheres of Dharma or Bodhi Seed with its pieces fused into one solid; faceColours\n")
        fh.write("// keep each face's piece colour from the app's views. Checked: simple faces, volume = the fused pieces' volume.\n")
        fh.write("import { specOf } from './stellaJewel.js';\n")
        fh.write(f"const RAW = {json.dumps(raw, separators=(',', ':'))};\n")
        fh.write("export const TRANSITIONAL_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, { ...specOf(id, p.name, p.vertices, p.faces, true, 1), faceColours: p.faceColours, source: p.source }]));\n")
        fh.write("export const TRANSITIONAL_IDS = Object.keys(RAW);\n")
    print('wrote', out, len(raw), 'shapes')
