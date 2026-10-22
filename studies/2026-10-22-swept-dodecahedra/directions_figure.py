# Figure for #49: the dodecahedron (edge 1) swept one edge-length along four directions, oblique view.
# Faces: pentagons violet, rhombi/rectangles lilac, hexagons and heptagons blue, triangles gold.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mixes3 as M, pieces_figure as PF
phi=M.phi
src=open('swept_dodeca.py').read(); head=src[:src.index("views=")]
head=head.replace("allT=T5+T4+T3; cols=[(138,92,196)]*len(T5)+[(196,170,232)]*len(T4)+[(232,200,82)]*len(T3)   # triangles gold-yellow",
 "T67=[t for f in F if len(f) in (6,7) for t in PF.tri([f])]\n    allT=T5+T4+T3+T67; cols=[(138,92,196)]*len(T5)+[(196,170,232)]*len(T4)+[(232,200,82)]*len(T3)+[(110,160,225)]*len(T67)")
dirs=[('cube axis: DICTO\'s F11 (shown at 2/φ, squares)',(1,0,0),2/phi),('face diagonal: 12 pentagons + 10 rhombi',(1,1,0),1.0),('body diagonal: 12 pentagons + 12 rhombi',(1,1,1),1.0),('five-fold axis: 12 pentagons + 10 equal rhombi',(1,0,phi),1.0),('along two faces: 10 pentagons, 6 rhombi, 2 heptagons',(0,1,phi),1.0)]
px=600; fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
sheet=Image.new('RGB',(3*px,2*(px+50)),PF.GROUND); d=ImageDraw.Draw(sheet)
R=PF.rot((1,0,0),-0.95)@PF.rot((0,0,1),0.35)
for k,(name,u,s) in enumerate(dirs):
    u=np.array(u,float); u/=np.linalg.norm(u)
    g={}; exec(head.replace("V=np.vstack([M.DOD, M.DOD+np.array([phi,phi,0])])",f"V=np.vstack([M.DOD, M.DOD+{s}*np.array({list(u)})])").replace("scale=px*0.15","scale=px*0.2"),g)
    x,y=(k%3)*px,(k//3)*(px+50); sheet.paste(g['draw'](R,px),(x,y)); d.text((x+px/2,y+px+10),name,font=fnt,fill=(233,224,208),anchor='mt')
sheet.save('directions.png'); print('ok')
