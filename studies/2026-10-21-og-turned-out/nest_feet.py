# DICTO 2026-10-21: nesting of the OG turned out and why the downward family breaks, EXACT in Q(sqrt5), on the solids D_k of
# golden-long-solids.pkl (D_0 = OG, D_k = P(D_{k-1}) = hull of the foot points of D_{k-1}'s face planes; the solids are hulls).
#  (a) Lemma: P(S) lies in S iff every face's foot point lies in its own (closed) face; a foot point outside its face lies outside S
#      (the face plane supports S, and S meets it exactly in the face). Here, for every face of every D_k: is the foot point inside,
#      on the boundary of, or outside its face? (exact: the sign of the foot point against each edge, in the face plane)
#  (b) the turned-out sequence S_k = phi^k D_k: S_{k-1} inside S_k, i.e. every corner v of D_{k-1} satisfies n.v <= phi d for every face
#      plane n.x = d of D_k (exact), for every k built; and, for comparison, D_k inside D_{k-1} (the downward family's own nesting).
# usage: python3 nest_feet.py <studies/2026-10-19-five-fold-octet>     (env TO=k to stop after D_k)
import sys, os, json, pickle
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb')); TO = int(os.environ.get('TO', str(len(D) - 1)))
names = ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'] + [f'down {k}' for k in range(5, 13)]
Z0 = Q5(0)
res = {'mark': 'DICTO OG turned out: foot points and nesting, exact, 2026-10-21 · DICTO · dictospheres.com', 'feet': {}, 'nest': {}}
H = {}
for k in range(TO + 1):
    S = D[k]; H[k] = solid(S)
    # (a) foot points against their own faces
    cnt = {}
    for n, d in H[k]:
        F = [v for v in S if dot(n, v) == d]
        f = tuple((d / dot(n, n)) * x for x in n)
        # order-free test: f is in the closed face iff it is on the inner side of every edge line of the face; edges = pairs of face
        # points whose line has all other face points on one side (exact)
        sides = []
        for i, a in enumerate(F):
            for b in F[i + 1:]:
                e = sub(b, a); m = cross(n, e)                      # in-plane normal to the edge line
                s = [dot(m, sub(p, a)).sign() for p in F]
                if all(x >= 0 for x in s) and any(x > 0 for x in s): sides.append(dot(m, sub(f, a)).sign())
                elif all(x <= 0 for x in s) and any(x < 0 for x in s): sides.append(-dot(m, sub(f, a)).sign())
        where = 'outside' if any(x < 0 for x in sides) else 'on the boundary' if any(x == 0 for x in sides) else 'inside'
        key = f'{len([v for v in F])}-point face, foot {where}'; cnt[key] = cnt.get(key, 0) + 1
    res['feet'][names[k]] = cnt
    ok(True, f'(a) {names[k]}: ' + '; '.join(f'{n} x {k_}' for k_, n in sorted(cnt.items())) + (' -> P(' + names[k] + ') inside ' + names[k] if not any('outside' in k_ for k_ in cnt) else ' -> P(' + names[k] + ') NOT inside ' + names[k]))
    if k == 0: continue
    # (b) nesting
    Sm = D[k - 1]
    turned = all((dot(n, v) - PHI * d).sign() <= 0 for v in Sm for n, d in H[k])
    down = all((dot(n, v) - d).sign() <= 0 for v in S for n, d in H[k - 1])
    res['nest'][names[k]] = {'turned_out_nested': turned, 'downward_nested': down}
    ok(turned, f'(b) phi^{k - 1} {names[k - 1]} lies inside phi^{k} {names[k]} (turned out, exact)' + f'; downward: {names[k]} inside {names[k - 1]}: {down}')
    json.dump(res, open(os.path.join(HERE, 'nest-feet.json'), 'w'), indent=1)
