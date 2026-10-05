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
| `merho_ges_gold_train_tense_filled.jsonl` | 1,110 | Same + tense filled from real sources where possible |
| `merho_ges_gold_train_tense_sources.jsonl` | 876 | Where each filled tense came from |
| `merho_ges_gold_val.jsonl` | 140 | Val |
| `merho_ges_gold_test.jsonl` | 212 | Held-out test (do not train on this) |
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
