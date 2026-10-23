# Differences from v1

v1: tag `v1`, commit `337cdf0`.

| | v1 | v2 |
|---|---:|---:|
| gold pairs that load (train / val / test) | 8,060 / 1,154 / 1,514 | 8,124 / 1,152 / 1,525 |
| rows of other books that load (train / val / test) | 7,599 / 388 / 454 | 11,512 / 728 / 937 |
| unified rows | 24,352 | 46,157 |
| synthetic training pair (lines) | | 120,685 |
| lexicon, parallel and corpus files | | unchanged |

## Gold

Roots and forms, read on the printed page:

| Page | Record | v1 | v2 |
|---:|---|---|---|
| 173 | fe56fd77a429 | ዐሰበ / ተዐስበ | ዐሰበ / ተዐሰበ (the page prints ወተዐሰበ) |
| 224 | cec6f1da85f9 | አንትዐ, መንተዕ, አንተዕ, አንተዓት, አናተዕ; root ነ-ተ-ዐ | አንጉዐ, መንጉዕ, አንጉዕ, አንጉዓት, አናጉዕ; root ነ-ጐ-ዐ |
| 226 | e27dfa30dc1a | ተፀኀዘ / አዕኀዘ; root ፀ-ኀ-ዘ | ተፀንግዐ / አፀንግዐ; root ፀ-ነ-ገ-ዐ |
| 34 | a8f2b85981b1 | ነኰነ, መንኰን | ነስኀ 'stink', መንስኅ (root ነ-ሰ-ኀ) |
| 98 | ffec00d9a7b4 | ምስድሳታት, ትስድሳታት | ምስድስታት, ትስድስታት (plurals) |
| 91 | a308cec52106 | separate records ፈፀመ (train) and ፈጸመ (test) | one record ፈጸመ in test; the ፀ spelling is kept in `spelling_note` |

Moved to test, printed spelling kept, the other spelling noted in `spelling_note`: acc4f9cac1b0 ወፅአ (p.228, also ወጽአ) and 110f07e7677d ፀንሰ (p.109, also ጸንሰ), so ፀ/ጸ spellings of one root share a split.

The ፈፀመ record of p.91 (ፈፀመ, ፍፁም, መፍፅም, ፈፀምት, ፍፅማት) is merged into ፈጸመ; ፍፅማት is kept as the plural ፍጽማት (number p).

Stems, 21 rows, all `basic` in v1 (train 18, val 2, test 1). Basis `page`: the printed entry, its gloss or its neighbouring forms show the stem. Basis `form`: set from the prefix and root of the form only.

| Page | Form | v2 stem | Split | Basis |
|---:|---|---|---|---|
| 84 | አረመ | causative | train | form |
| 84 | አርመመ | causative | train | form |
| 84 | አርመመት | causative | train | form |
| 119 | አቍረሩ | causative | train | page |
| 124 | ተደረ | passive | train | form |
| 147 | ተፈጥረ | passive | train | form |
| 159 | አደቀቀ | causative | train | form |
| 173 | ተዐሰበ | passive | train | page |
| 216 | ተቀጽዑ | passive | train | form |
| 224 | አስትዐ | causative | train | page |
| 226 | ተፀንግዐ | passive | train | page |
| 226 | አፀንግዐ | causative | train | page |
| 230 | አግብኡ | causative | train | form |
| 234 | ወተፀአፀኡ | passive | train | form |
| 252 | ተቀሎኩ | passive | val | page |
| 259 | ተዐልዋ | passive | train | page |
| 259 | ተዐሎክሙ | passive | train | page |
| 280 | ተሐበለይዎሙ | passive | train | form |
| 280 | ኢተሀከይነ | passive | train | page |
| 317 | ተፋቀዱ | reciprocal | val | page |
| 353 | ተገለፍኩ | passive | test | page |

Two test rows are flagged and no longer load: አጠቀ (p.157) and አንብዐ (p.224); the page does not settle whether the stem is causative or basic.

A form cell with two forms of different stems is split into one row per form (`source_variant`).

## Other books (data/unified)

- Labels read on the page for 44 rows of ርባሐ ስም ወአንቀጽ and ግዕዝ ቋንቋ ፪; 26 more rows of ግዕዝ ቋንቋ ፪ relabelled; 20 load as printed because another book has the same row.
- Kidane Wold derivatives whose root no other book gives: class `nominal`, train only. 13 of them held out: 5 share a spelling with another root in another book, 8 are derived verbs.
- Root ቈ-ጠ-ፈ corrected to ቀ-ጠ-ፈ (Kidane Wold prints ይቅጥፍ, ቃጣፍ).
- Held out or excluded as printed slips or exercise forms: ይጸዐዹ, ይጻዕዱ (የግእዝ መማሪያ p.35); nine ወቀደሰ* forms (ግዕዝ ቋንቋ ፪ p.50); others listed in the rows' `status_reason`.
- Of 124 roots found only in Kidane Wold, 11 roots and 11 further forms excluded (loanwords, words of another root, readings not settled).

## Two more books

- The entry lists of ፍሬ ግእዝ (4,039 forms) and of የግዕዝ መማሪያ by ለይኩን ብርሃኑ (1,817 forms) are in `data/books/` and in `data/unified/` (5,856 rows; 249 load: train 176, val 32, test 41). Eight forms of የግዕዝ መማሪያ whose reading is not settled are left out.
- 82 roots found only in these books are added to `data/unified/book_root_splits.tsv` (val 7, test 7, train 68). The synthetic lines of the three of them that the generator writes (ነ-ቀ-ለ, ነ-ኀ-ለ, መ-ገ-ለ; 407 lines) moved from the training pair to `data/synthetic/`.
- A row without a root takes the split of the rows of the same spelling (twin letters merged), so that a spelling sits in one split; gold rows keep their split. 290 rows moved. Such a row of these two books also takes the root of those rows when the entry's headword is that root (20 rows); otherwise its root stays empty. `data/lexicon/book_forms.jsonl` follows the moved rows.
- ጌገየ: every row of this verb is written ገ-ገ-የ (it was ገ-የ-ገ-የ in the p. 69 table and in 16 rows of `data/lexicon/book_forms.jsonl`), and all of them are in train.
- አልቦ (root አ-ለ-በ) is in train with the other forms of its entry.
- Kidane Wold p. 403: the subjunctive of ወረወ is ይውሩ (the page breaks it across a line; it was read as ውሩ).
- Gold p. 284 (record `269827c0b68e`, ሠቀየ / ሣቀየ): class ባረከ, as ፍሬ ግእዝ p. 40 gives it.
- የግዕዝ መማሪያ: three readings settled on the scan and added at the end of its file (lines 1,818-1,820): ኮጱ (p. 25), ኤኀ (p. 37) and ዘኅዝኀ (p. 37, fourth letter ኀ). Five forms whose reading is not settled are still left out.

