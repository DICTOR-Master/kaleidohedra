"""DICTO's conjecture (27 Nov 2026, from his cube and octahedron models): when the Vacuus and Resonus planes are aligned, the gaps
between the two shapes become linear trigonometry for space filling. With Claude (Anthropic).
Step 1 (exact): for each solid, are its Vacuus planes (through O and an edge) and Resonus planes (through O parallel to a face)
mirror planes of the solid, and do the two together give ALL its mirror planes? If yes, the planes cut the gap into congruent
mirror chambers (one piece, reflected, fills it). Numbers in Q(sqrt5) or Q(sqrt2), exact (K class of the Vacuus-Solids study).
Mirror planes found exactly: every mirror swaps some pair of corners u, v (same distance from O), so its normal is u - v; each
candidate is kept only if the reflection maps the corner set onto itself (exact). Snub cube and snub dodecahedron: chiral, no
mirror planes at all (not built here; their coordinates need cubic irrationals)."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-11-25-partial-vacuus/scripts'))
from exact_check import K, cross, dot, sub, scl, faces, polar, solid as solid5
from fractions import Fraction as Fr
def gen2(ts):
    out = []
    for t in ts:
        for q in itertools.permutations(t):
            for sg in itertools.product((1, -1), repeat=3):
                z = tuple(x if s > 0 else -x for x, s in zip(q, sg))
                if not any(all((a - b).iszero() for a, b in zip(z, w)) for w in out): out.append(z)
    return out
def solid(name):
    k = lambda a, b=0: K(a, b, 2); o, z, s2 = k(1), k(0), k(0, 1)
    cube = {'cube': [(o, o, o)], 'cuboctahedron': [(o, o, z)], 'truncated octahedron': [(z, o, 2 * o)],
            'rhombicuboctahedron': [(o, o, o + s2)], 'truncated cuboctahedron': [(o, o + s2, o + 2 * s2)]}
    if name in cube: return gen2(cube[name])
    if name in ('tetrahedron', 'octahedron', 'truncated tetrahedron', 'truncated cube'): return solid5(name, 2)
    return solid5(name, 5)
ARCH = ['truncated tetrahedron', 'cuboctahedron', 'truncated cube', 'truncated octahedron', 'rhombicuboctahedron',
        'truncated cuboctahedron', 'icosidodecahedron', 'truncated dodecahedron', 'truncated icosahedron',
        'rhombicosidodecahedron', 'truncated icosidodecahedron']
CAT = {'truncated tetrahedron': 'triakis tetrahedron', 'cuboctahedron': 'rhombic dodecahedron', 'truncated cube': 'triakis octahedron',
       'truncated octahedron': 'tetrakis hexahedron', 'rhombicuboctahedron': 'deltoidal icositetrahedron',
       'truncated cuboctahedron': 'disdyakis dodecahedron', 'icosidodecahedron': 'rhombic triacontahedron',
       'truncated dodecahedron': 'triakis icosahedron', 'truncated icosahedron': 'pentakis dodecahedron',
       'rhombicosidodecahedron': 'deltoidal hexecontahedron', 'truncated icosidodecahedron': 'disdyakis triacontahedron'}
SOL = [(n, solid(n)) for n in ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron']]
SOL += [(n, solid(n)) for n in ARCH] + [(CAT[n], polar(solid(n))) for n in ARCH]
def same_dir(m, n): return all(c.iszero() for c in cross(m, n))
def add(lst, m):
    if all(c.iszero() for c in m): return
    if not any(same_dir(m, n) for n in lst): lst.append(m)
def reflect(x, m):
    t = 2 * dot(x, m) / dot(m, m); return tuple(a - t * b for a, b in zip(x, m))
def has(V, p): return any(all((a - b).iszero() for a, b in zip(p, w)) for w in V)
rows = []; ok_controls = True
for name, V in SOL:
    F = faces(V)
    edges = set()
    for idx, N, d in F:
        for i in range(len(idx)): edges.add(frozenset((idx[i], idx[(i + 1) % len(idx)])))
    vac, res, mir, cand = [], [], [], []
    for e in edges:
        a, b = tuple(e); add(vac, cross(V[a], V[b]))
    for idx, N, d in F: add(res, N)
    R2 = [dot(v, v) for v in V]
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            if R2[i] == R2[j]: add(cand, sub(V[i], V[j]))
    for m in cand:
        if all(has(V, reflect(v, m)) for v in V): mir.append(m)
    inM = lambda P: sum(1 for m in P if any(same_dir(m, q) for q in mir))
    union = list(vac); [add(union, m) for m in res]
    full = len(union) == len(mir) and inM(union) == len(union)
    r = dict(solid=name, corners=len(V), faces=len(F), edges=len(edges), vacuus=len(vac), resonus=len(res), mirrors=len(mir),
             vacuus_mirrors=inM(vac), resonus_mirrors=inM(res), union=len(union), all_mirrors_exactly=full)
    rows.append(r)
    print(f"{name:28s} V{len(V):3d} F{len(F):3d} | Vacuus {len(vac):3d} ({inM(vac)} mirrors) | Resonus {len(res):3d} ({inM(res)} mirrors) | "
          f"mirrors {len(mir):2d} | Vacuus+Resonus = all mirrors: {full}", flush=True)
exp = {'cube': 9, 'octahedron': 9, 'tetrahedron': 6, 'dodecahedron': 15, 'icosahedron': 15}
ctl = all(r['mirrors'] == exp[r['solid']] for r in rows if r['solid'] in exp)
cc = [r for r in rows if r['solid'] in ('cube', 'octahedron')]
print('control: mirror counts 15, 15, 9, 6, 9 for D I C T O:', ctl, '; cube and octahedron give all 9:', all(r['all_mirrors_exactly'] for r in cc))
import json; json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mirrors.json'), 'w'), indent=1)
print('FINAL ok' if ctl else 'FINAL FAIL (control)')
