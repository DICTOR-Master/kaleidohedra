# Survey map of all works (DICTO 21 Nov: "a new survey ... map of all works").
# For every paper in the Concordance: which books cite it (by its DICTO DOI, concept or version, or by "#N"),
# its Concordance strands, and its latest Zenodo version. Papers in no book are listed as "no home yet".
# Usage: survey.py <papers dir> <out dir>. Text parsing only; no network.
import json, re, glob, os, sys
P, OUT = sys.argv[1], sys.argv[2]
C = json.load(open(f'{P}/dicto-concordance/concordance.json'))
papers = C['papers']
strands = {}
for s in C['strands']:
    for x in s['papers']: strands.setdefault(x['n'], []).append(s['name'])
# all DOIs (concept + versions) per paper: from zenodo-state.json + the concordance doi
dois = {n: {str(v['doi'])} for n, v in papers.items() if v.get('doi')}
for st in glob.glob(f'{P}/**/zenodo-state.json', recursive=True):
    try: j = json.load(open(st))
    except Exception: continue
    for n, v in papers.items():
        if str(j.get('conceptrecid')) in dois.get(n, set()) or str(j.get('id')) in dois.get(n, set()):
            dois[n] |= {str(j.get('conceptrecid')), str(j.get('id'))}
BOOKS = [b for b in sorted(os.listdir(P)) if b.startswith('book-') and not re.search(r'-(ar|fa|ja|zh)$', b) and b != 'book-arcs-2026-11-13']
text = {}
for b in BOOKS:
    t = ''
    for f in glob.glob(f'{P}/{b}/**/*.html', recursive=True):
        if re.search(r'/v\d+/|collected-v', f): continue
        t += open(f, encoding='utf-8', errors='ignore').read()
    text[b] = t
home = {}
for n in papers:
    for b, t in text.items():
        if any(d and re.search(r'zenodo\.' + d + r'\b', t) for d in dois.get(n, ())) or re.search(r'#' + re.escape(n) + r'(?![0-9a-z])', t):
            home.setdefault(n, []).append(b.removeprefix('book-'))
order = sorted(papers, key=lambda s: (int(re.match(r'\d+', s).group()), s))
rows = [{'n': n, 'title': papers[n]['title'], 'books': home.get(n, []), 'strands': strands.get(n, [])} for n in order]
os.makedirs(OUT, exist_ok=True)
json.dump(rows, open(f'{OUT}/survey-map.json', 'w'), indent=2, ensure_ascii=False)
with open(f'{OUT}/survey-map.md', 'w') as f:
    f.write(f'# Survey map of all works ({len(rows)} papers in the Concordance v{C["version"]})\n\n| # | Title | Books citing it | Strands |\n|---|---|---|---|\n')
    for r in rows: f.write(f"| {r['n']} | {r['title']} | {', '.join(r['books']) or '**no home yet**'} | {', '.join(r['strands']) or '—'} |\n")
    nohome = [r['n'] for r in rows if not r['books']]; nostrand = [r['n'] for r in rows if not r['strands']]
    f.write(f'\n**No home yet ({len(nohome)}):** {", ".join(nohome)}\n\n**In no strand ({len(nostrand)}):** {", ".join(nostrand)}\n')
    for b in BOOKS: f.write(f"\n- {b.removeprefix('book-')}: {sum(b.removeprefix('book-') in r['books'] for r in rows)} papers")
print('FINAL ok', len(rows), 'papers;', len(nohome), 'no home;', len(nostrand), 'no strand')