## Yared Shiferaw's Mesehaf Gese Wesewasew

- The entries of the verb book *Mesehaf Gese Wesewasew* by Yared Shiferaw are in `data/books/yared_shiferaw/forms.jsonl` (12,633 forms of 2,659 entries) and appended to `data/unified/` (ids u029988-u042623; 12,633 rows of this book; 1,546 load: train 1,252, val 119, test 175). Forms of entries whose reading is not settled and forms that cannot be read on the scan are left out. No existing row or id changed.
- Roots keep the book's spelling; labialized letters are distinct (ቈ-ጸ-ረ ≠ ቀ-ጸ-ረ, ኰ-ረ-ጸ ≠ ከ-ረ-ጸ). 275 roots found only in this book are added to `data/unified/book_root_splits.tsv`: 274 in train, ቈ-ረ-በ in test. Rows whose root differs from a val/test root only by a twin letter (ነ-ፀ-ፈ, ሰ-ገ-ዐ, መ-ዘ-ገ-ለ, ኈ-ሠ-ሠ, ቈ-ረ-በ) do not load.
- Rows held back as `CHECK` sit in the same split as the other rows of their root: ሐበለ (ሐ-በ-ለ, geezbook_1z) moves from test to train, and the 9 ቈ-ረ-በ rows of this book move from train to test, beside ቈረበ of ፍሬ ግእዝ.
- 78 Yared Shiferaw entries whose root or stray marks were settled against the printed page are appended (696 forms, ids u044408-u045103; 67 load: train 59, val 3, test 5); the printed headword is kept, ዘመ on p.16 is `EXCLUDED` as the first half of the mark ዘመ ዘ, and 3 roots found only there (ጸ-ተ-ወ, ነ-ገ-ገ-ወ, ዘ-ረ-ጸ) are added to `book_root_splits.tsv` in train. The 20 forms of ደቀ (p.144) take the root ደ-ቀ-ቀ. The names ሙሴ, ሀዊ and ማጎግ are `CHECK`. 14 forms printed before a mark that the entry lists did not hold are appended with that mark (ids u045104-u045117, all `CHECK`): መርሕ, ቁጸል, ስሱ, ስድሱ, ርእስ, ፅረስ, አገር, ጽፈር, ፅፈር, እዘብ, ስነን, ጸፈናት, መበለት, ጋይድ; ቁጸል, ጽፈር and ስነን belong to entries that print no root.
- Of the 14 forms printed before a mark, 6 are nouns with their entry's root (u045104, u045108, u045112, u045114, u045116, u045117; ርእስ, ፅፈር, ስነን and መበለት are singular and load, መርሕ and ጋይድ give no number), and ቁጸል (u045105) takes the root ቈ-ጸ-ለ in test; ስሱ, ስድሱ, ፅረስ, አገር, ጽፈር, እዘብ and ጸፈናት stay `CHECK`. The forms of three entries whose root was settled later are appended (ids u045118-u045142): ዖረ (ዐ-ወ-ረ, p.121, train), ተሳነነ (ሰ-ነ-ነ, p.180, test; only ስኑን, መስነን, ስነናት: the other forms printed there are of ቀ-ረ-ነ) and ትባሕተወ (በ-ሐ-ተ-ወ, p.236, test). Every root keeps the split it already had. None of the 25 appended forms loads: 2 repeat a row already in the file and are `EXCLUDED`, the rest are `CHECK`.

## Ge'ez verb list

- The 1,784 headwords of a 25-page Ge'ez verb list (class marks and Amharic glosses; no title or author printed) are in `data/books/verb_list/forms.jsonl` and appended to `data/unified/` (ids u042624-u044407; 531 load: train 451, val 30, test 50; 1,081 are `EXCLUDED`, 1,071 of them because they repeat a row already in the file). No existing row or id changed.
- 65 roots found only in this list are added to `data/unified/book_root_splits.tsv`, all in train.
- Roots of the same verb in another book: ቆጰረ is ቈ-ጸ-ረ, ለንጰሰ is ለ-ነ-ጸ-ሰ, ገንጰለ is ገ-ነ-ጸ-ለ, አስፌድለወ is ፈ-ደ-ለ-ወ. ተወሕሠ, ተዋህውኀ, ጸቈሰ and አሰውሰጠ stay `CHECK`.
- Roots of the same verb in another book, where the meaning matches: ወቀሰ ወ-ቀ-ሠ, ኮፈረ ከ-ፈ-ረ, ዘኮረ ዘ-ከ-ረ, መሞዐ መ-መ-ዐ, ከልኦ ከ-ለ-አ, ጠሞዐ ጠ-መ-ዐ, አስደለወ ደ-ለ-ወ, ሴሰየ ሰ-ሰ-የ, ረሞፀ ረ-መ-ፀ (a ወ or የ read from the vowel of the headword is not a radical). ጥሕረ, ሠነቀ, ተሠአነ and አስተናአወ keep their own roots; ተደረ (ተ-ደ-ረ) and አሰበ (አ-ሰ-በ) stay `CHECK`, their roots not confirmed. ኀለቈ, አከፈ, አስቆቀወ and አመዐርዐረ stay `CHECK`.
- Roots confirmed by the same verb in the gold paradigms or another book: ጦመረ ጠ-መ-ረ, ተሞዕዐ መ-ዐ-ዐ, አንጦልዐ ነ-ጠ-ለ-ዐ, ቆለወ ቈ-ለ-ወ, አስዖዘዘ ዐ-ዘ-ዘ, አቅዜዘየ ቀ-ዘ-የ (a ወ or የ read from the vowel of the headword is not a radical); መትሀ, ጐርሐ, ቈልቈለ, ርኅበ, ቈንቈነ, ለምአ, ሰጕዐ, ጐጕአ, ፃእፅአ, ምዕከ, ረጕነኰ, ቀልጰወ, ፆተወ, ዐወደ, ዐወገ, ሠበጠ, አከጠ and ፀረፈ keep their own roots.
- A derived stem keeps the root of its base, with the prefix stripped: ተመዝጐለ መ-ዘ-ጐ-ለ, ተሠሀለ ሠ-ሀ-ለ, አንዛህለለ ነ-ዘ-ሀ-ለ-ለ, አርመስመሰ ረ-መ-ሰ-መ-ሰ, አክሞሰሰ ከ-መ-ሰ-ሰ, ተሥዕዐ ሠ-ዐ-ዐ, አንጕዐ ነ-ጐ-ዐ, አስደለወ ደ-ለ-ወ, አስፌድለወ ፈ-ደ-ለ-ወ, ተመኵሰየ መ-ኰ-ሰ-የ. ጸቈሰ, አሰውሰጠ and ሀየጰ stay `CHECK`.
- Class marks settled against the same verb in the gold paradigms: the list class is kept for ቃሕቅሐ, ቆመሰ, ቆበረ, ተጽዕረ, አማዕዘረ, ቀስተወ, አመንሰወ, አመንተወ, አቀምጠወ, አመስከየ, አመክነየ, ዘርከየ and ደርበየ; the list class agrees with the gold for ከረመ, ለጸቀ, ተላጸቀ, ነፈቀ, አልጸቀ, ከልአ, በረከ, አስተብረከ, ሰለወ, ተደለወ, አድለወ, ደለወ, ተጋአዘ, ገአዘ, መረየ, ዐለየ, ዐረየ and አስተጋየደ. Entries whose class differs from the gold stay `CHECK`.

