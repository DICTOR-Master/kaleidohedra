# Figure: the seven connectors, each from its own faces (closed surfaces, volumes checked against Table 1),
# drawn with a depth buffer so the non-convex pieces (cap, Dogstar, X) show correctly. All at one scale.
import math, itertools, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
import mixes3 as M
phi=M.phi; s=2**-0.5; L=phi**2/2**.5; h=phi/2
def hull_faces(V):
    V=np.asarray(V,float); H=ConvexHull(V); F={}
    for simp,eq in zip(H.simplices,H.equations): F.setdefault(tuple(np.round(eq,6)),set()).update(simp)
    out=[]
    for eq,idx in F.items():
        n=np.array(eq[:3]); idx=list(idx); c=V[idx].mean(0); u=V[idx[0]]-c; w=np.cross(n,u)
        idx.sort(key=lambda i: math.atan2((V[i]-c)@w,(V[i]-c)@u)); out.append([V[i] for i in idx])
    return out
def tri(polys):
    T=[]
    for p in polys:
        for k in range(1,len(p)-1): T.append(np.array([p[0],p[k],p[k+1]]))
    return T
def orient(T):
    # make the triangles of a closed surface consistently oriented (neighbours traverse a shared edge in opposite
    # directions), outward (positive volume)
    key=lambda p: tuple(np.round(p,7))
    T=[t.copy() for t in T]; done=[False]*len(T); edges={}
    for i,t in enumerate(T):
        for a in range(3): edges.setdefault(frozenset((key(t[a]),key(t[(a+1)%3]))),[]).append(i)
    for st in range(len(T)):
        if done[st]: continue
        done[st]=True; stack=[st]
        while stack:
            i=stack.pop(); t=T[i]
            for a in range(3):
                e=(key(t[a]),key(t[(a+1)%3]))
                for j in edges[frozenset(e)]:
                    if j==i or done[j]: continue
                    u=T[j]; dirs=[(key(u[b]),key(u[(b+1)%3])) for b in range(3)]
                    if e in dirs: T[j]=u[::-1].copy()
                    done[j]=True; stack.append(j)
    v=sum(np.dot(t[0],np.cross(t[1],t[2])) for t in T)/6
    return T if v>0 else [t[::-1].copy() for t in T]
def volume(T): return sum(np.dot(t[0],np.cross(t[1],t[2])) for t in T)/6
OCT1=np.vstack([np.eye(3),-np.eye(3)])*s
P=tri(hull_faces(np.vstack([OCT1[:4],OCT1[4:5]])))   # half octahedron: equator + apex
T1=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/(2*2**.5)
Q=tri(hull_faces(np.vstack([T1[:3],[[0,0,0]]])))
Qp=[t*L for t in Q]
# Admiral Cap round the octahedron corner (phi^2/2,0,0): 4 corner triangles of the octahedron faces + its free icosahedron faces
ICO=np.array([p for a in (1,-1) for b in (phi,-phi) for p in [(0,a,b),(a,b,0),(b,0,a)]])/2
OCT=np.vstack([np.eye(3),-np.eye(3)])*phi**2/2; V0=OCT[0]
icof=hull_faces(ICO)
onoct=lambda f: abs(np.abs(np.mean(f,0)).sum()*0+ (np.abs(f).sum(1)).std())<1e-9 and np.allclose(np.abs(f).sum(1),phi**2/2) and len({tuple(np.sign(np.round(v,9))) for v in f})>=1 and all(np.allclose(np.sign(f[0][np.abs(f[0])>1e-9]),np.sign(v[np.abs(v)>1e-9])) or True for v in f)
cap=[]
for sx in (1,): 
    for sy,sz in itertools.product((1,-1),(1,-1)):
        n=np.array([sx,sy,sz]); corner=V0
        on=[v for v in ICO if abs(v@n-phi**2/2)<1e-9]            # icosahedron corners on this octahedron face
        near=sorted(on,key=lambda v:np.linalg.norm(v-corner))[:2]
        cap.append([corner]+near)
free=[f for f in icof if not any(abs(np.mean(f,0)@np.array(sg)-phi**2/2*1)<1e-6 for sg in itertools.product((1,-1),repeat=3))]
# free faces: centroid not on any octahedron face plane; keep those nearest this corner
fc=[(np.linalg.norm(np.mean(f,0)/np.linalg.norm(np.mean(f,0))-V0/np.linalg.norm(V0)),f) for f in free]
fc.sort(key=lambda t:t[0]); A=tri(cap+[f for _,f in fc[:2]])
# Euclid's roof on the top face of the cube of edge phi, and the inward copy
roof_up=M.ROOF[(2,1)]; roof_in=roof_up*np.array([1,1,-1])+np.array([0,0,phi])   # reflected into the cube
def roof_sides(R,top_z):
    base=[v for v in R if abs(v[2]-top_z)<1e-9]; return [f for f in hull_faces(R) if not all(abs(v[2]-top_z)<1e-9 for v in f)]
cube=hull_faces(M.CUBE)
def cube_without(axis_faces):
    return [f for f in cube if not any(all(abs(v[a]-sg*h)<1e-9 for v in f) for a,sg in axis_faces)]
Y=tri(cube_without([(2,1)])+roof_sides(roof_up,h))
X=tri(cube_without([(2,1)])+roof_sides(roof_in,h))
# Dogstar: six inward roofs, one on each face
S=[]
for a,sg in [(0,1),(0,-1),(1,1),(1,-1),(2,1),(2,-1)]:
    R=M.ROOF[(a,sg)].copy(); R[:,a]=2*sg*h-R[:,a]                # reflect the outward roof into the cube
    S+=roof_sides(R,sg*h) if a==2 else [f for f in hull_faces(R) if not all(abs(v[a]-sg*h)<1e-9 for v in f)]
