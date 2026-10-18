# Clitic forms

`clitic_forms.jsonl` holds word forms with Ge'ez clitics, made by rule from the settled rows of
`data/unified/geez_morphology_rows_reviewed.jsonl` (rows with an empty `status`). It is rebuilt by
`python scripts/build_clitic_forms.py`.

Ge'ez writes its proclitics joined to the next word and its enclitics joined to the end of the word:

| clitic | position | meaning | joins |
|---|---|---|---|
| ወ | before | and | any word |
| ዘ | before | relative "who, which"; "of" | any word |
| ለ | before | to, for | nominals |
| በ | before | in, by, with | nominals |
| እም | before | from | nominals |
| ሰ | after | as for (topic) | any word |
| ኒ, ሂ | after | also, even | any word |
| ኑ | after | question | any word |

Chains of two proclitics (ወለ, ወበ, ወእም, ወዘ, ዘበ, ዘእም) and a proclitic with an enclitic also occur.

Each row copies the root, word class and features of its source row (`base_id`) and keeps its split.
`evidence` names the clitics and the source row, so every root still comes from a book or gold record.
The fields `proclitic` and `enclitic` give the clitics (null when absent). Each source row has at most three
clitic forms; the choice is a fixed hash of the row id. A string that is already a form of the books is
not added.

Train only on rows with `split` = `train`. The spelling of the bare form is not changed; contractions
and sound changes at the join are not modelled.
