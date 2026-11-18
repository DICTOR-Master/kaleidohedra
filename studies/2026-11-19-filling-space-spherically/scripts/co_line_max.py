# Where do the two scores peak on the cube-octahedron line? (IQ peak at mu = sqrt3 per 2026-11-18; Mahler peak: here)
src = open('ladder2.py').read(); exec(src[:src.index('\nrows = [')])
from scipy.optimize import minimize_scalar as m
r = m(lambda u: -mahler(co(u)), bounds=(1.2, 2.8), method='bounded', options={'xatol': 1e-10})
q = m(lambda u: -iq(co(u)), bounds=(1.2, 2.8), method='bounded', options={'xatol': 1e-10})
print('Mahler peak mu = %.8f value %.6f | IQ peak mu = %.8f value %.6f | sqrt3 = %.8f' % (r.x, -r.fun, q.x, -q.fun, 3**.5))
