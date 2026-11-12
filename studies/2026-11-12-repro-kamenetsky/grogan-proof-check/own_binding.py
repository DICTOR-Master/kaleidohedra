# Our own check (12 Nov 2026) that the Lean key literals keys5 / keys7 are exactly the keys defined by the paper's JSON specs and (14).
# usage: own_binding.py LEAN_DIR JSON_DIR
import sys, re, json
from fractions import Fraction as Q
from pathlib import Path
lean_dir, json_dir = Path(sys.argv[1]), Path(sys.argv[2])
def num(s):
    s = s.strip().strip('()')
    if '/' in s: a, b = s.split('/'); return Q(int(a), int(b))
    return Q(int(s))
ok = True
for d in (5, 7):
    text = (lean_dir / f'Tile{d}Data.lean').read_text()
    pat = re.compile(r'⟨!\[([^\]]*)\],\s*!\[([^\]]*)\],\s*!\[([^\]]*)\],\s*(true|false)⟩')
    lean = [(tuple(map(num, a.split(','))), tuple(map(num, b.split(','))), tuple(map(num, c.split(','))), t == 'true') for a, b, c, t in pat.findall(text)]
    j = json.loads((json_dir / f'tile{d}_final_spec.json').read_text()); k = d - 1; D = 4 * d
    xbar = [Q(i + 1, D) for i in range(k)]; w = [Q(1) / (4 * D) * (1 + Q(i, k)) for i in range(k)]; o = [w[i] / (i + 3) for i in range(k)]; h = Q(1, 48 * d)
    mine = []
    for r in j['facets' if d == 5 else 'rows']:
        c = r['cell']; a = r['normal_axis' if d == 5 else 'axis']; s = r['normal_side' if d == 5 else 'side']; ra = [i for i in range(d) if i != a]
        fc = [Q(c[i]) + (Q(1 + s, 2) if i == a else Q(1, 2)) for i in range(d)]
        for key in r['keys']:
            p = key['orientation_gamma']['perm'] if d == 5 else key['gamma_perm']; sg = key['orientation_gamma']['signs'] if d == 5 else key['gamma_sign']
            sigma = 1 if Q(key['signed_height']) > 0 else -1
            ctr = list(fc); rad = [Q(0)] * d; apex = list(fc)
            for i, ax in enumerate(ra):                 # tangent slot i carries reference axis p[i] with sign sg[i]
                ctr[ax] = fc[ax] + sg[i] * xbar[p[i]]; rad[ax] = w[p[i]]; apex[ax] = ctr[ax] + sg[i] * o[p[i]]
            apex[a] = fc[a] + sigma * s * h
            mine.append((tuple(ctr), tuple(rad), tuple(apex), sigma > 0))
    same = sorted(lean) == sorted(mine)
    print(f'd={d}: Lean literal keys {len(lean)}, keys from JSON + (14) {len(mine)}, same multiset: {same}', flush=True)
    ok &= same and len(lean) == (256 if d == 5 else 1024)
print('FINAL ok' if ok else 'FINAL FAIL')
