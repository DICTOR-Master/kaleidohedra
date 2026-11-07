import re,html,json,statistics
from collections import Counter
exec(open('/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/51e0eb9e-694a-43f8-bd1f-4b85585fb441/scratchpad/audit.py').read().split('rows=[]')[0])
rows=[]
for m in re.finditer(r'<div class="paper[^"]*"[^>]*>(.*?)</div>',body,re.S):
    c=m.group(1)
    tm=re.search(r'<span class="t">(.*?)</span>\s*<span class="s">',c,re.S); t=T(tm.group(1)) if tm else ''
    dm=re.search(r'<span class="s">(.*?)</span>\s*<span class="(pdoi|btns)',c,re.S); d=T(dm.group(1)) if dm else ''
    full=t+' '+d; jh=sorted({j for j in J if j in full}); fh=len(F.findall(full))
    rows.append(dict(title=t,words=len(d.split()),jargon=jh,formula=fh,d=d))
N=len(rows); med=statistics.median(r['words'] for r in rows)
nf=sum(r['formula']>0 for r in rows); nj=sum(len(r['jargon'])>=4 for r in rows); nn=sum(bool(re.match(r'(#|Map|Paper)',r['title'])) for r in rows)
proved=sum(('Proved' in r['d'] or 'proved' in r['d']) for r in rows)
top=sorted(rows,key=lambda r:-(r['formula']*2+len(r['jargon'])))[:10]
FULL={'truncat':'truncated','rhombohedr':'rhombohedron','rhombic dodecahedr':'rhombic dodecahedron','polyhedr':'polyhedron','zonohedr':'zonohedron','cuboctahedr':'cuboctahedron','crystallograph':'crystallography','tessellat':'tessellation','parallelohedr':'parallelohedron','deltahedr':'deltahedron','stellation':'stellation'}
for r in rows: r['jargon']=sorted({FULL.get(j,j) for j in r['jargon']})
cj=Counter(j for r in rows for j in r['jargon'] if j not in ('Proved','proved')).most_common(20)
alts=re.findall(r'alt="([^"]*)"',body); FA=re.compile(r'[√φπ⊗ℤ²³μ]|\d+/\d+|\bcos\b|\bsin\b')
na=len(alts); naf=sum(bool(FA.search(a)) for a in alts); nae=sum(a=='' for a in alts)
li=lambda xs:''.join(f'<li>{x}</li>' for x in xs)
toprows=''.join(f'<tr><td>{html.escape(r["title"])}</td><td>{r["formula"]}</td><td>{html.escape(", ".join(r["jargon"]))}</td></tr>' for r in top)
H=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>dictospheres.com: Accessibility Audit</title><link rel="stylesheet" href="../paper.css">
<style>table.t{{border-collapse:collapse;font-size:8.8pt;width:100%;margin:2mm 0}} table.t td,table.t th{{border-bottom:1px solid #ccc;padding:1mm 1.5mm;text-align:left;vertical-align:top}} li{{margin:1mm 0}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>dictospheres.com: Accessibility Audit<br><span style="font-size:0.72em;font-weight:normal">Step 1 of the accessibility roadmap</span></h1>
<div class="meta"><b>DICTO</b> · dictospheres.com · 8 November 2026 · Audit of the live page as in the local copy (commit with the Version 11 book cards). Measured by script; read by Claude (Anthropic).</div>
<div class="status">Working document for DICTO, not for publication. Next: the glossary (step 2) and the "Start Here" page draft (step 3).</div>
<h2>1. The first screen</h2>
<p>A visitor sees: the name DICTO, the five solids behind the letters, "Geometric sculptor in Osaka using recycled PET", a DOI badge, and two buttons, "Read the books and papers" and "Open the app". There is no picture of a sculpture or of the PET work, no video, and no sentence on what the work is about or why it matters. The DOI badge, a library code, is the third thing on the page.</p>
<h2>2. The order of the page</h2>
<p>Apps · Books · Papers ({N} cards) · What's new · Discoveries · Work · Follow · Before you go. The physical art (B1NR at Fumin Hall ALTI, RHOMBITURE, the registered designs) is in "Work", sixth of eight sections, after about 50 000 characters of books and papers.</p>
<h2>3. Papers</h2>
<ul>{li([f"{N} cards; {nn} titles open with a paper number or label.", f"Median card text {med:.0f} words, up to {max(r['words'] for r in rows)}.", f"{nf} cards hold formulas or symbols (√, φ, fractions, sums); {nj} use four or more technical words.", f"{proved} cards say \"proved\": true and important, but it tells a newcomer this is for specialists.", "Most frequent technical words: "+", ".join(f"{w} ({n})" for w,n in cj)+"."])}</ul>
<p>One card title carries its DOI inside the title (#22 The Chain of Karma). The ten hardest cards (formula count, technical words):</p>
<table class="t"><tr><th>Card</th><th>Formulas</th><th>Technical words</th></tr>{toprows}</table>
<h2>4. Books</h2>
<p>Eight books; the turned-over cards are dense (the Golden Ladder card names E8, 600-cells and four-dimensional solids in its first lines). The books are the only part offered in seven languages.</p>
<h2>5. Discoveries</h2>
<p>Sixteen findings in technical names (Sunstar clusters, Dogstar, octet network, tridiminished icosahedra), text only, no pictures.</p>
<h2>6. Pictures and screen readers</h2>
<p>{na} image descriptions: {naf} contain formulas, which a screen reader reads out symbol by symbol (for example "2 cos(180°/p) = 1, √2, φ"); {nae} are empty (the decorative DICTO marks on the book backs are empty on purpose).</p>
<h2>7. Things to make and hold</h2>
<p>No printable nets or paper-craft downloads are offered on the site; one book card mentions origami nets. The apps hold nets, but nothing on the page leads to them.</p>
<h2>8. Already working for newcomers</h2>
<ul>{li(["\"New here? Try RHOMBIS\", the 3D puzzle: a low floor that already exists.","The tetrapod visitor book on the Misaki coast: playful and personal.","Book covers that turn over; seven languages for the books.","Paper images on every card."])}</ul>
<h2>9. What follows from it</h2>
<ul>{li(["Open with the physical work: one picture or film of a piece DICTO made, and one sentence on what the work is about (needs DICTO's footage).","Put a \"Start Here\" path first, before Apps: three visual rules, then the Before the Ladder lessons.","Give each paper card a first line in everyday words (from the glossary), with the technical text kept below it.","Rewrite the formula image descriptions in words.","Offer printable nets as their own section."])}</ul>
</body></html>'''
open('paper.html','w').write(H); print('ok',N,nf,nj,proved,na,naf,nae)
