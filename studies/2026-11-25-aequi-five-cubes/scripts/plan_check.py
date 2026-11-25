# Copy from study 2026-11-24-aequi-certify-extend, used unchanged except where marked 'study 2026-11-25' (groups.py here: the five-cube directions; mixed = RD directions from two or more cubes).
# every planned (class, m) of a stage searched completely?  usage: plan_check.py classes.json sol.jsonl "ci:m ci:m ..."
import json, sys
cls = json.load(open(sys.argv[1])); R = {}
for L in open(sys.argv[2]):
    try: r = json.loads(L)
    except Exception: continue
    R.setdefault((r['cls'], r['m']), set()).add(tuple(r['subset']))
bad = 0
for cm in sys.argv[3].split():
    ci, m = map(int, cm.split(':')); want = cls[ci]['counts'][str(m)]; got = len(R.get((ci, m), ()))
    print('%-4s class %2d m=%d sets %5d searched %5d' % (cls[ci]['name'], ci, m, want, got)); bad += got != want
sys.exit(1 if bad else 0)
