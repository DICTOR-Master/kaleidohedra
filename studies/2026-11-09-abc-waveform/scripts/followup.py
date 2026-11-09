"""Follow-up of scan CANDIDATES (patch exists, no torus found at index <= 3).
For each candidate (tag, rule, mirrors):
  (1) words admitted on a bigger patch (K slabs, n), to see what the wave forces in the stacking;
  (2) in-plane tori of index <= IMAX for the stacking words the candidate admits among S (= SS...), T^6 and (ST)^6, every skew.
Verdict: PERIODIC (torus found) / NO PATCH (patch dies at the bigger size) / STILL OPEN.
Usage: followup.py cand.json K n IMAX ntorus workers"""
import sys, os, json, time, itertools, numpy as np
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave_lib as W
t0 = time.time()
cands = json.load(open(sys.argv[1])); K, NP, IMAX, NT, NWK = (int(x) for x in sys.argv[2:7])
NRM = W.lean_normals(); H = W.H
MENU = {}
for name, n in NRM.items():
    offs = {H * j / 6 for j in range(-12, 13)}
    for j in range(-3, 3): offs |= {H * (j + 1 / W.PHI), H * (j + 1 / W.PHI ** 2)}
    MENU[name] = sorted(offs)
SR = [W.affine(W.P0, W.P0, p)[0] for p in W.SYM]
def planes_of(tag):
    kind, body = tag.split(':', 1); out = []
    for c, part in enumerate(body.split('+')):
        name, v = part.split('@'); v = float(v[:-1]) * H
        d = min(MENU[name], key=lambda x: abs(x - v)); assert abs(d - v) < 1e-3
        col = c if kind == '2c' else 0
        if kind in ('C3', 'C3v'):
            G = [R for R in SR if np.linalg.det(R) > 0] if kind == 'C3' else SR
            for R in G:
                q = (R @ NRM[name], d, 0)
                if not any(np.allclose(q[0], x[0]) and abs(q[1] - x[1]) < 1e-9 for x in out): out.append(q)
        else: out.append((NRM[name], d, col))
    return out
PATCH = {''.join(w): W.Structure(''.join(w), NP) for w in itertools.product('ST', repeat=K - 1)}
print(f"HEARTBEAT {time.time()-t0:.0f}s patch structures {len(PATCH)} (K={K}, n={NP})", flush=True)
MS = [(ha, hb, hd) for ha in range(1, IMAX + 1) for hd in range(1, IMAX + 1) if ha * hd <= IMAX for hb in range(ha)]
TOR = []
for u in [] if os.environ.get('NOTORI') else ('SS', 'TTTTTT', 'STSTSTSTSTST'):
    S = W.Structure(u * 2, NT if u == 'SS' else max(3, min(NT, 5)))
    for m in MS:
        for p_ in range(m[0]):
            for q_ in range(m[2]):
                cl = W.classes_for(S.Ps, u, 2, m, skew=p_ * W.a1 + q_ * W.a2)
                if cl is not None: TOR.append((f"{u}/{m}+skew({p_},{q_})", S, cl, m[0] * m[2]))
TOR.sort(key=lambda x: x[3])
print(f"HEARTBEAT {time.time()-t0:.0f}s tori {len(TOR)} (index <= {IMAX})", flush=True)
def run(c):
    deco = planes_of(c['tag']); mode, mirror = c['mode'], c['mirror']
    words = [w for w, S in PATCH.items() if W.solve(S, W.signatures(S, deco, mode), mirror)]
    per = None; sc = {}
    if words and not os.environ.get('NOTORI'):
        for lab, S, cl, idx in TOR:
            if id(S) not in sc: sc[id(S)] = W.signatures(S, deco, mode)
            if W.solve(S, sc[id(S)], mirror, cl): per = lab; break
    v = 'NO PATCH' if not words else ('PERIODIC ' + per if per else 'STILL OPEN')
    return dict(c, verdict2=v, words2=words)
with mp.get_context('fork').Pool(NWK) as pool:
    res = []
    for r in pool.imap_unordered(run, cands):
        res.append(r)
        print(f"  {r['tag']} {r['mode']} mirrors={'yes' if r['mirror'] else 'no'}: {r['verdict2']}  words {len(r['words2'])}/{2**(K-1)} {r['words2'][:8]}", flush=True)
json.dump(res, open(sys.argv[1].replace('.json', f'-followup-K{K}-n{NP}-I{IMAX}.json'), 'w'))
from collections import Counter
print('SUMMARY', Counter(r['verdict2'].split()[0] for r in res), flush=True)
openc = [r for r in res if r['verdict2'] == 'STILL OPEN']
print(f"STILL OPEN {len(openc)}", [(r['tag'], r['mode'], r['mirror']) for r in openc][:30], flush=True)
print('FINAL ok' if len(res) == len(cands) else 'FINAL FAIL: missing results', f'{time.time()-t0:.0f}s', flush=True)
