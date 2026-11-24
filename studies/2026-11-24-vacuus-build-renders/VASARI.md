# Vasari's *Lives* searched for the Vacuus history

Search of 24 Nov 2026. Question: what does Giorgio Vasari's *Lives* (1550 and
1568) say about Luca Pacioli, the regular solids, *De divina proportione*,
Leonardo's drawings for it, "vacuo/vacuus" solids, and the golden ratio?

**Conclusion.** Vasari names Pacioli only as "Fra Luca dal Borgo" /
"Maestro Luca dal Borgo", only in the Life of Piero della Francesca, and only to
accuse him of printing Piero's books as his own. He says Luca "wrote about the
regular bodies of geometry". He never names *De divina proportione*, the divine
proportion, Leonardo's solids drawings, hollow ("vacuo") solids, or any
polyhedron by name. The nearest other items are Uccello's 72-faced spheres and
mazzocchi, and the 72-faced ball Michelangelo had made for the lantern of the New
Sacristy.

## Sources searched

| Text | Source | Coverage | Method |
|---|---|---|---|
| English, de Vere translation (1912-15), 10 vols | Project Gutenberg ebooks 25326, 25759, 26860, 28420, 28421, 28422, 31845, 31938, 32362, 33203 (plain text from a Gutenberg mirror; the main site was down for maintenance) | full, all 10 vols incl. general index | grep, case-insensitive |
| English, Everyman/Blashfield-Hopkins ed., vol. 1 of 8 | Gutenberg 21212 | vol. 1 only | grep |
| Italian 1550 (Torrentino), Parts I-II | archive.org `gri_vitedepivecc01vasa` (Getty scan, OCR text) | Parts I-II only; Part III (vol. 2, incl. Leonardo) not available as OCR text (`gri_vitedepivecc02vasa` returned an error) | grep on OCR |
| Italian 1568 (Giunti), Parts I-II | archive.org `levitedepiue01vasa1568` (OCR) | full | grep on OCR |
| Italian 1568, Part III | archive.org `levitedepiue03vasa1568` (OCR) | full | grep on OCR |
| Italian 1550 and 1568, all Lives | it.wikisource "Le vite de' più eccellenti pittori, scultori e architettori (1550)" and "(1568)" | full-text search across all subpages of both editions; Piero Lives read in full | Wikisource search API (prefix-limited), then page text |

Terms searched (English): Luca, Pacio-, Paciuo-, Pacciuo-, regular bod-,
regular solid, Platonic, polyhedr-, divine proportion, divina, proporzione,
vacuo, vacuum, vacuus, icosahed-, dodecahed-, octahed-, tetrahed-, five bodies,
corpi, mazzocch-, facets, faces, Euclid, geometr-, mathemat-, sphere,
Giovanni da Verona. Every "Luca" hit was read and sorted (most are Luca della
Robbia, Luca Signorelli, Luca Martini, Luca Pitti etc.).

Terms searched (Italian, OCR and Wikisource): luca dal / luca del / maestro
luca / fra luca / frate luca, Pacioli, Paciolo, Pacciuolo, pacio/paciuo,
corpi regolari / regolari, poliedri, vacuo, divina proporzione / proportione,
proporzione divina, mazzocch-, settantadue / 72 facce, Euclide, Geometra,
Piloto, groppi.

## What IS there

### 1. Life of Piero della Francesca: the accusation (opening)

**1550**, Parte II, pp. 360-361 (Wikisource text; checked against the Getty
scan OCR):

> "... sí come tante decine di anni ne è stato defraudato Pietro della Francesca
> da 'l Borgo San Sepolcro. Il quale, essendo stato tenuto maestro raro e divino
> nelle difficultà de' corpi regolari, e nella aritmetrica e geometria,
> sopraggiunto nella vecchiaia dalla cecità corporale e dalla fine della vita,
> non possette mandare in luce le virtuose fatiche sue et i molti libri scritti
> da lui, che nel Borgo, sua patria, a' dí nostri ancora si conservano. E colui,
> che con tutte le forze sue si doveva ingegnare di mantenergli la gloria e di
> accrescerli nome e fama, per aver pure appreso da lui tutto quello che e'
> sapeva, non come grato e fedele discepolo, ma come empio e maligno nimico,
> annullato il nome del precettore, usurpatosi il tutto, dette in luce sotto
> nome suo proprio ciò è di fra Luca da 'l Borgo tutte le fatiche di quel buon
> vecchio."

**1568**, Seconda parte, pp. 353-354 (Wikisource marks the page break at
p. 354; the OCR page header reads "554"):

