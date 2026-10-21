# DICTO 2026-10-21: "build the 3 and 5 beat shells too" -> OG turned out, golden step, beats 5-12 EXACT. Same rule and machinery as
# golden_exact.py: beat k = phi^k x the k-th solid of the OG's downward family; shells 4 (3 beats: phi^4 -> phi^7) and 5 (5 beats:
# phi^7 -> phi^12). Each new solid is saved as it is made (golden-long-solids.pkl), so a long run keeps its progress.
# usage: python3 golden_exact_long.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, time, pickle
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
def pw(k):
    r = Q5(1)
    for _ in range(k): r = r * PHI
    return r
PK = os.path.join(HERE, 'golden-long-solids.pkl')
D = pickle.load(open(PK, 'rb')) if os.path.exists(PK) else [OG]
while len(D) <= 12:
    t = time.time(); D.append(rev(D[-1])); pickle.dump(D, open(PK, 'wb'))
    print(f'down {len(D) - 1}: {len(D[-1])} corners ({time.time() - t:.0f} s)', flush=True)
B = [[tuple(pw(k) * x for x in v) for v in D[k]] for k in range(13)]
res = {'mark': 'DICTO OG turned out, golden step, beats 5-12, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}, 'shells': []}
for k in range(4, 13):
    r = sorted({round(dot(v, v).f() ** .5, 4) for v in B[k]}); C, F, K = kinds(B[k])
    res['solids'][f'beat {k}'] = {'corners': len(B[k]), 'faces': len(F), 'face_kinds': [(q[0], c) for q, c in K.items()], 'corner_radii_float': r,
                                 'symmetric': all({app(M, v) for v in B[k]} == set(B[k]) for M in G)}
    ok(res['solids'][f'beat {k}']['symmetric'], f"beat {k}: {len(B[k])} corners, {len(F)} faces {[(q[0], c) for q, c in K.items()]}, radii {r[0]}..{r[-1]}")
    if k > 4:
        o, nbad, worst = inside(B[k - 1], B[k]); ok(o, f'beat {k - 1} inside beat {k} exactly (corners outside {nbad})')
for a, b in [(4, 7), (7, 12)]:
    t = time.time(); out = shell(B[a], B[b], G, f'beat {a} -> beat {b} ({b - a} beats)'); res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'], f"shell beat {a} -> {b}: towers {out['pieces']}, shapes per kind {[len(v) for v in out['exact_volumes'].values()]}, sum = gap exactly ({time.time() - t:.0f} s)")
res['boundaries_float'] = {f'beat {k}': [[x.f() for x in v] for v in B[k]] for k in (4, 7, 12)}
json.dump(res, open(os.path.join(HERE, 'golden-long-exact.json'), 'w'), indent=1)
