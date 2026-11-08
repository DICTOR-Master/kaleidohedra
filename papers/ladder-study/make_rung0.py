# Rung 0 of the Golden Ladder study companion: from a point to the triangle of mirrors.
from math import *
G='#b8962e'; B='#3b6fb6'; V='#7a4fa6'; K='#333'; L='#bbb'
import re as _re
def _bbox(body, w, h):
    """frame fitted to everything drawn (GUARD 11-08, DICTO: figures were clipped): points, lines, circles, and text by its anchor"""
    xs, ys = [0, w], [0, h]
    for m in _re.finditer(r'points="([^"]+)"', body):
        for pr in m.group(1).split():
            x, y = pr.split(','); xs.append(float(x)); ys.append(float(y))
    for m in _re.finditer(r'<line [^>]*x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', body):
        xs += [float(m.group(1)), float(m.group(3))]; ys += [float(m.group(2)), float(m.group(4))]
    for m in _re.finditer(r'<circle [^>]*cx="([-\d.]+)" cy="([-\d.]+)" r="([-\d.]+)"', body):
        cx, cy, r = map(float, m.groups()); xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
    for m in _re.finditer(r'<text x="([-\d.]+)" y="([-\d.]+)" text-anchor="(\w+)" font-size="([\d.]+)"[^>]*>([^<]*)</text>', body):
        x, y, anc, sz, t = float(m.group(1)), float(m.group(2)), m.group(3), float(m.group(4)), m.group(5)
        tw = 0.66 * sz * len(t); x0 = x - tw / 2 if anc == 'middle' else (x - tw if anc == 'end' else x)
        xs += [x0, x0 + tw]; ys += [y - sz, y + 0.4 * sz]
    pad = 8
    return min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
def svg(w,h,body):
    x0, y0, W, H = _bbox(body, w, h)
    return f'<svg viewBox="{x0:.1f} {y0:.1f} {W:.1f} {H:.1f}" width="100%" style="max-height:62mm" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans" font-size="11">{body}</svg>'
def poly(pts,fill='none',stroke=K,sw=1.4,op=1): return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>'
def txt(x,y,s,anchor='middle',size=11,col=K): return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{col}">{s}</text>'
def tri_from_angles(A,Bang,base=80):
    # triangle with base angles A (left), Bang (right)
    a,b=radians(A),radians(Bang); C=pi-a-b
    side=base*sin(b)/sin(C)
    return [(0,0),(base,0),(side*cos(a),-side*sin(a))]
def place(pts,x0,y0,s=1): return [(x0+s*x,y0+s*y) for x,y in pts]

# Fig 1: special triangles
f1=''
shapes=[((60,60),'equilateral','60° 60° 60°','1',G),((45,90),'half a square','90° 45° 45°','√2',B),((60,90),'half an equilateral','90° 60° 30°','√3',B),((72,72),'golden triangle','36° 72° 72°','φ',V),((36,36),'golden gnomon','108° 36° 36°','φ',V)]
for i,((a,b),name,ang,num,col) in enumerate(shapes):
    p=tri_from_angles(a,b,70 if i!=4 else 100); xs=[q[0] for q in p]; ys=[q[1] for q in p]
    x0=20+i*125+(100-(max(xs)-min(xs)))/2-min(xs); y0=95
    f1+=poly(place(p,x0,y0),col,K,1.2,0.35)+txt(70+i*125,115,name,size=10)+txt(70+i*125,129,ang,size=9.5)+txt(70+i*125,145,'number '+num,size=10,col=col)
FIG1=svg(640,150,f1)

