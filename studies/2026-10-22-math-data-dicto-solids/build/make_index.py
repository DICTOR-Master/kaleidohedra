# DICTO · dictospheres.com — writes index.csv, the inventory of DICTO's named shapes (2026-10-22).
# Status wording follows DISCOVERIES.md (master) and the published papers; nothing here is a new claim.
# One name per shape (DICTO 2026-10-23): the first name DICTO chose wins (Oktaktis, #43, is the Cleo-Icos, #29: one row),
# unless DICTO picks a later, more concise name (the F15 Jewel clusters are the #41 Jewel-Tetra and Jewel-Octa, the F16 Sunstar clusters the #42 Sunstar-Tetra and Sunstar-Octa: one row each).
# kind: solid (one polyhedron), piece (a named piece of a kit/dissection), cluster (several solids as one named body or group),
# compound, structure (a named nest, network, tiling or cycle), curved (not a polyhedron).
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
K = '10.5281/zenodo.23173809'                       # Kaleidohedra by DICTO, the findings archive (concept)
P = {'8': '10.5281/zenodo.23284106', '13': '10.5281/zenodo.23284281', '14': '10.5281/zenodo.23284213', '17': '10.5281/zenodo.23376317',
     '18': '10.5281/zenodo.23376320', '19': '10.5281/zenodo.23351291', '20': '10.5281/zenodo.23357896', '22': '10.5281/zenodo.23310541',
     '23': '10.5281/zenodo.23310833', '24': '10.5281/zenodo.23311353', '25': '10.5281/zenodo.23332821', '26': '10.5281/zenodo.23333183',
     '27': '10.5281/zenodo.23345502', '28': '10.5281/zenodo.23360857', '29': '10.5281/zenodo.23378070', '31': '10.5281/zenodo.23404688',
     '31a': '10.5281/zenodo.23430870', '33': '10.5281/zenodo.23407106', '34a': '10.5281/zenodo.23430868', '35': '10.5281/zenodo.23429911',
     '35a': '10.5281/zenodo.23430864', '35b': '10.5281/zenodo.23430866', '36': '10.5281/zenodo.23451210', '37': '10.5281/zenodo.23457016',
     '37a': '10.5281/zenodo.23484012', '38': '10.5281/zenodo.23463305', '38a': '10.5281/zenodo.23464021', '39': '10.5281/zenodo.23488944',
     '41': '10.5281/zenodo.23496353', '42': '10.5281/zenodo.23497702', '43': '10.5281/zenodo.23532013', '44': '10.5281/zenodo.23529497',
     '45': '10.5281/zenodo.23529499', '47': '10.5281/zenodo.23551326',
     '48': '10.5281/zenodo.23596362', '51': '10.5281/zenodo.23606828',
     '55': '10.5281/zenodo.23632358', '56': '10.5281/zenodo.23635823', '57': '10.5281/zenodo.23647898', '59': '10.5281/zenodo.23677485'}
