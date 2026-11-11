"""Figure for #97 draft: (a) Narcissus with face roles; (b) three slabs, word S then T, pulled apart vertically."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from n_slabs import build, H, narc, SITE
GOLD='#c9a227'; PURP='#7b4fa0'; TEAL='#2a8c8c'
def faces(P):
    h=ConvexHull(P); F={}
    for eq,sp in zip(h.equations,h.simplices): F.setdefault(tuple(np.round(eq,7)),set()).update(sp)
    out=[]
    for eq,idx in F.items():
        V=P[sorted(idx)]; n=np.array(eq[:3]); c=V.mean(0)
        u=np.cross(n,[0,0,1] if abs(n[2])<.9 else [1,0,0]); u/=np.linalg.norm(u); v=np.cross(n,u)
        ang=np.arctan2((V-c)@v,(V-c)@u); out.append((V[np.argsort(ang)],n))
    return out
def draw(ax,P,col_by_kind=True,alpha=.85,dz=0,lw=.5,single=None):
    for V,n in faces(P):
        k=len(V); col={6:GOLD,4:PURP,3:TEAL}[k] if single is None else single
        V=V+np.array([0,0,dz])
        ax.add_collection3d(Poly3DCollection([V],facecolor=col,edgecolor='k',linewidths=lw,alpha=alpha))
fig=plt.figure(figsize=(10,4.6))
ax=fig.add_subplot(1,2,1,projection='3d')
P=narc(SITE['A'],H,0,'C'); draw(ax,P)
ax.set_box_aspect((1,1,.9)); ax.view_init(18,-62); ax.set_axis_off()
ax.set_xlim(-.6,.6); ax.set_ylim(-.6,.6); ax.set_zlim(-.1,.9)
ax.set_title('(a) Narcissus',fontsize=9)
ax=fig.add_subplot(1,2,2,projection='3d')
Ps=build('ST',n=1)
for P in Ps:
    ctr=P[:,:2].mean(0)
    if np.linalg.norm(ctr)>1.05: continue
    k=int(np.floor(P[:,2].mean()/H)); down=np.isclose(P[9,2],P[:,2].min())
    draw(ax,P,single=(GOLD if down else PURP),alpha=.9,dz=.9*k,lw=.35)
ax.set_box_aspect((1,1,1.5)); ax.view_init(14,-60); ax.set_axis_off()
ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.set_zlim(0,3*H+1.9)
ax.set_title('(b) three layers, pulled apart',fontsize=9)
fig.text(.99,.01,'DICTO',fontsize=8,ha='right',color='#888')
plt.tight_layout(); plt.savefig('~/k-research/papers/2026-11-05-keyed-narcissus/figures/fig1-keyed-narcissus.png',dpi=200)
print('ok')
