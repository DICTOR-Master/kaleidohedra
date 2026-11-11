# bridge_count.py, DICTO 12 Nov 2026 ("go ahead with the bridge count"). The isometric bridge from the certified marked chair
# (Tsiokos's Chair44 mechanism; frame marking and certificate by Kamenetsky, arXiv 2610.00916, code vendored in vendor/) to the
# rhombic dodecahedron packing. Chair coordinates (Kamenetsky): unit cubes of side 2 with odd centres. The fcc sites are the
# integer points with ODD coordinate sum: every cube centre (one RD lying wholly inside its cube) and every cube-edge midpoint (an RD
# shared by the 4 cubes round that edge); RDs have corners at the face centres of their cube, nearest neighbours at distance sqrt2.
# Every chair motion (signed permutation + even translation) keeps this site set, so a hierarchical chair tiling labels every RD.
# Question: how many DIFFERENT marked RDs does the bridge need? An RD's label = what it sees of the chair tiling: for each cube
# that contains part of it, that cube's chair frame and cell, written relative to the RD and taken up to the RD's 24 proper turns
# (a marked RD piece can be placed in any of its 24 turns). Counted over level-k supertiles, k = 3..6 (all configurations inside a supertile occur in tilings; stable?).
# Controls: (1) the patch is a partition (every cube once, 7 per chair); (2) every centre RD sees 1 cube, every edge RD 4;
# (3) cell types of centre RDs = exactly the 7 cells; (4) the count must be the same at the two largest k (else: not yet complete).
# usage: python3 bridge_count.py <out.json>
import sys, os, json, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor'))
from chairN import Chair, apply, compose, inverse, make_group, det, vsub, vadd
from collections import Counter
t0 = time.time()
FR = {'0': (0, 1, 2), (0, 0, 0): (0, 1, 2), (0, 0, 1): (0, 2, 1), (0, 1, 0): (2, 1, 0), (0, 1, 1): (1, 2, 0), (1, 0, 0): (1, 0, 2), (1, 0, 1): (0, 1, 2), (1, 1, 0): (2, 0, 1)}
C = Chair(3, FR)
ROT = [g for g in make_group(3) if det(g) == 1]; assert len(ROT) == 24
assert all(det(h) == 1 for h, _ in C.children), 'certified assignment is homochiral'
res = {}; ok = True
KS = tuple(int(a) for a in sys.argv[2].split(",")) if len(sys.argv) > 2 else (3, 4, 5, 6)
for k in KS:
    tiles = C.patch(k); print(f'PROGRESS {KS.index(k) / len(KS):.2f} level {k}', flush=True)
    owner = {}
    for ti, (g, t) in enumerate(tiles):
        for ui, c in enumerate(C.cubes((g, t))):
            assert c not in owner; owner[c] = (ti, ui)
    ok &= len(owner) == 7 * len(tiles)
    lo = min(min(c) for c in owner); hi = max(max(c) for c in owner)
    span = hi - lo; inner = lambda x: all(lo + 0.3 * span <= v <= hi - 0.3 * span for v in x)   # central part, away from the patch rim
    def label(x, cubes):
        """canonical label of the RD at site x: min over the 24 turns R about x of the offset-sorted (R(cube - x), R*g_chair, cell,
        chair id renumbered by first appearance) (fixed 12 Nov: chair ids had followed the world order of the cubes)"""
        best = None
        for R in ROT:
            rows = sorted(((apply(R, vsub(c, x)), compose(R, tiles[owner[c][0]][0]), owner[c][1], owner[c][0]) for c in cubes), key=lambda r: r[0])
            ren = {}; L = tuple((o, g, u, ren.setdefault(ti, len(ren))) for o, g, u, ti in rows)
            if best is None or L < best: best = L
        return best
    cen = Counter(); edg = Counter(); nchairs = Counter(); bad = 0
    sites = set()
    for c in owner:
        sites.add(c)
        for i in range(3):
            for a, b in itertools.product((1, -1), repeat=2):
                d = [a, b]; d.insert(i, 0); sites.add(vadd(c, tuple(d)))      # the 12 edge midpoints of the cube
    for x in sites:
        odd = sum(v % 2 for v in x)
        if odd == 3: cubes = [x]
        elif odd == 1:
            i = next(j for j in range(3) if x[j] % 2)
            cubes = []
            for a, b in itertools.product((1, -1), repeat=2):
                d = [a, b]; d.insert(i, 0); cubes.append(vadd(x, tuple(d)))
        else: bad += 1; continue
        if not all(cc in owner for cc in cubes): continue          # RD cut by the patch rim (every configuration inside a supertile is a genuine one)
        L = label(x, cubes)
        if odd == 3: cen[L] += 1
        else: edg[L] += 1; nchairs[len({owner[cc][0] for cc in cubes})] += 1
    cells_seen = sorted({L[0][2] for L in cen})
    ok &= cells_seen == list(range(7)) and bad == 0
    res[k] = dict(chairs=len(tiles), centre_types=len(cen), edge_types=len(edg), edge_sites=sum(edg.values()),
                  edge_sites_by_chairs_met=dict(sorted(nchairs.items())), edge_types_by_chairs_met=dict(sorted(Counter(len({e[3] for e in L}) for L in edg).items())))
    print(f'k {k}: chairs {len(tiles)}, centre RD types {len(cen)} (cells {cells_seen}), edge RD types {len(edg)} '
          f'(by number of chairs met: {res[k]["edge_types_by_chairs_met"]}); edge sites counted {sum(edg.values())} '
          f'{res[k]["edge_sites_by_chairs_met"]}; {time.time() - t0:.0f}s', flush=True)
stable = res[KS[-2]]['edge_types'] == res[KS[-1]]['edge_types'] and res[KS[-2]]['centre_types'] == res[KS[-1]]['centre_types']
print(f"stable k{KS[-2]} -> k{KS[-1]}: {stable}; TOTAL marked RD types (centre + edge): {res[KS[-1]]['centre_types'] + res[KS[-1]]['edge_types']}")
json.dump(res, open(sys.argv[1], 'w'), indent=1)
print('FINAL ok' if ok and stable else f'FINAL FAIL: controls {ok} stable {stable}')
