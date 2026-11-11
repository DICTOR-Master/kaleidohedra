# AI process notes: paper #102, "Every Site Hears the Same: The Loop Equality Is a Theorem"

DICTO · DICTO DOI 10.5281/zenodo.24037664 (all versions); Version 2 = 10.5281/zenodo.24091224.
Credit line of the paper (Version 3): the Loop Equality surfaced in DICTO's study of stackings (#74): the loop counts computed there came out identical on every stacking to length 34, which neither DICTO nor Claude had expected; #74 stated it as a conjecture for all lengths. Proof, checks and drafting with Claude (Anthropic).

## 1. Models and tools

- **Model:** Claude Opus (model id `claude-opus-5-5`), used through **Claude Code** (agent harness version 2.1.317), as one main agent and three subagents. Thinking blocks are not kept in the session files.
- **Computation:** Python 3 with NumPy and SciPy (`scipy.sparse` for walk propagation), and Python's exact integers and `fractions.Fraction` for every count. No floating-point number enters a count. Figures: matplotlib.
  - Original runs (7 November 2026): NumPy 2.5.4 on a second computer of DICTO's; the Python, SciPy and matplotlib versions of those runs were not recorded.
  - Reproduction run (11 November 2026, see `reproduce.md`): Python 3.14.4, NumPy 2.5.0, SciPy 1.18.0.
- **No** computer-algebra system (no SymPy) and **no** proof assistant (no Lean or Coq) was used. The proof is written by hand in the paper and was checked numerically, not formally.
- **Literature tools:** web search and page fetch from the harness; the Crossref and OpenAlex APIs for references and citing works; the OEIS search; `pdftotext` full-text search over DICTO's private reference library (259 PDFs).
- **Printing:** HTML paper typeset to PDF with Chromium (Playwright).

## 2. Process summary

1. **28 October 2026, paper #74** (DOI 10.5281/zenodo.23730421). The closed non-backtracking loops per site were counted on the tetrahedral networks of five stackings (3C, 2H, 4H, 6H, 9R): identical for every even length 6 to 34, although the networks differ from the third shell of neighbours on. DICTO stated this as the Loop Equality, a conjecture for all lengths. Script and output: `studies/2026-10-28-pyrochlore-kagome/loops2.py`, `loops2.out`. The working sessions of that day are no longer on disk (seven-day retention), so the session record starts on 7 November.
2. **7 November, 06:10-06:29 UTC.** A subagent searching DICTO's results for OEIS sequences recomputed the loop counts by the Ihara-Bass formula from the Domb numbers (A002895). It found that ordinary closed walks are also equal at every site of 3C, 2H, 4H and 6H (to length 30), and sketched a Fourier argument that would prove the equality for every stacking.
3. **07:49 UTC.** Claude recommended a short paper after a prior-art check, and DICTO approved ("all recommendations ok go ahead").
4. **07:50-07:58 UTC.** A first drafting subagent wrote a first check script and began the prior-art search. It was stopped by the usage limit.
5. **08:11-08:38 UTC.** A restarted subagent:
   - wrote the proof: Lemma 1 (walks = level paths times a Fourier integral; the stacking enters only as the sign of the step triangle at each bond layer), Lemma 2 (walks between the ends of a bond or a two-bond path do not depend on the stacking), Lemma 3 (non-backtracking loops reduced to such walks), then Ihara-Bass;
   - wrote and ran `loop_checks.py` (42 stackings, 686 sites, exact integers);
   - searched the prior art and found the closed-walk part already known (Nagle 1966; Thorpe 1972);
   - drafted `paper.html`, the figures and the Zenodo metadata.
6. **7 November, later.** The main agent typeset the draft, and DICTO read it. At 14:13 UTC he wrote "all read and approved at their current stage for dissemination if complete", and #102 was released (v1). On "go ahead with the #102 follow-ups", #74 (v2) and the HexOct book (v11) were changed from "conjecture" to "theorem (#102)" and now credit Nagle and Thorpe.
7. **10 November (Japan time), Version 2.** DICTO noticed that machine names had appeared in published papers. The methods notes of #102 (and of other papers) were cleaned and re-released. No result changed.

