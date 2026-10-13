# Fused outer solids for the stages the paper examines (run on dicto-node; uses the study's scripts/build_transitional.py functions
# without writing transitional.js). Output: data/fused-extra.json. DICTO · dictospheres.com
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/fused-shells/scripts'))
import numpy as np
from scipy.spatial import ConvexHull
import build_transitional as bt
JOBS=[('KARMA_LOTUS_2','karma.lotus','app',2),('KARMA_LOTUS_3','karma.lotus','app',3),('BODHI_B2','bodhi.kitB','app',2),('DHARMA_80','dharma.cycle','route',7),
      ('DHARMA_10','dharma.cycle','route',10),('DODECA_2','karma.dodeca','app',2),('DODECA_3','karma.dodeca','app',3),('STEP2_2','karma.step2','app',2),('STEP2_4','karma.step2','app',4),('DHARMA_8','dharma.cycle','route',8),('DHARMA_5','dharma.cycle','route',5),('DHARMA_2','dharma.cycle','route',2)]
out={}
for sid,view,how,k in JOBS:
    pcs=bt.stage_pieces(view,how,k)
    V,F,C,holes,vol,ns=bt.fused_polyhedron(pcs)
    want=sum(ConvexHull(Q).volume for _,Q,_ in pcs)
    print(sid,len(pcs),'V',len(V),'F',len(F),'holes',holes,'split',ns,'vol',round(vol,5),'want',round(want,5),flush=True)
    out[sid]={'view':view,'how':how,'k':k,'vertices':np.round(V,7).tolist(),'faces':[list(map(int,f)) for f in F],'colours':list(map(int,C)),'volume':vol,'pieces_volume':want,'holes':holes,'split':ns}
json.dump(out,open(os.path.expanduser('~/paper-work/fused-extra.json'),'w'))
