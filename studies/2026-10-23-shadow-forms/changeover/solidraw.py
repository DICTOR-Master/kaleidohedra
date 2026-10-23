# Draw convex solids with their true faces (coplanar hull triangles merged), for figures where faces must read as hexagons/squares.
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
def faces_of(V):
    h=ConvexHull(V); out=[]
    for e in h.equations:
        if any(np.dot(e[:3],q[:3])>1-1e-7 and abs(e[3]-q[3])<1e-7 for q,_ in out): continue
        on=V[np.abs(V@e[:3]+e[3])<1e-7]; c=on.mean(0); u=on[0]-c; u/=np.linalg.norm(u); w=np.cross(e[:3],u)
        on=on[np.argsort(np.arctan2((on-c)@w,(on-c)@u))]; out.append((e,on))
    return out
def draw_solids(ps,size,R,COL,L,bg=(255,255,255)):
    im=Image.new('RGB',(size,size),bg); d=ImageDraw.Draw(im)
    allV=np.vstack([p['V'] for p in ps]); c=allV.mean(0); r=np.max(np.linalg.norm(allV-c,axis=1)); polys=[]
    for p in ps:
        for e,on in faces_of(p['V']):
            n=R@e[:3]
            if n[2]<=1e-9: continue
            W=(on-c)@R.T; sh=0.45+0.55*max(0,n@L); col=tuple(int(x*sh) for x in COL[p['name']])
            polys.append((W[:,2].mean(),[(size/2+q[0]/r*size*0.42,size/2-q[1]/r*size*0.42) for q in W],col))
    for z,pts,col in sorted(polys,key=lambda x:x[0]): d.polygon(pts,fill=col,outline=tuple(max(0,x-70) for x in col),width=2)
    return im
