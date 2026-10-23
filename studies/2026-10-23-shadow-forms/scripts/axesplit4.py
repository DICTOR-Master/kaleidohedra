# Pictures of the golden split: each padded piece (core + AXE pyramids, coloured) from two sides with its plain hull, and a patch of
# the two-piece fill (big truncated octahedra at the old icosahedra, small ones at the old Unborns).
import os
src=open('fuse4.py').read(); exec(src.split("res=json.load")[0])
exec(open('axesplit2.py').read().split('T=1/phi')[0])
COL.update({'big':(92,170,96),'small':(236,150,70),'pyr':(40,190,210)})
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
OUT='/home/dicto/Documents/papers-to-read/golden-split'; os.makedirs(OUT,exist_ok=True)
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((110,110))
T=1/phi; S=600
def sheet(title,sub,panels,legend,fn):
    im=Image.new('RGB',(len(panels)*(S+20)+40,S+190),(244,241,234)); d=ImageDraw.Draw(im)
    for i,(ps,R,cap) in enumerate(panels):
        im.paste(draw(ps,S,R),(20+i*(S+20),120)); d.text((30+i*(S+20),S+120),cap,font=F(19),fill=(109,101,86))
    d.text((30,24),title,font=F(36,True),fill=(43,38,32)); d.text((30,72),sub,font=F(21),fill=(109,101,86))
    x=40
    for n,lab in legend:
        d.rectangle((x,S+152,x+22,S+174),fill=COL[n]); d.text((x+30,S+150),lab,font=F(21),fill=(43,38,32)); x+=60+int(d.textlength(lab,font=F(21)))
    im.paste(logo,(im.width-130,10),logo); d.text((im.width-300,S+166),'DICTO · dictospheres.com',font=F(17),fill=(109,101,86))
    im.save(os.path.join(OUT,fn))
R1,R2=rot(0.6,0.45),rot(0.6+np.pi,-0.45)
for k,(nm,base,c,col,sq) in enumerate([('icosahedron',ico,np.zeros(3),'icosahedron','big squares, side 1/√2'),('Unborn',H-uc,uc,'Unborn','small squares, side 1/(φ√2)')]):
    P,pv=piece(T,base,c)
    parts=[{'name':col,'V':P[0]}]+[{'name':'pyr','V':Q} for Q in P[1:]]
    hullp=[{'name':'big' if k==0 else 'small','V':np.vstack(P)}]
    sheet('Golden split: padded %s = truncated octahedron'%nm,'%s + 12 AXE pyramids (AXE cut at t = 1/φ) · exactly convex · 24 corners, 8 hexagons, 6 %s · volume %.4f'%(nm,sq,pv),
          [(parts,R1,'%s (core) + AXE pyramids'%nm),(parts,R2,'other side'),(hullp,R1,'the piece as one solid')],
          [(col,nm),('pyr','AXE pyramids')],'%02d-padded-%s.png'%(k+1,nm))
Pi,_=piece(T,ico,np.zeros(3)); Pu,_=piece(T,H-uc,uc); Bi,Bu=np.vstack(Pi),np.vstack(Pu)
patch=[]
for cc in itertools.product(range(2),repeat=3):
    o=np.array(cc)*phi; patch.append({'name':'big','V':Bi+o})
patch.append({'name':'small','V':Bu})
for cc in [(0,0,1)]: patch.append({'name':'small','V':Bu+np.array(cc)*phi})
sheet('Golden split: the network as two truncated octahedra','big ones where the icosahedra were, small ones where the Unborns were · body-centred · fills space exactly (500,000-point test: 0 gaps, 0 overlaps)',
      [(patch[:8],rot(0.5,0.6),'8 big around a cell (small one hidden inside)'),(patch,rot(0.5,0.6),'with 2 small ones'),([patch[0],patch[8]],rot(0.3,0.3),'big meets small on a hexagon')],
      [('big','padded icosahedron'),('small','padded Unborn')],'03-two-piece-fill.png')
print(sorted(os.listdir(OUT)))
