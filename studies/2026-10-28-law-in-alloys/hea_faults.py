# Fe-Mn / high-entropy step (DICTO 10-28). The standard fault model of TRIP/TWIP steels and high-entropy alloys is Olson and Cohen's:
# gamma_ISF = 2 rho dG(fcc->hcp) + 2 sigma (intrinsic fault = two-layer hcp embryo). In the ANNNI form used in #68 (relative to 3C):
# X(2H) = 2(J1+J3) per layer, ISF = 4(J1+J2+J3), ESF = 4(J1+2J2+2J3), TSF = 2(J1+2J2+3J3), so rho dG = 2(J1+J3) and
#   2 sigma = ISF - 2 rho dG = 4 J2   (sigma = 2 J2),   ESF - ISF = 4(J2+J3).
# The Hexagonality Law (two-layer roles) <=> J2 = J3 = 0 <=> sigma = 0 and ISF = ESF = 2 TSF = 2 rho dG.
# Data: Ding, Yu, Asta, Ritchie, arXiv 1806.00718 (PNAS 2018), DFT for CrCoNi, mean over 108 faults per state: random CH_0
# ISF -42.9, ESF -27.8; most ordered CH_F ISF 30.0, ESF 66 mJ/m^2; ISF at dE(fcc->hcp) = 0 about 18 mJ/m^2 (= 2 sigma, their Fig. 5D).
d = {'CH_0 (random)': (-42.9, -27.8), 'CH_F (most ordered)': (30.0, 66.0)}
two_sigma = 18.0
J2 = two_sigma / 4
print(f'2 sigma = 4 J2 = {two_sigma} mJ/m^2  ->  J2 = {J2:.1f} mJ/m^2 (one fit over all states)')
for k, (isf, esf) in d.items():
    j23 = (esf - isf) / 4; J3 = j23 - J2; J1 = isf / 4 - J2 - J3
    rhoDG = 2 * (J1 + J3); tsf = 2 * (J1 + 2*J2 + 3*J3)
    print(f'{k:22s} ISF {isf:6.1f} ESF {esf:6.1f} | J2+J3 = {j23:5.2f}, J3 = {J3:5.2f}, J1 = {J1:6.2f} | rho dG = {rhoDG:6.1f}'
          f' | law-only prediction ESF = ISF: off by {esf - isf:5.1f} mJ/m^2; predicted TSF {tsf:6.1f}')
