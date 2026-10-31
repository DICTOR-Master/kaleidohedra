# Camera spec for a model without a photo (e.g. the h-tile): model stands on the table as built (lowest point on z = 0),
# camera looks at its centre from elevation/azimuth, distance chosen so the bounding sphere fills `fill` of the frame width.
# Usage: ~/geom/bin/python mkcam.py model.obj out.json [elev_deg az_deg lens_mm fill]
import sys, json, math
import numpy as np
objp, outp = sys.argv[1:3]
el, az, lens, fill = (list(map(float, sys.argv[3:7])) + [30, -60, 50, 0.8][len(sys.argv[3:7]):])
V = np.array([[float(x) for x in l.split()[1:4]] for l in open(objp) if l.startswith('v ')])
M = np.eye(4); M[:3, 3] = [-V[:, 0].mean(), -V[:, 1].mean(), -V[:, 2].min()]
W = V + M[:3, 3]; c = np.array([0, 0, W[:, 2].max() / 2]); R = np.linalg.norm(W - c, axis=1).max()
half = math.atan(18 / lens); d = R / math.sin(half * fill)
e, a = math.radians(el), math.radians(az)
C = c + d * np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
z = (C - c) / np.linalg.norm(C - c); x = np.cross([0, 0, 1], z); x /= np.linalg.norm(x); y = np.cross(z, x)
cam = np.eye(4); cam[:3, 0], cam[:3, 1], cam[:3, 2], cam[:3, 3] = x, y, z, C
json.dump(dict(M_obj=M.tolist(), cam=cam.tolist(), lens_mm=lens), open(outp, 'w'), indent=1)
print(outp, 'distance %.3f m' % d)
