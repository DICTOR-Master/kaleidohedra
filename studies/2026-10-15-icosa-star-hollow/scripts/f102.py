# DICTO 2026-10-15: "can't we get it down to 102 fused pieces?" (the Hecatodihedron has 102 faces). Symmetry count: the pieces come in
# sets of 1, 12, 20, 30 and 60; splitting the core into its 20 Cleo-Icos, one grouping gives exactly 20 + 20 + 20 + 12 + 30 = 102:
#   inner Cleo-Ico + its 3 Y | bipyramid + its 3 X | cap | flat pentagonal pyramid + twisted pentagonal frustum | t1
# Check each fused piece: are the parts joined face to face, and is the union convex?
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
J = json.load(open('cleo_heca.json')); FU = json.load(open('cleo_heca_fusions.json'))
P = lambda m: np.array(m['v']); vol = lambda Q: ConvexHull(Q).volume
core = P(J['core icosahedron'][0]); CH = ConvexHull(core)
inner = [np.vstack([core[t], [0, 0, 0]]) for t in CH.simplices]
bip = [P(m) for m in FU['Cleo-Ico + tripyr (to dodecahedron)']]; X = [P(m) for m in J['X']]; Y = [P(m) for m in J['Y']]
fp = [P(m) for m in J['flat pentagonal pyramid']]; fr = [P(m) for m in J['twisted pentagonal frustum']]; caps = [P(m) for m in J['cap (to Hecatodihedron)']]; t1 = [P(m) for m in J['t1']]
key = lambda p: tuple(np.round(p, 4))
def shared_face(A, B):     # 3 or more common corners
    a = {key(p) for p in A}; return sum(key(p) in a for p in B) >= 3
def group(base, cands, k):
    out = []
    for B in base:
        mine = sorted([C for C in cands if shared_face(B, C)], key=lambda C: np.linalg.norm(C.mean(0) - B.mean(0)))[:k]
        out.append((B, mine))
    return out
def report(name, G):
    used = sum(len(m) for _, m in G); conv = 0; vols = set()
    for B, m in G:
        U = np.unique(np.round(np.vstack([B] + m), 6), axis=0); s = vol(B) + sum(map(vol, m))
        conv += abs(vol(U) - s) < 1e-6; vols.add(round(s, 5))
    return f'{len(G):3d} x {name}: parts per piece {sorted({len(m) for _, m in G})}, convex {conv} of {len(G)}, volume(s) {sorted(vols)}'
gi = group(inner, Y, 3); gb = group(bip, X, 3); gp = [(F, [R for R in fr if shared_face(F, R)]) for F in fp]
out = [report('inner Cleo-Ico + 3 Y', gi), report('bipyramid + 3 X', gb), report('flat pentagonal pyramid + frustum', gp),
       f' 20 x cap (alone)', f' 30 x t1 (alone)']
allY = {id(c) for _, m in gi for c in m}; allX = {id(c) for _, m in gb for c in m}
out.append(f'every Y used once: {len(allY) == 60}; every X used once: {len(allX) == 60}; total pieces {len(gi) + len(gb) + len(gp) + len(caps) + len(t1)}')
print('\n'.join(out)); open('f102.txt', 'w').write('\n'.join(out) + '\n')
