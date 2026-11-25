# #119: for the next version (from Palomar's automated review, 25 Nov 2026)
1. Lean release commit moves to 8bdd1e15f66e03959cd05438056da909762c7682 (metadata and README only; Lean files identical to 3ba4cfc4).
2. Describe Lemma 2 exactly as the Lean statement: each other tile's number is pi, 2 pi or a dihedral angle of that tile at some
   edge point of it, chosen independently (not a common nearby point); only these values enter the proof of Theorem 4.
3. Gabbrielli-Jiao-Torquato 2012 and Conway-Radin-Sadun 1999 are now structured sources of the Palomar entry.

- Palomar automated review (25 Nov 2026, 14:10Z, codex:gpt-6-sol): "No blocking problems were identified." Disclosed warning: Lemma 2
  as formalized can count tiles that do not meet the edge point x. Next version: say plainly in the Lemma 2 statement (paper and
  formalization.yaml/README) that the selected tiles need not contain x; the weaker form is all Theorem 4 uses. No Lean change.
