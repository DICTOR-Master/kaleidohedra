# G1 and E1 exactly (DICTO 10 Nov 2026: "I meant computing their exact forms")
R1 is already exact (Theorem 2 of #103: every coordinate a fraction).

## G1 (Cleo-Octangula, u = 2/phi^2 = 3 - sqrt5, v = 1/sqrt2, with (b) and (d)) - EXACT
g1_exact.py (30 s; log g1-pilot.log, FINAL ok). Natural coordinates: t1's corner (t/(1+t^2), t^2/(1+t^2));
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

## E1 refined (update, same day)
Not free after all: E1 lies on the edge where t4's right leg passes through t5's corner (lines t4 right leg, t5 base, t6 right
leg concurrent: the same meeting as the rhombus threshold u*), to 2e-10 at double precision. e1_refine.py: S from that meeting,
spread minimised over (u, v, Q) by Newton at 90 digits; quadratic convergence (|step| 2.7e-60), Hessian eigenvalues 76.2, 3.61,
1.63e4 (all > 0: a true minimum on the edge). u 0.77774072453700599930520, v 0.74345883945950976367820, Q 0.54155899281283542323132,
S 0.87196163834102841888194, spread/mean 0.614193120241354. Exact form: one incidence + three stationarity equations (open).

## Rhombus threshold u* exactly
threshold_exact.py (33 s): Res_S(G, H1), Res_S(G, C), Res_t (PARI): degree 1928 = ... 8 12^4 180 408. u* is a root of the
irreducible even factor of degree 180 (91 terms, coefficients up to 12 digits, 26 real roots): threshold-minpoly-u.txt.
