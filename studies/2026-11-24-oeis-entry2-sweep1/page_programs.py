"""Run every program printed on the two working pages exactly as printed; compare with the data lines."""
import subprocess, cypari2
pari = cypari2.Pari()
b1 = [int(l.split()[1]) for l in open('../../papers/oeis-submissions/working/b-sweep1-pyrochlore.txt')]
b2 = [int(l.split()[1]) for l in open('../../papers/oeis-submissions/working/b-entry2-4H.txt')]
PY1 = '''from math import comb
def domb(m):  # A002895
    return sum(comb(m,k)**2*comb(2*k,k)*comb(2*m-2*k,m-k) for k in range(m+1))
def a(n):
    return (sum(comb(n,2*i)*2**(n-2*i)*domb(i) for i in range(n//2+1)) + (-2)**n)//2
print([a(n) for n in range(26)])'''
out = subprocess.run(['python3', '-c', PY1], capture_output=True, text=True).stdout.strip()
print('sweep1 Python:', eval(out) == b1[:26])
P1a = ['D(m)=sum(k=0,m,binomial(m,k)^2*binomial(2*k,k)*binomial(2*m-2*k,m-k))',
       'a(n)=(sum(i=0,n\\2,binomial(n,2*i)*2^(n-2*i)*D(i))+(-2)^n)/2', 'vector(26,n,a(n-1))']
for s in P1a: r = pari(s)
print('sweep1 PARI (a):', [int(t) for t in r] == b1[:26])
P1b = 'my(N=25,G=sum(m=0,N\\2,sum(k=0,m,binomial(m,k)^2*binomial(2*k,k)*binomial(2*m-2*k,m-k))*x^(2*m))+O(x^(N+1))); Vec((subst(G,x,x/(1-2*x))/(1-2*x)+1/(1+2*x))/2)'
print('sweep1 PARI (b), g.f.:', [int(t) for t in pari(P1b)] == b1[:26])
P2 = 'Vec((1+2*x+5*x^2+4*x^3+6*x^4+6*x^5+6*x^6+4*x^7+5*x^8+2*x^9+x^10)/((1-x)^2*(1-x^8))+O(x^58))'
print('entry2 PARI Vec(g.f.):', [int(t) for t in pari(P2)] == b2[:58])
out = subprocess.run(['python3', 'entry2_prog_as_written.py', '57'], capture_output=True, text=True).stdout.strip()
print('entry2 Python (ENTRIES program as written, last line print(coordseq("ABAC",1,0,57))):', eval(out) == b2[:58])
