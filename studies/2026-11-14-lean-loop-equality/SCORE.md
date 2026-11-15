# Palomar score estimate: Loop Equality entry (15 November 2026)

**Conclusion. Notability 3 out of 5. That is below Palomar's floor of 4, so the outcome would be `rejected`.** The other scores reach 4:
- statement alignment 4;
- definition fidelity 4;
- clarity 4;
- literature 3, which a corrected account should lift to 4.

**The score is not guaranteed. Do not submit this entry as it stands.**

**Status:** estimate only. The production reviewer could not be run (see Method). Nothing was submitted.

## How Palomar scores

These rules come from the sources listed under Method.

- **Production reviewer:** `palomar-review` (PalomarReviewer @ ba9b26c). It runs on Codex CLI 0.147.0 with the model **`gpt-6-sol`** ("Production uses `codex:gpt-6-sol`").
- **What the model reads:** the fixed prompts in PalomarPolicy @ 28bd48b, `prompts/00`–`06` and `materiality.md`, in the order given by `rubric.json`, schema version 10.
- **Steps:**
  1. classification
  2. metadata (clarity, provenance)
  3. statement alignment
  4. definition fidelity (with auditability)
  5. literature and notability
  6. proof account (when present)
  7. synthesis
- **Scores:** each runs from 1 to 5, and the minimum is 4.
- **Mandatory floor:** `mandatory_reject_below_minimum: ["notability"]`. A notability score below 4 forces `rejected`. There is no appeal.
- **Notability anchors** (CONTRIBUTING §7):
  - 2: trivial, routine or lightly repackaged;
  - 3: borderline, where paper-worthiness or a research audience is "not affirmatively established";
  - 4: "plausibly paper-worthy, with a specifically identified credible research audience";
  - 5: unusually consequential.
- **Prompt 04:** "Formal verification, effort, length, and polish do not by themselves establish research interest."
- **Scores are private.** The policy itself notes that the same commit has scored 5 and then 4 on one dimension in two runs. So one point of run-to-run noise is expected.

## Method

1. **The real reviewer cannot be run here.**
   - `palomar-review run --submission ID` reads a submission record from the private `PalomarSubmissionState` repository, which needs Palomar's credentials.
   - It needs a mechanical report from a public verification run.
   - Its production engine goes through Palomar's OpenAI model broker.
   - No API key was sought.
2. **A blind replay was run instead.**
   - A separate Claude agent (Opus 5.5) was given only the pinned policy (CONTRIBUTING.md, rubric.json, every prompt) and the package. It was not given the earlier estimates in LITERATURE.md.
   - It ran all seven steps, searched the web on its own, and returned the JSON each prompt asks for.
   - It is a different model from production (Claude, not gpt-6-sol), run outside the broker. Palomar's own audit (PalomarReviewer `docs/audits/2026-08-20-reviewer/REPORT.md`) found that model tiers disagree on outcome in 2–3 of 5 cases, so read the replay as an estimate.
3. **Own reading.** The rubric was then applied point by point by the packaging agent. It agrees with the replay, and with the estimate of 3–3.5 made earlier in LITERATURE.md.

## Replay result, step by step