NEW, RED, KN = 'new', 'rediscovered', 'known'
# name, kind, finding, paper (#), status, prior-art / note, dataset slug, Polyhedraverse id
R = [
 ('DICTO skewed rhombic dodecahedron', 'solid', 'F1', '', NEW, 'new member of a known family (RD parallelohedra: Fedorov 1885; Lalvani US 5,623,790, 1997)', 'dicto-skewed-rhombic-dodecahedron', 'DICTO_SKEWED_RD'),
 ('DICTO all-rhombus block', 'piece', 'F1', '', KN, 'a parallelepiped (part of F1); not assessed separately', '', 'DICTO_ALL_RHOMBUS_BLOCK'),
 ('DICTO flattened rhombohedron', 'piece', 'F1', '', KN, 'a rhombohedron (part of F1); not assessed separately', '', 'DICTO_FLATTENED_RHOMBOHEDRON'),
 ('Bain disphenoid', 'solid', 'F3', '', KN, 'Bain 1924 (known result shown in the apps, not DICTO\'s)', '', ''),
 ('Bain rhombic dodecahedron', 'solid', 'F4', '', KN, 'known (squares + 60 deg rhombi); not DICTO\'s', '', ''),
 ('Regular-hexagon elongated dodecahedron', 'solid', 'F5', '', RED, 'found by DICTO independently; Grunbaum 2010 Fig. 2(b) (Fedorov ED)', '', 'REGULAR_HEX_ED'),
 ('DICTO skewed elongated dodecahedron ED F16', 'solid', 'F7', '', NEW, 'new member of a known family (ED parallelohedra: Fedorov; Lalvani US 5,623,790)', 'dicto-skewed-ed-16', 'DICTO_SKEWED_ED_16'),
 ('DICTO skewed elongated dodecahedron ED F18', 'solid', 'F7', '', NEW, 'new member of a known family (ED parallelohedra: Fedorov; Lalvani US 5,623,790)', 'dicto-skewed-ed-18', 'DICTO_SKEWED_ED_18'),
 ('Euclid-Kepler-Pacioli (EKP) cell', 'structure', 'F8', '8', NEW, 'periodic approximant-type structure; not found', '', ''),
 ('Euclid-Kepler-Pacioli network', 'structure', 'F8b', '8', NEW, 'not found', '', ''),
 ('DICTO Jewel (EKP windows; first called Dragon Jewel)', 'solid', 'F10', '41', NEW, 'not found', 'dicto-jewel', 'DRAGON_JEWEL'),
 ('Stretched dodecahedron', 'solid', 'F11', '', NEW, 'candidate; simple construction, may appear elsewhere (crystal habits)', '', ''),
 ('Star Chain Reaction', 'structure', 'F12', '42', NEW, 'not found (web-level search)', '', ''),
 ('Jewel chain', 'structure', 'F12a', '', NEW, 'study of F12', '', ''),
 ('Dogstar', 'solid', 'F12', '42', RED, 'G. W. Hart 1996, stellation 8 of the dodecahedron', '', 'DOGSTAR'),
 ('Sunstar Lattice (dodecahedra and Dogstars)', 'structure', 'F16', '42', RED, 'the honeycomb is Hart\'s (1996)', '', ''),
 ('DICTO Dodeca-13', 'cluster', 'F13', '13', NEW, 'not found (the 10.3 deg gap is well known)', '', 'DICTO_DODECA13'),
 ('DICTO Dodeca-13 Wedge', 'piece', 'F13', '13', NEW, 'not found', 'dicto-dodeca-13-wedge', 'DICTO_DODECA13_WEDGE'),
 ('DICTO Dodeca-13 Needle', 'piece', 'F13', '13', NEW, 'not found', 'dicto-dodeca-13-needle', 'DICTO_DODECA13_NEEDLE'),
 ('DICTO Dodeca-13 Unit (finned unit)', 'piece', 'F13', '13', NEW, 'not found', '', 'DICTO_DODECA13_UNIT'),
 ('DICTO Dodeca-13 Star', 'piece', 'F13', '13', NEW, 'not found', '', 'DICTO_DODECA13_STAR'),
 ('DICTO-Star', 'cluster', 'F14', '14', NEW, 'not found (the overlapping whole-icosahedron version is Austin 2014)', '', ''),
 ('Kagome hulls (six hull networks)', 'structure', 'F17', '17', NEW, 'corner-sharing octahedra/tetrahedra known (perovskite, pyrochlore)', '', ''),
 ('DICTO Hexa', 'cluster', 'F18', '18', NEW, 'not found', '', 'DICTO_HEXA'),
 ('DICTO Hexa-Key', 'solid', 'F18', '18', NEW, 'not found', '', 'DICTO_HEXA_KEY'),
 ('DICTO Hexa Jewel', 'piece', 'F18', '18', NEW, 'not found', '', ''),
 ('DICTO Icosa-13', 'structure', 'F19', '19', NEW, 'not found as dissections/fillings', '', ''),
 ('UNITY (icosidodecahedron + 12 J11)', 'cluster', 'F19', '19', NEW, 'not found', '', ''),
 ('AXE', 'piece', 'F19', '19', KN, 'Mosseri-Sadoc tile', '', 'KIT13_ICOSA13_AXE'),
 ('CLEO', 'piece', 'F19', '19', KN, 'Mosseri-Sadoc tile', '', 'KIT13_ICOSA13_CLEO'),
 ('FUJI', 'piece', 'F19', '19', NEW, 'not a Mosseri-Sadoc tile; family in #20', '', 'KIT13_ICOSA13_FUJI'),
 ('VAJRA', 'piece', 'F19', '19', NEW, 'not found', '', 'KIT13_UNITY_VAJRA'),
 ('DESHI arrangement', 'structure', 'F19', '19', KN, 'Gray 2002', '', ''),
 ('DICTO Stella-Corona', 'cluster', 'F20', '19', NEW, 'the 20-icosahedron shell is a Wolfram Demonstration', '', ''),
 ('King of Pentacles', 'piece', 'F20', '19', NEW, 'not found', '', ''),
 ('Icosahedral octet', 'structure', 'F21', '', NEW, 'icosahedron in octahedron at the golden section classical (Pacioli; Fuller)', '', ''),
 ('Lotus Jewel (clawed icosahedron)', 'solid', 'F21', '', NEW, 'not found', '', ''),
 ('Admiral Cap (icosahedron edge roof)', 'piece', 'F21', '47', NEW, 'DICTO\'s; icosahedron + 6 caps = octahedron', '', 'DICTO_EDGE_ROOF'),
 ('Chain of Karma', 'structure', 'F22', '22', NEW, 'nested golden icosahedra: Gray 2002; point shells: Tsai clusters', '', ''),
 ('Spheres of Dharma', 'structure', 'F23', '23', NEW, 'shells of the Tsai cluster family (Takakura et al. 2007)', '', ''),
 ('Bodhi seed', 'structure', 'F24', '24', RED, 'partly known: Kabai\'s RT cluster layer; closure, centre, kits not found', '', ''),
 ('Crown Jewel', 'piece', 'F24', '24', NEW, 'not found', '', 'KIT13_BODHI_B4'),
 ('Vajra (fine)', 'piece', 'F24', '24', NEW, 'not found', '', 'KIT13_BODHI_B1'),
 ('DICTO Spheroid-13 RD', 'cluster', 'F25', '25', NEW, 'the tiling is known (A3 perfect code: Kovacevic-Tan 2018; Singer 1938); the block not found', '', ''),
 ('DICTO ATOM-13x13', 'structure', 'F26', '26', NEW, 'the tiling known; the set and kits not found', '', ''),
 ('Stupa', 'piece', 'F27', '27', NEW, 'Dharma piece name', '', ''),
 ('Monkey Staff', 'piece', 'F27', '27', NEW, 'Dharma piece name', '', ''),
 ('Shield', 'piece', 'F27', '28', NEW, 'pyramid on a truncated-icosahedron hexagon at the Hecatodihedron height', '', ''),
 ('DICTO Truncated-Icosahedral Hecatodihedron', 'solid', 'F28', '28', NEW, 'derived from a known solid (jtI with 12 five-fold corners cut flat; #28 V2); not found named', 'dicto-hecatodihedron', 'TRANS_DHARMA_80'),
 ('Cleo-Icos', 'piece', 'F29', '29', KN, 'the icosahedron\'s central face pyramid (classical shape; the name is DICTO\'s); appears in #43 as the OTT\'s octahedral ray, there called Oktaktis (DICTO DOI: 10.5281/zenodo.23532013)', '', 'ICOSA_FACE_PYRAMID / OTT_CLEO_ICOS'),
 ('Kion', 'piece', 'F29', '29', NEW, 'not found', '', ''),
 ('Atraktos', 'piece', 'F29', '29', NEW, 'not found', '', ''),
 ('Aetos', 'piece', 'F29', '29', NEW, 'not found', '', ''),
 ('Sphen', 'piece', 'F29', '29', NEW, 'hollow split is the shadow of Klitzing K-4.137', '', ''),
 ('Sphenion', 'piece', 'F29', '29', NEW, 'hollow split is the shadow of Klitzing K-4.137', '', ''),
 ('DICTO Ogdoecontahedron (OG)', 'solid', 'F31', '31', NEW, 'face arrangement known (dual of L0(D), Antiprism); derived from the canonical pentakis dodecahedron (#31 V2)', 'dicto-ogdoecontahedron', ''),
 ('DICTO Hecatogdoecontahedron', 'compound', 'F31', '34a', NEW, 'core and hull as the classical TI-PD compound; components in this dataset', '', ''),
 ('DICTO OCD Stella', 'solid', 'F31a', '31a', NEW, 'not found', 'dicto-ocd-stella', ''),
 ('DICTO Interlock set 1 and set 2 (piece sets)', 'structure', 'F33', '33', NEW, 'common refinement is standard', '', ''),
 ('Cleo star', 'cluster', 'F35', '35', NEW, 'not found', '', ''),
 ('DICTO Metaxyhexecontahedron', 'solid', 'F35', '35a', NEW, 'new as a named, distinguished member; the dodecahedron-icosahedron hull family is known', 'dicto-metaxyhexecontahedron', ''),
 ('DICTO Palintriacontahedron', 'solid', 'F35', '35b', NEW, 'new as a named, distinguished member; the dodecahedron-icosahedron hull family is known', 'dicto-palintriacontahedron', ''),
 ('Golden Bodhi Pyrochlore', 'structure', 'F36', '36', NEW, 'not found', '', ''),
 ('GBPC (Golden Bodhi Pyrochlore Corner)', 'piece', 'F36', '36', NEW, 'not found', '', ''),
 ('Bull-horns OG adaptor', 'piece', 'F36', '36', NEW, 'not found', '', ''),
 ('Keyed octahedron (golden-key octet)', 'piece', 'F37', '37', NEW, 'not found', '', ''),
 ('Dented tetrahedron L/R (golden-key octet)', 'piece', 'F37', '37', NEW, 'not found', '', ''),
 ('W (one-piece glue)', 'piece', 'F37', '37', NEW, 'not found', '', ''),
 ('Tetartoid core (golden envelope network)', 'piece', 'F37', '37', NEW, 'not found', '', ''),
 ('DICTO Belted Triacontahedron (DBT)', 'solid', 'F37a', '37a', NEW, 'not found', 'dicto-dbt', ''),
 ('DICTO OTT (Octahedrally Truncated Triacontahedron)', 'solid', 'F37a', '37a', NEW, 'not found (closest: Kabai 54-faced)', 'dicto-ott', ''),
 ('Mirror middle piece Mg', 'piece', 'F37a', '37a', NEW, 'not found', '', ''),
 ('DICTO Fill set 1 / 2 pieces (grown bipyramid, grown tetrahedra L/R)', 'piece', 'F37a', '37a', NEW, 'not found', '', ''),
 ('DICTO GTI (golden truncated icosahedron)', 'solid', 'F38', '38', NEW, 'cycle and pieces not found; Bergman US 4,719,726 has octet-like shells', 'dicto-gti', ''),
 ('DICTO FPD (flat pentakis dodecahedron)', 'solid', 'F38', '38', NEW, 'as above', 'dicto-fpd', ''),
 ('Five-sided Vajra', 'piece', 'F38', '38', NEW, 'not found', '', ''),
 ('Hexagonal Cleo', 'piece', 'F38', '38', NEW, 'not found', '', ''),
 ('Monkey Staff B', 'piece', 'F38', '38', NEW, 'not found', '', ''),
 ('DICTO Kepler-Poinsot-UP cycle', 'structure', '', '38a', NEW, 'not found', '', ''),
 ('DICTO KRE', 'solid', '', '39', NEW, 'combinatorics of the rhombic enneacontahedron (known type); this metric solid new', 'dicto-kre', ''),
 ('DICTO PHE', 'solid', '', '39', NEW, 'face counts of Goldberg GP(3,0); this solid new', 'dicto-phe', ''),
 ('DICTO TPP', 'solid', '', '39', NEW, 'not found', 'dicto-tpp', ''),
 ('DICTO DPHP', 'solid', '', '39', NEW, 'not found', 'dicto-dphp', ''),
 ('DICTO TPH', 'solid', '', '39', NEW, 'not found', 'dicto-tph', ''),
 ('DICTO TQH', 'solid', '', '39', NEW, 'not found', 'dicto-tqh', ''),
 ('DICTO TQP', 'solid', '', '39', NEW, 'not found', 'dicto-tqp', ''),
 ('DICTO TQHD', 'solid', '', '39', NEW, 'not found', 'dicto-tqhd', ''),
 ('DICTO Jewel-Tetra', 'cluster', 'F15', '41', NEW, 'not found; first called the DICTO Jewel tetrahedral cluster (F15), the same solid (corners matched, scale φ/2); DICTO chose the concise #41 name', '', 'DJ_TETRAHEDRAL_CLUSTER'),
 ('DICTO Jewel-Octa', 'cluster', 'F15', '41', NEW, 'not found; first called the DICTO Jewel octahedral cluster (F15), the same solid (corners matched, scale φ/2); DICTO chose the concise #41 name', '', 'DJ_OCTAHEDRAL_CLUSTER'),
 ('DICTO Jewel-Rhombi', 'cluster', '', '41', NEW, 'not found', '', ''),
 ('DICTO Sunstar-Tetra', 'cluster', 'F16', '42', NEW, 'not found; first called the Sunstar tetrahedral cluster (4 dodecahedra) (F16), the same solid (corners matched, scale φ/2); DICTO chose the concise #42 name', '', 'DODECA_TETRAHEDRAL_CLUSTER'),
 ('DICTO Sunstar-Octa', 'cluster', 'F16', '42', NEW, 'not found; first called the Sunstar octahedral cluster (6 dodecahedra round a Dogstar) (F16), the same solid (corners matched, scale φ/2); DICTO chose the concise #42 name', '', 'DODECA_OCTAHEDRAL_CLUSTER'),
 ('DICTO Sunstar-Rhombi', 'cluster', '', '42', NEW, 'not found', '', ''),
 ('DICTO Sunstar-Hexa', 'cluster', '', '42', NEW, 'not found', '', ''),
 ('DICTO Sunstar-Hexa-Key', 'solid', '', '42', NEW, 'not found', '', ''),
 ('Cleo Towers (8 tower pieces)', 'piece', '', '43', NEW, 'not found', '', 'CLEO_TOWER_*'),
 ('Polar Cleo Towers (7 tower pieces + core ray)', 'piece', '', '43', NEW, 'not found', '', 'POLAR_TOWER_* / POLAR_CORE_RAY'),
 ('DICTO Hex Aktis', 'piece', '', '43', NEW, 'not found', '', 'HEX_AKTIS'),
 ('DICTO Deltoid Aktis', 'piece', '', '43', NEW, 'not found', '', 'DELTOID_AKTIS'),
 ('DICTO Triaktis (OTT triangle ray)', 'piece', '', '43', NEW, 'not found', '', 'OTT_TRIANGLE_RAY'),
 ('DICTO Tetraktis (OTT rhombic ray)', 'piece', '', '43', NEW, 'not found', '', 'OTT_RHOMBIC_RAY'),
 ('DICTO TQP-252', 'solid', '', '43', NEW, 'not found', '', ''),
 ('DICTO TQ-320', 'solid', '', '43', NEW, 'not found', '', ''),
 ('DICTO TQP-402', 'solid', '', '43', NEW, 'not found', '', ''),
 ('DICTO TQ-500', 'solid', '', '43', NEW, 'not found', '', ''),
 ('DICTO TQD-732', 'solid', '', '43', NEW, 'not found', '', ''),
 ('DICTO TQHD-662', 'solid', '', '43', NEW, 'not found', '', ''),
 ('DICTO TQP-672', 'solid', '', '43', NEW, 'not found', '', ''),
 ('Antonius', 'piece', '', '44', NEW, 'Cleo-Icos and Antonius: a new space-filling pair from the golden rhombohedron (#20, #44)', '', 'ANTONIUS'),
 ('Penta-cleo', 'piece', '', '20', NEW, 'named in #20', '', 'PENTA_CLEO'),
 ('Reuleaux tetrahedron', 'curved', '', '45', KN, 'Reuleaux tetrahedron (classical)', '', ''),
 ('Reuleaux octahedron, Reuleaux cube, Reuleaux icosahedron, Reuleaux dodecahedron (balls on the cube, octahedron, dodecahedron, icosahedron corners; names by look)', 'curved', '', '45', NEW, 'four bodies; not Reuleaux polyhedra in the strict sense (#45)', '', ''),
 ('Half octahedron P (#47 connector)', 'piece', '', '47', KN, 'square pyramid, half the regular octahedron', '', ''),
 ('Tetrahedron face pyramid Q and Q\' (#44, #47 connectors)', 'piece', '', '47', KN, 'central face pyramid of the tetrahedron', '', ''),
 ('X (cube of edge phi minus one Euclid roof) (#47)', 'piece', '', '47', NEW, 'named connector of #47', '', ''),
 ('Y (cube of edge phi plus one Euclid roof) (#47)', 'piece', '', '47', NEW, 'named connector of #47', '', ''),
 # version 2 (2026-10-24): the six DICTONIC SOLIDS of #48 and #51 (DICTO's names; the three DICTONIC BONDS are in packings/)
 ('Icosaxes', 'solid', '', '48', KN, 'known shape: Koca et al. 2015 non-regular truncated octahedron x = tau (semi-uniform truncated octahedron); new route (the golden split of the AXE in the icosahedron lattice, #48); the name is DICTO\'s', 'dicto-icosaxes', ''),
 ('Unborn Axes', 'solid', '', '48', KN, 'known shape: Koca et al. 2015 non-regular truncated octahedron x = 1/tau; new route (#48); the name is DICTO\'s', 'dicto-unborn-axes', ''),
 ('Lotus Jewel Axes', 'solid', '', '48', NEW, 'not found; the Icosaxes with 8 Tricap dents (#48 Theorem 3)', 'dicto-lotus-jewel-axes', ''),
 ('Dodecaxes', 'solid', '', '48', NEW, 'not found; the Unborn Axes with 8 Tricap keys, holding a whole regular dodecahedron (#48 Theorem 3)', 'dicto-dodecaxes', ''),
 ('Samson', 'solid', '', '51', NEW, 'new proportion: the cube with four alternate corners cut, at the Delian bond; not found in the sources (#51)', 'dicto-samson', ''),
 ('Delilah', 'solid', '', '51', KN, 'known shape (regular octahedron), of edge 2^(-1/3) at octet edge 1; DICTO\'s name for it at the Delian bond (#51)', 'dicto-delilah', ''),
]
N_V2 = len(R)                                       # rows of versions 1 and 2: their D-numbers D1-D75 stay as they are
# version 3 (2026-10-27): twelve named solids of #55, #56, #57 and #59 (DICTO's names; status and notes from the papers)
R += [
 ('Goliath', 'solid', '', '55', KN, 'known shape: the classical Z12 coordination icosahedron of A15 (Frank and Kasper 1958), the convex hull of Jessen\'s orthogonal icosahedron (Jessen 1967) scaled by 1/2; here the A15 power cell at weight difference 3/4 (#55: the tiling is the classical picture of A15 shifted by half a body diagonal); the name is DICTO\'s', 'dicto-goliath', ''),
 ('David', 'solid', '', '55', KN, 'known shape: a tetragonal disphenoid, the empty Cr4 tetrahedron of A15 moved by half a body diagonal (#55 Corollary 1); the name is DICTO\'s', 'dicto-david', ''),
 ('Sonsam', 'solid', '', '56', NEW, 'not found in the sources checked (#56): the twinned octet\'s tetrahedral-hole piece at its equal-volume point (19 corners, a nine-sided face on the mirror plane); #56: easy to compute, so an unnamed drawing may exist', 'dicto-sonsam', ''),
 ('Lahdeli', 'solid', '', '56', NEW, 'not found in the sources checked (#56): the twinned octet\'s octahedral-hole piece at its equal-volume point, Delilah\'s twin', 'dicto-lahdeli', ''),
 ('Ian Dury', 'solid', '', '56', NEW, 'not found in the sources checked (#56): the twinned octet\'s tetrahedral-hole piece at the stop 5/24, beside the classical 60 deg rhombohedron', 'dicto-ian-dury', ''),
 ('Blockhead', 'solid', '', '56', NEW, 'not found in the sources checked (#56): the twinned octet\'s tetrahedral-hole piece at 3/8, the twin of the cube', 'dicto-blockhead', ''),
 ('Chucky', 'solid', '', '57', NEW, 'not found in the sources checked (#57): a Janus c/h piece of ABAC at -3/8 (hexagonal top half, cubic bottom half); its volume is the mean of its two parents\'', 'dicto-chucky', ''),
 ('Fang', 'solid', '', '57', NEW, 'not found in the sources checked (#57): a Janus c/h piece of ABAC at 5/24 (hexagonal top half, cubic bottom half); its volume is the mean of its two parents\'', 'dicto-fang', ''),
 ('Triskelion Tetrahedron', 'solid', '', '57', NEW, 'the cubic octet\'s tetrahedral piece at 5/24, a member of Samson\'s sliding family (#51); met in ABAC and named in #57 (the name marks that member)', 'dicto-triskelion-tetrahedron', ''),
 ('Keyaxes', 'solid', '', '59', NEW, 'the piece of the keyed Icosaxes Kagome network (the Icosaxes with 2 Tricap dents and 6 mirrored Tricap keys, volume phi^2); the network was not found in the sources searched (#59)', 'dicto-keyaxes', ''),
 ('Icosaxes Hexa', 'cluster', '', '59', NEW, 'eight Icosaxes round an Unborn Axes as one solid (= nine Icosaxes passing through each other), the node of the Icosaxes Kagome network; the network was not found in the sources searched (#59)', 'dicto-icosaxes-hexa', ''),
 ('Lotus Hexa', 'cluster', '', '59', NEW, 'the keyed Icosaxes Hexa: eight corner pieces dented towards a Dodecaxes and keyed outward (mirrored Tricaps) on their other seven hexagons (#59)', 'dicto-lotus-hexa', ''),
]
# universal_number (version 2, DICTO 2026-10-23): established catalogue numbers of earlier creators first (Johnson J, uniform U,
# Wenninger W, Hart's stellation lists, Mosseri-Sadoc tiles); DICTO D-numbers (below) for DICTO's new shapes; see d-numbers.md. Empty = no number. Only numbers we are sure of.
UNUM = {
 'Dogstar': 'Hart 1996, tetrahedral stellations of the dodecahedron, no. 8',
 'AXE': 'Mosseri-Sadoc t6 (scaled by 1/tau)',
 'CLEO': 'Mosseri-Sadoc t4 (scaled by 1/tau)',
 'Half octahedron P (#47 connector)': 'J1',
 'Delilah': 'U5; W2',
}
# D-numbers (DICTO 2026-10-24): DICTO's permanent catalogue number, one per new solid or piece (status new, kind solid/piece), in the
# order of first publication (this list's order), never reused. D1-D71 for the single shapes, then D72-D75 for the four rows that group
# several pieces (one number per group row for now; per piece to confirm with DICTO). Known/rediscovered shapes get no D-number. A shape
# with an outside catalogue number that is also DICTO's new shape would show both, outside number first, "; "-separated (none so far).
GROUPS = ['Dented tetrahedron L/R (golden-key octet)', 'DICTO Fill set 1 / 2 pieces (grown bipyramid, grown tetrahedra L/R)',
          'Cleo Towers (8 tower pieces)', 'Polar Cleo Towers (7 tower pieces + core ray)']
