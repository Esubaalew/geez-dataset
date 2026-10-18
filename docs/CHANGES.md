# Differences from v1

v1: tag `v1`, commit `337cdf0`.

| | v1 | v2 |
|---|---:|---:|
| gold pairs that load (train / val / test) | 8,060 / 1,154 / 1,514 | 8,087 / 1,164 / 1,543 |
| rows of other books that load (train / val / test) | 7,599 / 388 / 454 | 10,065 / 572 / 767 |
| unified rows | 24,352 | 45,152 |
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
- Merho Ges p. 284 (record `269827c0b68e`, ሠቀየ / ሣቀየ): class ባረከ, as ፍሬ ግእዝ p. 40 gives it.
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
- Roots confirmed by the same verb in the Merho Ges paradigms or another book: ጦመረ ጠ-መ-ረ, ተሞዕዐ መ-ዐ-ዐ, አንጦልዐ ነ-ጠ-ለ-ዐ, ቆለወ ቈ-ለ-ወ, አስዖዘዘ ዐ-ዘ-ዘ, አቅዜዘየ ቀ-ዘ-የ (a ወ or የ read from the vowel of the headword is not a radical); መትሀ, ጐርሐ, ቈልቈለ, ርኅበ, ቈንቈነ, ለምአ, ሰጕዐ, ጐጕአ, ፃእፅአ, ምዕከ, ረጕነኰ, ቀልጰወ, ፆተወ, ዐወደ, ዐወገ, ሠበጠ, አከጠ and ፀረፈ keep their own roots.
- A derived stem keeps the root of its base, with the prefix stripped: ተመዝጐለ መ-ዘ-ጐ-ለ, ተሠሀለ ሠ-ሀ-ለ, አንዛህለለ ነ-ዘ-ሀ-ለ-ለ, አርመስመሰ ረ-መ-ሰ-መ-ሰ, አክሞሰሰ ከ-መ-ሰ-ሰ, ተሥዕዐ ሠ-ዐ-ዐ, አንጕዐ ነ-ጐ-ዐ, አስደለወ ደ-ለ-ወ, አስፌድለወ ፈ-ደ-ለ-ወ, ተመኵሰየ መ-ኰ-ሰ-የ. ጸቈሰ, አሰውሰጠ and ሀየጰ stay `CHECK`.
- Class marks settled against the same verb in the Merho Ges paradigms: the list class is kept for ቃሕቅሐ, ቆመሰ, ቆበረ, ተጽዕረ, አማዕዘረ, ቀስተወ, አመንሰወ, አመንተወ, አቀምጠወ, አመስከየ, አመክነየ, ዘርከየ and ደርበየ; the list class agrees with the gold for ከረመ, ለጸቀ, ተላጸቀ, ነፈቀ, አልጸቀ, ከልአ, በረከ, አስተብረከ, ሰለወ, ተደለወ, አድለወ, ደለወ, ተጋአዘ, ገአዘ, መረየ, ዐለየ, ዐረየ and አስተጋየደ. Entries whose class differs from the gold stay `CHECK`.

## README

Line counts corrected to the files: synthetic files 121,206 (v1 README: 125,020); `book_forms.jsonl` 14,110 (14,118); gold test records 219 (220).

## Flagged gold rows (2026-10-15)

- All 323 rows listed in `merho_ges_gold_flagged_rows.tsv` were checked against the printed *Merho Ges* pages and Yared Shiferaw's typed edition. Each was corrected or removed; no flagged rows remain.
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

## 17 October 2026: combine reviewed corrections

Seventeen OCR errors in Kidane Wold text corrected from the printed pages; person cleared on noun-list rows; imperative person, number and gender labels and duplicate book rows fixed.

## 17 October 2026: gold cleanup

- Removed 42 example phrases and title abbreviations from the gold tables; fixed two person labels.
- Part of speech set to noun on 745 rows of noun tables.
- Roots corrected to ለ-የ-ለ-የ and ዐ-ወ-የ-ወ; one book row that repeats a gold row folded into it; root ዐ-ወ-የ-ወ added for dictionary entry አዐውየወ.
- Headword on p.129 read as አመንዘረ (root መ-ነ-ዘ-ረ), printed twice with two glosses; lemmas and forms corrected from the pages on pp.40, 320, 337 and 383; two OCR readings corrected in Kidane Wold pp.375 and 455.
