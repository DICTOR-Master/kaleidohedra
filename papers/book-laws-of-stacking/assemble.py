# Assemble the book "HexOct: The Laws of Stacking" (second edition, DICTO 10-29; first edition "The Laws of Stacking") from the published paper sources (DICTO 10-28).
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
    ('12','real-materials-5',73),('13','magnets',74),
    ('14','two-tiles',75)]
PART={'1':'Part I. The laws','8':'Part II. Real materials','14':'Part III. HexOct'}
styles=set(); chapters=[]; sources=[]; toc=[]
cw=open(os.path.join(P,'collected','paper.html'),encoding='utf8').read()
PAPERS={int(m.group(1)):(html.unescape(re.sub('<[^>]+>','',m.group(2))),m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)',cw,re.S)}
INBOOK={num:('P' if lab=='Prologue' else lab) for lab,_,num in CH}
REFERRED=set()
def link_text(t):
    def r(mo):
        n=int(mo.group(1))
        if n in INBOOK: return f'<a href="#ch{INBOOK[n]}">#{n}</a>'
        if n in PAPERS: REFERRED.add(n); return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a>'
        return mo.group(0)
    return re.sub(r'(?<![&\w])#(\d{1,2})\b',r,t)
def link_html(h):
    parts=re.split(r'(<[^>]+>)',h); out=[]; inA=False
    for p in parts:
        if p.startswith('<'):
            if re.match(r'<a\b',p): inA=True
            if p.startswith('</a'): inA=False
            out.append(p)
        else: out.append(p if inA else link_text(p))
    return ''.join(out)
CORR=[('With this paper the series on real materials (#68, #70–#73) is complete.','The series on real materials (Chapters 8 to 12) was followed by a companion on magnets, Chapter 13.'),
      ('This study closes the line of work on materials.','This chapter closes the line of work on materials.')]
INDEX_TERMS=['HexOct','HexOct-K','Wang','silicon carbide','silicon','germanium','diamond','lonsdaleite','ice','tin','cobalt','iron','titanium','zirconium','magnesium','hydrogen','CrCoNi','perovskite','BaRuO','BaMnO','LiCoO','cathode','GaAs','InP','nanowire','spin ice','kagome','pyrochlore','Mn<sub>3</sub>Sn','Mn<sub>3</sub>Ir','rock salt','cadmium iodide','zinc blende','Laves','Fibonacci','golden ratio','ANNNI','stacking fault','Pauling','Onsager','Jagodzinski','Ganesha','Janus','octet','rhombic dodecahedron']
INDEX={}
# pass 2 (DICTO 10-28 'remove unrelated content'): cut sections and clauses about other lines of work (4D solids, named
# pairs, lists of other papers); theorems and proofs untouched. Sections renumbered after cuts.
CUTSEC={'the-focus':['5. The map'],'series-web-of-bonds':['3. Named pairs along the way','The papers of the series']}
EDITS={'two-tiles':[
 ('The Endless Stack Cell: every close-packed stacking is a string of two layer tiles','HexOct: every close-packed stacking is a string of two layer tiles, the c-tile and the h-tile')],
 'the-focus':[
 (', the Swap Rule (#61), the White Queen 600-cell and its Cleo shells (#62, #63), and the Red Queen 120-cell with Aristotle\'s five pyramids at the cores of the four-dimensional solids (#65).',' and the Swap Rule (#61).'),
 ('space, in the flat stackings and in the four-dimensional solids alike, is shared out','space in the flat stackings is shared out'),
 ('when a stacking or a view changes, pieces change by swapping','when a stacking changes, pieces change by swapping'),
 ('This paper does two things. It draws the map (§5), with the status of every link, and it proves the theorem','This chapter proves the theorem'),
 ('This paper sets out that focus: one map of how the threads of the recent papers meet, with the status of every link, and one new theorem that ties the flat stackings together.','This chapter sets out the new theorem that ties the flat stackings together.'),
 ('; and Regge calculus has used the 600-cell as a model universe (De Felice and Fabri, 2001; Tsuda and Fujiwara, 2020).','.'),
 ('Two further echoes, of form only: causal','One further echo, of form only: causal'),
 ('Space, in flat stackings and in the four-dimensional 600-cell alike, is shared out','Space in flat stackings is shared out'),
 ('when a view or a stacking changes','when a stacking changes')]}
def cut_sections(body,folder):
    for t in CUTSEC.get(folder,[]):
        body=re.sub(r'<h2>'+re.escape(t)+r'</h2>.*?(?=<h2>|$)','',body,flags=re.S)
    k=[0]
    def ren(mo):
        k[0]+=1; return f'<h2>{k[0]}. '
    if any(re.match(r'<h2>\d+[a-z]?\. ',h) for h in re.findall(r'<h2>[^<]*',body)):
        body=re.sub(r'<h2>\d+\. ',ren,body)
    return body
for label,folder,num in CH:
    s=open(os.path.join(P,folder,'paper.html'),encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>',s,re.S): styles.add(st.strip())
    doi=re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)',s); doi=doi.group(1) if doi else ''
    body=s[s.index('<h1'):s.rindex('</body>')]
    title=html.unescape(re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S).group(1))).strip()
    body=re.sub(r'<div class="meta">.*?</div>','',body,count=1,flags=re.S)
    # move sources / data / references out
    out=[]
    for m in re.finditer(r'<p class="prec">.*?</p>',body,re.S):
        if folder=='series-web-of-bonds' and 'Precisely' in m.group(0)[:60]: continue
        out.append(m.group(0))
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
    for a,b in EDITS.get(folder,[]):
        if a not in body: print('EDIT MISS',folder,a[:50])
        body=body.replace(a,b)
    if folder=='two-tiles':   # second edition (DICTO 10-29): the HexOct-K study closes the chapter, before its conclusion
        k=body.index('<h2>8. Conclusion</h2>'); body=body[:k]+open(os.path.join(HERE,'keyed.html'),encoding='utf8').read()+body[k:]
    body=cut_sections(body,folder)
    for a,b in CORR: body=body.replace(a,b)
    body=body.replace('this paper','this chapter').replace('This paper','This chapter')
    body=link_html(body)
    for term in INDEX_TERMS:
        if re.search(r'\b'+re.escape(term)+('' if term in ('BaRuO','BaMnO','LiCoO') or term.endswith('</sub>Sn') or term.endswith('</sub>Ir') else r'(s|es)?\b'),re.sub('<[^>]+>',' ',body) if '<' not in term else body): INDEX.setdefault(term,[]).append(tag)
    head=('Prologue. ' if label=='Prologue' else f'Chapter {label}. ')
    body=re.sub(r'<h1[^>]*>.*?</h1>',f'<h1 class="chapter" id="ch{tag}">{head}{title}</h1>',body,count=1,flags=re.S)
    body=body.replace('</h1>',f'</h1>\n<p class="from">From paper #{num}, DICTO DOI {doi}</p>',1)
    if label in PART: chapters.append(f'<div class="part"><h1 class="partt">{PART[label]}</h1></div>')
    chapters.append(f'<section class="ch">{body}</section>'); toc.append((head+title,tag,num,doi))
    sources.append(f'<h3>{head}{html.escape(title)} (#{num}, DICTO DOI {doi})</h3>'+''.join(out))
