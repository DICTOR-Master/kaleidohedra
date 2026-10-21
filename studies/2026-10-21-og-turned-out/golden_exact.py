# DICTO 2026-10-21: OG turned out, golden step, EXACT ("go ahead build it exact and show me"). Each Aktis shortened to 1/phi of its
# height and flipped out over its face: tip = phi x the face's foot point. So beat k = phi^k x the k-th solid of the OG's downward
# family (#39). Shells in Fibonacci beats 1, 1, 2: OG core | phi TPH | phi^2 TQH | phi^4 TQHD (phi^3 TQP fused inside shell 3).
# In Q(sqrt5) with the #39 machinery: each solid exact and symmetric, each one holds the one before (exact), and each shell cut into
# towers (cone from the centre over each face of the inner solid, cut by the outer solid): one shape per kind, sum = shell exactly.
# usage: python3 golden_exact.py <studies/2026-10-19-five-fold-octet>
import sys, os, json
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
names = ['OG', 'phi TPH', 'phi^2 TQH', 'phi^3 TQP', 'phi^4 TQHD']
D = [OG]
for k in range(1, 5): D.append(rev(D[-1]))
def pw(k):
    r = Q5(1)
    for _ in range(k): r = r * PHI
    return r
B = [[tuple(pw(k) * x for x in v) for v in D[k]] for k in range(5)]
res = {'mark': 'DICTO OG turned out, golden step, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}, 'shells': []}
for k in range(5):
    r = sorted({round(dot(v, v).f() ** .5, 6) for v in B[k]})
    res['solids'][names[k]] = {'corners': len(B[k]), 'corner_radii_float': r, 'symmetric': all({app(M, v) for v in B[k]} == set(B[k]) for M in G)}
    ok(res['solids'][names[k]]['symmetric'], f'{names[k]}: {len(B[k])} corners, radii {r}, full symmetry')
    if k:
        o, nbad, worst = inside(B[k - 1], B[k]); ok(o, f'{names[k - 1]} lies inside {names[k]} exactly (corners outside {nbad})')
        tips = {tuple(PHI * x for x in v) for v in rev(B[k - 1])}; ok(tips == set(B[k]), f'{names[k]} corners = the flipped spire tips (phi x foot points) exactly')
for a, b in [(0, 1), (1, 2), (2, 4)]:
    out = shell(B[a], B[b], G, f'{names[a]} -> {names[b]} ({b - a} beat{"s" if b - a > 1 else ""})'); res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_kind'] and all(out['one_symmetry_orbit_per_kind'].values()),
       f"shell {names[a]} -> {names[b]}: towers {out['pieces']}, each kind one shape, adding up to the shell exactly")
res['boundaries_float'] = {names[k]: [[x.f() for x in v] for v in B[k]] for k in range(5)}
json.dump(res, open(os.path.join(HERE, 'golden-exact.json'), 'w'), indent=1)
