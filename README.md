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
├── output/               extraction and run_all.py output (generator output here is not kept in git)
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
| `synthetic_morphology_train.jsonl` | 210,348 | Synthetic generate training (sha256 `f9b52cd4f4edb199075fc09b0c3dac7d3fe14502ac15605ea84b6f92a54a3a5d`) |
| `synthetic_morphology_analyze.jsonl` | 210,348 | Same pairs, analyze direction |
| `merho_ges_gold_train.jsonl` | see the gold section below | Merho Ges gold train tables: tense filled from real sources where possible; corrections written in |
| `merho_ges_gold_val.jsonl` | see the gold section below | Val; corrections written in |
| `merho_ges_gold_test.jsonl` | see the gold section below | Held-out test (do not train on this); corrections written in |
| `merho_ges_gold_flagged_rows.tsv` | see the gold section below | Gold pairs kept in the files but left out of training and scoring |
| `merho_ges_gold_allowed_duplicates.tsv` | see the gold section below | Exact duplicate pairs kept on purpose (the book prints the same form twice), with page and reason |

Only the corrected gold files are kept: the files as extracted (`merho_ges_gold_all.jsonl`, the uncorrected `merho_ges_gold_train.jsonl`, `merho_ges_gold_train_tense_sources.jsonl` and `data/merho_ges_gold_{train,val,test}.jsonl`) were deleted, and `merho_ges_gold_train_tense_filled.jsonl` was renamed `merho_ges_gold_train.jsonl`. They stay in git history (commit `544271a`).

`data/synthetic/synthetic_forms_for_val_test_roots.jsonl` (6,629 lines, with its `_analyze` mirror) holds the generated lines whose root is a root of the gold val or test file; they are kept out of the training file so the val and test scores are on roots the model never saw, and the trainer does not read them. The split is redone by `synthetic_heldout.py` in the model repo from the full generator output and the current gold val/test files.

Each synthetic line is `{"features": {...}, "surface_form": "..."}` (the analyze file uses `"analysis"` instead of `"features"`). The training script reads the gold-train pairs from `merho_ges_gold_train.jsonl` (counts in the gold section below).

**Tenses in synthetic train:** past 72,977 · present 59,102 · subjunctive 57,027 · imperative 21,242.

- **past** = perfect (ቀተለ)
- **present** = imperfect (ይቀትል)
- **subjunctive** = subjunctive and jussive merged (ይቅትል)
- **imperative** (ቅትል)

**Verb classes in synthetic train** (pairs):

| Internal `verb_type` | Class (traditional model) | Example (perfect ፡ present ፡ subjunctive) | Pairs |
|---|---|---|---:|
| `strong_A` | Type A · ቀተለ | ቀተለ ፡ ይቀትል ፡ ይቅትል (also ይግበር shape; middle guttural: መሐለ ፡ ይምሕል ፡ ይምሐል) | 188,473 |
| `strong_B` | Type B · ቀደሰ | ቀደሰ ፡ ይቄድስ ፡ ይቀድስ | 170 |
| `strong_C` | Type C · ባረከ | ባረከ ፡ ይባርክ ፡ ይባርክ | 510 |
| `strong_D` | Type D · ጽሕቀ (middle guttural, 6th-order first letter in the perfect) | ጽሕቀ ፡ ይጽሕቅ ፡ ይጽሐቅ; ስእለ ፡ ይስእል ፡ ይስአል | 204 |
| `quadriliteral` | ተንበለ (four radicals) | ደንገፀ ፡ ይደነግፅ ፡ ይደንግፅ | 10,626 |
| `weak_middle` | hollow (middle w/y) | ሞተ ፡ ይመውት ፡ ይሙት; ሤመ ፡ ይሠይም ፡ ይሢም | 7,288 |
| `weak_initial` | first w/y | ወለደ ፡ ይወልድ ፡ ይለድ; ወረደ ፡ ይወርድ ፡ ይረድ | 2,839 |
| `weak_final` | final-w ተለወ · final-y ሰትየ | ተለወ ፡ ይተሉ ፡ ይትሉ; ሰትየ ፡ ይሰቲ ፡ ይስተይ | 238 |

