# Figure: the icosahedron (edge 1) stretched one edge-length along four directions, and with three and four caps.
# Triangles blue (the icosahedron's own), rhombi lilac, pentagons violet, hexagons gold-yellow; gold edges.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mixes3 as M, pieces_figure as PF
exec(open('ring1.py').read().split("fmt=lambda")[0])
V0=SOL['icosahedron']
src=open('swept_dodeca.py').read(); head=src[:src.index("views=")]
head=head.replace("allT=T5+T4+T3; cols=[(138,92,196)]*len(T5)+[(196,170,232)]*len(T4)+[(232,200,82)]*len(T3)   # triangles gold-yellow",
 "T6=[t for f in F if len(f)==6 for t in PF.tri([f])]\n    allT=T5+T4+T3+T6; cols=[(138,92,196)]*len(T5)+[(196,170,232)]*len(T4)+[(70,118,210)]*len(T3)+[(232,200,82)]*len(T6)")
cases=[('five-fold axis: 20 triangles + 10 rhombi',[(0,0,0),(0,1,phi)]),('face diagonal: 16 triangles, 2 rhombi, 4 pentagons',[(0,0,0),(1,1,0)]),
       ('body diagonal: 20 triangles + 6 rhombi',[(0,0,0),(1,1,1)]),('cube axis: 16 triangles, 4 rhombi, 2 squares',[(0,0,0),(1,0,0)]),
       ('three caps: 15 tri, 3 rhombi, 3 pent, 2 hex',None),('four caps: 16 triangles, 6 rhombi, 4 hexagons',None)]
px=520; fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
sheet=Image.new('RGB',(3*px,2*(px+44)),PF.GROUND); d=ImageDraw.Draw(sheet)
R=PF.rot((1,0,0),-0.95)@PF.rot((0,0,1),0.35)
for k,(name,pts) in enumerate(cases):
    if pts is None:
        P=[np.array(p,float)/2**.5 for p in ([(0,0,0),(1,1,0),(1,0,1)] if k==4 else [(0,0,0),(1,1,0),(1,0,1),(0,1,1)])]
    else:
        u=np.array(pts[1],float); u/=np.linalg.norm(u); P=[np.zeros(3),u]
    expr="np.vstack(["+",".join(f"V0+np.array({list(p)})" for p in P)+"])"
    g={'V0':V0}; exec(head.replace("import mixes3 as M, pieces_figure as PF","import mixes3 as M, pieces_figure as PF").replace("V=np.vstack([M.DOD, M.DOD+np.array([phi,phi,0])])","V="+expr).replace("scale=px*0.15","scale=px*0.22"),g)
    x,y=(k%3)*px,(k//3)*(px+44); sheet.paste(g['draw'](R,px),(x,y)); d.text((x+px/2,y+px+8),name,font=fnt,fill=(233,224,208),anchor='mt')
sheet.save('icosahedron-family.png'); print('ok')