## 3. Prompts and harness

- The task prompts given to the subagents are reproduced verbatim (redacted) in `session-record/session-record-102.md`, Parts 2, 4 and 5. They include DICTO's house rules for wording, and the rules "do not print, publish, run git, or start background jobs or agents".
- The harness also loads a private file of DICTO's standing instructions (style, credit, release and safety rules) into the main agent's context. That file is not included: it is private and mostly about other work. The rules that shaped this paper are visible in the prompts.
- Long runs were made in the foreground with time limits, on a second computer of DICTO's. The harness moved one 3-minute run into the background on its own; that is visible in the record.

## 4. Verification

- **Exact checks** (`studies/2026-11-07-loop-equality/loop_checks.py`, output `data-loop-checks.txt`). Every site of a whole period was tested (12 consecutive bilayers if aperiodic), on finite windows chosen so that no walk can wrap round or reach the edge. 42 stackings: 3C, 2H, 4H, 6H, 9R; 30 random periodic stackings (periods 4-12); Fibonacci approximants of periods 3, 5, 8, 13 and 21; the aperiodic Fibonacci stacking; one random aperiodic stacking. 686 sites in all. Checked at every site:
  - W: closed walks, lengths 0-30, equal the diamond values (Domb numbers);
  - F: the chain formula W_2n = Σ_a c(n,a) H(a) used in the proof;
  - B and D: walks between the ends of every bond and of every two-bond path (Lemma 2);
  - T: closed non-backtracking loops, lengths 1-24, equal the Ihara-Bass values;
  - P and S (19 stackings): the pyrochlore network to length 14, and close-packed spheres to length 12, equal 3C and fcc.
- **Control:** the numbers of atoms 3 to 8 bonds away differ between sites by up to 4.9%, so the networks tested really do differ.
- **Two independent counts** of the loops agree term by term for lengths 6-34: the direct count of #74 (`loops2.py`) and the Ihara-Bass transform of the Domb numbers.
- **Re-run from the public repository on 11 November 2026:** output identical to the committed `data-loop-checks.txt` apart from timings (`reproduce.md`).
- **Human reading:** DICTO read the typeset draft before release. No outside referee has checked the proof, and it has not been formally verified.
- **Prior-art limits:** Thorpe (1972) was read as an abstract only (the paper is paywalled). Nagle's 1966 observation is known second-hand, from Isaev-McKay-Zhang (arXiv 2409.04989, §8.2).

## 5. Negative results and corrections

- **Concordance ledger:** it holds no entries on loops or walks; nothing about this result was tried and failed. The Concordance's only related item is the gap "Loop Equality for all lengths (to length 34)", source #74, marked "CLOSED 7 Nov 2026 (#102)".
- **Wrap-around error in #74's first count:** the small-cell run `loops.py` was inflated from length 16 on by walks wrapping round the periodic cell (194262 instead of 194256). `loops2.py` (large cell) superseded it. `loop_checks.py` avoids the error by making every window wider than the walk length.
- **#74's prior-art sentence was too broad.** It said there was "no earlier statement" of equal loop counts. That holds for non-backtracking loops, but not for closed walks (Nagle 1966; Thorpe 1972). Corrected in #74 v2.
- **Limits stated in #102:**
  - the equality is of counts, not of loop shapes;
  - walk counts between sites more than two bonds apart do differ between stackings;
  - equal loop counts do not by themselves prove equal ice entropy.
- **Process faults:**
  - the first drafting attempt was cut off by the usage limit, and its partial script was overwritten;
  - the figure script printed "FINAL ok" without checking that the figures existed, and was fixed to check them before the commit;
  - a reference (Kotani-Sunada) was dropped because its record could not be verified;
  - Version 1's methods notes named a computer and private paths, and Version 2 removed them.
