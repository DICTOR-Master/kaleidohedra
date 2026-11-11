# theoremB.py: independent recomputation of Kamenetsky's Theorem B (paper §8): over all 3^7 = 2187 homochiral frame assignments of the
# eight children of 2C3 with the central child a plain translate, exactly 3 are coarsening-closed with |P*| <= 300 (the certified one and
# its two conjugates by cyclic coordinate permutation, closing at 44); 6 fail by an admissible offset supertile pose; 2178 exceed 300
# poses within two steps. Also |Sigma(P0)| takes the values 44, 62, 99, 103, 113, 114, 119, 158, 186, and its minimum 44 is attained
# exactly by the three closed ones. Our own code (recount.py), the paper's stopping rules: stop at the first offset pose, or when |P| > 300.
# usage: theoremB.py <workers> [sample]
import sys, itertools, time, json, multiprocessing as mp
from recount import *
W = int(sys.argv[1]); SAMPLE = int(sys.argv[2]) if len(sys.argv) > 2 else 0
def parity(p):
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]: s = -s
    return s
OPT = {v: [p for p in itertools.permutations(range(3)) if parity(p) == (-1) ** sum(v)] for v in U}   # D_s(v) pi_v must be a rotation
ALL = [dict(zip(U, c)) for c in itertools.product(*[OPT[v] for v in U])]
assert len(ALL) == 2187
def one(fr):
    CH = children(fr); assert check_partition(CH) and all(det(h) == 1 for h, _ in CH)
    P = language(CH); s0 = sigma(P, CH); n_s0 = len(s0); hist = [len(P)]
    S = s0
    while True:
        if any(x % 2 for _, T in S for x in T): return dict(fr={str(k): v for k, v in fr.items()}, status='offset', sigma0=n_s0, hist=hist)
        new = {(G, tuple(x // 2 for x in T)) for G, T in S}
        if new <= P: return dict(fr={str(k): v for k, v in fr.items()}, status='closed' if new == P else 'closed-strict', sigma0=n_s0, hist=hist, Pstar=len(P))
        P = P | new; hist.append(len(P))
        if len(P) > 300: return dict(fr={str(k): v for k, v in fr.items()}, status='capped', sigma0=n_s0, hist=hist)
        S = sigma(P, CH)
if __name__ == '__main__':
    t0 = time.time(); todo = ALL[::max(1, len(ALL) // SAMPLE)][:SAMPLE] if SAMPLE else ALL
    FRc = {(0, 0, 0): (0, 1, 2), (0, 0, 1): (0, 2, 1), (0, 1, 0): (2, 1, 0), (0, 1, 1): (1, 2, 0), (1, 0, 0): (1, 0, 2), (1, 0, 1): (0, 1, 2), (1, 1, 0): (2, 0, 1)}
    if FRc not in todo: todo = [FRc] + todo
    res = []
    with mp.get_context('fork').Pool(W) as pool:
        for k, r in enumerate(pool.imap_unordered(one, todo, chunksize=1)):
            res.append(r)
            if k % 50 == 0: print(f'PROGRESS {(k + 1) / len(todo):.3f} assignments ({time.time()-t0:.0f}s)', flush=True)
    from collections import Counter
    st = Counter(r['status'] for r in res); s0 = sorted(set(r['sigma0'] for r in res))
    closed = [r for r in res if r['status'].startswith('closed')]
    print(f'assignments {len(res)}: {dict(st)}; closed at {[r["Pstar"] for r in closed]}; |Sigma(P0)| values {s0}; '
          f'min {s0[0]} attained by {sum(r["sigma0"] == s0[0] for r in res)}', flush=True)
    cert = str({str(k): v for k, v in FRc.items()})
    print('certified assignment closes:', any(str(r['fr']) == cert and r['status'] == 'closed' for r in res), flush=True)
    json.dump(res, open('../theoremB.json' if not SAMPLE else '../theoremB-pilot.json', 'w'))
    ok = (not SAMPLE and st['closed'] == 3 and st['offset'] == 6 and st['capped'] == 2178 and all(r['Pstar'] == 44 for r in closed)
          and s0 == [44, 62, 99, 103, 113, 114, 119, 158, 186] and sum(r['sigma0'] == 44 for r in res) == 3) or (SAMPLE and any(r['status'] == 'closed' for r in res))
    print('FINAL ok' if ok else 'FINAL FAIL', f'({time.time()-t0:.0f}s)', flush=True)