> "... come avvenne a Piero della Francesca dal Borgo a S. Sepolcro. Il quale,
> essendo stato tenuto maestro raro nelle difficoltà de' corpi regolari e
> nell'aritmetica e geometria, non potette, sopragiunto nella vecchiezza dalla
> cecità corporale e dalla fine della vita, mandare in luce le virtuose fatiche
> sue et i molti libri scritti da lui, i quali nel Borgo, sua patria, ancora si
> conservano. Se bene colui che doveva con tutte le forze ingegnarsi di
> accrescergli gloria e nome, per aver appreso da lui tutto quello che sapeva,
> come empio e maligno cercò d'annullare il nome di Piero suo precettore, et
> usurpar quello onore, che a colui solo si doveva, per sè stesso, publicando
> sotto suo nome proprio, cioè di fra' Luca dal Borgo, tutte le fatiche di quel
> buon vecchio, il quale, oltre le scienze dette di sopra, fu eccellente nella
> pittura."

**de Vere**, vol. III, Life of Piero della Francesca (Life on pp. 17-23;
Gutenberg 26860):

> "He, having been held a rare master of the difficulties of drawing regular
> bodies, as well as of arithmetic and geometry, was yet not able--being
> overtaken in his old age by the infirmity of blindness, and finally by the
> close of his life--to bring to light his noble labours and the many books
> written by him, which are still preserved in the Borgo, his native place. The
> very man who should have striven with all his might to increase the glory and
> fame of Piero, from whom he had learnt all that he knew, was impious and
> malignant enough to seek to blot out the name of his teacher, and to usurp
> for himself the honour that was due to the other, publishing under his own
> name, Fra Luca dal Borgo, all the labours of that good old man, who, besides
> the sciences named above, was excellent in painting."

(De Vere adds "of drawing" to "regular bodies"; the Italian has only "nelle
difficoltà de' corpi regolari".)

### 2. Life of Piero: Luca "wrote about the regular bodies" (second passage)

**1550**, Parte II, p. 365:

> "Egli fu studiosissimo nell'arte, e nella prospettiva valse tanto, che nessuno
> piú di lui fu mirabile nelle cose della cognizione di Euclide, e tutti i
> miglior giri tirati ne' corpi regolari egli meglio ch'altro geometra intese,
> et i maggiori lumi che di tal cose ci sieno, ci sono di man sua; perché
> maestro Luca da 'l Borgo frate di San Francesco che sopra i corpi regolari
> della geometria scrisse, fu suo discepolo. E vedendo in vecchiezza Pietro che
> aveva composto di molti libri, Maestro Luca facendoli stampare, tutti gli
> usurpò per se stesso, come già s'è detto di sopra, sí come quello a cui erano
> pervenuti nelle mani dopo la morte di Maestro Pietro."

**1568**, Seconda parte, p. 356 (from OCR page headers):

> "Fu Piero, come si è detto, studiosissimo dell'arte e si esercitò assai nella
> prospettiva, et ebbe bonissima cognizione d'Euclide in tanto che tutti i
> miglior giri tirati ne' corpi regolari, egli meglio che altro geometra
> intese, et i maggior lumi che di tal cosa ci siano, sono di sua mano; per che
> Maestro Luca dal Borgo, frate di S. Francesco che scrisse de' corpi regolari
> di geometria, fu suo discepolo. E venuto Piero in vecchiezza et a morte doppo
> aver scritto molti libri, maestro Luca detto, usurpandogli per se stesso, gli
> fece stampare come suoi, essendogli pervenuti quelli alle mani, dopo la morte
> del maestro."

**de Vere**, vol. III, same Life:

> "Piero, as it has been said, was a very zealous student of art, and gave no
> little attention to perspective; and he had a very good knowledge of Euclid,
> insomuch that he understood all the best curves drawn in regular bodies
> better than any other geometrician, and the clearest elucidations of these
> matters that we have are from his hand. Now Maestro Luca dal Borgo, a friar
> of S. Francis, who wrote about the regular geometrical bodies, was his pupil;
> and when Piero, after having written many books, grew old and finally died,
> the said Maestro Luca, claiming the authorship of these books, had them
> printed as his own, for they had fallen into his hands after the death of
> Piero."

### 3. Life of Piero: the 1550 epitaph (cut in 1568)

**1550**, Parte II, p. 367, after the note that Piero's books are in the
library of Federigo II of Urbino: "Per il che non è poi mancato chi lo abbia
onorato di questi versi:"

> "Geometra e pittor, penna e pennello
> Cosí ben misi in opra; che natura
> Condannò le mie luci a notte scura
> Mossa da invidia: e de le mie fatiche
> Che le carte allumar dotte et antiche,
> L'empio discepol mio fatto si è bello."

("L'empio discepol mio" = the impious pupil, Fra Luca, in context.) These
verses are not in the 1568 Life or in de Vere.

### 4. Other relevant lines in the Piero Life

- 1568 (de Vere vol. III): Piero's geometry writings and "a vase drawn in
  squares and sides" (Italian 1568: "un vaso in modo tirato a quadri e
  faccie, che si vede dinanzi, di dietro e dagli lati, il fondo e la bocca").
- 1568 close: "I libri di Pietro sono, per la maggior parte, nella libreria del
  Secondo Federigo duca d'Urbino, e sono tali che meritamente gli hanno
  acquistato nome del miglior geometra che fusse ne' tempi suoi." (de Vere:
  "the name of the best geometrician of his time.")
