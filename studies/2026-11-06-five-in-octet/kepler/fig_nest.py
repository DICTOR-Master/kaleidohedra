# Figure 1 in the Kepler style: the nest in one octahedron (O > I > D > C > T), outer shells as tinted glass.
import numpy as np, sys
sys.path.insert(0, '../scripts'); sys.path.insert(0, '.')
from kepler_render import render, view
exec(open('../scripts/nest.py').read().split("def inside")[0])
S = [(O, (226, 196, 120), 0.95), (I, (122, 150, 196), 0.95), (D, (156, 124, 178), 0.95), (C, (126, 168, 120), 0.95), (T, (196, 96, 72), 1.0)]
# cutaway: front faces whose centre leans toward the viewer's upper right are removed from every outer shell (Kepler's open shells)
cutdir = np.array([0.55, 0.35, 0.76]); cutdir /= np.linalg.norm(cutdir)
render(S, '../kepler-nest.png', view(-68, 24), dist=6.0, cut=(cutdir, 0.05, 0.16))
print('ok')
