#!/usr/bin/env python3
"""Dehn screen of the HexOct tiles (#75) and of each of their four pieces, at several λ. Tile Dehn = sum of its pieces' (additivity); tiles tile space, so the
tile sums MUST be zero (calibration of the multi-piece mode). Pieces: could one alone tile? (Dehn zero necessary.)"""
import os, sys, math, json, numpy as np
from fractions import Fraction as Fr
sys.argv = sys.argv[:1] + ['x', '8', '300']
src = open('scripts/dehn.py').read().split("if __name__")[0]; exec(src)
HEX = os.path.expanduser('~/work/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as T
os.chdir(here)
H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
out = []
for lam in (Fr(1, 10), Fr(1, 6), Fr(1, 5), Fr(1, 4)):
    for word, L, nm in (('ABC', 1, 'c-tile'), ('AB', 0, 'h-tile')):
        try:
            os.chdir(HEX); pieces, tz = T.tile(word, L, lam); os.chdir(here)
        except Exception as e:
            os.chdir(here); print(lam, nm, 'build failed', e); continue
        allrows = []; pr = []
        for k, up, s_, P, J in pieces:
            X = np.unique(np.round(np.array([cart(p) for p in P]), 11), axis=0)
            X, F = hull_faces(X); r = dehn(X, F, f'{nm} piece {k}{"↑" if up else "↓"}'); pr.append((r['name'], r['dehn_zero'], len(X)))
            allrows += dehn(X, F, rows_only=True)
        tot = dehn(np.zeros((0, 3)), [], f'{nm} whole', extra_rows=allrows) if False else None
        # whole tile from pooled rows
        exec_rows = allrows
        V_dummy = np.array([(0,0,0),(1,0,0),(0,1,0),(0,0,1)], float); Fd = [[0,2,1],[0,1,3],[0,3,2],[1,2,3]]
        base = dehn(V_dummy, Fd, rows_only=True)  # unit corner tetrahedron rows; subtract by adding its mirror? simpler: compute pooled directly
        rec = {'lam': str(lam), 'tile': nm, 'pieces': pr}
        # pooled computation: reuse the core on rows only
        import types
        def pooled(rows):
            angs = []
            for L_, th in rows:
                if not any(abs(th - a) < 1e-8 for a in angs): angs.append(th)
            basis = []; coef = {}
            for i, a in enumerate(angs):
                vec = [mp.mpf(a)] + [mp.mpf(angs[b]) for b in basis] + [mp.pi]
                r = mp.pslq(vec, maxcoeff=300, maxsteps=10**5, tol=mp.mpf(10)**-8)
                if r is not None and r[0] != 0: coef[i] = {b: Fraction(-r[1 + j], r[0]) for j, b in enumerate(basis)}
                else: basis.append(i); coef[i] = {i: Fraction(1)}
            X_ = {b: 0.0 for b in basis}
            for L_, th in rows:
                i = next(k for k, a in enumerate(angs) if abs(th - a) < 1e-8)
                for b, c in coef[i].items(): X_[b] += float(c)*L_
            return {f'{math.degrees(angs[b]):.5f}': X_[b] for b in basis}
        sums = pooled(allrows); rec['tile_sums'] = sums; rec['tile_dehn_zero'] = all(abs(v) < 1e-8 for v in sums.values())
        print(json.dumps(rec, ensure_ascii=False), flush=True); out.append(rec)
json.dump(out, open('data/hexoct-dehn.json', 'w'), indent=1, ensure_ascii=False)
