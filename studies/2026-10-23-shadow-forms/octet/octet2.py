# Pictures: the octet family (tetrahedron piece gold, octahedron piece blue) and the factor-x family (T(x) green, T(1/x) orange).
import os
os.chdir('/home/dicto/shadow-fusions'); src=open('fuse4.py').read(); exec(src.split("res=json.load")[0]); os.chdir('octet')
exec(open('octet1.py').read().split('ts=[')[0])
COL.update({'tet':(232,186,64),'oct':(70,130,180),'big':(92,170,96),'small':(236,150,70)})
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((100,100))
OUT='/home/dicto/Documents/papers-to-read/golden-split'; SZ=330
def strip(title,sub,cols,fn):
    im=Image.new('RGB',(len(cols)*SZ+40,2*SZ+200),(244,241,234)); d=ImageDraw.Draw(im)
    d.text((24,20),title,font=F(32,True),fill=(43,38,32)); d.text((24,64),sub,font=F(19),fill=(109,101,86))
    for i,(lab,a,b) in enumerate(cols):
        x=20+i*SZ
        if a is not None: im.paste(draw([a],SZ,rot(0.6,0.45)),(x,110))
        if b is not None: im.paste(draw([b],SZ,rot(0.6,0.45)),(x,110+SZ))
        d.text((x+10,110+2*SZ+8),lab,font=F(20,True),fill=(43,38,32))
    im.paste(logo,(im.width-115,10),logo); d.text((im.width-280,im.height-30),'DICTO · dictospheres.com',font=F(16),fill=(109,101,86)); im.save(os.path.join(OUT,fn))
cols=[]
for t,lab in [(0.03,'t ≈ 0'),(0.2,'t = 0.2'),(1/3,'t = 1/3 octet'),(0.5,'t = 0.5'),(0.75,'t = 0.75'),(0.97,'t ≈ 1')]:
    A=cell('T',Tc[0],t); B=cell('O',O[0],t)
    cols.append((lab,{'name':'tet','V':A} if A is not None and ConvexHull(A).volume>1e-4 else None,{'name':'oct','V':B} if B is not None and ConvexHull(B).volume>1e-4 else None))
strip('The octet family: rhombic dodecahedron → octet → cube','top: tetrahedron piece (gold) · bottom: octahedron piece (blue) · each pair fills space, every t (power-diagram cut of each tetra–octa double cone at fraction t)',cols,'07-octet-family.png')
def TO(x,s): return np.array(sorted({tuple(sg[k]*perm[k]*s for k in range(3)) for perm in itertools.permutations((1+x,x,0)) for sg in itertools.product((1,-1),repeat=3)}))
LL=2.0; cols=[]
phi=(1+5**.5)/2
for x,lab in [(0.02,'x ≈ 0'),(0.3,'x = 0.3'),(1.0,'x = 1 Kelvin'),(phi,'x = τ golden'),(3.0,'x = 3'),(50.0,'x → ∞')]:
    cols.append((lab,{'name':'big','V':TO(x,LL/(2*(1+x)))},{'name':'small','V':TO(1/x,LL/(2*(1+1/x)))}))
strip('Factor x: T(x) at the corners, T(1/x) at the centres','top: T(x) (green) · bottom: T(1/x) (orange) · x ≈ 0: octahedra + cuboctahedra · x = 1: Kelvin · x = τ: Icosaxes + Unborn Axes',cols,'08-factor-x-family.png')
print('ok')
