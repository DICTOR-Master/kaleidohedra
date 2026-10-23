# Figures for paper #51 (no title bars; captions live in the paper): panels side by side, light background, DICTO mark small.
import os
exec(open('axesplit4.py').read().split('R1,R2=')[0])
exec(open('jewelsplit1.py').read().split('VD=ConvexHull')[0].split("exec(open('axesplit2.py')")[1].split('\n',1)[1])
COL.update({'dodecahedron':(230,180,60)})
OUT='/home/dicto/k-research/papers/2026-10-23-golden-split/figures'; T=1/phi; S=700
exec(open('/home/dicto/shadow-fusions/solidraw.py').read())
def fig(panels,fn):
    im=Image.new('RGB',(len(panels)*S,S),(255,255,255))
    for i,(ps,R) in enumerate(panels):
        p=draw_solids(ps,S,R,COL,L,(244,241,234)) if all(q['name'] in ('big','small') for q in ps) else draw(ps,S,R); px=p.load()
        im.paste(p,(i*S,0))
    d=ImageDraw.Draw(im)
    for x in range(im.width):
        for y in range(im.height):
            pass
    im=Image.eval(im,lambda v:v)  # keep
    # replace the drawing background (244,241,234) by white
    data=[(255,255,255) if c==(244,241,234) else c for c in im.getdata()]; im.putdata(data)
    lg=logo.copy(); lg.thumbnail((70,70)); im.paste(lg,(im.width-80,8),lg); im.save(os.path.join(OUT,fn)); print(fn,im.size)
R1,R2=rot(0.6,0.45),rot(0.6+np.pi,-0.45); R3=rot(np.pi/4,np.arctan(1/2**.5))
Pi,_=piece(T,ico,np.zeros(3)); Pu,_=piece(T,H-uc,uc); Bi,Bu=np.vstack(Pi),np.vstack(Pu)
bigP=[{'name':'icosahedron','V':Pi[0]}]+[{'name':'pyr','V':Q} for Q in Pi[1:]]
smallP=[{'name':'Unborn','V':Pu[0]}]+[{'name':'pyr','V':Q} for Q in Pu[1:]]
fig([(bigP,R1),([{'name':'big','V':Bi}],R1),(smallP,R1),([{'name':'small','V':Bu}],R1)],'fig1-golden-pair.png')
patch=[{'name':'big','V':Bi+np.array(c)*phi} for c in itertools.product(range(2),repeat=3)]+[{'name':'small','V':Bu},{'name':'small','V':Bu+np.array([0,0,phi])}]
fig([(patch[:8],rot(0.5,0.6)),(patch,rot(0.5,0.6)),([patch[0],patch[8]],rot(0.3,0.3))],'fig3-fill.png')
# the AXE and its split
A=cellA[0]; m1=(A[0]+A[1])/2; m2=(A[2]+A[3])/2; p=m1+T*(m2-m1)
cones=[{'name':'icosahedron' if set(f)>={0,1} else 'Unborn','V':np.vstack([A[list(f)],p])} for f in itertools.combinations(range(4),3)]
fig([([{'name':'AXE','V':A}],rot(1.0,0.75)),(cones,rot(1.0,0.75)),([dict(c,V=c['V']+1.1*(c['V'].mean(0)-p)) for c in cones],rot(1.0,0.75))],'fig2-axe-split.png')
bigK=[{'name':'Lotus Jewel','V':JV}]+[{'name':'pyr','V':Q} for Q in Pi[1:]]
smallK=[{'name':'dodecahedron','V':D}]+[{'name':'pyr','V':Q} for Q in Pu[1:]]
pair=[{'name':'big','V':q['V']} for q in bigK]+[{'name':'small','V':q['V']} for q in smallK]
fig([(bigK,R3),(smallK,R3),(pair,rot(0.3,0.3))],'fig4-keyed-pair.png')