front=open(os.path.join(HERE,'front.html'),encoding='utf8').read()
epi=open(os.path.join(HERE,'epilogue.html'),encoding='utf8').read()
refhtml='<section class="app"><h1 class="chapter">Papers referred to, not in this book</h1><table>'+''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td></tr>' for n in sorted(REFERRED))+'</table></section>'
def nice(t): return re.sub('<[^>]+>','',t)
idxhtml='<section class="app"><h1 class="chapter">Index</h1><p style="font-size:9pt">Chapters (P = Prologue) in which each term appears.</p><table>'+''.join(f'<tr><td>{nice(t)}</td><td>{", ".join(v)}</td></tr>' for t,v in sorted(INDEX.items(),key=lambda kv:nice(kv[0]).lower()))+'</table></section>'
tochtml='<h2>Contents</h2><table class="toc">'+''.join(f'<tr><td>{html.escape(t)}</td><td>#{n}</td></tr>' for t,tag,n,d in toc)+'<tr><td>Epilogue. What has been shown</td><td></td></tr><tr><td>Appendix. Sources by chapter</td><td></td></tr><tr><td>Papers referred to, not in this book</td><td></td></tr><tr><td>Index</td><td></td></tr></table>'
css='\n'.join(sorted(styles))+'''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e}
table.toc td{border-bottom:1px dotted #ccc;padding:1.2mm 2mm} .titlepage{height:240mm;display:flex;flex-direction:column;justify-content:center}
.titlepage h1{font-size:30pt} section.epi,section.app{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li{font-size:8.6pt}
figure img{width:100%;display:block}
/* DICTO 10-29: neutral sans-serif for the whole book (the papers' DejaVu Serif read as Times-like) */
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}
body{font-size:10pt}'''
doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HexOct: The Laws of Stacking</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{front.replace('__TOC__',tochtml)}
{''.join(chapters)}
<section class="epi">{epi}</section>
<section class="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>Each chapter's own list of sources checked, data and code, as published with its paper.</p>{''.join(sources)}</section>
{refhtml}
{idxhtml}
{open(os.path.join(HERE,'about.html'),encoding='utf8').read()}
</body></html>'''
open(os.path.join(HERE,'paper.html'),'w',encoding='utf8').write(doc)
print('referred',len(REFERRED),'index terms',len(INDEX),'chapters',len(toc),'figures',sum(len(fs) for _,_,fs in os.walk(os.path.join(HERE,'figures'))),'chars',len(doc))
