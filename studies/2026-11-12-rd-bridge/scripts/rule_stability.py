# rule_stability.py: the RD pair rules of a scheme are read from a level-k supertile. They must be COMPLETE: every neighbour pair that
# occurs anywhere in an infinite hierarchical tiling must already occur at level k, else the true tiling would break the rules. Check:
# the rule set (type a, local direction, neighbour type, relative turn) and the type set are the same at levels k and k+1.
# usage: rule_stability.py <scheme> <k> <k+1>
import sys, os
here = os.path.dirname(os.path.abspath(__file__)); SCH, ks = sys.argv[1], [int(a) for a in sys.argv[2:4]]
res = {}
for k in ks:
    src = open(os.path.join(here, 'cut_down.py')).read(); src = src[:src.index('def sublattices')]
    sys.argv = ['cut_down.py', str(k), '1', '/dev/null']; g = {'__file__': os.path.join(here, 'cut_down.py')}; exec(src, g)
    f = g['SCHEMES'][SCH]; lab = {}; tid = {}
    for x in g['sites']:
        L, arg = g['canon'](f(g['entries'](x))); lab[x] = (tid.setdefault(L, len(tid)), tuple(sorted(g['RI'][R] for R in arg)))
    rules = set(); seen = set()
    for x in g['sites']:
        for d in g['NB']:
            y = g['vadd'](x, d)
            if y not in lab or (lab[x], lab[y], d) in seen: continue
            seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
            for r in Ra:
                R = g['ROT'][r]
                for q in Rb: rules.add((list(tid)[a], g['apply'](R, d), list(tid)[b], g['RI'][g['compose'](g['ROT'][q], g['inverse'](R))]))
    res[k] = (set(tid), rules); print(f'level {k}: types {len(tid)}, pair rules {len(rules)}', flush=True)
same = res[ks[0]] == res[ks[1]]
print(f'types equal: {res[ks[0]][0] == res[ks[1]][0]}; rules equal: {res[ks[0]][1] == res[ks[1]][1]}; new at level {ks[1]}: {len(res[ks[1]][1] - res[ks[0]][1])}', flush=True)
print('FINAL ok (rules complete by level %d)' % ks[0] if same else 'FINAL FAIL: rules still growing', flush=True)
