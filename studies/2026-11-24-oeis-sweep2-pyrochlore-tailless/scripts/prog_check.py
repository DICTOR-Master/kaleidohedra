# The Python program proposed for %o, run as written; its output must equal the direct count.
from math import comb
from fractions import Fraction
def domb(m):  # A002895
    return sum(comb(m,k)**2*comb(2*k,k)*comb(2*m-2*k,m-k) for k in range(m+1))
def w(n):  # closed n-step walks per pyrochlore site
    return (sum(comb(n,2*i)*2**(n-2*i)*domb(i) for i in range(n//2+1)) + (-2)**n)//2
def loops(W, q):  # Ihara-Bass per vertex of a (q+1)-regular net; W[i] = closed i-step walks
    M = len(W)-1; c = [Fraction(0)]*(M+1)
    for k in range(1, M//2+1): c[2*k] += Fraction(q-1, 2*k)
    for j in range(1, M+1):
        for i in range(j+1):
            if 2*j-i <= M: c[2*j-i] += Fraction(comb(j,i)*W[i]*(-q)**(j-i), j)
    return [int(m*c[m]) for m in range(1, M+1)]   # lengths 1..M
print(loops([w(i) for i in range(41)], 5))
