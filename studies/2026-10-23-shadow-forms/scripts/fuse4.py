# Shadow forms, step 4: a picture sheet of the chunky fusions (fuse3), each drawn twice: pieces coloured by kind, and from a second side.
import numpy as np, json, itertools
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
src=open('fuse3.py').read(); exec(src.split('out={}')[0])
COL={'icosahedron':(76,175,80),'Lotus Jewel':(46,125,50),'dodecahedron':(230,180,60),'Unborn':(240,140,50),'Tricap':(160,110,220),'AXE':(40,190,210)}
def tris(p):
    V=p['V']
    if p['name']=='Lotus Jewel':
        T=[]; c=V.mean(0)
        for f in JF:
            for k in range(1,len(f)-1): T.append([f[0],f[k],f[k+1]])
        return V,T
    hl=ConvexHull(V); return V,hl.simplices.tolist()
def rot(a,b):
    ca,sa,cb,sb=np.cos(a),np.sin(a),np.cos(b),np.sin(b)
    return np.array([[1,0,0],[0,cb,-sb],[0,sb,cb]])@np.array([[ca,0,sa],[0,1,0],[-sa,0,ca]])
L=np.array([0.4,0.7,0.6]); L/=np.linalg.norm(L)
def draw(ps,size,R):
    im=Image.new('RGB',(size,size),(244,241,234)); d=ImageDraw.Draw(im)
    allV=np.vstack([p['V'] for p in ps]); c=allV.mean(0); r=np.max(np.linalg.norm(allV-c,axis=1))
    polys=[]
    for p in ps:
        V,T=tris(p); W=(V-c)@R.T
        for t in T:
            P=W[t]; n=np.cross(P[1]-P[0],P[2]-P[0]); nn=np.linalg.norm(n)
            if nn<1e-12: continue
            n/=nn
            # outward: away from the piece centre
            if n@(P.mean(0)-(p['V'].mean(0)-c)@R.T)<0: n=-n
            if n[2]<=0: continue
            sh=0.45+0.55*max(0,n@L); col=tuple(int(x*sh) for x in COL[p['name']])
            pts=[(size/2+P[k,0]/r*size*0.42, size/2-P[k,1]/r*size*0.42) for k in range(3)]
            polys.append((P[:,2].mean(),pts,col))
    for z,pts,col in sorted(polys,key=lambda x:x[0]): d.polygon(pts,fill=col,outline=tuple(max(0,x-50) for x in col))
    return im
res=json.load(open('fuse3-results.json'))
picks=[r for r in res if r['fill']>=0.85 and r['elong']<=1.8]
# regenerate each pick's cluster geometry
geo=[]
for kind in ['icoUnborn','jewelDodeca','four']:
    P=net(kind); C=np.array([p['V'].mean(0) for p in P])
    mid=[i for i in range(len(P)) if np.linalg.norm(C[i]-np.array([h,h,h]))<1.5]
    near=lambda i,j:np.linalg.norm(C[i]-C[j])<2.3
    adj={}
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            if near(i,j) and (touch(P[i],P[j]) or touch(P[j],P[i])): adj.setdefault(i,set()).add(j); adj.setdefault(j,set()).add(i)
    seen=set()
    for i in mid:
        for j in adj.get(i,()):
            for cl in [frozenset((i,j))]+[frozenset((i,j,k)) for k in (adj[i]|adj[j])-{i,j}]:
                ps=[P[x] for x in cl]; fill,el,hv,vol=chunk(ps); names=tuple(sorted(p['name'] for p in ps))
                s=(kind,names,round(vol,5),round(hv,5))
                if s in seen: continue
                for r in picks:
                    if (r['network'],tuple(r['pieces']),round(r['vol'],5),round(r['hull'],5))==s: seen.add(s); geo.append((r,ps))
F=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if n>30 else '')+'.ttf',n if n<=30 else n-10)
NET={'icoUnborn':'Icosahedra and Unborn','jewelDodeca':'Lotus Jewel network','four':'Jewel | Tricap | Unborn | AXE'}
S=420; cols=4; rows=(len(geo)+cols-1)//cols; W=cols*S*2//1; sheet=Image.new('RGB',(cols*(2*S//2*2)+80, rows*(S+120)+200),(244,241,234))
d=ImageDraw.Draw(sheet); d.text((40,30),'Shadow forms: chunky fusions in the simple cubic icosahedron networks',font=F(44),fill=(43,38,32))
d.text((40,90),'Face-sharing clusters of 2-3 pieces; fill = pieces / convex hull; colours: icosahedron green, Lotus Jewel dark green, dodecahedron gold, Unborn orange, Tricap purple, AXE cyan',font=F(20),fill=(109,101,86))
for k,(r,ps) in enumerate(sorted(geo,key=lambda g:-g[0]['fill'])):
    x=40+(k%cols)*(2*S//2*2)//cols*1; x=40+(k%cols)*((sheet.width-80)//cols); y=150+(k//cols)*(S+120)
    im=draw(ps,S,rot(0.6,0.45)); sheet.paste(im,(x,y))
    t=' + '.join(r['pieces']); d.text((x+8,y+S+6),t,font=F(20),fill=(43,38,32))
    d.text((x+8,y+S+34),'%s · fill %.1f%% · vol %.4f'%(NET[r['network']],100*r['fill'],r['vol']),font=F(17),fill=(109,101,86))
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((140,140)); sheet.paste(logo,(sheet.width-180,20),logo)
d.text((sheet.width-330,sheet.height-40),'DICTO · dictospheres.com',font=F(20),fill=(109,101,86))
sheet.save('/home/dicto/Documents/papers-to-read/shadow-fusions-chunky.png'); print(len(geo),'drawn',sheet.size)
