# Step 19 (DICTO: "cut the golden region into Bodhi pieces"). Float.
# The golden region of one bcc cell: the Voronoi cell V minus the cut golden envelopes (rhombic triacontahedra cut at the joints)
# of every nearby copy. Cut it by every envelope face plane that crosses it (the full arrangement of golden planes: canonical).
# Each piece: faces golden (perpendicular to a 2-fold axis), on V's walls (artificial cell cuts), or on joint planes (star tips).
# Then kinds (congruence) and comparison with the five Bodhi pieces (shape up to scale).
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, '../_lib'); import geomcheck as gc
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T']); r = np.linalg.norm(O, axis=1)
ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9]); D2 = np.vstack([ax['2'], -ax['2']])
G = json.load(open('data/gaps.json')); V = np.array(G['V']); EV = ConvexHull(V).equations
Ec = np.array(json.load(open('data/bodhi-envelope-cut.json'))['envelope_cut']); EE = ConvexHull(Ec).equations
B = np.array([T[0] + T[1], T[0] + T[2], T[0]]).T
near = [B @ np.array(m, float) for m in itertools.product(range(-2, 3), repeat=3)]
near = [c for c in near if np.linalg.norm(c) < 2.2]
envs = [EE - np.c_[np.zeros((len(EE), 3)), EE[:, :3] @ c] for c in near]
def uniq(E):
    out = []
    for e in E:
        e = e / np.linalg.norm(e[:3])
        if not any(np.allclose(e, q, atol=1e-9) for q in out): out.append(e)
    return np.array(out)
planes = uniq(np.vstack(envs))
def poly(H):
    H = np.array(H); nrm = np.linalg.norm(H[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if rr.status != 0 or rr.x[3] < 1e-7: return None
    X = np.unique(np.round(HalfspaceIntersection(H, rr.x[:3]).intersections, 10), axis=0)
    return (H, X) if len(X) >= 4 and ConvexHull(X).volume > 1e-10 else None
def inside_env(X):   # is the convex piece (corners X) inside some envelope (all corners inside one envelope)?
    return any(np.all(X @ E[:, :3].T + E[:, 3] <= 1e-9) for E in envs)
def touches_env_interior(H):
    return [E for E in envs if poly(list(H) + list(E)) is not None]
pieces, stack = [], [list(EV)]
while stack:
    H = stack.pop(); P = poly(H)
    if P is None: continue
    H, X = P
    if inside_env(X): continue
    hit = touches_env_interior(H)
    if not hit: pieces.append(X); continue
    # split by a plane of an envelope that crosses the piece
    for e in planes:
        s = X @ e[:3] + e[3]
        if s.max() > 1e-8 and s.min() < -1e-8:
            stack.append(list(H) + [e]); stack.append(list(H) + [-e]); break
    else:
        pieces.append(X)
vol = sum(ConvexHull(X).volume for X in pieces)
cellgap = ConvexHull(V).volume - ConvexHull(Ec).volume
def face_types(X):
    h = ConvexHull(X); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    t = []
    for e in pl:
        n = e[:3]
        if np.max(D2 @ n) > 1 - 1e-7: t.append('golden')
        elif any(np.allclose(e, q, atol=1e-7) for q in EV): t.append('cell wall')
        else: t.append('other')
    return t
kinds = gc.kinds(pieces, gc.group(ax))
out = [f'golden region of one cell: {vol:.6f} (expected V - cut envelope = {cellgap:.6f}); {len(pieces)} pieces, {len(kinds)} kinds',
       f'pieces with only golden faces: {sum(1 for X in pieces if set(face_types(X)) == {"golden"})}; touching the cell walls: {sum(1 for X in pieces if "cell wall" in face_types(X))}; other faces (star tips): {sum(1 for X in pieces if "other" in face_types(X))}']
# compare with the Bodhi pieces (shape up to scale: corner count, face count, edge-length ratios)
def sig(P):
    P = np.unique(np.round(P, 9), axis=0); E = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); return len(P), tuple(np.round(np.array(E) / E[-1], 4))
bodhi = {}
for b, nm in [('B1', 'Vajra (fine)'), ('B2', 'Chatra'), ('B3', 'Mudra'), ('B4', 'Crown Jewel'), ('B5', 'Diadem')]:
    bodhi[sig(np.array(json.load(open(f'../2026-10-12-bodhi-pieces/data/bodhi-{b}-unit.json'))['vertices']))] = nm
match = {}
for c, i in kinds:
    nm = bodhi.get(sig(pieces[i]))
    ft = face_types(pieces[i])
    out.append(f'   {c:3d} x {len(pieces[i])} corners, faces ' + ', '.join(f'{ft.count(k)} {k}' for k in sorted(set(ft))) + f', volume {ConvexHull(pieces[i]).volume:.6f}' + (f'  = {nm}' if nm else ''))
    if nm: match[nm] = match.get(nm, 0) + c
out.append(f'Bodhi pieces among them: {match if match else "none"}')
print('\n'.join(out)); open('data/golden-cut.txt', 'w').write('\n'.join(out) + '\n')
json.dump([X.tolist() for X in pieces], open('data/golden-cut.json', 'w'))
