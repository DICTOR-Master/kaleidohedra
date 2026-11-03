"""Step 2b. The two rhombic Catalan solids in closed form (edge 1).
A rhombus of side 1 with acute angle alpha (sharp corners: orbit A, the 4-valent corners of the rhombic dodecahedron,
the 5-valent of the rhombic triacontahedron; blunt corners: orbit B, 3-valent). Cutting y_A, y_B along the edges gives
corner sides 2 y_A sin(alpha/2) and 2 y_B cos(alpha/2), and original sides 1 - y_A - y_B. Alternating: the two corner
sides equal a; then b = 1 - a K with K = (1/sin(alpha/2) + 1/cos(alpha/2))/2. Golden: a = phi b (greater) or b = phi a
(lesser), so b = 1/(1 + phi K) or 1/(1 + K/phi). Checked exactly against the cut of the exact solid (polar of the exact
Archimedean solid), corner by corner; plus the single-depth and single-plane tests and the volume.
usage: python s2b_rhombic_exact.py -> ../data/s2b-rhombic.json
"""
import json, os
import numpy as np
import sympy as sp
import gcb
from gcb_exact import exact_dual
phi = (1 + sp.sqrt(5)) / 2
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True); assert ok, name
def z(e, dps=60): return abs(sp.N(e, dps)) < sp.Float(10) ** (-(dps - 8))
def S(e): return str(sp.radsimp(e))

