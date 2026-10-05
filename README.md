# Classical Ge'ez Lexical, Morphological, and Parallel Corpus

A comprehensive computational linguistic dataset for Classical Ge'ez natural language processing, root-and-pattern morphological analysis, and Ge'ez-to-Amharic machine translation.

---

## 1. Canonical Dataset Architecture (`data/`)

All curated, deduplicated, and production datasets are structured under `data/`:

### A. Morphological Paradigms (`data/paradigms/` — ርባሕ ወአንቀጽ)
* **`synthetic_morphology_train.jsonl`** (**98,128 records** | 17.2 MB): Cleaned bidirectional synthetic training pairs. Features full verb-type compatibility (0.00% cross-type corruption) and classical glide contractions (e.g., $q-w-m \to$ ቆመ, $m-w-t \to$ ሞተ, $s-y-m \to$ ሤመ).
* **`synthetic_morphology_analyze.jsonl`** (**98,128 records** | 17.2 MB): Inverse analysis target mapping inflected surface words back to roots and grammatical features.
* **`merho_ges_gold_train.jsonl`** (**3,194 authentic forms** across 1,169 roots): Authentic church conjugation matrices across past, present, subjunctive, and imperative moods.
* **`merho_ges_gold_val.jsonl`** (**394 forms**): Held-out validation split for in-training zero-shot evaluation on unseen roots.
* **`merho_ges_gold_test.jsonl`** (**586 forms**): Strict, uncompromised evaluation benchmark with **0.00% surface form leakage** against train/val.
* **`merho_ges_gold_all.jsonl`** (**4,041 table rows** | 2.0 MB): Master reference of all 1,375 extracted root tables from *Merho Ges*.

### B. Lexicon & Dictionaries (`data/lexicon/` — መዝገበ ቃላት)
* **`classical_dictionary_kidane_wold.jsonl`** (**13,234 entries** | 10.0 MB): Master classical dictionary from Aleqa Kidane Wold Kifle. Contains inferred roots with the corrected initial-`አ` disambiguation rule (278 previously corrupted roots restored to valid triliterals).
* **`modern_geez_amharic_dictionary.jsonl`** (**1,722 entries** | 390 KB): Clean 1-to-1 vocabulary dictionary from the 102-page *Rbahe Asma'e We-Anqets*, featuring 881 verbs and 826 nouns with modern Amharic glosses.

### C. Bilingual Parallel Data (`data/parallel/`)
* **`true_parallel_pairs.jsonl`** (**2,780 pairs**): High-precision Ge'ez-to-Amharic parallel sentences filtered with a 5-feature linguistic discriminator (eliminating the legacy 33% preposition mislabel defect).
* **`uncertain_pairs.jsonl`** (**9,066 entries**): Short 1–2 word glosses, isolated noun definitions, and entries lacking complex verbal syntax.

### D. Monolingual & Explanatory Corpora (`data/corpora/` — ድርሰት / ንባብ)
* **`yared_shiferaw_corpus.txt`** (**90,699 words** | 610 KB): Full continuous grammatical and morphological text from Liqe Liqawunt Yared Shiferaw (422 pages).
* **`merho_ges_prose_rules.txt`** (**717 records** | 703 KB): Extracted historical and grammatical prose commentaries from *Merho Ges*.
* **`geez_geez_monolingual.jsonl`** (**1,388 passages**): Ge'ez definitional texts salvaged from mislabeled dictionary segments.
* **`phrasebook_pairs.jsonl`** (**218 phrases**): Contextual parallel idioms from the final pages of *Rbahe Asma'e We-Anqets*.

---

## 2. Provenance & Source Authorities

This repository is grounded in primary philological volumes from the Ethiopian scholarly tradition:
1. **Aleqa Kidane Wold Kifle (1872–1944)**: *Mets'hafe Sewasew Weges Wemezgebe Qalat Haddis* («መጽሐፈ ሰዋስው ወግስ ወመዝገበ ቃላት ሐዲስ») — Comprehensive Ge'ez-Amharic dictionary (1948 E.C., 716 print pages, 13,234 entries).
2. **Traditional School Tradition / Kidane Wold Kifle**: *Rbahe Asma'e We-Anqets* («ርባሐ አስማእ ወአንቀጽ») — 102-page manual of nominal declensions, verbal classes, and parallel phrase pairs.
3. **Liqe Liqawunt Yared Shiferaw (ሊቀ ሊቃውንት ያሬድ ሽፈራው)**: *Mets'hafe Ges Wesewasew* («መጽሐፈ ግስ ወሰዋስው») — 422-page modern traditional treatise on verbal classification and weak verbs (*ሆህያተ ድካም*).
4. **Traditional Church Curriculum**: *Merho Ges Wesewasew Ze-Yared* («መርኆ ግስ ወሰዋስው ዘያሬድ») — Complete 509-page manual of verbal conjugation matrices across all 10 grammatical persons and gates (*ርባሕ ወአንቀጽ*).

---

## 3. Data Quality & Auditing History

* **Weak Verb Phonological Contraction:** Generator applies classical Semitic glide contractions ($aw \to o, ay \to e, əw \to u$) so hollow roots generate authentic forms (`ቆመ`, `ሞተ`, `ሤመ`, `ይቁም`).
* **Root-Type Compatibility:** The synthetic generator loop checks root-pattern compatibility (`if ptype != rtype: continue`), preventing cross-class corruption.
* **Root-Initial `አ` Disambiguation:** 278 previously truncated roots were restored to valid triliterals (`አበኃ` $\to$ `a-b-kh`, `አበወ` $\to$ `a-b-w`) by verifying consonant counts and 2nd-radical vowel orders.
* **Zero Leakage Split:** All *Merho Ges* test records are partitioned by canonical 1st-order Ethiopic root, ensuring 0.00% surface form leakage between train and test.

---

## 4. Usage in Python

```python
import json

# Load canonical dictionary
with open("data/lexicon/classical_dictionary_kidane_wold.jsonl", "r", encoding="utf-8") as f:
    dictionary = [json.loads(line) for line in f]

print(f"Loaded {len(dictionary)} dictionary entries.")

# Load held-out gold test paradigms
with open("data/paradigms/merho_ges_gold_test.jsonl", "r", encoding="utf-8") as f:
    test_paradigms = [json.loads(line) for line in f]

print(f"Loaded {len(test_paradigms)} held-out gold paradigm records.")
```

---

## License

This dataset is released under the **Apache License 2.0**.
