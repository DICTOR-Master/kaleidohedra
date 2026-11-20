# Blind pre-score (reusable step)

An estimate of Palomar's `literature_notability` review step, made before building an entry and once more on the
finished entry. The production reviewer cannot be run outside Palomar's broker, so two fresh scorers replay the step
from the registry's own policy text. Used for Yantra (16 Nov 2026), Dehn (19 Nov) and Grünbaum k = 10 (20 Nov). Yantra
and the Dehn Canon, 4 / 4 in every blind score, were both registered (Dehn: review outcome `neutral`).

## When

1. **Before building**: score the planned result (one candidate per possible scope, e.g. D1 / D2, G1 / G2). Build only
   a candidate whose notability clears the floor in both scores. A wider scope that does not raise notability is left
   out of the entry (Dehn D2, Grünbaum G2).
2. **Once after building**: score the finished entry with the real Challenge quoted in full and the literature
   corrected (D1b, G1b). Not more often: each run costs two agents, and the score moves by about one point between runs.

## Steps

1. **Study folder** `studies/<date>-palomar-<subject>/blind/` with `policy/`, `inputs/`, `raw/`.
2. **Policy**: copy `policy/` from this kit unchanged. The four files are CONTRIBUTING §1 and §7, prompt 04 and
   rubric.json from PalomarPolicy @ 28bd48b (the policy commit of the Dehn review record). Check with `cmp` that they are
   byte-identical to the kit's copy. If Palomar's policy commit changes, refresh all four from the new commit and note it.
3. **Input**: write `inputs/<CAND>-<subject>.md` from `input-template.md`: neutral abstract, sources with exact
   citations and what was read, prior formalizations searched, the author's prior work, what is claimed, the Challenge
   verbatim, and "Statement to score". DICTO is never named ("the submitter"); the submitter's own names for objects are
   neutralized and the input says so. Disclose every earlier appearance found and every source not read.
4. **Two scorers in parallel**: two fresh general-purpose agents, each given only `scorer-prompt.md` with POLICY, INPUT
   and CAND filled in (absolute paths). The same prompt for both; no notes, no earlier scores, no studies. Web reading
   only; they write no files and start no background work.
5. **Record**: save each hand-back verbatim as `raw/blind-A-<CAND>.json` and `raw/blind-B-<CAND>.json` (exactly the
   JSON the scorer returned; never edited or summarised).
6. **Tally**: `python3 -I <kit>/prescore/tally.py <study>/blind/raw` prints the table and the floor verdict.
7. **Judge** (in the study README, my own judgement): the table; the reasons both scorers give; "Where they are right"
   (each with the action it needs) and "Where they are mistaken or overstate"; check every citation a scorer raises
   against the source itself; final estimate with the risk; LEADS.

## The floor

Palomar's rubric minimum is **4** for notability (mandatory) and for literature. Notability below 4 is outcome
`failure` and blocks registration. Literature 3 with outcome `warning` does not block, but a scorer's literature
finding (a missed earlier source, an unsupported priority claim) must be fixed in `formalization.yaml` before
submission and the entry re-scored once (Grünbaum: G1 4 / 3 with the Hall 2016 finding, then G1b 4 / 4 after citing it).
4 at the floor is the honest estimate when both scorers give 4; never claim 5 unless both give it. The pattern so far:
4 needs a question or theorem that someone else put in print (Kulaichev's uniqueness question, Hilbert's third problem,
Grünbaum's zone question); questions DICTO posed himself scored 2 to 3.
