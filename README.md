# geez-dataset

Classical Ge'ez morphology. The gold files are paradigms from *Merho Ges Wesewasew Ze-Yared* (መርሐ ግስ ወሰዋሰው ዘያሬድ), read from the printed book. The rest of the repository is lexicon, Ge'ez–Amharic pairs, prose, and synthetic paradigms.

## Version

2.0.0. The previous version is the tag `v1` (commit `337cdf0`). Differences: [docs/CHANGES.md](docs/CHANGES.md).

## Layout

```
data/paradigms/     gold splits, and synthetic forms used in training
data/unified/       every labelled form of every book in one row schema, with splits
data/books/         the forms of ፍሬ ግእዝ and የግዕዝ መማሪያ (ለይኩን ብርሃኑ), one form per line
data/synthetic/     synthetic forms whose roots sit in val or test
data/lexicon/       Kidane Wold, and the concise Ge'ez–Amharic glossary
data/parallel/      Ge'ez–Amharic pairs
data/corpora/       prose and the phrasebook
docs/schema.md      fields in the gold files
docs/CHANGES.md     differences from v1
docs/DATASHEET.md   contents, method, intended use, limits
scripts/check_dataset.py   checks the gold files and the other data files
scripts/check_unified.py   checks data/unified
```

Three combined files sit directly under `data/`: `geez_amharic_dictionary.jsonl`, `geez_literature_corpus.txt`, and `true_parallel_pairs.jsonl`. They are separate from the split files in `data/parallel/` and `data/corpora/`. Training reads `data/paradigms/`.

## Gold files

| File | Records |
|---|---:|
| `data/paradigms/merho_ges_gold_train.jsonl` | 1,116 |
| `data/paradigms/merho_ges_gold_val.jsonl` | 136 |
| `data/paradigms/merho_ges_gold_test.jsonl` | 219 |

A root appears in one split. Each record keeps a `record_id`. A `geez_form` may hold more than one spelling, separated by ` / `. Noun and adjective rows have a `type` and no tense.

All 323 previously flagged rows in `merho_ges_gold_flagged_rows.tsv` have been resolved against the printed *Merho Ges* scan, Yared Shiferaw's typed edition, and dual OCR passes (either corrected in place and unflagged or removed when unprinted/garbled), leaving 0 flagged rows. Three repeated pairs are listed in `merho_ges_gold_allowed_duplicates.tsv` because the book prints each of them twice.

Field reference: [docs/schema.md](docs/schema.md).

## Reading a Merho Ges entry

The book files every verb under one of six heads (አርእስት). A branch (ሠራዊት) takes the rules of its head. Page 19 states them. ራሱ means the head is its own branch. ሞርቅሐን የመሰለ means that head follows the pattern of ሞርቅሐን.

| አርእስት | ሠራዊት |
|---|---|
| ቀተለ | ቀደሰ, ገብረ, ሐተተ |
| ባረከ | ራሱ |
| ሴሰየ | አንጌገየ |
| ክህለ | ራሱ ብቻ |
| ጦመረ | ሞርቅሐን የመሰለ |
| ተንበለ | ማህረከ |

A `paradigm_class` in the gold files is the label printed on that entry. It may be the head or a branch.

