# Palomar pre-score: the Lean Dehn work (19 November 2026)

**Verdict: D1 (Hilbert's third problem with the set-defined Dehn invariant and the geometric bridge) scores notability 4 / literature 4 from both blind scorers, at the floor. D2 (the complete canon) scores notability 3 (failure) from both. Submit D1, if at all; the canon belongs with it as worked corollaries, not as its own entry. Nothing was submitted; submission only on DICTO's word.**

Method as in studies/2026-11-16-palomar-yantra (copied policy files in blind/policy, byte-identical): neutral blind inputs (blind/inputs/D1-hilbert3-geometric.md, D2-dehn-canon.md) disclosing the prior Lean formalization (FormalBook ch. 10) and the results known on paper; two fresh scorers per candidate, each given only the policy and one input, web read-only; outputs summarised in blind/blind-{A,B}-{D1,D2}.json.

| candidate | scorer A | scorer B |
|---|---|---|
| D1 | 4 / 4, neutral | 4 / 4, neutral |
| D2 | 3 / 4, failure | 3 / 4, failure |

Why D1 holds 4 and not more: the theorem is classical and already formalized in Lean (FormalBook, abstract model); the contribution is the set-level invariant and the bridge FormalBook says it lacks; restricted scope (convex pieces, one tetrahedron model, the cube).
Why D2 fails: nearly all invariants and the angle independence are on paper (Conway–Radin–Sadun; Ogievetsky–Papadopolos); scorer B: β = (π + γ − α)/2, so the joint independence follows from Conway–Radin–Sadun directly (the paper should say so); the solid list is hand-picked; only FUJI is not on paper.

What would raise D1 (both scorers): Hilbert's literal statement (two tetrahedra of equal base and height not scissors congruent); the bridge as headline for finite unions; dehnSet = classical edge sum for every convex polytope; cite Hartshorne (Geometry: Euclid and Beyond, ch. 27), Boltianskii 1978, Sah 1979, Dupont 2001, Benko 2007, Zakharevich; credit Hadwiger/Groemer for the valuation extension; pin the other formalizations' commits; a real Challenge file and Comparator configuration; Sydler's converse (long term).
