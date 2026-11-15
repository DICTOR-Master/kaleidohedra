# Palomar pre-score: #102 v6, the polygon laws (15 November 2026)

**Verdict.**
- **Two blind reviewers gave the bare statement notability 4.** That applies to (a) the results as they stand and to (b) the same results framed against an outside question. The floor is 4. Both reviewers said it "just" clears the floor, and both marked literature 3 (outcome `warning`).
- **The 4 rests on Theorem 5 alone.** Per theorem, reviewer (a) scored Theorem A at 3, Theorem B at 3 and Theorem 5 at 4.
- **So a real submission is not yet a safe 4, for three reasons.**
  1. The margin is zero, and Palomar's own notes allow one point of run-to-run noise.
  2. The earlier full replay of the Loop Equality entry scored 3.
  3. The part that carries the 4, Theorem 5 at lengths 18 and 20, rests on finite tables that are hard to check in the Lean kernel. The part that is easy to formalise, Theorem A, scores 3.
- **No question someone else stated in print is settled by these results.** The nearest is the long-standing question whether ice Ih and Ic have equal residual entropy (quoted below). The theorems do not decide it, and the reviewers judged it a neighbouring question.
- **What would make 4 robust (new mathematics):** Theorem A carries over to fcc/hcp sphere packings (Statement C, checked by reviewer (c)). Add a local formula that gives exactly where, and by how much, hcp and fcc self-avoiding walk counts first differ: that version scored 4/4 (variant c-ii). As written, without that formula, it scored 3.
- **Literature fixes needed in any case:**
  - Herrero 2014: self-avoiding walks on ice Ih and Ic.
  - Nagle 1966 and Onsager: the ice cycle series and W_hex ≥ W_cub.
  - Conway–Sloane 1997: Barlow coordination sequences.
  - Schram–Barkema–Bisseling–Clisby 2017: the fcc SAW series.

**Status:** estimate only. The blind replay ran the literature-and-notability step only, on bare statements; it was not a full seven-step review of a package. The reviewers were Claude agents, not production `codex:gpt-6-sol`. Nothing was built or submitted.

## Method

As in study 2026-11-15-palomar-permutohedron.
- **Inputs.** Three fresh agents (Claude Opus 5.5) were each given only PalomarPolicy @ 28bd48b (CONTRIBUTING §1 and §7, rubric.json, prompt 04), read from GitHub, plus one input file (`blind/inputs/`).
- **Isolation.** None of them saw our notes or earlier scores.
- **Output.** Each searched the web on its own and wrote prompt 04's JSON (`blind/blind-*.json`).

## Scores

| Framing | Input | Notability | Literature | Outcome |
|---|---|---|---|---|
| (a) As it stands: Theorems A, B, 5 | `a-as-stands.md` | **4** (A 3, B 3, Thm 5 4) | 3 | warning |
| (b) Framed against Xu–Lin–Zhang (Ih/Ic entropy) and Benito et al. (hcp/fcc SAWs) | `b-framed.md` | **4** | 3 | warning |
| (c-i) Plus Statement C (twist on sphere packings), local SAW formula not done | `c-strongest.md` | 3 | 4 | failure |
| (c-ii) Hypothetical: plus the exact first hcp/fcc SAW difference by a local formula | `c-strongest.md` | **4** | 4 | neutral |

**Reasons (from the replies).**
- **(a)** Theorem 5 is concrete, and it has an audience that can be named: people who enumerate lattice polygons and self-avoiding walks, and people who study ring statistics of polytypes and stacking-disordered ice. A and B are tools.
  - Literature 3: the closest comparison is missing. Herrero, *Chem. Phys.* 439 (2014) 49, arXiv:1402.5036, counts self-avoiding walks on ice Ih and Ic. According to reviewer (a), Table II agrees at n = 5 and 10 (324; 70188) and differs at n = 15 (14776128 against 14774652). So open walks see the stacking before polygons do.
  - We confirmed the paper and its subject (SAWs on eight ice polymorphs to n = 27). We did not open Table II ourselves.
- **(b)** Same audience; the framing "partly holds". The outside questions are real but are neighbours of what is proved.
  - Literature 3: Nagle 1966 (*J. Math. Phys.* 7, 1484) is the real bridge. His cycle-corrected coefficients for hexagonal and cubic ice agree to n = 10 and then separate; this is from a secondary summary in Ferreyra–Rossini–Grigera, *PRE* 98 (2018) 042146. Onsager's W_hex ≥ W_cub is also uncited.
  - The claim to be "the first exact, structural account" must be narrowed.
- **(c-i)** Statement C is correct. One caveat: if v lies above the gap, twist the lower side instead, which flips letter k + 1. C itself is a short reduction with no new count, so notability is 3.
- **(c-ii)** A proved, exact first hcp/fcc separation would answer what Benito et al. treated only by enumeration and an informal bending/torsion argument. That gives notability 4. It is not 5: the audience is narrow, and it does not decide Sh = Sc.

## 1. Literature: questions others stated in print (free sources)

**Found, quoted exactly:**
- **Xu, Lin, Zhang, arXiv:2511.22477 v3 (June 2026), Introduction:** "Despite the long history of studies on ice-type models, one of the long-standing unsolved problems concerns whether the residual entropy of hexagonal ice (Sh) equals that of cubic ice (Sc)." Abstract: "While analytical studies have established the inequality Sh ≥ Sc, numerical investigations suggest that the two values are very close."
  - This is a stated open question about stacking and lattice statistics on exactly our network.
  - #102 v6 does not decide it. Simple cycles through a site are not the ice-rule count.
  - #102 v5's ice series (first difference at 16 bonds) also differs in kind, because graded coefficients that differ do not imply Sh ≠ Sc.
