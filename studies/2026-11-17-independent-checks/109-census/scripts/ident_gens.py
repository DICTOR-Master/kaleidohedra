"""Identify the census's H4 generator ids as actual H4 elements, from the census's own stored data
(600-cell and E8 orbit sets, whose point orderings are known), then check the 120-cell census
without its point ordering: for every census 120-cell group, recompute its orbits on our 120-cell
and compare (i) the stored orbit-size list, (ii) the (size, zeros) of every stored orbit set and
(iii) of every stored union set against our unions of two orbits of that group.
usage: python ident_gens.py CENSUS_DIR"""
import sys, os, json, itertools
from fractions import Fraction as Fr
from collections import Counter, defaultdict
import numpy as np
from core import *
from engine import *
from worlds import world

CEN = sys.argv[1]
J = {k: json.load(open(os.path.join(CEN, f'census-{v}.json'))) for k, v in
     (('600', 'U600'), ('E8', 'E8'), ('120', 'U120'))}
W6 = world('600'); W120 = world('120')
def s5(x):
    a, b = Fr(x[0]), Fr(x[1]); return (a + b / 2, b / 2)
o6 = np.array(sorted(range(120), key=lambda i: tuple(s5(c) for c in W6.exact[i])))
oE = np.concatenate([o6, o6 + 120])
H = W6.G.P                     # our H4, on our 600-cell indices
HE = np.concatenate([H, H + 120], axis=1)
ok = True

# constraints: id -> list of (universe, our-index set)
cons = defaultdict(list)
for U, o, PP in (('600', o6, H), ('E8', oE, HE)):
    d = J[U]
    for s in d['sets']:
        if s['kind'] != 'orbit': continue
        S = np.sort(o[np.array(s['rep'])])
        for gi in s['groups']:
            for g in d['groups'][gi]['gens']:
                cons[g].append((U, S))
def preserves(PP, n, S):
    m = np.zeros(n, bool); m[S] = True
    return m[PP[:, S]].all(1)
ids = sorted({g for d in J.values() for gr in d['groups'] for g in gr['gens']})
cand = {}
for g in ids:
    good = np.ones(len(H), bool)
    for U, S in cons[g]:
        good &= preserves(H if U == '600' else HE, 120 if U == '600' else 240, S)
    cand[g] = np.where(good)[0]
cnt = Counter(len(c) for c in cand.values())
print('generator ids:', len(ids), ' candidates per id (count: number of ids):', dict(sorted(cnt.items())))

# refine with group orbit-size lists on the 600-cell and E8: try all candidate combinations when small
def orbit_sizes(PP, n, gens):
    lab = components(n, [PP[g] for g in gens]); return sorted(np.bincount(lab).tolist())
resolved = {g: c for g, c in cand.items()}
for U, PP, n in (('600', H, 120), ('E8', HE, 240)):
    for gr in J[U]['groups']:
        gens = gr['gens']; want = sorted(gr['orbits'])
        opts = [resolved[g] for g in gens]
        if np.prod([len(x) for x in opts]) > 20000: continue
        keep = [set() for _ in gens]
        for combo in itertools.product(*opts):
            if orbit_sizes(PP, n, combo) == want:
                for i, c in enumerate(combo): keep[i].add(int(c))
        for g, k in zip(gens, keep):
            resolved[g] = np.array(sorted(set(resolved[g].tolist()) & k)) if k else np.array([], int)
cnt = Counter(len(c) for c in resolved.values())
print('after orbit-size refinement (candidates: ids):', dict(sorted(cnt.items())))

# 120-cell check, group by group, using every candidate combination (must agree for all)
d = J['120']; PC = W120.PU
sets_by_group = defaultdict(list)
for si, s in enumerate(d['sets']):
    for gi in s['groups']:
        sets_by_group[gi].append(si)
stats = Counter(); bad = []
for gi, gr in enumerate(d['groups']):
    opts = [resolved.get(g, np.array([], int)) for g in gr['gens']]
    if any(len(x) == 0 for x in opts):
        stats['group not identified'] += 1; continue
    if np.prod([len(x) for x in opts]) > 64:
        stats['group ambiguous (>64 combos)'] += 1; continue
    results = []
    for combo in itertools.product(*opts):
        lab = components(600, [PC[g] for g in combo])
        orbs = [np.where(lab == k)[0] for k in range(lab.max() + 1)]
        sizes = sorted(len(x) for x in orbs)
        oz = Counter((len(x), tuple(W120.T.zeros(x))) for x in orbs)
        results.append((sizes, oz, orbs))
    if any(r[0] != sorted(gr['orbits']) for r in results):
        stats['orbit sizes differ for some candidate'] += 1
    if all(r[0] != sorted(gr['orbits']) for r in results):
        stats['orbit sizes differ for every candidate'] += 1; bad.append(('sizes', gi)); continue
    sizes, oz, orbs = [r for r in results if r[0] == sorted(gr['orbits'])][0]
    stats['groups checked'] += 1
    uz = None
    for si in sets_by_group[gi]:
        s = d['sets'][si]; key = (s['size'], tuple(s['zeros']))
        if s['kind'] == 'orbit':
            stats['orbit sets checked'] += 1
            if key in oz: stats['orbit sets: (size, zeros) found among our orbits'] += 1
            else: stats['orbit sets: NOT found'] += 1; bad.append(('orbit', si, key))
        else:
            found = False
            for a, b in itertools.combinations(range(len(orbs)), 2):
                if len(orbs[a]) + len(orbs[b]) != s['size']: continue
                S = np.concatenate([orbs[a], orbs[b]])
                if tuple(W120.T.zeros(S)) == key[1]: found = True; break
            uz = {key} if found else set()
            stats['union sets checked'] += 1
            if key in uz: stats['union sets: (size, zeros) found among our unions of two orbits'] += 1
            else: stats['union sets: NOT found'] += 1; bad.append(('union', si, key))
for k, v in stats.items(): print(f'  {k}: {v}')
for b in bad[:30]: print('  MISMATCH', b)
covered = set()
for gi, gr in enumerate(d['groups']):
    pass
print('FINAL ok' if not bad else 'FINAL FAIL see mismatches')
