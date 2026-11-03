# Quanta of Space v1.5: exact-construction models (floating point, for the catalogue pictures only) of the new solids of
# #88 and #89, written in the DICTO Solids json layout read by render_atoms.py. Geometry from #89's gcb.py (cut at x of
# each edge from every corner) and s2b-rhombic.json (rhombic cuts, edge 1). Usage: new_atoms.py <s2b-rhombic.json> <out dir>
import sys, os, json, re, numpy as np
import gcb
g = gcb.g; s5 = 5 ** .5
rh, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def xg(n): c = 2 * np.cos(np.pi / n); return g / (c + 2 * g)      # greater: corner sides long
def xl(n): c = 2 * np.cos(np.pi / n); return 1 / (g * c + 2)      # lesser: original sides long
def cutP(name, x): V = gcb.platonic(name); F = gcb.faces(V); return gcb.cut(V, F, [x] * len(V))[0]
def cutA(name, x): V = gcb.archimedean(name); F = gcb.faces(V); return gcb.cut(V, F, [x] * len(V))[0]
R = json.load(open(rh))['rhombic']
def rhomb(cat, which): return np.array(next(c for c in R[cat]['cuts'] if c['cut'].startswith(which))['vertices_edge1'])
S = []   # (name, status, vertices)
nfaces = {'dodecahedron': 5, 'icosahedron': 3, 'cube': 4, 'tetrahedron': 3}
for p in ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron']:   # D·I·C·T·O; the octahedron's pair = Icosaxes, Unborn Axes
    n = nfaces[p]
    S.append((f'Greater Golden Cut {p.title()}', 'new', cutP(p, xg(n)), xg(n)))
    S.append((f'Lesser Golden Cut {p.title()}', 'new', cutP(p, xl(n)), xl(n)))
for cat in ['rhombic dodecahedron', 'rhombic triacontahedron']:
    for w in ['greater', 'lesser']:
        S.append((f'{w.title()} Golden Cut {cat.title()}', 'new', rhomb(cat, w), None))
S.append(('Greater Golden Cut Icosidodecahedron', 'rediscovered', cutA('icosidodecahedron', 1 / 3), 1 / 3))
S.append(('Lesser Golden Cut Icosidodecahedron', 'rediscovered', cutA('icosidodecahedron', 1 / (g * s5)), 1 / (g * s5)))
S.append(('Greater Golden Cut Snub Dodecahedron', 'new', cutA('snub dodecahedron', 1 / 3), 1 / 3))
S.append(('Lesser Golden Cut Snub Dodecahedron', 'new', cutA('snub dodecahedron', 1 / (g * s5)), 1 / (g * s5)))
for name, st, V, x in S:
    F = gcb.faces(V); E = gcb.edges_of(F)
    L = sorted(set(round(float(np.linalg.norm(V[a] - V[b])), 6) for a, b in E))
    cnt = {}
    for f in F: cnt[len(f)] = cnt.get(len(f), 0) + 1
    assert len(V) - len(E) + len(F) == 2, name
    slug = 'piece-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    json.dump({'name': name, 'status': st, 'convex': True, 'vertices': [{'decimal': [f'{c:.12f}' for c in v]} for v in V], 'faces': F},
              open(os.path.join(out, slug + '.json'), 'w'))
    print(f'{name:42s} x={x if x is None else round(x, 6)} V={len(V)} E={len(E)} F={len(F)} faces={dict(sorted(cnt.items()))} edges={L}')
