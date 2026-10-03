# Classical Ge'ez Lexical, Morphological, and Parallel Corpus

A curated computational dataset for Classical Ge'ez natural language processing, root-and-pattern morphological analysis, and Ge'ez-to-Amharic machine translation.

---

## Provenance & Sources

This dataset is compiled and curated from primary philological and lexicographical authorities of the Ethiopian traditional school:
1. **Aleqa Kidane Wold Kifle (1872–1944)**: *Mets'hafe Sewasew Weges Wemezgebe Qalat Haddis* («መጽሐፈ ሰዋስው ወግስ ወመዝገበ ቃላት ሐዲስ») — Comprehensive Ge'ez-Amharic dictionary and grammatical treatise (published 1948 E.C. / 1955 A.D., Artistic Printing Press, Addis Ababa).
2. **Kesis Desta Tekle Wold (1901–1986)**: *Rbahe Asma'e We-Anqets* («ርባሐ አስማእ ወአንቀጽ / ርእሰ ስም ወአንቀጽ») — Authoritative Ge'ez manual of noun declensions, broken plurals, and full verbal conjugation matrices across all 10 grammatical persons (1946 E.C.).
3. **Liqe Liqawunt Yared Shiferaw (ሊቀ ሊቃውንት ያሬድ ሽፈራው)**: *Mets'hafe Ges Wesewasew* («መጽሐፈ ግስ ወሰዋስው») — Authoritative 422-page modern traditional treatise on Ge'ez verbal classification, weak verbs (*ሆህያተ ድካም*), and complex stem derivations.
4. **Classical Yaredic Tradition**: *Merho Ges Wesewasew Ze-Yared* («መርኆ ግስ ወሰዋስው ዘያሬድ») — Comprehensive traditional manual of verbal inflection across all 10 grammatical persons and irregular classes (511 pages).

---

## Dataset Overview

| File | Records | Size | Description |
| :--- | :--- | :--- | :--- |
| **`dictionary.jsonl`** | **13,234** | ~9.4 MB | Consolidated Ge'ez lemmas with inferred roots, POS, definitions, and citations. |
| **`parallel_pairs.jsonl`** | **13,234** | ~5.2 MB | Aligned Ge'ez headword and definition/gloss pairs for translation modeling. |
| **`output/yared_shiferaw_pages.jsonl`** | **422** | ~1.5 MB | Extracted page-by-page structured grammatical text from Liqe Liqawunt Yared Shiferaw. |
| **`output/yared_shiferaw_corpus.txt`** | **90,699 words** | ~1.2 MB | Clean compiled textual corpus for language model pretraining and tokenizer vocabularies. |
| **`scans/merho_ges_511/`** | **509** | ~41 MB | Complete page scans of the traditional verbal paradigm manual (*Merho Ges*). |
| **`morphology.jsonl`** | **208** | ~392 KB | Grammatical paradigms, pronoun tables, noun declensions, and conjugation matrices. |
| **`errata.jsonl`** | **12** | ~2.1 KB | Reconciled orthographic and philological errata table from Page 909. |
| **`output/synthetic_morphology_train.jsonl`** | **196,936** | ~36.2 MB | Bidirectional synthetic morphological training targets ($\text{features} \to \text{surface}$). |
| **`output/extended_paradigms.jsonl`** | **3,968** | ~15.9 MB | Exhaustive verbal paradigm tables generated across all 64 template combinations. |
| **`output/noun_patterns.json`** | **13** | ~13.8 KB | Extracted Ge'ez nominal and broken plural templates. |
| **`output/quality_scores.jsonl`** | **13,234** | ~645 KB | Algorithmic quality confidence ratings (0.0 to 1.0) and anomaly detection flags. |
| **`sources/`** | **6 volumes** | ~486 MB | Local archive library of reference PDFs and source facsimiles (see `sources/README.md`). |

---

## Schema Specifications

### 1. Dictionary Schema (`dictionary.jsonl`)
Each line represents an independent JSON object:

```typescript
interface DictionaryEntry {
  id: number;                     // Unique record identifier
  page_number: number;            // Page in Kidane Wold Kifle print edition (193 to 908)
  headword_geez: string;          // Ge'ez lemma in Ethiopic script (e.g., "ቀተለ")
  root: string | null;            // Triliteral/quadriliteral root as noted by author
  inferred_root: string | null;   // Algorithmic consonantal skeleton (e.g., "q-t-l")
  root_confidence: "high" | "low" | "na"; // Confidence in root isolation
  pos: string;                    // Part of speech (verb, noun, adjective, particle, name)
  verb_class: string | null;      // Morphological paradigm class (e.g., "ቀተለ", "ባረከ")
  etymology_notes: string | null; // Comparative Semitic notes (Hebrew, Arabic, Syriac, Greek)
  forms: string[];                // Derived nominals, inflections, or alternate spellings
  amharic_definition: string;     // Complete definition and Amharic explanation
  citations: string[];            // Biblical, patristic, or liturgical citations
  column_pos: "left" | "right";   // Column position on scanned page
  is_subentry?: boolean;          // True if derived sub-sense linked to a parent lemma
  parent_headword?: string;       // Parent lemma for sub-entries
}
```

