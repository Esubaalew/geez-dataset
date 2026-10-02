# Dataset Development Roadmap

This document outlines key technical milestones and planned extensions for the Classical Ge'ez NLP and lexicographical dataset.

---

## 1. Lexical Verification & Expansion

- [x] **Consolidation of Multi-Column Continuations:** Merge 656 fragmented dictionary entries into parent lemmas.
- [x] **Empty Definition Resolution:** Cross-reference and provide structured morphological glosses for all clustered derivations.
- [x] **Errata Table Integration:** Transcribe and apply 100% of the 12 errata records from Page 909.
- [x] **Missing Scan Retrieval:** Download original high-resolution scan for dictionary Page 618 (`n_gzMezgebeQalat_61802.gif`).
- [ ] **Page 618 Integration:** Verify and append the remaining lexical records under letter `ነ` into `dictionary.jsonl`.
- [ ] **Cross-Validation with Dillmann's Lexicon:** Cross-reference Kidane Wold Kifle's lemmas against August Dillmann's *Lexicon Linguae Aethiopicae* (1865) for comparative Semitic root validation.

---

## 2. Morphological Modeling & Analysis

- [x] **Triliteral & Quadriliteral Root Inference:** Compute consonantal skeletons across 13,234 dictionary headwords.
- [x] **Rule-Based Conjugation Matrix Generation:** Generate ~145,000 synthetic inflectional pairs from 2,267 verified verbal roots.
- [ ] **Weak Verb Allomorphy Modeling:** Formalize phonological contraction rules for initial, medial, and final glides ($w, y$) and gutturals ($h, ḥ, ḫ, ', ‘$).
- [ ] **Broken Plural Template Catalog:** Expand the catalog of 13 major nominal broken plural templates (`noun_patterns.json`) to cover irregular construct-state declensions.

---

## 3. Downstream NLP & Machine Translation

- [x] **Parallel Corpus Extraction:** Index 13,234 Ge'ez-Amharic definition and gloss pairs in `parallel_pairs.jsonl`.
- [ ] **Standard Train/Val/Test Splits:** Partition the parallel corpus by root family and page ranges to prevent data leakage in sequence-to-sequence evaluation.
- [ ] **Named Entity Recognition (NER) Annotations:** Tag Biblical, liturgical, and historical geographic names in dictionary citations.
- [ ] **Hugging Face Datasets Integration:** Package and publish the corpus on the Hugging Face Hub under a structured Python dataset loader.
