# Builds the Zenodo SOFTWARE metadata for DICTO's four Palomar-registered Lean repos (one JSON per repo).
#   python3 make_meta.py
import json
LEAN = 'Lean 4 (leanprover/lean4:v4.35.0-rc2) with Mathlib at commit 0653561 (tag v4.35.0-rc2)'
PAL = 'https://data.palomar-registry.org/entries/{}.json'
R = [
 dict(repo='dehn-canon-lean', commit='9ea20f6dfd64fc3f10f64b1fb59a754a77e5cf57', palomar='PALOMAR-2026-11-20-000003-v1',
      short='The Dehn Canon', paper='#113', concept='10.5281/zenodo.24383552',
      what="Dehn's answer to Hilbert's third problem, with the Dehn invariant defined from the solid as a set of points: Hilbert's two tetrahedra on one base are neither scissors congruent nor equicomplementable; the set-defined invariant equals the classical edge sum of length ⊗ dihedral angle; scissors-congruent convex polytopes have the same invariant; and no similar copy of the regular tetrahedron is scissors congruent to a similar copy of the cube."),
 dict(repo='dehn-hadwiger-4d-lean', commit='5a2cf4ca1b3a5f14f9e2cfd5596189219bdd31e9', palomar=None,
      short='The Dehn–Hadwiger Invariant in Four Dimensions', paper='#116', concept='10.5281/zenodo.24393967',
      what="The Dehn–Hadwiger invariant defined from the set alone, in every finite-dimensional real inner product space: scissors-congruent convex polytopes, and finite unions of them, have the same invariant in every dimension; its values on the six regular 4-polytopes (0 for the tesseract, 16-cell, 24-cell and 120-cell; nonzero for the 5-cell and the 600-cell, of opposite signs); and the resulting non-congruences between similar copies of these polytopes."),
 dict(repo='grunbaum-k10-lean', commit='a6b16c25d80fa90ea28259bad6a53d7e81d01779', palomar='PALOMAR-2026-11-20-000013-v1',
      short='Ten Faces in Every Zone', paper='#115', concept='10.5281/zenodo.24389006',
      what="An answer to Grünbaum's zone question (Math. Intelligencer 32(4), 2010) for k = 10: there is a polyhedron of spherical type whose 30 faces are congruent golden rhombi, in which every zone has exactly 10 faces, and whose lattice translates tile space face to face; the zone definition is calibrated on the cube (4) and the rhombic dodecahedron (6)."),
 dict(repo='kulaichev-yantra-lean', commit='6bf9e0401c673ccf1030794493650331b7962b25', palomar='PALOMAR-2026-11-17-000006-v2',
      short='The DICTO Yantra', paper='#103', concept='10.5281/zenodo.24052633',
      what="Kulaichev's uniqueness question for the Śrī Yantra (1984): under the classical conditions in Huet's form as given by Chiodo, Kulaichev's four conditions and the admissibility of paper #103, exactly one figure exists, and its slope w7/b7 lies in a proved interval of width 2⁻²¹; the proof uses a kernel-checked certificate of 64,613 rational boxes."),
]
for r in R:
    s = r['commit'][:7]
    tree = f"https://github.com/DICTOR-Master/{r['repo']}/tree/{r['commit']}"
    pid = r['palomar'].rsplit('-v', 1)[0] if r['palomar'] else 'PALOMAR registration pending'
    reg = (f"registered in the Palomar registry as {r['palomar']} at this commit" if r['palomar']
           else "submitted for registration in the Palomar registry at this commit")
    desc = (f"<p>Lean 4 formalization accompanying DICTO's paper {r['paper']}, <i>{r['short']}</i> "
            f"(<a href=\"https://doi.org/{r['concept']}\">doi:{r['concept']}</a>). It proves: {r['what']}</p>"
            f"<p>Built with {LEAN}. This archive is the GitHub repository DICTOR-Master/{r['repo']} at commit {r['commit']}, "
            f"{reg}; every proof is checked by the Lean kernel.</p>")
    rel = [dict(identifier=f"https://doi.org/{r['concept']}", relation='isSupplementTo', resource_type='publication-preprint', scheme='doi'),
           dict(identifier=tree, relation='isIdenticalTo', resource_type='software', scheme='url')]
    if r['palomar']:
        rel.append(dict(identifier=PAL.format(r['palomar']), relation='isDocumentedBy', resource_type='other', scheme='url'))
    m = dict(upload_type='software', title=f"{r['short']}: Lean 4 formalization ({pid})",
             creators=[dict(name='DICTO', affiliation='Independent artist, Osaka, Japan', orcid='0009-0001-2620-2036')],
             description=desc, access_right='open', license='Apache-2.0', version=f"registered commit {s}",
             language='eng', keywords=['Lean 4', 'Mathlib', 'formalization', 'machine-checked proof'],
             related_identifiers=rel)
    json.dump(dict(repo=r['repo'], commit=r['commit'], zip=f"{r['repo']}-{s}.zip", palomar=r['palomar'], metadata=m),
              open(f"meta-{r['repo']}.json", 'w'), ensure_ascii=False, indent=1)
    print(m['title'])
