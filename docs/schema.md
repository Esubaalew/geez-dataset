# Schema: Merho Ges gold files

Field reference for `data/paradigms/merho_ges_gold_{train,val,test}.jsonl`. One JSON record per line. The checker (`scripts/check_dataset.py`) enforces this schema.

## Record fields

Required fields (every record has these):

| Field | Type | Description |
|---|---|---|
| `record_id` | string | Stable id: the first 12 hex digits of sha1(`page_number|title_or_lemma|raw_transcription`), computed once from the values as extracted. Never recomputed: a corrected title or a merged record keeps its id. |
| `category` | string | `verb_conjugation`, `noun_declension`, `grammatical_rule`, or a lexical record. A record with an empty root is kept, and its rows do not load. |
| `root` | string | The record's root: 2-5 Ge'ez letters in the 1st order of their series, hyphen-separated (e.g. `ሀ-ለ-ወ`). Empty when every row carries its own root. Not used when `root_unsettled` is set. |
| `table_data` | array | The paradigm rows (see below). |
| `page_number` | integer | Printed book page. |

Optional fields:

| Field | Type | Description |
|---|---|---|
| `title_or_lemma` | string | Headword as printed; may carry `/`-variants. |
| `stem` | string | The record's stem: the rows' stem when they agree, else the headword row's. One of the stem values below. |
| `paradigm_class` | string or null | Class label printed on the entry: one of the six heads (አርእስት) or a branch (ሠራዊት) of that head. The heads, the branches, and the book's abbreviations are in the README, under "Reading a Merho Ges entry". Null on noun and grammar records. A few records still carry the label as printed, with more than one class. |
| `sub_pattern` | string | The sub-class or derived pattern the book files the verb under (e.g. `ተቀተለ`), when there is one. |
| `amharic_notes` | string | Amharic notes from the book. |
| `raw_transcription` | string | The printed entry, in reading order. |
| `source` | string | Source work. |
| `root_unsettled` | boolean | When set, the record root is not used; rows with their own root still load. |
| `source_record_id` | string | On rows taken over from a merged record: the original record's id. |
| `merged_record_ids` | array | Ids merged into this record. |

## Row fields (`table_data`)

| Field | Type | Description |
|---|---|---|
| `person` | string | `1`, `2`, or `3`. |
| `gender` | string | `m`, `f`, or `c`. |
| `number` | string | `s` or `p`. |
| `tense` | string | `past`, `present`, `subjunctive`, or `imperative`. |
| `geez_form` | string | The Ge'ez form. `/` separates printed variants; `(...)` notes are dropped when loading. |
| `amharic_equivalent` | string | Amharic gloss. |
| `root` | string | Overrides the record root for this row. |
| `stem` | string | Overrides the record stem for this row. |
| `type` | string | `verb` (default), `noun`, or `adjective`. |
| `object` | string | Object suffix as person/gender/number joined (e.g. `3ms`); empty when absent. |
| `source_row` | integer | Original row index, set when a printed cell was split into rows. |
| `source_variant` | integer | Variant index, set when a printed cell was split. |

## Allowed values

- **type**: `verb`, `noun`, `adjective`
- **tense**: `past`, `present`, `subjunctive`, `imperative` (the extraction's `jussive` is written as `subjunctive`)
- **stem**: `basic`, `passive`, `causative`, `reciprocal`, `aste`
- **person/gender/number** (verbs): the 10 combinations `1cs`, `1cp`, `2ms`, `2fs`, `2mp`, `2fp`, `3ms`, `3fs`, `3mp`, `3fp`
- **object**: the same 10 combinations joined (e.g. `3ms`); empty when the row has no object suffix
- **number** (nouns): `s`, `p`
- **gender** (adjectives): `m`, `f`, `c`, or empty
- **root**: 2-5 letters, each in the 1st order of its Ge'ez series (ሀ ለ ሐ, not ሃ ለ ሓ), hyphen-separated

## Loading rules

- A row's own `root`, `stem`, `type`, and `object` override the record's.
- A printed cell with two forms of different stems is split into one row per form (`source_variant`), each with its own `stem`; the record `stem` is the stem of the first row, and a verb row without a `stem` of its own takes the record's.
- Nouns and adjectives carry no verb labels (`tense`, `person`, `object`).
- Rows with an empty root, and records marked `root_unsettled` are kept in the files but do not load for training or scoring.
- A "pair" is one form of one row with the labels the row gives it. No pair appears twice in one split or across splits, except the pairs listed in `merho_ges_gold_allowed_duplicates.tsv`.
- No root appears in more than one split (train / val / test).
- Variant notation: a `geez_form` cell like `ሃልሀ / ሀልሀ` holds two variants; a parenthesized note like `form (variant)` is dropped and only `form` loads.

## The unified file (all books)

`data/unified/geez_morphology_rows.jsonl` holds the gold paradigm rows and the rows of every other book, one schema. It has more classes than the gold paradigm files above: `verb`, `noun`, `adjective`, `nominal` (Kidane Wold's headwords, which print no noun or adjective label), `infinitive`, `gerund`, `verbal_noun`, and the rootless function-word classes (`pronoun`, `preposition`, `particle`, `numeral`, `demonstrative`, `adverb`), plus the slots `possessor` and `negated`. `scripts/check_dataset.py` checks the gold paradigm files (`verb`, `noun`, `adjective`) and then runs `scripts/check_unified.py`, which checks the unified file and the book files under `data/books`. The fields, statuses, split rule and the checked-table files are in `data/unified/README.md`.

## Root fields in the other files

The checker also reads the root fields of the dictionaries, the Kidane Wold tables and the synthetic files: every key named `root` or ending in `_root`. None may hold the placeholder `CHECK`.

- `geez_amharic_dictionary.jsonl`, `lexicon/classical_dictionary_kidane_wold.jsonl`: `root` (Ge'ez text from the source; mostly null, sometimes empty), `inferred_root` (Latin root notation, e.g. `q-t-l`), `root_confidence`, `root_notes` (free text: how the root was inferred, or why there is none). An unsettled root is null, and `root_notes` gives the reason.
- `lexicon/book_forms.jsonl`: one printed form per line, not generated: `root` (Ge'ez letters, as in the gold files, or null), `form`, `type`, `person`, `gender`, `number`, `tense`, `stem`, `object` (the labels of the gold rows), `book`, `page` (printed page), `traditional_label` (the book's own tag as printed), `confidence` (of the reading), `status` (empty, `CHECK`, `CONFLICT` or `NO_ROOT`), `source_id` (row of the transcription), `note`, and `split` (`train`, or `heldout` when the root or form is a gold val/test one).
- `parallel/uncertain_pairs.jsonl`: a row may carry `note`, a free-text reason why it is not a trusted pair.
