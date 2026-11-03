# Cross-links audit (DICTO 11-04: "make sure nothing is missed"): which papers share distinctive shapes, names or exact values
# but the later one does not cite the earlier. Reads ~/k-research/papers/*/paper.src.html and the site's card list for numbers.
import re, html, glob, os, math, json, collections
P = os.path.expanduser('~/k-research/papers'); SITE = os.path.expanduser('~/dictospheres/index.html')
txt = lambda s: html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)))
site = open(SITE).read()
cards = {}   # concept doi -> number
for m in re.finditer(r'class="num">#(\d+[a-z]?)</span>', site):
    seg = site[max(0, m.start() - 3000):m.start() + 3000]
    for d in re.findall(r'zenodo\.(\d{8})', seg): cards.setdefault(d, m.group(1))
papers = {}
SKIP = ('book-', 'plan-', 'proposed-batch', 'sa-batch', 'v3-batch', 'collected', 'japanese', 'figures-draft')
norm = lambda x: re.sub(r'[^a-z0-9]+', ' ', html.unescape(x).lower()).strip()
cardtitles = [(m.group(1), norm(m.group(2))) for m in re.finditer(r'class="num">#(\d+[a-z]?)</span>\s*([^<]+)</span>', site)]
files = []
for d in glob.glob(f'{P}/*/'):
    if d.rstrip('/').split('/')[-1].startswith(SKIP): continue
    for n in ('paper.src.html', 'paper.html'):
        if os.path.exists(d + n): files.append(d + n); break
for f in files:
    s = open(f).read(); t = txt(s); folder = f.split('/')[-2]
    title = (re.search(r'<title>([^<]*)', s) or [None, folder])[1]
    st = os.path.join(os.path.dirname(f), 'zenodo-state.json'); num = None
    if os.path.exists(st):
        try:
            j = json.load(open(st)); num = cards.get(str(j.get('conceptrecid'))) or cards.get(str(j.get('id')))
        except Exception: pass
    nt = norm(title)
    byt = [c for c, ct in cardtitles if ct and (nt.startswith(ct) or ct.startswith(nt))]
    if byt: num = byt[0]
    papers[folder] = dict(title=title, num=num, text=t, cites=set(re.findall(r'#(\d+)\b', t)), dois=set(re.findall(r'zenodo\.(\d{8})', t)),
                          concept=(json.load(open(st)).get('conceptrecid') if os.path.exists(st) else None))
# vocabulary: shape words and DICTO names (capitalised multiword) plus exact values
SHAPES = r"(?:truncated|rhombic|snub|great|small|golden|lesser|greater|stellated|cut)?\s?(?:tetrahedr|octahedr|cub|dodecahedr|icosahedr|icosidodecahedr|cuboctahedr|triacontahedr|tesseract|cell|honeycomb|octet|bipyramid|pyramid)\w*"
NAME = r"\b(?:[A-Z][a-z]+(?:[- ][A-Z][a-z]+){0,3})\b"
VAL = r"(?:\d+\s?[+−-]\s?)?(?:\d+/)?√\d+|1/φ\S?|φ[²³⁴⁵⁶]?|\b\d+/\d+\b"
STOP = set('The A An In On Of And For With From To By We Our This That These Those Each Every Figure Table Section Theorem Proof Proposition Lemma Corollary Version Main Part Here It Its Two Three Four Five Six One DICTO DOI Claude Anthropic View Licence Abstract Introduction Conclusion References Data Notes Status Draft January February March April May June July August September October November December Osaka Japan Zenodo Kaleidohedra Polyhedraverse Rhombiverse App Wikipedia'.split())
feat = {}
for k, p in papers.items():
    t = p['text']; f = collections.Counter()
    cut = [i for i in (t.rfind(' References '), t.rfind(' Sources '), t.rfind(' Bibliography ')) if i > len(t) * 0.5]
    if cut: t = t[:min(cut)]
    t = re.sub(r'\(([A-Z][a-z]+( and | et al\.?|, )?)+[^)]*\d{4}[^)]*\)', ' ', t)   # inline author-year citations
    for n in re.findall(NAME, t):
        if n.split()[0] in STOP or len(n) < 5: continue
        f['N:' + n] += 1
    for v in re.findall(VAL, t): f['V:' + v.replace(' ', '')] += 1
    for sh in re.findall(SHAPES, t, re.I): f['S:' + sh.lower().strip()] += 1
    feat[k] = {x: c for x, c in f.items() if c >= 2}
df = collections.Counter(x for f in feat.values() for x in f)
N = len(papers)
def score(a, b):
    sh = [x for x in feat[a] if x in feat[b] and 2 <= df[x] <= 8]   # distinctive: in 2..8 papers
    return sum(math.log(N / df[x]) for x in sh), sh
def cites(a, b):  # does a cite b?
    pa, pb = papers[a], papers[b]
    return (pb['num'] and pb['num'] in pa['cites']) or (pb['concept'] and str(pb['concept']) in pa['dois'])
rows = []
ks = sorted(papers)
for i, a in enumerate(ks):
    for b in ks[i + 1:]:
        sc, sh = score(a, b)
        if sc < 7: continue
        if cites(a, b) or cites(b, a): continue
        rows.append((round(sc, 1), a, papers[a]['num'], b, papers[b]['num'], sorted(sh, key=lambda x: df[x])[:10]))
rows.sort(reverse=True)
json.dump(rows, open('candidates.json', 'w'), ensure_ascii=False, indent=0)
print(N, 'papers;', sum(1 for p in papers.values() if p['num']), 'numbered;', len(rows), 'uncited pairs with score >= 12')
for r in rows[:45]: print(r[0], f"#{r[2]} {r[1]}", '<->', f"#{r[4]} {r[3]}", '|', '; '.join(r[5][:7])[:230])
