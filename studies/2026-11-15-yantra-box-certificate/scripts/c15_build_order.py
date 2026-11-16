"""Build order for memory (17 Nov 2026; Palomar's standard runner has 4 cores and 16 GB, and `lake build` runs up to 4 modules
at once). The modules listed in data/lean-build-order.json ("solo", measured peak above the threshold given there) are put in one
chain: each imports the previous one (a plain, non-public `import`, marked "-- build order"), so lake never builds two of them
at the same time. The chain follows the real import graph (topological order), so no cycle can arise; the script checks it.
Nothing else changes: an extra import adds no axiom and changes no statement.
Run after the generators (it is idempotent: old build-order lines are removed first).
Usage: c15_build_order.py [LEANDIR]      FINAL ok iff the chain is acyclic and every solo module exists."""
import json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
LEAN = sys.argv[1] if len(sys.argv) > 1 else D_('lean')
cfg = json.load(open(D_('data', 'lean-build-order.json')))
TAG = '-- build order (memory): see scripts/c15_build_order.py'
path = lambda m: os.path.join(LEAN, *m.split('.')) + '.lean'
IMP = re.compile(r'^(?:public )?import (YantraCert\S*)', re.M)

def imports(m):
    return [x for x in IMP.findall(open(path(m)).read())]

# the YantraCert import graph, after removing earlier build-order lines
mods = []
for r, d, fs in os.walk(os.path.join(LEAN, 'YantraCert')):
    for f in fs:
        if f.endswith('.lean'):
            m = os.path.relpath(os.path.join(r, f), LEAN)[:-5].replace(os.sep, '.')
            t = open(path(m)).read(); t2 = '\n'.join(l for l in t.split('\n') if TAG not in l)
            if t2 != t: open(path(m), 'w').write(t2)
            mods.append(m)
G = {m: imports(m) for m in mods}
anc = {}
def ancestors(m):
    if m in anc: return anc[m]
    anc[m] = set()
    for x in G.get(m, []): anc[m] |= {x} | ancestors(x)
    return anc[m]
solo = cfg['solo']
missing = [m for m in solo if m not in G]
# topological order of the solo modules (ancestors first), ties by the listed order
order = []
left = list(solo)
while left:
    for m in left:
        if not any(x in ancestors(m) for x in left if x != m):
            order.append(m); left.remove(m); break
    else:
        print('FINAL FAIL (solo modules form a cycle)'); sys.exit(1)
for prev, m in zip(order, order[1:]):
    if m in ancestors(prev): print(f'FINAL FAIL ({m} is an ancestor of {prev})'); sys.exit(1)
    t = open(path(m)).read().split('\n')
    last = max(i for i, l in enumerate(t) if IMP.match(l))
    t.insert(last + 1, f'import {prev}  {TAG}')
    open(path(m), 'w').write('\n'.join(t)); G[m] = G[m] + [prev]
# acyclicity of the new graph
anc.clear(); state = {}
def dfs(m):
    state[m] = 1
    for x in G.get(m, []):
        if state.get(x) == 1 or (state.get(x) is None and not dfs(x)): return False
    state[m] = 2; return True
ok = all(state.get(m) == 2 or dfs(m) for m in G)
print('solo chain:', ' -> '.join(order))
print('FINAL ok' if ok and not missing else f'FINAL FAIL (cycle {not ok}, missing {missing})')
