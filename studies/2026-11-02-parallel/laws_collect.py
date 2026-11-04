# First collection for "DICTO's Laws" (DICTO, 11-02): every paper's stated main result, as marked in its source
# (<... class="thm"> boxes, else the subtitle under the title). Output laws.json + laws.html. A collection only: statements are
# checked against their papers before use.
import re, json, html, glob, os
R = os.path.expanduser('~/k-research/papers'); cw = open(R + '/collected/paper.html').read()
num = {html.unescape(re.sub('<[^>]+>', '', m.group(2))).strip(): int(m.group(1)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>', cw, re.S)}
def clean(x): return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', x))).strip()
out = []
for f in sorted(glob.glob(R + '/*/paper.src.html')):
    s = open(f).read(); t = re.search(r'<h1>(.*?)</h1>', s, re.S)
    if not t: continue
    title = clean(t.group(1)); n = num.get(title)
    thm = [clean(m.group(1)) for m in re.finditer(r'<(?:p|div)[^>]*class="thm"[^>]*>(.*?)</(?:p|div)>', s, re.S)]
    sub = re.search(r'<p class="sub">(.*?)</p>', s, re.S)
    out.append(dict(paper=n, title=title, dir=os.path.basename(os.path.dirname(f)), main=thm[0] if thm else (clean(sub.group(1)) if sub else None),
                    n_boxes=len(thm), others=thm[1:4]))
out.sort(key=lambda r: (r['paper'] is None, r['paper'] or 0))
json.dump(out, open('laws.json', 'w'), indent=1, ensure_ascii=False)
with open('laws.html', 'w') as h:
    h.write('<meta charset="utf-8"><h1>DICTO\'s Laws: first collection</h1><ol>')
    for r in out: h.write(f"<li><b>#{r['paper']} {html.escape(r['title'])}</b><br>{html.escape(r['main'] or '(no marked statement)')}</li>")
    h.write('</ol>')
print(len(out), 'papers;', sum(1 for r in out if r['main']), 'with a statement;', sum(1 for r in out if not r['main']), 'without')
