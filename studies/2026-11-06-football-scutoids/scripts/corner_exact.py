"""Football scutoid study, step 3c: the scutoid corner at the closest stacking, exactly.
corner_solve.py found the corner (float): its nearest features are, on the four balls, one pentagon face, two hexagon faces and one
hexagon-hexagon edge (all on balls, none on a bridge). Here: the stacking (h, a, b) is re-solved at DPS digits from its three contact
planes (stack_solve.py), every feature is rebuilt from exact football vertices, and the corner is solved in closed form:
  three faces at equal distance d -> x = x0 + d*y (linear); distance to the edge line = d -> one quadratic A d^2 + B d + C = 0.
Checks: the root agrees with the float corner, the nearest point on the edge lies inside the segment, each face foot lies inside its
polygon, and every face equation holds. Then integer-relation searches for h, b and the corner (minimal polynomials, higher degree and
coefficients than stack_solve.py).  Run: STACK=tight python3 tools/runjob.py <this> <data file>"""
import os, sys, json, numpy as np, mpmath as mp
sys.path.insert(0, '.')
# float machinery for feature identification (first: the exact block below reuses the names P1, P2)
os.environ['STACK'] = 'tight'; sys.argv = [sys.argv[0]]
exec(open('move_vertex.py').read().split('# ---- the moves seen in cell_track')[0].replace('print(', '(lambda *a, **k: None)('))
DPS = 400
src = open('stack_solve.py').read().replace('mp.mp.dps = 60', f'mp.mp.dps = {DPS}')
exec(src.split("for nm, x in (('h', h)")[0].replace('print(', '(lambda *a, **k: None)('))
hM, aM, bM = h, aa, bb
print(f"stacking at {DPS} digits: h = {mp.nstr(hM, 50)}, a = {mp.nstr(aM, 5)}, b = {mp.nstr(bM, 50)} (contact residual {mp.nstr(res, 3)})")
TM = hM * nrm + aM * P1 + bM * P2
corners = json.load(open('../data-corners-tight--0.094.json')) + json.load(open('../data-corners-tight-+0.118.json'))
def cell(nmc):
    k = 'XY'.index(nmc[0]); p, q, r = map(int, nmc[2:-1].split(',')); return k, p, q, r
