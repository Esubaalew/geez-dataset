# Differences from v1

v1: tag `v1`, commit `337cdf0`.

| | v1 | v2 |
|---|---:|---:|
| gold pairs that load (train / val / test) | 8,060 / 1,154 / 1,514 | 8,104 / 1,165 / 1,548 |
| rows of other books that load (train / val / test) | 7,599 / 388 / 454 | 8,083 / 422 / 497 |
| unified rows | 24,352 | 29,987 |
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

Moved to test, printed spelling kept, the other spelling noted in `spelling_note`: acc4f9cac1b0 ወፅአ (p.228, also ወጽአ) and 110f07e7667d ፀንሰ (p.109, also ጸንሰ), so ፀ/ጸ spellings of one root share a split.

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

## README

Line counts corrected to the files: synthetic files 121,206 (v1 README: 125,020); `book_forms.jsonl` 14,110 (14,118); gold test records 219 (220).

## Master Flagged-Rows & Gap Cleanup (2026-10-15)

- Resolved or removed all 323 flagged rows in `merho_ges_gold_flagged_rows.tsv` (`0` flagged rows remain):
  - Removed 158 unprinted/duplicate/garbled rows across `train`, `val`, and `test` (26 flagged and 18 unflagged duplicate 3ms past headwords mislabelled as nominals, 32 Amharic glosses and `የ...` domain notes extracted as Ge'ez rows, 17 OCR book-tag fragments such as `ሰሴ`, `ሳስ`, `እብ`, `ኣብ`, `ኢብ`, `ክብ`, `ብዙ`, `ኩፋኔ`, and unprinted or merged OCR rows).
  - Corrected labels on 52 feminine plural adjectives (`-አት`/`-ዋት`/`-ያት` tagged `በብ` after `ለሴ`/`ለስ`: `gender="m"` -> `"f"`), 17 agentive adjectives (`ባዕ ሣ ቅ`: `type="noun"` -> `"adjective"`), and 25 nominal/verb type, gender, number, stem, and object-suffix mismatches.
  - Corrected section-mismatched OCR roots and forms verified against the printed book and Yared Shiferaw's typed edition (`ደ-ኀ-ነ` -> `ደ-ኀ-ኀ` on pp. 41-42, `ገ-ደ-ፈ` -> `ገ-የ-ረ` on p. 143, `ቀ-ጠ-ነ` -> `ቀ-ጠ-ጠ` on p. 329, `ለ-አ-ከ` -> `ለ-ከ-አ` on p. 210, `ረ-ገ-በ` -> `ረ-ገ-ዐ` on p. 214, `ጐ-ጐ-ለ` -> `ጐ-ጐ-አ` on p. 231, `ሐ-ቀ-ቀ` -> `ሐ-ቀ-የ` on p. 280, `ነ-አ-የ` -> `ነ-አ-ደ` on p. 310, `ነ-ጐ-ደ-ጐ` -> `ነ-ጐ-ደ-ጐ-ደ` on p. 312, `መ-ለ-ጠ` -> `ሰ-ፈ-ጠ` on p. 329, `አ-ከ-ተ` -> `አ-ከ-ጠ` on p. 329, `ደ-ነ-ደ-ነ` -> `ደ-ነ-ጸ` on p. 341, `ዐ-ሰ-ተ` -> `ዐ-ሰ-ቀ` on p. 156, `ሰ-ከ-ተ` -> `ሰ-ከ-ተ-የ` on p. 290, `ጠ-ጠ-በ` -> `ጠ-በ-ጠ-በ` on p. 181), plus held-back strong OCR spelling fixes.
  - Full audit log recorded in `geez-dataset-internal/gold_changes/fix_1015_master/master_cleanup_applied.tsv`.
