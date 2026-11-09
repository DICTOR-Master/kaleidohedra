# t1_lines.py -- the turn theorem checked on polar lines S(mu) = P ∩ mu P* of regular polytopes (study 2026-11-09-turn-theorem).
# For each P and each sample mu (all walls, all turned walls, midpoints and quarter points of the pieces between them):
#   (a) antipol: corners of S^v(mu) (inverted distances) == |N|^2 * corners of S(c/mu), exactly;
#   (b) t_min(S(mu)) = max x.y over corners of S(mu) x S^v(mu), exactly (all pairs in 3D; exact on the float-selected near-maximal
#       pairs for the 720-plane 600-cell/120-cell lines), equals the closed form E min(U_mu, U_{c/mu})/h^2;
#   (c) the flag Gram identity q_j.q_k = r2[max(j,k)];
#   (d) t_min(mu) = t_min(c/mu) (follows from (a)), and t_min(mu) < t_min at the fixed point (closed form there, R(S)^2/h^2 checked
#       against the corners of S at the nearest exact sample when sqrt(c) is not in Q(sqrt5)).
# usage: python -u t1_lines.py NAME [NAME ...]   (names: T C O D I simplex4 tesseract cross16 cell24 cell600 cell120 cube5 cross5)
import sys, time, math, json
from fractions import Fraction as Fr
from turnlib import *

POLY = {'D': dodecahedron, 'I': icosahedron, 'C': cube, 'T': tetrahedron, 'O': octahedron,
        'simplex4': simplex4, 'tesseract': tesseract, 'cross16': cross16, 'cell24': cell24,
        'cell600': cell600, 'cell120': cell120,
        'cube5': lambda: perms_signs((1, 1, 1, 1, 1)), 'cross5': lambda: perms_signs((1, 0, 0, 0, 0))}

def samples(st, nq=4):
    h2, R2, c = st['h2'], st['R2'], st['c']
    pts = set(st['nodes']) | {c / x for x in st['nodes']}
    pts = sorted([p for p in pts if h2 < p < R2], key=lambda x: x.f())
    edges = [h2] + pts + [R2]
    out = list(pts)
    for a, b in zip(edges, edges[1:]):
        for k in range(1, nq):
            out.append(a + (b - a) * Q5(Fr(k, nq)))
    return sorted(set(out), key=lambda x: x.f())

def run(name, nq=int(__import__("os").environ.get("NQ", "4"))):
    t0 = time.time()
    V = POLY[name](); st = setup(V)
    d = len(V[0]); big = len(V) + len(st['N']) > 200
    h2, R2, c, nodes, n2 = st['h2'], st['R2'], st['c'], st['nodes'], st['n2']
    ok = gram_check(st['q'], st['r2'])
    print(f'== {name}: d={d}, corners {len(V)}, facets {len(st["N"])}; h^2 = {h2}, R^2 = {R2}, c = h^2 R^2 = {c}', flush=True)
    print(f'   squared flag radii (corner ... facet): {[str(x) for x in st["r2"]]}  ~ {[round(x.f(), 6) for x in st["r2"]]}')
    print(f'   flag Gram identity q_j.q_k = r2[max(j,k)]: {ok}')
    sc = math.sqrt(c.f())
    # fixed point: closed form (float of exact expression) value
    hop = [(r, A) for r, A in zip(nodes, nodes[1:]) if r.f() <= sc <= A.f()][0]
    r, A = hop[0].f(), hop[1].f()
    peak = (r + (sc - r) ** 2 / (A - r)) / h2.f()
    print(f'   fixed point sqrt(c) = {sc:.12f} in hop [{hop[0]}, {hop[1]}]; predicted peak t_min = R(S)^2/h^2 = {peak:.12f}')
    rows = []
    import os
    sl = os.environ.get('SL')   # optional slice a:b of the sample list (to keep each run short on the 720-plane lines)
    smp = samples(st, nq)
    if sl: a, b = map(int, sl.split(':')); smp = smp[a:b]
    for mu in smp:
        P = line_planes(st['N'], V, mu); D = antipol_planes(P)
        X = corners(P); Y = corners(D)
        Yt = corners(line_planes(st['N'], V, c / mu))
        anti = sorted(Y, key=lambda v: tuple(x.f() for x in v)) == sorted([scal(n2, y) for y in Yt], key=lambda v: tuple(x.f() for x in v))
        tb = tmin_brute(X, Y, exact_all=not big)
        tc = tmin_closed(mu, nodes, h2, c)
        tt = tmin_closed(c / mu, nodes, h2, c)
        good = anti and tb == tc and tc == tt and tc.f() < peak + 1e-12
        ok = ok and good
        rows.append(dict(mu=str(mu), mu_f=mu.f(), corners=len(X), tmin=str(tb), tmin_f=tb.f(), closed=str(tc), antipol=anti, ok=good))
        print(f'   mu = {mu.f():.6f} ({mu}): corners {len(X)}/{len(Y)}, antipol {anti}, t_min = {tb.f():.10f} exact {tb}, closed form equal {tb == tc}, turned equal {tc == tt}', flush=True)
    # float scan of the closed form: maximum at sqrt(c), symmetric
    grid = [h2.f() * (R2.f() / h2.f()) ** (k / 4000) for k in range(4001)]
    vals = [tmin_closed_f(m, [x.f() for x in nodes], h2.f(), c.f()) for m in grid]
    k = max(range(len(grid)), key=lambda i: vals[i])
    scan_ok = abs(grid[k] - sc) < 2e-3 * sc and abs(vals[k] - peak) < 1e-5 and max(vals) <= peak + 1e-12
    sym_ok = all(abs(vals[i] - vals[len(grid) - 1 - i]) < 1e-12 for i in range(len(grid)))
    print(f'   float scan (4001 log-spaced points): argmax {grid[k]:.6f} vs sqrt(c) {sc:.6f}; max {vals[k]:.10f} vs peak {peak:.10f}; '
          f'scan symmetric under mu -> c/mu: {sym_ok}')
    ok = ok and scan_ok and sym_ok
    print(f'   {name}: {"ok" if ok else "FAIL"} ({time.time() - t0:.1f} s)', flush=True)
    return ok, dict(name=name, d=d, h2=str(h2), R2=str(R2), c=str(c), r2=[str(x) for x in st['r2']], sqrt_c=sc, peak=peak, rows=rows)

if __name__ == '__main__':
    names = sys.argv[1:]
    allok = True; out = []
    for nm in names:
        o, rec = run(nm); allok = allok and o; out.append(rec)
    tag = '_'.join(names) + ('_' + __import__('os').environ['SL'].replace(':', '-') if __import__('os').environ.get('SL') else '')
    with open(f'../data/t1_{tag}.json', 'w') as f: json.dump(out, f, indent=1)
    print('FINAL ok' if allok else 'FINAL FAIL: see lines above')
