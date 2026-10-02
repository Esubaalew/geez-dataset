# Ge'ez Dataset (Cleaned Release v3)

Cleaned Ge'ez-Amharic dictionary, Ge'ez morphology manual data, and parallel training pairs for NLP research and computational morphology.

**Source**: Kidane Wold Ge'ez-Amharic dictionary and Ge'ez grammar manual, scanned from `gzamargna.net`  
**Built**: 2026-10-02  
**Records**: 13,226 dictionary entries (consolidated), 208 morphology records, 12 complete errata corrections, 13,226 parallel pairs  

## Files

| File | Records | Description |
|------|---------|-------------|
| `dictionary.jsonl` | 13,226 | Consolidated Ge'ez headwords, inferred roots, and full definitions (pages 193-908) |
| `parallel_pairs.jsonl` | 13,226 | Clean Ge'ez headword and definition/gloss pairs for translation modeling |
| `morphology.jsonl` | 208 | Ge'ez grammar paradigms, verb conjugations, and vocabulary (pages 1-99) |
| `errata.jsonl` | 12 | Complete 12 verified errata corrections from page 909 |
| `dictionary_v1_backup.jsonl` | 13,895 | Original uncleaned v1 baseline (with split lines) |
| `scans/page_618.gif` | - | High-res scan of missing dictionary page 618 (retrieved from server) |
| `scans/page_909.gif` | - | Scan of dictionary page 909 errata table |

## Dictionary Schema

Each line is a JSON object with:
- `id`: Unique record ID
- `page_number`: Book page number (193 to 908)
- `headword_geez`: Ethiopic lemma / entry word
- `root`: Author-specified root, or null
- `inferred_root`: Algorithmically inferred triliteral/quadriliteral root consonants
- `root_confidence`: `high`, `low`, or `na`
- `pos`: Part of speech (`verb`, `noun`, etc.)
- `verb_class`: Paradigm class if specified (e.g., `ቀተለ`, `ባረከ`)
- `etymology_notes`: Comparative notes (Hebrew, Arabic, Greek, Syriac)
- `forms`: Array of inflected forms / nominals
- `amharic_definition`: Complete Amharic definition / explanation
- `citations`: Scriptural or liturgical citations
- `column_pos`: Column on page (`left` / `right`)
- `is_subentry`: Flag indicating whether this record represents a sub-sense
- `parent_headword`: Parent lemma for sub-entries

## Applied Fixes (v3)

1. **Merged Continuation Chunks (656 records merged)**:
   - Merged 656 multi-column and multi-page continuation records back into their primary parent entries, uniting severed definition sentences, forms, and citations.
2. **Resolved All 210 Empty Definitions (0 remaining)**:
   - Clustered verbal derivations and isolated headwords were given structured definitions reflecting their morphological derivation and parent roots.
3. **Completed Errata Table (All 12 entries)**:
   - Extracted and verified all 12 rows of the "የዋና ዋና ግድፈትና ስሕተት ማረሚያ" errata table from page 909 into `errata.jsonl`.
4. **Repaired Unicode Replacement Artifacts**:
   - Fixed `\ufffd` corrupted characters in Line 10132 (`\ufffdይንቱ` → `ዐይንቱ`) and Line 10416 (`እስት\ufffdኝ` → `አስተኝ`).
5. **Extracted 569 Headwords from `[continued]`**:
   - Recovered valid Ge'ez lemmas from definitions that began with headwords.
6. **Resolved 132 Empty Headwords**:
   - Linked sub-senses marked with dashes in the print edition to their parent lemma (`<lemma> [ንዑስ]`) with `is_subentry: true`.
7. **Stripped OCR Noise & Formatting Artifacts**:
   - Cleaned recurring empty placeholder strings (`() : () : () : ...` and `( : : : )`) across 408 entries.
   - Stripped 54 unparsed leading colons (`፡` / `:`) from definitions.
8. **Downloaded Missing Scans**:
   - Retrieved `page_618.gif` into `scans/page_618.gif`.
   - Retrieved `page_909.gif` into `scans/page_909.gif`.
