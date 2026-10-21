# DICTO 2026-10-21: the Platonic solids as Reuleaux figures (DICTO's idea; his reading: "balls at the corners"). Each body is the
# common part of balls centred on the solid's corners, radius = the solid's widest span (its diameter). For the tetrahedron this is
# the classical Reuleaux tetrahedron; the general construction is known (Reuleaux polytopes / ball polyhedra). Edge 1. Reports the
# volume and the width range (a body of constant width would have one width in every direction).
import os, json, itertools, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__)); phi = (1 + 5 ** .5) / 2
def cyc(v): return [np.roll(v, k) for k in range(3)]
S = {'Tetrahedron': [p for p in itertools.product((1, -1), repeat=3) if np.prod(p) > 0],
     'Cube': list(itertools.product((1, -1), repeat=3)),
     'Octahedron': [s * e for e in np.eye(3) for s in (1, -1)],
     'Dodecahedron': list(itertools.product((1, -1), repeat=3)) + [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a / phi, b * phi]))],
     'Icosahedron': [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a, b * phi]))]}
GOLD, PURPLE, LILAC, BRONZE = '#d9a441', '#6b3fa0', '#9a78c8', '#8a5a24'
rng = np.random.default_rng(0); U = rng.normal(size=(4000, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
scenes = []
for name, Vs in S.items():
    V = np.array(Vs, float); E = min(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)); V /= E
    D = max(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2))
    body = None
    for v in V:
        b = m3.Manifold.sphere(D, 192).translate(list(v)); body = b if body is None else body ^ b
    me = body.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts)
    w = (P @ U.T).max(0) - (P @ U.T).min(0)
    X = P[T].mean(1); own = np.argmin(np.abs(np.linalg.norm(X[:, None] - V[None], axis=2) - D), axis=1)   # which ball each patch lies on
    # colour: neighbouring faces never share a colour, with the fewest colours the body allows (cube 2, octahedron and dodecahedron 3,
    # tetrahedron and icosahedron 4), from the gold-and-purple family
    adj = {o: set() for o in range(len(V))}
    by = {}
    for f, tri in enumerate(T):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])): by.setdefault((min(a, b), max(a, b)), []).append(f)
    from collections import Counter
    seam = Counter(tuple(sorted((own[fs[0]], own[fs[1]]))) for fs in by.values() if len(fs) == 2 and own[fs[0]] != own[fs[1]])
    for (a, b), n in seam.items():                            # neighbours share a real seam, not just a point
        if n >= 6: adj[a].add(b); adj[b].add(a)
    best = None
    for k in range(2, 5):                                    # smallest k with a proper colouring (backtracking)
        cl = {}
        def go(i, order=sorted(adj, key=lambda o: -len(adj[o]))):
            if i == len(order): return True
            o = order[i]
            for c in range(k):
                if all(cl.get(n) != c for n in adj[o]):
                    cl[o] = c
                    if go(i + 1): return True
                    del cl[o]
            return False
        if go(0): best = dict(cl); break
    PAL = [GOLD, PURPLE, LILAC, BRONZE]; col = [PAL[best[o]] for o in own]
    nk = len(set(best.values()))
    print(f'{name:12s} corners {len(V):2d}  diameter {D:.4f}  volume {body.volume():.4f}  width {w.min():.4f}..{w.max():.4f} (ratio {w.max() / w.min():.4f})  colours {nk}')
    scenes.append({'title': f'Reuleaux {name.lower()}', 'sub': f'{len(V)} balls of radius {D:.3f} (edge 1)', 'parts': [{'v': np.round(P, 5).tolist(), 't': T.tolist(), 'c': col, 'e': None, 'a': 1.0}]})
for s in scenes:
    pts = np.array(s['parts'][0]['v']); s['E'] = round(float(np.linalg.norm(pts, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
open(os.path.join(HERE, 'renders', 'reuleaux.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'reuleaux-labels.json'), 'w'), indent=1)
print('reuleaux.html', len(scenes))
