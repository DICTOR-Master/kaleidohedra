# A small ring-built stack of HexOct tiles at lambda = -1/8 (DICTO 2026-10-31): the 4H stacking ABCB (types h c h c).
# Exact checks (fractions):
#  1. a string: tile L+1 placed so that its lower octahedron half is the other half of tile L's upper octahedron; then the two
#     tiles meet in a full regular hexagon (side 1/2), and nothing else of area;
#  2. which parts are joined over area (h-tile = one part, c-tile = its two towers), for one string and for patches of strings
#     side by side (all patches of 1, 2 and 3 strings near the first are tried);
#  3. the ring count of the stack with every shared wall built once: distinct ring triangles and distinct ring sides
#     (two zip ties per ring side, through all rings meeting there).
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless ~/geom/bin/python stack.py -> stdout, ../out/stack.json
import os, sys, json, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build as B
import exactfaces as E
from tiles import tile, types
from stackings import POS
WORD, NL, LAM = 'ABCB', 4, B.LAM
T = types(WORD)

def tile_abs(L, du, dv):
    """pieces of layer L's tile at the ball POS[word[L]] + (du, dv), absolute coordinates (z in layers)"""
    P = tile(WORD, L % len(WORD), LAM)[0]; b = POS[WORD[L % len(WORD)]]
    out = []
    for k, up, s, pts, J in P:
        f = lambda p: (p[0] + b[0] + du, p[1] + b[1] + dv, p[2] + L)
        out.append(dict(kind=k, up=up, site=f(s), pts=[f(p) for p in pts], L=L))
    return out

def string(du0=0, dv0=0):
    tiles = [tile_abs(0, du0, dv0)]; offs = [(du0, dv0)]
    for L in range(1, NL):
        top = [p for p in tiles[-1] if p['kind'] == 'oct' and p['up'] is False][0]['site']
        P0 = tile_abs(L, 0, 0); bot = [p for p in P0 if p['kind'] == 'oct' and p['up'] is True][0]['site']
        du, dv = top[0] - bot[0], top[1] - bot[1]; assert du.denominator == 1 and dv.denominator == 1 and top[2] == bot[2]
        tiles.append(tile_abs(L, du, dv)); offs.append((du, dv))
    return tiles, offs

def parts_of(tilelist):
    """parts: list of (tile index, set of piece indices) -- pieces of one tile glued over area"""
    parts = []
    for ti, P in enumerate(tilelist):
        E.union_faces([p['pts'] for p in P]); g = E.GLUE
        par = list(range(len(P)))
        def fd(i):
            while par[i] != i: i = par[i]
            return i
        for a, b in g: par[fd(a)] = fd(b)
        S = {}
        for i in range(len(P)): S.setdefault(fd(i), set()).add(i)
        for s in S.values(): parts.append((ti, s))
    return parts

FCACHE = {}
def pfacets(pts):
    k = tuple(pts)
    if k not in FCACHE:
        out = []
        for n, c, q in E.facets(pts):
            ax = E.proj_axes(n)[1]; out.append((n, c, E.hull2([(p[ax[0]], p[ax[1]]) for p in q]), ax))
        FCACHE[k] = out
    return FCACHE[k]
def conv_overlap(P, Q):
    """positive-area overlap of two convex ccw polygons (exact): clip P by Q's edge lines"""
    C = P
    for i in range(len(Q)):
        a, b = Q[i], Q[(i + 1) % len(Q)]
        L = (b[1] - a[1], a[0] - b[0], (b[1] - a[1]) * a[0] + (a[0] - b[0]) * a[1])   # Q left of a->b: a x + b y <= c
        C = E.clip(C, L, -1)
        if not C: return False
    return True
def glued(X, Y):
    """two convex pieces glued over a positive area: a facet plane in common with opposite outward normals, overlapping"""
    for i in range(3):
        if max(p[i] for p in X) < min(p[i] for p in Y) or max(p[i] for p in Y) < min(p[i] for p in X): return False
    FY = {(n, c): (P, ax) for n, c, P, ax in pfacets(Y)}
    for n, c, P, ax in pfacets(X):
        m = tuple(-x for x in n)
        if (m, -c) in FY and conv_overlap(P, FY[(m, -c)][0]): return True
    return False
def contact_graph(tilelist):
    pieces = [(ti, pi, p) for ti, P in enumerate(tilelist) for pi, p in enumerate(P)]
    glue = set()
    for a in range(len(pieces)):
        for b in range(a + 1, len(pieces)):
            if glued(pieces[a][2]['pts'], pieces[b][2]['pts']): glue.add((a, b))
    faces = None
    parts = parts_of(tilelist); pid = {}
    for k, (ti, s) in enumerate(parts):
        for pi in s: pid[(ti, pi)] = k
    edges = set()
    for a, b in glue:
        A = pid[pieces[a][:2]]; Bp = pid[pieces[b][:2]]
        if A != Bp: edges.add((min(A, Bp), max(A, Bp)))
    par = list(range(len(parts)))
    def fd(i):
        while par[i] != i: i = par[i]
        return i
    for a, b in edges: par[fd(a)] = fd(b)
    comps = len({fd(i) for i in range(len(parts))})
    deg = [sum(1 for e in edges if k in e) for k in range(len(parts))]
    return dict(parts=len(parts), joins=len(edges), components=comps, min_degree=min(deg), degrees=deg, faces=faces,
                part_list=[(ti, sorted(s)) for ti, s in parts], edges=sorted(edges))

