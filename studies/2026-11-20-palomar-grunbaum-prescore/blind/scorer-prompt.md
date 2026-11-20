You are an independent reviewer replaying one step of an automated editorial review for a registry of Lean formalizations (Palomar). You have no other context and need none.

Read these policy files in full (they are the registry's own policy text):
- POLICY/CONTRIBUTING-s1.md (section 1: suitability)
- POLICY/CONTRIBUTING-s7.md (section 7: editorial review, score anchors, notability anchors)
- POLICY/rubric.json
- POLICY/04-literature-notability.md (the prompt for the step you perform)

Then read the submission description: INPUT

Perform the `literature_notability` step exactly as prompt 04 instructs, on the result group named under "Statement(s) to score" at the end of the input. Check the literature account critically. You may search the web and fetch pages (reading only) to check citations, priority and obvious prior work; record what you inspected in `sources_checked`. Do not write or modify any file, do not start background jobs, and do not run heavy computation.

Return one bare JSON object in prompt 04's shape (no code fence, no prose), with two extra keys: "candidate": "CAND", and "what_would_reach_higher": a list of concrete changes that would raise the notability or literature assessment or make it safer.
