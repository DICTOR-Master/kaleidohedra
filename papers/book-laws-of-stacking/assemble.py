# Assemble the book "The Laws of Stacking" (placeholder title) from the published paper sources (DICTO 10-28).
# Mechanical pass: each paper becomes a chapter (title, abstract, sections, theorems, figures kept word for word);
# the meta line goes; "Sources checked", "Data and code" and "References" move to one appendix by chapter;
# figures are copied into figures/<folder>/ and renumbered per chapter. Front matter and epilogue come from front.html
# and epilogue.html (written by hand). Output: paper.html (typeset by print.mjs).
import re, os, shutil, html
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.dirname(HERE)
CH=[('Prologue','series-web-of-bonds',58),
    ('1','2026-10-26-rule-of-halves',57),('2','pyrochlore-halves',60),('3','swap-rule',61),('4','swap-crystals',64),
    ('5','the-focus',66),('6','random-stackings-faults',67),('7','fibonacci-stackings',69),
    ('8','real-polytypes',68),('9','real-materials-2',70),('10','real-materials-3',71),('11','real-materials-4',72),
    ('12','real-materials-5',73),('13','magnets',74)]
PART={'1':'Part I. The laws','8':'Part II. Real materials'}
styles=set(); chapters=[]; sources=[]; toc=[]
for label,folder,num in CH:
    s=open(os.path.join(P,folder,'paper.html'),encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>',s,re.S): styles.add(st.strip())
    doi=re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)',s); doi=doi.group(1) if doi else ''
    body=s[s.index('<h1'):s.rindex('</body>')]
    title=html.unescape(re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S).group(1))).strip()
    body=re.sub(r'<div class="meta">.*?</div>','',body,count=1,flags=re.S)
    # move sources / data / references out
    out=[]
    for m in re.finditer(r'<p class="prec">.*?</p>',body,re.S): out.append(m.group(0))
    body=re.sub(r'<p class="prec">.*?</p>','',body,flags=re.S)
    m=re.search(r'<h2>References</h2>(.*?)(?=<h2|$)',body,re.S)
    if m: out.append(m.group(1)); body=body.replace(m.group(0),'')
    # figures: copy and renumber
    def fig(mo):
        src=mo.group(1); dst=f'figures/{folder}/{os.path.basename(src)}'
        os.makedirs(os.path.join(HERE,os.path.dirname(dst)),exist_ok=True)
        shutil.copy(os.path.join(P,folder,src),os.path.join(HERE,dst)); return f'<img src="{dst}"'
    body=re.sub(r'<img src="(figures/[^"]+)"',fig,body)
    tag='P' if label=='Prologue' else label
    body=re.sub(r'\bFigure (\d+)',lambda mo:f'Figure {tag}.{mo.group(1)}',body)
    body=re.sub(r'\bFig\. (\d+)',lambda mo:f'Fig. {tag}.{mo.group(1)}',body)
    head=('Prologue. ' if label=='Prologue' else f'Chapter {label}. ')
    body=re.sub(r'<h1[^>]*>.*?</h1>',f'<h1 class="chapter" id="ch{tag}">{head}{title}</h1>',body,count=1,flags=re.S)
    body=body.replace('</h1>',f'</h1>\n<p class="from">From paper #{num}, DICTO DOI {doi}</p>',1)
    if label in PART: chapters.append(f'<div class="part"><h1 class="partt">{PART[label]}</h1></div>')
    chapters.append(f'<section class="ch">{body}</section>'); toc.append((head+title,tag,num,doi))
    sources.append(f'<h3>{head}{html.escape(title)} (#{num}, DICTO DOI {doi})</h3>'+''.join(out))
front=open(os.path.join(HERE,'front.html'),encoding='utf8').read()
epi=open(os.path.join(HERE,'epilogue.html'),encoding='utf8').read()
tochtml='<h2>Contents</h2><table class="toc">'+''.join(f'<tr><td>{html.escape(t)}</td><td>#{n}</td></tr>' for t,tag,n,d in toc)+'<tr><td>Epilogue. The laws and the materials, in one table</td><td></td></tr><tr><td>Appendix. Sources by chapter</td><td></td></tr></table>'
css='\n'.join(sorted(styles))+'''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e}
table.toc td{border-bottom:1px dotted #ccc;padding:1.2mm 2mm} .titlepage{height:240mm;display:flex;flex-direction:column;justify-content:center}
.titlepage h1{font-size:30pt} section.epi,section.app{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li{font-size:8.6pt}
figure img{width:100%;display:block}'''
doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Laws of Stacking</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{front.replace('__TOC__',tochtml)}
{''.join(chapters)}
<section class="epi">{epi}</section>
<section class="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>Each chapter's own list of sources checked, data and code, as published with its paper.</p>{''.join(sources)}</section>
</body></html>'''
open(os.path.join(HERE,'paper.html'),'w',encoding='utf8').write(doc)
print('chapters',len(toc),'figures',sum(len(fs) for _,_,fs in os.walk(os.path.join(HERE,'figures'))),'chars',len(doc))
