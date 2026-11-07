# Assemble the book "HexOct: The Hexagonality Law" (retitled by DICTO 10-30; "HexOct: The Laws of Stacking" 10-29; first edition "The Laws of Stacking") from the published paper sources (DICTO 10-28).
# Mechanical pass: each paper becomes a chapter (title, abstract, sections, theorems, figures kept word for word);
# the meta line goes; "Sources checked", "Data and code" and "References" move to one appendix by chapter;
# figures are copied into figures/<folder>/ and renumbered per chapter. Front matter and epilogue come from front.html
# and epilogue.html (written by hand). Output: paper.html (typeset by print.mjs).
# v6 (DICTO 2026-10-31): plates.html, full-page plates of the tiles, stackings and named pieces, after Chapter 14 and before the
# epilogue; pictures from studies/2026-10-31-hexoct-plates (scripts/plates.py), kept in figures/plates/.
# v7 (DICTO 2026-11-01): Part IV, Chapter 15 The Window Law, from the paper papers/window-law (not yet published: its number and DOI
# were written [Window Law paper] until it was published as #84, 10.5281/zenodo.23848832, 1 November 2026); one sentence added to the conclusions of Chapters 3-8 and 10-14 so the whole
# book reads within the Window Law; plates stay after Chapter 14, before Part IV.
# v9 (2026-11-07): Part VI, Further results: Chapter 17 The Turned Twin, from the study note papers/study-note-trd (read by DICTO 4 Nov, taken in as a
# chapter, headings and cross-references adapted only), and Chapter 18 from further-results.html (written for the book from three studies). Chapters
# without a paper of their own are listed in NOTE; their own styles and draft boxes are not carried in.
# KDP=1: Amazon paperback interior (DICTO 10-29): no cover page (it goes on the printed cover), one blank page at the end
# so the count passes 79 (KDP allows spine text only above 79 pages).
import re, os, shutil, html
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.dirname(HERE)
CH=[('Prologue','series-web-of-bonds',58),
    ('1','2026-10-26-rule-of-halves',57),('2','pyrochlore-halves',60),('3','swap-rule',61),('4','swap-crystals',64),
    ('5','the-focus',66),('6','random-stackings-faults',67),('7','fibonacci-stackings',69),
    ('8','real-polytypes',68),('9','real-materials-2',70),('10','real-materials-3',71),('11','real-materials-4',72),
    ('12','real-materials-5',73),('13','magnets',74),
    ('14','two-tiles',75),
    ('15','window-law',84),
    ('16','2026-11-04-hexoct-narcissus',98),   # v8 (DICTO 2026-11-06 'both separate paper and chapter'): #98 Narcissus and Covenant, Part V
    ('17','study-note-trd',None),              # v9 (2026-11-07): the study note The Turned Twin, read by DICTO 4 Nov as a chapter of this book (Concordance waiting 7)
    ('18','./further-results',None)]           # v9: written for the book (further-results.html) from three studies (Concordance waiting 32, 21, 58)
PART={'1':'Part I. The laws','8':'Part II. Real materials','14':'Part III. HexOct','15':'Part IV. The Window Law','16':'Part V. The end of the walk','17':'Part VI. Further results'}
# v9: chapters with no paper of their own: (contents label, line under the chapter title, appendix note)
NOTE={'study-note-trd':('study note',"From DICTO's study note The Turned Twin (4 November 2026), which DICTO read and took into this book as a chapter; it has no separate DICTO DOI.",
        "<p>Study note, 4 November 2026: study 2026-11-04-trd (trd_checks.py, 11 PASS) and 2026-11-04-cuboctahedron-pyramids (12 PASS). Everything is checked numerically to 10<sup>−9</sup> (float, scipy) on the stackings ABC, AB, ABCB and ABCACB, and the node's ties from DICTO's own script turned_node_network.py. The TRD DICTOnode and its turned layout are DICTO's work; the note explains the geometry under it. Computation and drafting with Claude (Anthropic).</p>"),
      './further-results':('new',"New in this book (Version 9, 7 November 2026), from the studies 2026-11-04-hopf-interlock, 2026-11-04-fibonacci-spectrum and 2026-11-06-premise-challenge; it has no separate DICTO DOI.",'')}
