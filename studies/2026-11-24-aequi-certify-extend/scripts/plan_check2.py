# Part 2(b) completeness: every bounded orbit set (reduced by the normaliser) of each planned (class, m) has a record.
# usage: plan_check2.py classes.json sol.jsonl "ci:m ..."
import json, sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS
from solve import bounded
cls = json.load(open(sys.argv[1])); R = {}
for L in open(sys.argv[2]):
    try: r = json.loads(L)
    except Exception: continue
    R.setdefault((r['cls'], r['m']), set()).add(tuple(r['subset']))
bad = 0
for cm in sys.argv[3].split():
    ci, m = map(int, cm.split(':')); C = cls[ci]; orbs = C['orbits']; Np = [tuple(p) for p in C['normaliser_perms']]
    reps = {min(tuple(sorted(P[i] for i in S)) for P in Np) for S in itertools.combinations(range(len(orbs)), m)}
    reps = {S for S in reps if bounded(DIRS[[j for i in S for j in orbs[i]]])}
    got = R.get((ci, m), set()); print('%-3s m=%d sets %4d searched %4d' % (C['name'], m, len(reps), len(reps & got))); bad += not reps <= got
sys.exit(1 if bad else 0)
