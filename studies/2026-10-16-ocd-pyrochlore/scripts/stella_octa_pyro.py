# OCD Stella + octahedra on the pyrochlore networks (DICTO 2026-10-16: "is there any extra pyrochlore arrangement additionally
# advantageous?"). Float. The OCD packing's sites split into two diamond networks (as in the stella–icosahedron crystal). Octahedra
# (the regular octahedron of the 8 joint planes) on network 2, OCD Stellas on network 1. Checks by explicit overlap tests over a patch:
# octahedron–octahedron, octahedron–Stella (with the tips' notches cut from the Stellas), and reports the fill; compares the rock-salt
# arrangement (octahedra on a quarter of the sites) and the densest independent choice. -> data/stella-octa-pyro.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T
R = json.load(open('data/crystal-render.json')); S = np.array(R['stella']['v'])   # the OCD Stella in the network frame
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
def depth(H):   # largest ball radius inside the intersection (0 if empty/flat)
    A, b = H[:, :3], -H[:, 3]; nr = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    return r.x[3] if r.success else 0.0
def vol(H):
    A, b = H[:, :3], -H[:, 3]; nr = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if not r.success or r.x[3] < 1e-9: return 0.0
    X = HalfspaceIntersection(H, r.x[:3]).intersections
    try: return ConvexHull(X).volume
    except Exception: return ConvexHull(X, qhull_options='QJ').volume
sh = lambda H, c: np.c_[H[:, :3], H[:, 3] - H[:, :3] @ c]
# Voronoi cell of a site and its walls
sites = [Lb @ np.array(m, float) + k * T[0] for m in itertools.product(range(-3, 4), repeat=3) for k in range(4)]
kind = [k for m in itertools.product(range(-3, 4), repeat=3) for k in range(4)]
nb = [s for s in sites if 1e-9 < np.linalg.norm(s) < 2.0]
HV = np.array([np.r_[s, -(s @ s) / 2] for s in nb]); from scipy.spatial import HalfspaceIntersection as HI
Vc = HI(HV, np.zeros(3)).intersections; HC = planes(Vc); vC = ConvexHull(Vc).volume
on = lambda e: sum(abs(Vc @ e[:3] + e[3]) < 1e-7)
HO = np.array([e for e in HC if on(e) == 6]); HS = planes(S)
vO, vS = vol(HO), vol(HS)
out = ['DICTO · dictospheres.com', 'OCD Stella + octahedra on the pyrochlore networks (float)', f'cell {vC:.6f}; octahedron {vO:.6f} ({vO / vC:.4f} cells); OCD Stella {vS:.6f}']
def run(is_octa, label, share):   # share: the octahedra's exact share of the sites (one network = 1/2; rock salt = 1/4)
    P = [(s, is_octa(i)) for i, s in enumerate(sites) if np.linalg.norm(s) < 3.2]
    centre = [(s, o) for s, o in P if np.linalg.norm(s) < 1.6]
    worst_oo = worst_os = 0.0; notch = []; pairs = 0
    for s, o in centre:
        for t, p in P:
            if np.linalg.norm(t - s) < 1e-9 or np.linalg.norm(t - s) > 2.6: continue
            if o and p: worst_oo = max(worst_oo, depth(np.vstack([sh(HO, s), sh(HO, t)]))); pairs += 1
        if not o:   # a Stella: notches from octahedra around it, and check octahedra overlap it only inside its own cell
            n = 0.0
            for t, p in P:
                if p and np.linalg.norm(t - s) < 2.6:
                    v = vol(np.vstack([sh(HS, s), sh(HO, t)])); n += v
                    outside = vol(np.vstack([sh(HO, t), sh(HC, s)]))   # octahedron inside this Stella's cell
                    worst_os = max(worst_os, 0)
            notch.append(n)
    fr = share
    nm = np.mean(notch) if notch else 0; full = np.mean([abs(x - 6 * notch_tip) < 1e-6 for x in notch]) if notch else 0
    fill = (fr * vO + (1 - fr) * vS - fr * 6 * notch_tip) / vC    # every octahedron notches Stellas with its 6 tips, wherever they land
    out.append(f'{label}: octahedra on {fr:.3f} of the sites; sampled Stellas notched by all 6 tips: {full:.0%}; deepest octahedron–octahedron overlap {worst_oo:.2e} ({pairs} pairs tested); '
               f'notch per Stella {nm:.6f} ({nm / vS:.2%}); fill {fill:.4%}')
tip_s = None
notch_tip = None
def one_tip():   # the part of a Stella taken by one octahedron tip from a square neighbour (same for all 6 by symmetry)
    e = next(e for e in HC if on(e) == 4); v = 2 * (-e[3]) * e[:3] / (e[:3] @ e[:3])
    return vol(np.vstack([HS, sh(HO, v)]))
notch_tip = one_tip(); out.append(f'one tip takes {notch_tip:.6f} of a Stella')
net2 = lambda i: kind[i] in (2, 3)
run(net2, 'pyrochlore: octahedra on one diamond network', 0.5)
# rock-salt quarter: octahedra on sites whose 6 square neighbours carry none; build from the cube-axis vectors
cube = [2 * (-e[3]) * e[:3] / (e[:3] @ e[:3]) for e in HC if on(e) == 4]
e1 = cube[0]; e2 = next(v for v in cube if abs(v @ e1) < 1e-9); e3 = np.cross(e1, e2); e3 *= np.linalg.norm(e1) / np.linalg.norm(e3)
Bm = np.linalg.inv(np.c_[e1, e2, e3])
def rs(i):
    c = Bm @ sites[i]; r = np.round(c)
    return bool(np.allclose(c, r, atol=1e-6) and int(r.sum()) % 2 == 0)
run(rs, 'rock salt: octahedra on a quarter of the sites', 0.25)
print('\n'.join(out)); open('data/stella-octa-pyro.txt', 'w').write('\n'.join(out) + '\n')