## README

Line counts corrected to the files: synthetic files 121,206 (v1 README: 125,020); `book_forms.jsonl` 14,110 (14,118); gold test records 219 (220).

## Flagged gold rows (2026-10-15)

- All 323 rows listed in `merho_ges_gold_flagged_rows.tsv` were checked against the printed gold pages and Yared Shiferaw's typed edition. Each was corrected or removed; no flagged rows remain.
  - 158 rows that the book does not print as Ge'ez forms were removed from `train`, `val` and `test`: 26 flagged and 18 unflagged repeats of 3ms past headwords that had been labelled as nouns, 32 Amharic glosses and `የ...` subject notes, 17 fragments of the book's class marks (such as `ሰሴ`, `ሳስ`, `እብ`, `ኣብ`, `ኢብ`, `ክብ`, `ብዙ`, `ኩፋኔ`), and rows that were not printed or that ran two words together.
  - Labels corrected: 52 feminine plural adjectives (`-አት`/`-ዋት`/`-ያት` marked `በብ` after `ለሴ`/`ለስ`: `gender` `m` -> `f`), 17 adjectives naming the doer (`ባዕ ሣ ቅ`: `type` `noun` -> `adjective`), and 25 other `type`, `gender`, `number`, `stem` and object-suffix labels.
  - Roots and forms that did not match their section were corrected against the printed book and the typed edition (`ደ-ኀ-ነ` -> `ደ-ኀ-ኀ` on pp. 41-42, `ገ-ደ-ፈ` -> `ገ-የ-ረ` on p. 143, `ቀ-ጠ-ነ` -> `ቀ-ጠ-ጠ` on p. 329, `ለ-አ-ከ` -> `ለ-ከ-አ` on p. 210, `ረ-ገ-በ` -> `ረ-ገ-ዐ` on p. 214, `ጐ-ጐ-ለ` -> `ጐ-ጐ-አ` on p. 231, `ሐ-ቀ-ቀ` -> `ሐ-ቀ-የ` on p. 280, `ነ-አ-የ` -> `ነ-አ-ደ` on p. 310, `ነ-ጐ-ደ-ጐ` -> `ነ-ጐ-ደ-ጐ-ደ` on p. 312, `መ-ለ-ጠ` -> `ሰ-ፈ-ጠ` on p. 329, `አ-ከ-ተ` -> `አ-ከ-ጠ` on p. 329, `ደ-ነ-ደ-ነ` -> `ደ-ነ-ጸ` on p. 341, `ዐ-ሰ-ተ` -> `ዐ-ሰ-ቀ` on p. 156, `ሰ-ከ-ተ` -> `ሰ-ከ-ተ-የ` on p. 290, `ጠ-ጠ-በ` -> `ጠ-በ-ጠ-በ` on p. 181), with a few more spelling corrections.

## Gold paradigms checked against the printed page

- Spellings and roots of 42 gold cells were corrected in place to match the printed page; 7 cells were added at the end of the files (ids up to u045152).
- Record c7abd29c5acf (p.333) has root ገ-ነ-ጰ, as both books print it; its cells are spelled with ጰ (ግኑጵ, ግንጵት, ገነጵ / ገነጵት, ምጕንጳ / ምጕንጳት). The cell ምግናጽ, which the page does not print, was removed.
- 4 more cells were removed (ፅሩፋት, መዕምድ, መሳምን, ኂርት); each removed row is kept as `EXCLUDED` with its reason.

## Rows of other books

- Book rows take their stem, root and class from the printed tables. Rows that the tables show to be copies of another row (same form and labels) are `EXCLUDED`, and the book and page are added to the kept row's `also_in`.
- When a row gets a root, it moves to the split that root already has, so each root stays in one split.

## Layout cleanup
- Merged root corrections into the dictionaries (`inferred_root`); removed duplicate and empty files; moved the literature corpus to `corpora/` and the Geez-Amharic dictionary to `lexicon/`. Training and evaluation data are unchanged.

## 17 October 2026: corrections combined

Seventeen OCR errors in Kidane Wold text corrected from the printed pages; person cleared on noun-list rows; imperative person, number and gender labels and duplicate book rows fixed.

## 17 October 2026: gold cleanup

- Removed 42 example phrases and title abbreviations from the gold tables; fixed two person labels.
- Part of speech set to noun on 745 rows of noun tables.
- Roots corrected to ለ-የ-ለ-የ and ዐ-ወ-የ-ወ; one book row that repeats a gold row folded into it; root ዐ-ወ-የ-ወ added for dictionary entry አዐውየወ.
- Headword on p.129 read as አመንዘረ (root መ-ነ-ዘ-ረ), printed twice with two glosses; lemmas and forms corrected from the pages on pp.40, 320, 337 and 383; two OCR readings corrected in Kidane Wold pp.375 and 455.

## 18 October 2026: readings checked against Yared Shiferaw's dictionary

