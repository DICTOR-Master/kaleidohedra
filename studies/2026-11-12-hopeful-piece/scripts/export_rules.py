# export_rules.py, 12 Nov 2026 (aim 3, hopeful-piece hunt): CONTROL DATA ONLY. Export the face-to-face pair rules of marked-RD schemes
# from the RD bridge (studies/2026-11-12-rd-bridge/scripts/cut_down.py, read unchanged by exec of its preamble, as keyed_rd.py does), so
# that hunt.py's torus engine can be checked on sets with known answers:
#   CELL+EPART  periodic at torus index 4 (rd-bridge table);  CELLFRAME  no torus up to index 16 (rd-bridge job rd-cut16s);
#   FRAME+EFR   the 90-type set certified strongly aperiodic (rd-bridge, whole-chair chain): no torus at any index.
# Mechanism credit: Tsiokos (Chair44, arXiv 2609.19214); frames and certified assignment Kamenetsky (vendor code, MIT).
# Output JSON: {scheme: {"types": T, "rules": [[a, local dir index, b, relative turn index], ...]}} with dir index into NB and turn index
# into cut_down's ROT (24 proper rotations, make_group order; exported as matrices M with M x = apply(g, x)). usage: export_rules.py <level> <out.json> <schemes comma list>
import sys, os, json
BR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-11-12-rd-bridge', 'scripts')
BR = os.path.abspath(BR); sys.path.insert(0, os.path.join(BR, 'vendor'))
K_, OUTX, WANT = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3].split(',')
src = open(os.path.join(BR, 'cut_down.py')).read(); src = src[:src.index('def sublattices')]
sys.argv = ['cut_down.py', K_, '1', '/dev/null']; exec(src)
res = {}
for name in WANT:
    f = SCHEMES[name]; lab = {}; tid = {}
    for x in sites:
        L, arg = canon(f(entries(x))); lab[x] = (tid.setdefault(L, len(tid)), tuple(sorted(RI[R] for R in arg)))
    rules = set(); seen = set()
    for x in sites:
        for d in NB:
            y = vadd(x, d)
            if y not in lab or (lab[x], lab[y], d) in seen: continue
            seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
            for r in Ra:
                R = ROT[r]
                for q in Rb: rules.add((a, NB.index(apply(R, d)), b, RI[compose(ROT[q], inverse(R))]))
    res[name] = dict(types=len(tid), rules=sorted(rules), rot=[[[g[1][i] if j == g[0][i] else 0 for j in range(3)] for i in range(3)] for g in ROT], nb=NB)
    print(f'{name}: {len(tid)} types, {len(rules)} rules', flush=True)
json.dump(res, open(OUTX, 'w'))
print('FINAL ok', flush=True)
