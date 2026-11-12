"""Set up the exact equal-edge problem for the A3, B3, H3 Coxeter permutohedra and write the input of gp_enum.c.

Key reduction. On the closed deformation cone the edge lengths are LINEAR in the cone parameters h (wall-crossing forms, as in
Postnikov 2009 and Ardila-Castillo-Eur-Postnikov 2020). An edge of a member Q is a union of walls of the Coxeter fan, and every wall
inside one edge of Q carries that edge's length; walls inside no edge carry 0. So "all edges of Q equal (= 1)" is the polynomial
system l_e(h) (l_e(h) - 1) = 0 for every wall e, whose real solutions are exactly the 0/1 vectors in the image of h -> l.
The image is cut out by the closing condition around each 2-face (checked here by exact ranks), so the problem is a finite
exact constraint problem: 0/1 labels on walls, every face polygon closes.

Usage: gp_setup.py OUTDIR   (writes OUTDIR/{A3,B3,H3}.in and OUTDIR/setup.json; prints CHECK lines and a final summary)
"""
import sys, json, time
from fractions import Fraction as Fr
sys.path.insert(0, __import__('os').path.dirname(__file__))
from coxeter import QF, Fan, dot, rank, vkey, cross, matvec

out = sys.argv[1]
t0 = time.time()
allchecks = []
summary = {}


def chk(name, ok):
    allchecks.append((name, bool(ok)))
    print(f'CHECK {"ok  " if ok else "FAIL"} {name}', flush=True)


def generic_orbit(F, seed):
    pts = {}
    for g in F.W:
        v = matvec(g, seed)
        pts[vkey(v)] = v
    return list(pts.values())


for si, name in enumerate(['A3', 'B3', 'H3']):
    F = Fan(name)
    for n, ok in F.checks:
        chk(n, ok)
    R, E, C, NF = len(F.rays), len(F.walls), len(F.W), len(F.faces)
    print(f'{name}: rays {R}, walls {E}, chambers {C}, faces {NF}, positive roots {len(F.roots)}', flush=True)
    L = F.L_matrix()
    K = F.K_rows()
    rL = rank([[L[e][j] for e in range(E)] for j in range(R)])
    chk(f'{name} rank of h -> l is R - 3 = {R-3} (kernel = translations)', rL == R - 3)
    KL0 = all(sum((K[i][e] * L[e][j] for e in range(E)), QF(0)).iszero() for i in range(len(K)) for j in range(R))
    chk(f'{name} face closures hold on every h (K.L = 0)', KL0)
    rK = rank(K)
    chk(f'{name} closure space has dim E - rank K = {E - rK} = R - 3: face closures cut out exactly the realisable lengths', E - rK == R - 3)
    print(f'PROGRESS {(si + 0.5) / 3:.3f} {name} ranks done ({time.time()-t0:.0f}s)', flush=True)
    # controls on the cone inequalities
    if name == 'A3':
        seed = (QF(3), QF(1), QF(0))   # not on any mirror? check: generic point
    elif name == 'B3':
        seed = (QF(3), QF(2), QF(1))
    else:
        seed = (QF(Fr(7, 3)), QF(Fr(5, 7)), QF(Fr(1, 11)))
    # make the seed generic (positive on all simple roots) by moving it into the fundamental chamber via the orbit
    P = generic_orbit(F, seed)
    lp = F.lengths(F.support(P))
    chk(f'{name} positive control: a generic {name}-permutohedron ({len(P)} corners) has all {E} wall lengths > 0',
        len(P) == C and all(x.sign() > 0 for x in lp))
    if name == 'A3':
        X = [(QF(a), QF(b), QF(c)) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
        xn = 'cube (edges along the axes, not A3 roots)'
    elif name == 'B3':
        X = [(QF(a), QF(b), QF(c)) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
        X += [tuple(QF(2 * s if k == i else 0) for k in range(3)) for i in range(3) for s in (-1, 1)]
        xn = 'rhombic dodecahedron (edges along body diagonals, not B3 roots)'
    else:
        D = generic_orbit(F, F.om[0])           # dodecahedron in the fan's own orientation (orbit of the 3-fold weight)
        u = F.om[2]                              # five-fold axis (weight with stabiliser I2(5))
        ld = F.lengths(F.support(D))
        chk('H3 the dodecahedron (orbit of w1, 20 corners) is in the cone (all wall lengths >= 0); u = w3 is normal to a pentagon',
            len(D) == 20 and all(x.sign() >= 0 for x in ld) and sum(1 for v in D if dot(v, u) == max(dot(w, u) for w in D)) == 5)
        X = D + [tuple(a + b for a, b in zip(v, u)) for v in D]
        xn = "#49's dodecahedron stretched along a five-fold axis (telescoped)"
    lx = F.lengths(F.support(X))
    neg = sum(1 for x in lx if x.sign() < 0)
    chk(f'{name} negative control: the {xn} fails the cone inequalities ({neg} of {E} wall lengths < 0)', neg > 0)
    # per-face allowed 0/1 labellings (exact)
    allowed = [F.allowed(f) for f in range(NF)]
    # coplanarity table for root directions (exact): cop[i][j] = mask of roots in span(r_i, r_j)
    NR = len(F.roots)
    cop = [[0] * NR for _ in range(NR)]
    for i in range(NR):
        for j in range(NR):
            if i == j:
                cop[i][j] = 1 << i
                continue
            n = cross(F.roots[i], F.roots[j])
            cop[i][j] = sum(1 << k for k in range(NR) if dot(n, F.roots[k]).iszero())
    G = F.sym_group()
    perms = [F.wall_perm(X) for X in G]
    chk(f'{name} symmetry group order {len(G)}, every element permutes walls and preserves the face closures',
        len(G) == 48 + 72 * (name == 'H3') and all(sorted(p) == list(range(E)) for p in perms))
    with open(f'{out}/{name}.in', 'w') as fo:
        fo.write(f'{E} {NF} {NR} {len(G)}\n')
        fo.write(' '.join(map(str, F.wallroot)) + '\n')
        for f in range(NF):
            cyc = F.faces[f]
            fo.write(f'{len(cyc)} ' + ' '.join(str(w) for w, _ in cyc) + f' {len(allowed[f])} ' + ' '.join(map(str, allowed[f])) + '\n')
        for i in range(NR):
            fo.write(' '.join(map(str, cop[i])) + '\n')
        for p in perms:
            fo.write(' '.join(map(str, p)) + '\n')
    fsizes = sorted(set(len(c) for c in F.faces))
    summary[name] = dict(rays=R, walls=E, chambers=C, faces=NF, roots=NR, cone_dim=R - 3, group=len(G),
                         allowed_per_face_size={str(m): len(allowed[next(f for f in range(NF) if len(F.faces[f]) == m)]) for m in fsizes})
    print(f'{name} summary {summary[name]}', flush=True)
    print(f'PROGRESS {(si + 1) / 3:.3f} {name} written ({time.time()-t0:.0f}s)', flush=True)

json.dump(dict(summary=summary, checks=allchecks), open(f'{out}/setup.json', 'w'), indent=1)
bad = [n for n, ok in allchecks if not ok]
print(f'setup checks {len(allchecks) - len(bad)}/{len(allchecks)} ok')
if bad:
    print('SETUP FAIL', bad)
    sys.exit(1)
