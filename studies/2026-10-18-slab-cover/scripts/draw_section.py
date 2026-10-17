# DICTO 2026-10-18: SVGs for renders/slab-section.html from data/section-110-float.json
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data'))
import json,numpy as np
D=json.load(open('section-110-float.json'))
def clip(P,Q):  # P ∩ convex Q (both CCW?) Sutherland–Hodgman
    def area(X): return sum(X[i][0]*X[(i+1)%len(X)][1]-X[(i+1)%len(X)][0]*X[i][1] for i in range(len(X)))/2
    if area(Q)<0: Q=Q[::-1]
    out=[np.array(p) for p in P]
    for i in range(len(Q)):
        a,b=np.array(Q[i]),np.array(Q[(i+1)%len(Q)]);ed=b-a;inside=lambda x:ed[0]*(x[1]-a[1])-ed[1]*(x[0]-a[0])>=-1e-12
        inp=out;out=[]
        for j in range(len(inp)):
            A,B=inp[j],inp[(j+1)%len(inp)]
            ia,ib=inside(A),inside(B)
            if ia: out.append(A)
            if ia!=ib:
                da=ed[0]*(A[1]-a[1])-ed[1]*(A[0]-a[0]);db=ed[0]*(B[1]-a[1])-ed[1]*(B[0]-a[0])
                out.append(A+(B-A)*da/(da-db))
        if len(out)<3: return None
    return out
R=D['rts'];O=[r for r in R if np.hypot(*r['c'])<1e-9][0]
reds=[]
for i in range(len(R)):
    for j in range(i+1,len(R)):
        X=clip(R[i]['p'],R[j]['p'])
        if X: reds.append(X)
rin=0.66667;g=0.1049191;sd=np.array(D['slabdir'])
# slab face extent: origin polygon vertices with u ~ rin
fw=[p[1] for p in O['p'] if abs(p[0]-rin)<1e-3]
nbp=[r for r in R if abs(r['c'][0]-sd[0])<1e-6 and abs(r['c'][1]-sd[1])<1e-6][0]
fw2=[p[1] for p in nbp['p'] if abs(p[0]-(sd[0]-rin))<1e-3]
w0,w1=max(min(fw),min(fw2)),min(max(fw),max(fw2))
print('slab face w-extent',w0,w1, 'origin face',min(fw),max(fw))
def svg(view,W,H,scale_lbl,zoom=False):
    H=round(W*(view[3]-view[2])/(view[1]-view[0]))
    x0,x1,y0,y1=view;sx=W/(x1-x0)
    T=lambda p:(f'{(p[0]-x0)*sx:.2f}',f'{(y1-p[1])*sx:.2f}')
    pts=lambda P:' '.join(','.join(T(p)) for p in P)
    s=[f'<svg viewBox="0 0 {W} {H}" role="img">']
    s.append(f'<rect width="{W}" height="{H}" class="gap"/>')
    for r in R: s.append(f'<polygon points="{pts(r["p"])}" class="rt"/>')
    for X in reds: s.append(f'<polygon points="{pts(X)}" class="red"/>')
    # slab layers
    for k in range(2):
        a=rin+k*g/2;b=a+g/2
        s.append(f'<polygon points="{pts([(a,w0),(b,w0),(b,w1),(a,w1)])}" class="layer l{k}"/>')
    s.append(f'<line x1="{T((rin+g/2,w0))[0]}" y1="{T((0,w0))[1]}" x2="{T((rin+g/2,w1))[0]}" y2="{T((0,w1))[1]}" class="mid"/>')
    for t in D['tiles']: s.append(f'<polygon points="{pts(t["p"])}" class="tile {t["k"]}"/>')
    for r in R: s.append(f'<polygon points="{pts(r["p"])}" class="rtl"/>')
    for r in R:
        c=r['c']
        if x0<c[0]<x1 and y0<c[1]<y1: s.append(f'<circle cx="{T(c)[0]}" cy="{T(c)[1]}" r="{3 if not zoom else 4}" class="ctr"/>')
    s.append('</svg>');return '\n'.join(s)
main=svg((-1.15,2.45,-1.25,1.25),720,500,'')
zoom=svg((0.42,1.02,-0.32,0.32),480,0,'',True)
json.dump(dict(main=main,zoom=zoom,w0=w0,w1=w1),open('section-110-svgs.json','w'))