The Merho Ges class tags the generator uses come from the corrected gold train file, never from the gold train split as extracted.

Every random draw in the generator is per root: which base pairs of a root get object and negative forms, which object suffixes, which of those get the ኢ- form, and whether a quadriliteral root is used come from that root's own random stream (seeded with sha256 of the global seed, the purpose and the root). A change to one root changes only that root's lines; every other root's lines stay identical and in the same order.

Ordinary middle-guttural verbs like መሐለ are Type A, not Type D. Type D is only the ጽሕቀ / ስእለ pattern (6th-order first letter in the perfect).

**Stems:** basic (ቀተለ), causative አ- (አቅተለ), passive ተ- (ተቀትለ), aste አስተ- (አስተቅተለ).

Guttural-initial present takes የ-/ተ-/አ-/ነ- in every person (የኀድግ); the subjunctive keeps ይ- (ይኅድግ).

Guttural-final past (last radical አ ዐ ሀ ሐ ኀ; Merho p.22 ቃርሐ, ሰምዐ): the 3rd person is short, with the middle radical in the 6th order (ሰምዐ ሰምዐት ሰምዑ ሰምዓ; causative አስምዐ, aste አስተስምዐ; passive ተሰምዐ was already so), and the 1st/2nd person take ā on the middle radical (ሰማዕኩ ሰማዕከ ሰማዕነ; አስማዕኩ, አስተስማዕኩ, ተሰማዕኩ). Same for Type B (ሰብሐ, ሰባሕኩ) and Type C (ቃርሐ, ቃራሕኩ). Quadriliterals and hollow roots (ሞአ, ኖኀ) are unchanged. 10,555 lines of the synthetic files changed (negative and object-suffix copies included); no other line moved.

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

- Root `dictionary.jsonl` is byte-identical to `data/lexicon/classical_dictionary_kidane_wold.jsonl` (the copy `output/dictionary_with_roots.jsonl` was removed from git on 2026-10-06; `run_all.py` still writes it locally). The generator, the analyzer, `run_all.py` and `build_canonical_dataset.py` read it, so it stays. Edit the dictionary in `data/lexicon/` only.
- `morphology.jsonl` is read by `run_all.py`. `errata.jsonl` holds Kidane Wold errata (dictionary work in progress).
- The `*.db` extraction databases are local only (not in git).
- `build_canonical_dataset.py` with its default `--out_dir` still writes an older, uncorrected gold split to `data/merho_ges_gold_{train,val,test}.jsonl`. Those files were deleted (2026-10-06): do not add them back; run it with `--out_dir /tmp/...`. The gold files are in `data/paradigms/` only.
- `build_canonical_dataset.py` settles ambiguous Latin letters in the Merho Ges roots from the Ethiopic headword and logs swaps, unsettled cases, the hand override and dropped records in `output/merho_root_review_log.tsv` (written locally, not kept in git since 2026-10-06). It reads the synthetic lines for `data/verbs_rbha_anqets.jsonl` from `data/paradigms/synthetic_morphology_train.jsonl`. Test: `python -m pytest tests/`.
- `data/geez_amharic_dictionary.jsonl`, `data/geez_literature_corpus.txt`, `data/verbs_rbha_anqets.jsonl` and `data/true_parallel_pairs.jsonl` also come from `build_canonical_dataset.py`. The generator reads `data/geez_amharic_dictionary.jsonl`.
- The synthetic generator lives in **geez-morphology-model** (`generate_synthetic_fixed.py`). It writes `output/` (not kept in git; the stale 217,417-line copies from 9d3f15d were removed on 2026-10-06), copies the paradigm files to `data/paradigms/` and moves the lines with a gold val/test root to `data/synthetic/` (`synthetic_heldout.py`).

