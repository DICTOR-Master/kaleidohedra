# Fixes, batch 1 (sections 01–17)

Japanese Quanta v2 accuracy pass against Quanta of Space v2.1 (English). Each section's -ja.html was rewritten in place to follow the English sentence by sentence; HTML tags, classes, img src paths and DOIs were checked against the English (all match). Items below often bundle several replacements of the same kind.

## Recurring fixes (applied in every section where they occurred)
- Section header "If you held it/them/one": v1 had truncated or wrong renderings (もしあなたがそれを, もしあなたが片側を, もしそれらを手で持ったなら) → 手に取れば (glossary).
- "paper" mistranslated as 紙 / ペーパー / 号紙 → 論文.
- End line "From paper #n, Version v, date. Licence CC BY-SA 4.0." → 論文 #n（第 v 版、日付）より。ライセンス CC BY-SA 4.0。 (glossary); "Volume II" → 第 II 巻 (v1 mixed 巻 II / 巻II / 第2巻).
- "Computation … with Claude (Anthropic)": v1 often said "by Claude" (によって作成/行われました) → Claude（Anthropic）と共に行いました (glossary credit line).
- partner (= dual) → 双対 (v1: 相棒 / パートナー); regular solids given 正 (正四面体, 正八面体, 正十二面体, 正二十面体).
- Spurious （数式・計算の詳細は英語版をご覧ください。） deleted wherever nothing had been left out (01, 03, 04×2, 06×4, 10, 12×2, 13, 15).