Beside a form, the book uses the shorts below. The key is printed on pages 16 and 17, headed በምኅጻረ ቃል ለተጻፉ ማብራሪያ. Read the short as the full form in the second column. A paradigm line usually drops the dot the key prints (`ባዕ ቅ` is the key's `ባዕ.ቅ`). The lines write `በብ` where the key prints `ለብ`, and one line writes `ለ፩ ለብ` where the key prints `ለአ ለብ`. The last rows are the heads and branches cut short: `ቀተ` is ቀተለ.

| Short | Full |
|---|---|
| ው | ውስጠዘ |
| በብ | ለብዙኅ |
| ለሴ | ለሴት |
| ባዕ ቅ | ባዕድ ቅጽል |
| መድ | መድበል |
| ሳ ዘ | ሳቢ ዘር |
| ጥ ዘ | ጥሬ ዘር |
| ዘመ ዘ | ዘመድ ዘር |
| ዘ ው | ዘር ውስጠዘ |
| ጥ ው | ጥሬ ውስጠዘ |
| ባዕ ሣ ቅ | ባዕድ ሣልስ ቅጽል |
| ባዕ ጥ | ባዕድ ጥሬ |
| ባዕ ጉ | ባዕድ ጉልት |
| ባዕ ዘ | ባዕድ ዘር |
| ባዕ ከም | ባዕድ ከምዕላድ |
| ምዕ ው | ምዕላድ ውስጠዘ |
| ምዕ | ምዕላድ |
| ጉል | ጉልት |
| ለአ ለብ | ለአንድ ለብዙኅ |
| የሰ ስ | የሰው ስም |
| አስ አደ | አስማተ አደው |
| አስ አን | አስማተ አንስት |
| አስ አህ | አስማተ አህጉር |
| አብ | አብዛሂ |
| ጉል ው | ጉልት ውስጠዘ |
| ጥ ምዕ | ጥሬ ምዕላድ |
| ጥ ምዕ ው | ጥሬ ምዕላድ ውስጠዘ |
| ባዕ ዘ ው | ባዕድ ዘር ውስጠዘ |
| እን | እንዲል |
| የሁ | የሁሉ |
| የሴቶ | የሴቶች |
| አው | አውርድ |
| ግስ | ግእስ |
| በቀ | በቁሙ |
| ቀተ | ቀተለ |
| ባረ | ባረከ |
| ክህ | ክህለ |
| ማህ | ማህረከ |
| ቀደ | ቀደሰ |
| ተን | ተንበለ |
| ሴሰ | ሴሰየ |
| ጦመ | ጦመረ |
| ገብ | ገብረ |

## Other files

| File | Lines |
|---|---:|
| `data/paradigms/synthetic_morphology_train.jsonl` | 120,685 |
| `data/paradigms/synthetic_morphology_analyze.jsonl` | 120,685 |
| `data/synthetic/synthetic_forms_for_val_test_roots.jsonl` | 17,571 |
| `data/synthetic/synthetic_forms_for_val_test_roots_analyze.jsonl` | 17,571 |
| `data/lexicon/classical_dictionary_kidane_wold.jsonl` | 13,234 |
| `data/lexicon/modern_geez_amharic_dictionary.jsonl` | 1,722 |
| `data/lexicon/kidane_wold_verb_triples.jsonl` | 583 |
| `data/lexicon/kidane_wold_verb_triples_rejected.jsonl` | 137 |
| `data/lexicon/kidane_wold_root_fixes.jsonl` | 1,060 |
| `data/lexicon/book_forms.jsonl` | 14,110 |
| `data/parallel/true_parallel_pairs.jsonl` | 2,779 |
| `data/parallel/uncertain_pairs.jsonl` | 9,067 |
| `data/corpora/yared_shiferaw_corpus.txt` | 1,266 |
| `data/corpora/merho_ges_prose_rules.txt` | 4,818 |
| `data/corpora/geez_geez_monolingual.jsonl` | 1,388 |
| `data/corpora/phrasebook_pairs.jsonl` | 218 |
| `data/geez_amharic_dictionary.jsonl` | 14,956 |
| `data/geez_literature_corpus.txt` | 6,090 |
| `data/unified/geez_morphology_rows.jsonl` | 29,987 |
| `data/books/fre_geez/forms.jsonl` | 4,039 |
| `data/books/geezbook_1z/forms.jsonl` | 1,817 |
| `data/unified/book_root_splits.tsv` | 336 |
| `data/true_parallel_pairs.jsonl` | 2,997 |

A synthetic line is `{"features": {...}, "surface_form": "..."}`. The analyze files use `"analysis"` instead of `"features"`.

`data/lexicon/book_forms.jsonl` holds forms printed in the books other than the Merho Ges gold, in the gold label set: *ርባሐ ስም ወአንቀጽ* (አለቃ ደስታ ተክለ ወልድ, 1946 E.C.), the grammar tables and the dictionary of Kidane Wold, the teaching books ፍሬ ግእዝ, የግእዝ መማሪያ (Year 1) and ግዕዝ ቋንቋ ፪, and the first 14 rows (Kidane Wold triples of ወ-ቀ-የ, ወ-ረ-ወ, ወ-ረ-የ; *Mesehaf Gese Wesewasew* nouns and adjectives of መ-ከ-ለ and ሰ-ነ-ገ). Each row names its book and printed page. The root is the book's own (paradigm head, printed triple, derived-stem section), or the root of the gold record with the same headword; it is never inferred. `status` is empty for a row that loads, `CHECK` for a reading or label that is not settled or a type the training target has no slot for (infinitives, gerunds, forms with a possessive suffix), `CONFLICT` when the gold gives the same form another root, and `NO_ROOT`. `split` is `heldout` when the root or the form is a gold val/test one: those rows are never trained on and score the model on forms from other books; the rest are `train`.

`data/books/<book>/forms.jsonl` lists every form of the entry lists of ፍሬ ግእዝ (4,039 forms of 2,105 entries) and የግዕዝ መማሪያ by ለይኩን ብርሃኑ (1,817 forms of 1,751 entries). A line has `form`, `root` (as printed in the entry; for a form without one, the root of a row of the same spelling when the entry's headword is that root; else null), `pos`, `number`, `gender`, `class` (the paradigm class), `book`, `page` (scan page; one scan page holds two printed pages) and `split`. The same forms are rows of `data/unified/` with `source_ref` pointing at the line. Verbs there do not load: the entry lists give no tense or person. Eight forms of የግዕዝ መማሪያ whose reading is not settled are left out.

Headwords in `classical_dictionary_kidane_wold.jsonl` were taken from the typed Kidane Wold transcription in [geezorg/data](https://github.com/geezorg/data) (CC BY-SA 4.0, commit `3904462c`).

## Unified rows

`data/unified/geez_morphology_rows.jsonl` holds 29,987 labelled forms in one schema: the gold paradigm rows and the rows of seven other books (ርባሐ ስም ወአንቀጽ, Kidane Wold's tables and dictionary, the typed Mesehaf Gese Wesewasew, ፍሬ ግእዝ, የግእዝ መማሪያ (Year 1), የግዕዝ መማሪያ (ለይኩን ብርሃኑ), ግዕዝ ቋንቋ ፪). Every row names its book and page. A row that does not load keeps its `status` and the reason. Fields, statuses and the split rule: [data/unified/README.md](data/unified/README.md).

| Rows | train | val | test | not loaded |
|---|---:|---:|---:|---:|
| gold (Merho Ges) | 8,104 | 1,165 | 1,548 | 1,128 |
| other books | 8,083 | 422 | 497 | 9,040 |

Not loaded, other books: `NO_ROOT` 3,807, `CHECK` 4,653, `EXCLUDED` 580. Not loaded, gold: `NO_ROOT` 1,128, `FLAGGED` 0.

## Sources

| Work | Author | Pages | Used for |
|---|---|---:|---|
| *Merho Ges Wesewasew Ze-Yared* (መርኆ ግስ ወሰዋስው ዘያሬድ) | traditional church grammar | 509 | gold paradigms |
| *Mets'hafe Sewasew Weges Wemezgebe Qalat Haddis*, 1948 E.C. | Aleqa Kidane Wold Kifle | 917 | `classical_dictionary_kidane_wold.jsonl` and the files derived from it |
| *Mesehaf Gese Wesewasew* | Liqe Liqawunt Yared Shiferaw | 422 | `yared_shiferaw_corpus.txt` |
| ግዕዝ አማርኛ መዝገበ ቃላት | | 102 | `modern_geez_amharic_dictionary.jsonl`, `phrasebook_pairs.jsonl` |

## How the data was made

- The gold rows were read from scans of the printed Merho Ges pages (the scans are not distributed here) by OCR, then corrected against the page images. Each record keeps the page number and the raw reading of its entry.
- Kidane Wold headwords come from the geezorg typed transcription named above.
- Kidane Wold definitions were split into Ge'ez–Amharic pairs, Ge'ez-only passages, and uncertain fragments by a score over Ge'ez and Amharic function words and affixes: `true_parallel_pairs.jsonl` (Amharic dominates), `geez_geez_monolingual.jsonl` (Ge'ez dominates), and `uncertain_pairs.jsonl`.
- Synthetic forms are generated by the paradigm generator in the companion `geez-morphology` repository. It conjugates only roots that have a verb entry in the dictionary, a root in the gold files, or a Kidane Wold verb triple, plus eight roots checked by hand (`m-h2-l`, `m-s-l`, `S-w-t`, `b-y-S`, `f-r-S`, `h2-r-g`, `m-s-k` and `w-k-a2`, in the root notation of the synthetic files), and it drops every line whose form is spelled exactly like a gold val or test form, and every training line whose form differs from one only by a labiovelar letter against its plain letter or by one spelling twin against the other (such as `s` and `s2`). Every synthetic line whose root is a gold val or test root, or the same root with those letters folded (such as `w-S2-a` for `w-S-a`), is held out in `data/synthetic/` and is not in the training file. The training file covers 1,118 roots; `data/synthetic/` covers 116 roots: the 77 gold val and test roots and 39 roots that equal one of them once the letters are folded. Passive, causative and aste forms are generated for Type A and quadriliteral roots, and for Type B roots whose radicals are strong and whose middle radical is not a guttural; 236 roots have none yet (Type C, Type D, the weak classes and 4 Type B roots).
- Split rule: a root appears in only one of train, val, and test.

## Known limits

- Only the Merho Ges gold is checked page by page. Rows of the other books are read by hand and by rule from scans and typed editions; `CHECK` rows are the readings not settled.
- A Kidane Wold derivative whose root no other book gives is class `nominal`, in train only.
- Spelling twins (ሐ-በ-ለ / ኀ-በ-ለ, ቀ-ጸ-ለ / ቈ-ጸ-ለ and the like) count as different roots for the split; 19 such pairs sit in different splits.

- Rows with no root yet are kept in the files and do not load (1,128 pairs).
- The rows listed in `merho_ges_gold_flagged_rows.tsv` do not load.
- 8,095 of the 8,489 noun and adjective rows have no Amharic gloss.
- 19 record titles still carry a parenthesis: they are book section headings printed with parentheses.
- One dictionary entry (id 7546, page 585) has no root: its definition belongs to the verb መኅፀ, and the two entries were merged. Its `inferred_root` is null in both dictionary files and its `new_root` is null in `kidane_wold_root_fixes.jsonl`; `root_notes` gives the reason. Its pair was moved from `true_parallel_pairs.jsonl` to `uncertain_pairs.jsonl`, with a `note`.
- 40 more dictionary entries have a null `inferred_root` in both dictionary files: the root is unclear, or the word is a loan with no Ge'ez root. `root_notes` gives the reason.

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
python scripts/check_unified.py .
cd data && sha256sum -c SHA256SUMS
```

The checker prints how many pairs load. It requires one Ge'ez word per loaded form, a root of 2–5 letters in the first order, labels from the set in `docs/schema.md`, no duplicate pair, and no root in more than one split. It also fails if any root field in the gold files, the dictionaries, the Kidane Wold tables or the synthetic files holds the placeholder `CHECK`.

## License

The files under `data/` are licensed under CC BY-SA 4.0 (see [LICENSE-DATA](LICENSE-DATA)). `scripts/check_dataset.py` and `scripts/check_unified.py` are licensed under the Apache License 2.0 (see [LICENSE](LICENSE)).

## Citation

See [CITATION.cff](CITATION.cff).
