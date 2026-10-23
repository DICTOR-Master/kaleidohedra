# Shadow forms, step 5: each chunky fusion (fuse4) as its own picture, two sides, large; plus the single pieces they are made of.
import os
src=open('fuse4.py').read(); exec(src.split("F=lambda")[0])
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
NET={'icoUnborn':'Icosahedra and Unborn','jewelDodeca':'Lotus Jewel network','four':'Jewel | Tricap | Unborn | AXE'}
OUT='/home/dicto/Documents/papers-to-read/shadow-shapes'; os.makedirs(OUT,exist_ok=True)
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((110,110))
S=760
def card(ps,title,line2,fn):
    im=Image.new('RGB',(2*S+60,S+190),(244,241,234)); d=ImageDraw.Draw(im)
    im.paste(draw(ps,S,rot(0.6,0.45)),(20,120)); im.paste(draw(ps,S,rot(0.6+np.pi,-0.45)),(S+40,120))
    d.text((30,24),title,font=F(40,True),fill=(43,38,32)); d.text((30,76),line2,font=F(22),fill=(109,101,86))
    x=40
    for n in dict.fromkeys(p['name'] for p in ps):
        d.rectangle((x,S+138,x+22,S+160),fill=COL[n]); d.text((x+30,S+136),n,font=F(22),fill=(43,38,32)); x+=60+int(d.textlength(n,font=F(22)))
    d.text((im.width-360,S+136),'two sides · DICTO · dictospheres.com',font=F(18),fill=(109,101,86))
    im.paste(logo,(im.width-130,10),logo); im.save(os.path.join(OUT,fn))
singles={}
for kind in ['icoUnborn','jewelDodeca','four']:
    for p in net(kind): singles.setdefault(p['name'],p)
for k,n in enumerate(['AXE','Unborn','Tricap','Lotus Jewel','icosahedron','dodecahedron']):
    if n in singles: card([singles[n]],n,'single piece',f'0{k}-{n.replace(" ","-")}.png')
for k,(r,ps) in enumerate(sorted(geo,key=lambda g:-g[0]['fill']),1):
    t=' + '.join(r['pieces'])
    card(ps,t,'%s · fill %.1f%% of its convex hull · volume %.4f · elongation %.2f'%(NET[r['network']],100*r['fill'],r['vol'],r['elong']),
         '%02d-%s.png'%(10+k,t.replace(' + ','+').replace(' ','-')))
print(sorted(os.listdir(OUT)))
