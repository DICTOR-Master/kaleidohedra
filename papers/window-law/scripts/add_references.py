# Window Law v1: add the numbered list of outside works (DICTO 2026-11-01: "references may not be enough").
# Inserts [n] after each place an outside work is named (body only; the Sources-checked paragraph is untouched),
# numbers by first citation, and appends <h2>References</h2> after the existing end paragraphs. Run once.
import re, os, sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','paper.html')
s=open(P,encoding='utf8').read()
if '<h2>References</h2>' in s: sys.exit('already done')
cut=s.index('<p class="prec"><b>Sources checked')
body,tail=s[:cut],s[cut:]
R={
'jag':'H. Jagodzinski, Eindimensionale Fehlordnung in Kristallen und ihr Einfluss auf die Röntgeninterferenzen. I. Berechnung des Fehlordnungsgrades aus den Röntgenintensitäten, <i>Acta Crystallographica</i> 2 (1949) 201–207. DOI 10.1107/S0365110X49000552.',
'dek':'F. M. Dekking, On the Thue–Morse measure, <i>Acta Universitatis Carolinae, Mathematica et Physica</i> 33 (1992) 35–40. No DOI; data as cited in Balková and Pelantová (2009).',
'ber':'V. Berthé, Fréquences des facteurs des suites sturmiennes, <i>Theoretical Computer Science</i> 165 (1996) 295–309. DOI 10.1016/0304-3975(95)00224-3.',
'bp':'L. Balková and E. Pelantová, A note on symmetries in the Rauzy graph and factor frequencies, <i>Theoretical Computer Science</i> 410 (2009) 2779–2783. DOI 10.1016/j.tcs.2009.04.002; arXiv 0902.0632.',
'ht':'S. Hendricks and E. Teller, X-ray interference in partially ordered layer lattices, <i>Journal of Chemical Physics</i> 10 (1942) 147–167. DOI 10.1063/1.1723678.',
'selke':'W. Selke, The ANNNI model — theoretical analysis and experimental application, <i>Physics Reports</i> 170 (1988) 213–264. DOI 10.1016/0370-1573(88)90140-8.',
'cnh':'C. Cheng, R. J. Needs and V. Heine, Inter-layer interactions and the origin of SiC polytypes, <i>Journal of Physics C: Solid State Physics</i> 21 (1988) 1049–1063. DOI 10.1088/0022-3719/21/6/012.',
'py':'G. D. Price and J. Yeomans, The application of the ANNNI model to polytypic behaviour, <i>Acta Crystallographica B</i> 40 (1984) 448–454. DOI 10.1107/S0108768184002469.',
'cava':'L. T. Nguyen and R. J. Cava, Hexagonal perovskites as quantum materials, <i>Chemical Reviews</i> 121 (2021) 2935–2965. DOI 10.1021/acs.chemrev.0c00622; arXiv 2006.05864 (cited in the text as Cava et al.).',
'jin':'C.-Q. Jin, J.-S. Zhou, J. B. Goodenough, Q. Q. Liu, J. G. Zhao, L. X. Yang, Y. Yu, R. C. Yu, T. Katsura, A. Shatskiy and E. Ito, High-pressure synthesis of the cubic perovskite BaRuO<sub>3</sub> and evolution of ferromagnetism in ARuO<sub>3</sub> (A = Ca, Sr, Ba) ruthenates, <i>Proceedings of the National Academy of Sciences USA</i> 105 (2008) 7115–7119. DOI 10.1073/pnas.0710928105.',
'ah':'J. J. Adkin and M. A. Hayward, BaMnO<sub>3−x</sub> revisited: a structural and magnetic study, <i>Chemistry of Materials</i> 19 (2007) 755–762. DOI 10.1021/cm062055r.',
'ram':'L. S. Ramsdell, Studies on silicon carbide, <i>American Mineralogist</i> 32 (1947) 64–82. No DOI.',
'fk58':'F. C. Frank and J. S. Kasper, Complex alloy structures regarded as sphere packings. I. Definitions and basic principles, <i>Acta Crystallographica</i> 11 (1958) 184–190. DOI 10.1107/S0365110X58000487.',
'fk59':'F. C. Frank and J. S. Kasper, Complex alloy structures regarded as sphere packings. II. Analysis and classification of representative structures, <i>Acta Crystallographica</i> 12 (1959) 483–499. DOI 10.1107/S0365110X59001499.',
'nel':'D. R. Nelson, Order, frustration, and defects in liquids and glasses, <i>Physical Review B</i> 28 (1983) 5515–5535. DOI 10.1103/PhysRevB.28.5515.',
'aflow':'M. J. Mehl, D. Hicks, C. Toher, O. Levy, R. M. Hanson, G. Hart and S. Curtarolo, The AFLOW Library of Crystallographic Prototypes: Part 1, <i>Computational Materials Science</i> 136 (2017) S1–S828. DOI 10.1016/j.commatsci.2017.01.017.',
'cod':'S. Gražulis, D. Chateigner, R. T. Downs, A. F. T. Yokochi, M. Quirós, L. Lutterotti, E. Manakova, J. Butkus, P. Moeck and A. Le Bail, Crystallography Open Database – an open-access collection of crystal structures, <i>Journal of Applied Crystallography</i> 42 (2009) 726–729. DOI 10.1107/S0021889809016690.',
'sul':'J. M. Sullivan, The geometry of bubbles and foams, in <i>Foams and Emulsions</i> (Springer, Dordrecht, 1999) 379–402. DOI 10.1007/978-94-015-9157-7_23.',
'sm':'J.-F. Sadoc and R. Mosseri, Quasiperiodic Frank–Kasper phases derived from the square–triangle dodecagonal tiling, <i>Structural Chemistry</i> 28 (2017) 63–73 (online 2016). DOI 10.1007/s11224-016-0846-2; arXiv 1609.01624.',
'yk':'Ya. P. Yarmolyuk and P. I. Kripyakevich, <i>Soviet Physics – Crystallography</i> 19 (1974) 334–337. No DOI; data as cited by Gvozdetskyi, Gladyshevskii and Hlukhyy (2014), ref. 4; the paper itself was not reached.',
'dsdd':'M. Dutour Sikirić, O. Delgado-Friedrichs and M. Deza, Space fullerenes: a computer search for new Frank–Kasper structures, <i>Acta Crystallographica A</i> 66 (2010) 602–615. DOI 10.1107/S0108767310022932.',
'talk':'O. Delgado Friedrichs, M. Deza and M. Dutour Sikirić, Space fullerenes, talk slides, https://poivs.tsput.ru/conf/international/XVI/files/talks/newSpaceFull.pdf (no date or venue in the record found).',
'ss':'D. P. Shoemaker and C. B. Shoemaker, Concerning the relative numbers of atomic coordination types in tetrahedrally close packed metal structures, <i>Acta Crystallographica B</i> 42 (1986) 3–11. DOI 10.1107/S0108768186098671.',
'mh':'M. Morse and G. A. Hedlund, Symbolic dynamics II. Sturmian trajectories, <i>American Journal of Mathematics</i> 62 (1940) 1–42. DOI 10.2307/2371431.',
'jd':'A. Jagannathan and M. Duneau, Properties of the Ammann–Beenker tiling and its square periodic approximants, <i>Israel Journal of Chemistry</i> 64 (2024) e202300119. DOI 10.1002/ijch.202300119; arXiv 2308.07701 (2023).',
'eh':'V. Elser and C. L. Henley, Crystal and quasicrystal structures in Al–Mn–Si alloys, <i>Physical Review Letters</i> 55 (1985) 2883–2886. DOI 10.1103/PhysRevLett.55.2883.',
'hen':'C. L. Henley, Crystals and quasicrystals in the aluminum–transition metal system, <i>Journal of Non-Crystalline Solids</i> 75 (1985) 91–96. DOI 10.1016/0022-3093(85)90208-X.',
'dmo':'M. Duneau, R. Mosseri and C. Oguey, Approximants of quasiperiodic structures generated by the inflation mapping, <i>Journal of Physics A: Mathematical and General</i> 22 (1989) 4549–4564. DOI 10.1088/0305-4470/22/21/017.',
'gv':'V. Gvozdetskyi, R. Gladyshevskii and V. Hlukhyy, Structure of a new multicomponent stannide and comments on the Yarmolyuk–Kripyakevich criterion for Frank–Kasper phases, <i>Chemistry of Metals and Alloys</i> 7 (2014) 169–180.',
'bg':'M. Baake and U. Grimm, <i>Aperiodic Order. Volume 1: A Mathematical Invitation</i> (Cambridge University Press, Cambridge, 2013). DOI 10.1017/CBO9781139025256.',
}
# (phrase, replacement with {key} markers); every occurrence in the body not already cited
SUB=[
("Jagodzinski's notation","Jagodzinski's notation {jag}"),
("(Dekking;","(Dekking {dek};"),
("Berthé 1996","Berthé 1996 {ber}"),
("Balková and Pelantová)","Balková and Pelantová {bp})"),
("Hendricks and Teller 1942","Hendricks and Teller 1942 {ht}"),
("Jagodzinski 1949","Jagodzinski 1949 {jag}"),
("(the ANNNI model)","(the ANNNI model {selke})"),
("Cheng, Needs and Heine 1988","Cheng, Needs and Heine 1988 {cnh}"),
("Price and Yeomans)","Price and Yeomans {py})"),
("Cava et al.,","Cava et al. {cava},"),
("Jin et al.","Jin et al. {jin}"),
("Adkin and Hayward;","Adkin and Hayward {ah};"),
("Ramsdell symbols","Ramsdell symbols {ram}"),
("Frank and Kasper's major skeleton, Nelson's disclination network","Frank and Kasper's major skeleton {fk58,fk59}, Nelson's disclination network {nel}"),
("AFLOW prototype encyclopedia and the Crystallography Open Database","AFLOW prototype encyclopedia {aflow} and the Crystallography Open Database {cod}"),
("(Sullivan;","(Sullivan {sul};"),
("Sadoc and Mosseri 2016","Sadoc and Mosseri 2016 {sm}"),
("Frank and Kasper 1959","Frank and Kasper 1959 {fk59}"),
("This is Frank and Kasper's and Nelson's picture","This is Frank and Kasper's {fk58,fk59} and Nelson's {nel} picture"),
("Yarmolyuk and Kripyakevich 1974","Yarmolyuk and Kripyakevich 1974 {yk}"),
("tabulated by Deza, Delgado Friedrichs and Dutour Sikirić","tabulated by Deza, Delgado Friedrichs and Dutour Sikirić {dsdd}"),
("Shoemaker and Shoemaker 1986","Shoemaker and Shoemaker 1986 {ss}"),
("Dutour Sikirić, Delgado Friedrichs and Deza (2010)","Dutour Sikirić, Delgado Friedrichs and Deza (2010) {dsdd}"),
('talk "Space fullerenes"','talk "Space fullerenes" {talk}'),
("Dutour Sikirić–Delgado-Friedrichs–Deza table","Dutour Sikirić–Delgado-Friedrichs–Deza table {dsdd}"),
("Morse and Hedlund 1940","Morse and Hedlund 1940 {mh}"),
("Jagannathan and Duneau (2023, Table 1)","Jagannathan and Duneau {jd} (2023, Table 1)"),
("Elser and Henley 1985; Henley;","Elser and Henley 1985 {eh}; Henley {hen};"),
("Elser and Henley 1985)","Elser and Henley 1985 {eh})"),
("Duneau, Mosseri and Oguey 1989","Duneau, Mosseri and Oguey 1989 {dmo}"),
("(Frank and Kasper; Nelson)","(Frank and Kasper {fk58,fk59}; Nelson {nel})"),
("Gvozdetskyi et al. 2014","Gvozdetskyi et al. 2014 {gv}"),
("Dutour Sikirić et al. 2010","Dutour Sikirić et al. 2010 {dsdd}"),
("(Sadoc and Mosseri;","(Sadoc and Mosseri {sm};"),
("Morse–Hedlund;","Morse–Hedlund {mh};"),
("Baake–Grimm;","Baake–Grimm {bg};"),
("Jagannathan–Duneau 2023","Jagannathan–Duneau 2023 {jd}"),
]
i0=body.index('<h2>1. Introduction')   # abstract left without numbers
head,body=body[:i0],body[i0:]
for a,b in SUB:
    n=body.count(a)
    if n==0: sys.exit('MISS '+a)
    body=body.replace(a,b); print(n,'x',a)
order=[]
for m in re.finditer(r'\{([a-z0-9,]+)\}',body):
    for k in m.group(1).split(','):
        if k not in order: order.append(k)
assert set(order)==set(R), set(R)^set(order)
num={k:i+1 for i,k in enumerate(order)}
body=re.sub(r'\{([a-z0-9,]+)\}',lambda m:'['+', '.join(str(num[k]) for k in m.group(1).split(','))+']',body)
refs='\n<h2>References</h2>\n<p class="prec">Outside works cited in the text, numbered in order of first citation; DICTO\'s own papers are listed above. Every entry was checked against the publisher\'s or Crossref\'s record on 1 November 2026, except where the entry says otherwise.</p>\n<ol class="refs">\n'+''.join(f'<li>{R[k]}</li>\n' for k in order)+'</ol>\n'
j=tail.index('</body>') if '</main>' not in tail else tail.index('</main>')
tail=tail[:j].rstrip()+'\n'+refs+tail[j:]
open(P,'w',encoding='utf8').write(head+body+tail)
print(len(order),'references')
