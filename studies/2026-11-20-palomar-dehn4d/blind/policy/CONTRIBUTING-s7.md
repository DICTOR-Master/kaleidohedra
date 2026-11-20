## 7. Editorial review

The review is performed by a language model working through a fixed sequence of
prompts. No person reads an ordinary submission before the outcome, and no
person signs it off. It is not peer review, and it is not evidence that a
mathematician has checked the result. It is a structured, recorded, automated
filter, and it should be weighed as that.

The review consists of required evidence checks followed by a synthesis step. A
check examines one subject and returns an outcome, findings tied to files or
other evidence, and one or more scores. Synthesis combines those fixed check
results into the final review outcome; it does not raise or average scores.

Every substantive check must return a coverage manifest containing every
theorem name and then every definition name in the recorded Comparator
configuration. The reviewer rejects an incomplete or reordered manifest. Clean
declarations need no individual comment, but every distinct material criticism
must be reported; finding one problem must not suppress review of later
declarations. A classification check likewise records every submitted code.
The reviewer mechanically requires the final AI-comment list to contain every
material finding from every evidence check, once and in order. A finding is an
author-facing criticism and may later be published. Positive checks, harmless
edge cases, excluded failure modes, and non-material concerns instead go into
private `internal_notes`; those notes cannot justify an outcome or requested
change. Severity remains internal; all findings are presented under the same
AI-comments heading. One Palomar
submission records one Comparator configuration. A
repository with several configurations must submit each configuration
separately if all of them are to become Palomar records.

The required checks examine:

- whether any arXiv or MSC2020 classification is egregiously off-topic, while
  presuming possible proof relevance without investigating it;
- the clarity, accuracy, and completeness of the required structured metadata,
  provenance, and narrative account across its supplied locations;
- alignment between every compared theorem and its informal account, including
  definitions, quantifiers, hypotheses, coercions, degenerate cases, and
  claimed scope;
- the fidelity and auditability of every material definition and imported
  concept used by the compared statements;
- the literature account and the result's research interest.

If an informal proof account is present in any eligible narrative location, an
additional check compares it with the actual Solution proof and its imports.

Each check uses one of three machine-readable outcomes:

- `neutral`: the check identified no material problem;
- `warning`: the check identified a specific non-blocking warning;
- `failure`: the check identified a material deficiency or contradiction, or could not
  affirmatively establish a mandatory criterion from the available evidence.

A failed check does not by itself choose the final outcome. Synthesis returns
`revision_required` when a specific, realistically correctable evidence or
presentation gap could make the submission qualify, and `rejected` for a
fundamental failure.
The report should describe uncertainty as an evidence limitation rather than
making a stronger negative claim than the evidence supports.

Scores run from 1 to 5:

- `1`: unusable, materially incorrect, or misleading;
- `2`: major errors or omissions;
- `3`: minimally adequate, but with meaningful limitations or unverified
  claims;
- `4`: thorough, fair, supported by evidence, and correct apart from minor
  issues;
- `5`: exceptionally complete and independently checkable, with no meaningful
  gap found after critical review.

The current rubric minimum is **4**. A score of 4 or 5 requires
concrete positive evidence, not merely successful compilation, populated
fields, familiar terminology, or the absence of an obvious contradiction. A
clean check must reach 4 on every score it owns. A non-mandatory dimension may
score 3 with a `warning` outcome and a concrete material finding without
blocking registration. A score of 1 or 2 is a failed check. Notability is
mandatory: below 4 it fails the check and requires rejection.

One exception, or these anchors would forbid what section 3 permits: a source
disclosed as unconfirmable, precisely stated, is not an "unverified claim" for
the `3` anchor, and does not by itself hold literature below 4. It cannot
support a `5`, which requires an account somebody else can check.

No score is published. They decide the outcome; the five above are kept in a
private file beside the database entry and the rest stay in the private review,
and the outcome is what a reader is shown, because the same repository at the
same commit has scored 5 and then 4 on one dimension across two runs of this
policy with the same outcome both times.

**No text a reader may see may state, bound, or imply a score.** That covers
every `summary` and every finding `message`. It is not enough to leave the
number out: "this prevents a literature score of 5 but not 4" names the score
exactly, and "every score meets the minimum" bounds all of them. Say what is
wrong or missing, and what would put it right. Write

> The unconfirmable source is disclosed precisely, and no priority is claimed
> from it.

rather than

> This prevents a literature score of 5 but not 4.

Both say the same thing about the submission; only the first says nothing about
the arithmetic.

Notability has its own anchors:

- `1`: incoherent, manufactured, materially deceptive, or framed in a way
  associated with mathematically baseless claims, with no credible
  contribution;
- `2`: identifiable but trivial, routine, lightly repackaged, or without a
  plausible research audience;
- `3`: borderline interest, where paper-worthiness or a credible research
  audience has not been affirmatively established;
- `4`: plausibly paper-worthy, with a specifically identified credible research
  audience;
- `5`: unusually consequential, with clear interest beyond a narrow specialist
  audience.

A notability score below 4 is a fundamental editorial failure and leads to
`rejected`, including when a credible research audience or plausible
paper-worthiness has not been affirmatively established. Findings may say
plainly that work is `trivial`, `confusing`, `unclear`, or `niche without an
identifiable research audience` where the evidence supports it. When the
evidence establishes only that the requirement was not demonstrated, the
finding should say that instead. Findings assess the work and its presentation,
never the submitter.

### Final outcomes

- `neutral`: the automated review identified no blocking problem. This permits
  registration but does not accept, approve, or endorse the submission. It may
  include disclosed, non-blocking warnings but no requested changes;
- `revision_required`: the result may qualify after specific, realistically
  correctable changes, which the review lists;
- `rejected`: there is a fundamental semantic, provenance, or editorial failure,
  including failure to affirmatively establish the research-interest
  requirement.

Palomar has no appeals route and no human sign-off on review outcomes. A submitter
who believes the reading is wrong should correct or strengthen the submission
and submit the corrected commit.

If an operator or tool failure prevents the automated review from completing,
the submission is marked `review-failed`. That is an operational state, not a
review outcome about the submission; Palomar may investigate and rerun it.

Every review includes a summary, author-facing findings, any requested
changes, private scores and audit notes, and a machine-readable report.

