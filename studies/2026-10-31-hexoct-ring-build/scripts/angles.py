# Inside each open interval of the walk the face planes and side directions stay fixed (corners move affinely with lambda),
# so the corner angles are fixed. A face with a corner angle other than 60 or 120 degrees can never be laid with rings
# anywhere in that interval. This checks one weight inside each interval and at each breakpoint.
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless ~/geom/bin/python angles.py  -> stdout (saved as ../out/angles.txt)
import os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('TILES_DIR', os.path.join(HERE, '../../2026-10-29-endless-stack-cell/scripts'))); sys.path.insert(0, HERE)
from tiles import tile
from exactfaces import union_faces, gip, sub, Fr as _F
BR = [Fr(-11, 24), Fr(-3, 8), Fr(-7, 24), Fr(-1, 8), Fr(5, 24), Fr(3, 8)]
def angle_ok(f):
    for lp in f['loops']:
        n = len(lp)
        for i in range(n):
            a, b = sub(lp[i - 1], lp[i]), sub(lp[(i + 1) % n], lp[i])
            c2 = gip(a, b) ** 2 / (gip(a, a) * gip(b, b))
            if c2 != Fr(1, 4): return False
    return True
pts = []
for a, b in zip(BR, BR[1:]): pts += [(a, 'breakpoint'), ((a + b) / 2, f'inside ({a}, {b})')]
pts.append((BR[-1], 'breakpoint'))
for lam, what in pts:
    out = []
    for t, w, L in (('c', 'ABC', 1), ('h', 'AB', 0)):
        F = union_faces([p[3] for p in tile(w, L, lam)[0]]); ok = sum(angle_ok(f) for f in F)
        out.append(f'{t}: {ok}/{len(F)} faces with all angles 60/120')
    print(f'{str(lam):>7}  {what:<22} ' + '   '.join(out), flush=True)