S=tri(S)
PIECES=[('P','half octahedron',P,(240,222,160)),('Q','quarter tetrahedron',Q,(230,140,120)),("Q′",'big quarter tetrahedron',Qp,(150,170,215)),
        ('A','Admiral Cap',A,(120,160,230)),('S','Dogstar',S,(170,130,215)),('X','cube minus a roof',X,(150,120,190)),('Y','cube plus a roof',Y,(190,160,230))]
PIECES=[(k,n,orient(T),c) for k,n,T,c in PIECES]
for k,_,T,_ in PIECES: print(k, 'triangles',len(T),'volume',round(volume(T),5))
# ---- draw: depth buffer, one panel per piece, all at one scale
def rot(ax,a):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+math.sin(a)*K+(1-math.cos(a))*K@K
Rv=rot((1,0,0),-0.62)@rot((0,0,1),0.42)          # looking down onto the top face, so dents show
light=np.array([-0.6,0.5,0.62]); light/=np.linalg.norm(light)
GROUND=(20,15,11); GOLD=(222,178,80)
def render(T,col,px,scale):
    T=[t@Rv.T for t in T]; c=np.mean(np.vstack(T),0)
    img=np.zeros((px,px,3)); img[:]=GROUND; Z=np.full((px,px),-1e9)
    for t in T:
        n=np.cross(t[1]-t[0],t[2]-t[0]); n/=np.linalg.norm(n)
        if n[2]<=0: continue
        b=0.18+0.82*max(0,n@light)**1.15; shade=np.array(col)*b
        P=(t-c)[:,:2]*scale*np.array([1,-1])+px/2; zz=(t-c)[:,2]
        x0,y0=np.floor(P.min(0)).astype(int); x1,y1=np.ceil(P.max(0)).astype(int)
        x0,y0=max(x0,0),max(y0,0); x1,y1=min(x1,px-1),min(y1,px-1)
        if x1<x0 or y1<y0: continue
        X,Y=np.meshgrid(np.arange(x0,x1+1)+0.5,np.arange(y0,y1+1)+0.5)
        (ax,ay),(bx,by),(cx,cy)=P; det=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(det)<1e-12: continue
        l1=((by-cy)*(X-cx)+(cx-bx)*(Y-cy))/det; l2=((cy-ay)*(X-cx)+(ax-cx)*(Y-cy))/det; l3=1-l1-l2
        m=(l1>=-1e-9)&(l2>=-1e-9)&(l3>=-1e-9); z=l1*zz[0]+l2*zz[1]+l3*zz[2]
        sub=Z[y0:y1+1,x0:x1+1]; upd=m&(z>sub); sub[upd]=z[upd]
        im=img[y0:y1+1,x0:x1+1]; im[upd]=shade
    out=Image.fromarray(img.astype(np.uint8)); d=ImageDraw.Draw(out)
    # gold edges: polygon outlines of front faces, drawn where the edge is on top (approximate: depth-tested by midpoint)
    for t in T:
        n=np.cross(t[1]-t[0],t[2]-t[0])
        if n[2]<=0: continue
        P=(t-c)[:,:2]*scale*np.array([1,-1])+px/2
        for a in range(3):
            e=(t[a],t[(a+1)%3])
            # skip the diagonals inside flat polygons: an edge shared by two coplanar triangles
            if any(np.allclose(sorted([tuple(np.round(e[0],6)),tuple(np.round(e[1],6))]),sorted([tuple(np.round(u[b],6)),tuple(np.round(u[(b+1)%3],6))])) and u is not t and abs(np.dot(np.cross(u[1]-u[0],u[2]-u[0])/np.linalg.norm(np.cross(u[1]-u[0],u[2]-u[0])),n/np.linalg.norm(n))-1)<1e-6 for u in T for b in range(3)): continue
            mid=(e[0]+e[1])/2-c; mx,my=mid[:2]*scale*np.array([1,-1])+px/2
            ix,iy=int(mx),int(my)
            if 0<=ix<px and 0<=iy<px and Z[iy,ix]<=mid[2]+0.004:
                d.line([tuple(P[a]),tuple(P[(a+1)%3])],fill=GOLD,width=3)
    return out
if __name__=='__main__':
    px=520; scale=px*0.32
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',40); small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
    cols=4; rows=2; W=cols*px; H=rows*(px+90)
    sheet=Image.new('RGB',(W,H),GROUND); d=ImageDraw.Draw(sheet)
    for i,(k,name,T,col) in enumerate(PIECES):
        r,cc=divmod(i,cols); x=cc*px; y=r*(px+90)
        sheet.paste(render(T,col,px,scale),(x,y))
        d.text((x+px/2,y+px+8),k,font=font,fill=GOLD,anchor='mt'); d.text((x+px/2,y+px+52),name,font=small,fill=(233,224,208),anchor='mt')
    # last cell: scale bar of length 1
    x=3*px; y=px+90; d.line([(x+px/2-scale/2,y+px/2),(x+px/2+scale/2,y+px/2)],fill=GOLD,width=5)
    d.text((x+px/2,y+px/2+20),'edge 1',font=small,fill=(233,224,208),anchor='mt'); d.text((x+px/2,y+px/2-60),'all at one scale',font=small,fill=(233,224,208),anchor='mt')
    sheet.save('connectors.png'); print('saved')