# Fig 2: tear off the corners
f2=poly([(30,110),(190,110),(80,30)],'#eee')
for (x,y,c) in [(30,110,G),(190,110,B),(80,30,V)]: f2+=f'<circle cx="{x}" cy="{y}" r="7" fill="{c}" opacity="0.8"/>'
cx,cy=420,110; f2+=f'<line x1="300" y1="{cy}" x2="540" y2="{cy}" stroke="{K}" stroke-width="1.4"/>'
# angles of triangle
import cmath
A=degrees(atan2(80,50)); Bq=degrees(atan2(80,110)); C=180-A-Bq
start=0
for ang,c in [(Bq,B),(C,V),(A,G)]:
    a0,a1=radians(start),radians(start+ang); r=60
    f2+=f'<path d="M{cx},{cy} L{cx+r*cos(a0):.1f},{cy-r*sin(a0):.1f} A{r},{r} 0 0 0 {cx+r*cos(a1):.1f},{cy-r*sin(a1):.1f} Z" fill="{c}" fill-opacity="0.55" stroke="{K}" stroke-width="0.8"/>'
    start+=ang
f2+=txt(110,135,'any triangle')+txt(420,135,'its three corners, side by side: a straight line, 180°')+txt(245,75,'→',size=22)
FIG2=svg(640,145,f2)

# Fig 3: round a point
def regpoly(n,cx,cy,r,rot=0): return [(cx+r*cos(rot+2*pi*k/n),cy+r*sin(rot+2*pi*k/n)) for k in range(n)]
def around(n,k,cx,cy,s,col):
    # k regular n-gons sharing vertex (cx,cy)
    out=''; ang=pi-2*pi/n  # interior angle
    for j in range(k):
        a=-pi/2+j*ang
        # polygon with one vertex at centre, edges along a and a+ang
        pts=[(cx,cy)]; x,y=cx,cy; d=a
        for m in range(n-1):
            x+=s*cos(d); y+=s*sin(d); pts.append((x,y)); d+=2*pi/n
        # orient: build counterclockwise from edge direction a
        out+=poly(pts,col,K,1,0.4)
    return out
f3=around(3,6,70,70,45,G)+txt(70,140,'6 × 60° = 360°',size=10)
f3+=around(4,4,215,70,42,B)+txt(215,140,'4 × 90° = 360°',size=10)
f3+=around(6,3,365,70,32,B)+txt(365,140,'3 × 120° = 360°',size=10)
f3+=around(5,3,530,70,40,V)+txt(540,163,'3 × 108° = 324°: gap 36°',size=10)
FIG3=svg(640,172,f3)

# Fig 4: two mirrors at 60 degrees, one bead becomes six
cx,cy,R=120,85,70
f4=''
for k in range(3):
    a=radians(60*k); f4+=f'<line x1="{cx-R*cos(a):.1f}" y1="{cy+R*sin(a):.1f}" x2="{cx+R*cos(a):.1f}" y2="{cy-R*sin(a):.1f}" stroke="{L}" stroke-width="1" stroke-dasharray="3,3"/>'
f4+=f'<line x1="{cx}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{K}" stroke-width="2.5"/><line x1="{cx}" y1="{cy}" x2="{cx+R*cos(radians(60)):.1f}" y2="{cy-R*sin(radians(60)):.1f}" stroke="{K}" stroke-width="2.5"/>'
t=radians(20)
for k in range(3):
    for s in (1,-1):
        a=s*t+radians(120*k); col=G if (k==0 and s==1) else B
        f4+=f'<circle cx="{cx+45*cos(a):.1f}" cy="{cy-45*sin(a):.1f}" r="6" fill="{col}"/>'
f4+=txt(cx,172,'two mirrors at 60° = 180°/3:',size=10)+txt(cx,186,'one bead (gold) makes six',size=10)
# flat mirror triangles
for i,(a,b,lab) in enumerate([(60,60,'60° 60° 60°'),(45,90,'90° 45° 45°'),(60,90,'90° 60° 30°')]):
    p=tri_from_angles(a,b,80); f4+=poly(place(p,290+i*120,120),G,K,1.2,0.35)+txt(330+i*120,140,lab,size=10)
f4+=txt(450,172,'the only three flat triangles whose corners',size=10)+txt(450,186,'are all mirror angles 180°/n',size=10)
FIG4=svg(640,195,f4)

