# Does the chain ID -> D -> cage -> RT continue outward at a golden step? Sizes in the chain's own units (dodecahedron edge 1). For
# the RT at the end, list every form that wraps it naturally (touching: its corners on our faces, edge midpoints, corners), and
# compare each wrapper with the forms already in the chain (ID phi/2, D 1, I phi which shares the ID core, cage 1/phi): a ratio
# that is an exact power of phi means the chain repeats.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('touch_screen.py').read().split('out = []')[0].replace("__file__.replace('touch_screen.py', 'network_screen.py')", "'network_screen.py'"))
rt_edge = np.sqrt(45 - 18 * np.sqrt(5)) / 2   # the cage of edge 1/phi sits in an RT whose edge is cage/0.567101 (rt_ti.py)
H = ConvexHull(np.vstack([ref['I'] * PHI, ref['D']])); RTc = np.vstack([ref['I'] * PHI, ref['D']])
e_c = min(np.linalg.norm(RTc[i] - RTc[j]) for i in range(32) for j in range(i) if np.linalg.norm(RTc[i] - RTc[j]) > 1e-9)
print(f'chain RT edge {rt_edge:.6f}; the hull of I(phi) and D(1) (their dual compound) is an RT of edge {e_c:.6f}')
chain = {'ID': PHI / 2, 'D': 1.0, 'I': PHI, 'TI': 1 / PHI, 'RT': rt_edge}
a = info['RT']
for Y in FORMS:
    b = info[Y]
    for label, ok, ri, ro in [('RT corners on its face centres', same(a['cdir'], b['fdir']), a['R'], b['r']),
                              ('RT corners on its edge midpoints', same(a['cdir'], b['mdir']), a['R'], b['m']),
                              ('RT corners on its corners', same(a['cdir'], b['cdir']), a['R'], b['R']),
                              ('RT edges touching its face centres', same(a['mdir'], b['fdir']), a['m'], b['r'])]:
        if not ok: continue
        ye = rt_edge * ro / ri      # wrapper edge length in chain units
        if not np.all((ref['RT'] * rt_edge * 0 + a['V'] * (rt_edge)) @ (b['F'][:, :3] / 1).T + b['F'][:, 3] * ye <= 1e-7): pass
        for X, xe in chain.items():
            if X != Y: continue
            k = np.log(ye / xe) / np.log(PHI)
            tag = f'= {X} of the chain x phi^{round(k)}' if abs(k - round(k)) < 1e-6 else f'(x{ye / xe:.6f} of the chain {X}, not golden)'
            print(f'  {Y} wrapping RT ({label}): edge {ye:.6f} {tag}')
        if Y not in chain: print(f'  {Y} wrapping RT ({label}): edge {ye:.6f}')