## Generate / train / eval (from the model repo)

```bash
cd ../geez-morphology-model
source .venv/bin/activate
python generate_synthetic_fixed.py      # rewrites output/, data/paradigms/synthetic_* and data/synthetic/
python train_byt5_morphology.py         # reads data/paradigms/synthetic_morphology_train.jsonl + gold train
python evaluate_gold.py --model_dir checkpoints_full   # Merho Ges held-out test
```

## License / privacy

Apache License 2.0. Repo is private while work is in progress. Dictionary text and scans stay in this private tree; do not publish them.

<!-- gold-split-moves:start -->

### Merho Ges gold files: corrections written into the files

`merho_ges_gold_train.jsonl`, `merho_ges_gold_val.jsonl` and `merho_ges_gold_test.jsonl` carry the page-checked corrections (from the book scans) and the root decisions in `data/corrections/`, written into the files: there is nothing to apply at load time. They are rebuilt from the files as extracted (git commit `544271a` of this repository); the full change log (old value, new value, page, source and reason of every change) is kept with the project's notes material and is available on request.

- records now: train 1105, val 135, test 219 (1462 as extracted; none dropped, 3 merged into the record they continue on the page, listed in `merged_record_ids`); rows are corrected, never dropped: the only pairs removed are exact duplicates (the same form with the same labels twice in one split; one copy kept, 148 copies removed);
- changes: 4841 values (duplicate_kept 1, duplicate_removed 148, form 286, geez_form 273, gender 311, number 83, object 67, person 724, record_merge 6, root 1008, root_unsettled 1, row_removed 130, row_split 22, split_move 20, stem 205, tense 773, title_or_lemma 20, type 763);
- tense: the files say `subjunctive` where the extraction said `jussive` (one subjunctive label, as in the synthetic data): 45 values changed, 41 copies that became exact duplicates removed;
- `merho_ges_gold_flagged_rows.tsv`: 17 pairs kept in the files but left out of training and scoring, with the reason;
- `merho_ges_gold_allowed_duplicates.tsv`: 1 exact duplicate pair(s) kept on purpose (the book prints the same form twice, e.g. one spelling under two class marks), with page and reason;
- a row may carry `root`, `stem`, `type` (noun/adjective), `object` where they differ from the record, and `source_row`/`source_variant` where a cell was split; a record may carry `root_unsettled` (its root is not used; rows with their own root still load); a record root may be empty when every row carries its own root (a section heading); rows taken over from a merged record carry `source_record_id` and `source_row`;
- record `stem` (a schema value): the rows' stem when they agree, else the headword row's (the first unflagged row); 47 record stems set this way, a row that read the old record stem carries it explicitly;
- `record_id`: every record stores a stable id, computed once from its values as extracted (`544271a`): the first 12 hex digits of sha1(`page_number|title_or_lemma|raw_transcription`). It is never recomputed: a corrected `title_or_lemma` or a merge keeps it (a merged record keeps the id of the record it was merged into). The flagged-rows file and the change log name records by it;
- these three files and the flagged-rows list are the only gold files: the uncorrected files as extracted (`merho_ges_gold_all.jsonl`, the extracted `merho_ges_gold_train.jsonl`, `merho_ges_gold_train_tense_sources.jsonl`, `data/merho_ges_gold_{train,val,test}.jsonl`) were deleted and `merho_ges_gold_train_tense_filled.jsonl` was renamed `merho_ges_gold_train.jsonl` (2026-10-06); they stay in git history (`544271a`).

### Gold records moved between splits (each root in one split)

A root (after all corrections) may appear in one gold split only, so that the val and test scores are on roots the model never saw in gold training. Records that share a root are moved as whole records to the split with most of that root's gold pairs (on a tie the record stays in val/test, and test wins over val). Line numbers are those of the files as extracted (commit `544271a`); moved records are at the end of their new file. The list is rebuilt whenever the corrections change.

