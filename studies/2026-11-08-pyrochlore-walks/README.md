# Pyrochlore walks (2026-11-08)
walks.py: closed walks and tailless non-backtracking closed walks per site on the pyrochlore network (spin ice, #74), lengths to 30,
counted directly on the network; checked by the Ihara-Bass formula (6-regular, q = 5) for every length and against the Loop
Equality study's data (first 10 terms). data-walks-30.txt, FINAL ok (run on compute-host). Neither sequence is in the OEIS
(matcher, 8 Nov 2026): candidate entries after A400949 is approved.
Side result (gap #43): the corner counts along the chain of DICTO's growth rule T from the OG (92, 180, 212, 270, 452, 642, 1220,
1352, 2240; studies/2026-10-30-star-cores-exact/data/study4.json) follow no linear recurrence and are not in the OEIS: the
octahedral constant 3 has to come from the metric gains, not from counting.
