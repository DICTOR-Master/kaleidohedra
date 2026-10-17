# DICTO 2026-10-18: 2D sketch of the Admiral Cap analog -> renders/ocd-octahedron-caps.html (data/ocd-octa-sketch.json)
import json,os,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); d=json.load(open(os.path.join(H,'..','data','ocd-octa-sketch.json')))
R=d['R']
def panel(view,W,body):
    x0,x1,y0,y1=view;Hh=round(W*(y1-y0)/(x1-x0));s=W/(x1-x0)
    T=lambda p:((p[0]-x0)*s,(y1-p[1])*s)
    pts=lambda P:' '.join('%.2f,%.2f'%T(p) for p in P)
    return f'<svg viewBox="0 0 {W} {Hh}" role="img">'+body(T,pts,s)+'</svg>'
dia=[(R,0),(0,R),(-R,0),(0,-R)]
def A(T,pts,s):
    o=[f'<polygon points="{pts(dia)}" class="shell"/>']
    caps={'+x':[(0,0),(R/2,R/2),(R,0),(R/2,-R/2)],'+y':[(0,0),(-R/2,R/2),(0,R),(R/2,R/2)],'-x':[(0,0),(-R/2,-R/2),(-R,0),(-R/2,R/2)],'-y':[(0,0),(R/2,-R/2),(0,-R),(-R/2,-R/2)]}
    for k,P in caps.items(): o.append(f'<polygon points="{pts(P)}" class="cap c{k[1]}"/>')
    o.append(f'<polygon points="{pts(d["ocd_z0"])}" class="ocd"/>')
    for a,b in [((-R/2,-R/2),(R/2,R/2)),((-R/2,R/2),(R/2,-R/2))]:
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="cut"/>'%(*T(a),*T(b)))
    o.append(f'<polygon points="{pts(dia)}" class="oct"/>')
    for k,(x,y) in {'+x cap':(R*.7,0),'−x cap':(-R*.7,0),'+y cap':(0,R*.7),'−y cap':(0,-R*.7)}.items():
        X,Y=T((x,y));o.append(f'<text x="{X:.1f}" y="{Y:.1f}" class="lbl" text-anchor="middle">{k}</text>')
    X,Y=T((0,0));o.append(f'<text x="{X:.1f}" y="{Y+4:.1f}" class="lbl strong" text-anchor="middle">OCD</text>')
    return ''.join(o)
def B(T,pts,s):
    o=[f'<polygon points="{pts(dia)}" class="shell"/>']
    for f in d['top']: o.append(f'<polygon points="{pts(f["p"])}" class="{"hex" if f["k"]==6 else "kite"}"/>')
    for a,b in [((-R,0),(R,0)),((0,-R),(0,R))]: pass
    for a,b in [((-R/2,-R/2),(R/2,R/2)),((-R/2,R/2),(R/2,-R/2))]:
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="cut"/>'%(*T(a),*T(b)))
    o.append(f'<polygon points="{pts(dia)}" class="oct"/>')
    return ''.join(o)
def C(T,pts,s):
    P=np.array(d['hex']);o=[f'<polygon points="{pts(P)}" class="hex"/>']
    for i,k in enumerate(d['hexkind']):
        q=P[i]
        if k=='side':
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="ridge"/>'%(*T((0,0)),*T(q)))
        X,Y=T(q*1.16);o.append(f'<text x="{X:.1f}" y="{Y+4:.1f}" class="lbl small" text-anchor="middle">{"ridge end" if k=="side" else "2-fold"}</text>')
        o.append('<circle cx="%.1f" cy="%.1f" r="4" class="%s"/>'%(*T(q),'dot2' if k=='two' else 'dots'))
    X,Y=T((0,0));o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="5" class="apex"/>')
    return ''.join(o)
pa=panel((-1.2,1.2,-1.2,1.2),460,A); pb=panel((-1.2,1.2,-1.2,1.2),460,B); pc=panel((-0.34,0.34,-0.3,0.3),460,C)
r=d; frac=1-r['shell_frac']
html=open(os.path.join(H,'template.html')).read()
for k,v in dict(PA=pa,PB=pb,PC=pc,FILL='%.1f'%(100*r['ocd_vol']/r['oct_vol']),SHELL='%.1f'%(100*r['shell_frac']),CAP='%.4f'%r['cap_vol'],
  CAPPC='%.2f'%(100*r['cap_vol']/r['oct_vol']),EDGE='%.4f'%(R*2**.5),HEXE='%.4f'%r['hex_edge'],KEYH='%.4f'%r['key_h'],KEYR='%.3f'%(r['key_h']/r['hex_edge']),TIN='%.4f'%(R*2**.5/(2*6**.5))).items():
    html=html.replace('{'+k+'}',v)
open(os.path.join(H,'..','renders','ocd-octahedron-caps.html'),'w').write(html)
print('ok')
