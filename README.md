# geez-dataset

Classical Ge'ez lexical, morphological, and parallel data. Private repo.

## Layout

```
geez-dataset/
├── data/
│   ├── paradigms/        training + gold morphology (canonical)
│   ├── lexicon/          dictionaries and verb triples
│   ├── parallel/         Ge'ez–Amharic sentence pairs
│   ├── corpora/          monolingual / prose text
│   └── *.jsonl, *.txt    older combined files from build_canonical_dataset.py (see below)
├── output/               generator and run_all.py output; paradigm files mirror data/paradigms/
├── scans/                page images (keep; private)
│   ├── sewasew_1_192/    Kidane Wold dictionary, pages 1–192 (192 GIF)
│   ├── merho_ges_511/    Merho Ges (509 JPG)
│   └── page_618.gif, page_909.gif
├── sources/              source notes (README.md; the PDFs are not in git)
├── scripts/              extraction scripts (OCR / ingestion of the scans)
├── tests/                checks for build_canonical_dataset.py
├── docs/
│   └── extraction_methods.md
├── dictionary.jsonl      Kidane Wold dictionary, read by the generator and analyzer (see below)
├── morphology.jsonl      208 Merho Ges records, read by run_all.py
├── errata.jsonl          12 Kidane Wold errata rows
├── build_canonical_dataset.py
└── run_all.py
```

Do not put new training files at the repo root. Prefer `data/…`.

## `data/paradigms/` (use these for training)

| File | Rows | Role |
|------|------|------|
| `synthetic_morphology_train.jsonl` | 217,417 | Synthetic generate training (sha256 `7973b501bb41421b34a19aa6f06ff6a4b4807f7eb67c1d78683da02be0893e45`) |
| `synthetic_morphology_analyze.jsonl` | 217,417 | Same pairs, analyze direction |
| `merho_ges_gold_train.jsonl` | 1,110 | Merho Ges gold train tables |
| `merho_ges_gold_train_tense_filled.jsonl` | see the gold section below | Same + tense filled from real sources where possible; corrections written in |
| `merho_ges_gold_train_tense_sources.jsonl` | 876 | Where each filled tense came from |
| `merho_ges_gold_val.jsonl` | see the gold section below | Val; corrections written in |
| `merho_ges_gold_test.jsonl` | see the gold section below | Held-out test (do not train on this); corrections written in |
| `merho_ges_gold_all.jsonl` | 1,462 | All extracted Merho Ges tables |

Each synthetic line is `{"features": {...}, "surface_form": "..."}` (the analyze file uses `"analysis"` instead of `"features"`). The training script turns the 1,110 gold-train tables into 3,322 gold-train pairs.

**Tenses in synthetic train:** past 75,505 · present 60,848 · subjunctive 59,103 · imperative 21,961.

- **past** = perfect (ቀተለ)
- **present** = imperfect (ይቀትል)
- **subjunctive** = subjunctive and jussive merged (ይቅትል)
- **imperative** (ቅትል)

**Verb classes in synthetic train** (pairs):

| Internal `verb_type` | Class (traditional model) | Example (perfect ፡ present ፡ subjunctive) | Pairs |
|---|---|---|---:|
| `strong_A` | Type A · ቀተለ | ቀተለ ፡ ይቀትል ፡ ይቅትል (also ይግበር shape; middle guttural: መሐለ ፡ ይምሕል ፡ ይምሐል) | 194,874 |
| `strong_B` | Type B · ቀደሰ | ቀደሰ ፡ ይቄድስ ፡ ይቀድስ | 170 |
| `strong_C` | Type C · ባረከ | ባረከ ፡ ይባርክ ፡ ይባርክ | 544 |
| `strong_D` | Type D · ጽሕቀ (middle guttural, 6th-order first letter in the perfect) | ጽሕቀ ፡ ይጽሕቅ ፡ ይጽሐቅ; ስእለ ፡ ይስእል ፡ ይስአል | 204 |
| `quadriliteral` | ተንበለ (four radicals) | ደንገፀ ፡ ይደነግፅ ፡ ይደንግፅ | 10,983 |
| `weak_middle` | hollow (middle w/y) | ሞተ ፡ ይመውት ፡ ይሙት; ሤመ ፡ ይሠይም ፡ ይሢም | 7,469 |
| `weak_initial` | first w/y | ወለደ ፡ ይወልድ ፡ ይለድ; ወረደ ፡ ይወርድ ፡ ይረድ | 2,935 |
| `weak_final` | final-w ተለወ · final-y ሰትየ | ተለወ ፡ ይተሉ ፡ ይትሉ; ሰትየ ፡ ይሰቲ ፡ ይስተይ | 238 |

