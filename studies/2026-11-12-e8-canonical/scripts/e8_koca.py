"""Chunk 7 window vs Koca-Koca-Al-Ajmi 2011 (12 Nov 2026), exact over Q(sqrt5).
Koca, Koca, Al-Ajmi (2011), 'Branching of the W(H4) polytopes and their dual polytopes...', sec. 5.3, say the projection of the E8 Voronoi
cell (Elser-Sloane) is the dual of their '720-cell' O(0,0,1,0) = the rectified 600-cell: 720 vertices on two spheres (radius ratio 1.023),
720 cells, pentagonal dipyramids (7 vertices). Their sec. 5.2 dual of the rectified 120-cell O(0,1,0,0) also has 720 vertices (ratio
1.061) but 1200 triangular-dipyramid cells (5 vertices). Our window W = pi_perp(Voronoi) is built here again from all 19440 Voronoi
vertices and compared EXACTLY (vertex sets equal up to one positive scale) with both candidates, each built as the polar of its Wythoff
orbit: f-vectors, cell types, radius ratios. Control: each candidate must match its own description (cells, counts).
Usage: python -u e8_koca.py"""
import sys, os, time
from multiprocessing import get_context
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import e8_leads as L
from e8_leads import Q5, Fr, key, dotg, nrm, scl, sig, exact_hull, dedup, analyse, simple_system, coxeter, orbit, refl, solve, Rq, Nq
import itertools

T0 = time.time()
def say(*a): print(*a, flush=True)
shadow = dedup([sig(q) for q in Rq]); roots = [r for r in shadow if nrm(r) == Q5(1)]

def wy_orbit(ring_rule):
    _, simple = simple_system(roots); m = coxeter(simple)
    adj = {i: [j for j in range(4) if j != i and m[tuple(sorted((i, j)))] != 2] for i in range(4)}
    n1 = next(i for i in range(4) if len(adj[i]) == 1 and m[tuple(sorted((i, adj[i][0])))] == 5)
    chain = [n1]
    while len(chain) < 4: chain.append(next(j for j in adj[chain[-1]] if j not in chain))
    v = solve([list(simple[i]) for i in range(4)], [Q5(1) if i == chain[ring_rule] else Q5(0) for i in range(4)])
    return list(orbit(tuple(v), [refl(a, nrm(a)) for a in simple]).values())

def same_up_to_scale(A, B):
    a0 = max(A, key=lambda x: nrm(x).f())
    for b in B:
        if all((a0[i] * b[j] - a0[j] * b[i]).z() for i, j in itertools.combinations(range(4), 2)) and dotg(a0, b).sign() > 0:
            lam = dotg(a0, b) / nrm(b)
            return {key(scl(lam, x)) for x in B} == {key(x) for x in A}
    return False

def task(name):
    if name == 'W':
        P = dedup([sig(q) for q in Nq]); verts, N, _ = exact_hull(P)
        V = [P[i] for i in verts]; F = [tuple(n) for n in N]
    else:
        O = wy_orbit({'dual rectified 120-cell (Koca 5.2)': 1, 'dual rectified 600-cell (Koca 5.3)': 2}[name])
        verts, N, _ = exact_hull(O)
        V = [tuple(n) for n in N]; F = [O[i] for i in verts]          # polar: vertices = facet normals of the orbit hull
    a = analyse(name, V, F); a.pop('E')
    r = sorted(nrm(v).f() for v in V); a['radius_ratio'] = (r[-1] / r[0]) ** 0.5
    return name, a, V

def main():
    OK = True
    def check(m, c):
        nonlocal OK
        OK &= bool(c); say(('ok   ' if c else 'FAIL ') + m)
    names = ['W', 'dual rectified 120-cell (Koca 5.2)', 'dual rectified 600-cell (Koca 5.3)']
    if 'pilot' in sys.argv[1:]: names = names[1:]
    with get_context('fork').Pool(3) as pool:
        R = {n: (a, V) for n, a, V in pool.map(task, names)}
    for n in names:
        a = R[n][0]
        say(f"{n}: f = {a['f']}, radii2 {[ (x[0][0], x[0][1]) for x in a['radii2']]}, radius ratio {a['radius_ratio']:.4f}, edge2 classes {len(a['edge2'])}, 2-faces {a['faces2']}, cells {a['cells']}")
    c2, c3 = R['dual rectified 120-cell (Koca 5.2)'][0], R['dual rectified 600-cell (Koca 5.3)'][0]
    check('control Koca 5.2: 720 vertices, 1200 cells, all triangular dipyramids (5 vertices, 9 edges, 6 triangles), radius ratio 1.061',
          c2['f'][0] == 720 and c2['f'][3] == 1200 and c2['cells'] == [((5, 9, ((3, 6),)), 1200)] and abs(c2['radius_ratio'] - 1.061) < 1e-3)
    check('control Koca 5.3: 720 vertices, 720 cells, all pentagonal dipyramids (7 vertices, 15 edges, 10 triangles), radius ratio 1.023',
          c3['f'][0] == 720 and c3['f'][3] == 720 and c3['cells'] == [((7, 15, ((3, 10),)), 720)] and abs(c3['radius_ratio'] - 1.023) < 1e-3)
    if 'W' not in R:
        say('pilot: candidates only'); say('FINAL ok' if OK else 'FINAL FAIL: see the FAIL lines above'); return
    W = R['W'][0]
    m2 = same_up_to_scale(R['W'][1], R['dual rectified 120-cell (Koca 5.2)'][1]); m3 = same_up_to_scale(R['W'][1], R['dual rectified 600-cell (Koca 5.3)'][1])
    check(f"W = pi_perp(E8 Voronoi), exact hull of all 19440 shadows: f = {W['f']}, cells {W['cells']}, radius ratio {W['radius_ratio']:.4f}", W['f'][0] == 720)
    check(f'FIND W equals the dual of the rectified 120-cell (Koca 5.2) up to scale, exactly: {m2}', m2)
    check(f'FIND W is NOT the dual of the rectified 600-cell (Koca 5.3), which Koca 5.3 names as the Voronoi projection: equal = {m3}', not m3)
    say(f'total {time.time()-T0:.0f} s')
    say('FINAL ok' if OK else 'FINAL FAIL: see the FAIL lines above')

if __name__ == '__main__':
    main()
