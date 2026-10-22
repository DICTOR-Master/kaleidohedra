# DICTO 10-22: in the dodecahedron layer, "two partially rotated dodecas and the hourglass space between them;
# the profile of an elongated hexagon". Two dodecahedra on cubes that share an edge (cells (0,0,0) and (1,1,0) of the
# cubic lattice of edge phi), and the space between them that is not dodecahedron: the parts of the two Dogstars on
# the cells (1,0,0) and (0,1,0) next to both (each Dogstar = cube minus six roofs). Drawn: dodecahedra violet,
# the two Dogstars as glass. Three views: along the shared cube edge (z), side on (along x+y), and oblique.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mixes3 as M
import pieces_figure as PF
phi=M.phi; h=phi/2
def faces_of(V): return PF.tri(PF.hull_faces(V))
cell=lambda i,j,k: np.array([i*phi,j*phi,k*phi])
dodecs=[PF.orient(faces_of(M.DOD+cell(0,0,0))), PF.orient(faces_of(M.DOD+cell(1,1,0)))]
S=[PF.orient([t+cell(1,0,0) for t in PF.PIECES[4][2]]), PF.orient([t+cell(0,1,0) for t in PF.PIECES[4][2]])]
def view(Rv,px=640):
    PF.Rv=Rv
    allT=[t for T in dodecs+S for t in T]; c=np.mean(np.vstack(allT),0)
    scale=px*0.17
    def lay(T,col):
        T2=[t-c for t in T]
        return PF.render(T2,col,px,scale)
    base=lay([t for T in dodecs for t in T],(138,92,196))
    glass=lay([t for T in S for t in T],(150,200,230))
    a=np.array(base).astype(float); g=np.array(glass).astype(float); bg=np.array(PF.GROUND,float)
    gm=np.any(np.abs(g-bg)>3,axis=2); dm=np.any(np.abs(a-bg)>3,axis=2)
    out=a.copy(); out[gm&~dm]=g[gm&~dm]*0.75+bg*0.25          # glass where no dodecahedron
    out[gm&dm]=a[gm&dm]*0.72+g[gm&dm]*0.28                    # glass over dodecahedra: a tint
    return Image.fromarray(out.astype(np.uint8))
V=[('along the shared edge',PF.rot((1,0,0),0)),('side on',PF.rot((1,0,0),-math.pi/2)@PF.rot((0,0,1),math.pi/4)),('oblique',PF.rot((1,0,0),-0.9)@PF.rot((0,0,1),0.5))]
px=640; f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26)
sheet=Image.new('RGB',(3*px,px+60),PF.GROUND); d=ImageDraw.Draw(sheet)
for i,(name,R) in enumerate(V):
    sheet.paste(view(R,px),(i*px,0)); d.text((i*px+px/2,px+12),name,font=f,fill=(233,224,208),anchor='mt')
sheet.save('hourglass.png'); print('ok')
