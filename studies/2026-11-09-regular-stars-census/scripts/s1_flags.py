# s1_flags.py -- every regular polytope (convex or star) with the symmetry of the regular solids in 3D and 4D, from mirror chains
# (Wythoff), exactly. Study 2026-11-09-regular-stars-census.
# For each symmetry group G (3D: Td, Oh, Ih; 4D: A4, B4, F4, H4) the mirrors are found exactly from a corner set, every chain
# m_0..m_{d-1} with m_0 fixed is formed, its flag q_0..q_{d-1} is built (regstar.flag_from_mirrors), the flag Gram identity is checked
# exactly, and the Schlafli symbol is read from the mirror angles. Polytopes are kept when the chain's reflections generate all of G
# (so the polytope has the full symmetry; proper subgroups give the convex polytopes of the smaller groups, found under their own
# G). Counts (corners, edges, faces, cells) are orbit sizes of the flag points; the density is the number of chambers inside the
# flag cone. Known-case check: the convex list (5 + 6) and Coxeter's star list (4 Kepler-Poinsot + 10 Schlafli-Hess) must come out.
# Usage: python3 -u s1_flags.py <out json>
import sys, json, time
import numpy as np
from regstar import *
import turnlib as TL
OUT = sys.argv[1]; T0 = time.time()

GROUPS = [('Td', 3, TL.tetrahedron()), ('Oh', 3, TL.cube()), ('Ih', 3, TL.icosahedron()),
          ('A4', 4, TL.simplex4()), ('B4', 4, TL.tesseract()), ('F4', 4, TL.cell24()), ('H4', 4, TL.cell600())]
ORDER = {'Td': 24, 'Oh': 48, 'Ih': 120, 'A4': 120, 'B4': 384, 'F4': 1152, 'H4': 14400}
KNOWN = {'Td': ['{3,3}'], 'Oh': ['{3,4}', '{4,3}'], 'Ih': ['{3,5}', '{5,3}', '{5/2,5}', '{5,5/2}', '{5/2,3}', '{3,5/2}'],
         'A4': ['{3,3,3}'], 'B4': ['{3,3,4}', '{4,3,3}'], 'F4': ['{3,4,3}'],
         'H4': ['{3,3,5}', '{5,3,3}', '{3,5,5/2}', '{5/2,5,3}', '{5,5/2,5}', '{5,3,5/2}', '{5/2,3,5}', '{5/2,5,5/2}', '{5,5/2,3}',
                '{3,5/2,5}', '{3,3,5/2}', '{5/2,3,3}']}
NAMES = {'{3,3}': 'tetrahedron', '{3,4}': 'octahedron', '{4,3}': 'cube', '{3,5}': 'icosahedron', '{5,3}': 'dodecahedron',
         '{5/2,5}': 'small stellated dodecahedron', '{5,5/2}': 'great dodecahedron', '{5/2,3}': 'great stellated dodecahedron',
         '{3,5/2}': 'great icosahedron', '{3,3,3}': '5-cell', '{3,3,4}': '16-cell', '{4,3,3}': 'tesseract', '{3,4,3}': '24-cell',
         '{3,3,5}': '600-cell', '{5,3,3}': '120-cell', '{3,5,5/2}': 'icosahedral 120-cell', '{5/2,5,3}': 'small stellated 120-cell',
         '{5,5/2,5}': 'great 120-cell', '{5,3,5/2}': 'grand 120-cell', '{5/2,3,5}': 'great stellated 120-cell',
         '{5/2,5,5/2}': 'grand stellated 120-cell', '{5,5/2,3}': 'great grand 120-cell', '{3,5/2,5}': 'great icosahedral 120-cell',
         '{3,3,5/2}': 'grand 600-cell', '{5/2,3,3}': 'great grand stellated 120-cell'}
res = []; ok = True
for gname, d, V in GROUPS:
    M = mirrors_of(V)
    G = group_float([refl_mat(m) for m in M]); assert len(G) == ORDER[gname], (gname, len(G))
    chains = enumerate_chains(M, d, starts=(0,) if gname in ('Ih', 'H4', 'Td', 'A4') else tuple(range(len(M))))
    seen = {}
    for ch in chains:
        ms = [M[i] for i in ch]
        sym = '{' + ','.join(mirror_angle(ms[i], ms[i + 1]) for i in range(d - 1)) + '}'
        if 'other' in sym or '2' in sym.replace('5/2', 'x'): continue
        q = flag_from_mirrors(ms, d)
        if q is None: continue
        g_ok, r2 = gram_ok(q)
        assert g_ok, 'flag Gram identity fails'
        if not all(r2[k] > r2[k + 1] for k in range(d - 1)): continue
        ratio = tuple((x / r2[0]).a for x in r2) + tuple((x / r2[0]).b for x in r2)
        k = (sym, ratio)
        if k in seen: continue
        seen[k] = (ms, q, r2)
    print(gname, 'mirrors', len(M), 'chains', len(chains), 'distinct flags', len(seen), round(time.time() - T0, 1), 's', flush=True)
    z = np.array([1.0, 2.0 ** .5, 3.0 ** .5, 5.0 ** .5][:d]) * np.array([1, 0.37, 0.11, 0.023][:d])
    for (sym, ratio), (ms, q, r2) in seen.items():
        Gc = group_float([refl_mat(m) for m in ms], cap=ORDER[gname] + 10)
        full = Gc is not None and len(Gc) == ORDER[gname]
        if not full: continue
        counts = [len(orbit_float(Gc, flv(x))) for x in q]
        # chamber point z: a generic point; density = chambers inside the flag cone
        dens = density(Gc, q, z)
        h2, R2 = r2[-1], r2[0]
        row = dict(group=gname, d=d, symbol=sym, name=NAMES.get(sym, 'unlisted'), counts=counts, density=dens,
                   r2_over_R2=[q5s(x / R2) for x in r2], q=[vs(x) for x in q], r2=[q5s(x) for x in r2], mirrors=[vs(m) for m in ms],
                   g=q5s(R2 / h2), g_float=(R2 / h2).f(), r2_float=[x.f() for x in r2])
        res.append(row)
        print(' ', sym, row['name'], 'counts', counts, 'density', dens, 'R2/h2 =', q5s(R2 / h2), flush=True)
    found = sorted({r['symbol'] for r in res if r['group'] == gname})
    if found != sorted(KNOWN[gname]):
        ok = False; print('MISMATCH', gname, found, 'expected', KNOWN[gname], flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
print('polytopes', len(res), 'time', round(time.time() - T0, 1), 's')
print('FINAL ok' if ok and len(res) == 25 else 'FINAL FAIL: list differs from the known 25 (see MISMATCH lines)')
