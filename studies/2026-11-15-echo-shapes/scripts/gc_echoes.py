#!/usr/bin/env python3
"""Part A, subdivided echoes: Goldberg-Coxeter (h,k) subdivisions of the icosahedron, octahedron and tetrahedron (Goldberg 1937,
Caspar-Klug 1962, Coxeter 1971; for any 3-/4-valent map: Deza-Dutour 2004), T = h^2 + hk + k^2.
Geodesic point set: the triangular-lattice points of the (h,k) Goldberg triangle on every face, mapped flat (exact, Q5 coordinates),
then read as directions on the sphere. Geodesic polyhedron = convex hull of the unit directions; Goldberg polyhedron = its polar
(faces tangent to the unit sphere at the geodesic points).
For every (h,k): point count (10T+2, 4T+2, 2T+2), symmetry group (computed), chirality, tones T_1..T_30 with forced/unforced zeros
(exact re-check of every unforced even zero), and for T <= TMAX_SOLID: hull/polar face census, Dehn invariant (PSLQ), translation
tiling (Venkov-McMullen). Usage: gc_echoes.py out.json [hkmax] [tmax_solid]"""
import sys, os, json, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from echo_lib import *
OUT = sys.argv[1]; HKMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 7; TMAXS = int(sys.argv[3]) if len(sys.argv) > 3 else 7
t0 = time.time(); FAILS = []
def check(c, msg):
    print(('CHECK ok   ' if c else 'CHECK FAIL ') + msg, flush=True)
    if not c: FAILS.append(msg)

def base(name):
    if name == 'icosahedron':
        V = []
        for a, b in ((1, PHI), (1, -PHI), (-1, PHI), (-1, -PHI)):
            V += [(Q5(0), q5(a), q5(b)), (q5(a), q5(b), Q5(0)), (q5(b), Q5(0), q5(a))]
        e2 = Q5(4); grp = 'I'
    elif name == 'octahedron':
        V = [];
        for i in range(3):
            for s in (1, -1): v = [Q5(0)]*3; v[i] = Q5(s); V.append(tuple(v))
        e2 = Q5(2); grp = 'O'
    else:
        V = [tuple(Q5(x) for x in v) for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]; e2 = Q5(8); grp = 'T'
    F = []
    for a, b, c in itertools.combinations(range(len(V)), 3):
        if all(dot(vsub(V[x], V[y]), vsub(V[x], V[y])) == e2 for x, y in ((a, b), (b, c), (a, c))):
            # orient outward: (B-A)x(C-A) . A > 0
            A, B, C = V[a], V[b], V[c]; u, v = vsub(B, A), vsub(C, A)
            n = (u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])
            F.append((a, b, c) if dot(n, A).sign() > 0 else (a, c, b))
    return V, F, grp

def geodesic_points(name, h, k):
    V, F, grp = base(name); T = h*h + h*k + k*k
    # lattice coords (i, j) = i u + j v; triangle corners P0 = 0, P1 = (h, k), P2 = (-k, h + k); point p = beta P1 + gamma P2
    pts = {}
    R = range(-k - 1, h + k + 2)
    for i in R:
        for j in range(-1, h + 2*k + 2):
            # solve [h -k; k h+k] [beta gamma]^T = [i j]^T
            beta = Fr(i*(h + k) + j*k, T); gamma = Fr(-i*k + j*h, T)
            if beta < 0 or gamma < 0 or beta + gamma > 1: continue
            alpha = 1 - beta - gamma
            for a, b, c in F:
                p = tuple(V[a][t]*Q5(alpha) + V[b][t]*Q5(beta) + V[c][t]*Q5(gamma) for t in range(3))
                pts.setdefault(vkey(p), p)
    return list(pts.values()), grp, T

