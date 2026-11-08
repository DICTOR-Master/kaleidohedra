# Rung 0, simpler: one idea per step, a picture, one sentence, one mnemonic, one line up, one line down, one thing to try.
exec(open('make_rung0.py').read().split("STEPS=[")[0])   # reuse drawing helpers and FIG1..FIG5
from math import *
def S(w,h,b):
    x0, y0, W, H = _bbox(b, w, h)   # frame fitted to everything drawn (guard 11-08)
    return f'<svg viewBox="{x0:.1f} {y0:.1f} {W:.1f} {H:.1f}" width="100%" style="max-height:48mm" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans" font-size="12">{b}</svg>'
dot=lambda x,y,c=K,r=5:f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
ln=lambda x1,y1,x2,y2,c=K,w=2:f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"/>'
def arc(cx,cy,r,a0,a1,c):
    a0,a1=radians(a0),radians(a1); big=1 if (a1-a0)>pi else 0
    return f'<path d="M{cx},{cy} L{cx+r*cos(a0):.1f},{cy-r*sin(a0):.1f} A{r},{r} 0 {big} 0 {cx+r*cos(a1):.1f},{cy-r*sin(a1):.1f} Z" fill="{c}" fill-opacity="0.5" stroke="{K}" stroke-width="0.8"/>'