# Fig 5: angle deficit table drawing - faces round a corner, laid flat with the gap
f5=''
cases=[(5,3,'dodecahedron','3 pentagons','36°'),(3,5,'icosahedron','5 triangles','60°'),(4,3,'cube','3 squares','90°'),(3,3,'tetrahedron','3 triangles','180°'),(3,4,'octahedron','4 triangles','120°')]
for i,(n,k,name,faces,gap) in enumerate(cases):
    cx=64+i*128; cy=72
    f5+=around(n,k,cx,cy,30 if n==3 else (26 if n==4 else 22),[V,V,B,G,G][i])+txt(cx,135,name,size=10)+txt(cx,149,faces,size=9.5)+txt(cx,163,'gap '+gap,size=9.5)
FIG5=svg(660,170,f5)

STEPS=[
('1','A place, a path, a turn',
'<p>A <b>point</b> marks a place and has no size. Two points fix exactly one straight <b>line</b> between them. Where two lines meet they make an <b>angle</b>, and an angle is best seen as a turn: a full turn is 360°, half a turn is 180° and makes a straight line, a quarter turn is 90°, the right angle, the corner of a sheet of paper.</p>',
'',
'<b>Place, path, turn.</b> A point is where; a line is between; an angle is how far you turn.',
'Three points not on one line fix a triangle: three places, three paths, three turns.',
'This is the ground floor.',
['How many straight lines pass through two given points?','How many pass through one point?','What angle is a straight line?']),
('2','How many triangles? How many kinds?',
'<p>Any three points not on one line make a triangle, so there are <b>infinitely many triangles</b>. But many of them are the same triangle at a different size. Enlarge a triangle, as a photocopier does, and its angles do not change; triangles with the same angles are <b>similar</b>, the same shape. So the better question is how many <i>shapes</i> there are.</p><p>Cut the three corners off a paper triangle and lay them side by side: they always make a straight line (Figure 2). <b>The angles of every flat triangle add up to 180°</b>, half a turn. So once two angles are chosen the third is fixed, and a triangle\'s shape is given by just two numbers. Those two numbers can be anything that adds up to less than 180°, so there are infinitely many shapes as well; but now they can be laid out, named and compared.</p>',
FIG2+'<figcaption><b>Figure 2.</b> The three corners of any triangle make half a turn.</figcaption>',
'<b>Three corners make one straight line.</b>',
'Two angles fix a shape, so shapes can be sorted into kinds: step 3.',
'The straight line is the half turn of step 1.',
['Can a triangle have two right angles?','Two triangles have angles 50° and 60°. What is the third angle of each, and are they the same shape?','Why does size not matter for shape?']),
('3','The kinds, and five special shapes',
'<p>By their angles, triangles are <b>acute</b> (every angle under 90°), <b>right</b> (one angle exactly 90°) or <b>obtuse</b> (one angle over 90°). By their sides they are <b>equilateral</b> (three equal sides, so three angles of 60°), <b>isosceles</b> (two equal sides and two equal angles) or <b>scalene</b> (all different).</p><p>Five shapes carry this whole book (Figure 1). The <b>equilateral</b> triangle. <b>Half a square</b>, cut along its diagonal: its long side is √2 ≈ 1.414 times its short ones. <b>Half an equilateral triangle</b>, angles 90°, 60°, 30°: its sides are 1, √3 ≈ 1.732 and 2. And two shapes cut from the regular pentagon, whose diagonal is φ ≈ 1.618 times its side, the <b>golden ratio</b> φ = (1 + √5)/2: the <b>golden triangle</b> (36°, 72°, 72°) and the <b>golden gnomon</b> (108°, 36°, 36°). In each, long side to short side is φ.</p>',
FIG1+'<figcaption><b>Figure 1.</b> The five special triangles and the number each one carries.</figcaption>',
'<b>Halve a square, find √2; halve a triangle, find √3; cut a pentagon, find φ.</b>',
'These numbers, 1, √2, √3 and φ, come back at the top of this rung as the numbers of the mirror triangles.',
'Each special shape is one choice of two angles from step 2.',
['Is the half-square triangle isosceles?','Which special triangle has an obtuse angle?','A pentagon has side 1. How long is its diagonal?']),
('4','Round a point: tiling the floor',
'<p>Lay tiles round a point with no gaps and no overlaps, and their angles at the point must add up to a full turn, 360°. <b>Every triangle tiles the floor</b>: two copies make a parallelogram, and parallelograms fill the floor in rows. Regular tiles are pickier. A regular polygon\'s corner is 60° (triangle), 90° (square), 108° (pentagon) or 120° (hexagon). Six triangles, four squares or three hexagons make exactly 360°, but three pentagons make 324° and leave a gap of 36°, and four would overlap (Figure 3).</p>',
FIG3+'<figcaption><b>Figure 3.</b> Only triangles, squares and hexagons close the full turn; pentagons leave a gap.</figcaption>',
'<b>Six, four, three: the floor is complete. The pentagon leaves thirty-six.</b>',
'The gap is not a failure. Close it by folding, and the floor rises into a solid corner: step 6.',
'The full turn of step 1, and the angle sum of step 2 (six triangles of 60°).',
['Why does a regular pentagon not tile the floor?','How many squares meet at a corner of a chessboard?','Does a scalene triangle tile the floor?']),
('5','Mirrors: halve the turn, double the beads',
'<p>One mirror makes one copy. Two mirrors hinged at an angle make many: if the angle is 180°/n, a single bead between them becomes a ring of 2n beads. At 90° you see 4, at 60° you see 6 (Figure 4), at 45° 8, at 36° 10. This is the kaleidoscope. The angle must be 180°/n exactly, or the copies do not close up into a ring.</p><p>Now put three mirrors round a triangle on the floor. The copies tile the floor only if every corner is a mirror angle 180°/n; with the 180° sum of step 2 that leaves exactly three triangles: 60°-60°-60°, 90°-45°-45° and 90°-60°-30°. Three of the special shapes of step 3 are the three flat kaleidoscopes.</p>',
FIG4+'<figcaption><b>Figure 4.</b> Two mirrors make a ring; three mirrors round one of three triangles make a floor.</figcaption>',
'<b>Halve the turn, double the beads.</b> A mirror angle of 180°/n gives 2n copies.',
'Three mirrors meeting in space, like the corner of a box, make not a floor but a whole solid: steps 7 and 8.',
'The full and half turns of step 1; the special triangles of step 3.',
['Two mirrors at 30°: how many beads?','Why must a mirror angle be 180°/n?','Which flat mirror triangle is half an equilateral triangle?']),
('6','Folding the floor: five solids, and no more',
'<p>If the faces round a point add up to <i>less</i> than 360°, the gap can be closed by folding, and the corner rises out of the floor: a solid corner. Exactly 360° stays flat; more cannot fold into a corner that points outwards. With regular faces, at least three at each corner, there are exactly five ways (Figure 5), and each makes one <b>Platonic solid</b>. In DICTO order: the <b>D</b>odecahedron (3 pentagons), the <b>I</b>cosahedron (5 triangles), the <b>C</b>ube (3 squares), the <b>T</b>etrahedron (3 triangles) and the <b>O</b>ctahedron (4 triangles). Euclid closes his <i>Elements</i> with this proof (Book XIII).</p><p>Count the gaps over a whole solid: dodecahedron 20 corners × 36°, icosahedron 12 × 60°, cube 8 × 90°, tetrahedron 4 × 180°, octahedron 6 × 120°. Every one comes to 720°, <b>two full turns</b> (Descartes).</p>',
FIG5+'<figcaption><b>Figure 5.</b> The five corners laid flat, with the gap that folding closes.</figcaption>',
'<b>D·I·C·T·O: Dodeca, Icosa, Cube, Tetra, Octa.</b> And: <b>every solid misses two full turns.</b>',
'Blow a solid up onto a sphere round it; its faces become curved triangles, and the 720° becomes the sphere itself: step 7.',
'The gap of step 4 (the pentagon\'s 36°) is exactly the dodecahedron\'s corner.',
['Why can six triangles not make a solid corner?','Why are there no Platonic solids with hexagon faces?','How many corners has the icosahedron, and what is its gap at each?']),
('7','Triangles on a ball',
'<p>Draw a triangle on a ball with arcs of great circles, the straightest lines on a sphere. Its angles add up to <b>more</b> than 180°, and the extra, the <b>excess</b>, measures its area. Cut an orange into eighths: each piece has three right angles, 270°, an excess of 90°, and 8 × 90° = 720° covers the whole ball. The two full turns of step 6 are the whole sphere, and any set of equal triangles that covers it has excesses adding up to 720°.</p>',
'',
'<b>Flat: three corners make a line. Round: more than a line, and the extra is the area.</b>',
'Now let the triangles on the ball be mirrors: step 8.',
'The 180° of step 2, and the 720° of step 6.',
['A triangle on a ball has angles 90°, 90° and 60°. What is its excess?','How many such triangles cover the ball?','Can a triangle on a ball have three right angles?']),
('8','The triangle of mirrors: the first rung',
'<p>Every Platonic solid has mirror planes through its centre: cut along one and the halves are mirror images. These planes cut the sphere round the solid into small identical triangles, and every one has the angles <b>90°, 60° and 180°/p</b>: p = 3 for the tetrahedron, p = 4 for the cube and octahedron, p = 5 for the dodecahedron and icosahedron. Each is a kaleidoscope of three mirrors (step 5): one point inside it, reflected again and again, makes the corners of a whole solid.</p><p>Its excess is 90° + 60° + 180°/p − 180°. For p = 3 that is 30°, so 720°/30° = <b>24</b> triangles; for p = 4, 15° and <b>48</b>; for p = 5, 6° and <b>120</b>. For p = 6 the excess is 0: the triangle is the flat 90°-60°-30° of steps 3 and 5, and it tiles the floor of close-packed balls instead of the sphere. For p = 7 or more the excess is negative and no triangle closes on a ball. <b>That is why there are three families and five solids.</b></p><p>Each triangle carries one number, 2 cos(180°/p): <b>1</b> for p = 3, <b>√2</b> for p = 4, <b>φ</b> for p = 5, <b>√3</b> for the flat p = 6, the numbers of the special triangles of step 3. Everything golden in this book lives with φ, in the p = 5 triangle. That is the first rung: Chapter 1 of The Golden Ladder, "One Triangle, Three Numbers", begins here.</p>',
'<img src="../book-golden-ladder/figures/ch1-fig1-kaleidoscopes.png" alt="the three spherical kaleidoscopes and the flat one" style="width:100%"><figcaption><b>Figure 6</b> (The Golden Ladder, Figure 1). The mirror triangles of the three families, 24, 48 and 120 on the sphere, and the flat one, p = 6.</figcaption>',
'<b>Three, four, five curl into a ball; six lies flat. One, root two, phi; root three for the floor.</b>',
'Chapter 1 of The Golden Ladder: where a point sits in this triangle decides the solid, and the golden cuts are points on its sides.',
'Its corners are the mirror pairs of step 5 (90°, 60°, 180°/p); its excess is the area of step 7; its three families are the five solids of step 6.',
['What are the angles of the cube\'s mirror triangle?','Why is there no mirror triangle with p = 7 on the sphere?','Which number belongs to the dodecahedron\'s triangle?']),
]
ANS=[['One.','Infinitely many.','180°, half a turn.'],
['No: two right angles already make 180°, leaving nothing for the third.','70° for both; yes, the same shape (similar).','Enlarging changes the sides but not the angles, and the angles fix the shape.'],
['Yes: two equal sides, and angles 45° and 45°.','The golden gnomon (108°).','φ ≈ 1.618.'],
['108° does not divide 360°: three leave 36°, four overlap by 72°.','Four.','Yes: every triangle tiles the floor.'],
['12 (30° = 180°/6, so 2 × 6).','Otherwise the copies do not close up into a ring.','90°-60°-30°.'],
['Six times 60° is 360°: the corner stays flat.','Three hexagons already make 360°: flat, no gap to fold.','12 corners, a gap of 60° at each (12 × 60° = 720°).'],
['60° (240° − 180°).','720°/60° = 12.','Yes: the orange eighth, 90°-90°-90°.'],
['90°, 60°, 45°.','90° + 60° + 180°/7 is less than 180°: the excess is negative.','φ, the golden ratio.']]