def main():
    res = []
    pairs = [(h, k) for h in range(1, HKMAX + 1) for k in range(0, h + 1)]
    jobs = [(nm, h, k) for nm in ('icosahedron', 'octahedron', 'tetrahedron') for h, k in pairs]
    for n_done, (nm, h, k) in enumerate(jobs):
        pts, grp, T = geodesic_points(nm, h, k)
        expect = {'icosahedron': 10*T + 2, 'octahedron': 4*T + 2, 'tetrahedron': 2*T + 2}[nm]
        check(len(pts) == expect, f'{nm} ({h},{k}) T={T}: {len(pts)} points = {expect}')
        # unit directions (float for symmetry/hull; mp for tones/Dehn)
        Xmp = []
        for p in pts:
            m = to_mp(p); r = mp.sqrt(sum(x*x for x in m)); Xmp.append([x/r for x in m])
        X = np.array([[float(x) for x in p] for p in Xmp])
        Xflat = np.array([to_np(p) for p in pts])
        order, inv, nimp = sym_group(Xflat); gname = group_name(order, inv, nimp)
        # signed amplitude of the lowest invariant tone: A = sum_x sum_a P_k(x.a) over the base vertex directions a (an invariant
        # harmonic of the base group); T_k = c A^2, so a sign change of A between members marks a crossing (not a law)
        Vb, _, _ = base(nm); kA = {'icosahedron': 6, 'octahedron': 4, 'tetrahedron': 3}[nm]
        Am = []
        for v in Vb:
            m = to_mp(v); r = mp.sqrt(sum(x*x for x in m)); Am.append([x/r for x in m])
        A = sum(legendre_all(sum(a*b for a, b in zip(x, y)), kA)[kA] for x in Xmp for y in Am)
        chiral = nimp == 0
        expect_chiral = (k != 0 and k != h)
        check(chiral == expect_chiral, f'{nm} ({h},{k}): chiral = {chiral} (class III expected chiral: {expect_chiral}); group {gname}')
        T_ = tones(pts, 30)
        rep = tone_report(T_, gname)
        # exact re-check of unforced even zeros
        exact = {}
        for kk in rep['unforced_zero']:
            if kk % 2 == 0:
                e = tones_exact_even(pts, kk); exact[kk] = str(e); check(e.iszero(), f'{nm} ({h},{k}) unforced zero T_{kk} exact')
        check(not rep['forced_but_nonzero'], f'{nm} ({h},{k}) every forced silence of {gname} is zero')
        row = {'base': nm, 'h': h, 'k': k, 'T': T, 'points': len(pts), 'group': gname, 'order': order, 'chiral': chiral,
               'goldberg_faces': {'icosahedron': (12, 10*(T - 1)), 'octahedron': (6, 4*(T - 1)), 'tetrahedron': (4, 2*(T - 1))}[nm],
               'tones': rep, 'T6': float(T_[6]), 'T15': float(T_[15]), 'amp_degree': kA, 'amp': float(A/len(pts)),
               'group_raised': order > {'I': 60, 'O': 24, 'T': 12}[grp] * (1 if chiral else 2) or gname not in (grp, grp + 'h', 'Td'), 'exact_unforced': exact}
        if T <= TMAXS:
            Hg = hull3(X); fv = fvec(Hg)
            row['geodesic_hull'] = {'fvec': fv, 'faces': face_census(Hg), 'name': name_of(Hg),
                                    'matches_GC_triangulation': fv[2] == {'icosahedron': 20, 'octahedron': 8, 'tetrahedron': 4}[nm]*T}
            row['geodesic_hull']['dehn'] = dehn(Xmp, Hg)
            row['geodesic_hull']['translation'] = parallelohedron(Hg)
            # Goldberg polyhedron = polar: vertices n_f / offset_f, computed in mp from the hull faces
            Pp = []
            for f in Hg['faces']:
                a, b, c = (Xmp[f[0]], Xmp[f[1]], Xmp[f[2]])
                u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
                n = [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
                d = sum(n[i]*a[i] for i in range(3))
                if d < 0: n = [-x for x in n]; d = -d
                Pp.append([x/d for x in n])
            Xp = np.array([[float(x) for x in p] for p in Pp]); Hp = hull3(Xp)
            check(len(Hp['faces']) == len(pts), f'{nm} ({h},{k}) polar has one face per geodesic point')
            row['goldberg_polar'] = {'fvec': fvec(Hp), 'faces': face_census(Hp), 'name': name_of(Hp),
                                     'dehn': dehn(Pp, Hp), 'translation': parallelohedron(Hp)}
        res.append(row)
        print(f'PROGRESS {(n_done + 1)/len(jobs):.3f} {nm} ({h},{k}) T={T} {gname} zeros {rep["zero"][:12]} unforced {rep["unforced_zero"]}'
              + (f' | hull {row["geodesic_hull"]["name"]} dehn0={row["geodesic_hull"]["dehn"]["zero"]} | polar {row["goldberg_polar"]["name"]} dehn0={row["goldberg_polar"]["dehn"]["zero"]}' if T <= TMAXS else ''), flush=True)
    # controls with known answers
    byk = {(r['base'], r['h'], r['k']): r for r in res}
    oc = byk.get(('octahedron', 1, 1))
    if oc:
        check(oc['goldberg_polar']['name'] == 'truncated octahedron', 'control: octahedral GP(1,1) polar is a truncated octahedron (combinatorially)')
    ic = byk.get(('icosahedron', 1, 0))
    if ic:
        check(ic['geodesic_hull']['name'] == 'icosahedron' and ic['goldberg_polar']['name'] == 'dodecahedron', 'control: icosahedral (1,0) gives icosahedron / dodecahedron')
        check(ic['geodesic_hull']['dehn']['zero'] is False, 'control: icosahedron Dehn nonzero')
    cu = byk.get(('octahedron', 1, 0))
    if cu:
        check(cu['goldberg_polar']['dehn']['zero'] and cu['goldberg_polar']['translation']['tiles_by_translation'], 'control: cube Dehn zero and tiles')
    json.dump({'results': res, 'fails': FAILS, 'seconds': time.time() - t0}, open(OUT, 'w'), indent=1, default=str)
    print(f'{len(res)} subdivisions, {len(FAILS)} failed checks, {time.time() - t0:.0f} s')
    print('FINAL ok' if not FAILS else 'FINAL FAIL')

if __name__ == '__main__': main()
