"""Step 9 (27 Nov 2026): are the fair dice from the cube + octahedron pieces in the Aequi catalogue? With Claude (Anthropic).
For each fair die (fairdice_centroid.json): its symmetry group (from the signed permutations that keep its pattern, named by
counting rotations, inversion and mirrors) and its combinatorial type (face-adjacency graph with side counts). Catalogue: every
die of catalogue 2 (app_dice.json: directions from the extension study's DIRS, one depth per orbit) and of the first 1232 with
the same face count N; its graph built from its planes. A fair die is NEW AS A TYPE if no catalogue die of the same group and N
has an isomorphic graph; if one does, it is reported as a possible match (the catalogue die may be a member of its family).
Groups of order 1 and 2 are not in the catalogue at all (it starts at order 4)."""
import os, sys, json, itertools
import numpy as np, networkx as nx
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-certify-extend/scripts'))
import importlib.util
spec = importlib.util.spec_from_file_location('g', os.path.join(ST, '2026-11-24-aequi-certify-extend/scripts/groups.py'))
gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm); DIRS = gm.DIRS
def graph(normals, depths):
    U = np.asarray(normals, float); d = np.asarray(depths, float)
    H = HalfspaceIntersection(np.hstack([U, -d[:, None]]), np.zeros(3)); P = H.intersections
    on = [set(np.where(np.abs(U @ p - d) < 1e-7)[0]) for p in P]
    G = nx.Graph()
    for k in range(len(U)):
        G.add_node(k, sides=sum(1 for s in on if k in s))
    for s in on:
        for a, b in itertools.combinations(sorted(s), 2):
            # adjacent faces share an edge = two common vertices
            if sum(1 for t in on if a in t and b in t) >= 2: G.add_edge(a, b)
    return G
def group_name(mats):
    order = len(mats); rot = [M for M in mats if np.linalg.det(M) > 0]; inv = any(np.allclose(M, -np.eye(3)) for M in mats)
    mir = sum(1 for M in mats if np.linalg.det(M) < 0 and abs(np.trace(M) - 1) < 1e-9)
    four = any(np.linalg.det(M) > 0 and abs(np.trace(M) - 1) < 1e-9 for M in mats)            # rotation by 90 degrees
    three = any(np.linalg.det(M) > 0 and abs(np.trace(M)) < 1e-9 for M in mats)               # rotation by 120 degrees
    r = len(rot)
    table = {(48,): 'Oh', (24, True): 'Th', (24, False, 6): 'Td', (24, False, 0): 'O'}
    if order == 48: return 'Oh'
    if order == 24: return 'Th' if inv else ('Td' if mir == 6 else 'O')
    if order == 16: return 'D4h'
    if order == 12: return 'T' if r == 12 else ('D3d' if inv else 'C6v?')
    if order == 8:
        if r == 8: return 'D4'
        if inv: return 'D2h' if not four else 'C4h'
        return 'D2d' if mir == 2 else 'C4v'
    if order == 6: return 'D3' if r == 6 else ('S6' if inv else 'C3v')
    if order == 4:
        if r == 4: return 'C4' if four else 'D2'
        if inv: return 'C2h'
        return 'S4' if mir == 0 else 'C2v'
    if order == 3: return 'C3'
    if order == 2: return 'C2' if r == 2 else ('Ci' if inv else 'Cs')
    return 'C1'
SG = []
for perm in itertools.permutations(range(3)):
    for sgn in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i, j in enumerate(perm): M[i, j] = sgn[i]
        SG.append(M)
R = json.load(open(os.path.join(HERE, '../fairdice.json'))); C = json.load(open(os.path.join(HERE, '../fairdice_centroid.json')))
fair = {c['index']: c for c in C if c['fair']}
retry = os.path.join(HERE, '../logs/fair_centroid_retry.log')
if os.path.exists(retry) and any('die 9:' in l and 'fair True' in l for l in open(retry)): pass
# piece centres to recover each die's symmetry matrices
exec(open(os.path.join(HERE, 'fairsearch.py')).read().split('from ortools.sat.python import cp_model')[0].split('# symmetry: the 48')[0])
cenp = []
for P in polys:
    c = np.mean([np.array([float(x) for x in v]) / np.linalg.norm([float(x) for x in v]) for v in P], axis=0); cenp.append(c / np.linalg.norm(c))
cenp = np.array(cenp)
def mats_of(faces):
    fs = set(tuple(F) for F in faces); out = []
    for M in SG:
        img = [int(np.argmin(np.linalg.norm(cenp - M @ c, axis=1))) for c in cenp]
        if set(tuple(sorted(img[i] for i in F)) for F in faces) == fs: out.append(M)
    return out
cat = {}
A = json.load(open(os.path.join(ST, '2026-11-24-aequi-catalogue-2/app_dice.json')))
for d in A:
    if d['N'] not in (16, 24, 48): continue
    U = np.vstack([DIRS[i] for o in d['orbits'] for i in o]); dep = np.concatenate([[dd] * len(o) for o, dd in zip(d['orbits'], d['depths'])])
    U = U / np.linalg.norm(U, axis=1)[:, None]
    try: cat.setdefault((d['group'], d['N']), []).append((d['no'], graph(U, dep)))
    except Exception as e: print('catalogue die', d['no'], 'not built:', e)
print('catalogue dice built per (group, N):', {k: len(v) for k, v in sorted(cat.items())}, flush=True)
out = []
for idx, r in enumerate(R):
    if idx not in fair and not (idx == 9): continue
    if idx == 9 and idx not in fair: continue
    n = np.array(fair[idx]['normals']); Gd = graph(n / np.linalg.norm(n, axis=1)[:, None], 1 / np.linalg.norm(n, axis=1))
    g = group_name(mats_of(r['faces']))
    nm = lambda a, b: a['sides'] == b['sides']
    hits = [no for no, Gc in cat.get((g, r['N']), []) if nx.is_isomorphic(Gd, Gc, node_match=nm)]
    out.append(dict(index=idx, N=r['N'], group=g, order=r['symmetry_order'], catalogue_same_type=hits[:20], new_type=not hits))
    print(f'die {idx}: N {r["N"]} {g}: ' + (f'same type as catalogue Nos. {hits[:8]}' if hits else ('NEW TYPE' if (g, r['N']) in cat or r['symmetry_order'] < 4 else 'NEW TYPE (no catalogue dice of this group and N)')), flush=True)
json.dump(out, open(os.path.join(HERE, '../catalogue_match.json'), 'w'), indent=1)
from collections import Counter
print('summary new types by group:', sorted(Counter((o['N'], o['group']) for o in out if o['new_type']).items()))
print('summary possible matches:', sorted(Counter((o['N'], o['group']) for o in out if not o['new_type']).items()))
print('FINAL ok' if out else 'FINAL FAIL')
