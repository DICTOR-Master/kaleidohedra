"""VERTICAL-PLANE WAVE pilot (DICTO 12 Nov 2026: "go ahead with the vertical plane wave pilot"; ledger retry 'route-4 vertical-plane
Ammann system only', lead 2 of this study). Two crest families that share the row direction a1 (b1 = lean B-ward, c1 = lean C-ward):
in the vertical plane across the rows (normal a1) they are the two crossing zigzag line directions, and the layers are the rows, so the
crest-spacing word along the stacking direction is the stacking word (an Ammann grid in that plane). New against the 9 Nov scan:
SEVERAL crests per family in one piece (1-2 offsets in b1 x 1-2 offsets in c1, offsets H*j/6), i.e. a two-family grid with uneven
spacing carried by one piece; colours: one wave (same colour) or two waves (b colour 0, c colour 1).
Rules STRICT / BEND x mirror copies yes / no (chiral = no, the Lemma-3 lesson). Tests exactly as scan.py (PATCH / PERIODIC / WORDS).
Controls: (1) empty decoration -> PATCH + PERIODIC, all words; (2) the 9 Nov designs 1 b1 + 1 c1 crest are re-run and must give the
9 Nov verdicts (checked afterwards by vplane_check.py against data/scan-*.json); (3) C3:c1@H/3 STRICT -> TTTT only (known forcing).
Usage: vplane.py K n PMAX IMAX nt [pilot_count] [workers]"""
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
NRM = W.lean_normals(); H = W.H
def offs(name):
    s = W.P0 @ NRM[name]; return [H * j / 6 for j in range(-12, 13) if s.min() + 1e-7 < H * j / 6 < s.max() - 1e-7]
OB, OC = offs('b1'), offs('c1')
SR = []
for p in W.SYM:
    R, t = W.affine(W.P0, W.P0, p); assert np.allclose(t, 0, atol=1e-9); SR.append(R)
def ckey(planes):
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
pl = []
for R in [R for R in SR if np.linalg.det(R) > 0]:
    q = (R @ NRM['c1'], H / 3, 0)
    if not any(np.allclose(q[0], x[0]) for x in pl): pl.append(q)
add('control-C3:c1@0.3333H', pl)
def subsets(O): return [c for r in (1, 2) for c in itertools.combinations(O, r)]
for sb in subsets(OB):
    for sc in subsets(OC):
        lab = 'b1@' + ','.join(f'{d/H:.4f}' for d in sb) + 'H+c1@' + ','.join(f'{d/H:.4f}' for d in sc) + 'H'
        for two in (False, True):
            add(('2w:' if two else '1w:') + lab, [(NRM['b1'], d, 0) for d in sb] + [(NRM['c1'], d, 1 if two else 0) for d in sc])
D = list(designs.values()); D = D[:2] + sorted(D[2:], key=lambda x: (len(x[1]), x[0]))
if PILOT: D = D[:2] + D[2:][::max(1, (len(D) - 2) // PILOT)][:PILOT]
DI = list(enumerate(D))
SH = os.environ.get('SHARD')
if SH:
    si, sm = map(int, SH.split('/')); DI = [x for x in DI if x[0] % sm == si or x[0] < 2]
SHTAG = f"-shard{SH.replace('/', 'of')}" if SH else ''
print(f"offsets b1 {len(OB)} c1 {len(OC)}; designs up to symmetry {len(designs)}; running {len(DI)}; K={K} n={NP} PMAX={PMAX} IMAX={IMAX} torus-n={NT}", flush=True)

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
        if k % 20 == 0: hb(f"{k+1}/{len(DI)} designs done"); print(f"PROGRESS {(k+1)/len(DI):.3f} designs", flush=True)
from collections import Counter
summ = Counter((x['mode'], x['mirror'], x['verdict'].split()[0]) for x in res)
print('SUMMARY', sorted(summ.items()), flush=True)
wc = Counter((x['mode'], x['mirror'], len(x['words'])) for x in res if x['words'])
print('PATCH-WORD COUNTS (mode, mirrors, #words admitted): designs', sorted(wc.items()), flush=True)
json.dump(res, open(os.path.join(OUT, f'vplane-K{K}-n{NP}-P{PMAX}-I{IMAX}{"-pilot" if PILOT else ""}{SHTAG}.json'), 'w'))
ctrl = [x for x in res if x['design'] == 0]
c3 = [x for x in res if x['design'] == 1 and x['mode'] == 'STRICT']
CTRL_OK = all(x['verdict'].startswith('PERIODIC') and len(x['words']) == 2 ** (K - 1) for x in ctrl) and len(ctrl) == 2 and len(c3) == 2 and all(x['words'] == ['T' * (K - 1)] for x in c3)
print('CONTROL C3:c1 STRICT words', [x['words'] for x in c3], flush=True)
nondeg = Counter(tuple(sorted(x['words'])) for x in res if x['words'] and 'S' * (K - 1) not in x['words'] and 'T' * (K - 1) not in x['words'])
print('WORD SETS WITHOUT BOTH CONSTANT WORDS (the only possible non-repeating signals):', nondeg.most_common(10), flush=True)
cands = [(x['design'], x['tag'], x['mode'], x['mirror']) for x in res if x['verdict'] == 'CANDIDATE']
print(f"CANDIDATES {len(cands)} {cands[:20]}", flush=True)
print('FINAL ok' if (CTRL_OK and GEOM_OK) else f'FINAL FAIL: control {ctrl} geom {GEOM_OK}', f'{time.time()-t0:.0f}s', flush=True)
