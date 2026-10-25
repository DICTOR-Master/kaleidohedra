# Figure 1 of the David and Goliath paper: Goliath, David, and Goliath clad by its 12 Davids (float rendering of the exact cells).
# Run: ~/geom/bin/python make_figure.py  (dicto-big-brother; needs ../../dicto-logo.png)
import numpy as np, itertools, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
here=os.path.dirname(os.path.abspath(__file__))
G=np.array([v for a in (.5,-.5) for b in (1,-1) for v in [(0,a,b),(b,0,a),(a,b,0)]])   # Goliath corners (0, ±1/2, ±1) cyclic
CR=[(.5,0,1),(1.5,0,1),(1,.5,0),(1,1.5,0),(0,1,.5),(0,1,1.5)]
corners=np.array([np.array(c)+(1,1,1)+2*np.array(t) for t in itertools.product(range(-2,3),repeat=3) for c in CR])  # the 6d sites = Cr sites + (1,1,1): all corners of the tiling
assert all(((corners-g)**2).sum(1).min()<1e-12 for g in G)
def david(c):
    d=((corners-c)**2).sum(1); P=np.unique(np.round(corners[np.abs(d-.5)<1e-9],9),axis=0)
    assert len(P)==4 and abs(ConvexHull(P).volume-1/6)<1e-12; return P
cr=[np.array(v) for a in (.5,-.5) for b in (1,-1) for v in [(a,0,b),(b,a,0),(0,b,a)]]  # the 12 Cr around the origin, dist^2 5/4
assert len(cr)==12 and all(abs((c**2).sum()-1.25)<1e-12 for c in cr)
GOLD_EQ='#d4a72c'; GOLD_ISO='#f1d98a'; DAVID='#5b6fb8'; EDGE='#3a2f12'
def faces(P):
    h=ConvexHull(P); return [P[s] for s in h.simplices]
def tri_type(f):
    L=sorted(((f[i]-f[j])**2).sum() for i,j in [(0,1),(1,2),(0,2)]); return 'eq' if abs(L[0]-1.5)<1e-9 else 'iso'
def draw(ax,polys,colors,alpha=1.0,lw=.6):
    pc=Poly3DCollection(polys,facecolors=colors,edgecolors=EDGE,linewidths=lw,alpha=alpha); pc.set_sort_zpos=None; ax.add_collection3d(pc)
def setup(ax,r,title,elev=22,azim=33):
    ax.set_xlim(-r,r); ax.set_ylim(-r,r); ax.set_zlim(-r,r); ax.set_box_aspect((1,1,1)); ax.set_axis_off(); ax.view_init(elev=elev,azim=azim)
    ax.set_title(title,fontsize=9.5,pad=0)
fig=plt.figure(figsize=(10,3.9),dpi=220)
ax1=fig.add_subplot(131,projection='3d'); F=faces(G)
draw(ax1,F,[GOLD_EQ if tri_type(f)=='eq' else GOLD_ISO for f in F],alpha=.93)
ax1.scatter(*G.T,s=7,c=EDGE,depthshade=False)
setup(ax1,1.05,'Goliath (Si cell)\nhull of (0, ±1/2, ±1) cyclic · volume 7/2')
ax2=fig.add_subplot(132,projection='3d'); ax2.computed_zorder=False; D=david(cr[0]); FD=faces(D); c0=cr[0]
draw(ax2,[f-c0 for f in FD],[DAVID]*4,alpha=.55)
for i,j in itertools.combinations(range(4),2):
    if abs(((D[i]-D[j])**2).sum()-1)<1e-9: ax2.plot(*np.array([D[i]-c0,D[j]-c0]).T,color='#c0392b',lw=2.2,zorder=10)
ax2.scatter(0,0,0,s=10,c='k',depthshade=False)
setup(ax2,0.62,'David (Cr cell)\ntetragonal disphenoid · volume 1/6\n(red: the two opposite edges of length 1)',elev=28,azim=-62)
ax3=fig.add_subplot(133,projection='3d')
polys=[];cols=[]
for f in F:
    if tri_type(f)=='eq': polys.append(f); cols.append(GOLD_EQ)
for c in cr:
    for f in faces(david(c)):
        if not all(any(np.allclose(p,g) for g in G) for p in f): polys.append(f); cols.append(DAVID)
draw(ax3,polys,cols,alpha=.97,lw=.45)
setup(ax3,1.75,'Goliath clad by its 12 Davids\n(gold: the 8 faces shared with Goliaths)')
fig.subplots_adjust(left=0,right=1,top=.9,bottom=0,wspace=0)
logo=plt.imread(os.path.join(here,'..','..','dicto-logo.png'))
la=fig.add_axes([.905,.02,.085,.085*10/3.9*logo.shape[0]/logo.shape[1]]); la.imshow(logo); la.set_axis_off()
fig.text(.01,.02,'DICTO · dictospheres.com',fontsize=7,color='#6b5310')
fig.savefig(os.path.join(here,'fig1-david-goliath.png'),dpi=220,facecolor='white')
print('written')
