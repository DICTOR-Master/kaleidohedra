#!/usr/bin/env python3
"""Blueprint audit for paper.html (#119 draft).
1. Every <pre class="lean"> block must occur verbatim (whitespace collapsed, Lean comments removed) in the Lean
   sources: the Packets files and the Dehn Canon files vendored unchanged under Packets/Canon/.
2. Every Lean name in <code> inside the statement map (Table 3) must be declared in those sources.
3. Every theorem named in the map must appear in axioms.log with exactly [propext, Classical.choice, Quot.sound].
Usage: audit.py <packets entry dir>   (prints AUDIT OK on success)"""
import html, re, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
pk = pathlib.Path(sys.argv[1])
srcs = sorted((pk / 'Packets').glob('*.lean')) + sorted((pk / 'Packets' / 'Canon').glob('*.lean'))
def norm(s):
    s = re.sub(r'/-.*?-/', ' ', s, flags=re.S)
    s = re.sub(r'--[^\n]*', ' ', s)
    return ' '.join(s.split())
src = norm('\n'.join(p.read_text() for p in srcs))
page = (here.parent / 'paper.html').read_text()
bad = 0
blocks = re.findall(r'<pre class="lean">(.*?)</pre>', page, flags=re.S)
for b in blocks:
    raw = html.unescape(re.sub(r'<[^>]+>', '', b))
    for part in [norm(x) for x in re.split(r'\n\s*\n', raw) if x.strip()]:
        if part not in src:
            bad += 1; print('NOT IN SOURCE:', part[:160])
tab = re.search(r'<table class="w map">(.*?)</table>', page, flags=re.S).group(1)
names = set(re.findall(r'<code>([A-Za-z0-9_.αβγ]+)</code>', tab))
decl = set(re.findall(r'\b(?:theorem|lemma|def|structure|abbrev|noncomputable def)\s+([A-Za-z0-9_.αβγ]+)', src))
for n in sorted(names):
    if n.split('.')[-1] not in {d.split('.')[-1] for d in decl} and n not in decl:
        bad += 1; print('NOT DECLARED:', n)
ax = (here / 'axioms.log').read_text()
for n in sorted(names):
    m = re.search(r"'Packets\.%s' depends on axioms: \[(.*?)\]" % re.escape(n), ax)
    if m and m.group(1) != 'propext, Classical.choice, Quot.sound':
        bad += 1; print('AXIOMS:', n, m.group(1))
thms = [n for n in names if re.search(r'\btheorem\s+%s(?![\w.])' % re.escape(n), src) and n not in ('Packets',)]
missing = [n for n in thms if "'Packets.%s'" % n not in ax]
for n in missing:
    bad += 1; print('NO AXIOM LINE:', n)
print(f'{len(blocks)} Lean blocks, {len(names)} names, {len(thms)} theorems with axiom lines')
print('AUDIT OK' if bad == 0 else f'AUDIT FAILED ({bad})')
sys.exit(1 if bad else 0)
