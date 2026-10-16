# Builds src/app/theaetetus-data.js for the Theaetetus world (DICTO 2026-10-15; named by DICTO after Theaetetus, by tradition the first to
# construct the icosahedron): the Cleo core grown to the DICTO Hecatodihedron in DICTO's 102 clean pieces (20 core Cleo-Icos, 20 columns,
# Dharma's 12 frusta, 30 t1, 20 caps) and its 215-piece stations (every layer closed). Inputs: studies/2026-10-15-icosa-star-hollow/data/.
# Usage: python3 scripts/build-theaetetus-data.py
import json, os, numpy as np
from scipy.spatial import ConvexHull
D = 'studies/2026-10-15-icosa-star-hollow/data/'
C102 = json.load(open(D + 'cut102.json'))                                       # scripts/cut102.py
J = json.load(open(D + 'cleo_heca.json')); FU = json.load(open(D + 'cleo_heca_fusions.json'))   # scripts/cleo_heca.py
R102 = {'core Cleo-Ico': 'ccleo', 'column': 'col', 'twisted pentagonal frustum': 'nfru5', 't1': 'nt1', 'cap (to Hecatodihedron)': 'ncap'}
RST = {'core icosahedron': 'core', 'flat pentagonal pyramid': 'fpyr5', 'X': 'tx', 'Y': 'ty', 'twisted pentagonal frustum': 'nfru5', 't1': 'nt1',
       'cap (to Hecatodihedron)': 'ncap'}
def polys(V):
    """Whole faces: hull triangles grouped by plane (normals within 1e-4, offsets within 1e-4; the inputs are stored to 6 places),
    each as a corner list in order round the face."""
    W = np.array(V); h = ConvexHull(W); groups = []
    for e, t in zip(h.equations, h.simplices):
        for G in groups:
            if G['n'] @ e[:3] > 1 - 1e-4 and abs(G['d'] - e[3]) < 1e-4: G['i'].update(t); break
        else: groups.append({'n': e[:3], 'd': e[3], 'i': set(t)})
    out = []
    for G in groups:
        idx = sorted(int(i) for i in G["i"]); Q = W[idx]; c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(G['n'], a)
        out.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return out
piece = lambda role, m: [role, m['v'], polys(m['v'])]
# two stories (DICTO 2026-10-15, "show both"): the stations, every layer a closed solid (215 pieces, each Cleo-Ico fused with the
# dodecahedron's corner pyramid into a bipyramid), and the 102 clean pieces (the dual pair cut by the same 20 cones)
stations = [piece(RST[k], m) for k in ('core icosahedron', 'flat pentagonal pyramid', 'X', 'Y') for m in J[k]]
stations += [piece('bipyr', m) for m in FU['Cleo-Ico + tripyr (to dodecahedron)']]
stations += [piece(RST[k], m) for k in ('twisted pentagonal frustum', 't1', 'cap (to Hecatodihedron)') for m in J[k]]
# the Cleo star (DICTO 2026-10-16, studies/2026-10-16-progenitors steps 9–10): the core's 20 Cleo-Icos, 20 more stood on its faces as spikes
# (the same piece flipped out, apex at twice the face distance), whose tips are the corners of a dodecahedron D'; 12 pentagonal pyramids on
# D''s faces pointing in to the icosahedron's corners; 30 valley tetrahedra along the icosahedron's edges (corners: the edge's two ends and the
# tips of the two spikes beside it); together the 82 pieces fill D' exactly (float check below); D' as glass.
phi = (1 + 5 ** .5) / 2
ico = np.array([p for a, b in ((0.5, phi / 2),) for p in
                [(0, sa * b, sb * a) for sa in (1, -1) for sb in (1, -1)] + [(sb * a, 0, sa * b) for sa in (1, -1) for sb in (1, -1)] +
                [(sa * b, sb * a, 0) for sa in (1, -1) for sb in (1, -1)]])
core = [m for m in C102['core Cleo-Ico']]
assert all(min(np.linalg.norm(ico - np.array(v), axis=1)) < 1e-5 for m in core for v in m['v'][:3]), 'frame differs from the c102 core'
hI = ConvexHull(ico); tips = []; spikes = []
for t in hI.simplices:
    F = ico[t]; tip = 2 * F.mean(0); tips.append(tip); spikes.append({'v': np.round(np.vstack([F, tip]), 6).tolist()})
tips = np.array(tips); hD = ConvexHull(tips); pyrs = []; seen = []
for e in hD.equations:
    if any(np.allclose(e, q, atol=1e-7) for q in seen): continue
    seen.append(e); base = tips[np.abs(tips @ e[:3] + e[3]) < 1e-7]; apex = ico[np.argmax(ico @ e[:3])]
    pyrs.append({'v': np.round(np.vstack([base, apex]), 6).tolist()})
valleys = []
for i, j in [(i, j) for i in range(12) for j in range(i + 1, 12) if abs(np.linalg.norm(ico[i] - ico[j]) - 1) < 1e-9]:
    two = [k for k, t in enumerate(hI.simplices) if i in t and j in t]
    valleys.append({'v': np.round(np.vstack([ico[i], ico[j], tips[two[0]], tips[two[1]]]), 6).tolist()})
vol = lambda V: ConvexHull(np.array(V)).volume
total = 20 * vol(ico[hI.simplices[0]].tolist() + [[0, 0, 0]]) + sum(vol(m['v']) for m in spikes + pyrs + valleys)
assert abs(total - ConvexHull(tips).volume) < 1e-5, ('the Cleo star pieces do not fill D\'', total, ConvexHull(tips).volume)
cleostar = [piece('ccleo', m) for m in core] + [piece('cspike', m) for m in spikes] + [piece('gpyr5', m) for m in pyrs] + \
           [piece('cvalley', m) for m in valleys] + [piece('dprime', {'v': np.round(tips, 6).tolist()})]
views = {'c102': [piece(R102[k], m) for k in R102 for m in C102[k]], 'stations': stations, 'cleostar': cleostar}
out = {'theaetetus': {'views': views}}
open('src/app/theaetetus-data.js', 'w').write('// Generated by scripts/build-theaetetus-data.py (Theaetetus world, the Cleo core). Do not edit.\nexport default '
                                             + json.dumps(out, separators=(',', ':')) + ';\n')
print({k: len(v) for k, v in views.items()}, os.path.getsize('src/app/theaetetus-data.js'), 'bytes')
