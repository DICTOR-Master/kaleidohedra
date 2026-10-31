# Face list of both tiles at one weight (default the chosen lambda = -1/8): corners, sides (in units of the ball spacing),
# ring count, and which part (solid) of the tile each face belongs to.
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless ~/geom/bin/python faces_at.py [lambda] -> stdout, ../out/faces-<lam>.json
import os, sys, json
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('TILES_DIR', os.path.join(HERE, '../../2026-10-29-endless-stack-cell/scripts'))); sys.path.insert(0, HERE)
from tiles import tile
import exactfaces as E
lam = Fr(sys.argv[1]) if sys.argv[1:] else Fr(-1, 8)
res = {}
for t, w, L in (('c', 'ABC', 1), ('h', 'AB', 0)):
    P = tile(w, L, lam)[0]; F = E.union_faces([p[3] for p in P])
    print(f'== {t}-tile at lambda = {lam}: {len(F)} faces; pieces:', [(k, up, len(p)) for k, up, s, p, J in P], ' glued:', sorted(E.GLUE))
    out = []
    for f in F:
        lp = f['loops'][0]; n = len(lp); r = E.ring_test(f)
        sides = [E.is_sq(E.len2(E.sub(lp[(i + 1) % n], lp[i]))) for i in range(n)]
        print(f"  n={f['n']} c={f['c']}: {n}-gon sides {[str(s) for s in sides]} rings {r['rings'] if r else '-'} corners {[tuple(str(x) for x in p) for p in lp]}")
        out.append(dict(n=f['n'], c=str(f['c']), corners=[[str(x) for x in p] for p in lp], sides=[str(s) for s in sides],
                        rings=(int(r['rings']) if r else None), holes=len(f['loops']) - 1))
    # where the parts touch: corners shared by faces of different surface parts
    res[t] = out
json.dump(res, open(os.path.join(HERE, f'../out/faces-{str(lam).replace("/", "_")}.json'), 'w'), indent=1)
