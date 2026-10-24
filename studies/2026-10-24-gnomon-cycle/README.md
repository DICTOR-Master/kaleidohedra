# Gnomon rule, golden cycle (DICTO 2026-10-24)

Idea: DICTO, from Júlia Pimentel's square-root method ((n+1)² = n² + n + (n+1)): look at what each step of a cycle adds.
Float survey of the 12 stations (app data, 6 decimals): no single rule; step ratios 1.01–3.23.
Exact (gnomon_exact.py, from the Progenitors study volumes): the cycle opens by doubling (Cleo star = 2·I) and closes by φ (I·φ³ = φ·M, M = φ⁸·I).
Middle steps: not identified (float precision too low).

Exact gnomon table (gnomon_table.py, from the Progenitors exact layer volumes): clean landmarks: Cleo star = 2·I; RT = (81/φ²)·I (3⁴/φ², new); M = φ⁸·I; I·φ³ = φ⁹·I. D′, ID, OG, TI, H are golden numbers without a neat form; rTI and the hull jtI have no exact volume in the study.

All twelve stations exact (gnomon_all12.py → gnomon-all12.txt, ALL PASS; run on dicto-big-brother): the two missing stations now exact —
rTI (core) = −15/2 + (73/8)√5 = (183/8 + 39√5/40)·I; jtI (hull) = −3465/38 + (900/19)√5 = (3321/38 − 999√5/38)·I (PD corners computed exactly as poles of TI's faces in ρ² = 9/4; the method reproduces the table's TI, H, RT, I·φ³ exactly).
What each step adds (Júlia's gnomon), as a multiple of I: CLEAN — Cleo star − I = I; TI − rTI = (3/4)/φ²·I (new); H − TI = 18/φ⁴·I (new; the 20 Shields); I·φ³ − M = φ⁷·I. The other seven steps have no neat form.
Clean ratios: star = 2I, RT = 81I/φ², M = φ⁸I, I·φ³ = φ⁹I, so M/RT = φ¹⁰/81. jtI shares the factor 19 in its denominator with OG (456 = 24·19): jtI is the hull of the H–OG compound.
