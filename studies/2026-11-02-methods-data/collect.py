# Data for a future methods paper on human-AI co-research (DICTO, 11-02; PAPER ON HOLD, data only).
# (1) commits of every repository, classified by message keywords; (2) the dated working rules (feedback-* memory notes only:
# method rules, no personal facts); (3) dated correction / incident lines from the work log. Output: commits.csv, commit-summary.md,
# rules.csv, corrections.csv, README-data.md. Keyword classes are a first sort, to be checked by hand before any use.
import subprocess, re, csv, os, glob, collections
H = os.path.expanduser('~'); MEM = H + '/.claude/projects/-home-dicto-Downloads-pet-bottle-rhombiverse/memory'
# k-research, k-mix and kaleidohedra are worktrees of ONE repository: listed once (--all covers every branch)
REPOS = {'kaleidohedra (research, apps, papers)': H + '/kaleidohedra', 'dictospheres (site)': H + '/dictospheres', 'rhombiverse': H + '/Downloads/pet-bottle-rhombiverse', 'references': H + '/Documents/kaleidohedra-references'}
CLS = [('withdrawal', r'\bwithdr'), ('correction', r'\bcorrect|\bwrong\b|\bmisread|\berratum|\bfix(e[ds])?\b.*\b(claim|number|caption|text|order|credit)'),
       ('bug fix', r'\bfix|\bbug\b|\brevert'), ('rename', r'\brenam'), ('publish/release', r'\bpublish|\brelease|\bzenodo|\bdoi\b'),
       ('verification', r'\bcheck|\bverif|\baudit|\bexact\b|\bproof\b|\bprove'), ('new work', r'.')]
def cls(m):
    m = m.lower()
    for k, rx in CLS:
        if re.search(rx, m): return k
rows = []; seen = set()
for name, path in REPOS.items():
    if not os.path.isdir(path + '/.git') and not os.path.isfile(path + '/.git'): continue
    out = subprocess.run(['git', '-C', path, 'log', '--all', '--no-merges', '--date=short', '--pretty=%h\t%ad\t%s'], capture_output=True, text=True).stdout
    for line in out.splitlines():
        h, d, s = (line.split('\t', 2) + ['', ''])[:3]
        if h in seen: continue
        seen.add(h); rows.append(dict(repo=name, hash=h, date=d, kind=cls(s), message=s))
with open('commits.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['repo', 'hash', 'date', 'kind', 'message']); w.writeheader(); w.writerows(rows)
tot = collections.Counter((r['repo'], r['kind']) for r in rows); kinds = [k for k, _ in CLS]
with open('commit-summary.md', 'w') as f:
    f.write('| repository | ' + ' | '.join(kinds) + ' | total | first | last |\n|' + '---|' * (len(kinds) + 4) + '\n')
    for name in REPOS:
        rr = [r for r in rows if r['repo'] == name]
        if not rr: continue
        f.write(f'| {name} | ' + ' | '.join(str(tot[(name, k)]) for k in kinds) + f' | {len(rr)} | {min(r["date"] for r in rr)} | {max(r["date"] for r in rr)} |\n')
    f.write(f'\nAll: {len(rows)} commits. Classes by message keywords only (first sort).\n')
rules = []
for p in sorted(glob.glob(MEM + '/feedback-*.md')):
    s = open(p).read(); name = re.search(r'^name:\s*(.+)$', s, re.M); desc = re.search(r'^description:\s*(.+)$', s, re.M)
    body = s.split('---', 2)[-1]; d = re.search(r'(20\d\d-\d\d-\d\d|\b1[01]-\d\d\b)', body); why = re.search(r'\*\*Why:\*\*\s*(.+)', body)
    rules.append(dict(rule=name.group(1) if name else os.path.basename(p), date=d.group(1) if d else '', firm='FIRM' in s[:600],
                      summary=desc.group(1) if desc else '', why=why.group(1) if why else ''))
with open('rules.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['rule', 'date', 'firm', 'summary', 'why']); w.writeheader(); w.writerows(sorted(rules, key=lambda r: r['date']))
corr = []
for line in open(MEM + '/open-work.md'):
    if re.search(r'CORRECT|INCIDENT|WRONG|misread|unsupported|withdrawn|superseded|my mistake', line, re.I):
        d = re.match(r'-\s*(\d\d-\d\d)', line.strip()); corr.append(dict(date=d.group(1) if d else '', line=line.strip()[:400]))
with open('corrections.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['date', 'line']); w.writeheader(); w.writerows(corr)
open('README-data.md', 'w').write(f'# Methods data (collected {subprocess.run(["date", "+%F %T"], capture_output=True, text=True).stdout.strip()})\n\n'
    f'- commits.csv: {len(rows)} commits from {len([n for n in REPOS if any(r["repo"] == n for r in rows)])} repositories, keyword class per message\n'
    f'- commit-summary.md: counts per repository and class\n- rules.csv: {len(rules)} dated working rules (method rules only, no personal notes)\n'
    f'- corrections.csv: {len(corr)} correction/incident lines from the work log\n\nPaper ON HOLD (DICTO 11-02). Classes are a first sort; check by hand before any use.\n')
print(len(rows), 'commits;', len(rules), 'rules;', len(corr), 'corrections')
