# Fixes, batch C (units 027–050: data, work by work, second half; closing DICTONIC section; Kaleidohedra; data set)

Format: per section, v1 → v2, one line, why. Several same-kind changes inside one sentence are grouped on one line.

Conventions applied in this batch (for the lead's final sweep):
- Told line: 「第 I 巻 第n章 …で語られています。」 (v1 dropped "Volume I" in every unit); Findings and apps: 「第 I 巻「発見とアプリ」で語られています。」
- float → 浮動小数点; exact → 厳密; cell (of a lattice) → 単位胞; twin → 双晶; hull → 凸包; corner → 頂点; apex → 錐の頂; Searched → 調査; Open → 未解決; Study commit → 研究コミット; Lemma/Corollary/Proposition → 補題/系/命題.
- Names in running prose → katakana (glossary 516); author–year citation lists (e.g. "Takakura et al. 2007; Keef and Twarock 2009") kept in Latin as reference lists. Software/site names kept (Antiprism, Stella, MathWorld, Polytope Wiki, OEIS, Wolfram Demonstrations, Polyhedra-World).
- face pyramid → 面角錐 and connector → 連結ピース, following atom-names.tsv ("Tetrahedron face pyramid Q", "#47 connector"); glossary line 414 has 中心角錐 for "central face pyramid" — lead to choose one for the whole book.
- Vajra pieces → ヴァジュラ, ヴァジュラ（細）, ヴァジュラ（ねじれ）, ヴァジュラの刃, 五面のヴァジュラ (lead decision + atom-names D18/D42).

## 027 A.37a
1. h2 「DICTOの回転オクテット上のDICTO Ogdoecontahedron」 → 「回転オクテット上の DICTO オグドエコンタヘドロン」 (glossary title; English left in title; DICTO doubled)
2. told line 「第2章 結合で…」 → 「第 I 巻 第2章 結合で…」 (Volume I missing)
3. 「ℚ(√5) 内では正確ですが、浮動小数点としてマークされた部分を除きます」 → 「浮動小数点と記した箇所を除き、ℚ(√5) で厳密です」 (exact = 厳密)
4. セル → 単位胞; 双子層/双子/ツイン → 双晶層/双晶 (twin = crystallographic twin, throughout)
5. 「六角形の辺」 → 「接合六角形の辺²」 (joint missing)
6. 「キャップは両手の各 4 つずつ、計 8 つ」 → 「左右二つの手で 4 + 4 個」 (kept meaning, wording)
7. 双子キャップ「面の 85.41% を超えます」 → 「面の 85.41% の上に立つ」 (over = standing on, not exceeding)
8. Float line: 「OG（オリジナルグリッド）」 → 「OG」 (invented expansion; OG = Ogdoecontahedron); 「5 角形の角」 → 「五回対称の頂点」; "Float:" left in English → 浮動小数点
9. 「中央のピースを鏡像にする」 → 「鏡の中間ピース」 (Mirror middle piece is a noun, glossary); ハル → 凸包; ペンローズのコア → ペンローズ・コア; セルあたり → 単位胞あたり
10. OCD Stella / golden envelope: 結合三角形 → 接合三角形; 「浮遊版」 → 浮動小数点; 角 → 頂点
11. 「ジュエル・パッキング・ツイン（浮遊体）」 → 「ジュエル充填の双晶（浮動小数点）」; 未覆い → 覆われず
12. DBT: 「扁長菱形六面体」 → 「扁平菱面体」 (oblate, not prolate; rhombohedron = 菱面体); 球面性 → 球形度; 「切り取られた頂点の体積」 → 取り除いた頂点部
13. OTT: 「サイズ（フローティング）」 → 「大きさ（浮動小数点）」; 「48 の新しい頂点が現れる」 ok; 79.33% clause re-ordered to say "of its octahedron"
14. Table: headers and words left in English → translated (組（DICTO の命名）/格子/ピース/体積/手/球形度; DICTO 充填セット; 成長した双角錐/四面体; 回転オクテット/オクテット; 一つ/左、右)
15. Sources: 「二進四面体と八面体」 → 「正四面体と正八面体の二種充填」 (binary packing, not binary numbers); スピネル則 → スピネル式双晶則 (lead); 「切り取られた菱形三十面体」 → 切頂菱形三十面体; 5回対称の角 → 五回対称の頂点; 54面の空間充填形 → 空間充填体; 回転ハニカム → 回転した空間充填形（ハニカム）; 積み重ね → 積層; 「オープン」 → 未解決; 「単一の固体」 → 一つの立体 (solid = 立体, not the state of matter); 「コミット」 → 研究コミット
Fixes in this section: 15

## 028 A.40
1. h2 「すべての積み重ねにおける DICTO OG ファミリー」 → 「あらゆる積層上の DICTO OG ファミリー」 (glossary title; stacking = 積層)
2. told line: Volume I added
3. フレーム → 枠組み; セル体積 → 単位胞; ステップ → 段
4. 「双子の法則/適合の法則」 → 「双晶の規則/適合の規則」 (Rule = 規則 per glossary; twin = 双晶)
5. 「中心を通る平面内の鏡 M は −H（n に関する 180 度の回転 H を伴う反転）」 → 「鏡映 M は −H（反転と、n まわりの半回転 H との合成）」 (mirror = reflection)
6. Deleted （数式・計算の詳細は英語版をご覧ください。） (nothing was left out)
7. 「120°回転と層を横切る鏡面反射を持たない」 → 「120° 回転をもち、層を横切る鏡映はもたない」 (MEANING: v1 denied the 120° turn)
8. 「OCD Stella の対称性は浮遊します」 → 「OCD ステラの対称性は浮動小数点での確認」 (float = floating-point check, not "floats")
9. エンベロープ → 黄金の包み; 「上書き」 → 「に代わる」 (supersedes); 「すべての中心対称」 → 「すべて中心対称」
10. 「f 組の双子の角錐」 → 「双晶キャップ f 個」; 「8 − 2f 個の角錐」 → 「キャップ 8 − 2f 個」 (MEANING: caps rendered as pyramids); 各セル → 単位胞あたり
11. フィボナッチ語 → フィボナッチ列 (glossary); 双子の平面 → 双晶面
12. Both tables: headers/words in English → translated (立体/その正八面体の中に/その層の中に/適合/空間に占める割合; はい/いいえ/あらゆる積層/オクテットのみ; ポリタイプ/語/充填/キャップ/双晶キャップ/正四面体/双角錐; 決して繰り返さない; OCD ステラ; 黄金の包み)
13. Checks: 確認 → 検証; 「29 件合格、厳密解」 → 「29 件 PASS、厳密」; Conway, Jiao, Torquato, Jagodzinski, Ramsdell in Latin → katakana (running text); 「Jiao、Torquato」 → 「ジャオとトルクァート」 (one pair); スピネル則 → スピネル式双晶則; 「積層構造」 → これらの積層
Fixes in this section: 13

## 029 A.42
1. told line: Volume I added
2. 「有理数体 ℚ(√5) で厳密に一致します」 → 「ℚ(√5) で厳密です」 (ℚ(√5) is not the rational field; "一致" added)
3. 「（注記：辺の長さが 2 のセルは、体積が 64 倍大きくなります）」 → 「（スクリプトでは辺 2 の単位胞を使い、体積は 64 倍になります）」 (scripts = the computer scripts, not a note); セル → 単位胞
4. 「屋根の部分/十二面体の部分」 → 「屋根／正十二面体」
5. Betke と Henk → ベトケとヘンク (katakana in running text)
6. 「格子の 1/φ³ の正十二面体」 → 「格子の正十二面体の 1/φ³ 倍の正十二面体」 (ambiguous); 「有界な細胞」 → 「有界な領域」 (cells of a plane arrangement, not biological cells); 尖塔 → スパイク
7. 「その内部には、立方体の中に星型八面体が収まっています」 → 「ドッグスターは自身の立方体の星型八面体の内側に収まります」 (MEANING: v1 put the stella inside the Dogstar)
8. Deleted （数式・計算の詳細…） ×3 (nothing left out)
9. 大星 → 大星型十二面体 (great star = great stellated dodecahedron); 「きついフィット」 → 「ぴったり収まる」
10. 「コンタクト：頂点角が 108 度の太いペネローズ菱形」 → 「接触：太いペンローズ菱形 1 枚、稜の点で 108°」 (108° is at the ridge point, not a corner angle; Penrose misspelt)
11. 「対称性を含めるとそれぞれ 2、1、9 種類」 → 「対称性を除いて 2、1、9 通り」 (MEANING: up to symmetry = fewer, not "including"); 「1 枚あたり 4、5、7 個のドッグスター」 → 「ピース 1 個あたり遊離ドッグスター 4、5、7 個」 (per piece, loose); タイルリング → タイル張り
12. Sunstar-Hexa line left entirely in English → translated (サンスター・ヘクサ／サンスター・ヘクサ・キー／比／隣り合うピースごとに菱形 2 枚（全部で 24 枚）)
13. 「屋根の頂点」 → 「屋根の先端」 (tip); ステラ・ジュエル → ステラ＝ジュエル (glossary); ヘキサ → ヘクサ (glossary)
14. Sources: Hart, Walser, Betke and Henk, Euclid, Kepler, Fuller in Latin → katakana; 確認 → 検証; 厳密解 → 厳密; 「φ³膨張したP型二十面体タイル」 → 「P 型の正二十面体対称タイル張りの φ³ 膨張」; 検索：図書館 → 調査：ライブラリ
Fixes in this section: 14

## 030 A.44
1. told line: Volume I added
2. Table 1 headers and solid names in English → translated (面角錐 (atom-names.tsv: 正四面体の面角錐 Q)/底辺の数/二面角（底辺）/側辺の数/二面角（側辺）; 立方体（C）… 正二十面体（I、クレオ・イコス）)
3. 主要定理 → 主定理; 「埋め尽くす」 → 「充填する」 (space-filling term); 面角錐 kept (atom-names.tsv); (b) "iff" restored: 「T が現れるのは O が現れるとき、かつそのときに限ります」 (v1 gave only one direction)
4. 「有理数体 ℚ 上で」 → 「ℚ 上で」; 「接線 2√2…」 → 「正接 2√2…」 (MEANING: tangent of an angle, not tangent line); 「3 つの平方類に属し」 → 「三つの異なる平方類に属し」
5. Conway、Radin、Sadun → コンウェイ、ラディン、サダン
6. 「π を 0 とする加法関数 h」 → 「h(π) = 0 となる加法的な h」; 「底辺の辺は ½ を持つ」 → 「底辺はそれぞれ ½ を担う」
7. 「各オクテットの辺を丸めると 4 × α/2 … = 2π」 → 「オクテットの各辺のまわりで …= 2π」 (MEANING: "round each edge" = around, not rounding off)
8. オクテットセル/セル 2 → オクテットの単位胞/単位胞 2; 「スラブによって定義されます」 → 「板によって得られます」; deleted （数式・計算の詳細…） (nothing left out)
9. 「補題 2: |a N_T…|」 → 「系 2：…」; 「補題 3：アントニウス…」 → 「系 3：…」 (MEANING: Corollaries rendered as Lemmas)
10. 菱形六面体 ×2 → 菱面体 (rhombohedron, glossary); 「三角形の辺の角度」 → 「三角形の辺は」 (dihedral at those edges); 持ちます → 担います
11. Table 2 entirely English → translated (立体/空間を充填する相手/出典; 単独で/古典; 互いに、正八面体 1 個に正四面体 2 個; マウロリコ; フラーのオクテット・トラス; 二十面体オクテット; 提督帽 6 個; 頂点キャップと辺キャップ; 発見 F21; パチョーリ; ジッターバグ)
12. 「整数関係がないことを発見しました」 → 「整数関係を見つけません」 (the test found none; not a discovery of non-existence); 「証明は Lemma 2」 → 「補題 2」
13. Checks: チェック → 検証; 「31 の非空な集合全体」 → 「空でない 31 の集合すべてについての判定」; Lagarias と Zong, Conway…, Debrunner, Lagarias と Moews → katakana; 「第 3 巻第 8 章」 → III.8 kept as in English
Fixes in this section: 13

## 031 A.47
1. h2 「プラトン立体のすべての組み合わせが空間を埋める」 → 「正多面体のどの組み合わせも空間を充填する」 (glossary title)
2. told line: Volume I added
3. Deleted （数式・計算の詳細…） ×4 (nothing left out)
4. Connector table entirely English → translated (連結ピース (atom-names.tsv)/内容/体積; 辺 1 の正八面体の半分; 正四面体の面角錐; 大きさ L の Q; DICTO の六つの提督帽の一つ…パチョーリの位置; ドッグスター…; X, Y per glossary)
5. 「アドミラルキャップ」 → 「提督帽」 (glossary)
6. Lemma 1: 「スラブを任意の順序で積み重ね、タイル空間を繰り返す」 → 「板を任意の順に積み重ねて繰り返すと、空間をタイル張りします」 (MEANING: "tile" is the verb)
7. Lemma 3: 角 → 頂点; オクタヘドロン → 正八面体 (glossary); 「O が欠けると 2 つの P が…」 → 「O がなければ P 2 個、T がなければ Q 4 個」
8. Lemma 4: 「辺上の頂点は黄金比で分割されます。辺の長さ L のオクテットとオクタヘドロンを合わせるとイコサヘドロンと 6 個の A が得られ」 → 「その頂点はこの正八面体の辺を黄金比に分けます；辺 L のオクテットで、正八面体 = 正二十面体 + A 6 個」 (MEANING: octahedron = icosahedron + 6 A, not octet + octahedron); イコサヘドロン/テトラヘドロン → 正二十面体/正四面体
9. 「#44 のカウントマップによる補題 1」 → 「系 1 は #44 の数え上げ写像による」; 「補題 2：P、Q′、A、S、X、Y の 5 つすべて」 → 「系 2：P、Q′、A、S、X、Y を用いて五つすべて」 (MEANING: corollary; "all five" = the five Platonic solids)
10. 「補題 3：辺の長さが L…」 → 「系 3：…」
11. Open list v1 turned into statements (「最も小さなキットです。面と面を合わせて、3 方向に周期性を持ちます」) → 「未解決：連結ピースなしの C + T + O；最小の一式；面と面で接すること；三方向の周期性（…一致するとは限らない）」 (MEANING: these are open problems, not properties)
12. 「切頂正四面体」 → 切頂四面体 (glossary); 「（空間充填形（ハニカム））」 → 「（一様な空間充填形（ハニカム））」 (uniform missing); 橋 → 橋渡し
13. Checks: 「31 個のスタック」 → 「31 の積み重ね」; 「すべての点が合計でちょうど 1 になるようにカバーされる」 → 「どの点も被覆の合計がちょうど 1」; Gabbrielli、Jiao、Torquato、Hart → katakana (ジャオとトルクァート as a pair); パチオリ → パチョーリ (glossary); 既知の文献 → 既知
Fixes in this section: 13

## 032 A.48
1. told line: Volume I added
2. Deleted （数式・計算の詳細…） ×5 (nothing left out)
3. 二十面体/十二面体 → 正二十面体/正十二面体 (glossary); 「セルの体積」/「セルあたり」 → 単位胞; 「循環配置/巡回配置」 → 巡回置換
4. Koca et al. → コジャほか; Mosseri–Sadoc → モッセリ＝サドック (glossary); ロータスジュエル → ロータス・ジュエル
5. 「頂点は c と (±1/(2φ), ±φ/2, 0) のすべての順列」 → 「頂点は c + (…) のすべての置換」 (MEANING: c plus each permutation, not c and the permutations)
6. 「頂点は、x = y におけるコアの鏡像の頂点である」 → 「錐の頂は、コアを x = y で鏡映した像の頂点です」 (apices ≠ corners; register です・ます)
7. Uniqueness: AXE の「角」 → 頂点; 「頂点と面のペア」 → 「錐の頂と面の組」 (apex–face)
8. 「船体の充填率（浮体）」 → 「凸包に対する充填率（浮動小数点）」 (MEANING: hull = convex hull, float = floating point; v1 had "ship's hull, floating body")
9. 「AXE 全体を二十面体に変換すると、星型の割合は 68.2%」 → 「AXE を丸ごと正二十面体に付けると、充填率 68.2% の星になります」 (MEANING: AXE added whole, not converted)
10. キーペア → キー付きの組 (glossary keyed)
11. Theorem 4: 「埋め尽くし」 → 充填; 「立方体の整流化ハニカム」 → 「立方体の空間充填形を中点切頂したもの（rectified cubic honeycomb）」 (rectified ≠ 整流化); 「ケルビン構造」 → ケルビン; 「黄金比のペア」 → 「黄金の組」; deleted note
12. Known: Koca, Koca, Al-Mukhaini, Al-Qanobi → katakana; 「半正則な切頂八面体；…ピリトヘドラル二十面体が得られ、辺の比は正則（√5 − 1）/2」 → 「半一様な切頂八面体；交互化で黄鉄鉱型の二十面体が得られ、辺の比 (√5 − 1)/2 で正二十面体になる」 (MEANING: it is regular at that ratio); 加重ボロノイ細胞 → 重み付きボロノイ領域 (glossary); 「充填は Pm3̄m を持つ」 → 「この充填の対称性は Pm3̄m」
13. Checks: 「結合体と凸包の体積が等しい」 → 「和集合と凸包の体積が等しい」 (union, not "bond"); 正確な値 → 厳密; 「既知の成果には…があります」 → list form as English
Fixes in this section: 13

## 033 A.51
1. told line: Volume I added
2. 「辺 1 の 8 面体」 → 「辺 1 のオクテット」 (MEANING: octet ≠ octahedron); also table title 「8辺の辺長1」 → 「オクテットの辺 1」
3. 「4 つの角錐に分けられ」 → 「錐 4 個からなります」; 「空間を埋め尽くす面錐」 → 「面角錐で、これらは合わせて空間を充填します」 ("together" restored); 二重角錐/二重円錐/円錐 → 二重錐/錐 (cones of a polyhedron, not circular)
4. Classical facts: 「用いる」 restored ("Classical facts used"); 四面体角錐/正方形角錐 → 正四面体の錐/正四角錐; deleted note
5. h3 「HTML:\n主要定理」 → 「主定理」 (broken markup, rule 5)
6. Main theorem: 「隣にある」 → 「接する」; 埋め尽くし → 充填
7. (b) 「T(t) は正八面体の中心に 4 つの頂点を持つ立方体で、t > 1/3 の場合、4 つの三角形と 6 つの六角形が切り落とされます（数式…）」 → 「正八面体の中心にある頂点 4 個を切り落とした立方体（t > 1/3 では三角形 4 枚と六角形 6 枚）、体積 (3 − 2a³)·V_T」 (MEANING: corners are cut, triangles/hexagons are its faces; volume restored instead of the note)
8. Proof: 「3t 倍に拡大された四面体」 → 「3t 倍した正四面体」; 「a 倍に拡大された立方体と、4 枚の平面で切断された立方体」 → 「正八面体を a 倍；立方体を 4 枚の平面で切る」 (MEANING: it is the octahedron that is scaled); 「3 重の頂点を持つ 3 本の辺」 → 「三回対称の頂点に集まる 3 本の辺」; 「他方の種類の隣接する面の切断面」 → 「もう一方の種類の隣のピースの切断面」 (neighbour = piece); deleted note
9. 「確認しました。…厳密に一致します」 → 「検証。有理数の算術で厳密」
10. 「定理2（特別なメンバー）」 → 「定理 2（特別な一員）」
11. 2(a): 「3t = (√6/4)(1 − 3t) という関係から、菱形十二面体の辺の長さは √6/4 となります」 → 「菱形十二面体の辺を √6/4 として、3t = … から」 (MEANING: v1 derived the RD edge from the equation; it is the given); 2(b) likewise for the cube edge 1/√2
12. 2(d): カット立方体/カット菱形十二面体/カットされた角 → 切った立方体/切った菱形十二面体/切り落とした頂点; 「維持します」 → 保ちます
13. Theorem 3: 「切り落とされた立方体」 → 「切った立方体」; オクトット → オクテット (typo); deleted note ×2; 「正確に一致し」 → 「厳密」
14. Slider table: headers and all cells in English → translated (位置/正四面体側のピース/正八面体側のピース; 菱形十二面体, 等辺 (a)/(b), オクテット, 半分ずつ, デロスの結合, サムソン, デリラ, 切った立方体…)
15. h3 「DICTO による命名の 3 つの DICTONIC BOND（結合）」 → 「三つのディクトニック結合（名称は DICTO）」 (glossary DICTONIC BONDS; active credit)
16. Bonds table: English → translated (結合/立体/由来/体積; 黄金/キー付き/デロス; イコサックス + アンボーン・アックス…; 「それぞれ √2/6」)
17. 「黄金色で鍵のかかった体積は二十面体の辺長 1、デリアンは八面体の辺長 1」 → 「黄金とキー付きの体積は正二十面体の辺 1、デロスはオクテットの辺 1 での値」 (MEANING: golden/keyed bonds; octet, not octahedron); Koca たち → コジャほか
18. Remark cube: 「正八面体が配置された正八角形に切り詰められた立方体」 → 「（アルキメデスの）切頂六面体と正八面体」 (regular truncated cubes, glossary 切頂六面体); 「ケルビンの切り詰められた正八面体」 → 「ケルビンの切頂八面体」; 「一様切り詰め立方体空間充填形と一様直交立方体空間充填形」 → 「切頂立方体充填（truncated cubic honeycomb）と中点切頂立方体充填（rectified cubic honeycomb）」 (rectified ≠ 直交); 「実数根号による式」 → 「実数の冪根による表示」; deleted note
19. h3 「黄金の結合、極性」 → 「黄金の結合の極双対」 (polar = polar reciprocal, not polarity); 「DICTO のアイデア」 → 「DICTO の着想」 (rule 8); 「極反転（極性反転）」 → 「極変換」 (glossary); 「極」 → 極双対 throughout
20. 「四角錐六面体の一種」 → 「四方六面体の型」 (tetrakis hexahedron); 「その半分の立方体の辺の長さに対して」 → 「自身の立方体の辺の半分を単位として」; 「比例に関する記述」 → 「これは比率についての主張です」; 鍵付き → キー付き; 「4 つの交互の面」 → 「一つおきの四つの面」
21. Sources: 「四面体の 4 つの角を切り落としたものとしての立方体」 → 「四つの角（錐）を加えた正四面体としての立方体」 (MEANING: inverted — added, not cut off); 「力等分線」 → 「パワー二等分面」 (power bisectors are planes); パワ → パワー; names (Knoll, Morgan, Aurenhammer, Conway, Jiao, Torquato, Gabbrielli, Heath, Wantzel) → katakana; 四面体 - 八面体ハニカム → 正四面体・正八面体の空間充填 (glossary octet)
22. 「均一に切り落とされた立方体と正則化された立方体の空間充填形」 → 「一様な切頂立方体充填と中点切頂立方体充填」 (MEANING: rectified ≠ regularised)
23. Search list: 「4 つの交互する角を切り落とした立方体と八面体」 → 「一つおきの四つの頂点を切り落とした立方体と正八面体」; 「八面体の穴」 → 「四面体空隙と八面体空隙」 (glossary); 親戚 → 類縁; 「DICTO の参考文献」 → 「DICTO の参考文献ライブラリ」; 確認済み → 調べたもの; 未確認 → 調べていないもの
24. 「2 つの正三角形メンバー」 → 「二つの等辺の一員」 (MEANING: equal-edged members, not triangles); 半々メンバー → 半分ずつの一員; 「黄金分割したもの」 → 「黄金比での分割」 (STYLE: never 黄金分割); 立方体の倍積 → 立方体倍積問題; 研究ブランチ → research ブランチ (branch name)
Fixes in this section: 24

## 034 A.50
1. h2 「各 1 手ずつ（DICTO DOI: …）」 → 「一手ずつ <span style="font-weight:400">(DICTO DOI: …)</span>」 (glossary title; the DOI span markup had been lost)
2. told line: Volume I added
3. Lemma 1: 「タイル張りされるための条件は…」 → 「…ならば、L によって空間をタイル張りします」 (English states a sufficient condition "if", not a characterisation); 凸多面体 → 凸体
4. Table entirely English → translated (立体/動き/面；対称性/体積（辺 1）/古典的な構成; ベインの菱形十二面体; 正六角形の長菱形十二面体（F5）; 古典的な長菱形十二面体; ビリンスキーの十二面体; 60° の菱面体; せん断; 伸長; 帯; 単位胞 = 1; マウロリコ)
5. Corners line: 「ℚ(√2) の角（…）…における頂点」 → 「頂点は ℚ(√2)（…）、ℚ(√3)（…）、ℚ(√5)（…）にあります」 (garbled); 伸長十二面体 → 長菱形十二面体 (glossary elongated dodecahedron); ビリンスキ → ビリンスキー; 「接着の確認」 → 貼り合わせの検証, pairs restored (cuboctahedron + pyramids; tetrahedra + octahedron)
6. 「ベイン格子の 3 行目 (0, 0, 1)」 → 「ベイン格子の第三の直線 (0, 0, 1)」 (MEANING: a third free line/direction, not a matrix row); deleted note
7. F1: 「自由な線は、…にあります」 → 「自由な直線：…」 (the angles belong to each line's piece, not positions)
8. Prop. 3: 「ビルinski」 ×2 → ビリンスキー (broken word); 30 面体 → 菱形三十面体; 黄金菱形六面体/菱形六面体 → 黄金菱面体/菱面体 (glossary rhombohedron); 「2 通りの方法で結合できます」 → 「二通りに貼り合わせられ」; 「角が…方向に伸びており」 → 「頂点は…に沿って」; deleted note
9. 「54 件の誤りすべてを検出」 → 「わざと壊したデータ 54 件中 54 件を検出」 (corruptions = deliberately corrupted inputs, not errors found); 相互チェック → 照合
10. 参考文献 → 出典; Fedorov, Grünbaum, Delone, Minkowski, Venkov, McMullen, Maurolico, Bilinski, Wikipedia → katakana (フョードロフ, グリュンバウム (lead list)…); 伸長十二面体 → 長菱形十二面体; 「コミット bdc063d を参照」 → 「研究コミット bdc063d」
Fixes in this section: 10

## 035 A.DB (closing section)
1. h2 「ディクトニック立体と結合」 → 「ディクトニック立体とディクトニック結合」 (glossary closing-section title)
2. told line: Volume I added
3. 「黄金比：」 → 「黄金：」 (the golden bond/loop, not the golden ratio; also in Dual cells and Stops); 「デリアン」 → 「デロス」 throughout (glossary Delian)
4. 「四面体の破片／八面体の破片」 → 「正四面体側のピース／正八面体側のピース」 (pieces, not fragments); 「拡大倍率は 1/√2」 → 「アプリの尺度 1/√2」 (app scale); deleted （数式・計算の詳細…） ×4 (nothing left out)
5. h3 「両方のループは、固定されたサイトに対するパワー図です。」 → 「二つのループはどちらも固定されたサイトのパワー図」 (heading, no full stop)
6. Table "loops": headers and words in English → translated (ループ/サイト（アプリ単位）/重みの差/範囲; 黄金/デロス; 大/小; 体心立方の点; 四面体サイト/八面体サイト; Σn が奇数; ケルビン; オクテット; 立方体; デロスの結合で)
7. パワーセル → パワー領域; 「ウェブは」 → 「結合の網は」 (glossary web of bonds); デロネー → ドロネー (glossary)
8. h3 「結合面と面積（適用単位：黄金 L = φ、デリアン八面体辺 1）」 → 「結合の面と面積（アプリ単位：黄金 L = φ、デロス オクテットの辺 1）」 (MEANING: app units, octet edge, not octahedron edge)
9. Bond-faces table entirely English → translated (結合/面/面積/生まれる／消える/単調か; 大–小 etc.; 狭義単調増加/減少; 「どちらも起こらない」 for never; ケルビンで最大…)
10. Areas paragraph: ビッグ/スモール → 大/小; オクト–テトラ → 八面体–四面体; 「(φ/2)(1,1,1) 方向への並進」 → 「(φ/2)(1,1,1) だけの並進」 (translation by the vector); 「ビッグ–ビッグとスモール–スモールの比は x²」 kept as 大–大/小–小 = x²
11. h3 「ピースあたりの結合数」 → 「ピースあたりの結合」; both bonds-per-piece tables English → translated (黄金 大/小; デロス 八面体側/四面体側; なし（点）; 立方八面体; 正八面体; 立方体)
12. h3 「二重重み付けデロネ細胞」 → 「双対の重み付きドロネー分割の胞」 (MEANING: dual, not double; cells of a subdivision, not biological cells)
13. Golden dual cells: 「bcc スフェン四面体」 → 「体心立方の等面四面体」 (disphenoid; Sphen is a different piece); 「反転なし」 → 「フリップなし」 (flip of the subdivision); 正方形双角錐 → 四角双角錐
14. Delian dual cells: 「角錐（6 O、体積 4/3）」 → 「正八面体（O 6、体積 4/3）」 (MEANING: octahedra rendered as pyramids); 「単一のひっくり返し」 → 「一回だけのフリップ」; Delian → デロス
15. h3 「物理的アンカー：重さ = 半径²、コンタクトマップ」 → 「物理的な拠り所：重み = 半径²、接触写像」 (weight of a power diagram, not physical weight)
16. Contact-map table and window table English → translated (ループ/接触写像/逆写像; 立方体の辺; オクテットの辺; 接触の窓; 窓の両端; 同種の球どうしが接する; ポーリングの 8 配位／4 配位の限界; 重なりのない充填が一つでもある範囲; のみ)
17. 「ストップ値」 → 「停止位置」; 「（ウィンドウ内）」 → 「（窓の中）」; 「デロスの八面体 ρ = 1/2」 → 「デロスのオクテット ρ = 1/2」 (MEANING: octet position); CsCl → 塩化セシウム型 (glossary); 「（適用単位）」 → アプリ単位で; 「イオンを入れ替えた逆蛍石型」 → 「イオンを入れ替えると逆蛍石型」; 面積の同一性 → 恒等式
18. Both ion tables: headers and words English → translated (塩化セシウム型/r（陽イオン）CN/r（陰イオン）CN/x（厳密）/窓; 代用; キー; 内/外; 蛍石型/八面体サイト/四面体サイト/オクテットのどちら側か/同種の結合; 立方晶; 逆; 「外（四面体–四面体が重なる）」; 「外（充填はまだ存在する：t < 2/3）」); ion data unchanged
19. Radii: 「その側面は結論として採用できません」 → 「オクテットのどちら側かは結論になりません」 (MEANING: "side" = side of the octet, not a face); 「窓（t = …）内へ移動」 → 「窓の中に入ります（t = …）」; 除外されたもの → 除いたもの
20. Checks: 検証結果 → 検証; 「371 件合格、0 件不合格」 → 「371 PASS、0 FAIL」; 「相互チェック 105」 → 「アプリとの照合 105」 (app missing); 物理的なアンカー → 物理的な拠り所; 「本研究のために直接読まれていません」 → 「研究のためには読んでいません」
21. Not-found list: 「ソフトおよびハードのハンドオーバー」 → 「穏やかな受け渡しと急な受け渡し」 (glossary hand over); 「双対セル列」 → 「双対の胞の系列」; 「単一タイプメンバーとしてのオクテット」 → 「一種類だけからなる唯一の一員としてのオクテット」 (unique missing); コンタクトマップ → 接触写像; ポーリングウィンドウ → ポーリングの窓; 新規性 → 新しさ
Fixes in this section: 21

## 036 A.22
1. h2 「カルマの連鎖」 → 「業の連鎖」 (glossary #22)
2. told line 「第3章 殻で…」 → 「第 I 巻 第3章 殻で…」
3. Deleted （数式・計算の詳細…） ×3 (nothing left out); 「1 サイクルあたり φ³ です」 → 「φ³ 倍です」
4. 「J2 点が I(1/φ) に着地します：内接円半径」 → 「J2 の頂点は I(1/φ) の上に来ます：内接球の半径」 (inradius of a solid = sphere)
5. 「CLEO は…側面の 5 辺が長さ 1」, 「FUJI は…側面の 5 辺が長さ 1」 → 「側辺 1」 (MEANING: v1 invented "5" side edges); 「頂点が立方体の角に一致」 → 「頂は立方体の頂点」
6. 「チェーン/ステップ」 → 連鎖/段; 「体積は 3 × 10⁻⁹ 以内」 → 「体積の誤差は 3 × 10⁻⁹ 以内」
7. 「1 歩ごとに (12 + φ⁻³)/φ⁶ = 0.6823 ずつ減少」 → 「1 段ごとに … = 0.6823 倍になります」 (MEANING: multiplicative factor, not a subtraction); シエピンスキー → シェルピンスキー; 「と比較」 removed (not in English)
8. 「Dehn スクリーン」 → 「デーン不変量によるふるい分け」 (English left; glossary Dehn invariant)
9. FUJI line: 「CLEO の体積 3 個分」 → 「CLEO と同じ体積のピース 3 個」 (three pieces); 「12 個の直角で、…傾いた部品からなります」 → 「…直角のピース 12 個にも分けられます」 ("also"); deleted note
10. 十二面体の連鎖: 「…に対してそれぞれ 63、175、1,631 個のピースが必要です」 → 「…で 63、175、1,631 ピース」; deleted note
11. 600胞体 → 600胞体（正六百胞体） at first use (glossary); 外接半径 → 外接球の半径; 「蓮の実二十面体」 → 「蓮の実の正二十面体」
12. Surface: 「切り取られた三角形」 → 「切頂三角形」 (lead decision); 「60個の小さな三角形と20個の大きな切り取られた三角形」 → 「小さい切頂三角形 60 枚と大きい切頂三角形 20 枚」 (MEANING: both are truncated triangles); 「C180の80個の六角形は、ゴールドバーグ多面体ではありません」 → 「C180 の六角形 80 枚；ゴールドバーグ多面体ではありません」 (v1 said C180's hexagons are not a Goldberg polyhedron)
13. 参考文献 → 出典; パチオリ → パチョーリ (glossary)
Fixes in this section: 13

## 037 A.23
1. h2 「法の世界」 → 「法の球」 (MEANING: Spheres of Dharma; glossary #23)
2. told line: Volume I added
3. Table entirely English → translated (殻/辺/内側の殻からの充填に使うもの; 正二十面体; 二十・十二面体; 五角錐; ねじれた三角錐台/五角錐台; 36° 回転; 尺度 1/φ の t1; 隙間; 五角形・六角形のキャップ; 楔; 辺のピース; 面のピース; （中心）)
4. Shared core: 二十面体/十二面体 → 正二十面体/正十二面体; deleted note
5. 「30面体の中のケージ」 → 「菱形三十面体（辺 1）の中の籠」
6. 「外側の二十面体がφ³倍され内側と組み合わさる構造」 → 「外側の正二十面体は内側の φ³ 倍」 (MEANING: v1 invented a combining structure)
7. 八面体 → 正八面体; 「辺の長さが 1 の二十面体」 → 「辺 1 の正二十面体」
8. 確認 → 検証; 「双対複合体である五つの正八面体の複合体」 → 「双対の複合体、五つの正八面体の複合体」 (MEANING: two separate known items merged into one); パチオリ → パチョーリ; 「Takakura 他 2007 年、Keef と Twarock 2009 年」 → citation form as English
Fixes in this section: 8

## 038 A.24
1. told line: Volume I added
2. 「φ²の位置にある12個のRT(1)中心」 → 「12 個の RT(1) の中心が中央から φ² の距離にあり」; 「底面内接円の半径」 → 「内接球の半径」 (MEANING: RT has no base; inradius of a solid); 二十面体 → 正二十面体
3. "Hollow" line left in English → translated (中空部；扁長菱面体 20 個；扁平 O／扁長 φO；隙間；外側のくぼみ；内側のくぼみ)
4. Table entirely English → translated (ピース/一式/個数/体積/形; ヴァジュラ (lead decision, one name per shape); 冠の宝珠; 宝冠 L、R (glossary); 双三角錐; 二面角; 頂点; 面; キラル; 黄金菱形の上の角錐)
5. 「n ステップ後の 13ⁿ 個の三十面体」 → 「n 段の後に菱形三十面体 13ⁿ 個」
6. Checks: 「重複はなく（分離軸法）」 → 「重なりなし（分離軸）」; 「236,269 のランダムな点が一度ずつ覆われ」 → 「…がそれぞれちょうど一度覆われる」; 「120 の対称性に対して不変」 → 「120 の対称操作で不変」; キット → 一式 (glossary kit); 「キット B は独立して 235,529 の点を検証しました」 → 「一式 B を独立に：235,529 点」; 形状 → 形
7. 「既知の成果：Kabai（Wolfram デモ）、Kabai、Bérczi、Szilassi」 → 「既知：カバイ（Wolfram Demonstrations）；カバイ、ベールツィ、シラッシ」 (names in running text katakana; two separate sources kept separate)
Fixes in this section: 7

## 039 A.27
1. h2 「間を捉える」 → 「あいだを捉える」 (glossary #27 form)
2. told line: Volume I added
3. Stages table English → translated (構造/主経路の段数/輪を丸ごと加える段階（凸）/輪の一部を加える段階; 法の球; 業の連鎖、蓮の実; 菩提の種、一式 B)
4. Pieces table entirely English → translated with glossary/atom-names names (仏塔, ヴァジュラ（ねじれ）/ヴァジュラの刃/ヴァジュラ（細） (lead: Vajra → ヴァジュラ), クレオ・ロー, モンキー・スタッフ, 盾, 七重の刃, 正五角錐反柱 (J11), 傘蓋, 印相, 冠の宝珠, 宝冠; 蓮の実/法の球/菩提の種/一式 A・B; 三角錐, 六角錐, 錐台, キラル…)
5. 「五角錐 J2」 → 「五角形のキャップ J2」 (pentagonal cap); 「などもあります」 → 「ほかに」 (nothing added); 「モセリ＝サドック t3 の半分サイズの形状」 → 「モッセリ＝サドックの t3 を半分の大きさにした形」 (glossary spelling)
6. 「ロータス・ステージ 2」 → 「蓮の実の段階 2」 (Lotus = the Lotus seed, glossary); ウェニンガー・モデル → ウェニンガーのモデル
7. 「ボディーキットBステージ2」 → 「菩提の種 一式 B の段階 2」 (MEANING: Bodhi seed Kit B; v1 read "body kit")
8. 「ダルマステージ7」 → 「法の球の段階 7」 (Dharma = Spheres of Dharma, glossary 法); 「バージョン3で修正済み」 → 「第 3 版で訂正」
9. 「17 から 86 の面」 → 「面の数 17〜86」
10. Checks: 「融合した体積は各部分の和と一致しました」 → 「融合した立体の体積は、どの場合もピースの体積の和に等しい」; 「A4 用紙 12 枚」 → 「A4 で 12 ページ」; モッセリとサドク → サドック; コカ他 → コジャほか (glossary Koca); コクセター他 → コクセターほか
Fixes in this section: 10

## 040 A.29
1. h2 「テアテトス（DICTO DOI: …）」 → 「テアイテトス <span…>(DICTO DOI: …)</span>」 (glossary name; lost span markup restored)
2. told line: Volume I added
3. Deleted （数式・計算の詳細…） ×3 (nothing left out)
4. 「5 角錐 72 個、四面体 80 個）、計 185 個」 → 「…、計 185 ピース」; 「短く止まります」 → 「手前で止まります」
5. Cleo-Ico: 「側面の辺の長さ」 → 側辺; 「面の中心の点は 10⁻¹⁶ の精度まで一致」 → 「錐の頂は 10⁻¹⁶ まで面の中心に一致」; 「ロック状態」 → 固定（ロック）; シフト → ずらし; 「深さ」 → 食い込み
6. 「二十面体2個を残すと、5 + 2√5の空きが生じます」 → 「二つの正二十面体のあいだに 5 + 2√5 の空きが残ります」 (MEANING: the two icosahedra leave this empty space; nothing is "left behind")
7. Aetos: 「コアの角」 → 頂点; 「間隔」 → 隙間 (gap)
8. Klitzing → クリッツィング (lead list); 「側面の辺の長さは」 → 側辺
9. Fusion: 「クレオ・イコ」 → クレオ・イコス (lead: one name); 「t1＋台形」 → 「t1 + 錐台」 (MEANING: frustum, not trapezoid); 「凸な合併」 → 「凸な和集合」; 「ダルマ」 → 法の球 ×2; 「2/φ でスケール」 → 「2/φ 倍」
10. 「正二十面体の頂点にあるコーン = CLEO（クレオ）-Ico + Kion」 → 「正十二面体の頂点の錐 = クレオ・イコス + キオン」 (MEANING: corner cone of the DODECAHEDRON; Cleo-Ico is not CLEO); Kion → キオン
11. Table entirely English → translated (ピース/個数（段階ごとの版 / 102）(lead: stations → 段階ごとの版)/体積（厳密）; コアの正二十面体（辺 1）; クレオ・イコス; （アトラクトスの中）; ねじれた五角錐台; キャップ; ヘカトディヘドロン; atom names per atom-names.tsv)
12. 「イコシドデカヘドロン」 → 「二十・十二面体」 (STYLE standard term); 「両方の物語を合計すると」 → 「二通りの道筋はどちらも和が…」 (lead: stories → 道筋)
Fixes in this section: 12

## 041 A.34
1. h2 「祖先形（DICTO DOI: …）」 → 「始祖 <span…>(DICTO DOI: …)</span>」 (glossary #34; lost span restored)
2. told line: Volume I added
3. 「正確」 → 厳密; ネスト → 入れ子; 「ダルマサイズ」 → 「法の球の大きさ」 (glossary Dharma = 法)
4. ペア → 組; 「20 の角が接します」 → 「頂点 20 個が接する」
5. 「四重奏」 → 「四つ組」; 「循環順序」 → 巡回順; 「黄金比ではありません」 → 「黄金ではありません」; 「1 ラウンドあたり … の利益を得ます」 → 「1 周ごとに … 倍になります」 (MEANING: "gains" = grows by the factor, not a profit)
6. Search: 「I、ID、D、RT のいずれかを含む」 → 「…に I、ID、D、RT のいずれかを加えて通る」
7. Golden cycle: 「O は 3φ²/4 に位置します」 → 「O の大きさ 3φ²/4」 (size, not position); 「φ⁹ は体積で表されます」 → 「体積で I·φ³/I = … = φ⁹」; deleted note
8. Contact table entirely English → translated (段/接触（厳密）; ゆるい; ぴったり; …すべてが…の面上/辺上; jtI ⊂ RT keeps "80 corners" without "all", as in English)
9. 「十二駅サイクル（vajrayana）：I ⊂ CLEO 星」 → 「12 段階のサイクル（金剛乗）：I ⊂ クレオ・スター」 (glossary Vajrayana, Cleo star; CLEO is a different piece; English word left)
10. Sources: 「反角柱 0.29」 → 「Antiprism 0.29」 (MEANING: the Antiprism software, not an antiprism); 「840 の Conway 形式は、H でも O でもなく」 → 「840 のコンウェイ形は、どれも H にも O にも一致しません」; 外殻 → 凸包 (hull); 「Stella は実行されていない」 → 「実行していません」; Wikipedia, McCooey, Hart, Klitzing, Wenninger, Coxeter, Cromwell, Holden → katakana
Fixes in this section: 10

## 042 A.35
1. h2 「ヴァジュラヤナ」 → 「金剛乗」 (glossary #35)
2. told line: Volume I added
3. 「有理数体 ℚ(√5) において正確に一致し…（浮動小数点としてマークされていない限り）」 → 「浮動小数点と記した箇所を除き、ℚ(√5) で厳密、余り 0」
4. 「12 の駅」/「9 駅接触」 → 「12 の段階」/「9 段階での接触」 (stations = 段階, lead); 「CLEO（クレオ）星」 → 「クレオ・スター」 ×3 (glossary Cleo star; MEANING: not the CLEO piece)
5. Pieces table English → translated (ピース（D′ = (2/3)·D のクレオ・スターによる組み立て）/個数/総体積（厳密）; クレオ・イコス、コア（正二十面体）/スパイク; 内向きの五角錐; 谷の四面体)
6. 「CLEO 星形体 2·I は、三方二十面体の一つの断面であり、星状化（ステレーション）ではありません」 → 「クレオ・スターの体積は 2·I；これはある一つの高さの三方二十面体で、星型化ではありません」 (MEANING: "at one height" = one pyramid height, not a slice; "volume" restored); 「浮遊体」 → 浮動小数点
7. Reach table English → translated (RT をちょうど収める大きさの立体/I·φ³ の面への到達度（浮動小数点）; ヘカトディヘドロン; 二十・十二面体；パリントリアコンタヘドロン; 凧形六十面体; 切頂十二面体; 五方十二面体; 斜方二十・十二面体; 切頂二十面体; 大きすぎる; DICTO メタクシヘキセコンタヘドロン; 1（厳密）)
8. 「角の丸みの半径の 2 乗」 → 「頂点の半径の 2 乗」 (MEANING: corner radii = radii of the corners, nothing is rounded); 「RT から M への変換には 30 個のピースが必要で」 → 「RT → M：ピース 30 個」; ステップ → 段
9. 「M の極」 → 「M の極双対」; 「ダブル・ヴィジョンの両端にある球体」 → 「ダブル・ヴィジョンの端の球」; 「逆のステップ」 → 逆向きの段; deleted note
10. 「パリン・トリコサヘドロン X」 → 「パリントリアコンタヘドロン X」 (MEANING: wrong solid name, glossary); 「浮遊」 → 浮動小数点; CLEO（クレオ）星 → クレオ・スター
11. Sources: 「A.34 に加え」 → 「A.34 と同じものに加え」; 「<b>Kleetope</b>」 → 「クレートープ」 (bold added in v1, English word left; glossary); Grünbaum, Hypsicles → グリュンバウム, ヒュプシクレス; 「反角柱 0.29」 → 「Antiprism 0.29」 (software); 「記述された構造を持っています」 → 「記述どおりの構造をもちます」
Fixes in this section: 11

## 043 A.32
1. h2 「逆転した殻」 → 「裏返しの殻」 (glossary #32)
2. told line 「第4章 サイクルで…」 → 「第 I 巻 第4章 サイクルで…」
3. 「逆鎖 D ⊂ ID ⊂ Ogdoecontahedron」 → 「逆向きの連鎖 D ⊂ ID ⊂ オグドエコンタヘドロン」 (English left); 正確 → 厳密
4. Skin table English → translated (皮（反転テスト、浮動小数点）/ピース/中間で覆われる割合/二重/最も深い重なり; なし)
5. Layer table English → translated (層/ピース/各ピース/厳密な体積; 正十二面体の各面の上の柱; 二十・十二面体の各五角形の上のキャップ; 各正六角形の上の低い角錐; 不規則な楔、頂点 5、三角形 6; 正二十面体の各面の上の三角錐; 各菱形の上の屋根)
6. 「端がぶら下がっている状態（フローティング）では、RT は約 1.894 倍に、内部の D は約 1.232 倍に拡大します」 → 「ゆるみ（浮動小数点）：RT はあと 1.894 倍、内側の D は 1.232 倍まで大きくできます」 (MEANING: "could grow" = room to grow; "loose ends" ≠ dangling; float = floating point); 「タイト・ネスト」 → ぴったりの入れ子; 内接円 → 内接球; 「線形の比率」 → 長さの比
7. Stars: 「星を充填した立体」 → 「中身の詰まった立体としての星」 (MEANING: stars taken as filled bodies); 「体積は 3 個の二十面体」 → 「体積は正二十面体 3 個分」; 「60 個の三角錐」 → 「四面体 60 個」 (tetrahedra); 「点と谷」 → 「先端と谷」; deleted note
8. Inner gap: 「斜方切頂二十・十二面体 × (9 − 3√5)」 → 「六方二十面体 × (9 − 3√5)」 (MEANING: disdyakis triacontahedron, lead decision; v1 named the same solid twice); 「部品は 12、120、50 の 2 種類のキャップ」 → 「ピース 12、120、および 2 種類のキャップ 50」; 「菱二十・十二面体」 → 「斜方二十・十二面体」 (glossary); ロック → 固定
9. Frame: フレーム → 枠; 「隅の半径」 → 頂点の半径; 「長い辺は十二面体の（1 + 2φ = φ³）倍のφ³倍です」 → 「長い辺は正十二面体の辺の φ³ 倍（1 + 2φ = φ³）」 (garbled)
10. Hafner → ハフナー; 「同じ辺長における彼の四面体の体積」 → 「同じ辺での彼の体積」; deleted note
11. Checks: フレーム → 枠; 「両方の次数」 → 「入れ子の両方の順序」 (MEANING: both nesting orders, not degrees); 「正確なゲート」 → 「厳密判定のゲート」; 「既知のケース」 → 既知の場合
Fixes in this section: 11

## 044 A.33
1. told line: Volume I added
2. 「極性は r を ρ²/r へ変換し、φ³の繰り返しにより、半径が φ^3/2 倍の鏡像球を生成します」 → 「極変換は r を ρ²/r に移します；φ³ の繰り返しと合わせると、鏡の球は半径で φ^(3/2) ごとに現れます」 (polarity = polar reciprocation; spheres recur every factor, they are not "generated")
3. 端部設定/中間設定 → 端の設定/中間の設定; 「逆転した回転」 → 「逆向きの巡り」 (turn = one round of the cycle); 浮遊 → 浮動小数点; 「3 倍の I」 → 3·I; 二十面体 → 正二十面体; deleted note
4. "Never both:" missing → 「両立はしない：」 added; ペア → 組
5. 「円錐切断」 → 「錐による切断」; 「1 回転あたり」 → 「一巡りあたり」 (glossary #54 turn); 「すべての交点は凸」 → 「どの共通部分も凸」 (MEANING: intersections of solids, not points); 正確な → 厳密な
6. All three tables: headers/words English → translated (組 1（端）/組 2（中間）/個数/元の層/逆向きの層/体積（厳密）; 元の層/前/端/中間; （丸ごと）; 一巡り); piece codes I1·n unchanged
7. 「I1・10 と I2・9 は互いに完全に貫通しています」 → 「I1·10 = I2·9 はどちらの設定でも丸ごと通ります」 (MEANING: the piece passes uncut in both settings; "=" (same piece) restored; middle dot · restored)
8. 「角の数」 → 頂点
9. Sources: 「高倉他 2007 年；デシャント他…；トワロック他…；フィアッシング」 → citation list as in English (Takakura et al. 2007 …) (kanji 高倉 was a guess; reference lists stay in Latin)
Fixes in this section: 9

## 045 A.38
1. h2 「普遍パイテト」 → 「ユニバーサル・パイテト」 (glossary #38)
2. told line: Volume I added
3. 「HTML:\nルール：T(S) = {x : v·x ≤ v·v for all corners v of S}. Exact in ℚ(√5).」 → 「規則：T(S) = {x : S のすべての頂点 v について v·x ≤ v·v}。ℚ(√5) で厳密。」 (broken markup; English left)
4. 「外接半径φのIDのID」 → 「外接球の半径 φ の ID」 (doubled word)
5. 「各殻は内側の面ごとに1ピース、または1〜2つの合同類を持ちます」 → 「各殻は内側の面ごとにピース 1 個で、合同類は一つか二つ」 (MEANING: both hold, not alternatives); 「それぞれの殻は互いに内側にあり」 → 「それぞれが次のものの内側にあり」; 「自己双対」 → 「…の球に関して自己極双対」; 正確な → 厳密な; deleted note
6. Station table English → translated (段階/面/頂点（半径）; 三角形 20、五角形 12; 菱形 30; 正五角形 12、六角形 20、辺 1 : φ（正二十面体を各辺の 1/(2 + φ) の位置で切ったもの）; 二等辺三角形 60)
7. Shell table English → translated (殻/ピース/各ピースの厳密な体積/隙間（厳密）; 五角形の上に 12、三角形の上に 20; 菱形の上に 30; …)
8. 「半径 φ²/√3 の D′」 → 「外接球の半径 φ²/√3 の D′」; ステージ → 段階
9. 「モンキー・スタッフ B と、12 個の合同なひねられた台形」 → 「モンキー・スタッフ B、合同なねじれた錐台 12 個」 (MEANING: Monkey Staff B IS the 12 frusta; frustum ≠ trapezoid)
10. 「5 面の金剛杵 12 個、3 面の角錐 20 個」 → 「五面の角錐 12 個、三面の角錐 20 個」 (MEANING: five-sided pyramids, not Vajras); 谷型四面体 → 谷の四面体; 「修正版 1 から変更」 → 「第 1 版から訂正」; 「5 面の金剛杵」 → 「五面のヴァジュラ」 (atom-names D42; lead Vajra → ヴァジュラ)
11. OG line: 「OG は ID と RT の間に位置し、ID の 30 の角、60 の 2c − v 点、12 の頂点を形成します」 → 「ID と RT のあいだの OG：頂点は ID の 30 個、点 2c − v の 60 個、錐の頂 12 個」 (MEANING: these ARE the OG's corners; apexes ≠ 頂点); 「変換では…に分けられ」 → 「ID → OG は合同なピース 12 個」; deleted note
12. Sources: パチオリ → パチョーリ; ベルグマン → バーグマン (glossary Bergman); ラルワニ → ラルヴァーニ (glossary); スマランドチェ → スマランダケ (lead); 「面ペダル多面体」 → 「面の垂足多面体」, 「反復ペダル三角形」 → 「反復した垂足三角形」 (glossary pedal = 垂足); マッケイ → マッカイ (glossary); 「検索：87 の図書館資料」 → 「調査：ライブラリ資料 87 件」
Fixes in this section: 12

## 046 A.38a
1. h2 「ケプラー・ポアソ」 → 「ケプラー・ポアンソ」 (typo; glossary)
2. told line: Volume I added
3. All three tables English → translated (辺/尖塔の高さ ÷ 面の半径/星 ÷ コア（体積）; I（コア）; I の上の大星型の星; D1（その凸包）; 小星型の星; スパイク 1 本 = I/10; 尖塔 12 本; 一巡り; 殻/ピース/各ピースの厳密な体積/正体; スパイク/内向きの角錐/谷の四面体/キャップ/新/CLEO の逆数形; 先端/(高さ ÷ 底面の半径)²/その逆数形; 小さい殻・大きい殻)
4. 「φ³は長さあたり1回転で約4.24です」 → 「長さでは一巡りあたり φ³ ≈ 4.24 倍です」 (MEANING: per turn, in length); 「面の距離の3倍、尖塔は√5倍に達します」 → 「面までの距離の 3 倍まで…伸びます」
5. 「扁平化」 → 「ずんぐりして見えます」 (squatter); 「各殻（shell）の残差」 → 「各殻で余り」 (English left); 「すべての近接ペアに対して…存在する」 → 「近接するすべての組に…あります」 (です・ます)
6. Sources: 「クサート」 → 「コクセター」 (garbled name); 「コカ他」 → 「コジャほか」 (glossary Koca); 「アル・ライシ他」 → 「アル＝ライシほか」; 「検索：87件の図書館資料」 → 「調査：ライブラリ資料 87 件」
Fixes in this section: 6

## 047 A.39
1. h2 「DICTO OG ファミリー（DICTO DOI: …）」 → span markup restored
2. told line: Volume I added
3. 「フレーム：外接円の半径φ ⊂ OG ⊂ RT」 → 「枠組み：外接球の半径 φ の ID ⊂ OG ⊂ RT」 (MEANING: the solid ID was missing; circumsphere)
4. 「垂線の足（d/n·n）n」 kept; 「4 つの下降ステップすべてで正確に成り立ちます」 → 「下向きの 4 段すべてで…（厳密）」 (glossary "Four Down"); 「他の 90 の頂点」 → 「残りの 90 頂点」
5. Table entirely English → translated (立体/頂点/面/辺/体積/頂点の半径; 凧形, 正六角形, 菱形, 正五角形, 三角形, 五角形（2 種類）, 等辺の十角形, 二等辺三角形, 四角形)
6. Shells: 剰余 → 余り; v1 prefixed every piece volume with 「差」 (difference) → removed; only the last value of each group is the gap: 「隙間 ≈ 2.02617」 (MEANING: piece volumes were labelled as differences); 「60 個の凧形に」 → 「凧形の上に 60 個」; ひし形 → 菱形
7. Breaks: label 「破れ：」 restored; 「60 TPP の角」 → 「TPP の頂点 60 個」; 「突き出ています」 → 「はみ出します」; 「丸みの広がり」 → 「丸さのばらつき」
8. Sources: 「反垂線と垂線の構成」 → 「反垂足と垂足の構成」 (glossary pedal/antipedal); Smarandache → スマランダケ (lead); Goldberg → ゴールドバーグ; 「検索：…図書館資料 80 件」 → 「調査：ライブラリ資料 80 件」
Fixes in this section: 8

## 048 A.43
1. told line: Volume I added
2. Theorem 1: 「一般版」 → 「一般」; 「細長い正方形の双角錐」 → 「細い四角双角錐」; deleted note
3. Theorem 2: 「二十面体回転対称性」 → 「正二十面体の回転対称性」; 「最適」 → 「この評価は最良」 (sharp); モビウス → メビウス; 「辺の長さは 20.905°…」 → 「辺は…」; deleted note
4. 「補題 1：S_k = …」 → 「系 1：…」 (MEANING: Corollary, not Lemma); 「入れ子状に定義され」 → 「どの k でも入れ子」; マージン → 余裕
5. Theorem 3: 「半径²が…である点に対する極線変換」 → 「半径² … の球に関する極変換」 (MEANING: reciprocation about a sphere, not a point); ビート → 拍 (glossary beat)
6. 「補題 3：極線変換の極線は、元の図形の極線になります」 → 「補題 3：polar(P(S)) = T(polar S)」 (MEANING: v1 turned the formula into a wrong sentence)
7. Cleo Towers: 「外側の ID は c³ で、コアの約 3.11 倍」 → 「外側の ID はコアの c³ ≈ 3.11 倍」; タワー → 塔 (counts)
8. 「ヘックス・アクティス（Hex Aktis）」/「デルトイド・アクティス（Deltoid Aktis）」 → 「ヘクス・アクティス」/「デルトイド・アクティス」 (glossary; English gloss only in the catalogue)
9. OTT: 「38 本の放射線」 → 「光線 38 本」 (MEANING: rays of a solid, not radiation; atom-names "ray" 光線); 「似ている」 → 「相似」 (geometric similarity); 「側面²」 → 「側辺²」
10. 「OG は結果として、2 枚、3 枚、3 枚の形状でそれぞれ塔 80、132、140 を作り上げました」 → 「外へ裏返した OG：塔 80、132、140、形は 2、3、3 種類」 (MEANING: "OG turned out" = turned outward (study og-turned-out), not "as a result"; shapes are kinds, not sheets)
11. 「1 拍あたり 1.52…ずつ大きくなり」 → 「1 拍ごとに 1.52…倍」 (MEANING: growth factor); 「完全な反転（浮遊）」 → 「完全な裏返し（浮動小数点）」
12. 「極座標：…」 → 「極双対：…」 (MEANING: polar solids, not polar coordinates)
13. TQH ribbons: 「曲がり…（浮遊）」 → 「折れ…（浮動小数点）」; 「ダウン 8/9/5/11」 → 「下 8/下 9/下 5/下 11」 (glossary "Four Steps … Down")
14. Sources: 「Takakura 他」「Kroto 他」 → et al. (citation form); 「検索：テキストレイヤー付きの図書館資料 77 件、2026 年 10 月 20 日」 → 「調査：テキスト層のあるライブラリ資料 77 件、2026 年 10 月 21 日」 (MEANING: wrong date; English 21 October)
Fixes in this section: 14

## 049 A.K
1. h2 missing section number → 「A.K DICTO の Kaleidohedra（カレイドヘドラ）」 (A.K restored)
2. told 「巻Iの「発見とアプリ」で語られています」 → 「第 I 巻「発見とアプリ」で…」 (lead: 第 … 巻 form)
3. F1: volume formula 「2·φ/2 + 2·½ = φ²」 restored (v1 gave only φ²); 「DICTO FCCと呼ばれるせん断されたFCC格子をタイル敷き」 → 「せん断した FCC 格子（DICTO FCC）で空間をタイル張り」 (glossary tiling); Fedorov, Lalvani, Grünbaum → katakana (patent numbers kept); 「菱形単面多面体」 → 「菱形の単面体」; ファミリー/メンバー → 族/一員
4. F5: 「ベイン区間」 → 「ベイン伸長」 (MEANING: the Bain stretch, not an interval); ルート → 道筋
5. F10: 「EKP 細胞」 → 「EKP セル」 (glossary: Cell = セル); 「各屋根が自身の 1/φ を保持するため」 → 「各屋根はその 1/φ が残る」 (causal "ため" not in English); 「二十面体の 2 回対称軸」 → 「正二十面体の…二回対称軸」; ひし形 → 菱形
6. F11: 十二面体 → 正十二面体; deleted note
7. F12: 「φ/2（正二十面体の辺の長さが 1 の場合）」 → 「正十二面体の辺 1 で φ/2」 (MEANING: dodecahedron, not icosahedron)
8. F15: 「封じられたステラを囲む八面体クラスターも同様です」 → 「八面体クラスターは封じられたステラのまわりに」 ("likewise" added in v1); deleted note
9. 「Checks:」 left in English → 「検証：」; 「krp-**core**」 → 「krp-core」 (stray markdown); 「すべてのプッシュ時に検証します」 → 「プッシュのたびに実行」
Fixes in this section: 9

## 050 A.D
1. h2 「DICTO 立体：正確な幾何学（DICTO DOI: …）」 → 「DICTO の立体 ― 厳密な幾何 <span…>(DICTO DOI: …)</span>」 (glossary title; lost span restored)
2. told line: 巻I → 第 I 巻
3. Version 2: 「バージョン 2」 → 「第 2 版」; 「ℚ(√5) で正確、またはサムソンとデリラの場合は ℚ(∛2) で正確、小数点以下 15 桁まで」 → 「ℚ(√5)（サムソンとデリラは ℚ(∛2)）で厳密、および小数 15 桁」 (MEANING: exact AND also given to 15 decimals); 「面の巻き方」 → 「面の向き」; 「体積 1 にスケールしたコピー付き」 → 「体積 1 に縮尺した写し」
4. Packings: 「空間を埋める 6 つ（DICTO の斜め立体の 3 つの格子パッキングである、ゴールデン結合、キー結合、デロスの結合）」 → 「空間を充填するもの 6 つ（DICTO の斜交立体の格子充填 3 つ；黄金の結合、キー付きの結合、デロスの結合）」 (MEANING: v1 equated the three lattice packings with the three bonds; they are 3 + 3 = 6; glossary skewed 斜交, golden/keyed bond)
5. 「正確な格子ベクトルと配置は以下の通りです。（数式…）」 → 「厳密な格子ベクトルと配置つき」 (MEANING: nothing follows; the data set contains them); deleted note
6. Inventory line left in English → translated (目録 index.csv：122 行；確立したカタログ番号（ジョンソン、一様多面体、ウェニンガー、ハート、モッセリ＝サドック）と DICTO の D1–D75)
7. check.py: 「…扱うケースも含まれています」 → 「…として確かめる検査も含みます」 (wording kept close)
Fixes in this section: 7

## Count per section
- 027 A.37a: 15
- 028 A.40: 13
- 029 A.42: 14
- 030 A.44: 13
- 031 A.47: 13
- 032 A.48: 13
- 033 A.51: 24
- 034 A.50: 10
- 035 A.DB (closing section): 21
- 036 A.22: 13
- 037 A.23: 8
- 038 A.24: 7
- 039 A.27: 10
- 040 A.29: 12
- 041 A.34: 10
- 042 A.35: 11
- 043 A.32: 11
- 044 A.33: 9
- 045 A.38: 12
- 046 A.38a: 6
- 047 A.39: 8
- 048 A.43: 14
- 049 A.K: 9
- 050 A.D: 7
- **Total: 283**
