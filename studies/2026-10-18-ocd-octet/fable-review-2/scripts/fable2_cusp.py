# Fable review 2 (2026-10-18): the contact points of the step-22 outer corners (float, light). At the golden point A = (s, 0, 2/3) the
# envelope touches the octahedron edge from (0,0,R) to (R,0,0); the +z and +x outer corners both reach A. Solid angle of each at A
# (components of the local direction set octa minus RT), the full octahedron edge wedge for reference. -> data/fable2-cusp.json
import json, os, math, itertools, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, '..', 'data', 'fable2-input.json')))
R, s = D['R'], D['s']; P = np.array(D['planes']); PN, PD = P[:, :3], P[:, 3]
A = np.array([s, 0, 2 / 3]); assert abs(A[0] + A[2] - R) < 1e-12
rng = np.random.default_rng(7); n = 600000; dirs = rng.normal(size=(n, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
eps = 1e-4; pts = A + eps * dirs
octa_n = np.array(list(itertools.product((1, -1), repeat=3)), float)
in_octa = (pts @ octa_n.T <= R + 1e-15).all(1); in_rt = (pts @ PN.T <= PD + 1e-15).all(1)
S = in_octa & ~in_rt; idx = np.where(S)[0]; d = dirs[idx]
tree = cKDTree(d); pairs = tree.query_pairs(0.02, output_type='ndarray')
parent = np.arange(len(idx))
def find(i):
    while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
    return i
for a, b in pairs:
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb
roots = np.array([find(i) for i in range(len(idx))]); labs, counts = np.unique(roots, return_counts=True)
comps = []
for lab, cnt in sorted(zip(labs, counts), key=lambda x: -x[1]):
    sel = roots == lab; cen = d[sel].mean(0)
    comps.append(dict(solid_angle_sr=float(cnt / n * 4 * math.pi), mean_direction=cen.round(4).tolist(), towards='+z corner' if cen[2] > cen[0] else '+x corner'))
out = dict(mark='DICTO · dictospheres.com', A=A.tolist(), A_is_golden_point_of_edge='divides the octahedron edge (0,0,R)-(R,0,0) at s : 2/3 = 1 : phi from the +z corner',
           directions=n, octa_edge_wedge_sr=float(in_octa.mean() * 4 * math.pi), octa_minus_RT_sr=float(S.mean() * 4 * math.pi), components=comps[:4], components_total=len(comps),
           reference=dict(regular_tetrahedron_corner_sr=0.5513, cube_corner_sr=math.pi / 2, octahedron_corner_sr=1.3593),
           wedge_top_sliver_max_width=s - s / ((1 + 5 ** .5) / 2), wedge_top_sliver_note='diamond |x|+|y| <= s minus the RT rhombus at z = 2/3: 4 slivers of width 0 at the two cusps rising to s/phi^2 = 0.157 at (0, +-s, 2/3)')
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, '..', 'data', 'fable2-cusp.json'), 'w'), indent=1, ensure_ascii=False)
