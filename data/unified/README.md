# data/unified: one schema for every labelled form

`geez_morphology_rows.jsonl` holds every labelled form of the dataset in one row schema: the Merho Ges gold paradigms
and all rows of `lexicon/book_forms.jsonl` (ርባሐ ስም ወአንቀጽ, Kidane Wold's grammar tables and dictionary, the typed
Mesehaf Gese Wesewasew, ፍሬ ግእዝ, የግእዝ መማሪያ, ግዕዝ ቋንቋ ፪). Nothing is dropped: a row that cannot load keeps a
`status` and a `status_reason`. `scripts/check_unified.py` checks the file; `book_root_splits.tsv` lists the split of every
book-only root with its class mark.

| field | meaning |
|---|---|
| `id` | `u000001`, in file order; new rows are appended and existing ids never change |
| `form` | one Ge'ez word |
| `root` | first-order letters joined by `-`; `null` for words without a root |
| `word_class` | `verb`, `noun`, `adjective`, `infinitive`, `gerund` (ቦዝ, converb), `verbal_noun`, `pronoun`, `demonstrative`, `preposition`, `particle`, `numeral` (with its root), `adverb`, `nominal` (a noun or adjective of Kidane Wold's dictionary: the book prints no class), `proper_noun` (a name, which needs no root) |
| `stem` | `basic`, `passive`, `causative`, `reciprocal`, `aste`, `aste_reciprocal` (verbs, infinitives, gerunds, verbal nouns) |
| `tense` | `past`, `present`, `subjunctive`, `imperative` (verbs) |
| `person`, `gender`, `number` | the subject of a verb or gerund; gender and number of a noun or adjective; the person of a pronoun. `number` is `s`, `p`, or `sp` for a noun used unchanged as singular and plural |
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
- Words without a root (pronouns, prepositions, particles, demonstratives): the same 8% / 8% rule by a hash
  of the folded form, per word class.

## Roots of the teaching-book verbs

Teaching books often print no root. Each lemma gets a root with its evidence: the gold record titled with the lemma, a gold form, other rows of the books, or the lemma minus its prefix when that matches one gold root, plus five roots set by hand. The evidence is in the row's `evidence` field. The evidence of every root is stated per row; a root is never taken from a tool or a model.

## Labels read from the order of the page

Some tables print no tense or person labels (confidence "medium" in the row files). Their labels follow the row order of
the page (checked on the scan of ፍሬ ግእዝ pp.133–134). A row loads only if its form passes two rules of the books (a past
form carries no imperfect prefix unless the stem is derived; a present or subjunctive form starts with the prefix of its
person) and its whole table has no failing row. The rest stay `CHECK`.

## Tables checked against the scan

A table page whose every form and label agrees with the printed page loads as a unit. Further rows were checked on the scan one by one:

- the object suffix read from the form where the printed row order is shifted;
- in a possessive-suffix table of an adjective the suffix pronoun is the `possessor`, and the base word keeps its own gender and number;
- labels read from a printed paradigm and its glosses (ርባሐ p.60, the ከፈለ forms with ኢ-), and the few printed misprints or misreadings corrected (the printed spelling stays in `evidence`);
- forms the book prints wrongly (slips in a printed table) or that are exercise answers, not words: held out as `CHECK` or `EXCLUDED`, never corrected;
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

In the geez-morphology repository, `dataset_loader.load_unified(dataset_dir, split, sources=("book",))` returns the rows that load (status `""`) as pairs;
`dataset_loader.target_text` writes the target of every class (the shapes are in its docstring), and
`analyzer.parse_neural_output` reads them back.

## ፍሬ ግእዝ and የግዕዝ መማሪያ entry lists

Rows with `source_ref` `data/books/<book>/forms.jsonl:<line>` come from the entry lists of these two books. `page` is the scan page. A verb row is `CHECK`: the lists give no tense or person. A noun or adjective loads when the entry prints its root and the form has a number; without a root it is `NO_ROOT`. A row that repeats a form and labels already in the file is `EXCLUDED`. A row without a root takes the split of the rows of the same spelling, twin letters merged (gold rows keep theirs); when the entry's headword is the root of those rows, the row takes that root too.
Splits follow the rules above. A root that already has a split keeps it; a root that differs from a split root only by a twin letter (ሀ/ሐ/ኀ, ሰ/ሠ, ጸ/ፀ, አ/ዐ) or a labiovelar takes that split; the new book-only roots are split by the 8% / 8% rule among themselves and added to `book_root_splits.tsv`.

## Yared Shiferaw's Mesehaf Gese Wesewasew

Rows with `source_ref` `data/books/yared_shiferaw/forms.jsonl:<line>` come from the entries of this verb book; `page` is the printed page. Forms of entries whose reading is not settled and forms that cannot be read on the scan are left out. The roots are the book's own, letter for letter: a labialized letter stays apart from the plain one (ቈ-ጸ-ረ and ቀ-ጸ-ረ, ኰ-ረ-ጸ and ከ-ረ-ጸ are four roots). The rows follow the rules of the entry lists above, with these differences:

- a root that already has a split keeps it; every root first found in this book is in train (275 roots added to `book_root_splits.tsv`), except ቈ-ረ-በ, which is in test with ቈረበ of ፍሬ ግእዝ;
- twin letters are only compared, never merged into the root: a row whose root differs from a val/test root only by a twin letter or a labiovelar stays `CHECK`;
- a row whose form is a gold val/test form under a train root is `EXCLUDED`; a row whose spelling already loads in another split under another root stays `CHECK`. Rows already in the file are not changed.

## Ge'ez verb list

Rows with `source_ref` `data/books/verb_list/forms.jsonl:<line>` are the headwords of a 25-page Ge'ez verb list with class marks and Amharic glosses; `page` is the page of the list. A headword is read as the 3rd person masculine singular perfect; its stem follows the prefix (none: basic, ተ-: passive, አ-: causative, አስተ-: aste). The root is derived from the headword letter by letter, with the prefix stripped or kept as a radical as settled for each entry, or is the root of the same verb in another book when the meaning matches. Where the class mark of the list differs from the gold, the gold class is used when the two agree in substance; otherwise the row stays `CHECK`. Rows whose root, prefix or class is not settled stay `CHECK`.

Splits: a root that already has a split keeps it; a root found only as a twin-letter variant of a val/test root takes that split; a root with no exact or twin match is in train (65 roots added to `book_root_splits.tsv`). A row whose root differs from a root of another split only by a twin letter, whose form is a gold val/test form under a root of another split, or whose spelling loads in another split stays `CHECK` or `EXCLUDED`. A headword that repeats a row already in the file is `EXCLUDED`.

## Counts

58,050 rows. Rows that load: 35,972 (train 28,989, val 2,962, test 4,021): gold 11,004 (train 8,205, val 1,184, test 1,615); other books 24,968 (train 20,784, val 1,778, test 2,406). Not loaded: 22,078 (gold 956, other books 21,122).

## Corrected rows file

`geez_morphology_rows_reviewed.jsonl` is the unified file with corrections to held rows applied. It is checked with
`python scripts/check_unified.py . data/unified/geez_morphology_rows_reviewed.jsonl`. The base file and the
book files are not changed.

The corrections give a word class, a root or no root, and a note for the 1,435 held forms
that occur in the AGE Ge'ez–Amharic corpus ([HenokB/AGE-Dataset](https://github.com/HenokB/AGE-Dataset)), most frequent first. A corrected row loads only when the dataset supports it: a closed-class word
(pronoun, demonstrative, preposition, particle, adverb) loads with no root, and so may a `proper_noun` (a name); a numeral loads with its root; a word with a root loads
only if that root is already the root of settled rows, and it takes that root's split; nouns and adjectives
need a number and verbs their full labels. Other rows stay held and their `status_reason` records the
proposal and why it does not load (root not attested, noun without a root, labels missing).
A held row's `status_reason` records the proposed correction and why it does not load. Where a corrected row replaces a root or split printed in a
book, its `evidence` says so (`Settled: ...`), and `check_unified.py` reports these as overrides.

## Adjectives with no root

An adjective loads without a root only if `rootless_derived.tsv` lists it. Its columns are `form`, `base` (the rootless word it is derived from) and `ref` (page or reference). The form must end in -ዊ, -ዊት or -ውያን, and its base must load without a root, as a noun on `rootless_nouns.tsv` or as a name, in the same split. The base is given explicitly because the stem can change (ዕብራይ, ዕብራዊ).
