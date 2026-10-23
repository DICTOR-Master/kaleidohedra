# Flat top and bottom, step 5: pictures of the best turned-copy units (flat4): the unit from two sides, and a patch of the layer
# with the unit in red and its turned twin in blue.
import os, sys
src=open('fuse4.py').read(); exec(src.split("res=json.load")[0])
COL.update({'unit1':(214,96,77),'unit2':(70,130,180)})
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
OUT='/home/dicto/Documents/papers-to-read/flat-layer-units'; os.makedirs(OUT,exist_ok=True)
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((110,110))
LN={'A':'icosahedron middle to middle','B':'icosahedron middle to Unborn middle','C':'Unborn middle to middle'}
SUB={'x even':lambda a,b:a%2==0,'y even':lambda a,b:b%2==0,'checker':lambda a,b:(a+b)%2==0}
FL={(-1,1,1):'mirror across x',(1,-1,1):'mirror across y',(-1,-1,1):'half-turn about the upright axis',(1,1,-1):'mirror top↔bottom',
    (-1,1,-1):'half-turn about the y axis',(1,-1,-1):'half-turn about the x axis',(-1,-1,-1):'point reflection'}
res=json.load(open('flat4-units.json')); seen=set(); picks=[]
for r in res:
    if r['layer'] not in seen and len(picks)<3: seen.add(r['layer']); picks.append(r)
S=620
for k,r in enumerate(picks):
    U=[{'name':n,'V':np.array(P)} for n,P in r['unit']]; s=np.array(r['flip']); off=np.array(r['off']); sub=SUB[r['sub']]
    patch=[]; c0=np.vstack([p['V'] for p in U]).mean(0)
    for a,b in itertools.product(range(-3,4),repeat=2):
        if not sub(a,b): continue
        t=np.array([a*phi,b*phi,0])
        for nm,f in (('unit1',lambda V:V+t),('unit2',lambda V:V*s+off+t)):
            Vs=[f(p['V']) for p in U]; c=np.vstack(Vs).mean(0)
            if abs(c[0]-c0[0])<1.6*phi and abs(c[1]-c0[1])<1.6*phi: patch+=[{'name':nm,'V':V} for V in Vs]
    im=Image.new('RGB',(3*S+80,S+190),(244,241,234)); d=ImageDraw.Draw(im)
    im.paste(draw(U,S,rot(0.6,0.45)),(20,120)); im.paste(draw(U,S,rot(0.6+np.pi,-0.45)),(S+40,120)); im.paste(draw(patch,S,rot(0.5,0.6)),(2*S+60,120))
    d.text((30,24),'Flat layer %s, %s: unit + turned twin'%(r['layer'],LN[r['layer']]),font=F(34,True),fill=(43,38,32))
    d.text((30,72),'twin = %s + one-cell slide %s · unit fills %.1f%% of its convex hull (100%% = no protrusions)'%(FL[tuple(r['flip'])],r['slide'],100*r['fill']),font=F(21),fill=(109,101,86))
    x=40
    for n in ['icosahedron','Unborn','AXE']:
        d.rectangle((x,S+138,x+22,S+160),fill=COL[n]); d.text((x+30,S+136),n+' part',font=F(21),fill=(43,38,32)); x+=90+int(d.textlength(n,font=F(21)))
    d.text((2*S+70,S+136),'right: the layer, unit red, turned twin blue',font=F(19),fill=(109,101,86))
    im.paste(logo,(im.width-130,10),logo); d.text((im.width-300,S+166),'DICTO · dictospheres.com',font=F(17),fill=(109,101,86))
    im.save(os.path.join(OUT,'%02d-turned-layer-%s.png'%(k+4,r['layer'])))
print(sorted(os.listdir(OUT)))
