"""Sphere-unit sizes (DICTO 22 Oct: "among the exact sizes that fit, prefer ones where every solid is about the size of a unit sphere";
10 Nov: "go on with sphere-unit sizes"). In the one world every solid sits in a dodecahedral cell (D, edge 1). Larger exact choices:
 O(L): octahedron with corners at the 6 roof-ridge midpoints of D, edge L = phi^2/sqrt2; skin = 8 congruent caps (D ∩ octant ∩ beyond
       the octahedron's face there);
 I(1): icosahedron of edge 1 in Pacioli's position in O(L) (corners on its edges at the golden section; = #47's I + six Admiral Caps);
       also inscribed in Euclid's cube (one edge in each cube face); skin = 6 Admiral Caps + the 8 caps.
Checks: exact volumes (sympy); D = O(L) + 8 caps and O(L) = I(1) + 6 Admiral Caps by random points (each point of D in exactly one
part); radii table old/new. Usage: python sizes.py"""
import itertools, sys, os, numpy as np, sympy as sp
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import phi, DOD
from scipy.spatial import ConvexHull
r5 = sp.sqrt(5); P = (1 + r5) / 2
VD = (15 + 7 * r5) / 4; Ls = P ** 2 / sp.sqrt(2); VO = sp.sqrt(2) / 3 * Ls ** 3; VI = 5 * (3 + r5) / 12
cap = sp.simplify((VD - VO) / 8); acap = sp.simplify((VO - VI) / 6)
print(f'exact: V(D) = {sp.N(VD, 10)}, V(O(L)) = {sp.nsimplify(sp.simplify(VO))} = {sp.N(VO, 10)}, V(I(1)) = {sp.N(VI, 10)}')
print(f'       each of the 8 caps = {sp.nsimplify(cap)} = {sp.N(cap, 10)}; each Admiral Cap = {sp.nsimplify(acap)} = {sp.N(acap, 10)}')
p = phi; L = p ** 2 / 2 ** .5; R_O = L / 2 ** .5           # = phi^2/2
D = np.unique(np.round(DOD, 12), axis=0); HD = ConvexHull(D)
Ov = np.vstack([np.eye(3) * R_O, -np.eye(3) * R_O])
def cyc(v): return [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]
Iv = np.unique(np.round(np.array([np.array(w) * np.array(sg) for w in cyc((0, 0.5, p / 2)) for sg in itertools.product((1, -1), repeat=3)]), 12), axis=0)
HO = ConvexHull(Ov); HI = ConvexHull(Iv)
ridge_mid = all(any(np.allclose(v, (a + b) / 2) for a, b in itertools.combinations(D, 2) if abs(np.linalg.norm(a - b) - 1) < 1e-9) for v in Ov)
on_O_edges = all(abs(np.abs(v).sum() - R_O) < 1e-9 for v in Iv)
in_cube_faces = all(abs(np.abs(v).max() - p / 2) < 1e-9 for v in Iv)
print(f'O(L) corners = midpoints of dodecahedron edges (the roof ridges): {ridge_mid}; I(1) corners on the octahedron (Pacioli): {on_O_edges}; on the faces of Euclid\'s cube: {in_cube_faces}')
inside = lambda X, H: np.all(X @ H.equations[:, :3].T + H.equations[:, 3] < 1e-12, axis=1)
rs = np.random.default_rng(7); X = rs.uniform(-1.5, 1.5, (400000, 3)); X = X[inside(X, HD)]
inO = inside(X, HO); inI = inside(X, HI)
# caps: D ∩ octant ∩ {s.x >= R_O}; for each point outside O: its octant's cap must contain it, and no other cap
sgn = np.sign(X); beyond = np.sum(X * sgn, axis=1) >= R_O - 1e-12
caps_ok = np.all(inO ^ beyond)                               # each point of D: in O, or in exactly its own octant's cap
pac_ok = np.all(inI <= inO)                                  # I inside O
vol_ok = abs(HO.volume - float(VO)) < 1e-9 and abs(HI.volume - float(VI)) < 1e-9 and abs(HD.volume - float(VD)) < 1e-9
print(f'points of D in O(L) or in exactly one cap: {caps_ok}; I(1) inside O(L): {pac_ok}; hull volumes match the exact ones: {vol_ok}')
R = lambda k: {'D': p * 3 ** .5 / 2, 'C': p * 3 ** .5 / 2, 'T': p * 3 ** .5 / 2, 'O old': p / 2, 'O new': p ** 2 / 2, 'CO': p / 2 ** .5,
              'I old': 0.9510565163 / p, 'I new': 0.9510565163, 'RD': p}[k]
print('surrounding-sphere radii: ' + ', '.join(f'{k} {R(k):.4f}' for k in ['D', 'C', 'T', 'O old', 'O new', 'CO', 'I old', 'I new', 'RD']))
old = [R(k) for k in ['D', 'C', 'T', 'O old', 'CO', 'I old', 'RD']]; new = [R(k) for k in ['D', 'C', 'T', 'O new', 'CO', 'I new', 'RD']]
print(f'largest/smallest radius: before {max(old) / min(old):.3f}, after {max(new) / min(new):.3f}')
print('FINAL ok' if ridge_mid and on_O_edges and caps_ok and pac_ok and vol_ok else 'FINAL FAIL')
