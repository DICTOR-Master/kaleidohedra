# Pictures: Samson (cut-corner cube) and Delilah (octahedron), the Delian bond, t = 1 − (2/3)·2^(−1/3).
import os
os.chdir('/home/dicto/shadow-fusions'); src=open('fuse4.py').read(); exec(src.split("res=json.load")[0]); os.chdir('octet')
exec(open('octet1.py').read().split('ts=[')[0])
exec(open('/home/dicto/shadow-fusions/solidraw.py').read())
COL.update({'samson':(205,150,60),'delilah':(80,135,190)})
F=lambda n,b=False:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
t=1-(2/3)*2**(-1/3); Sm=cell('T',Tc[0],t); Dl=cell('O',O[0],t)
SZ=520; R1,R2=rot(0.6,0.45),rot(0.6+np.pi,-0.45)
# a patch: the tetra pieces and octa pieces of one cube of side 2
patch=[]
for c in itertools.product((0,),repeat=3):
    for p in Tc[:4]: 
        V=cell('T',p,t); patch.append({'name':'samson','V':V})
    for p in O[:3]:
        V=cell('O',np.array(p,float),t); patch.append({'name':'delilah','V':V})
pair=[{'name':'samson','V':Sm},{'name':'delilah','V':Dl}]
panels=[([{'name':'samson','V':Sm}],R1,'Samson'),([{'name':'samson','V':Sm}],R2,'Samson, other side'),([{'name':'delilah','V':Dl}],R1,'Delilah'),
        (pair,rot(0.3,0.35),'Samson and Delilah, face to face'),(patch,rot(0.5,0.6),'the Delian bond filling space')]
im=Image.new('RGB',(3*SZ+40,2*SZ+230),(244,241,234)); d=ImageDraw.Draw(im)
d.text((24,20),'Samson and Delilah: the Delian bond',font=F(38,True),fill=(43,38,32))
d.text((24,72),'In the octet family at t = 1 − (2/3)·2^(−1/3): Samson (a cube with 4 alternate corners cut so deep it looks like a clipped tetrahedron)',font=F(20),fill=(109,101,86))
d.text((24,100),'and Delilah (the regular octahedron) have exactly equal volume, 2/3 each; Delilah’s edge is 2^(1/6), the square root of ∛2, the Delian number. Names by DICTO.',font=F(20),fill=(109,101,86))
for i,(ps,R,cap) in enumerate(panels):
    x=20+(i%3)*SZ; y=140+(i//3)*SZ
    im.paste(draw_solids(ps,SZ,R,COL,L,(244,241,234)),(x,y)); d.text((x+14,y+SZ-34),cap,font=F(20,True),fill=(43,38,32))
logo=Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA'); logo.thumbnail((100,100)); im.paste(logo,(im.width-115,10),logo)
d.text((im.width-300,im.height-34),'DICTO · dictospheres.com',font=F(17),fill=(109,101,86))
im.save('/home/dicto/Documents/papers-to-read/golden-split/09-samson-and-delilah.png'); print('ok')