| Step | Outcome | Scores |
|---|---|---|
| classification | neutral | classification 4 |
| metadata | neutral | clarity 4, provenance 4 |
| statement alignment | neutral | 4 (all 17 theorems match their prose; m = 1, 2 not vacuous; diamond's reference point is a site) |
| definition fidelity | neutral | definition fidelity 4, auditability 4, trust high (Mathlib-only Challenge) |
| **literature and notability** | **failure** | **notability 3**, literature 3 |
| proof account | neutral | 4 |
| synthesis | **rejected** | (scores copied from the steps above) |

### The reviewer's reasons for notability 3

- The results break down into:
  - the closed-walk equality across stackings: Thorpe 1972 for periodic polytypes, extended to all stackings by locality;
  - a standard identity for walk-regular regular graphs, from the Hashimoto–Bass recursion, that gives the rooted non-backtracking loop count from the closed walks;
  - values computed by the kernel;
  - an instance on the classical Sturmian stacking.
- A research audience exists: ice and polytype lattice statistics, and zeta functions of infinite graphs. But paper-level interest is not established: #102 has not been peer reviewed, and no outside reception is documented.
- It is not 2, because the audience can be named and the explicit per-site formula for every stacking is a clean fact someone could cite. It sits near the 2/3 boundary.

### Literature findings, all accepted and fixed in the package

1. **Wrong "new step".** The README called the bond walk-count lemma (#102 Lemma 2 (b)) "the new step". The formal proof of `loop_count_eq` never uses it: it needs only `W_closed`, the local loop formula and 4-regularity, and `loop_equality` follows from it.
2. **Aperiodicity adds nothing on its own.** A loop of length m sees only a bounded window of layers, and every such window occurs in some periodic polytype.
3. **Missing prior work.** Grigorchuk–Żuk 2004 and Lenz–Pogorzelski–Schmidt 2019, on Ihara zeta functions of infinite graphs, were missing.

The README and `formalization.yaml` now state all three plainly (package commit `26fc584`).

### A mechanical point, also fixed

The replay noticed that source `type` must be one of paper, book, web discussion, folklore, original-proof or other (CONTRIBUTING §3). The draft had used `article` and `web post`; both have been corrected.

## Own reading, point by point

- **Classification, metadata, alignment, fidelity, proof account: 4 each.** No material issue was found. The Challenge is short (363 lines), imports Mathlib only, and every definition carries a docstring. The small-range checks (m ≤ 12, n < 10, positions < 100) are labelled as such. AI authorship is disclosed, and the review status is honest.
- **Literature: 3 before the fixes, 4 likely after them.** The account now names the reduction to Thorpe plus the Hashimoto–Bass reduction and the locality argument, and it cites the infinite-graph zeta work.
- **Notability: 3.**
  - Honest reporting of the reductions makes the "corollary" reading explicit, and that reading is correct.
  - What is new is real but small:
    - the explicit per-site statement for every stacking, including the aperiodic ones;
    - a complete machine-checked proof;
    - the local loop formula stated for infinite graphs.
  - Under anchor 4 an editor would still ask what a paper would add beyond Thorpe 1972 plus one page. A score of 4 cannot be claimed truthfully here.

**Honest outcome: rejected, with notability 3.** The bundled Fibonacci corollary and the general local formula do not change this. The aperiodic case reduces to the periodic one by locality.

## What would raise notability to 4 (new mathematics, not better prose)

In the order of best chance for the effort:

1. **Where the stackings differ.** Find the first length at which the counts of simple rings (or self-avoiding polygons) differ between stackings, with an exact formula for the difference. Better still, prove a consequence for the residual entropy of ice Ic against Ih (Nagle's loop series). This question is open and active (Chen–Ran 2026; Xu–Lin–Zhang 2025). It turns "every stacking is the same" into a sharp boundary between what is the same and what is not, which is a result an editor would recognise.
2. **The full per-site Ihara zeta in closed form.** Formalise the Ihara–Bass identity for all m and Bala's identity for all n. Then draw analytic consequences: the radius of convergence, the exponential growth rate of the loops, and a Ramanujan-type property of the network, valid uniformly over all stackings, aperiodic ones included.
3. **A classification theorem.** Characterise the layered networks (or the graphs in general) whose non-backtracking loop counts are equal at every site. For example: every walk-regular (q+1)-regular graph, and which layer constructions are walk-regular. That would make the result a general theorem, not one family.
4. **Outside evidence.** Peer review of #102, or uptake by experts in polytype physics or infinite-graph zeta functions. Under the anchors this supports "plausibly paper-worthy", but on its own it is unlikely to lift a corollary-level result.

Bundling more corollaries of the same theorem (the sphere packings of #102 Corollary 3) would not help: they are further instances.

## Recommendation

DICTO's condition was "move forward with Palomar, if score guaranteed". The condition is **not met**. Keep the package local, where it is ready and mechanically green, and submit only if one of items 1–3 is proved and added to the entry.
