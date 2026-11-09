"""ABC waveform scan (DICTO 9 Nov 2026: crest waves on the surfaces, reciprocal underneath, golden mix).
Designs = sets of crest planes in the reference Narcissus (wave_lib), menu: 6 tilted close-packed families (lean B-ward b1..b3,
lean C-ward c1..c3) + horizontal z; offsets H*(j/6) (crests through seat rows A, B, C and the rows between) and H*(j + 1/phi),
H*(j + 1/phi^2) (golden phases), only planes that cut the piece. Designs: every single plane, every pair (one colour = one wave;
two colours = DICTO's two-component golden mix), the 3-fold and 6-fold symmetric closures of every plane.
For each design x rule (STRICT / BEND) x placements (mirror copies yes / no):
  PATCH   - some stacking word of K slabs admits a decorated filling of the n-patch (free boundary)
  PERIODIC- a decorated filling on a torus: periodic words up to PMAX, in-plane sublattices of index <= IMAX, every skew representative
  WORDS   - the set of S/T words (length K-1) that admit a patch (what the wave forces)
CANDIDATE = PATCH and no PERIODIC. Control: the empty decoration must give PATCH + PERIODIC with all 2^(K-1) words.
Usage: scan.py K n PMAX IMAX nt [pilot_count] [workers]"""
import sys, time, itertools, pickle, os, json
import numpy as np
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave_lib as W
t0 = time.time()
def hb(m): print(f"HEARTBEAT {time.time()-t0:.0f}s {m}", flush=True)
K, NP, PMAX, IMAX, NT = (int(x) for x in sys.argv[1:6])
PILOT = int(sys.argv[6]) if len(sys.argv) > 6 else 0
NW = int(sys.argv[7]) if len(sys.argv) > 7 else 1
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# ---------- menu
NRM = W.lean_normals(); H = W.H
menu = []
for name, n in NRM.items():
    s = W.P0 @ n; lo, hi = s.min(), s.max()
    offs = {round(H * j / 6, 9) for j in range(-12, 13)}
    for j in range(-3, 3): offs |= {round(H * (j + 1 / W.PHI), 9), round(H * (j + 1 / W.PHI ** 2), 9)}
    for d in sorted(offs):
        if lo + 1e-7 < d < hi - 1e-7: menu.append((name, n, d))
SR = []
for p in W.SYM:
    R, t = W.affine(W.P0, W.P0, p); assert np.allclose(t, 0, atol=1e-9); SR.append(R)
def ckey(planes):   # canonical form under the symmetry of N and colour swap
    best = None
    for R in SR:
        for cs in ((0, 1), (1, 0)):
            k = tuple(sorted(tuple(np.round(R @ n, 5) + 0.0) + (round(d, 5), cs[c]) for n, d, c in planes))
            if best is None or k < best: best = k
    return best
designs = {}
def add(tag, planes):
    k = ckey(planes)
    if k not in designs: designs[k] = (tag, planes)
add('control-empty', [])
for name, n, d in menu: add(f'1:{name}@{d/H:.4f}H', [(n, d, 0)])
for (na, n, d), (nb, m, e) in itertools.combinations(menu, 2):
    add(f'2:{na}@{d/H:.4f}H+{nb}@{e/H:.4f}H', [(n, d, 0), (m, e, 0)])
    add(f'2c:{na}@{d/H:.4f}H+{nb}@{e/H:.4f}H', [(n, d, 0), (m, e, 1)])
for name, n, d in menu:
    for gname, G in (('C3', [R for R in SR if np.linalg.det(R) > 0]), ('C3v', SR)):
        pl = []
        for R in G:
            q = (R @ n, d, 0)
            if not any(np.allclose(q[0], x[0]) and abs(q[1] - x[1]) < 1e-9 for x in pl): pl.append(q)
        add(f'{gname}:{name}@{d/H:.4f}H', pl)
