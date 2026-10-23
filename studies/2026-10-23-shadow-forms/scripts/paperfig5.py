# Paper #51 figure: failures in the middle — what sticks out when the split is not golden, and when an AXE is given whole.
import os, json
exec(open('paperfigs.py').read().split("R1,R2=rot")[0])
tp=json.load(open('twopiece-ico.json'))
star=[{'name':'icosahedron','V':np.array(tp['base'])}]+[{'name':'AXE','V':np.array(V)} for V in tp['axes']]
Pa,_=piece(0.85,ico,np.zeros(3)); Pb,_=piece(0.35,H-uc,uc)
Ia=[{'name':'icosahedron','V':Pa[0]}]+[{'name':'pyr','V':Q} for Q in Pa[1:]]
Ub=[{'name':'Unborn','V':Pb[0]}]+[{'name':'pyr','V':Q} for Q in Pb[1:]]
fig([(star,rot(0.6,0.45)),(Ia,rot(0.6,0.45)),(Ub,rot(0.6,0.45))],'fig-failures.png')
