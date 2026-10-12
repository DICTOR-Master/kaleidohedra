# Outside-in (2026-10-11): lay the face tiling (2 triangles 1/phi + 2 triangles 1/phi^2 + flat-ended triangle 1/phi^2) on every
# sloping face of the side ring, then list the kit pieces (all sizes, Lotus-frame turns) that can sit exactly behind each tile:
# one face of the piece = the tile, the piece inside the band and clear of the turned-over small pyramid.
import sys, os, itertools, numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selfbuild_sides.py')).read()
exec(src[:src.index('place = {}')])          # kit shapes, band (TV, TE), hole (HV), overlap, clear_of_hole
axis = (apex - base.mean(0)); axis /= np.linalg.norm(axis)
faces = [e for e in np.unique(np.round(TE, 9), axis=0) if abs(abs(e[:3] @ axis) - 1) > 1e-6]
top = base; bot = TV[len(base):]
print(f'{len(faces)} sloping faces')
def tiles_for(e):
    n = e[:3]
    on = lambda P: np.abs(P @ n + e[3]) < 1e-6
    T = top[on(top)]; Bt = bot[on(bot)]
    if len(T) != 2 or len(Bt) != 2: return None
    # order so T[0] sits above B[0]
    if np.linalg.norm(T[0] - Bt[0]) > np.linalg.norm(T[0] - Bt[1]): Bt = Bt[::-1]
    B1, B2 = Bt; T1, T2 = T
    out = []
    if abs(np.linalg.norm(T1 - T2) - 1 * np.linalg.norm(B1 - B2) / PHI) > 1e-6: return 'not the 60-degree trapezoid'
    s = np.linalg.norm(T1 - T2)                       # = 1 in the face's own scale
    u = (B2 - B1) / np.linalg.norm(B2 - B1)
    a = s / PHI; c = s / PHI ** 2
    out.append(('tri 1/phi', np.array([B1, B1 + a * u, T1])))          # bottom-left corner triangle (its apex is T1? check below)
    out.append(('tri 1/phi', np.array([B2, B2 - a * u, T2])))
    # middle: the inverted triangle of side s on T1T2, minus its point below the floor
    M1, M2 = B1 + a * u, B2 - a * u                                   # floor points of the middle
    out.append(('tri 1/phi^2', np.array([T1, T1 + c * (T2 - T1) / s, T1 + c * (M1 - T1) / np.linalg.norm(M1 - T1)])))
    out.append(('tri 1/phi^2', np.array([T2, T2 + c * (T1 - T2) / s, T2 + c * (M2 - T2) / np.linalg.norm(M2 - T2)])))
    h = np.array([T1 + c * (T2 - T1) / s, T2 + c * (T1 - T2) / s, T2 + c * (M2 - T2) / np.linalg.norm(M2 - T2), M2, M1,
                  T1 + c * (M1 - T1) / np.linalg.norm(M1 - T1)])
    out.append(('flat-ended 1/phi^2', h))
    return out
def area(P):
    return np.linalg.norm(sum(np.cross(P[i], P[(i + 1) % len(P)]) for i in range(len(P)))) / 2
for fi, e in enumerate(faces[:1]):                    # all sloping faces are alike up to the symmetry: report one
    T = tiles_for(e)
    if not isinstance(T, list): print('face', fi, T); continue
    tot = sum(area(P) for _, P in T); outer = None
    print(f'face {fi}: tile areas sum {tot:.6f}')
    for name, P in T:
        sides = [np.linalg.norm(P[i] - P[(i + 1) % len(P)]) for i in range(len(P))]
        print(f'  {name}: sides {np.round(sides, 4).tolist()}')
        opts = set()
        for si, (nm, V, vol) in enumerate(shapes):
            for j in range(len(V)):
                W = V + (P[0] - V[j])
                d = W @ e[:3] + e[3]
                if d.max() > 1e-6: continue                 # piece must lie on the inner side of the face plane
                onp = W[np.abs(d) < 1e-6]
                if len(onp) != len(P): continue
                if not all(np.min(np.linalg.norm(onp - p, axis=1)) < 1e-6 for p in P): continue
                if not inside(W, 1e-6).all() or not clear_of_hole(W): continue
                opts.add(nm)
        print('     pieces that fit behind it:', sorted(opts) or 'NONE')
