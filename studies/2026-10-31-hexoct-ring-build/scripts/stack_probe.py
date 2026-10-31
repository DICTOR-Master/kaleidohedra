# Probe: which patches of strings (whole strings shifted by lattice vectors) and which layer windows of ABCB are joined
# over area into ONE piece (every part = h-tile or c-tower). Exact, pairwise facet test of stack.py.
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless ~/geom/bin/python stack_probe.py -> stdout (../out/stack_probe.txt)
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import stack as S
def patch(offsets, L0, L1):
    _, offs = S.string()
    return [S.tile_abs(L, offs[L % 4][0] + o[0], offs[L % 4][1] + o[1]) for o in offsets for L in range(L0, L1 + 1)]
P = {'1 string': [(0, 0)], '2 strings': [(0, 0), (1, 0)], '3 strings, triangle': [(0, 0), (1, 0), (0, 1)],
     '3 strings, other triangle': [(0, 0), (-1, 0), (0, -1)], '3 strings, row': [(0, 0), (1, 0), (-1, 0)],
     '4 strings, rhombus': [(0, 0), (1, 0), (0, 1), (1, -1)][:3] + [(1, 1)],
     '7 strings, hexagon': [(0, 0), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]}
W = {'h c h c (layers 0-3)': (0, 3), 'c h c h (layers 1-4)': (1, 4), 'h c h (layers 0-2)': (0, 2), 'h c h c h (layers 0-4)': (0, 4)}
ONLY = sys.argv[1:]
for wn, (a, b) in W.items():
    for pn, offs in P.items():
        if ONLY and not any(o == f'{a}{b}{pn[0]}' for o in ONLY): continue
        g = S.contact_graph(patch(offs, a, b))
        par = list(range(g['parts']))
        def fd(i):
            while par[i] != i: i = par[i]
            return i
        for x, y in g['edges']: par[fd(x)] = fd(y)
        loose = [g['part_list'][k] for k in range(g['parts']) if g['degrees'][k] == 0]
        sizes = sorted([sum(1 for k in range(g['parts']) if fd(k) == r) for r in {fd(k) for k in range(g['parts'])}], reverse=True)
        lz = [(k, g['part_list'][k]) for k in range(g['parts']) if g['degrees'][k] == 0]
        print(f'{wn:<22} {pn:<26} parts {g["parts"]:>3} joins {g["joins"]:>3} pieces {g["components"]} sizes {sizes} loose parts {len(loose)} {loose}', flush=True)
