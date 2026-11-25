# #121 next version notes

- Palomar entry fair-dice-lean: description corrected at commit 12c47478 (Lean unchanged from 939e6c55):
  Alexandrov's condition is stated over sets of rays, and its equivalence with the spherically convex form is not
  formalized; the die is fair about the origin (the centroid is not formalized); curvature and solid angle are
  3 × a volume inside the unit ball; Challenge.lean has `sorry` by design; source added: A. D. Alexandrov,
  Convex Polyhedra (Springer 2005). The paper's Lean section should use the same wording.

- Palomar automated review of fair-dice-lean (25 Nov 2026, 19:15Z): "No blocking problems were identified." Warning: formalization.yaml
  labels Oliker 2007 and Bertrand 2016 "background", though the entry follows Oliker's variational route and polytope theorem and
  Bertrand's necessity argument. Next version: relationship "independently-proves" for Oliker, Bertrand (and Alexandrov's polytope
  case), each note explaining the change to a condition over sets of rays; the fair-dice paper #112 stays the separate "formalizes" source.
