# G1 and E1 exactly (DICTO 10 Nov 2026: "I meant computing their exact forms")
R1 is already exact (Theorem 2 of #103: every coordinate a fraction).

## G1 (Cleo-Octangula, u = 2/phi^2 = 3 - sqrt5, v = 1/sqrt2, with (b) and (d)) - EXACT
g1_exact.py (dicto-big-brother, 30 s; log g1-pilot.log, FINAL ok). Natural coordinates: t1's corner (t/(1+t^2), t^2/(1+t^2));
H1(t, S) degrees (10, 3), bindu D(t, S) degrees (24, 4); Res_S degree 110 in t over Q(sqrt2, sqrt5); norm to Q degree 440 =
1^8 2^6 2^6 2^96 12^2 20^2 152. G1's t is a root of the irreducible factor of degree 152 (153 terms, not even, coefficients up
to 65 digits, 30 real roots), residual 7.3e-49 at the stored 40 digits: g1-minpoly-t.txt. b1 = t^2/(1+t^2).
Not yet: certificate (root isolation + interval Newton as in the #103 audit); minimal polynomial of S.

## E1 (most even) - why no exact form yet
E1 is fixed by an optimum (least spread of the 43 areas over the four free parameters), not by incidences. Checked: it sits
on no boundary (no near-concurrency beyond Huet's conditions), so no geometric equation pins it. Its exact form would be the
solution of the four gradient equations of spread/mean, with every area in Q(sqrt Delta): far larger than any elimination done.
Stored only to double precision (even.json, 16 digits; Huet residual 5.9e-17, as #103 says). Feasible next: refine E1 to 50
digits as a true critical point and certify it a local minimum (Hessian).
