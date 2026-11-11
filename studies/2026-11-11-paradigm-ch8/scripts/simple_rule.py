"""Chapter 8: which Wythoff polytopes are simple (clean scutoid tissues) and which are not (rosettes). Candidate rule read from the
Coxeter chain: SIMPLE iff every connected piece of the UNRINGED nodes is a chain of 3-bonds (type A) joined to exactly one ringed node,
at an end node of the piece. Checked against the Atlas (simple = every corner on exactly n edges) for all 0/1 seeds of A3, B3, H3, A4,
B4, F4, H4; for the non-simple ones, the cells at a corner (the rosette size)."""
import json, sys, itertools
CH = {'A3': [3, 3], 'B3': [4, 3], 'H3': [5, 3], 'A4': [3, 3, 3], 'B4': [4, 3, 3], 'F4': [3, 4, 3], 'H4': [5, 3, 3]}
def order(bonds, nodes):
    """order of the parabolic subgroup on a set of nodes of a chain (pieces of up to 3 nodes)"""
    nodes = sorted(nodes); total = 1; pieces = []
    for v in nodes:
        if pieces and pieces[-1][-1] == v - 1: pieces[-1].append(v)
        else: pieces.append([v])
    for p in pieces:
        b = tuple(bonds[k] for k in range(p[0], p[-1]))
        if len(p) == 1: total *= 2
        elif len(p) == 2: total *= 2 * b[0]
        elif len(p) == 3: total *= {(3, 3): 24, (4, 3): 48, (3, 4): 48, (5, 3): 120, (3, 5): 120}[b]
        else: raise ValueError(p)
    return total
def degree(bonds, lab):
    n = len(lab); U = {i for i in range(n) if not lab[i]}
    return sum(order(bonds, U) // order(bonds, U - {i - 1, i + 1}) for i in range(n) if lab[i])
def rule(bonds, lab): return degree(bonds, lab) == len(lab)
R = {}
for f in sys.argv[1:]: R.update(json.load(open(f)))
ok = True; table = []
for key, r in R.items():
    g = r['group']; lab = tuple(r['seed']) if isinstance(r['seed'], list) else tuple(json.loads(str(r['seed']).replace('(', '[').replace(')', ']')))
    pred = rule(CH[g], lab); d = degree(CH[g], lab); ok &= pred == r['simple'] and {str(d)} == set(map(str, r['degrees']))
    if pred != r['simple'] or {str(d)} != set(map(str, r['degrees'])): print('MISMATCH', key, 'degree', d, 'atlas', r['degrees'])
    if len(lab) == 4 and not r['simple']:
        table.append((g, lab, r['corners'], r['degrees']))
print(f"{len(R)} polytopes; edges per corner from the chain = the Atlas's measured degree, and simple iff it equals n, on all: {ok}")
for t in sorted(table): print('  not simple:', t)
print('FINAL ok' if ok else 'FINAL FAIL')