_eligible = [r[0] for r in R[:N_V2] if r[1] in ('solid', 'piece') and r[4] == NEW]
_single = [n for n in _eligible if n not in GROUPS]; _grp = [n for n in _eligible if n in GROUPS]
assert len(_grp) == 4 and len(_single) == 71
DNUM = {n: f'D{i + 1}' for i, n in enumerate(_single + _grp)}
# version 3 (2026-10-27): the next free D-numbers, D76 on, in the order of first publication (#56, #57, #59); never renumbering D1-D75.
# Clusters (the Icosaxes Hexa and Lotus Hexa, like the DICTO Hexa) and known shapes (Goliath, David) get none.
_v3 = [r[0] for r in R[N_V2:] if r[1] in ('solid', 'piece') and r[4] == NEW]
DNUM.update({n: f'D{76 + i}' for i, n in enumerate(_v3)})
for n, d in DNUM.items(): UNUM[n] = UNUM[n] + '; ' + d if n in UNUM else d
rows = []
for name, kind, fnum, paper, status, note, slug, pv in R:
    doi = P[paper] if paper else K
    rows.append({'name': name, 'universal_number': UNUM.get(name, ''), 'kind': kind, 'finding': fnum, 'paper': ('#' + paper) if paper else '', 'status': status, 'prior_art_or_note': note,
                 'dicto_doi': 'DICTO DOI: ' + doi, 'in_dataset': 'y' if slug else 'n', 'dataset_file': f'solids/{slug}.json' if slug else '',
                 'in_polyhedraverse': 'y' if pv else 'n', 'polyhedraverse_id': pv})
    assert set(UNUM) <= {r[0] for r in R}
    if slug: assert os.path.exists(os.path.join(ROOT, 'solids', slug + '.json')), slug
with open(os.path.join(ROOT, 'index.csv'), 'w', newline='') as fh:
    fh.write('# DICTO named-shape inventory · Created by DICTO · dictospheres.com · CC BY-SA 4.0 · 2026-10-22 (version 2: 2026-10-24; version 3: 2026-10-27)\n')
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r['status'] for r in rows), Counter((r['kind'], r['status']) for r in rows), sum(r['in_dataset'] == 'y' for r in rows))
