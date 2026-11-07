"""Nets made by unfolding the real solids along a path of faces, so they always fold up.
Glue tabs: one on each pair of cut edges. Checked: no triangles overlap, every cut edge gets exactly one tab."""
import math
def unfold(faces, path, E):
    # faces: list of vertex-id triples; path: face order, consecutive faces share an edge
    pos = {}
    f0 = faces[path[0]]; h = E * 3 ** 0.5 / 2
    pos[(path[0], f0[0])] = (0, 0); pos[(path[0], f0[1])] = (E, 0); pos[(path[0], f0[2])] = (E / 2, -h)
    tri = {path[0]: {v: pos[(path[0], v)] for v in f0}}
    for a, b in zip(path, path[1:]):
        sh = set(faces[a]) & set(faces[b]); assert len(sh) == 2, (a, b)
        u, v = sorted(sh); oa = (set(faces[a]) - sh).pop(); ob = (set(faces[b]) - sh).pop()
        P, Q, R = tri[a][u], tri[a][v], tri[a][oa]
        mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
        tri[b] = {u: P, v: Q, ob: (2 * mx - R[0], 2 * my - R[1])}
    return tri
def check(tri):
    cs = [tuple(sum(p[i] for p in t.values()) / 3 for i in (0, 1)) for t in tri.values()]
    for i in range(len(cs)):
        for j in range(i):
            assert math.dist(cs[i], cs[j]) > 1e-3, 'overlap'
def tabs(faces, path, tri):
    tree = {frozenset(set(faces[a]) & set(faces[b])) for a, b in zip(path, path[1:])}
    seen = set(); out = []
    for f in path:
        vs = faces[f]
        for i in range(3):
            e = frozenset((vs[i], vs[(i + 1) % 3]))
            if e in tree: continue
            if e in seen: continue
            seen.add(e); a, b = [tri[f][v] for v in e]
            c = [p for v, p in tri[f].items() if v not in e][0]
            out.append((a, b, c))
    return out
def svg(tri, tb, ox, oy):
    s = []
    for a, b, c in tb:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = mx - c[0], my - c[1]; L = math.hypot(nx, ny); nx, ny = nx / L * 7, ny / L * 7
        pts = [a, (a[0] + (b[0] - a[0]) * .2 + nx, a[1] + (b[1] - a[1]) * .2 + ny), (a[0] + (b[0] - a[0]) * .8 + nx, a[1] + (b[1] - a[1]) * .8 + ny), b]
        s.append('<polygon points="' + ' '.join(f'{x+ox:.1f},{y+oy:.1f}' for x, y in pts) + '" fill="#eee" stroke="#888" stroke-width="0.6" stroke-dasharray="2 1.5"/>')
    for t in tri.values():
        s.append('<polygon points="' + ' '.join(f'{x+ox:.1f},{y+oy:.1f}' for x, y in t.values()) + '" fill="none" stroke="#222" stroke-width="0.8"/>')
    return ''.join(s)
def bbox(tri):
    xs = [p[0] for t in tri.values() for p in t.values()]; ys = [p[1] for t in tri.values() for p in t.values()]
    return min(xs), min(ys), max(xs), max(ys)
# tetrahedron: vertices 0..3, faces = all triples
TF = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
# octahedron: vertices 0:+x 1:-x 2:+y 3:-y 4:+z 5:-z ; faces by sign triple
OF = {}
for sx in (1, -1):
    for sy in (1, -1):
        for sz in (1, -1):
            OF[(sx, sy, sz)] = (0 if sx > 0 else 1, 2 if sy > 0 else 3, 4 if sz > 0 else 5)
gray = [(1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,-1,-1),(-1,1,-1),(-1,1,1)]
OFL = [OF[g] for g in gray]
def make(E=60):
    t = unfold(TF, [0, 1, 3, 2], E); check(t); tt = tabs(TF, [0, 1, 3, 2], t); assert len(tt) == 3
    o = unfold(OFL, list(range(8)), E); check(o); ot = tabs(OFL, list(range(8)), o); assert len(ot) == 5
    return t, tt, o, ot
if __name__ == '__main__':
    t, tt, o, ot = make(); print('tetra', bbox(t), 'octa', bbox(o))