### 2. Morphology Schema (`morphology.jsonl`)
```typescript
interface MorphologyRecord {
  id: number;                     // Unique record identifier
  page_number: number;            // Page in Desta Tekle Wold print edition (1 to 99)
  category: string;               // verb_conjugation, noun_declension, pronoun_table, etc.
  title_or_lemma: string;         // Title of paradigm (e.g., "ርባሐ ቀተለ", "ስም አእላፍ")
  root: string | null;            // Underlying root if applicable
  paradigm_class: string | null;  // Paradigm class (ቀተለ, ባረከ, etc.)
  table_data: object | null;      // Structured JSON representation of paradigm table
  amharic_notes: string;          // Philological rules and explanatory notes
  raw_transcription: string;      // Verbatim transcription of table text
}
```

---

## Data Hygiene & Curation

The dataset was curated through a multi-pass reconciliation pipeline:
* **Continuation Merging:** 656 multi-column fragment records (`[ቀጣይ]`) were collapsed into their primary parent entries, reuniting severed definition sentences, forms, and citations.
* **Complete Definition Coverage:** 100% of dictionary entries have populated definitions (0 empty records).
* **Glyph Normalization:** All Unicode replacement artifacts (`\ufffd`) were identified and restored to valid Ethiopic characters (`ዐይንቱ`, `አስተኝ`).
* **OCR Artifact Pruning:** Cleaned repetitive empty placeholder brackets (`() : () : ...` and `( : : : )`) across 408 definitions.
* **Errata Reconciliation:** 100% of the 12 errata records from page 909 were transcribed and indexed.

---

## Usage in Python

```python
import json

# Load dictionary entries
dictionary = []
with open("dictionary.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        dictionary.append(json.loads(line))

print(f"Loaded {len(dictionary)} dictionary entries.")

# Filter verbs with high-confidence roots
verbs = [e for e in dictionary if e["pos"] == "verb" and e["root_confidence"] == "high"]
print(f"High-confidence verb entries: {len(verbs)}")

# Sample entry lookup
sample = next(e for e in dictionary if e["headword_geez"] == "ቀተለ")
print(json.dumps(sample, ensure_ascii=False, indent=2))
```

---

## License & Attribution

This dataset is released under the **Apache License 2.0**.  
When using this dataset for research or model training, please cite the underlying lexicographical works of Aleqa Kidane Wold Kifle and Kesis Desta Tekle Wold.

---

## Philological Glossary & Scribal Conventions

To facilitate machine learning, natural language processing, and human research, the dataset adheres to and documents the traditional scribal abbreviations and lexicographical conventions established by Aleqa Kidane Wold Kifle:

### 1. Biblical & Liturgical Citation Abbreviations (የመጻሕፍት ምህፃረ ቃላት)
* **`መኅ` / `መኃ`:** *መሓልየ መሓልይ* (Song of Songs / Canticles).
* **`መዝ`:** *መዝሙረ ዳዊት* (Psalms of David).
* **`ኦሪ` / `ኦ`:** *ኦሪት* (Pentateuch / Torah; e.g., `ኦ.ዘፍ` = Genesis, `ኦ.ዘጸ` = Exodus).
* **`ኢሳ`:** *ትንቢተ ኢሳይያስ* (Book of Isaiah).
* **`ወን` / `ወ`:** *ወንጌል* (Gospel; e.g., `ወ.ማቴ` = Matthew, `ወ.ዮሐ` = John).
* **`ስንክ`:** *መጽሐፈ ስንክሳር* (Synaxarium).
* **`ሃይ.አበ`:** *ሃይማኖተ አበው* (Faith of the Fathers).
* **`ቀለ`:** *ቀሌምንጦስ* (Pseudo-Clementine literature / Qalementos).
* **`ዜና.አይ`:** *ዜና አይሁድ* (Josippon / History of the Jews).

### 2. Comparative Semitic Cognate Markers (የቋንቋዎች ንጽጽር)
* **`ዕብ`:** *በዕብራይስጥ* (Biblical Hebrew cognate / etymological comparison).
* **`ዐረ`:** *በዐረብኛ* (Classical Arabic cognate).
* **`ሱር`:** *በሶርያ / በሱርስት* (Classical Syriac / Aramaic cognate).
* **`ጽር`:** *በጽርዕ / በግሪክ* (Greek loanword or parallel term).
* **`ላቲ`:** *በላቲን* (Latin parallel).
* **`ቁብ`:** *በቁብጥ* (Coptic parallel).

### 3. Structural & Grammatical Terminology (የሰዋስውና የመዝገበ ቃላት ቃላት)
* **`—` (ጭረት / መስመር):** Ditto mark denoting continuation of the preceding headword/root family.
* **`ንዑስ` / `[ንዑስ]`:** Sub-entry representing an inflected stem, verbal noun, or derived idiom belonging to the governing root.
* **`እይ` / `ተመልከት` / `ዕርኢ`:** Cross-reference marker directing the reader to consult another headword or primary root.
* **`አስደራጊ` / `ተደራጊ` / `አድራጊ`:** Morphological stem indicators (Causative, Passive/Reflexive, and Active Participle respectively).

### 4. Punctuation Delimiters (ሥርዓተ ነጥቦች)
* **`፡` (`U+1361`):** *ሁለት ነጥብ* (Ethiopic word divider).
* **`።` (`U+1362`):** *አራት ነጥብ* (Ethiopic full stop / sentence boundary).
* **`፤` (`U+1364`):** *ድርብ ሠረዝ* (Ethiopic semicolon / major clausal pause).
* **`፥` (`U+1363`):** *ነጠላ ሠረዝ* (Ethiopic comma / list delimiter).
