# geez-dataset

Classical Ge'ez morphology. The gold files are paradigms from *Merho Ges Wesewasew Ze-Yared* (መርሐ ግስ ወሰዋሰው ዘያሬድ), read from the printed book. The rest of the repository is lexicon, Ge'ez–Amharic pairs, prose, and synthetic paradigms.

## Layout

```
data/paradigms/     gold splits, and synthetic forms used in training
data/lexicon/       Kidane Wold, and the concise Ge'ez–Amharic glossary
data/parallel/      Ge'ez–Amharic pairs
data/corpora/       prose and the phrasebook
data/synthetic/     synthetic forms whose roots sit in val or test
docs/schema.md      fields in the gold files
scripts/check_dataset.py
scans/              page images
```

`scans/merho_ges_511/page_001.jpg` through `page_509.jpg` are the Merho Ges pages. `scans/sewasew_1_192/` is Kidane Wold. The source PDFs stay on disk (`*.pdf` is ignored). `output/` is local generator output and is not part of the dataset.

`dictionary.jsonl`, `morphology.jsonl`, and `errata.jsonl` at the repository root are inputs to the older extractors. `build_canonical_dataset.py` writes four bundle files directly under `data/`: `verbs_rbha_anqets.jsonl`, `geez_amharic_dictionary.jsonl`, `geez_literature_corpus.txt`, and `true_parallel_pairs.jsonl`. Those bundles are separate from the split files in `data/parallel/` and `data/corpora/`. Training reads `data/paradigms/`.

## Gold files

| File | Records |
|---|---:|
| `data/paradigms/merho_ges_gold_train.jsonl` | 1,118 |
| `data/paradigms/merho_ges_gold_val.jsonl` | 135 |
| `data/paradigms/merho_ges_gold_test.jsonl` | 219 |

A root appears in one split. Each record keeps a `record_id`. A `geez_form` may hold more than one spelling, separated by ` / `. Noun and adjective rows have a `type` and no tense.

Eighteen rows are listed in `merho_ges_gold_flagged_rows.tsv`. They stay in the files and stay out of the pairs that load. One repeated pair is listed in `merho_ges_gold_allowed_duplicates.tsv` because the book prints it twice.

Field reference: [docs/schema.md](docs/schema.md).

## Other files

| File | Lines |
|---|---:|
| `data/paradigms/synthetic_morphology_train.jsonl` | 210,348 |
| `data/paradigms/synthetic_morphology_analyze.jsonl` | 210,348 |
| `data/synthetic/synthetic_forms_for_val_test_roots.jsonl` | 6,629 |
| `data/synthetic/synthetic_forms_for_val_test_roots_analyze.jsonl` | 6,629 |
| `data/lexicon/classical_dictionary_kidane_wold.jsonl` | 13,234 |
| `data/lexicon/modern_geez_amharic_dictionary.jsonl` | 1,722 |
| `data/lexicon/kidane_wold_verb_triples.jsonl` | 262 |
| `data/lexicon/kidane_wold_verb_triples_rejected.jsonl` | 326 |
| `data/lexicon/kidane_wold_root_fixes.jsonl` | 955 |
| `data/parallel/true_parallel_pairs.jsonl` | 2,780 |
| `data/parallel/uncertain_pairs.jsonl` | 9,066 |
| `data/corpora/yared_shiferaw_corpus.txt` | 1,266 |
| `data/corpora/merho_ges_prose_rules.txt` | 4,818 |
| `data/corpora/geez_geez_monolingual.jsonl` | 1,388 |
| `data/corpora/phrasebook_pairs.jsonl` | 218 |

A synthetic line is `{"features": {...}, "surface_form": "..."}`. The analyze files use `"analysis"` instead of `"features"`. The generator is in the companion `geez-morphology` repository.

Headwords in `classical_dictionary_kidane_wold.jsonl` were taken from the typed Kidane Wold transcription in [geezorg/data](https://github.com/geezorg/data) (CC BY-SA 4.0, commit `3904462c`).

## Loading a gold file

```python
import json

def load_gold(path, flagged_path="data/paradigms/merho_ges_gold_flagged_rows.tsv"):
    flagged = set()
    with open(flagged_path, encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            flagged.add((parts[0], int(parts[2]), int(parts[4])))  # split, file line, row
    records = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                records.append((n, json.loads(line)))
    return records, flagged
```

Skip a row when `(split, file_line, row)` is in `flagged`.

## Check

```bash
python scripts/check_dataset.py
python scripts/check_dataset.py --list
```

The checker prints how many pairs load. It requires one Ge'ez word per loaded form, a root of 2–5 letters in the first order, labels from the set in `docs/schema.md`, no duplicate pair, and no root in more than one split.

## License

Apache License 2.0. See [LICENSE](LICENSE).
