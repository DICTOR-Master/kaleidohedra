# DICTO 2026-10-21: "the lines defining the shells denote the structures". The edge network (the lines) of every boundary solid of the
# Kyushindo cores, EXACT in Q(sqrt5) (same solids and frame as surface_patterns.py):
#   (a) straight runs: edges that continue in a straight line through a corner (exact: zero cross product, opposite directions), joined
#       into maximal runs; their number and the longest (edges; float length);
#   (b) parallel families: edges grouped by direction (exact: zero cross product); the number of directions, the family sizes, and which
#       families point along a symmetry axis (two-, three- or five-fold; exact, axes from the 60 rotations);
#   (c) central belts: edges lying in one plane through the centre (exact) that close up into one circuit round the solid.
# Writes surface-lines.json (float edges and the runs/belts for the figure).   usage: python3 surface_lines.py <studies/2026-10-19-five-fold-octet>
import sys, os, json
from collections import Counter
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
Z0 = Q5(0)
zero = lambda v: all(x == Z0 for x in v)
UP = [ID]
for _ in range(3): UP.append(step(UP[-1])[0])
DN = [OG]
for _ in range(4): DN.append(rev(DN[-1]))
SOL = [('ID', UP[0]), ('RT', UP[1]), ('GTI', UP[2]), ('FPD', UP[3]), ('OG', DN[0]), ('TPH', DN[1]), ('TQH', DN[2]), ('TQP', DN[3]), ('TQHD', DN[4])]
I3 = tuple(tuple(Q5(1 if i == j else 0) for j in range(3)) for i in range(3))
def order(M):
    A = M; k = 1
    while A != I3: A = tuple(tuple(sum((A[i][t] * M[t][j] for t in range(3)), Z0) for j in range(3)) for i in range(3)); k += 1
    return k
AX = []                                            # (fold, axis vector) for the 6 + 10 + 15 axes
for M in G:
    k = order(M)
    if k == 1: continue
    A = [tuple(M[i][j] - I3[i][j] for j in range(3)) for i in range(3)]
    v = next((cross(A[i], A[j]) for i, j in ((0, 1), (0, 2), (1, 2)) if not zero(cross(A[i], A[j]))), None)
    if not any(f == k and zero(cross(v, w)) for f, w in AX) and not any(f % k == 0 and zero(cross(v, w)) for f, w in AX): AX.append((k, v))