- **Benito, Urrutia, Karayiannis, Laso, *Crystals* 13 (2023) 1316, abstract** (via OpenAlex; the MDPI and preprints.org full texts returned 403): "In both cases, once a critical number of steps is reached, one of the crystals shows a higher number of SAWs compatible with its geometry. We explain the observed trends in terms of the bending and torsion angles as imposed by the geometric constraints of the crystal lattice."
  - This is an observation with a heuristic explanation. It is not a stated open question.
  - "Counts agree up to N = 5" comes from a search summary only and is unconfirmed.

**Not found:** any sentence of the form "at what length do hcp/fcc (or diamond/lonsdaleite) walk or polygon counts first differ?" or "explain the near-equality of SAW counts on hcp and fcc".

**Precedent for the audience:** Conway–Sloane, *Low-dimensional lattices VII: coordination sequences* (Proc. R. Soc. A 1997) proved O'Keeffe's 1995 conjecture that among Barlow packings hcp has the largest coordination sequences and fcc the smallest. A stated stacking-versus-counting conjecture did get settled in print.

**Sources checked:**
- arXiv:2511.22477 (full text);
- OpenAlex records for Benito et al. 2023 (abstract and all 93 references by title);
- the search summaries of the MDPI and preprints.org pages;
- arXiv:1402.5036 (Herrero 2014, abstract);
- arXiv:cond-mat/9810287 (Mau–Huse 1999, stacking entropy of hard spheres);
- arXiv:cond-mat/0506066 (Koch–Radin–Sadun 2005);
- arXiv:1403.1784 (Elser 2014);
- arXiv:1406.5929 and arXiv:1307.3950 (Herrero–Ramírez);
- arXiv:2404.13897 (transfer matrices, ice);
- arXiv:1703.09340 (Schram et al., fcc/bcc SAWs);
- Slade's lace-expansion notes;
- arXiv:2208.06744;
- the Wikipedia article on coordination sequences;
- the scilit record of Conway–Sloane VII.

The reviewers' own lists are in the JSON files. Hard-sphere entropy papers (Mau–Huse, Koch–Radin–Sadun, Bolhuis–Frenkel) ask which packing has more entropy. They state no question about walk or cycle counts. No source found treats polygons on lonsdaleite or other polytypes.

**Queries:**
1. SAWs hcp/fcc Benito 2023
2. hcp SAW series Domb, Sykes, Lin
3. hcp/fcc "same number" "up to N"
4. Mau–Huse stacking entropy series
5. Koch–Radin–Sadun
6. Ih/Ic residual entropy, Nagle, Herrero–Ramírez
7. coordination sequences of polytypes, O'Keeffe
8. Tindall–Sommers–Kappen ice series
9. SAWs/SAPs on hexagonal diamond, lonsdaleite, wurtzite

## 2. Statement C (Theorem A on sphere packings)

- **The twist.** In the contact graph of a Barlow packing, cut between layers k and k + 1. Take a walk or polygon with crossing edges (x1, y1), (x2, y2), where x_i is in layer k.
  - The half-turn g about (x1 + x2)/2 fixes the coset of layer k and swaps the other two. Twisting the far side by g flips only letter k (as in Lemma 1 of the bijection study).
  - g(y1) = x1 + x2 − y1 is a neighbour of x2, and g(y2) is a neighbour of x1. So the twisted edges are valid and the cycle closes.
  - A walk that crosses once uses the half-turn about x1.
- **The bijection.** The map is an involution and keeps length and every crossing count.
- **Corollary.** The walks or polygons that cross every gap at most twice are equinumerous on fcc, hcp and every Barlow packing, at every length.
- **Status:** our proof sketch, checked by reasoning by reviewer (c). It has not been checked by computer.
- **Not done:** a Theorem B for SAWs. Walks of three steps already cross one gap three times, so the first hcp/fcc difference needs that formula.

## What would reach 4 robustly

1. **The hcp/fcc SAW law (best route).** Corollary C plus a local Theorem-B formula for walks that cross some gap three or more times. Give the exact first N where hcp and fcc SAW counts differ and the exact difference. Cross-check by an independent count and against Benito et al.'s tables. Blind score 4/4.
2. **Literature in the #102 account:**
   - Herrero 2014: SAWs on Ih and Ic differ by n = 15 while polygons wait until 18. Reviewer (a) calls that contrast "the strongest case for interest".
   - Nagle 1966 and Onsager.
   - Conway–Sloane 1997.
   - Narrow the "first" claim.
3. **The Lean scope must match the claim.** Theorem A (about 1.4–2.5k lines, no tables) scores 3 on its own. Theorem 5 at l = 18 is at the edge of kernel `decide`, and l = 20 is probably beyond it. A Challenge that leaves Theorem 5 to computed tables would lose the part that scored 4.
4. **Not enough:** packaging the as-stands statement and hoping for the marginal 4. Two Claude reviewers gave 4, but the margin is zero and the production model differs.

## Files

- `blind/inputs/common.md`, `a-as-stands.md`, `b-framed.md`, `c-strongest.md`: what the reviewers saw.
- `blind/blind-a-as-stands.json`, `blind-b-framed.json`, `blind-c-strongest.json`: their replies (prompt 04 shape, with `what_would_reach_4`, `per_theorem`, `does_framing_hold`, `variants` and `statement_C_check`).
