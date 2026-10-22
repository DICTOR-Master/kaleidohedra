# Diagram for everyone: the layer cake. Each solid's own way of filling space becomes a layer with flat top and
# bottom; pick the layers your mix needs, stack them, repeat the stack.
from PIL import Image, ImageDraw, ImageFont
W,H=1800,1250; GROUND=(20,15,11); GOLD=(222,178,80); INK=(233,224,208); MUTED=(170,160,145)
img=Image.new('RGB',(W,H),GROUND); d=ImageDraw.Draw(img)
B=lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n)
R=lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
d.text((60,40),'How every mix fills space: a layer cake',font=B(54),fill=GOLD)
d.text((60,115),'Each solid has its own way to fill space. Make each into a layer with a flat top and bottom,',font=R(34),fill=INK)
d.text((60,160),'pick the layers your mix needs, stack them, and repeat the stack upward and downward for ever.',font=R(34),fill=INK)
layers=[  # top to bottom
 ((58,112,205),'ICOSAHEDRON layer','each icosahedron wrapped in 6 Admiral Caps (A) makes a bigger octahedron;','big octahedra + big quarter tetrahedra (Q′) fill the layer'),
 ((205,62,40),'TETRAHEDRON + OCTAHEDRON layer','the classical octet; cut flat, it leaves half octahedra (P) on top and bottom;','a solid not in your mix is cut up: octahedron = 2 P, tetrahedron = 4 Q'),
 ((72,142,72),'CUBE layer','just cubes',''),
 ((138,92,196),'DODECAHEDRON layer','dodecahedra (Euclid: a cube with 6 roofs) + Dogstars (S) between them;','at top and bottom, X (cube minus a roof) and Y (cube plus a roof) make it flat'),
]
x0,x1=60,1130; y=250; hgt=200
for col,title,l1,l2 in layers:
    d.rectangle([x0,y,x1,y+hgt],fill=tuple(int(c*0.55) for c in col),outline=GOLD,width=4)
    d.rectangle([x0,y,x0+26,y+hgt],fill=col)
    d.text((x0+50,y+22),title,font=B(36),fill=(255,248,232))
    d.text((x0+50,y+82),l1,font=R(24),fill=INK)
    if l2: d.text((x0+50,y+120),l2,font=R(24),fill=INK)
    y+=hgt+22
# flat seams note and repeat arrow
ax=1200
d.line([(ax,260),(ax,y-30)],fill=GOLD,width=6); d.polygon([(ax-20,280),(ax+20,280),(ax,240)],fill=GOLD); d.polygon([(ax-20,y-50),(ax+20,y-50),(ax,y-10)],fill=GOLD)
d.text((ax+40,300),'repeat the stack',font=B(32),fill=GOLD)
d.text((ax+40,345),'upward and downward',font=R(28),fill=INK)
d.text((ax+40,470),'Every layer has flat faces,',font=R(28),fill=INK)
d.text((ax+40,510),'so any layers sit on any others:',font=R(28),fill=INK)
d.text((ax+40,550),'faces need not match.',font=R(28),fill=INK)
d.text((ax+40,680),'Your mix, for example',font=B(30),fill=GOLD)
d.text((ax+40,725),'cube + icosahedron:',font=R(28),fill=INK)
d.text((ax+40,765),'use just the CUBE layer',font=R(28),fill=INK)
d.text((ax+40,805),'and the ICOSAHEDRON layer.',font=R(28),fill=INK)
d.text((ax+40,930),'All 31 mixes work,',font=B(30),fill=GOLD)
d.text((ax+40,975),'with only 7 helper pieces:',font=R(28),fill=INK)
d.text((ax+40,1015),'P, Q, Q′, A, S, X, Y',font=B(30),fill=INK)
img.save('layer-cake.png'); print('ok')
