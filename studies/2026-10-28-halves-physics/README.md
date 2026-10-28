# Halves and Swap Rule: the physics (placeholder "Hexagonality Law")
DICTO's idea 10-28: the quanta/Planck angle as ground for the rule of halves and the Swap Rule.
Status 10-28: survey done, finding 1 to be checked exactly.

1. Swap Rule = no coupling term in the Ising (ANNNI) language of polytypes (Jagodzinski h/k = our h/c).
   V(xy) = f(x)+g(y) iff V(ch)+V(hc)=V(cc)+V(hh). Corollary to check: total volume of each KIND of piece
   (octahedral, tetrahedral, ...) is linear in hexagonality (fraction of h layers), whatever the order.
   Physics counterpart: Choyke-Hamilton-Patrick (1964) band gap ~ linear in hexagonality (SiC);
   lattice constants linear in hexagonality (ECS abstract, Be/Mg/Pd/Pt); Heine ANNNI (Cheng-Needs-Heine 1988).
2. Causal dynamical triangulations: spacetime built in slabs between slices from (4,1) and (3,2) simplices,
   each typed by its two neighbouring slices, like our pieces between layers.
3. Regge calculus universes on the 600-cell: De Felice-Fabri 2001; Tsuda-Fujiwara 2020 (White/Red Queen link).

Sources checked: ask-library (5 queries: polytype ANNNI; LQG polyhedra; CDT layers; Voronoi polytypes; Regge):
Rodriguez-Horta et al 2017; Ganesh-Nasr 2023; Bianchi-Dona-Speziale 2011; Rovelli-Smolin 1995; Rovelli 1998;
Surya 2019; Tsuda-Fujiwara 2020; De Felice-Fabri 2001; Blatov 2004. Web: arXiv cond-mat/9709191; arXiv 2306.17756
(Ising-type additivity model for polytype band gaps); Pitt Choyke tribute; arXiv 1404.3588; PRB 49 7564;
ECS 236 Paper124142; arXiv 2401.09399, 1111.6938, 1704.00577 (CDT); arXiv 1508.05937, 2303.01761 (Voronoi fcc/hcp).

## Result 10-28: the Hexagonality Law (placeholder name) — exact check PASSED
Script scripts/hexlaw.py (+ hexlaw_cdi2.py), on the exact weight walks of Splash Rules run 2 (dbb ~/kres-tmp/splash2/raw),
every close-packed stacking up to 6 layers, every lam-window, every role:
total volume of a role over one period = n_c·alpha(lam) + n_h·beta(lam), alpha from ABC, beta from AC, exact (sympy).
- pyrochlore #60 96/96; rock salt/NiAs 80/80; zinc blende (MU ±1/20, ±1/10) 192+176+176+144; Laves 120/120.
- CdCl2/CdI2: two alternating kinds of layer (filled/empty); linear in the hexagonality of EACH kind of layer
  (4 unknowns per role, 6 words) consistent 80/80. (Single hexagonality fails only for ACBC, ACBCAC, whose h layers are all one kind.)
- Total 1230 + 80 exact tests, 0 failures.
- Holds even where the rule of halves does not (zinc blende empty holes; the Laves foot atom M0, which reads 3 layer types).
- Proof where pieces read only the two layers round their gap: Swap Rule <=> V(xy)=f(x)+g(y) => sum telescopes to counts.
  Wider-context roles: exact computation only (words up to 6 layers), proof open.
Physics counterpart: linear-in-hexagonality laws of polytypes (Choyke-Hamilton-Patrick 1964 band gap; lattice constants).