- p.200 ከረስተነ: forms ክርስቱን, ክርስትንት, ክርስትና, ክርስትናት, ክርስቲያን, ክርስቲያናት as printed in the dictionary; the note and raw reading begin with ከረስተነ.
- p.252 headword read as ሰከዐለወ / ሰካዕለወ, present ይሰከዐሉ.
- p.434 ንግምስምስጤ 'ወግ፣ ታሪክ' (was ንግግር ከምስጤ), a noun; root not settled.
- ፍሬ ግእዝ p.40: tenses set on ጐየ and ፃህየየ (root ጐ-የ-የ for ጐየ); አየየ and ተኀየየ added. They repeat rows that already load and stay `CHECK`.
- ፍሬ ግእዝ p.39: tenses set on ሐለየ, ይሔሊ, የሐሊ.
- ኀየለ: ይኄይል is the present (Kidane Wold p.475); the Year 1 p.34 rows printed with ሀ (ሀየለ, ይሄይል, የሀይል, ሀይሎ, ሀይሎት) moved to root ኀ-የ-ለ, since no book has ሀየለ as a separate word. Repeated rows are `EXCLUDED`; the infinitives are spelled ኀይሎ / ኀይሎት (printed ሀይሎ / ሀይሎት).
- ኀለየ follows the order of ፍሬ ግእዝ p.61 (ቀተለ, with the guttural): present የኀሊ, subjunctive ይኅሊ. A present ይኄሊ read from the dictionary (Yared Shiferaw p.258 በዘይኄልዩ) is added as `CHECK`.
- ተኀየየ / ይትኀየይ (ፍሬ ግእዝ pp.40, 50, 62) are under root ሀ-የ-የ 'ቸል አለ', the spelling the dictionaries give (Yared Shiferaw p.270, Kidane Wold p.368).

## Version 2.1.0 (19 October 2026): clitic forms and an alternate rows file

- `data/clitics/clitic_forms.jsonl`: 68,197 forms with the proclitics ወ, ዘ, ለ, በ, እም (and chains such as ወለ,
  ዘበ, ወእም) and the enclitics ሰ, ኒ, ሂ, ኑ, made by rule from the settled rows of `geez_morphology_rows_reviewed.jsonl` (train 55,720, val 5,349, test 7,128).
  Each copies the root, labels and split of its source row (`base_id`).
- `data/unified/geez_morphology_rows_reviewed.jsonl`: the 1,435 held forms that occur in the AGE corpus, each given a word class, root and note. 621 rows load that did not (22,763 in total);
  they cover 28.9% of AGE tokens by exact form, against 18.3% for the base file. Closed-class words load without
  a root (ከመ, እስመ, እለ, ኵሉ, ናሁ, ምስሌሁ ...); nouns load with roots already attested in settled rows (ሕዝብ ሐ-ዘ-በ,
  ሰብእ ሰ-በ-አ, ምድረ መ-ደ-ረ, ሀገር ሀ-ገ-ረ). Held: 72 rows whose proposed root is not a root of settled rows, 583
  rows of names and primary nouns without a root (422 forms), and rows whose number
  or verb labels are not given. 63 printed roots and 11 splits are replaced; each such row says so in `evidence`.
- The unified check takes an optional rows file and reports documented overrides of book lines.
- The base unified file and the book files are unchanged.

## 22 October 2026: word classes and roots of some common words

- Gold rows: እግዚእ is a noun with root ገ-ዘ-አ (was verb, no root); እሳት is a noun with no root (was verb); ሠለስቱ is a
  numeral with no root (was verb; numerals take no root, its root ሠ-ለ-ሰ is noted in `evidence`); ምድር (p.386) is a
  noun (was verb) and stays `CHECK`: its root መ-ደ-ረ is a test root and the row is in train.
- ልብ: three book rows printed under ለ-በ-ወ take root ለ-በ-በ, the root of the gold row, and its split (train); the
  ፍሬ ግእዝ row that repeats the gold row is `EXCLUDED`.
- ገጽ (Yared Shiferaw p.246) and ሙሴ (p.79, a personal name, now a noun) lose the printed roots ገ-ወ and ኀ-መ-ሰ.
- ውስቴታ, ምስሌከ, ምስሌሁ, ላዕሌሁ (ፍሬ ግእዝ) are prepositions with a pronoun suffix (possessor 3fs, 2ms, 3ms, 3ms) and no
  root; repeated rows are `EXCLUDED`. እስመ is a particle with no root. ሠለስቱ of የግዕዝ መማሪያ p.33 repeats the gold row
  and is `EXCLUDED`.
- New rows from Dillmann, *Lexicon Linguae Aethiopicae* (1865), col. 482-483: the short perfect forms of ብህለ
  ይቤ (3ms), ትቤ (3fs and 2ms), ይቤሉ (3mp), ይቤላ (3fp), root በ-ሀ-ለ, train; and the particle ከማሁ (no root).
- Names: a word class `proper_noun` for personal and place names, which take no root (a root may be kept
  where a book gives one). ሙሴ (Yared Shiferaw p.79) is a `proper_noun` with no root and loads (train).
- Counts: 45,170 unified rows; 22,154 load (train 18,124, val 1,730, test 2,300); `geez_morphology_rows_reviewed.jsonl`: 22,770 load
  (train 18,610, val 1,784, test 2,376); 68,219 clitic forms (train 55,744, val 5,349, test 7,126). No root is in
  more than one split.

## 22 October 2026: spelling variants of one root merged

- 48 pairs of roots that differ only by a sound-alike letter (ሀ/ሐ/ኀ, ሰ/ሠ, ጸ/ፀ, አ/ዐ) and are one root spelled two ways
  are merged under one spelling, chosen by the Bible frequency of the forms and the number of rows (for example ኀ-ለ-ወ
  into ሀ-ለ-ወ, ነ-ፀ-ረ into ነ-ጸ-ረ, በ-አ-ለ into በ-ዐ-ለ, ሠ-አ-ነ into ሰ-አ-ነ). Pairs with different meanings (ሰ-በ-ሐ
  'praise' and ሠ-በ-ሐ, ሰ-ረ-ቀ 'steal' and ሠ-ረ-ቀ 'rise', ...) and pairs with too little evidence stay apart; ጸ-መ-አ /
  ጸ-መ-ዐ stays open.
- Every changed row keeps the printed root in `evidence` (book rows: `note` in `lexicon/book_forms.jsonl`; gold
  records: `spelling_note`). The book files (`data/books/*/forms.jsonl`) carry the merged root.
- Four merged roots had their spellings in two splits; all rows now share one split: ሀ-ለ-ወ (12 train rows of ኀ-ለ-ወ
  to test), ለ-ሐ-የ (5 train rows to test, with ለ-ሀ-የ), ነ-ጸ-ፈ (10 train rows of ነ-ፀ-ፈ to val), ወ-ሐ-ደ (21 val rows
  to train, with ወ-ኀ-ደ); 3 `EXCLUDED` rows of these roots moved with them. Gold records d18e088c3d7e and
  8a40e5b926fa moved from train to test, be17bc2433de from val to train.