body=''
for (n,title,text,fig,mn,up,down,qs) in STEPS:
    body+=f'<h2>Step {n} · {title}</h2>{text}'
    if fig: body+=f'<figure>{fig}</figure>'
    body+=f'<div class="mn"><p><span class="tag">Mnemonic</span> {mn}</p><p><span class="tag up">Bridge up ↑</span> {up}</p><p><span class="tag dn">Bridge down ↓</span> {down}</p></div>'
    body+='<p class="q"><b>Questions.</b> '+' '.join(f'({chr(97+i)}) {q}' for i,q in enumerate(qs))+'</p>'
rows=''.join(f'<tr><td>{n}</td><td>{t}</td><td>{m}</td></tr>' for (n,t,_,_,m,_,_,_) in STEPS)
ans=''.join(f'<p class="small"><b>Step {i+1}.</b> '+' '.join(f'({chr(97+j)}) {a}' for j,a in enumerate(A))+'</p>' for i,A in enumerate(ANS))
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Golden Ladder, Rung 0</title>
<link rel="stylesheet" href="../paper.css">
<style>figure{{margin:3mm 0}} figcaption{{font-size:8.6pt}} p.small{{font-size:8.6pt}}
.mn{{border-left:3px solid {G};background:#fbf7ec;padding:1.5mm 3mm;margin:2.5mm 0;break-inside:avoid}} .mn p{{margin:1mm 0}}
.tag{{display:inline-block;font:bold 7.5pt "DejaVu Sans",sans-serif;color:#fff;background:{G};border-radius:1mm;padding:0.3mm 1.5mm;margin-right:1.5mm}} .tag.up{{background:{B}}} .tag.dn{{background:{V}}}
p.q{{font-size:9pt}} h2{{break-after:avoid}}
table.t{{border-collapse:collapse;font-size:9pt;margin:3mm 0;width:100%}} table.t td,table.t th{{border-bottom:1px solid #ccc;padding:1.1mm 1.8mm;text-align:left;vertical-align:top}}</style></head>
<body>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>The Golden Ladder · Rung 0<br><span style="font-size:0.72em;font-weight:normal">From a Point to the Triangle of Mirrors</span></h1>
<div class="meta"><b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com<br>
A study companion to The Golden Ladder (DICTO DOI: 10.5281/zenodo.23966554) · Sample lesson · 8 November 2026<br>
DICTO proposed a ladder of lessons with mnemonics as bridges between the steps, to be climbed upwards and downwards. Drafting with Claude (Anthropic).</div>
<div class="status">Draft for DICTO's reading: a sample of the format, not a record. If the format works, the same pattern continues rung by rung through the book, with each step's place in the Concordance added.</div>

<p class="hook">The Golden Ladder starts at one small triangle of mirrors. Why there, and why should anyone see that as a first step? This lesson climbs to it from nothing: from a point, through the kinds of triangle, the floor, the mirror and the fold, to the ball and its three mirror triangles. Every step has a mnemonic, a bridge to the step above and a bridge to the step below, so the ladder can be climbed both ways.</p>

<h2>How to use this lesson</h2>
<p>Read one step at a time. Say the mnemonic aloud, then cover the page and say the bridges in your own words: up, what this step makes possible; down, what it rests on. Answer the questions before turning to the answers at the end. Coming down, read the steps in reverse and use only the downward bridges.</p>
{body}
<h2>The rung at a glance</h2>
<table class="t"><tr><th>Step</th><th>Idea</th><th>Mnemonic</th></tr>{rows}</table>
<h2>Answers</h2>{ans}
<p class="small"><b>Sources.</b> Euclid, <i>Elements</i>, Book XIII (the five solids, and the dodecahedron as a cube with roofs); Descartes' theorem on the total angle deficit, 720°; Girard's theorem (a spherical triangle's area is its excess); H. S. M. Coxeter, <i>Regular Polytopes</i> (the mirror triangles, Wythoff's construction); The Golden Ladder, Chapter 1.</p>
</body></html>'''
open('/home/dicto/k-research/papers/ladder-study/paper.html','w').write(html)
print('written',len(html))
