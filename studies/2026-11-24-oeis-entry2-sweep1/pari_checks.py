"""Run the PARI programs offered on the working pages (via cypari2, PARI/GP 2.19) line by line, as gp would, and print the last result."""
import cypari2; pari = cypari2.Pari()
progs = {
 'sweep1_formula': ['D(m)=sum(k=0,m,binomial(m,k)^2*binomial(2*k,k)*binomial(2*m-2*k,m-k))',
                    'a(n)=(sum(i=0,n\\2,binomial(n,2*i)*2^(n-2*i)*D(i))+(-2)^n)/2',
                    'vector(41,n,a(n-1))'],
 'sweep1_gf': ['D(m)=sum(k=0,m,binomial(m,k)^2*binomial(2*k,k)*binomial(2*m-2*k,m-k))',
               'G=sum(m=0,20,D(m)*x^(2*m))+O(x^41)',
               'Vec((subst(G,x,x/(1-2*x))/(1-2*x)+1/(1+2*x))/2)'],
 'entry2_gf': ['Vec((1+2*x+5*x^2+4*x^3+6*x^4+6*x^5+6*x^6+4*x^7+5*x^8+2*x^9+x^10)/((1-x)^2*(1-x^8))+O(x^201))'],
}
for k, lines in progs.items():
    for s in lines: r = pari(s)
    print(k + ':', ','.join(str(t) for t in r))
