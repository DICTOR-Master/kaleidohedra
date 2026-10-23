# Paper #51 figure for Theorem 4: factor-x strip (top T(x), bottom T(1/x)), white background, small labels, DICTO mark.
import os
exec(open('octet2.py').read().split("OUT='/home")[0])
SZ=330; xs=[(0.02,'x ≈ 0'),(0.3,'x = 0.3'),(1.0,'x = 1'),((1+5**.5)/2,'x = τ'),(3.0,'x = 3'),(50.0,'x → ∞')]
def TO(x,s): return np.array(sorted({tuple(sg[k]*perm[k]*s for k in range(3)) for perm in itertools.permutations((1+x,x,0)) for sg in itertools.product((1,-1),repeat=3)}))
im=Image.new('RGB',(len(xs)*SZ,2*SZ+50),(255,255,255)); d=ImageDraw.Draw(im)
for i,(x,lab) in enumerate(xs):
    for r,(y,c) in enumerate([(x,'big'),(1/x,'small')]):
        exec(open('/home/dicto/shadow-fusions/solidraw.py').read()); p=draw_solids([{'name':c,'V':TO(y,1/(1+y))}],SZ,rot(0.6,0.45),COL,L,(244,241,234)); p.putdata([(255,255,255) if q==(244,241,234) else q for q in p.getdata()]); im.paste(p,(i*SZ,r*SZ))
    d.text((i*SZ+SZ//2-40,2*SZ+10),lab,font=F(24,True),fill=(43,38,32))
lg=logo.copy(); lg.thumbnail((60,60)); im.paste(lg,(im.width-70,6),lg)
im.save('/home/dicto/k-research/papers/2026-10-23-golden-split/figures/fig-factor-x.png'); print(im.size)
