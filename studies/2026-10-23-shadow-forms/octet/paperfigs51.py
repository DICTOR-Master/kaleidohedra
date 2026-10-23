# Figures for paper #51 The Delian Bond (white background, true faces, small DICTO mark).
import os
os.chdir('/home/dicto/shadow-fusions'); src=open('fuse4.py').read(); exec(src.split("res=json.load")[0]); os.chdir('octet')
exec(open('octet1.py').read().split('ts=[')[0])
exec(open('/home/dicto/shadow-fusions/solidraw.py').read())
COL.update({'samson':(205,150,60),'delilah':(80,135,190),'tet':(205,150,60),'oct':(80,135,190),'cone':(150,150,150)})
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
OUT='/home/dicto/k-research/papers/2026-10-24-delian-bond/figures'; W=(255,255,255)
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((64,64))
def sheet(panels,SZ,fn,labels=None,rows=1):
    cols=(len(panels)+rows-1)//rows; im=Image.new('RGB',(cols*SZ,rows*SZ+(40 if labels else 0)*rows),W); d=ImageDraw.Draw(im)
    for i,(ps,R) in enumerate(panels):
        x=(i%cols)*SZ; y=(i//cols)*(SZ+(40 if labels else 0))
        if ps: im.paste(draw_solids(ps,SZ,R,COL,L,W),(x,y))
        if labels and labels[i]: d.text((x+SZ//2-int(d.textlength(labels[i],font=F(22,True)))//2,y+SZ+6),labels[i],font=F(22,True),fill=(43,38,32))
    im.paste(logo,(im.width-72,6),logo); im.save(os.path.join(OUT,fn)); print(fn,im.size)
tD=1-(2/3)*2**(-1/3); Sm=cell('T',Tc[0],tD); Dl=cell('O',O[0],tD)
R1,R2=rot(0.6,0.45),rot(0.6+np.pi,-0.45)
sheet([([{'name':'samson','V':Sm}],R1),([{'name':'samson','V':Sm}],R2),([{'name':'delilah','V':Dl}],R1),([{'name':'samson','V':Sm},{'name':'delilah','V':Dl}],rot(0.3,0.35))],600,'fig1-samson-delilah.png')
ts=[(0.03,'t ≈ 0'),(1/(3+2*6**.5),'equilateral'),(1/3,'t = 1/3 octet'),(tD,'Delian bond'),(1-2*(2**.5-1)/3,'equilateral'),(0.97,'t ≈ 1')]
panels=[];labels=[]
for t,lab in ts:
    panels.append(([{'name':'tet','V':cell('T',Tc[0],t)}],R1)); labels.append(lab)
for t,lab in ts:
    panels.append(([{'name':'oct','V':cell('O',O[0],t)}],R1)); labels.append('')
sheet(panels,340,'fig2-family.png',labels=labels,rows=2)
# the double cone over one shared face, cut at t (tetra side gold, octa side blue)
c_T=Tc[0]; c_O=np.array(O[0],float)
face=np.array([v for v in [(0,0,0),(1,1,0),(1,0,1),(0,1,1)] if np.linalg.norm(np.array(v)-c_O)<1.01],float)
assert len(face)==3, face
fc=face.mean(0); t=0.55; m=c_T+t*(c_O-c_T)
cutT=np.array([c_T+(f-c_T)*(t*np.linalg.norm(c_O-c_T)/np.linalg.norm(fc-c_T)) if False else None for f in face]) if False else None
# points where the cut plane meets the edges c_T->face corners or c_O->face corners
n=(c_O-c_T)/np.linalg.norm(c_O-c_T)
def cutpts(apex):
    out=[]
    for f in face:
        s=((m-apex)@n)/((f-apex)@n)
        if 0<=s<=1: out.append(apex+s*(f-apex))
    return np.array(out)
pT=cutpts(c_T); pO=cutpts(c_O)
lowT=np.vstack([[c_T],pT]) if len(pT)==3 else np.vstack([[c_T],face])
partT=np.vstack([[c_T],face]) if len(pT)<3 else lowT
up=np.vstack([face,pT]) if len(pT)==3 else None
pieces=[]
if len(pT)==3: pieces=[{'name':'tet','V':np.vstack([[c_T],pT])},{'name':'oct','V':np.vstack([pT,face,[c_O]])}]
else: pieces=[{'name':'tet','V':np.vstack([[c_T],face,pO])},{'name':'oct','V':np.vstack([pO,[c_O]])}]
whole=[{'name':'cone','V':np.vstack([[c_T],face,[c_O]])}]
u0=np.cross(n,[0,0,1.]); u0/=np.linalg.norm(u0); v0=np.cross(n,u0)
Rs=np.array([n,v0,u0]); tilt=rot(0,0.35)@rot(0.25,0); Rs=tilt@Rs
sheet([(whole,Rs),(pieces,Rs),([dict(p,V=p['V']+(0.22 if p['name']=='oct' else -0.22)*n) for p in pieces],Rs)],560,'fig3-double-cone.png')
# Figure 4: the Delian bond filling space around one lattice cube (Samsons gold, Delilahs blue)
patch=[]
for p in Tc:
    patch.append({'name':'samson','V':cell('T',np.array(p,float),tD)})
for p in O:
    patch.append({'name':'delilah','V':cell('O',np.array(p,float),tD)})
sheet([(patch,rot(0.5,0.55)),(patch,rot(2.0,-0.4))],760,'fig4-delian-fill.png')
