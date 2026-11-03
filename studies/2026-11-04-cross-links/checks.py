from math import sqrt
p=(1+sqrt(5))/2
# 76 -> 91: 600-cell R=1, edge e=1/phi; Lemma 1(a) mu = R^2 - x e^2/2
e2=1/p**2; cos=1-e2/2
print('trunc600 x=1/3', 1-e2/6, (9+sqrt(5))/12)
l=3/5; print('bitrunc l=3/5', (1-l)*(1+cos)/2 + l*(1+2*cos)/3, (11+3*sqrt(5))/20)
r2=(7+3*sqrt(5))/16; f2=r2*(1/(p**2*sqrt(2)))**2; t=(5-sqrt(5))/10
print('trunc120 t', r2/(1-t*f2/(2*r2)), (15+8*sqrt(5))/38)
# rock salt lane = 24-cell vertex-first slice: lambda=1-2h; chamfered cube equal edges
h=(2*sqrt(3)-3)/2; print('chamfer h',h,'square edge',2*h,'hex edge',sqrt(3)*(0.5-h),'lambda',1-2*h,4-2*sqrt(3))
# CsCl lane (1,3): cube edge 2 cut at edge fraction x <-> lambda = 3-4x ; golden cut cube x_G,x_L
xG=p/(sqrt(2)+2*p); xL=1/(p*sqrt(2)+2); print('GCC lambdas', 3-4*xG, 3-4*xL)
# #54 Theorem B heights vs #90 mu: mu-1 = x/(1+x); Icosaxes mu=phi -> height 1/phi
print('Icosaxes height', p-1, 1/p)
# 43/80/91 constants (R/r)^2
import math
for name,(pp,q) in {'T':(3,3),'C':(4,3),'D':(5,3)}.items(): print(name, (math.tan(math.pi/pp)*math.tan(math.pi/q))**2)
print('15-6sqrt5',15-6*sqrt(5))
# 92: cube edge 1/sqrt2 minus inscribed tetra (edge 1): corner piece lateral edges
print('corner legs',1/sqrt(2),'O pyramid lateral',sqrt(2)/2, 'volumes cube',(1/sqrt(2))**3,'4T+4O',4*sqrt(2)/48+4*sqrt(2)/24)