P1=S(640,90,dot(100,45)+txt(100,80,'a point')+dot(260,45)+dot(400,45)+ln(260,45,400,45)+txt(330,80,'a line')+ln(520,60,600,60)+ln(520,60,575,15)+arc(520,60,30,0,40,G)+txt(560,85,'a turn'))
P2=S(640,110,arc(90,70,40,0,359.9,G)+txt(90,105,'full turn 360°')+arc(250,70,40,0,180,B)+txt(250,105,'half turn 180°')+arc(410,70,40,0,90,V)+txt(410,105,'quarter turn 90°')+ln(530,90,610,90)+ln(530,90,530,20)+txt(570,105,'a paper corner'))
P3=S(640,110,poly([(60,90),(170,90),(100,20)],G,K,1.2,.35)+poly([(230,90),(400,90),(370,40)],B,K,1.2,.35)+poly([(460,90),(520,90),(470,10)],V,K,1.2,.35)+poly([(560,90),(620,90),(600,60)],G,K,1.2,.35)+txt(320,108,'three points, three lines, three corners: no end to them',size=11))
P4=S(640,110,poly([(80,90),(140,90),(100,55)],G,K,1.2,.35)+poly([(220,90),(340,90),(260,20)],G,K,1.2,.35)+txt(210,108,'same shape, two sizes',size=11)+poly([(430,90),(550,90),(530,30)],B,K,1.2,.35)+txt(490,108,'another shape',size=11))
P_FOLD=S(640,120,around(5,3,140,60,40,V)+txt(140,115,'flat: a gap')+txt(320,65,'fold →',size=16)+poly([(470,95),(560,95),(515,20)],V,K,1.2,.45)+poly([(515,20),(560,95),(600,70)],V,K,1.2,.25)+poly([(515,20),(470,95),(440,70)],V,K,1.2,.25)+txt(515,115,'closed: a corner standing up'))
cx,cy=120,60
P_M=S(640,120,ln(cx,cy,cx+70,cy,K,3)+ln(cx,cy,cx+35,cy-60.6,K,3)+''.join(dot(cx+40*cos(radians(a)),cy-40*sin(radians(a)),G if a==30 else B,6) for a in (30,90,150,210,270,330))+txt(cx,115,'two mirrors: one bead, a ring of six')+FIG4.split('<svg',1)[1].split('>',1)[1].rsplit('</svg>',1)[0].split('<polygon',1)[0][:0]+''.join(poly(place(tri_from_angles(a,b,70),300+i*110,85),G,K,1.2,.35) for i,(a,b) in enumerate([(60,60),(45,90),(60,90)]))+txt(450,115,'three mirrors round a triangle: a floor'))
P_BALL='<img src="../book-golden-ladder/figures/ch1-fig1-kaleidoscopes.png" style="width:100%" alt="the mirror triangles on the ball">'
sph=S(640,130,'<circle cx="160" cy="65" r="55" fill="#f4efe2" stroke="#333"/><path d="M105,65 A55,18 0 0 0 215,65" fill="none" stroke="#333"/><path d="M160,10 A18,55 0 0 1 160,120" fill="none" stroke="#333"/><path d="M160,10 L160,65 Q 132 77 105 65" fill="none"/>'+f'<path d="M160,10 A18,55 0 0 1 177,72 A55,18 0 0 1 105,65 A55,55 0 0 1 160,10 Z" fill="{G}" fill-opacity=".55" stroke="#333"/>'+txt(160,128,'an eighth of an orange: three right angles')+txt(450,60,'on a ball, the three corners',size=12)+txt(450,78,'add up to MORE than a straight line',size=12))
STEPS=[
('A point','A point marks a place. It has no size.',P1,'<b>A point is where.</b>','two points give a line.','nothing: this is the ground.','Put a dot on paper. Put a second dot.'),
('A line','Two points fix exactly one straight line between them.','', '<b>A line is between.</b>','where two lines meet, they make a turn.','two points.','Join your two dots with a ruler. Try to draw a second straight line through both: you cannot.'),
('A turn','Where two lines meet they make an angle: how far you turn from one to the other. A full turn is 360°. Half a turn makes a straight line, 180°. A quarter turn is the corner of a sheet of paper, 90°.',P2,'<b>Full 360, half 180, quarter 90.</b>','three points, three lines and three turns make a triangle.','two lines meeting.','Stand up and turn round once, half, a quarter.'),
('A triangle','Any three points not on one line make a triangle. You can choose them in endless ways, so there are infinitely many triangles.',P3,'<b>Three points, three lines, three corners.</b>','so many triangles: which ones are really different?','points, lines, turns.','Draw three triangles that look as different as you can.'),
('Same shape','Make a triangle bigger, as a photocopier does, and its corners stay the same. Two triangles with the same corners have the same shape. Shape is what counts, not size.',P4,'<b>Bigger, same shape.</b>','what do the corners of every triangle have in common?','the triangle.','Photocopy or trace a triangle larger. Compare the corners.'),
('The corners make a line','Tear the three corners off any paper triangle and put them side by side. They always make a straight line: half a turn, 180°. So two corners decide the third.',FIG2,'<b>Three corners make one straight line.</b>','because two corners decide the shape, some shapes can be singled out.','the half turn.','Tear the corners off a paper triangle. Lay them together.'),
('Five special triangles','Five shapes carry the whole Ladder. The equal-sided triangle. Half a square: its long side is 1.41 times the short (√2). Half an equal-sided triangle: 1.73 (√3). Two triangles from the five-pointed star: 1.62, the golden ratio φ.',FIG1,'<b>Halve a square: √2. Halve a triangle: √3. Cut a star: φ.</b>','these numbers, 1, √2, √3 and φ, come back at the top of the rung.','two corners fix a shape.','Fold a square paper along its diagonal; fold an equal-sided triangle in half.'),
('Round a point','Put tiles round a point with no gaps: their corners must make a full turn. Six triangles, four squares or three hexagons fit exactly. Three pentagons leave a gap.',FIG3,'<b>Six, four, three fit. The pentagon leaves a gap.</b>','what happens if we close the gap?','the full turn.','Cut out three paper pentagons and put them round a point.'),
('Fold the gap','Close the gap by folding, and the corner stands up out of the paper: a corner of a solid. Less than a full turn folds up; a full turn stays flat.',P_FOLD,'<b>A gap folds up into a corner.</b>','how many solids can be made of equal faces?','tiles round a point.','Tape the three pentagons edge to edge across the gap. The corner rises.'),
('Five solids','With equal faces, exactly five corners fold up, and each closes into one solid. In DICTO order: Dodecahedron (3 pentagons at a corner), Icosahedron (5 triangles), Cube (3 squares), Tetrahedron (3 triangles), Octahedron (4 triangles). There are no more. Euclid ends his book with this.',FIG5,'<b>D·I·C·T·O.</b>','each solid can be seen in mirrors.','folded corners.','Make the five corners in paper.'),
('Mirrors','Two mirrors hinged at the right angle turn one bead into a ring: at 90°, four beads; at 60°, six. Three mirrors round one of three triangles make a whole floor.',P_M,'<b>Halve the turn, double the beads.</b>','three mirrors round a corner in space make a solid.','turns, and the special triangles.','Hinge two pocket mirrors and put a coin between them. Close them slowly.'),
('On a ball','Draw a triangle on a ball. Its corners add up to more than a straight line. An eighth of an orange has three right angles.',sph,'<b>Flat: a line. On a ball: more.</b>','now let the triangles on the ball be mirrors.','the straight line of the corners.','Cut an orange into eighths. Look at the corners of one piece.'),
('The triangle of mirrors: the first rung','The mirrors of each solid cut the ball round it into small equal triangles, each with corners 90°, 60° and one more: 60° for the tetrahedron, 45° for the cube and octahedron, 36° for the dodecahedron and icosahedron. Make that last corner 30° and the triangle lies flat: the floor of tightly packed balls. Each triangle has its number: 1, √2, φ, and √3 for the flat one. Everything golden lives in the φ triangle. This is where the Ladder begins.',P_BALL,'<b>Three kinds on the ball, one flat. One, root two, phi; root three on the floor.</b>','Chapter 1 of The Golden Ladder.','mirrors, the ball, the five solids and the special triangles.','Find the mirror triangle on a dice: the cube.'),
]
body=''
for i,(t,txt_,fig,mn,up,dn,tr) in enumerate(STEPS,1):
    body+=f'<div class="step"><h2>{i} · {t}</h2><p>{txt_}</p>'+(f'<figure>{fig}</figure>' if fig else '')+f'<p class="mn">{mn}</p><p class="br"><span class="u">↑</span> Next: {up}<br><span class="d">↓</span> Rests on: {dn}<br><span class="t">✋</span> Try: {tr}</p></div>'
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Golden Ladder, Rung 0</title>
<link rel="stylesheet" href="../paper.css">
<style>body{{font-size:11.5pt}} figure{{margin:2mm 0}} .step{{break-inside:avoid;margin-bottom:5mm}}
.mn{{font-size:12.5pt;border-left:3px solid {G};background:#fbf7ec;padding:1.5mm 3mm;margin:2mm 0}}
.br{{font-size:10pt;color:#444}} .u{{color:{B};font-weight:bold}} .d{{color:{V};font-weight:bold}} .t{{color:{G}}}</style></head>
<body>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>The Golden Ladder · Rung 0<br><span style="font-size:0.72em;font-weight:normal">From a Point to the Triangle of Mirrors</span></h1>
<div class="meta"><b>DICTO</b> (artist, Osaka, Japan) · dictospheres.com · A study companion to The Golden Ladder (DICTO DOI: 10.5281/zenodo.23966554) · Sample, version 2 · 8 November 2026<br>
DICTO proposed a ladder of lessons with mnemonics as bridges, to be climbed up and down. Drafting with Claude (Anthropic).</div>
<div class="status">Draft for DICTO's reading: sample of the format, simpler second try (one idea per step, no formulas). Not a record.</div>
<p class="hook">Thirteen small steps from a dot on paper to the first rung of the Ladder. Each step: one idea, one picture, one phrase to remember, what comes next, what it rests on, and something to try with your hands. Going down, read from 13 back to 1.</p>
{body}
</body></html>'''
open('paper.html','w').write(html); print('ok')
