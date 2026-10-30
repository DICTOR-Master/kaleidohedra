# Assemble the book "The Golden Cycle" (placeholder title) from the published paper sources (DICTO 10-28).
# Mechanical pass: each paper becomes a chapter (title, abstract, sections, theorems, figures kept word for word);
# the meta line goes; "Sources checked", "Data and code" and "References" move to one appendix by chapter;
# figures are copied into figures/<folder>/ and renumbered per chapter. Front matter and epilogue come from front.html
# and epilogue.html (written by hand). Output: paper.html (typeset by print.mjs).
import re, os, shutil, html
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.dirname(HERE)
CH=[('1','chain-of-karma',22,'paper.html'),('2','spheres-of-dharma',23,'paper.html'),('3','bodhi-seed',24,'paper.html'),
    ('4','../studies/2026-10-13-fused-shells/paper',27,'paper.html'),('5','theaetetus',29,'paper.html'),
    ('6','dharma-inside-out',32,'paper.html'),('7','both-cycles',33,'paper.html'),('8','progenitors',34,'paper.html'),('9','progenitors-2',35,'paper.html'),
    ('10','2026-10-19-universal-pitet',38,'paper.html'),('11','2026-10-20-og-family-both-ways',39,'paper.html'),
    ('12','2026-10-21-kyushindo-cores',43,'paper.html'),('13','spiked-ti',78,'paper.html'),
    ('14','2026-10-25-gnomon-polar',54,'paper.html')]   # v2 (DICTO 10-30): #78 The Truncated Icosahedron Star as Chapter 13, before the gnomon, which closes the book
