"""Collect DICTO's integer lists from the studies' data files for an OEIS match.
A candidate is a run of >= 6 integers written as a list (comma, space or semicolon separated) in a data file (data*.txt, *.json,
*.csv, *.md tables) under ~/k-research/studies. Skipped as uninformative: runs with <= 2 distinct values, constant-difference runs
(arithmetic), runs that are all 0/1, and anything that looks like coordinates or dates (years 19xx/20xx, many negatives).
Output: candidates.json [{seq, files:[...], first_context}] deduplicated by the first 10 terms."""
import os, re, json, glob, sys
ROOT = os.path.expanduser('~/k-research/studies')
PAT = re.compile(r'(?<![\w./-])-?\d{1,15}(?:\s*[,;]\s*-?\d{1,15}){5,}(?![\w./])')
pats = ['data*.txt', '*.json', '*.csv', '*.md']
files = sorted({f for p in pats for f in glob.glob(os.path.join(ROOT, '**', p), recursive=True)} - set(glob.glob(os.path.join(ROOT, '2026-11-08-oeis-matcher', '*'))))
cands = {}
def boring(s):
    if len(set(s)) <= 3: return True
    if max(s.count(x) for x in set(s)) > len(s) // 2: return True   # mostly one value: accidental matches (digit counts etc.)
    d = [b - a for a, b in zip(s, s[1:])]
    if len(set(d)) == 1: return True
    if all(1900 <= x <= 2100 for x in s[:3]): return True
    if sum(x < 0 for x in s) > len(s) // 3: return True
    if max(abs(x) for x in s) < 3: return True
    # index lists (vertex/face/cell numbers): strictly increasing with mostly unit steps, or a long jumble of small labels
    if all(b > a for a, b in zip(s, s[1:])) and sum(x == 1 for x in d) >= len(d) / 3: return True
    if len(s) > 40 and not all(b >= a for a, b in zip(s, s[1:])): return True
    if len(set(s)) == len(s) and sorted(s) == list(range(min(s), min(s) + len(s))): return True   # a permutation of a range
    return False
KEYS = re.compile(r'(seq|count|shell|term|coord|loop|walk|census|tally|layer|number|by_|per_|cs\b|series|chain|growth|sizes|totals)', re.I)
BAD = re.compile(r'(face|vert|index|indices|edge_list|edge_len|dihedral|render|pts|points|coords|xyz|tri|cells_list)', re.I)
def json_lists(o, key=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from json_lists(v, str(k))
    elif isinstance(o, list):
        if len(o) >= 6 and all(isinstance(x, int) and not isinstance(x, bool) for x in o):
            if KEYS.search(key) and not BAD.search(key): yield o, key
        else:
            for v in o: yield from json_lists(v, key)
def runs(f):
    if f.endswith('.json'):
        try: o = json.load(open(f))
        except Exception: return
        for s, k in json_lists(o): yield s, 'key ' + k
        return
    t = open(f, errors='ignore').read()
    for m in PAT.finditer(t):
        line_start = t.rfind('\n', 0, m.start()) + 1
        yield [int(x) for x in re.split(r'\s*[,;]\s*', m.group(0))], t[line_start:m.start()].strip()[-120:]
for f in files:
    if '/reference-library/' in f or '/cache/' in f or os.path.getsize(f) > 5_000_000: continue
    for s, ctx in runs(f):
        if boring(s): continue
        key = tuple(s[:10])
        c = cands.setdefault(key, {'seq': s, 'files': [], 'context': ctx})
        if len(s) > len(c['seq']): c['seq'] = s
        rel = os.path.relpath(f, ROOT)
        if rel not in c['files']: c['files'].append(rel)
out = sorted(cands.values(), key=lambda c: (-len(c['seq']), c['files'][0]))
json.dump(out, open('candidates.json', 'w'), indent=1)
print(len(files), 'files scanned;', len(out), 'candidate lists')
print('FINAL ok' if out else 'FINAL FAIL: no candidates found')
