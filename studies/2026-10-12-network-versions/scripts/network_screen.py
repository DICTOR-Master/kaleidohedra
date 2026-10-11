# Network versions, step 1 (DICTO 2026-10-12: "any and all possibilities"). The Lotus-type construction for every icosahedral
# form: an outer form Y with smaller copies Z at all its corners (each copy sharing that corner, same turn, as the Lotus seed's
# 12 icosahedra sit in I(phi^2)), and the largest centred inner form X that fits among them. Forms: icosahedron I, dodecahedron D,
# icosidodecahedron ID, rhombic triacontahedron RT (ID's dual), truncated icosahedron TI (the fullerene form); all edge 1 at
# size 1 except RT (short diagonal ... see below), all in one frame. Reported: do the corner copies fit without overlapping,
# do neighbours touch exactly, and at what size the inner form fits (exact golden powers flagged).
import itertools, numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
def cyc(v):
    out = set()
    for s in itertools.product(*[(-1, 1) if x else (1,) for x in v]):
        w = [a * b for a, b in zip(v, s)]
        for k in range(3): out.add(tuple(np.round(np.roll(w, k), 12)))
    return out
def _faces(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-6 for q in E): E.append(e)
    return np.array(E)
def _edges(V):
    d = min(np.linalg.norm(V[0] - w) for w in V[1:])
    return [(a, b) for a, b in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[a] - V[b]) - d) < 1e-9]
def _unit(V):
    return V / min(np.linalg.norm(V[0] - w) for w in V[1:])
# every form is built from one icosahedron, so all share its turn (the dual alignment):
_I = np.array(sorted(cyc((0, 1, PHI))), float)
def form(name):
    if name == 'I': return _unit(_I)
    if name == 'D': return _unit(np.array([-f[:3] / f[3] for f in _faces(_I)]))                 # dual: a corner per face
    if name == 'ID': return _unit(np.array([(_I[a] + _I[b]) / 2 for a, b in _edges(_I)]))      # edge midpoints
    if name == 'TI': return _unit(np.array([p for a, b in _edges(_I) for p in ((2 * _I[a] + _I[b]) / 3, (_I[a] + 2 * _I[b]) / 3)]))
    if name == 'RT':
        ID = np.array([(_I[a] + _I[b]) / 2 for a, b in _edges(_I)])
        W = np.array([-f[:3] / f[3] for f in _faces(ID)])
        return W / min(np.linalg.norm(W[0] - w) for w in W[1:])
FORMS = ['I', 'D', 'ID', 'RT', 'TI']
ref = {f: form(f) for f in FORMS}
for f in FORMS:
    H = ConvexHull(ref[f]); print(f'{f}: {len(ref[f])} corners, faces (merged) ~{len(np.unique(np.round(H.equations, 6), axis=0))}, volume {H.volume:.6f}')
def sat_overlap(A, B):
    HA, HB = ConvexHull(A), ConvexHull(B)
    axes = list(HA.equations[:, :3]) + list(HB.equations[:, :3])
    ea = [A[i] - A[j] for i, j in itertools.combinations(range(len(A)), 2)]
    eb = [B[i] - B[j] for i, j in itertools.combinations(range(len(B)), 2)]
    for u in ea[:60]:
        for v in eb[:60]:
            w = np.cross(u, v)
            if np.linalg.norm(w) > 1e-9: axes.append(w / np.linalg.norm(w))
    for ax in axes:
        a, b = A @ ax, B @ ax
        if a.max() <= b.min() + 1e-7 or b.max() <= a.min() + 1e-7: return False
    return True
def gap(A, B):   # smallest separation along the candidate axes (0 = touching)
    HA, HB = ConvexHull(A), ConvexHull(B); best = 0
    for ax in list(HA.equations[:, :3]) + list(HB.equations[:, :3]):
        a, b = A @ ax, B @ ax; best = max(best, b.min() - a.max(), a.min() - b.max())
    return best
SCALES = {'phi': PHI, 'phi^2': PHI ** 2, 'phi^3': PHI ** 3, '2': 2.0, '1+phi^-1... ': None}
rows = []
for Y in FORMS:
    Yv = ref[Y]
    for Z in FORMS:
        Zv = ref[Z]
        for k in range(1, 5):
            r = PHI ** k                                  # outer edge / corner-copy edge
            outer = Yv * r
            # corner copy: same turn, scaled so that one of its corners sits at the outer corner, pointing the same way
            cz = Zv[np.argmax(Zv @ (Yv[0] / np.linalg.norm(Yv[0])))]   # Z's corner in the direction of Y's first corner
            if np.linalg.norm(np.cross(cz, Yv[0])) > 1e-6: continue   # Z has no corner along Y's corner direction
            copies = [Zv + (y * r - cz) for y in Yv if True]
            # each copy must point the same way as its outer corner: use the corner of Z along that direction
            copies = []
            okdir = True
            for y in Yv:
                d = y / np.linalg.norm(y); j = np.argmax(Zv @ d)
                if np.linalg.norm(np.cross(Zv[j], y)) > 1e-6: okdir = False; break
                copies.append(Zv + (y * r - Zv[j]))
            if not okdir: continue
            Hout = ConvexHull(outer)
            inside = all(np.all(c @ Hout.equations[:, :3].T + Hout.equations[:, 3] <= 1e-7) for c in copies)
            if not inside: continue
            # neighbouring copies: overlap / touch
            cen = [c.mean(0) for c in copies]; dmin = min(np.linalg.norm(cen[0] - c) for c in cen[1:])
            nbr = [i for i in range(1, len(cen)) if abs(np.linalg.norm(cen[0] - cen[i]) - dmin) < 1e-6]
            ov = sat_overlap(copies[0], copies[nbr[0]]); g = gap(copies[0], copies[nbr[0]])
            if ov and g < -1e-6: print(f'outer {Y:2s} (edge phi^{k}), corners {Z:2s}: corner copies OVERLAP', flush=True); continue
            contact = 'touch' if abs(g) < 1e-6 else f'gap {g:.4f}'
            # inner forms: largest centred size that misses every copy
            inner = []
            for X in FORMS:
                lo, hi = 0.0, r * 2
                for _ in range(40):
                    m = (lo + hi) / 2
                    if sat_overlap(ref[X] * m, copies[0]): hi = m   # the copies are one symmetry orbit: one check covers all
                    else: lo = m
                kx = np.log(lo) / np.log(PHI) if lo > 1e-9 else float('nan')
                tag = f'{X} edge {lo:.5f}' + (f' = phi^{round(kx)}' if lo > 1e-9 and abs(kx - round(kx)) < 1e-4 else '')
                inner.append(tag)
            print(f'outer {Y:2s} (edge phi^{k}), corners {Z:2s} (edge 1): corner copies {contact}; inner: ' + '; '.join(inner), flush=True)

