# DICTO 2026-11-04, paper #92: independent check of Lemma 4 (the vertex stars of a face-to-face tiling by regular
# tetrahedra and octahedra of edge 1). Search: start from one tetrahedron at V = 0, close every face at V with a
# tetrahedron or an octahedron on its far side (both tried), reject any edge at V whose angle sum exceeds 2pi or any star
# whose solid angle exceeds 4pi; keep the closed stars. Floats (1e-9) for the search; each star found is then identified
# exactly by its 12 neighbour vectors (neighbour dot products are small rationals).
#   ~/geom/bin/python3 vertex_stars.py > data/vertex-stars.log
import numpy as np, itertools, math, json
from fractions import Fraction as Fr
EPS = 1e-9
al = math.acos(1 / 3)
key = lambda v: tuple(np.round(v, 7) + 0.0)

def tet_across(a, b, inside):          # tetrahedron on face (0,a,b), on the side away from 'inside'
    g = (a + b) / 3; n = np.cross(a, b); n /= np.linalg.norm(n)
    if np.dot(n, inside - g) > 0: n = -n
    c = g + math.sqrt(2 / 3) * n
    return ('T', (a, b, c))
def oct_across(a, b, inside):
    g = (a + b) / 3; n = np.cross(a, b); n /= np.linalg.norm(n)
    if np.dot(n, inside - g) > 0: n = -n
    m = g + n / math.sqrt(6)                         # octahedron centre
    return ('O', (a, b, 2 * m - a, 2 * m - b))       # its 4 edges at V (cyclic: a, b, 2m-a, 2m-b)
def faces(t):
    k, e = t
    if k == 'T': return [(e[0], e[1], e[2]), (e[1], e[2], e[0]), (e[0], e[2], e[1])]   # (a, b, a point inside)
    a, b, c, d = e; ctr = (a + c) / 2
    return [(a, b, ctr), (b, c, ctr), (c, d, ctr), (d, a, ctr)]
def tkey(t): return (t[0], tuple(sorted(key(x) for x in t[1])))
def fkey(a, b): return tuple(sorted([key(a), key(b)]))
def solid(t):
    k, e = t
    if k == 'T': return 3 * al - math.pi
    return 2 * math.pi - 4 * al
def dihedral(t): return al if t[0] == 'T' else math.pi - al
def edges(t): return [key(x) for x in t[1]]

found = {}
def search(tiles, depth=0):
    tot = sum(solid(t) for t in tiles)
    if tot > 4 * math.pi + EPS: return
    ang = {}
    for t in tiles:
        for e in edges(t): ang[e] = ang.get(e, 0) + dihedral(t)
    if any(v > 2 * math.pi + EPS for v in ang.values()): return
    cnt = {}
    for t in tiles:
        for a, b, _ in faces(t): cnt[fkey(a, b)] = cnt.get(fkey(a, b), 0) + 1
    if any(v > 2 for v in cnt.values()): return
    open_f = [(a, b, ins) for t in tiles for a, b, ins in faces(t) if cnt[fkey(a, b)] == 1]
    if not open_f:
        if abs(tot - 4 * math.pi) < 1e-7:
            nb = sorted({e for t in tiles for e in edges(t)})
            G = tuple(sorted(round(float(np.dot(np.array(p), np.array(q))), 6) for p, q in itertools.combinations(nb, 2)))
            tt = tuple(sorted(sum(1 for t in tiles if key_in(e, t)) for e in nb))
            found.setdefault(G, (len([t for t in tiles if t[0] == 'T']), len([t for t in tiles if t[0] == 'O']), nb, tiles))
        return
    a, b, ins = open_f[0]
    keys = {tkey(t) for t in tiles}
    for maker in (tet_across, oct_across):
        nt = maker(a, b, ins)
        if tkey(nt) in keys: continue
        search(tiles + [nt], depth + 1)
def key_in(e, t): return e in edges(t)

T0 = ('T', tuple(np.array(v, float) / math.sqrt(2) for v in [(1, 1, 0), (1, 0, 1), (0, 1, 1)]))
search([T0])
print(f'closed vertex stars found (up to the starting tetrahedron fixed): {len(found)} distinct by neighbour Gram spectrum')
out = []
for G, (nT, nO, nb, tiles) in found.items():
    nbv = [np.array(p) for p in nb]
    # flat hexagons: planes through V containing 6 neighbours
    planes = set()
    for p, q in itertools.combinations(nbv, 2):
        n = np.cross(p, q)
        if np.linalg.norm(n) < 1e-6: continue
        n /= np.linalg.norm(n)
        inpl = [r for r in nbv if abs(np.dot(r, n)) < 1e-7]
        if len(inpl) == 6: planes.add(key(n if n[np.argmax(np.abs(n))] > 0 else -n))
    # TTOO edges: an edge with two tetrahedra sharing a face
    ttoo = 0
    for e in nb:
        ts = [t for t in tiles if t[0] == 'T' and e in edges(t)]
        if len(ts) == 2 and len(set(edges(ts[0])) & set(edges(ts[1]))) == 2: ttoo += 1
    # exact identification: Gram entries x 2 must be integers in {-2..2}; cuboctahedron vs triangular orthobicupola
    fr = sorted(Fr(g).limit_denominator(12) for g in G)
    hist = {str(k): fr.count(k) for k in sorted(set(fr))}
    exact = all(abs(g - float(f)) < 1e-6 for g, f in zip(sorted(G), fr))
    name = 'cuboctahedron (octet vertex)' if len(planes) == 4 else 'triangular orthobicupola (twisted vertex)' if len(planes) == 1 else '?'
    print(f'  star: {nT} tetrahedra, {nO} octahedra, {len(nb)} neighbours, flat hexagons {len(planes)}, TTOO edges {ttoo}: {name}')
    print(f'     neighbour dot products (rationals with denominator <= 12 to 1e-6: {exact}): {hist}')
    out.append(dict(tetrahedra=nT, octahedra=nO, neighbours=len(nb), flat_hexagons=len(planes), ttoo_edges=ttoo, name=name, gram_hist=hist))
ok = sorted((o['flat_hexagons'], o['ttoo_edges']) for o in out) == [(1, 6), (4, 0)] and all(o['tetrahedra'] == 8 and o['octahedra'] == 6 for o in out)
print(('PASS' if ok else 'FAIL') + ' exactly two vertex stars: the octet star (4 flat hexagons, no twisted edge) and the twisted star (1 flat hexagon, its 6 edges twisted)')
json.dump(out, open('data/vertex-stars.json', 'w'), indent=1)
