"""Is pentagon -> square the best alignment? (27 Nov 2026; DICTO: "was the pentagon to square position ultimately the best change
alignment overall ... as we wish to replicate this study with other Aequi that fundamental question is worth asking").
With Claude (Anthropic). Combinatorics only. C116 (T_h) has face orbits 12 pentagons, 12 hexagons (A), 12 hexagons (B), 24 hexagons;
Minana #377 has 12 squares, 12 heptagons, 12 hexagons, 24 hexagons. Every T_h-equivariant bijection core faces -> Minana faces, for
EVERY assignment of the three 12-orbits (6 ways; the earlier study fixed pentagons -> squares), scored by:
  kept = neighbour pairs kept (of 174); lower bound on swaps = 174 - kept (a swap gains at most one pair);
  gained pairs' distances on C116 (a swap shortens any distance by at most 1, so a pair at distance d needs >= d - 1 swaps touching it);
  side change = sum over faces of |sides on Minana - sides on C116|.
Output data/c116/orbitpairs.json and a table per orbit assignment."""
import os, sys, json, itertools
from collections import Counter, deque
import numpy as np
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))
faces, gface, S = d['faces'], d['gface'], [np.array(m) for m in d['S']]
mf = d['minana_faces']
Dm = A.build("aequus-377")
mdir = np.array([[float(x) for x in u] for u, c in Dm["planes"]]); mdir /= np.linalg.norm(mdir, axis=1)[:, None]
Mg = [[int(np.argmax(mdir @ (S[g] @ mdir[t]))) for t in range(60)] for g in range(24)]
assert all(sorted(row) == list(range(60)) for row in Mg), 'T_h does not permute Minana faces in this frame'
def orbits(act):
    seen, out = set(), []
    for k in range(60):
        if k in seen: continue
        o = sorted({act[g][k] for g in range(24)}); seen |= set(o); out.append(o)
    return out
co, mo = orbits(gface), orbits(Mg)
cs = [len(f) for f in faces]; ms = [len(f) for f in mf]
print('C116 orbits (size, sides):', sorted((len(o), cs[o[0]]) for o in co), '; Minana:', sorted((len(o), ms[o[0]]) for o in mo), flush=True)
def adjset(fl): return {frozenset((a, b)) for a in range(60) for b in range(a + 1, 60) if len(set(fl[a]) & set(fl[b])) == 2}
A0, AM = adjset(faces), adjset(mf)
nb = {k: set() for k in range(60)}
for e in A0:
    a, b = tuple(e); nb[a].add(b); nb[b].add(a)
D = {}
for a in range(60):
    q, seen = deque([(a, 0)]), {a: 0}
    while q:
        x, k = q.popleft()
        for y in nb[x]:
            if y not in seen: seen[y] = k + 1; q.append((y, k + 1))
    D[a] = seen
def choices(o, mo_):
    k = o[0]; stab = [g for g in range(24) if gface[g][k] == k]; out = []
    for t in mo_:
        if all(Mg[g][t] == t for g in stab):
            sig = {}
            for g in range(24):
                j, u = gface[g][k], Mg[g][t]
                if sig.setdefault(j, u) != u: break
            else:
                if len(set(sig.values())) == len(o): out.append(sig)
    return out
c12 = [o for o in co if len(o) == 12]; c24 = [o for o in co if len(o) == 24]
m12 = [o for o in mo if len(o) == 12]; m24 = [o for o in mo if len(o) == 24]
assert len(c12) == len(m12) == 3 and len(c24) == len(m24) == 1
lab = lambda o, sides: f'{sides[o[0]]}-gon'
rows = []
for perm in itertools.permutations(range(3)):
    ch = [choices(c12[i], m12[perm[i]]) for i in range(3)] + [choices(c24[0], m24[0])]
    name = ', '.join(f'{lab(c12[i], cs)}{"" if cs[c12[i][0]] == 5 else "ABC"[i]}->{lab(m12[perm[i]], ms)}{"" if ms[m12[perm[i]][0]] != 6 else ""}' for i in range(3))
    n_eq = int(np.prod([len(c) for c in ch]))
    best = None; cnt = 0
    for combo in itertools.product(*ch):
        sig = {}
        for x in combo: sig.update(x)
        if len(set(sig.values())) != 60: continue
        cnt += 1; iv = {v: k for k, v in sig.items()}
        A1 = {frozenset(iv[x] for x in e) for e in AM}
        kept = len(A0 & A1); g = A1 - A0; ds = Counter(D[min(e)][max(e)] for e in g)
        side = sum(abs(ms[sig[k]] - cs[k]) for k in range(60))
        r = dict(kept=kept, lower_bound_swaps=174 - kept, max_dist=max(ds) if ds else 0,
                 dist_swaps=sum((k - 1) * c for k, c in ds.items()), dists=dict(sorted(ds.items())), side_change=side)
        key = (-kept, r['max_dist'], r['dist_swaps'])
        if best is None or key < best[0]: best = (key, r, {str(k): int(v) for k, v in sig.items()})
    rows.append(dict(assignment=name, perm=list(perm), choices_per_orbit=[len(c) for c in ch], pairings=cnt,
                     best=best[1] if best else None, best_pairing=best[2] if best else None))
    print(f'{name}: equivariant pairings {cnt} (choices per orbit {[len(c) for c in ch]}); best: '
          + (f"kept {best[1]['kept']}/174, swaps >= {best[1]['lower_bound_swaps']}, gained-pair distances {best[1]['dists']}, side change {best[1]['side_change']}" if best else 'none'), flush=True)
json.dump(rows, open(os.path.join(HERE, '../data/c116/orbitpairs.json'), 'w'))
ref = [r for r in rows if '5-gon->4-gon' in r['assignment'] and r['best']]
ok = bool(ref) and max(r['best']['kept'] for r in ref) == 108
print('control (pentagons -> squares best keeps 108, as before):', ok)
live = [r for r in rows if r['best']]
top = max(live, key=lambda r: (r['best']['kept'], -r['best']['max_dist']))
print('BEST ALIGNMENT OVERALL:', top['assignment'], top['best'])
print('FINAL ok' if ok else 'FINAL FAIL (control)')
