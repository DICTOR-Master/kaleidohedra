# Task step 4: other splits of the pieces between layers. split_check.py shows that only at λ = -1/8 every whole piece has one
# shape whatever the context (regular tetrahedra, regular octahedra); at every other weight tested the whole octahedral piece
# depends on both neighbouring layers and each tetrahedral piece on the layer of its base, so the Rule of Halves split is the
# only one that gives two layer tiles. At λ = -1/8 two other splits are tried, with all in-layer translates as in connect.py:
#  W: layer L's tile = its two tetrahedra (bases on layer L) + the WHOLE octahedron of the gap above (depends on L's letter only:
#     tetrahedra over pos(L-1) and pos(L+1), octahedron over the third position of L, L+1);
#  G: the whole gap slab between layers L and L+1 (octahedron + both tetrahedra): ONE tile for every stacking (no c/h).
# Usage: python3 alt_split.py -> data/alt_split.json
import json, os, sys
from fractions import Fraction as Fr
from engine import Cell
from tiles import tile, build, corners
from stackings import POS
import connect as K

LAM = Fr(-1, 8)
def whole(word, L, idx):
    net, spec = build(word); n = len(word); m = spec['motif']; c = Cell(net, idx, (LAM,), Fr(12)); X = corners(c, LAM)
    site = m[idx][1]; sh = round((site[2] * n - L) / n) * n
    ball = (*POS[word[L]], Fr(L))
    return [(p[0] - ball[0], p[1] - ball[1], (p[2] - Fr(sh, n)) * n - ball[2]) for p in X]

if __name__ == '__main__':
    out = {}
    for t, w, L in (('c', 'ABC', 1), ('h', 'AB', 0)):
        T = tile(w, L, LAM)[0]; tets = [p[3] for p in T if p[0] == 'tet']
        n = len(w); g1 = L % n
        P = tets + [whole(w, L, 3 * g1)]
        r = K.run_pieces(P); r.update(split='W', tile=t, pieces=['tet', 'tet', 'oct (whole, gap above)']); out['W_' + t] = r
    w, L = 'ABC', 0
    P = [whole(w, L, 3 * 0 + k) for k in range(3)]
    r = K.run_pieces(P); r.update(split='G', tile='gap', pieces=['oct', 'tet tip-down', 'tet tip-up']); out['G'] = r
    os.makedirs(os.path.join(K.HERE, 'data'), exist_ok=True)
    json.dump(out, open(os.path.join(K.HERE, 'data/alt_split.json'), 'w'), indent=1)
    for k, r in out.items():
        for a in r['classes'][:4]:
            print(k, a['faces'], a['sizes'], 'manifold', a['manifold'], 'hull %.4f' % a['hull_ratio'], 'convex', a['convex'],
                  'neck %.3f' % a['neck'], 'sym', a['sym'], a['translates'], flush=True)
