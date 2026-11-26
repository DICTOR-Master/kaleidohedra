# Permutohedron faces in Lean, on TauCeti (step 3 of the restructured Vacuus entry; 26 Nov 2026)
DICTO: "yes start step 3 on TauCeti". Lean v4.37.0-rc1; dependency TauCeti (Apache-2.0) at the commit pinned in lakefile.toml,
whose PermutationOrbit.lean formalizes Rado's theorem (credited; prior-formalisation search in
studies/2026-11-25-lean-vacuus-resonus/FABLE-REVIEW-2026-11-26.md). Built on the compute host (lake env lean; log logs-facets-build.log).

## Step 3a: DONE (compiles, no sorry)
PermFaces/Facets.lean: `P n` = convex hull of the rearrangements of (n, ..., 1);
- `sum_le_prefixSum_of_antitone`: for antitone v, any k coordinates sum to at most the first k (swap argument);
- `sum_le_top`: every point of P n has sum over S at most top |S| (facet inequality);
- `exists_top`: a vertex attains it (a permutation carrying the first |S| positions onto S, via Equiv.subtypeCongr);
- `facet_isExposed`: {x in P n | sum over S = top |S|} is an exposed face of P n.
## Next: step 3b
vectorSpan of the facet = {v | sum over S = 0 and sum over the complement = 0}, finrank n - 2 (for nonempty proper S, n >= 2);
then ridges (S1 strictly inside S2): exposed, finrank n - 3.
