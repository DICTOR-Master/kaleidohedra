# DICTO 2026-10-11: keep the tip, cut the band's side ring with sloping planes. Two plane families:
#  A: the sloping face planes of the turned-over small pyramid P(1/phi), extended across the band;
#  B: planes parallel to the outer sloping faces, through the edges of the small pyramid's base.
# For each family list the convex cells of the ring (band minus the small pyramid): volume, edge lengths, and whether a cell is a
# known piece (similar to a kit piece, at a phi-power size).
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
PHI = (1 + 5 ** .5) / 2
kit = json.load(open(sys.argv[1]))
def piece(role):
    for p in kit:
        if p['role'] == role: return np.array(p['vertices'])
ref = {r: piece(r) for r in ('axe', 'fuji', 'cleo', 't1', 't2', 't3', 't4', 't5', 't6', 'T2', 'j2')}
def pyramid(role):
    V = ref[role]
    if role == 'j2': return V[0], V[1:]
    H = ConvexHull(V); c = V.mean(0)
    # FUJI: apex = vertex off the 6-vertex plane
    for i in range(len(V)):
        rest = np.delete(V, i, 0); n = np.cross(rest[1] - rest[0], rest[2] - rest[0])
        if np.all(abs((rest - rest[0]) @ n) < 1e-6): return V[i], rest
def sig(V):
    V = np.array(V); e = sorted(np.linalg.norm(V[i] - V[j]) for i, j in itertools.combinations(range(len(V)), 2)); return np.array(e)
def known(V):
    if len(V) not in (4, 5, 6, 7): return ''
    hullv = ConvexHull(V).volume; out = []
    for r, R in ref.items():
        if len(R) != len(V): continue
        s = (hullv / ConvexHull(R).volume) ** (1 / 3)
        a, b = sig(V), sig(R) * s
        if len(a) == len(b) and np.allclose(a, b, atol=1e-5):
            k = np.log(s) / np.log(PHI); out.append(f'{r}·φ^{k:.2f}' if abs(k - round(k)) > 1e-4 else f'{r}·φ^{round(k)}')
    return ', '.join(out)
def cells(halfs_base, planes, hole):
    out = []
    for signs in itertools.product((1, -1), repeat=len(planes)):
        H = list(halfs_base) + [np.r_[s * n, s * d] for s, (n, d) in zip(signs, planes)]
        A = np.array(H)
        # Chebyshev centre: max r s.t. A x + r|n| <= -b
        norms = np.linalg.norm(A[:, :3], axis=1)
        res = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], norms], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
        if not res.success or res.x[3] < 1e-7: continue
        x0 = res.x[:3]
        if np.all(hole @ np.r_[x0, 1] < 0): continue          # inside the small pyramid: not part of the ring
        V = HalfspaceIntersection(A, x0).intersections
        V = np.unique(np.round(V, 9), axis=0); out.append(V)
    return out
for role in ('j2', 'fuji'):
    apex, base = pyramid(role)
    vP = ConvexHull(np.vstack([apex, base])).volume
    big = apex + PHI * (np.vstack([apex, base]) - apex)
    band = ConvexHull(np.vstack([base, big[1:]]))
    c1 = base.mean(0); small = c1 - (np.vstack([apex, base]) - c1) / PHI     # point-mirrored P(1/phi)
    sh = ConvexHull(small); hole = sh.equations
    # the small pyramid's sloping faces (exclude its base, which lies in the band's top plane)
    top_n = band.equations[np.argmax(band.equations[:, :3] @ (apex - c1) / np.linalg.norm(apex - c1))][:3]
    eqs = np.unique(np.round(hole, 9), axis=0)
    slopeA = [(e[:3], e[3]) for e in eqs if abs(abs(e[:3] @ top_n) - 1) > 1e-6]
    # family B: planes parallel to the outer sloping faces of phi*P, through the small pyramid's base edges
    outer = np.unique(np.round(band.equations, 9), axis=0)
    outer = [e for e in outer if abs(abs(e[:3] @ top_n) - 1) > 1e-6]
    sb = small[1:]                                             # small pyramid base corners (in the top plane)
    slopeB = []
    for e in outer:
        n = e[:3]; d = -max(sb @ n)                            # through the base corner farthest along n
        slopeB.append((n, d))
    for name, planes in (('A', slopeA), ('B', slopeB)):
        C = cells(np.unique(np.round(band.equations, 9), axis=0), planes, hole)
        vols = [ConvexHull(V).volume for V in C]
        print(f'\n{role.upper()} family {name}: {len(planes)} sloping planes -> {len(C)} cells, total {sum(vols) / vP:.6f} x P (should be 3)')
        kinds = {}
        for V, v in zip(C, vols):
            k = (len(V), round(v / vP, 5), tuple(np.round(sig(V), 4)))
            kinds.setdefault(k, 0); kinds[k] += 1
        for (nv, v, s), n in sorted(kinds.items(), key=lambda x: -x[0][1]):
            V = next(V for V in C if len(V) == nv and abs(ConvexHull(V).volume / vP - v) < 1e-5)
            print(f'   {n} x  {nv} corners, volume {v} P, edges {list(s)[:8]}{"…" if len(s) > 8 else ""}  {known(V)}')
