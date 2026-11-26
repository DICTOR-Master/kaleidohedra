"""Pillars and floors (26 Nov 2026; DICTO: "like pillars and floors so the pentagon to square could be pillars and the others change as
floors"). With Claude (Anthropic). Step 1, combinatorics only: the 66 neighbour changes C116 -> Minana #377 (best T_h pairing,
data/c116/pairing.json), sorted into those touching a pillar (one face a pentagon/square) and floor-only ones (both faces among the
48 others), each with its distance (steps between the two faces in C116's face-neighbour graph) and its T_h orbit."""
import os, json, itertools
from collections import Counter, deque
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))
faces, gface = d['faces'], d['gface']; inv = {v: int(k) for k, v in d['assign'].items()}; mf = d['minana_faces']
pill = {k for k, f in enumerate(faces) if len(f) == 5}
def adjset(fl):
    return {frozenset((a, b)) for a in range(60) for b in range(a + 1, 60) if len(set(fl[a]) & set(fl[b])) == 2}
A0 = adjset(faces); A1 = {frozenset(inv[x] for x in e) for e in adjset(mf)}
lost, gained = A0 - A1, A1 - A0
print('neighbour pairs: kept', len(A0 & A1), 'lost', len(lost), 'gained', len(gained), flush=True)
nb = {k: set() for k in range(60)}
for e in A0:
    a, b = tuple(e); nb[a].add(b); nb[b].add(a)
def dist(a, b):
    q, seen = deque([(a, 0)]), {a}
    while q:
        x, k = q.popleft()
        if x == b: return k
        for y in nb[x]:
            if y not in seen: seen.add(y); q.append((y, k + 1))
kind = lambda e: 'pillar' if e & pill else 'floor'
def orbit(e): return frozenset(frozenset(gface[g][x] for x in e) for g in range(24))
for name, S_ in (('lost', lost), ('gained', gained)):
    orbs = {}
    for e in S_: orbs.setdefault(orbit(e), e)
    rows = sorted((kind(e), len(o), dist(*tuple(e)) if name == 'gained' else 1) for o, e in orbs.items())
    print(f'{name}: by kind {dict(Counter(kind(e) for e in S_))}; orbits (kind, size, C116 distance):', rows, flush=True)
deg0 = {k: len(nb[k]) for k in range(60)}; deg1 = Counter(x for e in A1 for x in e)
print('pillars: degree on C116 -> on Minana', sorted(Counter((deg0[k], deg1[k]) for k in pill).items()), flush=True)
print('floor faces: degree changes', sorted(Counter((deg0[k], deg1[k]) for k in range(60) if k not in pill).items()), flush=True)
# ---- every T_h-equivariant pairing: the gained pairs' C116 distances (a local change joins faces 2 apart) ----
ALLP = json.load(open(os.path.join(HERE, '../data/c116/pairings_all.json')))
rows = []
for s_ in ALLP:
    iv = {v: int(k) for k, v in s_.items()}; A1x = {frozenset(iv[x] for x in e) for e in adjset(mf)}
    g = A1x - A0; ds = Counter(dist(*tuple(e)) for e in g)
    rows.append((max(ds) if ds else 0, sum(k * c for k, c in ds.items()), len(g), dict(sorted(ds.items()))))
rows_unsorted = list(rows); rows.sort(key=lambda r: r[:3])
print('pairings', len(rows), '; best by (max distance, total distance):', rows[:5], flush=True)
print('pairings whose gains are all at distance 2:', sum(1 for r in rows if r[0] <= 2), flush=True)
# store the best pairing by distance (for the floor search)
bi = min(range(len(ALLP)), key=lambda i: rows_unsorted[i][:3])
json.dump(ALLP[bi], open(os.path.join(HERE, '../data/c116/pairing_local.json'), 'w')); print('best-by-distance pairing stored: data/c116/pairing_local.json', rows_unsorted[bi][:3], flush=True)
print('FINAL ok' if len(lost) == len(gained) == 66 and len(A0 & A1) == 108 and len(rows) > 0 else 'FINAL FAIL (counts differ from the known 108 kept, 66 changed)')
