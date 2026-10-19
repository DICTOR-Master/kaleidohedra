# "DICTO proposed" batch (DICTO 2026-10-20): DICTO's ideas credited as his proposals, not questions. Exact old -> new pairs per paper,
# applied to the paper sources and (the same pairs) to the Zenodo descriptions. Each pair must occur exactly once.
EDITS = {
 '2026-10-18-bull-horns': [
  ("DICTO asked whether the five-lobed patterns could become Penrose prisms that connect the OGs.", "DICTO proposed that the five-lobed patterns could become Penrose prisms that connect the OGs."),
  ('DICTO asked to develop the octet "toward a minimal golden kit".', 'DICTO proposed developing the octet "toward a minimal golden kit".'),
  ("DICTO asked whether the small dodecahedral cell at the centre of each tetrahedron could be grown into a smaller kit.", "DICTO proposed growing the small dodecahedral cell at the centre of each tetrahedron into a smaller kit."),
  ("DICTO asked whether the faces could be exact imprints of the OG.", "DICTO proposed that the faces be exact imprints of the OG."),
  ("DICTO then asked for the imprint to be centred on the Penrose star.", "DICTO then proposed centring the imprint on the Penrose star."),
  ("DICTO asked for the piece to key with itself through the star's own pattern, while staying a single piece.", "DICTO proposed that the piece key with itself through the star's own pattern, while staying a single piece.")],
 '2026-10-20-og-gyrated-octet': [
  ("DICTO asked whether it can also live in the <i>gyrated</i> octet,", "DICTO proposed that it can also live in the <i>gyrated</i> octet,"),
  ("The question whether the Ogdoecontahedron can live in the gyrated octet as well as in the octet,", "The proposal that the Ogdoecontahedron lives in the gyrated octet as well as in the octet,")],
 'both-cycles': [
  ("DICTO asked whether the two cycles can share one space, and whether together they make one real solid.", "DICTO proposed that the two cycles can share one space and together make one real solid."),
  ("the question whether the ends could be bent to give both settings", "the proposal that the ends could be bent to give both settings")],
 'dharma-inside-out': [
  ("DICTO asked what the cycle looks like turned inside out.", "DICTO proposed turning the cycle inside out."),
  ("DICTO asked for a more even nest.", "DICTO proposed a more even nest."),
  ("DICTO asked whether a Kepler–Poinsot solid could sit in the faithful nest's large outer gap.", "DICTO proposed that a Kepler–Poinsot solid could sit in the faithful nest's large outer gap."),
  ("DICTO asked whether golden rectangles would frame the whole.", "DICTO proposed that golden rectangles would frame the whole."),
  ("DICTO asked for rules that would prevent this,", "DICTO proposed rules that would prevent this,"),
  ("DICTO then asked for a dual pair instead.", "DICTO then proposed a dual pair instead.")],
 'golden-bodhi-pyrochlore': [
  ("DICTO asked for a puzzler's search instead:", "DICTO proposed a puzzler's search instead:"),
  ("DICTO asked a different question: into what single shape could the resin around the two networks be cut? His answer, seen first in his head and then built:",
   "DICTO proposed a different approach: one single shape for the resin around the two networks. His design, seen first in his head and then built:")],
 'ogdoecontahedron': [
  ("DICTO asked what the Spheres of Dharma, an exact endless nesting of six icosahedral solids, look like turned inside out.", "DICTO proposed turning the Spheres of Dharma, an exact endless nesting of six icosahedral solids, inside out."),
  ("On 13 October 2026 DICTO asked what the cycle looks like turned inside out.", "On 13 October 2026 DICTO proposed turning the cycle inside out."),
  ("DICTO asked whether copies joined on their hexagons form pyrochlore networks.", "DICTO proposed that copies joined on their hexagons form pyrochlore networks.")],
 'progenitors': [
  ("DICTO asked whether the twin pair could seed a cycle of its own.", "DICTO proposed that the twin pair could seed a cycle of its own.")],
 'theaetetus': [
  ("DICTO asked whether the Hecatodihedron, with its 102 faces, could be made of 102 pieces with no dents.", "DICTO proposed that the Hecatodihedron, with its 102 faces, could be made of 102 pieces with no dents.")],
 'ocd-chorus': [
  ("the questions that led to the exact chorus", "the proposals that led to the exact chorus")],
}
if __name__ == '__main__':
    import sys, os, re
    root = sys.argv[1]; n = 0
    for folder, pairs in EDITS.items():
        p = os.path.join(root, folder, 'paper.html'); s = open(p).read()
        for a, b in pairs:
            assert s.count(a) == 1, (folder, a[:50], s.count(a)); s = s.replace(a, b); n += 1
        assert 'DICTO asked' not in s, folder
        open(p, 'w').write(s)
    print('applied', n, 'edits in', len(EDITS), 'papers')