AX = [(f, v) for f, v in AX if not any(g > f and g % f == 0 and zero(cross(v, w)) for g, w in AX)]
ok(sorted(Counter(f for f, _ in AX).items()) == [(2, 15), (3, 10), (5, 6)], f'axes from the 60 rotations: {sorted(Counter(f for f, _ in AX).items())} (fold, number)')
res = {'mark': 'DICTO Kyushindo cores, edge networks, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}}
for nm, S in SOL:
    C, Fc = polytope(solid(S)); E = set()
    for o, _ in Fc:
        for a, b in zip(o, o[1:] + o[:1]): E.add((min(a, b), max(a, b)))
    E = sorted(E); vec = lambda e: sub(C[e[1]], C[e[0]])
    # (a) straight runs
    at = {}
    for i, e in enumerate(E):
        for v in e: at.setdefault(v, []).append(i)
    link = {i: [] for i in range(len(E))}
    for v, es in at.items():
        for i in es:
            for j in es:
                if i < j:
                    a = sub(C[E[i][0] if E[i][1] == v else E[i][1]], C[v]); b = sub(C[E[j][0] if E[j][1] == v else E[j][1]], C[v])
                    if zero(cross(a, b)) and dot(a, b).sign() < 0: link[i].append(j); link[j].append(i)
    seen, runs = set(), []
    for i in range(len(E)):
        if i in seen or not link[i]: continue
        st, g = [i], set()
        while st:
            x = st.pop()
            if x in g: continue
            g.add(x); st += link[x]
        seen |= g; runs.append(sorted(g))
    rl = [sum(dot(vec(E[i]), vec(E[i])).f() ** .5 for i in r) for r in runs]
    # (b) parallel families
    fam = []
    for i, e in enumerate(E):
        for f in fam:
            if zero(cross(vec(E[f[0]]), vec(e))): f.append(i); break
        else: fam.append([i])
    along = Counter()
    for f in fam:
        k = next((fo for fo, w in AX if zero(cross(vec(E[f[0]]), w))), 0); along[k] += 1
    # (c) central belts: edges in one plane through the centre, closing into one circuit
    pl = []
    for i, e in enumerate(E):
        nrm = cross(C[e[0]], C[e[1]])
        if zero(nrm): continue
        for p in pl:
            if zero(cross(p[0], nrm)): p[1].append(i); break
        else: pl.append([nrm, [i]])
    belts = []
    for nrm, es in pl:
        if len(es) < 3: continue
        deg = Counter(v for i in es for v in E[i])
        if all(d == 2 for d in deg.values()):
            st, g = [es[0]], set()
            while st:
                x = st.pop()
                if x in g: continue
                g.add(x); st += [j for j in es if set(E[j]) & set(E[x])]
            if len(g) == len(es): belts.append(es)
    axfam = [f for f in fam if any(zero(cross(vec(E[f[0]]), w)) for _, w in AX)]
    if nm == 'TQH':                                 # the ribbon triples: the two-fold families are the trapezoids' parallel sides
        psides = set()
        for o, _ in Fc:
            if len(o) != 4: continue
            for r in (0, 1):
                a1, b1, c1, d1 = o[r], o[r + 1], o[(r + 3) % 4], o[r + 2]
                if zero(cross(sub(C[b1], C[a1]), sub(C[d1], C[c1]))): psides |= {(min(a1, b1), max(a1, b1)), (min(c1, d1), max(c1, d1))}
        fs = [{E[i] for i in f} for f in axfam]
        qe = Counter((min(a1, b1), max(a1, b1)) for o, _ in Fc if len(o) == 4 for a1, b1 in zip(o, o[1:] + o[:1])); seams = {e for e, n in qe.items() if n == 2}
        mids = lambda e: tuple(x + y for x, y in zip(C[e[0]], C[e[1]]))
        anti = all(len(f & seams) == 2 and mids(sorted(f & seams)[0]) == tuple(-x for x in mids(sorted(f & seams)[1])) for f in fs)
        ok(len(seams) == 30 and anti, 'TQH: each two-fold family holds two seams with opposite midpoints: the two ribbons at the two ends of one two-fold axis')
        ok(len(axfam) == 15 and all(len(f) == 6 for f in fs) and set().union(*fs) == psides,
           'TQH: the 15 edge families along the two-fold axes are exactly the trapezoids\' parallel sides (90 edges: 30 seams + 60 outer sides), 6 per family: the two ribbons at the ends of one two-fold axis, 3 lines each, all along a second two-fold axis')
    info = {'edges': len(E), 'straight_runs': len(runs), 'run_edges': sorted(Counter(len(r) for r in runs).items()), 'longest_run_float': round(max(rl), 4) if rl else 0,
            'directions': len(fam), 'family_sizes': sorted(Counter(len(f) for f in fam).items()), 'families_along_axes': {str(k): v for k, v in sorted(along.items())},
            'central_belts': len(belts), 'belt_edges': sorted(Counter(len(b) for b in belts).items()),
            'corners_float': [[x.f() for x in v] for v in C], 'edge_list': [list(e) for e in E], 'runs': runs, 'belts': belts, 'axis_families': axfam}
    res['solids'][nm] = info
    ok(True, f"{nm}: {len(E)} edges; straight runs {len(runs)} {info['run_edges'] or ''}" + (f" (longest {info['longest_run_float']})" if runs else '') +
       f"; {len(fam)} edge directions, family sizes {info['family_sizes']}, along axes (fold: families; 0 = none) {info['families_along_axes']}; central belts {len(belts)} {info['belt_edges'] or ''}")
json.dump(res, open(os.path.join(HERE, 'surface-lines.json'), 'w'))
