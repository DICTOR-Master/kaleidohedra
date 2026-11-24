# Shared loaders and the name rule for study 2026-11-24-aequi-catalogue-2.
import gzip, hashlib, json, os, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIES = os.path.dirname(HERE)
EXT = os.path.join(STUDIES, '2026-11-24-aequi-certify-extend', 'data')
NUMB = os.path.join(STUDIES, '2026-11-24-aequi-numberings')
OLD = os.path.join(STUDIES, '2026-11-19-aequi-complete', 'data', 'dice')
BATCHES = ['2a', '2caps', '2caps2', '2caps3']           # stable batch order (tie-break)
EXPECT = {'2a': 5935, '2caps': 336, '2caps2': 1375, '2caps3': 1910}
WITH_T = {'Oh', 'O', 'Td', 'Th', 'T', 'Ih', 'I'}
# Reserved 1233-1235 (decided 24 Nov): the three face-transitive permutahedron duals.
RESERVED = [(1233, 'Oh', 1, 24, 'TO-24'), (1234, 'Oh', 1, 48, 'TCO-48'), (1235, 'Ih', 1, 120, 'TID-120')]
ORDER = {'Ih': 120, 'Oh': 48}

# Name rule of study 2026-11-24-aequi-numberings (approved by DICTO 24 Nov), copied from its checks.py.
READ = {0: ["o", "re", "maru"], 1: ["i", "hi"], 2: ["ni", "fu"], 3: ["mi", "sa"], 4: ["yo", "shi"], 5: ["go", "ko"],
        6: ["mu", "ro"], 7: ["na"], 8: ["ya", "ha"], 9: ["ku"]}
SYL = {s: d for d, rs in READ.items() for s in rs}
def rule(n):
    o = []
    for ch in str(n):
        rs = READ[int(ch)]; s = rs[0]
        if o and s == o[-1] and len(rs) > 1: s = rs[1]
        o.append(s)
    w = "".join(o); return w[0].upper() + w[1:]
def parses(w):
    w = w.lower(); out = []
    def go(i, acc):
        if i == len(w): out.append(acc); return
        for s, d in SYL.items():
            if w.startswith(s, i): go(i + len(s), acc + str(d))
    go(0, ""); return out
def shown(n): return '%s (No.%d)' % (rule(n), n)
SHOWN_RE = re.compile(r'^([A-Z][a-z]+) \(No\.([1-9][0-9]*)\)$')

def load_batch(b):
    return json.load(gzip.open(os.path.join(EXT, 'aequi%s.json.gz' % b)))['new']

def sort_key(b, i, d):
    # each group one block: group order desc, group name, m asc, N asc; tie-break: corners, batch order, index in batch
    return (-int(d['sym_order']), d['group'], int(d['m']), int(d['N']), int(d['corners']), BATCHES.index(b), i)

# Congruence signature (description in checks.py, check 5).
Q = 1e4; stat = dict(gmargin=1.0, gap=9.0, width=0.0)
def sig(U, d):
    U = np.asarray(U, float); U = U / np.linalg.norm(U, axis=1)[:, None]; d = np.asarray(d, float); d = d / d.min()
    G = U @ U.T
    f = np.abs(G * Q - np.rint(G * Q)); stat['gmargin'] = min(stat['gmargin'], (0.5 - f.max()) / Q)
    ds = np.sort(d); cut = np.diff(ds) > 1e-7
    if cut.any(): stat['gap'] = min(stat['gap'], np.diff(ds)[cut].min())
    lev_s = np.r_[0, np.cumsum(cut)]
    for L in set(lev_s.tolist()): w = ds[lev_s == L]; stat['width'] = max(stat['width'], w.max() - w.min())
    lev = lev_s[np.searchsorted(ds, d - 5e-8)]
    gi = np.rint(G * Q).astype(np.int64)
    R = np.sort(gi * 1000 + lev[None, :], axis=1)
    R = np.c_[lev, R]; R = R[np.lexsort(R.T[::-1])]
    return hashlib.sha1(R.tobytes()).hexdigest() + ':%d' % len(d), ds
def congruent(a, b): return len(a) == len(b) and np.abs(a - b).max() < 1e-6
def find(table, key):
    h, ds = key; return [i for dd, i in table.get(h, []) if congruent(dd, ds)]
def add(table, key, i): table.setdefault(key[0], []).append((key[1], i))
import importlib.util
spec = importlib.util.spec_from_file_location('groups_ext', os.path.join(EXT, '..', 'scripts', 'groups.py'))
gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm); DIRS = gm.DIRS
def sig_new(d): return sig(DIRS[d['idx']], np.repeat(d['depths'], d['sizes']))