PART={'1':'Part I. Shells round a core','6':'Part II. The cycle turned and seeded','10':'Part III. The rule that grows the shells'}
styles=set(); chapters=[]; sources=[]; toc=[]
cw=open(os.path.join(P,'collected','paper.html'),encoding='utf8').read()
PAPERS={int(m.group(1)):(html.unescape(re.sub('<[^>]+>','',m.group(2))),m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)',cw,re.S)}
PAPERS.update({76:('Between the Queens','10.5281/zenodo.23780068'),77:('Face to Face','10.5281/zenodo.23779962'),78:('The Truncated Icosahedron Star (TI Star)','10.5281/zenodo.23782577')})   # papers newer than the Collected Works in use (v2)
INBOOK={num:lab for lab,_,num,_ in CH}
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
CORR=[('In short. ',''),('With this paper the series on real materials (#68, #70–#73) is complete.','The series on real materials (Chapters 8 to 12) was followed by a companion on magnets, Chapter 13.'),
      ('This study closes the line of work on materials.','This chapter closes the line of work on materials.')]
INDEX_TERMS=['TI Star','Star Halo','icosahedron','dodecahedron','icosidodecahedron','rhombic triacontahedron','truncated icosahedron','Hecatodihedron','Ogdoecontahedron','Metaxyhexecontahedron','Palintriacontahedron','pentakis dodecahedron','great stellated dodecahedron','AXE','CLEO','Cleo','FUJI','Lotus seed','Bodhi','Spheres of Dharma','Chain of Karma','golden ratio','golden rhombohedra','Dehn invariant','polar','gnomon','Euclid','Heron','Theaetetus','Kepler','Mosseri','PiTet','Cleo star','Kyushindo','tower','fullerene','600-cell','quasicrystal']
INDEX={}
# pass 2 (DICTO 10-28 'remove unrelated content'): cut sections and clauses about other lines of work (4D solids, named
# pairs, lists of other papers); theorems and proofs untouched. Sections renumbered after cuts.
CUTSEC={'chain-of-karma':['7. The 600-cell, flattened'],'theaetetus':['7. Theaetetus in the app'],'../studies/2026-10-13-fused-shells/paper':['5. In the apps and in paper']}
MOVESEC=r'(\d+\. )?(Reproducibility|Data and reproducibility|Data, scripts and checks|Credits|Appendix[ AB]*\. The reference library searched)'
EDITS={'2026-10-25-gnomon-polar':[('<b>In short.</b> ',''),('In short. ','')]}
def cut_sections(body,folder):
    for t in CUTSEC.get(folder,[]):
        body=re.sub(r'<h2>'+re.escape(t)+r'</h2>.*?(?=<h2>|$)','',body,flags=re.S)
    k=[0]
    def ren(mo):
        k[0]+=1; return f'<h2>{k[0]}. '
    if any(re.match(r'<h2>\d+[a-z]?\. ',h) for h in re.findall(r'<h2>[^<]*',body)):
        body=re.sub(r'<h2>\d+\. ',ren,body)
    return body
for label,folder,num,fname in CH:
    s=open(os.path.join(P,folder,fname),encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>',s,re.S): styles.add(st.strip())
    doi=re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)',s); doi=doi.group(1) if doi else ''
    doi=doi or {27:'10.5281/zenodo.23345502'}.get(num,'')   # #27 Capturing the In-betweens: its HTML carries no DOI line (DICTO 10-29)
    body=s[s.index('<h1'):s.rindex('</body>')]
    title=html.unescape(re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S).group(1))).strip()
    body=re.sub(r'<div class="meta">.*?</div>','',body,count=1,flags=re.S)
    # move sources / data / references out
    out=[]
    for m in re.finditer(r'<p class="prec">.*?</p>',body,re.S):
        out.append(m.group(0))
    body=re.sub(r'<p class="prec">.*?</p>','',body,flags=re.S)
    for m in list(re.finditer(r'<h2>('+MOVESEC+r'|References)</h2>(.*?)(?=<h2|$)',body,re.S)):
        out.append('<h4>'+m.group(1)+'</h4>'+m.group(4)); body=body.replace(m.group(0),'')
    # figures: copy and renumber
    def fig(mo):
        src=mo.group(1); dst=f'figures/ch{label}/{os.path.basename(src)}'
        raw='https://raw.githubusercontent.com/DICTOR-Master/kaleidohedra/master/'
        path=os.path.expanduser('~/k-mix/'+src[len(raw):]) if src.startswith(raw) else os.path.join(P,folder,src)
        if not os.path.exists(path): print('FIG MISSING',label,src); return mo.group(0)
        os.makedirs(os.path.join(HERE,os.path.dirname(dst)),exist_ok=True)
        shutil.copy(path,os.path.join(HERE,dst)); return f'<img src="{dst}"'
    body=re.sub(r'<img src="([^"]+)"',fig,body)
    tag='P' if label=='Prologue' else label
    body=re.sub(r'\bFigure (\d+)',lambda mo:f'Figure {tag}.{mo.group(1)}',body)
    body=re.sub(r'\bFig\. (\d+)',lambda mo:f'Fig. {tag}.{mo.group(1)}',body)
    for a,b in EDITS.get(folder,[]):
        body=body.replace(a,b)
    body=cut_sections(body,folder)
    for a,b in CORR: body=body.replace(a,b)
    body=body.replace('this paper','this chapter').replace('This paper','This chapter')
    body=link_html(body)
    for term in INDEX_TERMS:
        if re.search(r'\b'+re.escape(term)+('' if term in ('XXXX') or term.endswith('</sub>Sn') or term.endswith('</sub>Ir') else r'(s|es)?\b'),re.sub('<[^>]+>',' ',body) if '<' not in term else body): INDEX.setdefault(term,[]).append(tag)
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
idxhtml='<section class="app"><h1 class="chapter">Index</h1><p style="font-size:9pt">Chapters in which each term appears.</p><table>'+''.join(f'<tr><td>{nice(t)}</td><td>{", ".join(v)}</td></tr>' for t,v in sorted(INDEX.items(),key=lambda kv:nice(kv[0]).lower()))+'</table></section>'
tochtml='<h2>Contents</h2><table class="toc">'+''.join(f'<tr><td>{html.escape(t)}</td><td>#{n}</td></tr>' for t,tag,n,d in toc)+'<tr><td>Epilogue. What has been shown</td><td></td></tr><tr><td>Appendix. Sources by chapter</td><td></td></tr><tr><td>Papers referred to, not in this book</td><td></td></tr><tr><td>Index</td><td></td></tr></table>'
css='\n'.join(sorted(styles))+'''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e}
table.toc td{border-bottom:1px dotted #ccc;padding:1.2mm 2mm} .titlepage{height:240mm;display:flex;flex-direction:column;justify-content:center}
.titlepage h1{font-size:30pt} section.epi,section.app{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li{font-size:8.6pt}
figure img{width:100%;display:block}
/* DICTO 10-29: neutral sans-serif for the whole book, as in HexOct */
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}
body{font-size:10pt}'''
doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Golden Cycle</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{(re.sub(r'<div class="coverpage".*?</div>\n', '', front, count=1, flags=re.S) if os.environ.get('KDP') else front).replace('__TOC__',tochtml)}
{''.join(chapters)}
<section class="epi">{epi}</section>
<section class="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>Each chapter's own list of sources checked, data and code, as published with its paper.</p>{''.join(sources)}</section>
{refhtml}
{idxhtml}
{open(os.path.join(HERE,'about.html'),encoding='utf8').read()}
</body></html>'''
# figures re-made for the book (DICTO 10-29: Figure 1.1, the pulled-apart Lotus seed, re-shot so it fits the frame) replace the
# copies taken from the papers above, so a re-run can never put the old ones back
for root,_,fs in os.walk(os.path.join(HERE,'figures-fixed')):
    for f in fs: shutil.copy(os.path.join(root,f), os.path.join(HERE,'figures',os.path.relpath(os.path.join(root,f),os.path.join(HERE,'figures-fixed'))))
open(os.path.join(HERE,'paper.html'),'w',encoding='utf8').write(doc)
print('referred',len(REFERRED),'index terms',len(INDEX),'chapters',len(toc),'figures',sum(len(fs) for _,_,fs in os.walk(os.path.join(HERE,'figures'))),'chars',len(doc))
