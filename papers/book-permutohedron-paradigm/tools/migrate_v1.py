# One-off migration (13 Nov 2026): split the assembled 70-page draft (paper.html) into per-chapter sources with symbolic labels,
# so the book can be re-ordered on the arc of the proposal (PROPOSAL.html) and every number is assigned by assemble.py.
# Old label N.M becomes key oN.M: {{S:..}}/{{F:..}}/{{T:..}} declare, {{s:..}}/{{f:..}}/{{t:..}}/{{sec:..}} refer, {{ch:oN}} chapter.
# Output: tools/old/<label>.html (one per old chapter), front-old.html, epilogue-old.html, references-old.html. Run once.
import re, os, html
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = os.path.join(H, 'tools', 'old'); os.makedirs(O, exist_ok=True)
doc = open(os.path.join(H, 'paper.html'), encoding='utf8').read()
KIND = {'Theorem': 's', 'Lemma': 's', 'Proposition': 's', 'Corollar': 's', 'Figure': 'f', 'Table': 't', 'Section': 'sec'}
LW = r'(Theorems?|Lemmas?|Lemmata|Propositions?|Corollary|Corollaries|Figures?|Tables?|Sections?)'
NUM = r'\d{1,2}\.\d{1,2}'
def kind(w):
    for k, v in KIND.items():
        if w.startswith(k): return v
def conv_text(t):
    def lab(mo):
        k = kind(mo.group(1))
        nums = re.sub(NUM, lambda m: '{{%s:o%s}}' % (k, m.group(0)), mo.group(2))
        return mo.group(1) + mo.group(0)[len(mo.group(1)):len(mo.group(0)) - len(mo.group(2))] + nums
    t = re.sub(LW + r'(\s+)(' + NUM + r'′?(?:(?:,\s*|\s+and\s+|–|\s+to\s+|\s+or\s+)' + NUM + r'′?)*)', lambda mo: mo.group(1) + mo.group(2) + re.sub(NUM, lambda m: '{{%s:o%s}}' % (kind(mo.group(1)), m.group(0)), mo.group(3)), t)
    t = re.sub(r'\b(Chapters?)(\s+)(\d{1,2}(?:(?:,\s*|\s+and\s+|–|\s+to\s+)\d{1,2})*)\b', lambda mo: mo.group(1) + mo.group(2) + re.sub(r'\d+', lambda m: '{{ch:o%s}}' % m.group(0), mo.group(3)), t)
    return t
def conv(h):
    h = re.sub(r'<a href="https://doi\.org/[^"]*">(#\d+)</a>', r'\1', h)
    h = re.sub(r'<a href="#ch[0-9A-Za-z]+">(\d+)</a>', r'\1', h)
    out = []
    for p in re.split(r'(<[^>]+>)', h): out.append(p if p.startswith('<') else conv_text(p))
    h = ''.join(out)
    h = re.sub(r'<b>(Theorem|Lemma|Proposition|Corollary|Figure) \{\{(s|f):(o[\d.]+)\}\}(?!′)', lambda mo: '<b>%s {{%s:%s}}' % (mo.group(1), mo.group(2).upper(), mo.group(3)), h)
    h = re.sub(r'(<p style="font-size:9pt">Table )\{\{t:(o[\d.]+)\}\}', r'\1{{T:\2}}', h)
    h = re.sub(r'<h2>(\d+)\.(\d+) ', lambda mo: '<h2 data-k="o%s.%s">' % (mo.group(1), mo.group(2)), h)
    return h
for m in re.finditer(r'<section class="ch"><h1 class="chapter" id="ch([0-9A-Za-z]+)">(.*?)</h1>\s*<p class="sub">(.*?)</p>\s*<p class="from">(.*?)</p>(.*?)</section>', doc, re.S):
    lab, title, sub, frm, body = m.groups()
    open(os.path.join(O, f'{lab}.html'), 'w', encoding='utf8').write(f'<!--OLD title: {html.unescape(title)}\nsub: {sub}\nfrom: {frm}-->\n' + conv(body))
for f in ('front.html', 'epilogue.html', 'references.html'):
    open(os.path.join(O, f.replace('.html', '-old.html')), 'w', encoding='utf8').write(conv(open(os.path.join(H, f), encoding='utf8').read()))
print(sorted(os.listdir(O)))