## 01 Introduction
1. chapter-mark 導入 → 序論 (glossary "Introduction").
2. lead: 殻（shell）／サイクル（cycle） → 殻／サイクル (English left in text); "固体の集合体" → 正確な立体ピースの組 ("exact sets of solid pieces").
3. broken markup <p><p>…</p></p> → single <p>.
4. 部品 → ピース throughout (glossary "piece"); キット → 一式 (glossary "kit").
5. 原子と虚空 → 原子と空虚 (glossary).
6. Plato: 四面体/八面体/二十面体/十二面体 → 正四面体/正八面体/正二十面体/正十二面体 (regular).
7. Aristotle: "2 つだけ" → 二つ ("only" not in English); "#63" reference was missing → added; 『天体論』第3巻第8節 → 第3巻第8章 (consistent with credit).
8. #65: 正四次元立体 → 四次元の正多胞体 (regular 4-polytopes).
9. #65 title 『赤の女王 120 胞体』 → 『赤の女王 ― 120胞体』 (glossary).
10. Kepler: "小さな単位" → 等しい小さな単位 ("equal" dropped); 正多面体を惑星の球の間に「配置」 → 天球のあいだに入れ子にした ("nested").
11. #8 title ユークリッド・ケプラー・パチョーリ細胞 / 細胞 → ユークリッド＝ケプラー＝パチョーリ・セル / セル (glossary; 細胞 = biological cell).
12. Kepler para: deleted （数式・計算の詳細は英語版をご覧ください。） — nothing was left out.
13. LQG: "空間そのものも同様に量子化されています" kept meaning; Rovelli と Upadhya / Freidel and Speziale (Latin in running text) → ロヴェッリとウパディヤ / フライデルとスペツィアーレ.
14. "明確な違い" → 正直に言えば、違いがあります ("an honest difference").
15. "隅から隅まで常にきっちりフィット" (= thoroughly) → 頂点と頂点を合わせて正確に合います ("corner to corner").
16. Centre: 密詰構造 / 密詰パッキング → 最密充填; カタログ → 目録 (glossary "finite catalogue"); "純粋な積層のどちらかから" → 二つの純粋な積層から; "of every close packing there is" added (存在するあらゆる).
17. Six chapters: ヘカトダイヘドロン → ヘカトディヘドロン; ヘキサ → ヘクサ; ルローのプラトン立体 → ルーローの正多面体 (glossary #45).
18. ディクトニック立体 → ディクトニック立体（DICTONIC SOLIDS） at first use (glossary).
19. data-set title 『DICTO Solids: Exact Geometry』 (English) → 『DICTO の立体 ― 厳密な幾何』 (glossary).
20. Volume II title 『The DICTOnary of Atoms: Quanta of Space II』 → 『原子の DICTOnary ― 空間の量子 II』 (no glossary entry; FLAGGED); 巻 II → 第 II 巻.
21. Bonds: 3 つの DICTONIC BONDS（黄金、鍵形、デリアン） → 三つのディクトニック結合（黄金の結合、キー付きの結合、デロスの結合）; DICTONIC BOND → ディクトニック結合; パチオリのセル → パチョーリ・セル.
22. Shells: "層で閉じられた部分" → ピースがコアの周りに入れ子の層をなして閉じるもの (subject was lost); カルマの連鎖 → 業の連鎖; ダルマの球 → 法の球.
23. Cycles: 九洲心コア → 求心道コア (wrong kanji, wrong name); ユニバーサルパイテト → ユニバーサル・パイテト; OGファミリーのステップ → OG ファミリーの段; ルール → 規則.
24. Stacking: 積み上げ → 積層 (glossary ch.5); "中心にあり" → 上に述べた中心です ("is the centre above").
25. Four dimensions: 4 次元 → 四次元; 120 胞体 → 120胞体（正百二十胞体） (first use); book title (English) → 『不思議の国のアリシア ― 赤の女王と白の女王』.
26. ペンローズタイル → ペンローズ・タイル; 5回対称 → 五回対称.
27. Border: 繰り返す八重構造 → 繰り返すオクテット ("octet" mistranslated as "eight-fold structure").
28. #40 / #30 titles left in English → 『あらゆる積層上の DICTO OG ファミリー』 / 『フィボナッチの背骨』; 『Dharma の球体』 → 法の球; フィボナッチ鎖 → フィボナッチ列; パッキング → 充填.
29. What the pieces show: "二枚のタイルまで含まれています" (= includes up to two tiles) → 二つのタイルにまで絞られます ("down to two tiles").
30. 二つの黄金比の切断 → 二つの黄金切断 (STYLE term).
31. "4 次元の正多面体のコア" → 四次元の正多胞体のコア (regular 4-polytopes, not polyhedra).
32. "アリストテレスが議論した" kept as アリストテレスが論じた.
33. Credit: 導入の資料源 → 序論の出典; 『物の性質について』 → 『事物の本性について』 (glossary); journal names translated (『物理評論速報』, 『生ける一般相対性理論』 etc.) and author names in katakana → restored to Latin (reference lists stay Latin, glossary note 516); Strena title kept in italics after Japanese title.

## 02 #18 The DICTO Hexa
1. sub: ヘキサ・キー → ヘクサ・キー (glossary); 満たす → 充填する.
2. header もしあなたがそれを (truncated) → 手に取れば (glossary).
3. lead: 立方体（cube） → 立方体 (English left); "紙の言葉によれば" → 論文の言葉では ("paper" read as sheet of paper); ペンローズのタイルリングの厚い菱形 → ペンローズ・タイルの太い菱形.
4. "6と2/3のDICTO ジュエル分" → 6 と 2/3 個のジュエル分 (fine; kept).
5. Where: ユークリッド・ケプラー・パチョーリのセル → ユークリッド＝ケプラー＝パチョーリ・セル; "星型八面体…を切り取ります" → 削り取ります ("carve away"); チェス盤 → チェッカーボード (consistency with sub).
6. "Studies" → Studies (world name kept as on screen, per glossary 54).
7. Found: "面と面を合わせて重なることはありません" → 面と面で接することはありません ("meet face to face", not overlap).
8. ヘキサ → ヘクサ, ヘキサ・キー → ヘクサ・キー throughout; "Hexa-Key"/"Hexa" English left → ヘクサ・キー/ヘクサ.
9. "1 つの連続した立体" → ただ一つの立体 ("one single solid").
10. Last para: "8 つのヘキサは、1 つ上の階層にある Kagome Hulls のジュエル菱面体である Hexa-Key の周りに集まります" (made the Hexa-Key the Jewel rhombohedron) → 8 つのヘクサは閉じ込められたヘクサ・キーの周りに集まることができ、これはカゴメ凸包のジュエル菱面体を一段上げたもの ("sealed-in" added; Kagome Hulls → カゴメ凸包).
11. "4 つの切り詰められたジュエル" → 削られたジュエル ("trimmed").
12. Adds: 八面体 → 正八面体; ウィンドウ・ロームス → 窓の菱形; ラルヴァニ → ラルヴァーニ; 10 個の部品 → 10 個のピース.
13. "ステラ（星型多面体）の面内" → ステラの面の平面上 ("stellas' planes").
14. 彫刻 (sculpture) → 彫り込み ("carving"); 彫刻された十二面体 → 彫り込まれた十二面体.
15. "記録にも優先権を主張するものではありません" → この記録は優先権を主張しません; Hexa → ヘクサ.
16. dataref: 第2巻 → 第 II 巻; "体" → 体積 (word truncated); チェック → 検証.
17. credit: 「ヘキサ」 → ヘクサ; 『Kaleidohedra v2026.10.11-octet』 (title marks wrongly) → plain; end line → 論文 #18（第 2 版、2026 年 10 月 20 日）より。ライセンス CC BY-SA 4.0。 (glossary).

## 03 #19 AXE, CLEO and FUJI
1. h1 AXE（アックス）、CLEO（クレオ）、FUJI（フジ） → AXE、CLEO、FUJI (glossary title); katakana kept at first use in lead.
2. sub 3つ → 三つ (glossary).
3. header もしそれらを手で持ったなら → 手に取れば.
4. lead: "斧の刃のような形" → 斧頭の形 ("axe head"); 六角形の角錐 → 六角錐; 日本の藤の花 → 藤（ノダフジ）の花 (glossary 534).
5. caption: "一つのスケールで描かれています" → 三つが蓮の実を充填する、ただ一つの縮尺 ("the one scale at which they fill").
6. header 彼らが解く問題 → 解く問題.
7. 二十面体 → 正二十面体 throughout; "互いに接する二十面体" → 互いの周りに置いた正二十面体 ("placed round each other").
8. deleted （数式・計算の詳細は英語版をご覧ください。） — nothing omitted.
9. "頂蓋を欠いた二十面体（J11）" → 冠を一つ欠いた正二十面体（J11、正五角錐反柱） (glossary J11).
10. "この紙には" → 論文には ("paper" mistranslated as sheet).
11. "その相棒である十二面体" → その双対 (partner = dual, glossary 434); 12 個のキャップ → 12 個の冠.
12. カルマの連鎖 → 業の連鎖 (×3).
13. "形を保ちます" → 丸ごとのまま残ります ("stay whole").
14. Adds: R. W. Gray / Koca らの研究者 → R・W・グレイ / コジャら (running-text names, glossary 516); ケージ → かご; "黄金比のステップ 1 つ先まで" → 黄金の一段より先に (glossary "golden step"); 蓮の実（Lotus seed） → 蓮の実.
15. dataref: ピースの縁 → ピースの辺 ("edges"); 巻 II → 第 II 巻.
16. credit: "…はすべて DICTO によって命名されたものです" (all items as names) → 蓮の実、63 ピースの組み立て、UNITY、業の連鎖、ステラ・コロナ、および…という名称は DICTO のもの (works and names distinguished); トリスクエリオン → トリスケリオン; トリスクエリオン・ヘックス → トリスケリオン・ヘクス; "Claude を使用しました" → Claude（Anthropic）と共に行いました (glossary credit line); version line per glossary.

## 04 #20 The FUJI Family
1. sub: 切り取られた三角形 → 切頂三角形; 空間を埋める新しいペア → 空間を充填する新しい対.
2. header もしあなたが片側を (nonsense) → 手に取れば.
3. lead: 切り取られた三角形 → 切頂三角形 (term made consistent; v1 used three different renderings).
4. caption: FUJI 族のすべて → FUJI ファミリー; 四面体 → 正四面体; 平面の六角形 → 平らな六角形.
5. Where: 「dictosphere」 → DICTOspheres (glossary); "（blunted ones, truncated triangles）" English left → 角を落とした三角形、すなわち切頂三角形.
6. "FUJI が何らかのファミリーに属するかどうかを尋ねてみました。答えは「はい」です" → 調べました。属していました。 (no 尋ねた; plain fact).
7. 正方形反角柱 / 五角形反角柱 → 正四角反柱 / 正五角反柱 (glossary 411); "中間にある" → 中央部である.
8. ピロクロア / 呼吸する → ブリージング・パイロクロア (glossary 480).
9. "立方体と八角錐を同じ深さで切り取ると" → 立方体と正八面体を同じ深さで切ると (octahedron had become an octagonal pyramid).
10. "空間充填のために発見した" → 空間を充填することを見出した; "面は、別のメンバーの底面となっています" → 別のメンバーの底面を面として持ちます (direction reversed).
11. deleted the two （数式・計算…） notes — nothing omitted.
12. Wheels: "問い合わせてみました" → 調べました; "異なるスポークごとに交差する" → どの二枚も異なるスポークに沿って交わるように (each pair along a different spoke); Cleo-Icos (English) → クレオ・イコス.
13. 黄金の菱形六面体 → 黄金菱面体 (glossary); "鋭い角の部分に" → 両方の鋭い先端の ("at each sharp tip").
14. "二十面体の構成ピースは、1つのパートナーとともに" → 正二十面体自身のピースが、一つの相手とともに.
15. Adds: マッカリー → マッカイ (wrong name); "ユークリッドの「第 14 巻」" → ヒュプシクレスによるユークリッド『原論』「第 14 巻」 (Hypsicles dropped).
16. "輪で縛られたもの" (garbled) → 車輪の上限 ("the wheel bound"); 隙間材 → 隙間ピース.
17. dataref: 反角柱の法則 → 規則 (Rule ≠ Law); 部材の表 → メンバーの表; 輪の束縛 → 車輪の上限; 第 2 巻 → 第 II 巻.
18. credit: ディクトスフィア, デルタジップ, B1NR スカルプチャー → DICTOspheres, DeltaZip と B1NR の彫刻 (glossary 191); 切断三角形 → 切頂三角形; "そしてこれらすべてが" → そして名称は ("and the names"); version line per glossary.

## 05 #28 The DICTO Truncated-Icosahedral Hecatodihedron
1. sub: ダルマの球（Spheres of Dharma） → 法の球 (glossary; English left); "1 段階を構築することで得られます" → 一段階を組み立てることで見つかった (a noun phrase, as the English).
2. header もしあなたがそれを → 手に取れば.
3. "切断された正二十面体" → 切頂二十面体 (truncated icosahedron mistranslated).
4. 「Shield（盾）」 → <b>盾</b> (glossary; English left); "同じ平面に広がり、菱形を形成する" → 一つの平面上に平らに並び、合わさって一枚の菱形になる ("merge"); 稜線 → 辺.
5. caption & text: ヘカトダイヘドロン → ヘカトディヘドロン (glossary).
6. Where: ダルマの球体 → 法の球; 二十面体/十二面体 → 正二十面体/正十二面体; 菱三十面体 → 菱形三十面体; 黄金比のステップ分 → 黄金の一段; "back to" (戻ります) restored.
7. 『中間を捉える』 → 『あいだを捉える』 (glossary #27); 固体 → 立体; 部品 → ピース.
8. ひし形 → 菱形.
9. 五稜十二面体（pentakis dodecahedron） → 五方十二面体 (glossary; English left).
10. 半截二十面体（truncated icosahedron） → 切頂二十面体; 相棒 → 双対 (×2).
11. "半截二十面体を結合させたもので、12 の五角形を持つ 5 回対称の頂点を…" → ジョイン切頂二十面体（jtI）の、12 個の五回対称の頂点を五角形のところで平らに切り落としたもの (the known solid "joined truncated icosahedron" had been lost).
12. Adds: コンウェイの六面体変形截角二十面体 → 六方切頂二十面体（hexakis truncated icosahedron） (glossary: English at first use).
13. 準近接体 → それに近い立体（near-miss） (FLAGGED: no settled term).
14. Name sentence: garbled ("…成長の元となった截角二十面体から「truncated-icosahedral」と付けられています") → hecatodi- = 102 faces, Greek "百二", as in ヘカトニコサコロン（正百二十胞体）; 「切頂二十面体型」 = the solid it grows from.
15. dataref: 結合された切断された二十面体 → ジョイン切頂二十面体; 巻 II → 第 II 巻.
16. credit: 「Dharma の球体」シリーズの一形態 → 法の球の一段階 ("a stage"); "Claude によって行われました" → Claude（Anthropic）と共に行いました; version line per glossary.

## 06 #31 The DICTO Ogdoecontahedron
1. h1 DICTOのオグドエコンタヘドロン → DICTO オグドエコンタヘドロン (glossary).
2. sub: "80の面を持つ立体は…で得られます" (sentence) → 入れ子になった殻の一組を裏返すことで見つかった、八十の面を持つ立体.
3. header → 手に取れば.
4. lead: deleted （数式・計算…） — nothing omitted.
5. "どの方向から見ても" → 多くの方向から ("from many sides"); "二十面体" → 二十の面を持つ正多面体、正二十面体 (gloss "the twenty-sided regular solid" was missing).
6. "12 の五つの凧形（kite）の点" → 5 枚の凧形が集まる 12 の点 (English left; garbled).
7. "長さの異なる二種類の辺で接し" → 二種類の長さだけの辺で ("only two lengths").
8. <b>Ogdoecontahedron</b> → <b>オグドエコンタヘドロン</b> (English in running text).
9. caption: 12 個の外部の頂点 → 外側の 12 の点; 水色 → シアン (consistency with #28).
10. 『ダルマの球体』 → 『法の球』; 繰り返し部品 → 繰り返し現れるいくつかのピース; "六角形の蓋が閉じ" → 六角形の上の冠が閉じて.
11. "DICTO は…アイデアを思いつきました" → 入れ子全体を裏返すのは DICTO の着想でした (credit voice; glossary).
12. 殻（shell） → 殻; "平面が角に" → 平らな面が頂点に; 対応するパートナー → 双対; deleted （数式・計算…）.
13. ペンタキス・ドデカヘドロン → 五方十二面体; 凧の形 → 凧形; キャップ → 冠.
14. "内部の二十面十二面体…外部の五十二面体" → 内側の二十・十二面体 / 外側の五方十二面体 ("五十二面体" = 52-hedron, wrong solid); deleted （数式・計算…）.
15. "OG 六角形のコピー同士を六角形同士で" → OG の複製を六角形と六角形で (the copies are of the OG, not of a hexagon); "これも DICTO のアイデアです" → …のも、DICTO の着想でした.
16. 四面体 → 正四面体; ピロクロア格子 → パイロクロア格子.
17. 5 回対称 → 五回対称; "準結晶の一部" → 準結晶のピース; "5 つの異なる方法" → そのような積み方で五通り ("five such ways"); フィボナッチ鎖 → フィボナッチ列; <i>A Fibonacci Spine</i> → 『フィボナッチの背骨』; deleted （数式・計算…）.
18. Adds: "論文「球を介した立体の裏返し、…」で言及されています" (list turned into a paper title) → 論文の中で出典が示されています。球について立体を裏返すこと、…; DICTO の参考文献 → 参考文献ライブラリ; McCooey → マッコイ.
19. "確認された資料には見当たりませんでした" → 調べた資料には見つかりませんでした (glossary).
20. dataref: スタック → 積み重ね; テスト → 検証; 検索されたソース → 調べた資料; 巻 II → 第 II 巻.
21. credit: "ヘカトダイヘドロン（球体の裏返し）" (two items merged) → ヘカトディヘドロン、法の球を裏返すという着想; "計算、厳密な算術、および Claude によるレンダリングは、DICTO によって行われました" (credit reversed) → 計算・厳密な算術・レンダリングは Claude（Anthropic）と共に行いました; ピロクロアネットワーク → パイロクロア・ネットワーク; version line per glossary.

## 07 #31a The DICTO OCD Stella
1. sub: "オグドエコンタヘドロンの相棒" → コンパニオン ("companion" is DICTO's distinct term, not partner/dual; FLAGGED); "継ぎ目で切り離されたもの" → 継ぎ目に沿って切ったもの.
2. header → 手に取れば.
3. lead: 48の角 → 48 の頂点; "すべてが黄金の平面に配置" (all 50 faces) → 六角形と四辺形だけが黄金の平面の上 (the 20 triangles are not).
4. "周囲の二十面体よりも" → 周りの二十面体対称の立体ほど ("icosahedral solids"); 切り込み → 切り方; 「ピライト対称性」 → 黄鉄鉱型 (glossary 423).
5. Where: DICTO Ogdoecontahedron (English) → DICTO オグドエコンタヘドロン; 体心立方格子状 → 体心立方の配置; ゴールデンアダプターピース → 黄金のアダプター・ピース; 実体のある輪郭 → 中身の詰まった一つの輪郭.
6. OCD Stella / Stellas (English, ×10) → OCD ステラ.
7. "互いに向かい合い" → 面と面で接し ("meet face to face").
8. 種子 → 種; Bodhi seed（菩提の種） → 菩提の種; "OCD Stella の対称性はそれよりも低い" → …にもかかわらず (concession restored).
9. ダイヤモンド格子に分裂 → ダイヤモンド・ネットワークに分かれます; イコサヘドロン → 正二十面体 (×2); "考えは DICTO によるもの" → DICTO の着想でした (×3); "凸のピースはちょうど 4 種類に分類" → 隙間はちょうど四種類の凸のピースに分かれます; くぼみ → 切り欠き ("notches"); 八面体 → 正八面体.
10. Atom 13: "DICTOのアイデアをもう一度" → これも DICTO の着想です; "中心に届くまで押し出され" → 中央に触れるまで外へ押し出し ("pushed out until it touches").
11. Adds: "相棒となるパターンの面" → コンパニオンの面の配置; "同じ格子から切り出された菱形三十面体由来の" → 同じ種類の格子の上で菱形三十面体から切り出した ("same kind of lattice"); Kabai → カバイ.
12. "硬い固体の結晶の二種類" → 二種類の硬い立体からなる結晶 (meaning inverted); 四面体/八面体 → 正四面体/正八面体.
13. 切り込みのある → 切り欠きのある; 参考図書館 → 参考文献ライブラリ; "in the sources checked, which included 64 texts" structure restored (調べた資料には…が含まれます).
14. dataref: 巻II → 第 II 巻; 充填 → 充填率 ("fills").
15. credit: katakana word salad (コンパニオン、ステラ・カット、シード、ネーム) → コンパニオン、ステラ形の切り方、種、名称; ピロクロア配列 → パイロクロア配置; 部品 → ピース; パートナー → 相手; "Claude によって作成されました" → Claude と共に行いました; version line per glossary.

## 08 #34a The DICTO Hecatogdoecontahedron
1. sub: "2 つのパートナーとなる立体が1 つに結合した状態" → 一つに組み合わさった、双対の二つの立体 (partner = dual).
2. header → 手に取れば.
3. lead: "…両方を持ってください" (imperative) → 互いに貫通する二つの立体を手にすることになります; 四面体 → 正四面体; "面の隙間から突き出ています" → 面を突き抜けて出ています (no gaps).
4. <b>Hecatogdoecontahedron</b> → <b>ヘカトグドエコンタヘドロン</b>.
5. caption: ヘカトダイヘドロン → ヘカトディヘドロン; 水色 (teal) → 青緑色; 外殻 → 凸包 (glossary "core and hull").
6. Found: パートナー → 双対; "反転させる" → 裏返す; 完全に絡み合います → ちょうどかみ合います; オグドエコンタヘドン (typo) → オグドエコンタヘドロン.
7. "ペアは自分自身のパートナー" → この対はそれ自身の双対.
8. Core: 整流された切断二十面体 (calque "rectified" as electrical rectifying) → 中点切頂した切頂二十面体（rectified truncated icosahedron） (glossary 454 pattern; FLAGGED); ハル → 凸包; 結合された切断二十面体 → ジョイン切頂二十面体; 五面体十二面体 (pentahedral) → 五方十二面体; 相棒 → 双対; 八面体 → 正八面体.
9. 『Progenitors』 → 『始祖』; パートナー化合物 (chemical compounds) → 双対複合体; "古典的な二十面体と十二面体" → 正二十面体と正十二面体の古典的な複合体.
10. Adds: "ある立体とその相棒との組み合わせ" → 立体とその双対の複合体; 五重十二面体 → 五方十二面体; "切頂二十面体の二重化立体" (wrong solid) → 中点切頂した切頂二十面体; "コアや殻" → コアや凸包; 確認した文献 → 調べた資料.
11. Kaleidohedra path: "VAJRA（ヴァジュラ）、および多層殻の鎖" → Vajrayana、および Multi-shell chains (on-screen world names; Vajrayana had become the VAJRA piece).
12. dataref: ハル → 凸包; 巻 II → 第 II 巻.
13. credit: 化合物 → 複合体; "Claude によって作成" → Claude と共に行いました; バージョン 2 → 第 2 版; version line per glossary.

## 09 #35a The DICTO Metaxyhexecontahedron
1. header → 手に取れば.
2. lead: "少し丸みを帯びています" → より鈍くなっています ("blunter"); small rewording of inscribed ball.
3. "DICTO の立体は、その範囲内でちょうど一つの正確なサイズです" → その範囲の中のある一つの正確な大きさのもの; (中間) → （あいだに）.
4. Where: ダルマの球体 → 法の球; 黄金比のステップ → 黄金の一段; イコサヘドロン状の殻をネスト → 二十面体対称の殻を入れ子に.
5. <i>Progenitors</i> / <i>Vajrayana</i> → 『始祖』 / 『金剛乗』 (glossary).
6. "その緩んだステップを引き受けました" → その残っていた段を取り上げました; 菱面三十面体 → 菱形三十面体 (×2); イコサヘドロン → 正二十面体.
7. "DICTO は…と考えました" → …というのは DICTO の着想でした; "これまでにテストされた" → 調べた.
8. Found: メタクサヘクソントヘドロン (typo) → メタクシヘキセコンタヘドロン; トライコンタヘドロン → 菱形三十面体; 5 回/3 回 → 五回/三回.
9. "三角三十面体と新しい立体の間" → 菱形三十面体と… (wrong solid); 同一 → 合同; 二十面体 → 正二十面体; 相棒 → 双対; 裏返しバージョン → 裏返した版; ステップ → 段.
10. Family sentence rewritten to match ("all the skins round a dodecahedron and an icosahedron in this position, as the dodecahedron grows"); カターランの五重十二面体 → カタランの立体の五方十二面体.
11. "説明なしに記されていますが" → 説明のないまま記しておく; "1サイクルあたりの増加分" → 一巡りあたりの正確な倍率 ("exact gain per round"); <i>Progenitors</i> → 『始祖』.
12. Adds: McCooey / Catalan 族 → マッコイ / カタランの立体; "not found" sentence restructured (v1 said the ratio is "not distinguished", a claim; English says no source distinguishes it); "その数は" → その数値は; 検索しても該当する結果は得られません → この名前で検索しても結果は出ません ("the name").
13. Kaleidohedra path VAJRA（ヴァジュラ） → Vajrayana.
14. dataref: 閉じた形 → 閉じた式 ("closed form"); ステップ → 段; 巻 II → 第 II 巻.
15. credit: "Claude によって作成されました" → Claude と共に行いました; version line per glossary.

## 10 #35b The DICTO Palintriacontahedron
1. sub: "内側から外側へ反転した状態" → 裏返した菱形三十面体.
2. header → 手に取れば.
3. lead: ケプラーの菱形十二面体（Kepler's rhombic dodecahedron） → English removed.
4. <i>pálin</i>（「後ろ」） → （「戻って」） ("back" as in turned back); "内側にあり" → 近くにあり ("near in").
5. caption: 二十面体星 → 二十・十二面体の星 (icosidodecahedron star, wrong solid); 外殻 → 凸包; 二十面体 → 正二十面体; structure of the three items restored.
6. Where: "12 の駅からなる黄金サイクル（#35）の「ヴァジュラ」において" → 『金剛乗』（#35）の十二の駅からなる黄金サイクル (Vajrayana had become VAJRA); 二十面十二面体 → 二十・十二面体; 祖先 → 始祖.
7. Quote "より堅固な立体が必要だ" (= a sturdier solid) → 「もう一つの立体が必要だ」 ("one more solid is needed"); "ごまかし" → ずるい (kept sense).
8. パリントリコンヘドロン (typo) → パリントリアコンタヘドロン.
9. Found: "これはアックス（AXE）を裏返したような形です" (AXE!) → これは裏返した菱形三十面体です.
10. メタキシヘクソントヘドロン (×2) → メタクシヘキセコンタヘドロン; 十二面体/二十面体 → 正十二面体/正二十面体; "周りを覆う皮のような構造" → 巻いた皮のファミリー; カタランの五稜十二面体 → カタランの立体の五方十二面体.
11. "その大部分は次の回転の十二面体の内部にあり" → これは次の巡りの正十二面体の内側にあり (the whole solid, not "most of it"); "約 99.46 パーセント" → ほぼすべて、99.46 パーセント ("約" not in English); CLEO（クレオ）星 → クレオ・スター (glossary); 回転 → 巡り.
12. 星形化 → 星型化; deleted （数式・計算…）.
13. Adds: この図形の家族 → このファミリー; "not found" sentence restructured as in #35a; 確認した文献 → 調べた資料.
14. dataref: 閉じた形 → 閉じた式; 巻 II → 第 II 巻.
15. credit: イコシドデカヘドロン → 二十・十二面体; 中央の角錐 → 中心角錐 (glossary); "考え" removed (English: "Flipping … and the name, are DICTO's"); "Claude によって作成" → Claude と共に行いました; 紙番号 → 論文 (paper as sheet); version line per glossary.

## 11 #41 The DICTO Jewel
1. sub: 星々 → 星たち; 十二面体 → 正十二面体.
2. header → 手に取れば.
3. lead: "（厚みのあるペンローズの菱形）" (duplicate) removed; 非周期的 → 決して繰り返さない; "その6辺のそれぞれ" → 六つの側面 ("six sides" = faces of the underlying cube, not edges).
4. caption "Figure 41." → 図 41. (English left).
5. How: 三次元チェス盤 → 三次元のチェッカーボード; 埋め尽くします → 充填します; "the star made of two interlocking tetrahedra" was dropped → 二つの正四面体がかみ合ってできた星 added; 星型八面体がその一部を → 星が.
6. Found: 宝石と星 → ジュエルと星 (name); 食塩の結晶のようなパターン → 食塩の配置; 彫刻された → 削られた; "隣接する立方体によって" → 隣から.
7. Clusters: "DICTO によって単一の立体となり、それぞれの名前" → 彼の名前を持つ単一の立体になります; Jewel-Tetra / -Octa / -Rhombi (English) → ジュエル・テトラ / ジュエル・オクタ / ジュエル・ロンビ (glossary); "窓と窓が向かい合うようにして" → 窓と窓で.
8. Fill: 自由な星 / 緩い星 → ばらの星 ("loose stars"); "そのすべての正則な方法を見つけました" (subject unclear) → 私たちはその規則的な方法をすべて見つけました; 四面体/八面体 → 正四面体/正八面体; "ちょうど重なり合う立体として配置されていますが" → ちょうど収まります。ただしタイル張りとしてではなく、重なり合う立体として (logic restored).
9. Hexa: "#18番の紙" → 論文 #18 ("paper" as sheet); だ・である → です・ます (register).
10. Twins: "ジュエルの双子は DICTO の Ogdoecontahedron に似ています" (wrong: "the Jewel's twin resembles the OG") → ジュエルは DICTO オグドエコンタヘドロンと同じように双晶をなします; 双子 → 双晶 throughout; 維持しない → 保たない.
11. Adds: 部品 → 部分 ("parts"); 『Kagome Hulls』 → 『カゴメ凸包』; Hexa / Hexa-Key (English) → ヘクサ / ヘクサ・キー; "緩い星を含むこれら 3 つのすべての格子タイル" → 三つのクラスターとばらの星による格子状のタイル張りのすべて; "極限を持つオクテットパターン" → オクテットの模様とその限界.
12. Lalvani → ラルヴァーニ; icosahedral 軸 → 二十面体対称の軸; 部品 → ピース; ジュール (typo ×2) → ジュエル; "80 の図書館資料をすべて検索" → 全文を検索した 80 のライブラリ資料; 我々 → 私たち.
13. dataref: 第2巻 → 第 II 巻; 角 → 頂点; Hexa → ヘクサ; 双子 → 双晶.
14. credit: "そのステラ・オクタングラに対する対応物" → その相方である星型八面体; ヘキサ → ヘクサ; "計算、厳密な証明、および Claude による製図" (製図 = drafting drawings; Claude as one item) → 計算・厳密な証明・草稿は Claude（Anthropic）と共に行いました; ペーパー#41 → 論文 #41; version line per glossary.

## 12 #45 The Reuleaux Platonic Solids
1. h1 ルレー・プラトン立体 → ルーローの正多面体 (glossary #45).
2. sub: プラトン立体 → プラトンの立体; 角が丸い立体 → 丸みを帯びた立体.
3. header もしあなたが片側を → 手に取れば.
4. lead: "手に取ったと想像してください" → 手にすることになります; 縁 → 辺; "面影をまだ残した" → まだ覚えている (kept sense).
5. パートナー → 双対; 角 → 頂点; ボール → 球; 八面体/十二面体/二十面体 → 正八面体/正十二面体/正二十面体.
6. Names: ルロー八面体 / ルロー立方体 / ルロー二十面体 / ルロー十二面体 → ルーローの八面体 / 立方体 / 二十面体 / 十二面体 (glossary 308).
7. caption: "固体の辺 1 にある 5 つの物体" → 立体の辺の長さ 1 での五つの立体 ("at solid edge 1"); 固体の直径 → 立体の直径; ラベンダー → ライラック ("lilac"); 元の論文 → 論文.
8. How: 正多面体 → プラトンの立体 (as English); "遠くの頂点" → 最も遠い頂点 ("farthest"); 四面体 → 正四面体; 確認した文献 → 調べた資料; アイデア → 着想.
9. Found: "立体の幅より細くあってはなりません" (prescriptive) → 決して立体の幅より薄くない (a theorem); "それを包む立体よりも細いものは存在しません" → どんなものも、それが内に含む立体より薄くはなれません (direction reversed); 対角する 2 つの角 → 向かい合う二つの頂点.
10. deleted both （数式・計算…） notes — the English gives no formula there either.
11. "パートナーは同意します" → 双対どうしは一致します.
12. 四面体 → 正四面体; 独自の法則 → 独自の規則; "各頂点は他の球の表面のみに接している" → 各頂点が他のただ一つの球の表面の上にしかない ("only one other ball's surface").
13. 最も太い方向 → 最も厚い方向; "未解決の予想として残されています" → 予想として残します.
14. Colours: 対応するパートナー → 双対.
15. Adds: 完全検索した 81 件の図書館資料 → 全文を検索した 81 のライブラリ資料; Sallee → サリー; "実際に読まれていません" → 読んでいません.
16. dataref: 巻II → 第 II 巻.
17. credit: "計算、証明、および Claude を用いた作図は、#45 号紙、バージョン 2…のものです" (garbled; 作図 = drawing; "号紙" = newspaper issue) → 計算・証明・草稿は Claude（Anthropic）と共に行いました。論文 #45（第 2 版、2026 年 10 月 22 日）より; アイデア → 着想; 正多面体 → プラトンの立体.

## 13 #49 The Polyhedral Stretching Theorem
1. h1 多面体の伸縮定理 → 多面体伸長定理 (glossary #49).
2. sub: broken markup <slide>…</slide> removed; 実体 → 立体; "1辺分ずらす" → 辺一つ分の長さだけ滑らせる.
3. header もしあなたが片側を → 手に取れば.
4. lead: "長く、多面体の立体" → 長い、多くの面を持つ立体; ひし形 → 菱形; ベルト → 帯 (throughout).
5. caption: スウィープされた十二面体 → 掃引した正十二面体; 薄紫色 → 菫色 ("violet"); ラベンダー色 → ライラック ("lilac").
6. Where: 紙 #47 → 論文 #47 ("paper"); "交互に置かれています" → 一つおきに ("every other cube"); ヴォイド → 空洞; "DICTO は…アイデアを思いつきました" → …のは DICTO の着想でした.
7. Theorem: "描き出す軌道のすべての辺" → 掃引する形のすべての辺; "辺の長さだけ" → 辺一つ分の長さ; "スライドそのもののコピー" → 滑らせた移動そのものの写し.
8. Faces: "スライド方向にある面" → 滑らせる方向に沿った面; ダイヤモンド型の面がベルト状に広がります → 菱形の帯が育ちます; deleted （数式・計算…）.
9. Equal-edged: <b>DICTO 伸縮立体</b> → <b>DICTO 伸長立体</b> (glossary 188); "伸縮が 1 辺の場合に等辺となり、他の長さでは伸縮します" → 伸ばす長さが辺一つ分なら等辺形、それ以外の長さなら伸縮形 (glossary terms).
10. Caps: キャップ → 冠 (consistent with #19); 四面体 → 正四面体; 十二面体 → 正十二面体; "面の間に正三角形" → 面の中に正三角形 ("among the faces").
11. Every: プラトン立体 → プラトンの立体; 四面体/八面体/二十面体 → 正四面体/正八面体/正二十面体; 「伸ばす」操作 → 伸長.
12. Make: 印刷用ネットは紙に付いており → 論文には印刷用の展開図 ("nets", "paper").
13. Adds: ピッチオット → ピッチョット; ゾノヘドロン → ゾーン多面体 (glossary); フェドロフ → フョードロフ (glossary 516); グルンバウム → グリュンバウム; 5 回 → 五回; 三つ蓋・四つ蓋 → 三つの冠・四つの冠; "on that understanding" was dropped → その理解のうえで added; 半正多面体（アルキメデスの立体） → アルキメデスの立体 (STYLE 3).
14. dataref: イコサヘドロン族の表 → 正二十面体のファミリーの表; 巻 II → 第 II 巻.
15. credit: アイデア → 着想; "計算、証明、および Claude を用いた製図は、紙 #49…付です" (garbled) → 計算・証明・草稿は Claude（Anthropic）と共に行いました。論文 #49（第 2 版、2026 年 10 月 22 日）より.

## 14 #88 short entry + All the atoms
1. h2 "すべての正多面体は、ちょうど2つの黄金比の切り口を持っています" → すべてのプラトンの立体は、ちょうど二つの黄金切断を持つ (STYLE golden cut 黄金切断).
2. 「切断された三角形」 → 切頂三角形 (term).
3. DICTO Solids データセット → データセット『DICTO の立体』 (glossary).
4. Icosaxes, Unborn Axes, White Knight (English) → イコサックス、アンボーン・アックス、白の騎士 (glossary); 単独立体 → 単一の立体; "黄金比 φ の関係" → ちょうど黄金比 φ ("exactly").
5. DICTO-GTT-Solids → DICTO-GTT 立体（DICTO-GTT-Solids） (FLAGGED).
6. "正多面体のすべての角を" → プラトンの立体のすべての頂点を; 黄金比の切断多角形 → 黄金の切頂多角形 ("golden truncated polygon").
7. DICTO-Kepler 黄金切断 → DICTO-ケプラー黄金切頂 ("golden truncations"; FLAGGED); 「大黄金切断立体」と「小黄金切断立体」と呼びます kept as 大黄金切断立体と小黄金切断立体.
8. "空間を埋め合うペア" → 一緒に空間を充填する対; Icosaxes / Unborn Axes → イコサックス / アンボーン・アックス.
9. "#88 のチェック範囲内" → #88 の検証の範囲では; "Volume II のカタログ" → 第 II 巻の目録.
10. "中心から胞体までの距離の…位置で切り取ったスライス" → 中心から胞までの道のりの…位置での断面 (胞, 断面 per STYLE); 24 胞体 → 24胞体（正二十四胞体）; "アルキメデス的なスライス（ちょうど半分）" → ちょうど半分の位置にあるアルキメデスの立体の断面; "正二十面体と正八面体のペア" → 正二十面体の対と正八面体の対.
11. All the atoms: バージョン 1.4 → 第 1.4 版; 『DICTO 原子辞典』 → 『原子の DICTOnary』 (consistency with 01; FLAGGED); "本書には…" (made Volume II = this book) → そこには / 本巻で (Volume II vs this volume kept apart); "37 の新しいクラスター" → 彼の 37 の…; 画像 → 図.

## 15 #8 The Euclid–Kepler–Pacioli Cell
1. h1 ユークリッド・ケプラー・パチオリのセル → ユークリッド＝ケプラー＝パチョーリ・セル (glossary #8).
2. sub: sentence "…内包されています。" → noun phrase 一つの繰り返すセルの 13 点の上に入れ子になった、五つのプラトンの立体すべて.
3. header → 手に取れば.
4. lead: "すべての正多面体" → 他のプラトンの立体 ("the other Platonic solids"); 二十面体/八面体/四面体/十二面体 → 正… ; 相互に絡み合う → かみ合った.
5. caption: 十二面体 → 正十二面体; 二十面体 → 正二十面体; "論文の図 1 から" → より.
6. How: 屋根を設ける → 載せる; "十二の棟の頂点" → 十二の棟の点 ("ridge points"); "中心にある" → 中央の; deleted （数式・計算…）.
7. "6 つの隣接する面の稜" → 六つの隣のセルの棟 ("the six neighbours' ridges", not faces).
8. 『De divina proportione』 → 『神聖比例論』（<i>De divina proportione</i>）.
9. Found: イコサヘドロン/オクタヘドロン/テトラヘドロン (katakana) → 正二十面体/正八面体/正四面体; 繰り返しのセル → 繰り返すセル.
10. "すべての別のセルにある十二面体" (×2) → 一つおきのセルの (every other cell — v1 said "every other" = all the other cells); "重なり合いませ ん" typo fixed.
11. ユークリッド–ケプラー–パチョーリ・ネットワーク → ユークリッド＝ケプラー＝パチョーリ・ネットワーク (glossary).
12. Adds: パチオリ → パチョーリ; "立方体格子の中に" → 立方晶のセルの中に ("cubic cells"); "最も近いとされる" → 最も近いもの、ある種の ("certain"); EKP 格子の点 → EKP セルの点; 折れ目 → 折り返し ("the fold"); 13 点格子 → 13 点のセル; 本稿 → 論文; 2% → 2 パーセント.
13. dataref: エッジチェーン → 辺の連鎖; 被覆率 → 被覆; テスト → 検証; 巻 II → 第 II 巻.
14. credit: この構造 → 構成 ("construction"); "krp-core内のClaude（Anthropic）によって行われました" → krp-core において Claude（Anthropic）と共に行いました; version line per glossary.

## 16 #13 The DICTO Dodeca-13
1. h1 DICTO の十二角十三面体 ("dodecagonal 13-hedron") → DICTO ドデカ13 (glossary #13).
2. sub: "13 個の十二面体を一つに組み合わせて、再びバラバラにしたもの" → 一つの立体にされ、また分解される、十三の正十二面体.
3. header → 手に取れば.
4. lead: ドデカヘドロン (katakana) → 正十二面体.
5. "薄いつばを持つ正十二面体" → 薄いひれを持つ (glossary ひれ付き); 同一 → 合同; "まっすぐに持ち上がります" → まっすぐ持ち上がって外れます ("lift out").
6. caption: DICTO のドデカ -13 → DICTO ドデカ13; 楔形 → 楔 (glossary); 水色 → シアン.
7. Where: "六角形の雪の結晶のような帯状の 6 個" → 六個からなる雪の結晶のような帯 ("hexagonal" added in v1); "固く作りたいと考えていましたが、…" → 中身の詰まった立体にし、さらに…分解できるようにしたい ("made solid … and", not "but").
8. Found: 外部十二面体 → 外側の正十二面体.
9. 「ウェッジ」/「ニードル」 → <b>楔</b>/<b>針</b> (glossary; bold restored as in English); スロット → 溝.
10. "これら 63 個のピースと 13 個の十二面体を組み合わせる" (63 + 13) → 13 個の正十二面体と合わせて、これら 63 個のピースは (the 63 include the 13: 13 + 30 + 20).
11. 3回対称 → 三回対称; 鰭付き → ひれ付き.
12. "コピーをスライドさせるだけの最良の積み重ねは体心立方格子" → 複製を平行移動させるだけで得られる最良の積み方は体心立方.
13. Adds: 黄金色のタイル (golden-coloured) → 黄金のタイル; 接着剤 → つなぎ材 ("binders"); "それを取り外せるユニット" → 持ち上げて外せるユニット; これまでの探索 → 行った検索.
14. dataref: 外殻 → 凸包; パッキング → 充填; 巻II → 第 II 巻.
15. credit: 分離するという要件 → 分解できるという要件; "krp-core におけるデザイン研究と、Anthropic の Claude による検証" → 設計の検討と検証は krp-core において Claude（Anthropic）と共に行いました; version line per glossary.

## 17 #14 The DICTO-Star
1. "Where it started": v1 paragraph was corrupted — one broken sentence followed by about 2,000 repetitions of 二十面体 (runaway output). Whole paragraph translated from the English (physical build from PET caps and security rings round an icosidodecahedron; Polyhedraverse by 4 October 2026; flat-space cousin of a 4D fold; DICTO's idea that cut icosahedra close the gaps; computer search confirmed).
2. sub: 二十面十二面体 → 二十・十二面体; 十二面体 → 正十二面体; 切断された二十面体 → 切った正二十面体; 正確に閉じる → ちょうど閉じる.
3. header → 手に取れば.
4. lead: 部品 → ピース; 二十面十二面体 → 二十・十二面体; キャップ → 冠; "3 つの角が切り落とされた二十面体" → 三つの頂点を切り取った正二十面体.
5. "規則的な面" → 正多角形の面 ("regular faces"); "隙間はありません" → 開いたまま残るところはありません ("nothing is left open").
6. caption: イコシドデカヘドロン → 二十・十二面体; 三減角二十面体 → 三つの頂点を削った正二十面体 (FLAGGED); 水色 → シアン.
7. Found: 稜 → 辺; 部品 → ピース; 詰め物 → 充填ピース ("filler piece").
8. Why: だ・である → です・ます; バーチャルモデル → 仮想模型; 平面空間 → 平らな空間 ("flat space", not "the plane").
9. "それができない理由" (= "the reason it cannot") → これがしないこと ("What it does not do"); 縁 → 辺; 4 次元 → 四次元.
10. "正多面体で空間を埋めることもできません" → 正多角形の面を持つピースによる空間充填へと続けることもできません ("does not continue into a filling of space by regular pieces").
11. "星の格子を作ることはできません" → 星の格子は合いません ("no lattice of stars fits").
12. Adds: "曲がった双曲空間" → 曲がった空間、すなわち双曲空間; 未索引 → 索引に載っていない; "記録には優先権を主張していません" → この記録は優先権を主張しません; 非常に単純 → 十分に簡単 ("simple enough").
13. dataref: チェック → 検証; 巻 II → 第 II 巻.
14. credit: "Polyhedraverse 内で探索される前に構築されました" (wrong: "built before it was explored in Polyhedraverse") → 検索される前に、PET ボトルのキャップで物理的に、また Polyhedraverse で組み立てられました; "krp-core の Claude（Anthropic）によって行われました" → krp-core において Claude（Anthropic）と共に行いました; version line per glossary.

## Count of fixes per section
| Section | Entry | Fixes |
|---|---|---|
| 01 | Introduction | 33 |
| 02 | #18 DICTO Hexa | 17 |
| 03 | #19 AXE, CLEO, FUJI | 16 |
| 04 | #20 FUJI Family | 18 |
| 05 | #28 Hecatodihedron | 16 |
| 06 | #31 Ogdoecontahedron | 21 |
| 07 | #31a OCD Stella | 15 |
| 08 | #34a Hecatogdoecontahedron | 13 |
| 09 | #35a Metaxyhexecontahedron | 15 |
| 10 | #35b Palintriacontahedron | 15 |
| 11 | #41 Jewel | 14 |
| 12 | #45 Reuleaux Platonic Solids | 17 |
| 13 | #49 Stretching Theorem | 15 |
| 14 | #88 + All the atoms | 11 |
| 15 | #8 EKP Cell | 14 |
| 16 | #13 Dodeca-13 | 15 |
| 17 | #14 DICTO-Star | 14 |
| | **Total** | **279** |

## Terms rendered without full confidence (for the lead to decide)
1. Volume II title *The DICTOnary of Atoms: Quanta of Space II* → 『原子の DICTOnary ― 空間の量子 II』 (01, 14). Not in glossary; the DICTO-pun is kept in Latin.
2. *truncated triangle* → 切頂三角形 (04, 14). Glossary has only "flat-ended triangle 角切り三角形"; DICTO's rule is "truncated triangle" only, so 切頂三角形 was used throughout and 角切り三角形 avoided.
3. *companion* (OG's companion, #31a) → コンパニオン. Distinct from partner/dual; no glossary entry.
4. *rectified truncated icosahedron* → 中点切頂した切頂二十面体（rectified truncated icosahedron） (08), following glossary 454's pattern.
5. Johnson-solid *near misses* → それに近い立体（near-miss） (05).
6. *DICTO-GTT-Solids* → DICTO-GTT 立体（DICTO-GTT-Solids）; *DICTO-Kepler golden truncations* → DICTO-ケプラー黄金切頂; *Greater / Lesser Golden Cut solids* → 大黄金切断立体 / 小黄金切断立体 (14). None in glossary.
7. *tridiminished icosahedron* (J63) → 三つの頂点を削った正二十面体 (17 caption); v1's 三減角二十面体 is not a term I could confirm.
8. *stations* of the golden cycle → 駅 (08, 10), kept literal from v1.
9. *twin / twins* (#41) → 双晶 / 双晶をなす (crystallographic twinning).
10. *caps* (on hexagons, in dimples, three- and four-cap forms) → 冠 throughout (03, 06, 13, 17).
11. *Hexa-Key, its partner* (02 sub) → 相棒 kept: here partner is not a dual.
12. Colours: teal → 青緑色, violet → 菫色, lilac → ライラック.
13. STYLE vs glossary: STYLE gives Archimedean solids アルキメデスの立体 and Platonic solids プラトンの立体; the glossary gives 半正多面体（アルキメデスの立体） and 正多面体（プラトンの立体）. I used プラトンの立体 / アルキメデスの立体 where the English says Platonic / Archimedean, and 正多面体 where it says regular solids. 600-cell follows the glossary: 600胞体（正六百胞体） at first use.
14. Reference list in the 01 credit: v1 had translated journal names (『物理評論速報』, 『生ける一般相対性理論』) and put authors in katakana. Restored to Latin (glossary note 516: reference lists stay in Latin). In running text, Rovelli–Upadhya and Freidel–Speziale → katakana.