styles=set(); chapters=[]; sources=[]; toc=[]
cw=open(os.path.join(P,'collected','paper.html'),encoding='utf8').read()
PAPERS={int(m.group(1)):(html.unescape(re.sub('<[^>]+>','',m.group(2))),m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)',cw,re.S)}
INBOOK={num:('P' if lab=='Prologue' else lab) for lab,_,num in CH if num}
WL='[Window Law paper]'
def pnum(num): return f'#{num}' if num else WL
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
CORR=[('<div class="abstract"><b>In short.</b> ','<div class="abstract">'),   # v8: banned label (print guard)
      ('DICTO asked whether they belong to that one structure or to stacking itself.','DICTO proposed that they belong not to that one structure but to stacking itself.'),   # v8: banned phrase (print guard)
      ('With this paper the series on real materials (#68, #70–#73) is complete.','The series on real materials (Chapters 8 to 12) was followed by a companion on magnets, Chapter 13.'),
      ('This study closes the line of work on materials.','This chapter closes the series on single materials; Part IV returns to the perovskites and adds the Frank–Kasper phases and the approximants of quasicrystals, under one theorem (Chapter 15).')]
INDEX_TERMS=['trapezo-rhombic dodecahedron','anticuboctahedron','Dyskin','Thue–Morse','Window Law','Swap defect','Frank–Kasper','Yarmolyuk','quasicrystal','approximant','Ammann–Beenker','HexOct','HexOct-K','Wang','silicon carbide','silicon','germanium','diamond','lonsdaleite','ice','tin','cobalt','iron','titanium','zirconium','magnesium','hydrogen','CrCoNi','perovskite','BaRuO','BaMnO','LiCoO','cathode','GaAs','InP','nanowire','spin ice','kagome','pyrochlore','Mn<sub>3</sub>Sn','Mn<sub>3</sub>Ir','rock salt','cadmium iodide','zinc blende','Laves','Fibonacci','golden ratio','ANNNI','stacking fault','Pauling','Onsager','Jagodzinski','Ganesha','Janus','octet','rhombic dodecahedron']
INDEX={}
# pass 2 (DICTO 10-28 'remove unrelated content'): cut sections and clauses about other lines of work (4D solids, named
# pairs, lists of other papers); theorems and proofs untouched. Sections renumbered after cuts.
CUTSEC={'the-focus':['5. The map'],'series-web-of-bonds':['3. Named pairs along the way','The papers of the series']}
C15={
 'swap-rule':('However the layers are stacked, the space is still built from the halves of two pure orders.',' Chapter 15 gives the rule its exact weight: a count fixed by two neighbouring layers is a straight line in the hexagonality exactly when it obeys the Swap Rule, and where it does not, the failure F(c, c) + F(h, h) − F(c, h) − F(h, c), the Swap defect, is the coefficient of the one further number the count needs.'),
 'swap-crystals':('One rule runs through all four families.',' By Chapters 5 and 15, every count of these swapping pieces therefore totals a straight line in the hexagonality.'),
 'the-focus':('and in cadmium iodide for each kind of layer.',' Chapter 15 sets this theorem in a wider frame, the Window Law: whatever a stacking fixes through g neighbouring layers averages to a linear function of the shares of its c/h words of length g, and the Swap Rule is exactly what brings a two-layer count down to one layer.'),
 'random-stackings-faults':('1, 2 and 3 for those of hexagonal crystals.',' Where a count breaks the Swap Rule, exactly one more number enters at two layers, the share p<sub>hh</sub> of neighbouring hexagonal pairs (Chapter 15).'),
 'fibonacci-stackings':('here at the level of the pieces themselves.',' Its hexagonal layers never touch, so its share p<sub>hh</sub> of neighbouring hexagonal pairs is zero, and every count of two neighbouring layers, Swap Rule or not, is read on a straight line in h; Chapter 15 carries this to the repeating approximants of quasicrystals, window after window.'),
 'real-polytypes':('and the departures of real crystals from it are what they add.',' In the terms of Chapter 15, with J<sub>3</sub> = 0 a property is the plane X = (2J<sub>1</sub> + 4J<sub>2</sub>)h − 4J<sub>2</sub>p<sub>hh</sub> in h and the share p<sub>hh</sub> of neighbouring hexagonal pairs: J<sub>2</sub> is the Swap defect (Δ = −4J<sub>2</sub>), and J<sub>3</sub> needs a window of three layers.'),
 'real-materials-3':("twice the second-neighbour coupling, is large.",' In the terms of Chapter 15, that second-neighbour coupling is a Swap defect: the part of a stacking energy that needs, besides h, the share p<sub>hh</sub> of neighbouring hexagonal pairs.'),
 'real-materials-4':('x ≤ 1 − h.',' Chapter 15 extends the count: per octahedron, face-sharing clusters number 1 − h and A neighbours 8 − 2h in every stacking, while the octahedra with exactly 0, 1 or 2 shared faces break the Swap Rule and are planes in h and p<sub>hh</sub>.'),
 'real-materials-5':('For ice the law turns a qualitative remark into a number to measure.',' In the terms of Chapter 15, the J<sub>2</sub> part of that distance is a plane in h and the share p<sub>hh</sub> of neighbouring hexagonal pairs, and only J<sub>3</sub> needs a window of three layers.'),
 'two-tiles':('with the stacking itself as the clock.',' Each tile is decided by its own layer, so the tiles are the Window Law\'s window of one layer (Chapter 15): every count of a stacking read tile by tile is a straight line in h.'),
 'window-law':("DICTO's book HexOct: The Hexagonality Law gathers the whole line of work.",''),
}
EDITS={
 'the-focus':[
 (', the Swap Rule (#61), the White Queen 600-cell and its Cleo shells (#62, #63), and the Red Queen 120-cell with Aristotle\'s five pyramids at the cores of the four-dimensional solids (#65).',' and the Swap Rule (#61).'),
 ('space, in the flat stackings and in the four-dimensional solids alike, is shared out','space in the flat stackings is shared out'),
 ('when a stacking or a view changes, pieces change by swapping','when a stacking changes, pieces change by swapping'),
 ('This paper does two things. It draws the map (§5), with the status of every link, and it proves the theorem','This chapter proves the theorem'),
 ('This paper sets out that focus: one map of how the threads of the recent papers meet, with the status of every link, and one new theorem that ties the flat stackings together.','This chapter sets out the new theorem that ties the flat stackings together.'),
 ('; and Regge calculus has used the 600-cell as a model universe (De Felice and Fabri, 2001; Tsuda and Fujiwara, 2020).','.'),
 ('Two further echoes, of form only: causal','One further echo, of form only: causal'),
 ('Space, in flat stackings and in the four-dimensional 600-cell alike, is shared out','Space in flat stackings is shared out'),
 ('when a view or a stacking changes','when a stacking changes')],
 'study-note-trd':[   # v9: headings, numbering and cross-references only
 ('The c/h words of the Hexagonality Law papers are therefore also words in RD and TRD.','The c/h words of this book are therefore also words in RD and TRD.'),
 ('after the turn the lower part of one meets the upper part of the next in a single plane, making a trapezoid.</p>','after the turn the lower part of one meets the upper part of the next in a single plane, making a trapezoid (the same half and turn as in Chapter 16, §4).</p>'),
 ('<li>Outside (Concordance 5.5): the Burgers','<li>Outside the book: the Burgers')]}
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
    s=open(os.path.join(HERE,folder[2:]+'.html') if folder.startswith('./') else os.path.join(P,folder,'paper.html'),encoding='utf8').read()
    if folder not in NOTE:   # v9: the study note's own style (gold .status, boxed tables) would restyle the whole book
        for st in re.findall(r'<style>(.*?)</style>',s,re.S): styles.add(st.strip())
    s=re.sub(r'<div class="status">.*?</ul></div>\s*','',s,flags=re.S)   # v9: a source's draft box never enters the book
    doi=re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)',s); doi=doi.group(1) if doi else ''
    body=s[s.index('<h1'):s.rindex('</body>')]
    title=html.unescape(re.sub('<[^>]+>','',re.sub(r'<br>\s*',': ',re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S).group(1)))).strip()
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
    if folder not in NOTE:   # v9: the note chapters have no figures and cite the book's figures by their book numbers (Figure 7.1)
        body=re.sub(r'\bFigure (\d+)',lambda mo:f'Figure {tag}.{mo.group(1)}',body)
        body=re.sub(r'\bFig\. (\d+)',lambda mo:f'Fig. {tag}.{mo.group(1)}',body)
    if folder in C15:
        a,b=C15[folder]
        if folder=='window-law': body=body.replace(a,'This book gathers the whole line of work, and this chapter closes it.')
        elif a not in body: print('C15 MISS',folder)
        else: body=body.replace(a,a+b,1)
    for a,b in EDITS.get(folder,[]):
        if a not in body: print('EDIT MISS',folder,a[:50])
        body=body.replace(a,b)
    # #75 v2 (DICTO 10-29) holds the HexOct-K section itself (with the stacking as the clock), so keyed.html is no longer inserted
    body=cut_sections(body,folder)
    for a,b in CORR: body=body.replace(a,b)
    body=body.replace('this paper','this chapter').replace('This paper','This chapter')
    body=link_html(body)
    for term in INDEX_TERMS:
        if re.search(r'\b'+re.escape(term)+('' if term in ('BaRuO','BaMnO','LiCoO') or term.endswith('</sub>Sn') or term.endswith('</sub>Ir') else r'(s|es)?\b'),re.sub('<[^>]+>',' ',body) if '<' not in term else body): INDEX.setdefault(term,[]).append(tag)
    head=('Prologue. ' if label=='Prologue' else f'Chapter {label}. ')
    body=re.sub(r'<h1[^>]*>.*?</h1>',f'<h1 class="chapter" id="ch{tag}">{head}{title}</h1>',body,count=1,flags=re.S)
    if folder in NOTE: body=body.replace('</h1>',f'</h1>\n<p class="from">{NOTE[folder][1]}</p>',1)
    else: body=body.replace('</h1>',f'</h1>\n<p class="from">From paper #{num}, DICTO DOI {doi}'+(". Numbers in brackets refer to the chapter's list of outside works in the Appendix." if folder=='window-law' else '')+'</p>' if num else f'</h1>\n<p class="from">From DICTO\'s paper {WL}, DICTO DOI at publication. Numbers in brackets refer to the chapter\'s list of outside works in the Appendix.</p>',1)
    if label in PART: chapters.append(f'<div class="part"><h1 class="partt">{PART[label]}</h1></div>')
    chapters.append(f'<section class="ch">{body}</section>'); toc.append((head+title,tag,NOTE[folder][0] if folder in NOTE else pnum(num),doi))
    if folder in NOTE: sources.append(f'<h3>{head}{html.escape(title)} ({NOTE[folder][0]}, no separate DICTO DOI)</h3>'+NOTE[folder][2]+''.join(out))
    else: sources.append(f'<h3>{head}{html.escape(title)} ({pnum(num)}, DICTO DOI {doi or 'at publication'})</h3>'+''.join(out))