- The book row ሥኡን (Yared Shiferaw p.180) repeats the gold row of ሰ-አ-ነ after the merge and is `EXCLUDED`.
- ቀ-ረ-ጸ is merged into ቀ-ረ-ፀ (the gold book lists ቀረጸ inside the ቀረፀ entry); its one row (Ge'ez verb list p.23) was
  already in train with ቀ-ረ-ፀ, so no row changes split.
- Four book rows of Yared Shiferaw repeat a gold row in everything except an empty gender and are `EXCLUDED`: ሕዩስ
  (p.82, gold row u001807), እድው (p.237, u005592), ሳንይ (p.265, u006317), በራሕ (p.22, u010282).
- `book_root_splits.tsv`: the merged-away roots ሠ-ለ-ጠ, ነ-ፀ-ፈ and ከ-ሐ-ለ are removed (the 9 rows of ነ-ፀ-ፈ are
  added to ነ-ጸ-ፈ).
- Counts: gold records train 1,112, val 135, test 223; gold pairs that load 8,091 / 1,153 / 1,555; 45,170 unified
  rows, 22,149 load (train 18,119, val 1,718, test 2,312); `geez_morphology_rows_reviewed.jsonl`: 22,765 load (train 18,605, val 1,772, test
  2,388); 68,204 clitic forms (train 55,729, val 5,313, test 7,162). No root is in more than one split.

## 22 October 2026: numerals take their root

- A numeral now loads only with a root, like a noun; `proper_noun` still loads with no root.
- Cardinals, tens, ordinals and fractions take the root of their unit: ወ-ሐ-ደ (1), ሠ-ለ-ሰ (3), ረ-በ-ዐ (4), ኀ-መ-ሰ (5),
  ሰ-ደ-ሰ (6), ሰ-በ-ዐ (7), ሰ-መ-ነ (8), ተ-ሰ-ዐ (9), ዐ-ሠ-ረ (10 and 20). The earlier note is kept in `evidence`.
- Forms of "two" (ክልኤቱ, ካልእ), ምእት, እምአት, ሺሕ, እልፍ, አእላፍ and እልፈ are `CHECK` (numeral root not settled).
- Each numeral row takes the split of its root: 13 book rows move (ዐ-ሠ-ረ train to val: ዐሠርት, ዐሥሩ, ዕሥራ, ዓሥር,
  ዓሥርት, ዓሥረ, ዓሥሬት, ዓሥራን, ዓሥራት, ዓሥራነ, ዓሥራተ; ተስዑ and አሐዳን val to train). Book rows whose root is on the
  other side of the test split are `CHECK` and keep their split: ሰብዑ, አሐደ (test; root in train), ሰመንት, ሳምን,
  ሳምንት, ሳምናን, ሳምናት (train; ሰ-መ-ነ is in test). In `geez_morphology_rows_reviewed.jsonl` the gold row ዐሠርቱ (train; ዐ-ሠ-ረ is in val)
  is unchanged and still loads with no root.
- Counts: 45,170 unified rows, 22,130 load (train 18,093, val 1,727, test 2,310); `geez_morphology_rows_reviewed.jsonl`: 22,745 load (train
  18,578, val 1,781, test 2,386); 68,144 clitic forms (train 55,648, val 5,340, test 7,156). No root is in more than
  one split among the unified rows.

## 22 October 2026: numeral rows moved to the split of their root

- Seven book rows now load with their root and move to its split: ሰብዑ (ሰ-በ-ዐ) and አሐደ (ወ-ሐ-ደ) test to train;
  ሰመንት, ሳምን, ሳምንት, ሳምናን, ሳምናት (ሰ-መ-ነ) train to test.
- Gold row ዐሠርቱ moves train to val, the split of ዐ-ሠ-ረ. In `geez_morphology_rows_reviewed.jsonl` it is a numeral with root ዐ-ሠ-ረ and
  loads; in the unified rows it keeps its class and status (`NO_ROOT`) and only its split changes. The gold record
  of the numeral table stays in `merho_ges_gold_train.jsonl`: it holds the other numerals, whose roots are in train.
  The move is noted in `evidence`.
- Counts: 45,170 unified rows, 22,137 load (train 18,095, val 1,727, test 2,315); `geez_morphology_rows_reviewed.jsonl`: 22,752 load (train
  18,579, val 1,782, test 2,391); 68,165 clitic forms (train 55,651, val 5,343, test 7,171). No root is in more than
  one split.

## 22 October 2026: the numeral table split by root

- Gold record `056fc8ed75e6` (p.449, the numeral table) keeps 18 forms in `merho_ges_gold_train.jsonl`. The form
  ዐሠርቱ, whose unified row has root ዐ-ሠ-ረ (val), moves to a new record `9f6a3f914c87` in
  `merho_ges_gold_val.jsonl` (same page and raw reading; `source_record_id` names the old record). The id is the
  first 12 hex digits of sha1(`page_number|title_or_lemma|raw_transcription`) with the title suffixed by the form.
- `source_ref` of the 19 unified rows follows the new row positions. The record has no root, so no gold pair
  changes: gold records train 1,112, val 136, test 223; gold pairs that load 8,091 / 1,153 / 1,555.
- Counts unchanged: 45,170 unified rows, 22,137 load (train 18,095, val 1,727, test 2,315); `geez_morphology_rows_reviewed.jsonl`: 22,752
  load; 68,165 clitic forms.

## 22 October 2026: fourteen root merges and seven corrected rows

- Fourteen forms printed under two spellings of one root take the root of their other rows (book rows only; gold
  rows already have it): ሊሉይ ለ-የ-ለ-የ, ስቁር ሰ-ቈ-ረ, ተንባል and ትንቡል ተ-ነ-በ-ለ, ንጽብሩቅ ጸ-በ-ረ-ቀ, አብሐ በ-ወ-ሐ, ዋርስ and
  ውሩስ ወ-ረ-ሰ, ውርዝው ወ-ረ-ዘ-ወ, ዲጉን, ዴግኖ and ዴግኖት ደ-የ-ገ-ነ, ጸሎት ጸ-ለ-የ, ጽልሙት ጸ-ለ-መ. No row changes split.
- Seven rows checked against Dillmann and the Bible: መዝገበ is a noun (root ዘ-ገ-በ); እምነ is a preposition and
  እሙንቱ, እማንቱ are pronouns 3mp and 3fp, all with no root; these four load. ረገመ takes root ረ-ገ-መ and ማሕምም
  ሐ-መ-መ; both stay `CHECK` (no tense and person, no number). መካን keeps መ-ከ-ነ, adjective, unchanged.
- The printed root is kept in `evidence`; the book files (`data/books/*/forms.jsonl`) carry the new root.
- Counts: 45,170 unified rows, 22,141 load (train 18,096, val 1,730, test 2,315); `geez_morphology_rows_reviewed.jsonl`: 22,754 load (train
  18,579, val 1,784, test 2,391); 68,166 clitic forms (train 55,651, val 5,344, test 7,171). No root is in more
  than one split.

## 22 October 2026: 116 names from the New Testament text

- 116 word types of the New Testament verse text that are personal or place names, confirmed in a verse, are new
  rows u045171-u045286: `proper_noun`, no root, `status` empty, `source_ref` the first verse. The form is the word
  as written; `evidence` gives its analysis with the proclitics (ለ, ወ, በ, እም, ዘ, ኦ, ኢ) and enclitics split off,
  e.g. ለ + ዮሐንስ. One word with the negative ኢ has `negated` true. Names that are gold verb rows and አዳም are not
  added.
- Split: a fixed hash of the form (sha256) in the proportions of the rows that load (train 82, val 17, test 17).
  A split that already holds a row of the same form is not used, so 28 names are in a split other than their
  held rows of the same form; names have no root, so no root crosses splits.
- Counts: 45,286 unified rows, 22,257 load (train 18,178, val 1,747, test 2,332); `geez_morphology_rows_reviewed.jsonl`: 22,870 load (train
  18,661, val 1,801, test 2,408); 68,505 clitic forms (train 55,894, val 5,393, test 7,218). No root is in more
  than one split.

## 22 October 2026: six roots corrected against Dillmann

- Roots of six book rows corrected (printed root kept in `evidence`; book files carry the new root): ስን ወ-ሰ-ነ to
  ሰ-ነ-ነ; መንጦላዕት ነ-ጠ-ለ-ዐ to ጠ-ለ-ዐ; ጾታ ጸ-ተ-ወ to ጸ-ወ-ተ; ማዕሌት መ-ዐ-ለ-የ to ዐ-ለ-የ (train to val, the split of
  ዐ-ለ-የ); ዕውድ and ዑድ አ-ደ to ዐ-ወ-ደ (train to test, the split of ዐ-ወ-ደ).
- Corrections that would repeat an existing row (ይዴግን, መዐልት, ጽልመት, ምስፍና, መጽያሕት, ጸበል, ተንተነ, ድቀት) are not applied.
- The six rows stay `CHECK`, so counts are unchanged. No root is in more than one split.

## 22 October 2026: names share the split of their earlier rows

- 27 of the 116 New Testament names (`proper_noun`) had a form already present in earlier book rows of another
  split; each moves to that split, so every form sits in one split (for example ኢየሱስ val to train, ሄሮድስ train to
  val, ኢሳይያስ train to test). ሰሎሞን stays in val: its earlier rows are in train and in test.
- Counts: 45,286 unified rows, 22,257 load (train 18,195, val 1,741, test 2,321); `geez_morphology_rows_reviewed.jsonl`: 22,870 load (train
  18,678, val 1,795, test 2,397); 68,504 clitic forms (train 55,939, val 5,376, test 7,189).

## 22 October 2026: roots of rootless rows, three root corrections, 23 forms of the Bible text

- 49 rows with no root whose word has exactly one root in other rows (forms of ቃል, ስም, ቤት,
  አብ, ብእሲ, ግብር, ልብስ, ጽድቅ, ሰላም, ኀይል, ወልድ, and the verbs አምጽአ, ቦኡ, ይበውእ) take that root and the split
  it sits in (e.g. ብእሴ train to val, ግብረ val to test, ስሙ test to train). Rows that lack the number, tense or
  stem stay `CHECK`; ወልድ, አልባስ, አቡሁ and ቃል now load (one ቃል row repeats a loading row in `geez_morphology_rows_reviewed.jsonl`
  and is `EXCLUDED` there). Rows whose letters do not hold the root, a gold row, an `EXCLUDED` row and ኵሎ (a
  rootless pronoun in `geez_morphology_rows_reviewed.jsonl`) are not changed. Book files carry the new root and split.
- Roots corrected against Dillmann (printed root kept in `evidence`): ወርቅ ኀ-በ-ረ to ወ-ረ-ቀ; ዐውድ አ-ደ to ዐ-ወ-ደ
  (train to test, the split of ዐ-ወ-ደ); እፎ 'how' is an `adverb` with no root and now loads.
- እምነ (u019563): possessor 1cp.
- 23 new rows from the Bible verse text with a full analysis in a verse outside the held-out chapters (e.g.
  እንተ relative pronoun f sg, አምጽኡ causative past 3mp, ተጋብኡ reciprocal past 3mp, ደቂቁ, ውሉደ, ሰባዕቱ, በበ,
  ስምዖን, ልያ). A rooted row takes the split of its root; a rootless one a fixed hash of the form.
- Counts: 45,309 unified rows, 22,285 load (train 18,218, val 1,742, test 2,325); `geez_morphology_rows_reviewed.jsonl`: 22,897 load (train
  18,700, val 1,796, test 2,401); 68,585 clitic forms (train 56,005, val 5,379, test 7,201). No root is in more
  than one split.

## 22 October 2026: roots of two gold rows, two ጸዓዳ rows, a መርዓ row

- Gold rows (row-level root in the gold file; the record root is unchanged): በዳ (u006430, p.289) በ-ደ-የ to
  በ-ደ-ወ (train, the split of በ-ደ-ወ); ጸዓድው (u011550, p.313) ጸ-ዐ-ደ to ጸ-ዐ-ደ-ወ. With its new root ጸዓድው repeats
  gold row u011393, so it is listed in `merho_ges_gold_flagged_rows.tsv` and is `EXCLUDED` in the unified rows.
- Book rows ጸዓዳ (u039762) and ጸዓድው (u039763) ጸ-ዐ-ደ-ወ-ደ to ጸ-ዐ-ደ-ወ, printed root kept in `evidence`, train to
  test (the split of ጸ-ዐ-ደ-ወ); ጸዓድው repeats u037882 and is `EXCLUDED`. The book file carries the new root and split.
- New row መርዓ 'wedding' (u045310), noun singular, root መ-ረ-ዐ-ወ (a dictionary entry, s.v. አመርዐወ; Hos 4:13), train,
  the split of መ-ረ-ዐ-ወ. Gold መርዓ (u010647, መ-ረ-ዐ) is unchanged.
- መርሶ (u011757) is not changed: ረ-ሰ-ወ is a train root in the gold and the gold row is in test.
- Counts: 45,310 unified rows, 22,285 load (train 18,219, val 1,742, test 2,324); `geez_morphology_rows_reviewed.jsonl`: 22,897 load (train
  18,701, val 1,796, test 2,400); 68,585 clitic forms (train 56,008, val 5,379, test 7,198); gold pairs train 8,091,
  val 1,153, test 1,554. No root is in more than one split.

## 22 October 2026: fix-ups of the Dillmann corrections

- ስን (u035659) back to ወ-ሰ-ነ ('boundary'), test; stays `CHECK`.
- ማዕሌት (u038912, ዐ-ለ-የ, val): number s; it then repeats gold row u009889 and is `EXCLUDED`.
- ዕውድ (u039712): class adjective (participle); stays `CHECK` (no number). The other rows of its entry
  (u039710, u039711, u039713–u039719, u039721–u039723, u039725) አ-ደ to ዐ-ወ-ደ (printed root kept in `evidence`),
  train to test, the split of ዐ-ወ-ደ; the book file carries the new root and split. ዑድ (u039724) stays `CHECK`.
- Counts unchanged. No root is in more than one split.
- ዕውድ (u039712): number s (gender f as printed, unresolved); it then repeats gold row u011170 and is `EXCLUDED`. Counts unchanged.

## 22 October 2026: መርሶ 'harbor' to ረ-ሰ-ወ

- Gold record 1544b0c3ef6e (p.382, nouns ending in ስ/ሶ) moved from the test to the train gold file (appended), so
  that ረ-ሰ-ወ, a train root, is in one split. Its row 40 መርሶ (u011757, pl. መራሰው) takes the row root ረ-ሰ-ወ and loads
  (noun m sg); the old root is kept in `evidence`. The record root stays empty: the other 55 rows are unrelated names
  with no root; their unified rows move from test to train with the record. መ-ረ-ሰ stays in train only.
- Counts: gold records train 1,113, val 136, test 222; gold pairs 8,092 / 1,153 / 1,554; 22,286 unified rows load
  (train 18,220, val 1,742, test 2,324); `geez_morphology_rows_reviewed.jsonl`: 22,897 load (train 18,701, val 1,796, test 2,400); 68,585
  clitic forms (train 56,008, val 5,379, test 7,198).
- The second መርሶ of the record (row 43, u011760, ወደብ, pl. መራሰው) takes the row root ረ-ሰ-ወ; it then repeats row 40
  (u011757), so it is listed in `merho_ges_gold_flagged_rows.tsv` and is `EXCLUDED` in the unified rows. Counts unchanged.

## 22 October 2026: class and root of nine rootless gold rows

- Place names ሴይር, ሲና, ፋርስ, ባቢሎን, አሞሬዎን (a dictionary entry 'የሀ ስ'; አሞሬዎን Gen 15:16) and the person name ሳራ (አረገት ሳራ,
  Synaxarium Nahase) are `proper_noun` with no root, as the New Testament names; ናሁ 'now, behold' is an `adverb`
  with no root (Isa 49:16 ናሁ በእደውየ). They load in the unified rows; in the gold files the row type is set and,
  with no root, they do not load as gold pairs.
- ሀገር: noun, root ሀ-ገ-ረ; ወልድ: noun, root ወ-ለ-ደ (a dictionary entry, s.v. ወለደ). Both roots are train, as the gold rows; both load.
- The rows were tagged verb; tense and person are cleared, gender and number kept. Gold splits are unchanged.
- Counts: 22,295 unified rows load (train 18,227, val 1,742, test 2,326); `geez_morphology_rows_reviewed.jsonl`: 22,903 load (train 18,705,
  val 1,796, test 2,402); 68,603 clitic forms (train 56,020, val 5,379, test 7,204); gold pairs 8,094 / 1,153 / 1,554.
- ሴይር (u008147): evidence adds 'proper name of a person (Gen 36:20) and the mountain of Edom (Gen 14:6)'.

## 22 October 2026: Bible labels, second set

- Labels of 429 forms checked (root letters in the word, gold rows, other labels of the form, held-out
  verses, duplicates): 413 pass, 16 do not. ይቤ and other በ-ሀ-ለ forms are not changed beyond the first set.
- 38 rootless rows of other books take the root of their word (e.g. ርእስ, ልብ, ምድር, ብእሲ, ስም, ሰላም, ዓለም); ብእሲ
  (u028486) train to val, the split of በ-አ-ሰ. 2 now load, 8 repeat a loading row and are `EXCLUDED`, 28 stay `CHECK`.
- 36 new rows from the verse text with a full analysis (e.g. ላዕለ, እንዘ, ዲበ, ሶበ, ፈርዖን, አሮን, አበዊሆሙ, አልባሲሁ).
- Two forms of the gold paradigm of መ-ረ-ዐ-ወ, ተመራዐወ and አመርዓዌ, are new rows in train; they stay `CHECK`.
  Gold rows are not changed.

- ተመራዐወ (u045347) now has its features (perfect, 3rd person masculine singular, reciprocal stem) and loads.
  አመርዓዌ (u045348) stays `CHECK`.

## 22 October 2026: roots confirmed by the dictionary

- Rows still open whose root the dictionary confirms, plus ሰማየ under ሰ-መ-የ and አንቀጽ/አንቀጸ under ነ-ቀ-ጸ,
  take that root (29 rows: 5 now load, 12 repeat a row and are `EXCLUDED`, 12 stay `CHECK`); gold rows are not changed.
  Rows whose printed root was cut or carried a prefix (ማሕምም ሐ-መ, መዋርስት ወ-ሰ, ምስብዒት/መግዝእ/መጋዝእ with መ-, ተንተነ ነ-ተ-ነ)
  take the dictionary root. Rows move to the split of their root where needed. ዕጣነ, ደመ, ደሞ, ደም, ርስት/ርስተ and ማእከል are not changed.
- ግብረ (u014846) is `EXCLUDED` in `geez_morphology_rows_reviewed.jsonl` too, as a repeat of u028596, as in the main file.
- Number (and part of speech) filled in for 12 rows and for ስሞ u015275 from `geez_morphology_rows_reviewed.jsonl`; they load unless they repeat a row.

## 22 October 2026: main file in step with `geez_morphology_rows_reviewed.jsonl`

- 563 of the 601 rows that loaded only in `geez_morphology_rows_reviewed.jsonl` (all but 38 gold rows, which are not changed) take its root, class, number, gender, split and
  note in the main file. 542 now load; 21 fail a check (root letters, gold root, repeat, split, held-out
  chapter) and do not load in either file.
- እሙንቱ u019564 and እማንቱ u019565 are `EXCLUDED` in both files as repeats of u014816 and u014817.
- The main file is the training file. Training must not use `geez_morphology_rows_reviewed.jsonl`.
- Letter check: ሠ/ሰ, ጸ/ፀ, ሀ/ሐ/ኀ and አ/ዐ count as one series. Roots keep the gold book's spelling. EXCLUDED gold rows are no gold conflict. 13 rows held back earlier now load in both files (e.g. ሰኑይ, ሥልጣን, ፆም, ነፍስ u021719).
- ነፍስ u028700 and ነፍሰ u015074 get root ነ-ፈ-ሰ. ሊቃውንት u021827 gets root ለ-የ-ቀ and stays unloaded. እብላ u022584 is the noun 'moon', with no root, and does not load (a noun needs a root to load). The rootless እድ 'hand' rows get root ዐ-ደ-ወ (a dictionary entry); repeats are excluded.
- Personal, women's and place names (ሴም, ካም, ብንያም, ንፍታሌም, ኢያቄም, ሴሎም, ማርያም, ሐና, ሳሌም, ኢየሩሳሌም, ሮም) are `proper_noun` with no root in both files; the earlier root stays in the evidence. Repeats of loading rows are excluded.

## 23 October 2026: weak root letters

- Letter check: one root letter of the አ, ወ or የ series, as written in the root, may be absent from the word; every other root letter, including ዐ, must appear, with ሠ/ሰ, ጸ/ፀ, ሀ/ሐ/ኀ and አ/ዐ counted as one series.
- ኵሊቱ u012960 gets root ከ-ለ-አ and possessor 3ms, and ሊቃውንት u021827 (root ለ-የ-ቀ) passes; both load in both files.
- ኩልያት u012044, u028668 and u042121 (plural, root ከ-ለ-አ) stay unloaded with no root: they are in val and ከ-ለ-አ is a train root.
- Counts: 22,914 unified rows load (train 18,720, val 1,791, test 2,403); `geez_morphology_rows_reviewed.jsonl`: 22,952 load (train 18,751, val 1,795, test 2,406); 68,755 clitic forms.

## 23 October 2026: ኩልያት in train

- ኩልያት 'kidneys', plural of ኩሊት (a dictionary entry, ከልአ), gets root ከ-ለ-አ and number p, and moves from val to train so ከ-ለ-አ is in one split. u012044 loads in both files; u028668 and u042121 repeat it and are excluded. The book line of u028668 follows.
- Counts: 22,915 unified rows load (train 18,721, val 1,791, test 2,403); `geez_morphology_rows_reviewed.jsonl`: 22,953 load (train 18,752, val 1,795, test 2,406); 68,758 clitic forms (train 56,161, val 5,381, test 7,216).
- ልብ and its possessed forms are back under ለ-በ-በ (the dictionary lists ልብ under ለበበ; plural አልባብ), and the ለ-በ-በ rows are back in their earlier split. ጽዩእ (u036678) and ጽዩኣን (u036679) are masculine; they repeat gold rows u005083 and u005084 and are `EXCLUDED`.
- Bible labels, third set: 10 rootless rows get the root of the other rows of their word; 60 new forms from the verse text. አሐዱ, አሐቲ and አሐደ are under ወ-ሐ-ደ.
- Class of gold rows: ውእቱ pronoun; ዛቲ demonstrative; ኖኅ, ይሁዳ and ጳውሎስ proper nouns with no root; እኅት, ውሉድ, ብእሲት, ኑኅ, አባግዕ, ቍልዔ and ምት nouns (አባግዕ, ቍልዔ and ምት have no root and do not load).
- Bible labels, third set, remaining forms: 153 new forms from the verse text with full labels; ሰሚዐ and ሐዊረ as infinitives with their roots.
- Bible labels, fourth set: 55 new forms from the verse text (54 load).
- Bible labels, fifth set: 48 new forms from the verse text (46 load).
- Nouns with no root: 29 gold nouns that Merho lists among its stand-alone words now load with an empty root. The list is `data/unified/rootless_nouns.tsv`; only nouns on it may load without a root.
- Four gold nouns get the root of the Merho entry they appear in: ራማ (ረ-የ-መ), አስኬማ (ሰ-ከ-መ), እገር (አ-ገ-ረ), ቍልዔ (ቀ-ለ-ዐ).
- Four gold noun spellings corrected to the printed Merho form (በጉሬማ, ዕጉሥታር, ድልጉማ, ኤጥሞጶሞር); they load as nouns with no root.
- Gold ከፈር gets root ከ-ፈ-ረ (Merho, ከፈረ entry) and moves to test with that root.
- Gold ቃማ, አውቴዝራማ and ብሄማ (spelling fixes to Merho) load as nouns with no root.
- Gold ራግማ (spelling fix to Merho) loads as a noun with no root.
- Both gold ዜማ rows load under ዘ-መ-ረ (Merho, ዘመረ entry, printed p.125, plural ዜማት). This is a named exception: the ረ of the root does not appear in ዜማ or ዜማት. The rule that a root's letters appear in the word is otherwise unchanged.
- Some nouns with no root move to validation and test so the no-root answer is measured.
- Nouns with no root get every common proclitic form (ወ-, ለ-, በ-, ከ-, እም-, ዘ- and their combinations).
- Forms with endings of nouns with no root (from Bible verses) load with no root.

## 23 October 2026: gold word classes, names and numerals
- Fourteen gold rows printed as verbs are nouns (ኦሪት, ትካት, አፍራስ, ገነት, ሐመር, መና, ንስር, ኆኅት, ፍና, ገራህት, አውራኅ, ያክንት, ማዕበል, መስቀል); ትካት takes the root ተ-ከ-ተ and repeats an existing row.
- Fourteen gold names load as nouns with no root (ጴጥሮስ, አሴር, ሎጥ, ኤርትራ, ጲላጦስ, ገሊላ, ሶራ, ማኪር, አሶር, ፋሬስ, ደሊላ, ታራ, ገልገላ, ናቡከደነጾር).
- Gold ሠላሳ, ኀምሳ, ስሳ, ሰብዓ are numerals; ኅብረ and ሰንበተ are nouns; ማዕበል takes the root ዐ-በ-ለ.
- ማይ 'water' and its plural ማያት load as nouns with no root.
- Bible labels, sixth set: 26 rows that did not load now load (SURE labels with full analyses).