- 1568 general index (vol. 1, "Indice delle cose notabili"): an entry for
  "Luca dal borgo Framinore" [Frate minore] pointing to the Piero pages; the
  Wikisource OCR of that index is garbled ("tadato 5.3.^4 ..."), so the page
  numbers are read as 354-355 only tentatively.

### 5. Related but not about Pacioli

- **Paolo Uccello** (de Vere vol. II, Gutenberg 25759): Donatello's rebuke
  when Paolo showed him "mazzocchi with pointed ornaments, and squares drawn in
  perspective from diverse aspects; spheres with seventy-two diamond-shaped
  facets, with wood-shavings wound round sticks on each facet". 1550 (Parte II,
  p. 253): "mazzocchi a facce tirati in prospettiva, e di quegli a punte di
  diamanti ... e palle a settantadue facce molto difficili" (Wikisource; OCR
  reads "Tettata due"). 1568: "palle a 72. facce, a punte di diamanti" (OCR
  "7i."). Also in 1568: in Vasari's own drawing book "un mazzocchio tirato con
  linee sole" (de Vere: "a mazzocchio drawn only with lines"), and Uccello's
  panel of five men with Giovanni Manetti "for mathematics ... the problems of
  Euclid".
- **Michelangelo** (de Vere vol. IX, Gutenberg 32362): for the cupola of the
  New Sacristy of S. Lorenzo "he had a ball with seventy-two faces made by the
  goldsmith Piloto, which is very beautiful". 1568, Terza parte (about p. 739
  from OCR headers): "al Piloto orefice fece fare una palla a settantadue facce
  che è bellissima" (Wikisource; OCR "71.").
- **Leonardo** (de Vere vol. IV, Gutenberg 28420; 1568 Terza parte): only
  general praise. He was "an excellent geometrician" (1568 "bonissimo
  Geometra"), bewildered his arithmetic master, and drew "knots of cords"
  with "Leonardus Vinci Accademia". No mention of Pacioli, of the
  *De divina proportione* drawings, or of any solid.
- **Fra Giovanni da Verona**, inlay master (de Vere vol. IV, Life of Raphael;
  vol. VI, Lives of Fra Giocondo, Liberale and others): praised for
  "perspective-views in inlaid woodwork" at Monte Oliveto, the Vatican and
  S. Maria in Organo, Verona. Vasari does not say what the panels show; no
  solids are named.

## What is NOT there

Across all ten de Vere volumes, both Italian editions on Wikisource, and the
OCR of the 1550 (Parts I-II) and 1568 (all parts) scans:

- No surname of Pacioli in any spelling (Pacioli, Paciolo, Paciuolo,
  Pacciuolo, Paccioli). "Pacio" occurs only as the name of Beccafumi's father.
- No title or description of *De divina proportione* or the *Summa*. Luca's
  book is described only as writing "de' corpi regolari di geometria".
- No "divina proporzione/proportione", "proporzione divina", golden section,
  golden rectangle or extreme-and-mean ratio. ("Divina/divinely" occurs only
  as praise, e.g. "divinely well proportioned" columns in Piero's Arezzo
  frescoes.)
- No mention of Leonardo drawing solids for Pacioli, and no link at all
  between Leonardo and Pacioli.
- No "vacuo/vacuus/vacuum" solid. "Vacuo" occurs only in other senses: the
  hollow of a pulpit stair (Benedetto da Maiano, 1550 and 1568: "col vacuo
  della salita") and an emptied place (Andrea del Sarto, 1550: "quel luogo
  fussi vacuo").
- No Platonic solids by name, no "poliedri", no tetrahedron, octahedron,
  icosahedron or dodecahedron.

## Limits

- The 1550 Part III (Leonardo, Raphael, Michelangelo etc.) was searched only
  through Wikisource full-text search, not through scan OCR. The archive.org
  1550 volume 2 text did not download.
- Wikisource search is a word index. Variant spellings in its transcriptions
  could be missed. This risk is reduced by the matching OCR and English
  searches.
- The archive.org OCR is poor: long s read as f, numerals misread ("7i." for
  72, "554" for 354), broken words. Every quotation above is from the
  Wikisource transcription or the Gutenberg text. The OCR was used to find
  passages and page numbers, not for wording.
- Page numbers for the Italian editions come from OCR page headers and one
  Wikisource page marker. Check them against the scans before citing.
- Only volume 1 of the 8-volume Everyman translation (Gutenberg 21212) was
  available; de Vere is the full English text searched.
- The Wikisource bulk download was rate-limited (HTTP 429), so not every
  subpage was read in full. Coverage of the Italian Wikisource relies on its
  search index.
