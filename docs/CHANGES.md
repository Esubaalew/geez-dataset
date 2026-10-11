# Differences from v1

v1: tag `v1`, commit `337cdf0`.

| | v1 | v2 |
|---|---:|---:|
| gold pairs that load (train / val / test) | 8,060 / 1,154 / 1,514 | 8,060 / 1,154 / 1,512 |
| rows of other books that load (train / val / test) | 7,599 / 388 / 454 | 7,904 / 393 / 461 |
| unified rows | 24,352 | 24,299 |
| synthetic, lexicon, parallel and corpus files | | unchanged |

## Gold

Roots and forms, read on the printed page:

| Page | Record | v1 | v2 |
|---:|---|---|---|
| 173 | fe56fd77a429 | ዐሰበ / ተዐስበ | ዐሰበ / ተዐሰበ (the page prints ወተዐሰበ) |
| 224 | cec6f1da85f9 | አንትዐ, መንተዕ, አንተዕ, አንተዓት, አናተዕ; root ነ-ተ-ዐ | አንጉዐ, መንጉዕ, አንጉዕ, አንጉዓት, አናጉዕ; root ነ-ጐ-ዐ |
| 226 | e27dfa30dc1a | ተፀኀዘ / አዕኀዘ; root ፀ-ኀ-ዘ | ተፀንግዐ / አፀንግዐ; root ፀ-ነ-ገ-ዐ |

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

## README

Line counts corrected to the files: synthetic files 121,206 (v1 README: 125,020); `book_forms.jsonl` 14,110 (14,118); gold test records 219 (220).
