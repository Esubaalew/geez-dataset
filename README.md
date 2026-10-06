# geez-dataset

Classical Ge'ez verb morphology data: gold paradigms from Merho Ges, synthetic generated forms, lexicon, parallel pairs, and corpora.

## Sources

- **Merho Ges** (*Merho Ges Wesewasew Ze-Yared*): the gold paradigm tables, page-checked against the book scans. Corrections are written into the files; the change log keeps the original values.
- **Kidane Wold** classical Ge'ez dictionary: OCR text corrected from geezorg/data commit 3904462c (CC BY-SA 4.0).
- **Modern Ge'ez-Amharic glossary**: 1,722 entries.
- **Corpora**: Yared Shiferaw prose, Merho Ges prose, monolingual Ge'ez text, and a Ge'ez-Amharic phrasebook.

## Layout

```
geez-dataset/
├── data/
│   ├── paradigms/        gold morphology splits and synthetic training files
│   ├── lexicon/          dictionaries, verb triples, root fixes
│   ├── parallel/         Ge'ez-Amharic sentence pairs
│   ├── corpora/          monolingual text and phrasebook
│   ├── synthetic/        synthetic forms held out (gold val/test roots)
│   └── corrections/      correction tables applied to the gold files
├── docs/
│   ├── schema.md             field reference for the gold files
│   └── extraction_methods.md
├── scripts/              extraction scripts and check_dataset.py
├── tests/
├── dictionary.jsonl      Kidane Wold dictionary (read by the generator)
├── morphology.jsonl      208 Merho Ges records (read by run_all.py)
└── errata.jsonl          Kidane Wold errata rows
```

`output/` holds local generator output and is not kept in git. The `*.db` extraction databases are local only.

## Data files

### Gold paradigms (`data/paradigms/`)

| File | Contents | Rows | sha256 |
|---|---|---:|---|
| `merho_ges_gold_train.jsonl` | Gold verb paradigms, training split | 1104 records | `56345b5a4e3e0` |
| `merho_ges_gold_val.jsonl` | Gold verb paradigms, validation split | 135 records | `437afa0c2db62` |
| `merho_ges_gold_test.jsonl` | Gold verb paradigms, held-out test split | 219 records | `5972fad38704b` |
| `merho_ges_gold_flagged_rows.tsv` | Rows kept in the files but excluded from training and scoring, with reasons | 17 rows | `844b05766b3ed` |
| `merho_ges_gold_allowed_duplicates.tsv` | Exact duplicate pairs kept on purpose (the book prints the same form twice) | 1 row | `36e54b263842c` |

The three gold files carry the page-checked corrections written into the files: there is nothing to apply at load time. Rows are corrected, never dropped. The only pairs removed are exact duplicates (the same form with the same labels twice in one split; one copy kept).

**Split rule.** A root (after all corrections) appears in exactly one gold split, so validation and test scores are on roots the model never saw in gold training. Records that share a root move as whole records to the split holding most of that root's gold pairs (on a tie the record stays in val/test; test wins over val). If one quoted row would leak a root across splits, the row is flagged, not moved.

**Stable ids.** Every record has a `record_id`: the first 12 hex digits of sha1(`page_number|title_or_lemma|raw_transcription`), computed once from the values as extracted. It is never recomputed: a corrected title or a merged record keeps its id.

**Tense labels.** The files use `past`, `present`, `subjunctive`, `imperative`. The extraction's `jussive` is written as `subjunctive` (one label, matching the synthetic data).

Field reference: `docs/schema.md`.

### Synthetic forms (`data/paradigms/`, `data/synthetic/`)