PLATES_AT=next(i for i,c in enumerate(chapters) if 'partt">Part IV' in c)
front=open(os.path.join(HERE,'front.html'),encoding='utf8').read()
epi=open(os.path.join(HERE,'epilogue.html'),encoding='utf8').read()
refhtml='<section class="app"><h1 class="chapter">Papers referred to, not in this book</h1><table>'+''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td></tr>' for n in sorted(REFERRED))+'</table></section>'
def nice(t): return re.sub('<[^>]+>','',t)
idxhtml='<section class="app"><h1 class="chapter">Index</h1><p style="font-size:9pt">Chapters (P = Prologue) in which each term appears.</p><table>'+''.join(f'<tr><td>{nice(t)}</td><td>{", ".join(v)}</td></tr>' for t,v in sorted(INDEX.items(),key=lambda kv:nice(kv[0]).lower()))+'</table></section>'
tochtml='<h2>Contents</h2><table class="toc">'+''.join(f'<tr><td>{html.escape(t)}</td><td>{n}</td></tr>'+('<tr><td>Plates</td><td></td></tr>' if tag=='14' else '') for t,tag,n,d in toc)+'<tr><td>Epilogue. What has been shown</td><td></td></tr><tr><td>Appendix. Sources by chapter</td><td></td></tr><tr><td>Papers referred to, not in this book</td><td></td></tr><tr><td>Index</td><td></td></tr></table>'
css='\n'.join(sorted(styles))+'''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e}
table.toc td{border-bottom:1px dotted #ccc;padding:1.2mm 2mm} .titlepage{height:240mm;display:flex;flex-direction:column;justify-content:center}
.titlepage h1{font-size:30pt} section.epi,section.app{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li{font-size:8.6pt}
figure img{width:100%;display:block} figure.mid{width:auto} table.rules{font-size:8.6pt;margin:2mm 0 3mm} table.rules th{text-align:left} h2,h3{break-after:avoid}
section.plate{break-before:page;break-inside:avoid} section.plate>img{display:block;width:176mm;height:196mm;object-fit:contain;margin:0 auto}
.pcap h2{margin:3mm 0 1mm;font-size:13pt} .pcap p.pkey{font-size:8.6pt;color:#555;margin:0 0 1.5mm} .pcap ul{margin:0;padding-left:5mm} .pcap li{font-size:8.8pt;line-height:1.32;margin:0 0 .6mm}
/* DICTO 10-29: neutral sans-serif for the whole book (the papers' DejaVu Serif read as Times-like) */
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}
body{font-size:10pt}
/* v9: the draft box is red (paper.css), over the gold .status of one chapter's style */
.status{border:2px solid #a00;border-radius:2mm;padding:2mm 3mm;margin:3mm 0;font-size:9pt;color:#300;background:#fff6f6;break-inside:avoid} .status ul{margin:1mm 0 0;padding-left:5mm}'''
doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HexOct: The Hexagonality Law</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{(re.sub(r'<div class="coverpage".*?</div>\n', '', front, count=1, flags=re.S) if os.environ.get('KDP') else front).replace('__TOC__',tochtml)}
{''.join(chapters[:PLATES_AT])}
{open(os.path.join(HERE,'plates.html'),encoding='utf8').read()}
{''.join(chapters[PLATES_AT:])}
<section class="epi">{epi}</section>
<section class="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>Each chapter's own list of sources checked, data and code, as published with its paper.</p>{''.join(sources)}</section>
{refhtml}
{idxhtml}
{open(os.path.join(HERE,'about.html'),encoding='utf8').read()}
{'<section style="break-before:page">&nbsp;</section>' if os.environ.get('KDP') else ''}
</body></html>'''
open(os.path.join(HERE,'paper.html'),'w',encoding='utf8').write(doc)
print('referred',len(REFERRED),'index terms',len(INDEX),'chapters',len(toc),'figures',sum(len(fs) for _,_,fs in os.walk(os.path.join(HERE,'figures'))),'chars',len(doc))
