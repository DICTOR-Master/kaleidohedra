# Square-triangle row tilings decorated by the Frank-Kasper rule (Sullivan; Sadoc and Mosseri 2016, Z16-free decoration).
# A word over {S, T}: S = a row of unit squares, T = a row of unit triangles (horizontal period 1).
# Secondary layers z = 1/4, 3/4: tiling vertices. Primary layers z = 0, 1/2:
#   edge midpoints: 'dark' edges (direction a multiple of 60 deg) at z = 1/2, 'light' edges (90 deg) at z = 0;
#   squares: two atoms 1/4 inside from the midpoints of the light edges at z = 1/2 and of the dark edges at z = 0;
#   triangles (all dark in row tilings): centre at z = 0.
import numpy as np
R3 = np.sqrt(3.0)
def build(word):
    if word.count('T') % 2: word = word * 2          # vertex offset must close up
    pts, y, off = [], 0.0, 0.0
    for r in word:
        h = 1.0 if r == 'S' else R3 / 2
        x0 = off % 1.0
        pts += [(x0, y, .25), (x0, y, .75)]                      # vertices on the lower line of the row
        if r == 'S':
            pts += [(x0 + .5, y, .5)]                             # horizontal (dark) edge midpoint, lower edge
            pts += [(x0, y + .5, 0.0)]                            # vertical (light) edge midpoint
            pts += [(x0 + .25, y + .5, .5), (x0 + .75, y + .5, .5)]   # 1/4 in from the two vertical edges, z = 1/2
            pts += [(x0 + .5, y + .25, 0.0), (x0 + .5, y + .75, 0.0)] # 1/4 in from the two horizontal edges, z = 0
        else:
            pts += [(x0 + .5, y, .5)]                             # horizontal edge midpoint (lower)
            pts += [(x0 + .25, y + h / 2, .5), (x0 + .75, y + h / 2, .5)]   # the two slanted edges
            pts += [(x0 + .5, y + h / 3, 0.0), (x0 + 1.0, y + 2 * h / 3, 0.0)]  # up and down triangle centres
            off += .5
        y += h
    L = np.array([[1.0, 0, 0], [0, y, 0], [0, 0, 1.0]])
    frac = np.array([[(p[0] % 1.0), p[1] / y % 1.0, p[2] % 1.0] for p in pts])
    return L, frac, word