Ordinary middle-guttural verbs like መሐለ are Type A, not Type D. Type D is only the ጽሕቀ / ስእለ pattern (6th-order first letter in the perfect).

**Stems:** basic (ቀተለ), causative አ- (አቅተለ), passive ተ- (ተቀትለ), aste አስተ- (አስተቅተለ).

Guttural-initial present takes የ-/ተ-/አ-/ነ- in every person (የኀድግ); the subjunctive keeps ይ- (ይኅድግ).

Grammar rules used to build the synthetic set live in the morphology repo: [`docs/grammar_rules.md`](https://github.com/esubaalew/geez-morphology/blob/main/docs/grammar_rules.md).

## `data/lexicon/`

| File | Rows | Role |
|------|------|------|
| `classical_dictionary_kidane_wold.jsonl` | 13,234 | Kidane Wold classical dictionary |
| `modern_geez_amharic_dictionary.jsonl` | 1,722 | Modern Ge'ez–Amharic glossary |
| `kidane_wold_verb_triples.jsonl` | 262 | Accepted perfect ፡ imperfect ፡ subjunctive |
| `kidane_wold_verb_triples_rejected.jsonl` | 326 | Rejected (OCR / radical mismatch) |
| `kidane_wold_root_fixes.jsonl` | 955 | Root-letter repair log |

## `data/parallel/` and `data/corpora/`

- `parallel/true_parallel_pairs.jsonl` — 2,780 high-precision pairs
- `parallel/uncertain_pairs.jsonl` — 9,066 short / uncertain glosses
- `corpora/` — Yared Shiferaw text, Merho Ges prose, monolingual Ge'ez, phrasebook

## Other files (kept because code reads them)

- Root `dictionary.jsonl` is byte-identical to `data/lexicon/classical_dictionary_kidane_wold.jsonl` and `output/dictionary_with_roots.jsonl`. The generator, the analyzer, `run_all.py` and `build_canonical_dataset.py` read it, so it stays. Edit the dictionary in `data/lexicon/` only.
- `morphology.jsonl` is read by `run_all.py`. `errata.jsonl` holds Kidane Wold errata (dictionary work in progress).
- The `*.db` extraction databases are local only (not in git).
- `data/merho_ges_gold_{train,val,test}.jsonl` are an older split written by `build_canonical_dataset.py`. They differ from `data/paradigms/` and overlap its train roots. Use `data/paradigms/` only.
- `build_canonical_dataset.py` settles ambiguous Latin letters in the Merho Ges roots from the Ethiopic headword and logs swaps, unsettled cases, the hand override and dropped records in `output/merho_root_review_log.tsv`. Test: `python -m pytest tests/`.
- `data/geez_amharic_dictionary.jsonl`, `data/geez_literature_corpus.txt`, `data/verbs_rbha_anqets.jsonl` and `data/true_parallel_pairs.jsonl` also come from `build_canonical_dataset.py`. The generator reads `data/geez_amharic_dictionary.jsonl`.
- The synthetic generator lives in **geez-morphology-model** (`generate_synthetic_fixed.py`). It writes `output/` and copies the paradigm files to `data/paradigms/`.

## Generate / train / eval (from the model repo)

```bash
cd ../geez-morphology-model
source .venv/bin/activate
python generate_synthetic_fixed.py      # rewrites output/ and data/paradigms/synthetic_*
python train_byt5_morphology.py         # reads data/paradigms/synthetic_morphology_train.jsonl + gold train
python evaluate_gold.py --model_dir checkpoints_full   # Merho Ges held-out test
```

## License / privacy

Apache License 2.0. Repo is private while work is in progress. Dictionary text and scans stay in this private tree; do not publish them.

<!-- gold-split-moves:start -->

### Merho Ges gold files: corrections written into the files

`merho_ges_gold_train_tense_filled.jsonl`, `merho_ges_gold_val.jsonl` and `merho_ges_gold_test.jsonl` carry the page-checked corrections (from the book scans) and the root decisions in `data/corrections/`, written into the files: there is nothing to apply at load time. They are rebuilt from the files as extracted (git commit `544271a` of this repository); the full change log (old value, new value, page, source and reason of every change) is kept with the project's notes material and is available on request.

- records now: train 1106, val 137, test 219 (1462 in all, none dropped); rows are corrected, never dropped: the only pairs removed are exact duplicates (the same form with the same labels twice in one split; one copy kept, 102 copies removed);
- changes: 4210 values (duplicate_removed 102, form 205, geez_form 196, gender 285, number 72, object 58, person 672, root 973, root_unsettled 2, row_removed 95, row_split 19, split_move 17, stem 130, tense 672, type 712);
- `merho_ges_gold_flagged_rows.tsv`: 14 pairs kept in the files but left out of training and scoring, with the reason;
- a row may carry `root`, `stem`, `type` (noun/adjective), `object` where they differ from the record, and `source_row`/`source_variant` where a cell was split; a record may carry `root_unsettled` (its root is not used; rows with their own root still load);
- `merho_ges_gold_train.jsonl`, `merho_ges_gold_all.jsonl` and `merho_ges_gold_train_tense_sources.jsonl` are not rewritten (still as extracted).

### Gold records moved between splits (each root in one split)

A root (after all corrections) may appear in one gold split only, so that the val and test scores are on roots the model never saw in gold training. Records that share a root are moved as whole records to the split with most of that root's gold pairs (on a tie the record stays in val/test, and test wins over val). Line numbers are those of the files as extracted (commit `544271a`); moved records are at the end of their new file. The list is rebuilt whenever the corrections change.

- ሀ-ለ-ወ: gold pairs train 1, test 1; moved to test: train line 745 (1 pair). Synthetic training pairs with this root: ሀ-ለ-ወ 0.
- ሐ-መ-መ: gold pairs train 11, val 4; moved to train: val line 18 (1 pair); val line 19 (3 pairs). Synthetic training pairs with this root: ሐ-መ-መ 134.
- ረ-አ-የ: gold pairs train 7, val 1; moved to train: val line 112 (1 pair). Synthetic training pairs with this root: ረ-አ-የ 0.
- ሰ-ነ-አ-ለ: gold pairs train 6, test 2; moved to train: test line 15 (2 pairs). Synthetic training pairs with this root: ሰ-ነ-አ-ለ 0.
- ቀ-በ-ለ ቈ-በ-ለ: gold pairs train 2, test 2; moved to test: train line 128 (2 pairs). Synthetic training pairs with this root: ቀ-በ-ለ 0, ቈ-በ-ለ 0.
- በ-ወ-ሐ አ-በ-ሐ: gold pairs train 2, test 5; moved to test: train line 55 (2 pairs). Synthetic training pairs with this root: በ-ወ-ሐ 41, አ-በ-ሐ 0.
- ተ-በ-ዐ: gold pairs train 3, test 2; moved to train: test line 104 (2 pairs). Synthetic training pairs with this root: ተ-በ-ዐ 0.
- ተ-የ-ሀ: gold pairs train 1, test 1; moved to test: train line 60 (1 pair). Synthetic training pairs with this root: ተ-የ-ሀ 0.
- ኀ-ሠ-ሠ ጐ-ሠ-ሠ: gold pairs val 1, test 5; moved to test: val line 26 (1 pair). Synthetic training pairs with this root: ኀ-ሠ-ሠ 0, ጐ-ሠ-ሠ 0.
- ነ-ወ-መ: gold pairs train 1, val 1; moved to val: train line 212 (1 pair). Synthetic training pairs with this root: ነ-ወ-መ 41.
- ነ-ዐ-መ ፈ-አ-መ: gold pairs train 1, test 3; moved to test: train line 211 (1 pair). Synthetic training pairs with this root: ነ-ዐ-መ 0, ፈ-አ-መ 34.
- አ-ኰ-ተ: gold pairs train 1, test 1; moved to test: train line 564 (1 pair). Synthetic training pairs with this root: አ-ኰ-ተ 0.
- ከ-ረ-በ: gold pairs train 7, val 12; moved to val: train line 1107 (7 pairs). Synthetic training pairs with this root: ከ-ረ-በ 131.
- ወ-ጸ-አ: gold pairs train 1, test 2; moved to test: train line 672 (1 pair). Synthetic training pairs with this root: ወ-ጸ-አ 0.
- ዐ-የ-ረ: gold pairs train 1, test 2; moved to test: train line 368 (1 pair). Synthetic training pairs with this root: ዐ-የ-ረ 0.
- ደ-ኀ-ነ: gold pairs train 4, val 3; moved to train: val line 7 (3 pairs). Synthetic training pairs with this root: ደ-ኀ-ነ 34.

<!-- gold-split-moves:end -->