D = sorted(designs.values(), key=lambda x: (len(x[1]), x[0]))
if PILOT: D = D[:1] + D[1:][::max(1, (len(D) - 1) // PILOT)][:PILOT]
DI = list(enumerate(D))
SH = os.environ.get('SHARD')            # 'i/m': run designs i, i+m, ... (control d0 always included); keeps each run under 20 min
if SH:
    si, sm = map(int, SH.split('/')); DI = [x for x in DI if x[0] % sm == si or x[0] == 0]
SHTAG = f"-shard{SH.replace('/', 'of')}" if SH else ''
print(f"menu planes {len(menu)}; designs up to symmetry {len(designs)}; running {len(D)}; K={K} n={NP} PMAX={PMAX} IMAX={IMAX} torus-n={NT}", flush=True)

# ---------- structures (cached)
cache = os.path.join(OUT, f'struct-K{K}-n{NP}-P{PMAX}-I{IMAX}-t{NT}.pkl')
if os.path.exists(cache):
    PATCH, TOR = pickle.load(open(cache, 'rb'))
else:
    PATCH = {''.join(w): W.Structure(''.join(w), NP) for w in itertools.product('ST', repeat=K - 1)}
    hb(f"patch structures {len(PATCH)}")
    TOR = W.torus_instances(PMAX, IMAX, NT)
    pickle.dump((PATCH, TOR), open(cache, 'wb'))
hb(f"tori {len(TOR)}: words {sorted({t[0].split('/')[0] for t in TOR})}")
# geometry checks: every piece away from the boundary has 10 contacts, contacts are face to face of the same kind
S0 = PATCH['S' * (K - 1)]; deg = np.zeros(len(S0.Ps), int)
for i, fi, j, fj in S0.contacts: deg[i] += 1; deg[j] += 1
GEOM_OK = deg.max() == 10 and (deg == 10).sum() > 0
print(f"geometry: max contacts per piece {deg.max()}, pieces with all 10: {(deg==10).sum()} of {len(deg)}", flush=True)

def run(arg):
    di, (tag, planes) = arg; out = []
    deco = [(n, d, c) for n, d, c in planes]
    for mode in ('STRICT', 'BEND'):
        if not deco and mode == 'BEND': continue
        sigP = {w: W.signatures(S, deco, mode) for w, S in PATCH.items()}
        for mirror in (True, False):
            words = [w for w, S in PATCH.items() if W.solve(S, sigP[w], mirror)]
            per = None
            if words:
                cache_sig = {}
                for lab, S, cl in TOR:
                    if id(S) not in cache_sig: cache_sig[id(S)] = W.signatures(S, deco, mode)
                    if W.solve(S, cache_sig[id(S)], mirror, cl): per = lab; break
            v = 'NO PATCH' if not words else ('PERIODIC ' + per if per else 'CANDIDATE')
            out.append(dict(design=di, tag=tag, mode=mode, mirror=mirror, verdict=v, words=words))
    return out

res = []
with mp.get_context("fork").Pool(NW) as pool:
    for k, r in enumerate(pool.imap_unordered(run, DI, chunksize=1)):
        res += r
        for x in r:
            if x['verdict'] != 'NO PATCH' and (x['verdict'].startswith('CAND') or k % 25 == 0 or x['design'] == 0):
                print(f"  d{x['design']} {x['tag']} {x['mode']} mirrors={'yes' if x['mirror'] else 'no'}: {x['verdict']}  words {len(x['words'])}/{2**(K-1)} {x['words'][:6]}", flush=True)
        if k % 50 == 0: hb(f"{k+1}/{len(DI)} designs done")
from collections import Counter
summ = Counter((x['mode'], x['mirror'], x['verdict'].split()[0]) for x in res)
print('SUMMARY', sorted(summ.items()), flush=True)
wc = Counter((x['mode'], x['mirror'], len(x['words'])) for x in res if x['words'])
print('PATCH-WORD COUNTS (mode, mirrors, #words admitted): designs', sorted(wc.items()), flush=True)
json.dump(res, open(os.path.join(OUT, f'scan-K{K}-n{NP}-P{PMAX}-I{IMAX}{"-pilot" if PILOT else ""}{SHTAG}.json'), 'w'))
ctrl = [x for x in res if x['design'] == 0]
CTRL_OK = all(x['verdict'].startswith('PERIODIC') and len(x['words']) == 2 ** (K - 1) for x in ctrl) and len(ctrl) == 2
cands = [(x['design'], x['tag'], x['mode'], x['mirror']) for x in res if x['verdict'] == 'CANDIDATE']
print(f"CANDIDATES {len(cands)} {cands[:20]}", flush=True)
print('FINAL ok' if (CTRL_OK and GEOM_OK) else f'FINAL FAIL: control {ctrl} geom {GEOM_OK}', f'{time.time()-t0:.0f}s', flush=True)
