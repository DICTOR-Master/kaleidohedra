from PIL import Image, ImageDraw, ImageFont
R='/home/dicto/k-research/studies/2026-11-24-vacuus-build-renders/renders/'
P=Image.open('/home/dicto/k-research/studies/2026-11-25-slot-assemblies/renders/PREVIEW-slot-assemblies-1-dicto-construction.png').convert('RGB')
sx=P.width/1320; sy=P.height/1580
crop=lambda x0,y0,x1,y1: P.crop((int(x0*sx),int(y0*sy),int(x1*sx),int(y1*sy)))
tiles=[(crop(60,185,640,770),'Octahedral form, assembled'),(crop(60,800,640,1390),'Octahedral form: pieces A, B, C1, C2'),
       (crop(690,185,1290,770),'Cubic form (Resonus squares), assembled'),(crop(690,800,1290,1390),'Cubic form: pieces A, B, C1, C2'),
       (Image.open(R+'cube-b1nr-rings.jpg'),'Cube: 108 rings, 9 per fin, open centre'),(Image.open(R+'cube-b1nr-rings-fin.jpg'),'One fin: 9 rounded-triangle rings'),
       (Image.open(R+'cuboctahedron-ring-fins.jpg'),'Cuboctahedron: 24 rings, one per fin'),(Image.open(R+'cuboctahedron-ring-fins-axis3.jpg'),'Down a three-fold axis'),
       (Image.open(R+'cuboctahedron-ring-fins-pulled.jpg'),'Its four hexagon plates pulled apart'),
       (Image.open(R+'dodecahedron-ring-fins.jpg'),'Dodecahedron: 30 rings, one per fin'),(Image.open(R+'dodecahedron-ring-fins-axis5.jpg'),'Down a five-fold axis')]
W,H=2480,3508; BG=(20,22,28); M=90
S=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(S)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f1,f2,f3,f4=ImageFont.truetype(FB,58),ImageFont.truetype(FB,38),ImageFont.truetype(FN,30),ImageFont.truetype(FN,28)
d.text((M,70),"DICTO's Vacuus builds: exact renders",font=f1,fill=(232,226,214))
d.text((M,150),"Every corner exact; nothing fitted to a photo. Card models: 80 mm cards, 1.5 mm slots. Rings: PET-bottle security rings.",font=f4,fill=(190,186,176))
sections=[('1  Slotted card models (four pieces; proved to assemble, both forms)',[0,1,2,3]),
          ('2  B1NR cube Vacuus: rings folded into rounded triangles (no hull)',[4,5]),
          ('3  B1NR cuboctahedron Vacuus: bottle rings in the fins (no hull)',[6,7,8]),
          ('4  B1NR dodecahedron Vacuus: bottle rings in the fins (no hull)',[9,10])]
# layout: section 1 in 2 rows of 2? use 4 columns for row 1, 3 columns elsewhere
y=230
for head,idx in sections:
    d.text((M,y),head,font=f2,fill=(224,184,74)); y+=62
    n=4 if len(idx)==4 else 3
    T=min((W-2*M-(n-1)*30)//n, 680)
    k=len(idx); x0=(W-(k*T+(k-1)*30))//2
    for c,i in enumerate(idx):
        im,cap=tiles[i]; im=im.convert('RGB')
        from PIL import ImageChops
        bb=ImageChops.difference(im,Image.new('RGB',im.size,im.getpixel((2,2)))).point(lambda v:255 if v>18 else 0).getbbox()
        if bb: m=12; im=im.crop((max(bb[0]-m,0),max(bb[1]-m,0),min(bb[2]+m,im.width),min(bb[3]+m,im.height)))
        r=min(T/im.width,T/im.height); im=im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
        x=x0+c*(T+30); S.paste(im,(x+(T-im.width)//2,y+(T-im.height)//2))
        d.text((x+T//2,y+T+12),cap,font=f3 if n==3 else f4,fill=(205,205,210),anchor='ma')
    y+=T+80
d.text((W-M,H-60),'DICTO · dictospheres.com',font=f3,fill=(224,184,74),anchor='ra')
print('used height',y,'of',H)
S.save('/home/dicto/Documents/papers-to-read/VACUUS-BUILD-RENDERS-2026-11-25.pdf','PDF',resolution=300)
S.resize((620,877)).save('/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/d4219d89-8c65-4da0-9f1b-e8400fa445e8/scratchpad/onepage.jpg')
