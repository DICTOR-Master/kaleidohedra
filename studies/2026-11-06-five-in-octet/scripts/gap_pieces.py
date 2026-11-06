"""DICTO 11-06: "if each nested shell arrangement used the fractal pieces of the same solids to fill the gaps: Cleo-Icos, pentagonal
pyramids, Antonius etc". For the nest O > I > D > C > T: split each gap into its natural pieces and compare each piece with the solids'
own centre pyramids (face + centre: the tetrahedron's Q (#44), the octahedron's, the cube's, the icosahedron's = Cleo-Icos, the
dodecahedron's pentagonal pyramid) at any scale (shape test: sorted edge lengths up to scale, and volume)."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('nest.py').read().split("def inside")[0])
def pyramids(V):   # centre pyramids of a solid: (face corners + centre)
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
    c = V.mean(0); return [np.vstack([V[list(s)], c]) for s in F.values()]
def sig(P):
    P = np.unique(np.round(P, 9), axis=0); D_ = np.linalg.norm(P[:, None] - P[None], axis=2)[np.triu_indices(len(P), 1)]
    h = ConvexHull(P); hull_edges = set()
    for s in h.simplices:
        for a, b in itertools.combinations(s, 2): hull_edges.add(tuple(sorted((a, b))))
    L = sorted(np.linalg.norm(P[a] - P[b]) for a, b in hull_edges); return len(P), np.array(L) / max(L), h.volume, max(L)
REF = {'Q (tetrahedron centre pyramid, #44)': pyramids(T)[0], 'octahedron centre pyramid': pyramids(O)[0], 'cube centre pyramid': pyramids(C)[0],
       'Cleo-Icos (icosahedron centre pyramid)': pyramids(I)[0], 'pentagonal pyramid (dodecahedron centre pyramid)': pyramids(D)[0]}
def match(P):
    n, s, v, L = sig(P); out = []
    for name, R in REF.items():
        n2, s2, v2, L2 = sig(R)
        if n == n2 and len(s) == len(s2) and np.allclose(s, s2, atol=1e-6): out.append(f'{name} x{L / L2:.6f}')
    return out or ['no match']
pieces = {}
# I - D: over each D face (pentagon), the I corner above it -> pentagonal pyramid; over each I edge, its 2 ends + the 2 D corners of its 2 faces -> tetrahedron
hD = ConvexHull(D); FD = {}
for eq, sp in zip(hD.equations, hD.simplices): FD.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
pp = []
for key, s in FD.items():
    n = np.array(key[:3]); apex = I[np.argmax(I @ n)]; pp.append(np.vstack([D[list(s)], apex]))
pieces['I-D pentagonal caps (I corner over D face)'] = pp
DI = np.linalg.norm(I[:, None] - I[None], axis=2); e = DI[DI > 1e-9].min()
et = []
for a, b in itertools.combinations(range(12), 2):
    if abs(DI[a, b] - e) > 1e-9: continue
    m = (I[a] + I[b]) / 2; near = D[np.argsort(np.linalg.norm(D - m, axis=1))[:2]]; et.append(np.vstack([I[a], I[b], near]))
pieces['I-D edge wedges (I edge + 2 D corners)'] = et
vI, vD = ConvexHull(I).volume, ConvexHull(D).volume
tot = sum(ConvexHull(p).volume for p in pp) + sum(ConvexHull(p).volume for p in et)
print(f"I - D = {vI - vD:.6f}; 12 caps + 30 wedges = {tot:.6f}")
# C - T: four corner pyramids
ct = [np.vstack([c, T[np.argsort(np.linalg.norm(T - c, axis=1))[:3]]]) for c in C if np.prod(np.sign(c)) < 0]
pieces['C-T corner pyramids'] = ct
print(f"C - T = {ConvexHull(C).volume - ConvexHull(T).volume:.6f}; 4 corners = {sum(ConvexHull(p).volume for p in ct):.6f}")
for name, ps in pieces.items():
    print(f"{name}: {len(ps)} pieces, volume each {ConvexHull(ps[0]).volume:.6f}; matches: {match(ps[0])}")
# outward pyramid heights vs the solids' own centre pyramids
for nm, outer, inner in (('I over D', I, D), ('C over T', C, T)):
    rin = abs(ConvexHull(inner).equations[0, 3]); Rout = np.linalg.norm(outer[0])
    print(f"{nm}: cap height {Rout - rin:.6f} vs inner centre-pyramid height {rin:.6f} (ratio {(Rout - rin) / rin:.6f})")
print('FINAL ok')
