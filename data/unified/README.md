# data/unified: one schema for every labelled form

`geez_morphology_rows.jsonl` holds every labelled form of the dataset in one row schema: the Merho Ges gold paradigms
and all rows of `lexicon/book_forms.jsonl` (ርባሐ ስም ወአንቀጽ, Kidane Wold's grammar tables and dictionary, the typed
Mesehaf Gese Wesewasew, ፍሬ ግእዝ, የግእዝ መማሪያ, ግዕዝ ቋንቋ ፪). Nothing is dropped: a row that cannot load keeps a
`status` and a `status_reason`. `scripts/check_unified.py` checks the file; `book_root_splits.tsv` lists the split of every
book-only root with its class mark.

| field | meaning |
|---|---|
| `id` | `u000001`, in file order |
| `form` | one Ge'ez word |
| `root` | first-order letters joined by `-`; `null` for words without a root |
| `word_class` | `verb`, `noun`, `adjective`, `infinitive`, `gerund` (ቦዝ, converb), `verbal_noun`, `pronoun`, `demonstrative`, `preposition`, `particle`, `numeral`, `adverb`, `nominal` (a noun or adjective of Kidane Wold's dictionary: the book prints no class) |
| `stem` | `basic`, `passive`, `causative`, `reciprocal`, `aste`, `aste_reciprocal` (verbs, infinitives, gerunds, verbal nouns) |
| `tense` | `past`, `present`, `subjunctive`, `imperative` (verbs) |
| `person`, `gender`, `number` | the subject of a verb or gerund; gender and number of a noun or adjective; the person of a pronoun |
| `object` | object suffix of a verb or gerund (`3ms`, `2fp`, `1cs` ...) |
| `possessor` | pronominal suffix on a noun, infinitive, verbal noun, preposition or particle (same codes) |
| `negated` | the form carries ኢ- |
| `source`, `book`, `page`, `source_ref` | where the row was read: `gold` or `book`, the book, the printed page, the record or row file and line |
| `evidence` | how the root or label was settled (`root_basis: ...`, row-order labels checked, ...) |
| `also_in` | other books and pages that print the same form with the same root and labels |
| `status` | `""` loads; `CHECK` (reading or label not settled); `CONFLICT` (gold gives the form another root); `NO_ROOT`; `FLAGGED` (gold flagged row); `EXCLUDED` (phrase or no word class) |
| `split` | `train`, `val`, `test` |

## Splits

- Gold rows keep their file's split.
- A book row follows, in this order: the split of the gold val/test form it spells; the split of its gold root (exact
  root first, so the twin roots ሐ-መ-የ / ኀ-መ-የ stay apart); the split of its book-only root.
- Book-only roots: grouped by (verb or nominal, class mark of the verb index), sorted by sha256 of the folded
  consonants; the first 8% of a group go to val, the next 8% to test, the rest to train; a group of fewer than 7 roots is all
  train. A root is never in two splits among the rows that load.
- Words without a root (pronouns, prepositions, particles, numerals, demonstratives): the same 8% / 8% rule by a hash
  of the folded form, per word class.

## Roots of the teaching-book verbs

Teaching books often print no root. `work_1010_full/lemma_roots.tsv` gives each lemma a root with its evidence: the gold
record titled with the lemma, a gold form, other rows of the books, or the lemma minus its prefix when that matches one
gold root, plus five hand-set roots listed in `apply_lemma_roots_1010.py`. No other tool is used.

## Labels read from the order of the page

Some tables print no tense or person labels (confidence "medium" in the row files). Their labels follow the row order of
the page (checked on the scan of ፍሬ ግእዝ pp.133–134). A row loads only if its form passes two rules of the books (a past
form carries no imperfect prefix unless the stem is derived; a present or subjunctive form starts with the prefix of its
person) and its whole table has no failing row. The rest stay `CHECK`.

## Tables checked against the scan

A table page whose every form and label agrees with the printed page loads as a unit (`work_1010_full/page_verified.tsv`:
book, page, root, the rows kept back). Four small tables sit beside it, each row checked on the scan:

- `object_fixes.tsv`: the object suffix read from the form where the printed row order is shifted;
- `possessor_pages.tsv`: in a possessive-suffix table of an adjective the suffix pronoun is the `possessor`, and the
  base word keeps its own gender and number;
- `label_fixes.tsv`: labels read from a printed paradigm and its glosses (ርባሐ p.60, the ከፈለ forms with ኢ-), and the
  few printed misprints or misreadings corrected (`new_form`; the printed spelling stays in `evidence`);
- spelling lists with no tense, person or stem (ርባሐ pp.59–62: the vowel orders of a root, pairs of look-alike
  verbs) are `EXCLUDED`.

## The class `nominal`

Kidane Wold prints no noun/adjective label (his preface and the extraction notes say so). A derived word of his
dictionary whose root is a gold root loads as `nominal`; `number` is set only where the book prints it (ብ plural marker,
ሲያበዛ X ይላል), `gender` only for ሴ. Kidane words whose roots come only from his own entries stay `CHECK`.

## ኀ and ኅ

The scans do not separate ኀ (1st order) from ኅ (6th order) reliably. Where a form cannot be read, the gold pattern
decides: the present of ኀደገ-type verbs has ኀ, the subjunctive and the imperative have ኅ.

## Reading the rows for training

`dataset_loader.load_unified(dataset_dir, split, sources=("book",))` returns the rows that load (status `""`) as pairs;
`dataset_loader.target_text` writes the target of every class (the shapes are in its docstring), and
`analyzer.parse_neural_output` reads them back.
