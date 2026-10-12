# Dihedral angles and edge lengths of every kit piece, and of the two rings (J2 and FUJI).
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ring_core import *
from kit_exact import KIT as _K
KIT.update(_K)
al = np.degrees(np.arccos(5 ** .5 / 3)); de = np.degrees(np.arctan(3 - 5 ** .5))
print(f'alpha = {al:.6f}, delta = {de:.6f}')
allD = {}
for k, V in KIT.items():
    E = convex_edges(V)
    ds = sorted(set((round(d, 4), round(l, 4)) for i, j, l, d in E))
    print(f'{k:5s} vol {vol(V):.6f}: ' + ', '.join(f'{d}°/{l}' for d, l in ds))
    for d, l in ds: allD.setdefault(d, set()).add(k)
print('\nall kit dihedral values (deg): ', sorted(allD))
print('smallest:', sorted(allD)[:6])
for nm in ('J2', 'FUJI', 'AXE', 'CLEO'):
    r = ring(nm); P = KIT[nm]; apex, base = pyramid_parts(P)
    print(f'\nring of {nm}: band volume {vol(r["band"]):.9f}, hole {vol(r["hole"]):.9f}, ring {vol(r["band"]) - vol(r["hole"]):.9f} = {(vol(r["band"]) - vol(r["hole"])) / vol(P):.9f} x P')
    # hole inside band? apex on the floor plane?
    Fb = planes(r['band']); inside = np.all(r['hole'] @ Fb[:, :3].T + Fb[:, 3] <= 1e-9)
    floorpl = [e for e in Fb if np.all(np.abs(r['floor'] @ e[:3] + e[3]) < 1e-7)][0]
    print(f'  hole inside band: {inside}; hole apex distance to floor {r["hole_apex"] @ floorpl[:3] + floorpl[3]:.2e}; floor centre {np.linalg.norm(r["hole_apex"] - r["floor"].mean(0)):.2e} from hole apex')
    for i, j, l, d in convex_edges(r['band']): pass
    Eb = convex_edges(P)
    bset = set(map(tuple, np.round(base, 9)))
    for i, j, l, d in Eb:
        isbase = tuple(np.round(P[i], 9)) in bset and tuple(np.round(P[j], 9)) in bset
        if isbase: print(f'  floor edge: length {PHI * l:.6f}, ring dihedral {d:.4f}; top outer edge: {l:.6f}, {180 - d:.4f}; hole rim edge: {l / PHI:.6f}, {180 - d:.4f}')
        else: print(f'  side edge: length {l / PHI:.6f} (phi-1 times {l:.4f}), dihedral {d:.4f}; hole edge: length {l / PHI:.6f}, ring dihedral {360 - d:.4f}')
