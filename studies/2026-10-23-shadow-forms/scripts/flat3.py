# Flat top and bottom, step 3: pictures of each layer's best unit piece: the unit from two sides (coloured by the piece each part
# came from), and a 3x3 patch of the layer tiled by the unit (alternate units in two colours) to show the flat top.
import os
src=open('fuse4.py').read(); exec(src.split("res=json.load")[0])
COL.update({'unit1':(214,96,77),'unit2':(70,130,180)})
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
OUT='/home/dicto/Documents/papers-to-read/flat-layer-units'; os.makedirs(OUT,exist_ok=True)
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((110,110))
res=json.load(open('flat2-units.json')); S=620
for k,(name,r) in enumerate(res.items()):
    U=[{'name':n,'V':np.array(P)} for n,P in r['unit']]
    patch=[]
    for i,j in itertools.product(range(3),range(3)):
        for p in U: patch.append({'name':'unit1' if (i+j)%2==0 else 'unit2','V':p['V']+np.array([i,j,0])*phi})
    im=Image.new('RGB',(3*S+80,S+190),(244,241,234)); d=ImageDraw.Draw(im)
    im.paste(draw(U,S,rot(0.6,0.45)),(20,120)); im.paste(draw(U,S,rot(0.6+np.pi,-0.45)),(S+40,120)); im.paste(draw(patch,S,rot(0.5,0.9)),(2*S+60,120))
    d.text((30,24),'Flat layer %s: one unit piece'%name,font=F(36,True),fill=(43,38,32))
    d.text((30,72),'layer z = %.3f … %.3f · unit fills %.1f%% of its convex hull (100%% = no protrusions) · translation copies only'%(r['z'][0],r['z'][1],100*r['fill']),font=F(21),fill=(109,101,86))
    x=40
    for n in ['icosahedron','Unborn','AXE']:
        d.rectangle((x,S+138,x+22,S+160),fill=COL[n]); d.text((x+30,S+136),n+' part',font=F(21),fill=(43,38,32)); x+=90+int(d.textlength(n,font=F(21)))
    d.text((2*S+70,S+136),'right: 3×3 patch of the layer, flat top',font=F(19),fill=(109,101,86))
    im.paste(logo,(im.width-130,10),logo); d.text((im.width-300,S+166),'DICTO · dictospheres.com',font=F(17),fill=(109,101,86))
    im.save(os.path.join(OUT,'%02d-layer-%s.png'%(k+1,name.split()[0])))
print(sorted(os.listdir(OUT)))