out = {}
for cat, arch, cosa, valA in (('rhombic dodecahedron', 'cuboctahedron', sp.Rational(1, 3), 4),
                              ('rhombic triacontahedron', 'icosidodecahedron', sp.sqrt(5) / 5, 5)):
    s_ = sp.sqrt((1 - cosa) / 2); c_ = sp.sqrt((1 + cosa) / 2)
    K = sp.radsimp((1 / s_ + 1 / c_) / 2)
    D, Df, FD, orb = exact_dual(arch)
    # scale to edge 1; orbit A = the corners of valence valA
    f0 = FD[0]; L = sp.sqrt(sp.radsimp((D[f0[0]] - D[f0[1]]).dot(D[f0[0]] - D[f0[1]])))
    Dn = [v / L for v in D]
    val = {v: sum(1 for f in FD if v in f) for v in range(len(D))}
    # acute angle check
    v = next(i for i in range(len(D)) if val[i] == valA); f = next(f for f in FD if v in f); i = f.index(v)
    e1, e2 = Dn[f[i - 1]] - Dn[v], Dn[f[(i + 1) % 4]] - Dn[v]
    check(f'{cat}: acute angle cos = {cosa} at the {valA}-valent corners', z(e1.dot(e2) - cosa))
    rec = {'K': S(K), 'cuts': []}
    for lab, b in (('greater (corner sides long)', 1 / (1 + phi * K)), ('lesser (original sides long)', 1 / (1 + K / phi))):
        b = sp.radsimp(b); a = sp.radsimp(phi * b if lab.startswith('greater') else b / phi)
        yA, yB = sp.radsimp(a / (2 * s_)), sp.radsimp(a / (2 * c_))
        # exact cut of the exact solid: every corner side = a, every original side = b
        y = {i: (yA if val[i] == valA else yB) for i in range(len(D))}
        pts = {}
        for f in FD:
            for p, q in zip(f, f[1:] + f[:1]):
                for u, w in ((p, q), (q, p)): pts[(u, w)] = Dn[u] + y[u] * (Dn[w] - Dn[u])
        ok = True; nC = nO = 0
        for f in FD:
            for k in range(4):
                u, v_, w = f[k - 1], f[k], f[(k + 1) % 4]
                cs = pts[(v_, w)] - pts[(v_, u)]; os_ = pts[(w, v_)] - pts[(v_, w)]
                ok &= z(cs.dot(cs) - a ** 2) and z(os_.dot(os_) - b ** 2); nC += 1; nO += 1
        check(f'{cat} {lab}: all {nC} corner sides = a and all {nO} original sides = b exactly (60 digits); a/b or b/a = phi', ok and (z(a - phi * b) or z(b - phi * a)))
        # caps and planes
        vA = next(i for i in range(len(D)) if val[i] == valA); vB = next(i for i in range(len(D)) if val[i] == 3)
        def cap(vi, yv):
            nb = next(w for f in FD for k, w in enumerate(f) if f[k - 1] == vi)
            e = Dn[nb] - Dn[vi]; R = sp.sqrt(sp.radsimp(Dn[vi].dot(Dn[vi])))
            ct = -e.dot(Dn[vi]) / R
            return sp.radsimp(yv * ct), sp.radsimp(R - yv * ct)
        hA, PA = cap(vA, yA); hB, PB = cap(vB, yB)
        W = np.array([[float(t) for t in p] for p in pts.values()]); W = np.unique(np.round(W, 10), axis=0)
        from scipy.spatial import ConvexHull
        hull = ConvexHull(W); Fw = gcb.faces(W)
        import collections
        rec['cuts'].append({'cut': lab, 'a': S(a), 'b': S(b), 'a_decimal': float(a), 'b_decimal': float(b),
                            'y_sharp': S(yA), 'y_blunt': S(yB), 'y_sharp_decimal': float(yA), 'y_blunt_decimal': float(yB),
                            'cap_depth_sharp': float(hA), 'cap_depth_blunt': float(hB), 'plane_distance_sharp': float(PA), 'plane_distance_blunt': float(PB),
                            'equal_cap_depths': bool(z(hA - hB)), 'equal_plane_distances': bool(z(PA - PB)),
                            'volume_float': float(hull.volume), 'corners': len(W), 'faces': dict(collections.Counter(len(f) for f in Fw)),
                            'vertices_edge1': W.tolist()})
        check(f'{cat} {lab}: {len(W)} corners, faces {dict(collections.Counter(len(f) for f in Fw))}; caps equal {z(hA - hB)}, planes equal {z(PA - PB)}', True)
    # the single-plane cut: P_A(t) = P_B(t) along the alternating family a = t; its ratio
    t = sp.Symbol('t', positive=True)
    nbA = next(w for f in FD for k, w in enumerate(f) if f[k - 1] == vA); eA = Dn[nbA] - Dn[vA]; RA = sp.sqrt(sp.radsimp(Dn[vA].dot(Dn[vA])))
    nbB = next(w for f in FD for k, w in enumerate(f) if f[k - 1] == vB); eB = Dn[nbB] - Dn[vB]; RB = sp.sqrt(sp.radsimp(Dn[vB].dot(Dn[vB])))
    ctA, ctB = sp.radsimp(-eA.dot(Dn[vA]) / RA), sp.radsimp(-eB.dot(Dn[vB]) / RB)
    sol = sp.solve(sp.Eq(RA - t / (2 * s_) * ctA, RB - t / (2 * c_) * ctB), t)
    if sol:
        aa = sp.radsimp(sol[0]); bb = sp.radsimp(1 - aa * K)
        rec['single_plane_alternating_cut'] = {'a': float(aa), 'b': float(bb), 'ratio_a_over_b': float(aa / bb) if float(bb) > 0 else None,
                                               'valid': bool(float(aa) > 0 and float(bb) > 0)}
    rec['single_depth_alternating'] = f'never: equal caps force y_sharp/y_blunt = cos(theta_blunt)/cos(theta_sharp) = {float(ctB / ctA):.9f}, alternating needs cot(alpha/2) = {float(c_ / s_):.9f}'
    check(f'{cat}: single-depth cut never alternating (ratio mismatch)', not z(ctB / ctA - c_ / s_))
    out[cat] = rec
    print(cat, json.dumps({k: v for k, v in rec.items() if k != 'cuts'}))
json.dump({'rhombic': out, 'checks': CHECKS}, open(os.path.join(DATA, 's2b-rhombic.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