| File | Contents | Rows | sha256 |
|---|---|---:|---|
| `synthetic_morphology_train.jsonl` | Generated (root, form) pairs for training | 210,348 | `f9b52cd4f4edb` |
| `synthetic_morphology_analyze.jsonl` | Same pairs, analyze direction | 210,348 | `849672ed4e93` |
| `synthetic_forms_for_val_test_roots.jsonl` | Generated lines whose root is a gold val/test root; kept out of training (`data/synthetic/`) | 6,629 | `428059df2700` |
| `synthetic_forms_for_val_test_roots_analyze.jsonl` | Analyze-direction mirror | 6,629 | `e9789444bc16` |

Each synthetic line is `{"features": {...}, "surface_form": "..."}` (the analyze files use `"analysis"` instead of `"features"`). Tense counts in the training file: past 72,977; present 59,102; subjunctive 57,027; imperative 21,242. The generator lives in the companion `geez-morphology` repo (`generate_synthetic_fixed.py`); the grammar rules it implements are documented there in `docs/grammar_rules.md`.

### Lexicon (`data/lexicon/`)

| File | Contents | Rows | sha256 |
|---|---|---:|---|
| `classical_dictionary_kidane_wold.jsonl` | Kidane Wold classical Ge'ez dictionary | 13,234 | `d8d871a9` |
| `modern_geez_amharic_dictionary.jsonl` | Modern Ge'ez-Amharic glossary | 1,722 | `57bf6a19fc6e3` |
| `kidane_wold_verb_triples.jsonl` | Accepted perfect : imperfect : subjunctive triples | 262 | `f4f904681823` |
| `kidane_wold_verb_triples_rejected.jsonl` | Rejected triples (OCR / radical mismatch) | 326 | `948395fe41ae` |
| `kidane_wold_root_fixes.jsonl` | Root-letter repair log | 955 | `856a1ae83fb0` |

### Parallel pairs (`data/parallel/`)

| File | Contents | Rows | sha256 |
|---|---|---:|---|
| `true_parallel_pairs.jsonl` | High-precision Ge'ez-Amharic pairs | 2,780 | `2e0975c35b7b` |
| `uncertain_pairs.jsonl` | Short / uncertain glosses | 9,066 | `46251d5def59` |

### Corpora (`data/corpora/`)

| File | Contents | Rows | sha256 |
|---|---|---:|---|
| `yared_shiferaw_corpus.txt` | Yared Shiferaw prose | 1,266 lines | `7ab49a9cf4d0` |
| `merho_ges_prose_rules.txt` | Merho Ges prose and rules | 4,818 lines | `7feadbc44e1a` |
| `geez_geez_monolingual.jsonl` | Monolingual Ge'ez text | 1,388 | `9b5ba56027cb` |
| `phrasebook_pairs.jsonl` | Ge'ez-Amharic phrasebook pairs | 218 | `2320459848de` |

## Loading the gold files (Python)

```python
import json

def load_gold(path, flagged_path="data/paradigms/merho_ges_gold_flagged_rows.tsv"):
    flagged = set()
    with open(flagged_path, encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            flagged.add((parts[0], int(parts[2]), int(parts[4])))  # split, file_line, row
    records = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                records.append((n, json.loads(line)))
    return records, flagged
```

Rows listed in the flagged-rows file stay in the files but must be skipped for training and scoring. See `docs/schema.md` for the field reference.

## Checks

```bash
python scripts/check_dataset.py            # must print CLEAN
python scripts/check_dataset.py --list     # print every problem
```

The check verifies: every line is a JSON record with the documented fields; every loaded form is one Ge'ez word; roots are 2-5 first-order letters; no Latin letters; labels are from the documented set; nouns and adjectives carry no verb labels; no duplicate pairs; no root in more than one split; every flagged row points at a real row.

## Known limits

- 17 gold rows are flagged and excluded from training and scoring; the reasons are in `merho_ges_gold_flagged_rows.tsv`.
- The change log keeps every original value before correction; the files hold the corrected values.
- 1 exact duplicate pair is kept on purpose (the book prints the same form twice); see `merho_ges_gold_allowed_duplicates.tsv`.

## License

Apache License 2.0.