def hexagon_check(tiles):
    res = []
    for L in range(NL - 1):
        fa = B.split_edges(E.union_faces([p['pts'] for p in tiles[L]])); fb = E.union_faces([p['pts'] for p in tiles[L + 1]])
        top = [f for f in fa if f['n'] == (0, 0, 1) and f['c'] == L + Fr(1, 2)]
        bot = [f for f in fb if f['n'] == (0, 0, -1) and f['c'] == -(L + Fr(1, 2))]
        same = len(top) == 1 and len(bot) == 1 and set(top[0]['loops'][0]) == set(bot[0]['loops'][0])
        # and the pair glued only over that hexagon: union of the two tiles has 6+... check glued area = hexagon area
        both = tiles[L] + tiles[L + 1]; E.union_faces([p['pts'] for p in both])
        cross = [g for g in E.GLUE if (g[0] < len(tiles[L])) != (g[1] < len(tiles[L]))]
        res.append(dict(L=L, hexagon_same=same, corners=len(top[0]['loops'][0]) if top else 0,
                        cross_glued_pairs=[(both[a]['kind'], both[b]['kind']) for a, b in cross]))
    return res

def ring_census(tilelist):
    """distinct ring triangles and ring sides over all tile surfaces (shared walls once); also per-tile totals"""
    tris, sides_count, per_tile = {}, {}, []
    for P in tilelist:
        faces = B.split_edges(E.union_faces([p['pts'] for p in P])); n = 0
        for f in faces:
            for Tr in B.rings_of(f):
                key = frozenset(Tr); n += 1
                if key not in tris:
                    tris[key] = 1
                    for i in range(3): sides_count.setdefault(frozenset((Tr[i], Tr[(i + 1) % 3])), 0)
                else: tris[key] += 1
        per_tile.append(n)
    for key in tris:
        Tr = list(key)
        for i in range(3): sides_count[frozenset((Tr[i], Tr[(i + 1) % 3]))] += 1
    from collections import Counter
    mult = Counter(sides_count.values())
    return dict(rings=len(tris), shared_walls_rings=sum(1 for v in tris.values() if v == 2), sides=len(sides_count),
                ties=2 * len(sides_count), rings_per_side=dict(mult), sum_tiles_rings=sum(per_tile),
                sum_tiles_ties=3 * sum(per_tile), per_tile=per_tile), tris

if __name__ == '__main__':
    out = {'word': WORD, 'types': ''.join(T)}
    S0, offs = string()
    out['string_offsets'] = [list(map(str, o)) for o in offs]
    out['hexagons'] = hexagon_check(S0)
    print('types', ''.join(T), 'string offsets', offs); print('hexagon joints', out['hexagons'], flush=True)
    g = contact_graph(S0)
    print('one string: parts', g['parts'], 'joins', g['joins'], 'components', g['components'], 'degrees', g['degrees'], g['part_list'], g['edges'], flush=True)
    out['one_string'] = {k: g[k] for k in ('parts', 'joins', 'components', 'min_degree', 'degrees', 'edges')}
    out['one_string']['part_list'] = [[ti, s] for ti, s in g['part_list']]
    # patches: strings shifted by lattice vectors (whole string moved), the first at (0, 0)
    cand = [(a, b) for a in range(-1, 2) for b in range(-1, 2) if (a, b) != (0, 0)]
    best = {}
    for n in (2, 3):
        for extra in itertools.combinations(cand, n - 1):
            # neighbours only: every string touches another (checked by the contact graph anyway)
            tl = [t for o in [(0, 0), *extra] for t in [tile_abs(L, offs[L][0] + o[0], offs[L][1] + o[1]) for L in range(NL)]]
            gg = contact_graph(tl)
            key = (gg['components'], -gg['min_degree'])
            print(n, extra, 'components', gg['components'], 'min degree', gg['min_degree'], 'joins', gg['joins'], flush=True)
            if n not in best or key < best[n][0]: best[n] = (key, extra, gg)
    for n, (key, extra, gg) in best.items():
        out[f'best_{n}_strings'] = dict(extra=[list(e) for e in extra], components=gg['components'], min_degree=gg['min_degree'], joins=gg['joins'], parts=gg['parts'])
    # ring census: one string, and the best 3-string patch
    c1, _ = ring_census(S0); out['census_one_string'] = c1; print('census one string', c1, flush=True)
    if 3 in best:
        extra = best[3][1]
        tl = [tile_abs(L, offs[L][0] + o[0], offs[L][1] + o[1]) for o in [(0, 0), *extra] for L in range(NL)]
        c3, _ = ring_census(tl); out['census_three_strings'] = c3; print('census three strings', c3, flush=True)
    json.dump(out, open(os.path.join(B.OUT, 'stack.json'), 'w'), indent=1, default=str)