- ሀ-ለ-ወ: gold pairs train 1, test 1; moved to test: train line 745 (1 pair). Synthetic training pairs with this root: ሀ-ለ-ወ 0.
- ለ-ሰ-ሐ: gold pairs train 2, val 1; moved to train: val line 1 (1 pair). Synthetic training pairs with this root: ለ-ሰ-ሐ 137.
- ሐ-መ-መ: gold pairs train 11, val 4; moved to train: val line 18 (1 pair); val line 19 (3 pairs). Synthetic training pairs with this root: ሐ-መ-መ 138.
- ሠ-ረ-የ: gold pairs train 2, test 4; moved to test: train line 872 (2 pairs). Synthetic training pairs with this root: ሠ-ረ-የ 0.
- ረ-አ-የ: gold pairs train 7, val 1; moved to train: val line 112 (1 pair). Synthetic training pairs with this root: ረ-አ-የ 0.
- ሰ-ነ-አ-ለ: gold pairs train 6, test 2; moved to train: test line 15 (2 pairs). Synthetic training pairs with this root: ሰ-ነ-አ-ለ 0.
- ቀ-በ-ለ ቈ-በ-ለ: gold pairs train 2, test 2; moved to test: train line 128 (2 pairs). Synthetic training pairs with this root: ቀ-በ-ለ 0, ቈ-በ-ለ 0.
- በ-ወ-ሐ አ-በ-ሐ: gold pairs train 2, test 5; moved to test: train line 55 (2 pairs). Synthetic training pairs with this root: በ-ወ-ሐ 0, አ-በ-ሐ 0.
- ተ-በ-ዐ: gold pairs train 3, test 2; moved to train: test line 104 (2 pairs). Synthetic training pairs with this root: ተ-በ-ዐ 0.
- ተ-የ-ሀ: gold pairs train 1, test 1; moved to test: train line 60 (1 pair). Synthetic training pairs with this root: ተ-የ-ሀ 0.
- ኀ-ሠ-ሠ ጐ-ሠ-ሠ: gold pairs val 1, test 5; moved to test: val line 26 (1 pair). Synthetic training pairs with this root: ኀ-ሠ-ሠ 0, ጐ-ሠ-ሠ 0.
- ነ-ወ-መ: gold pairs train 1, val 1; moved to val: train line 212 (1 pair). Synthetic training pairs with this root: ነ-ወ-መ 0.
- ነ-ዐ-መ ፈ-አ-መ: gold pairs train 1, test 3; moved to test: train line 211 (1 pair). Synthetic training pairs with this root: ነ-ዐ-መ 0, ፈ-አ-መ 0.
- አ-ኰ-ተ: gold pairs train 1, test 1; moved to test: train line 564 (1 pair). Synthetic training pairs with this root: አ-ኰ-ተ 0.
- ከ-ረ-በ: gold pairs train 7, val 12; moved to val: train line 1107 (7 pairs). Synthetic training pairs with this root: ከ-ረ-በ 0.
- ወ-ጸ-አ: gold pairs train 1, test 2; moved to test: train line 672 (1 pair). Synthetic training pairs with this root: ወ-ጸ-አ 0.
- ዐ-የ-ረ: gold pairs train 1, test 2; moved to test: train line 368 (1 pair). Synthetic training pairs with this root: ዐ-የ-ረ 0.
- ደ-ኀ-ነ: gold pairs train 4, val 3; moved to train: val line 7 (3 pairs). Synthetic training pairs with this root: ደ-ኀ-ነ 34.
- ፈ-ወ-ዘ: gold pairs train 4, test 1; moved to train: test line 175 (1 pair). Synthetic training pairs with this root: ፈ-ወ-ዘ 0.

<!-- gold-split-moves:end -->
