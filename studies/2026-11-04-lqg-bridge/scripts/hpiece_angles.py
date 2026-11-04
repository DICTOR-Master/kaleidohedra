"""Ledger OPEN item: do HexOct h-pieces tile alone for 5/24 <= λ < 3/8 (Dehn zero there)? Apply the local edge-angle count (bridge.py angle_ok)."""
import os, sys, math, numpy as np
from fractions import Fraction as Fr
from collections import Counter
exec(open('scripts/bridge.py').read().split("FAM = {")[0])
HEX = os.path.expanduser('~/kres-tmp/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as Tl
os.chdir(here); Hh = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*Hh])
for l in ('1/5', '5/24', '11/48', '1/4', '7/24', '1/3', '17/48', '3/8', '2/5'):
    os.chdir(HEX); pcs, _ = Tl.tile('AB', 0, Fr(l)); os.chdir(here)
    out = []
    for k, up, s_, P, J in pcs:
        X = np.unique(np.round(np.array([cart(p) for p in P]), 10), axis=0); X, F = hull_faces(X)
        rows = dehn(X, F, rows_only=True); angs = sorted({round(math.degrees(t), 3) for L, t in rows})
        out.append(f"{k}{'+' if up else '-'}: Dehn0 {dehn(X, F)['dehn_zero']}, angle count {angle_ok([t for L, t in rows])}, dihedrals {angs}")
    print(f"λ={l}: " + ' | '.join(dict.fromkeys(out)))