def exact_ball(k, p, q, r): return [v + p * P1 + q * P2 + r * TM for v in ballm(k, 0)]
def dot(u, v): return (u.T * v)[0]
def cross(u, v): return mp.matrix([u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]])
results = []
for C in corners:
    x = np.array(C['x']); faces, edge = [], None
    for nmc in C['cells']:
        k, p, q, r = cell(nmc); Vf = ball(k, 0)[0] + p * P1n + q * P2n + r * Tn; VX = exact_ball(k, p, q, r)
        hf = hull_faces(Vf)
        ds = sorted(((poly_dist(x, nn, Q), Q) for nn, Q in hf), key=lambda t: t[0][0])
        (d0, kind), Q = ds[0]
        idx = [int(np.argmin(np.linalg.norm(Vf - v, axis=1))) for v in Q]
        cen = sum(VX, mp.matrix([0, 0, 0])) / 60
        if kind == 'face':
            A_, B_, C_ = (VX[i] for i in idx[:3]); nn = cross(B_ - A_, C_ - A_); nn = nn / mp.norm(nn)
            if dot(nn, A_ - cen) < 0: nn = -nn
            faces.append(dict(cell=nmc, n=nn, v=A_, poly=[VX[i] for i in idx], sides=len(idx)))
        else:   # edge: the two polygon corners nearest the point
            e = sorted(range(len(Q)), key=lambda i: seg_dist(x, Q[i], Q[(i + 1) % len(Q)])[0])[0]
            sizes = sorted(len(Q2) for (dd, Q2) in [(t[0], t[1]) for t in ds[:2]])
            edge = dict(cell=nmc, a=VX[idx[e]], b=VX[idx[(e + 1) % len(Q)]], between=sizes)
    assert len(faces) == 3 and edge is not None
    # three faces: n_k . x - d = n_k . v_k  ->  x = x0 + d y
    N = mp.matrix([[f['n'][j] for j in range(3)] for f in faces]); c = mp.matrix([dot(f['n'], f['v']) for f in faces])
    x0 = mp.lu_solve(N, c); y = mp.lu_solve(N, mp.matrix([1, 1, 1]))
    a_, u = edge['a'], (edge['b'] - edge['a']) / mp.norm(edge['b'] - edge['a'])
    def perp(v): return v - dot(v, u) * u
    w0, w1 = perp(x0 - a_), perp(y)
    QA, QB, QC = dot(w1, w1) - 1, 2 * dot(w0, w1), dot(w0, w0)
    roots = [(-QB + s * mp.sqrt(QB ** 2 - 4 * QA * QC)) / (2 * QA) for s in (1, -1)]
    d = min(roots, key=lambda t: abs(t - C['dist'])); X = x0 + d * y
    # checks
    t = dot(X - a_, u) / mp.norm(edge['b'] - edge['a'])
    inside = []
    for f in faces:
        foot = X - (dot(f['n'], X) - dot(f['n'], f['v'])) * f['n']; P = f['poly']
        inside.append(all(dot(cross(P[(i + 1) % len(P)] - P[i], foot - P[i]), f['n']) >= 0 for i in range(len(P))))
    eqres = max(abs(dot(f['n'], X) - dot(f['n'], f['v']) - d) for f in faces); edres = abs(mp.norm(perp(X - a_)) - d)
    MB = mp.matrix([[P1[i], P2[i], TM[i]] for i in range(3)]); wfrac = mp.lu_solve(MB, X)[2]
    ok = abs(d - C['dist']) < 1e-6 and 0 < t < 1 and all(inside) and eqres < mp.mpf(10) ** -(DPS - 20) and edres < mp.mpf(10) ** -(DPS - 20)
    print(f"corner of {', '.join(C['cells'])}: faces {[f['cell'] + ' ' + ('pentagon' if f['sides'] == 5 else 'hexagon') for f in faces]}, "
          f"edge of {edge['cell']} between faces of {edge['between']} sides (at {mp.nstr(t, 6)} along it)")
    print(f"  quadratic {mp.nstr(QA, 20)} d^2 + {mp.nstr(QB, 20)} d + {mp.nstr(QC, 20)} = 0; other root {mp.nstr([r_ for r_ in roots if r_ != d][0], 12)}")
    print(f"  d = {mp.nstr(d, 50)}\n  height w = {mp.nstr(wfrac, 40)} of a period = {mp.nstr(wfrac * hM, 40)} from the middle plane")
    print(f"  float corner: d {C['dist']:.10f}, w {C['w']:+.10f}; face feet inside {inside}; residuals {mp.nstr(eqres, 3)}, {mp.nstr(edres, 3)}: {'OK' if ok else 'FAIL'}")
    results.append((ok, d, abs(wfrac * hM)))
same = max(abs(r[1] - results[0][1]) for r in results) < mp.mpf(10) ** -(DPS - 20) and max(abs(r[2] - results[0][2]) for r in results) < mp.mpf(10) ** -(DPS - 20)
print(f"all {len(results)} corners: same distance and same height off the middle plane to {DPS - 20} digits: {same}")
# integer relations (minimal polynomials) at DPS digits
d, z = results[0][1], results[0][2]
for nm, val in (('h', hM), ('b', bM), ('d (corner distance)', d), ('z (corner height)', z)):
    p = None
    for deg in (2, 4, 8, 16):
        p = mp.findpoly(val, deg, maxcoeff=10 ** 18)
        if p: break
    print(f"minimal polynomial of {nm}: {p if p else 'none up to degree 16, coefficients < 1e18'}", flush=True)
print("FINAL ok" if results and all(r[0] for r in results) and same else "FINAL FAIL (a corner check failed)")
