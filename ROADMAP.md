# Dataset Development Roadmap

This document outlines key technical milestones and planned extensions for the Classical Ge'ez NLP and lexicographical dataset.

---

## 1. Lexical Verification & Expansion

- [x] **Consolidation of Multi-Column Continuations:** Merge 656 fragmented dictionary entries into parent lemmas.
- [x] **Empty Definition Resolution:** Cross-reference and provide structured morphological glosses for all clustered derivations.
- [x] **Errata Table Integration:** Transcribe and apply 100% of the 12 errata records from Page 909.
- [x] **Missing Scan Retrieval:** Download original high-resolution scan for dictionary Page 618 (`n_gzMezgebeQalat_61802.gif`).
- [x] **Initial-አ Root Disambiguation:** Implement 3-consonant vs. 4-consonant causative prefix rules to restore 278 previously truncated roots.
- [ ] **Cross-Validation with Dillmann's Lexicon:** Cross-reference Kidane Wold Kifle's lemmas against August Dillmann's *Lexicon Linguae Aethiopicae* (1865) for comparative Semitic root validation.

---

## 2. Morphological Modeling & Analysis

- [x] **Triliteral & Quadriliteral Root Inference:** Compute consonantal skeletons across 13,234 dictionary headwords.
- [x] **Clean Synthetic Inflectional Expansion:** Generate 98,128 clean synthetic pairs from 1,670 verified verbal roots with strict class-compatibility filters (0% corruption).
- [x] **Weak Verb Allomorphy Modeling:** Implement classical phonological contraction rules ($aw \to o, ay \to e, əw \to u$) in `engine.py` for hollow and weak roots (`ቆመ`, `ሞተ`, `ሤመ`, `ይቁም`).
- [x] **Yared Shiferaw Treatise Ingestion:** Extract 422 pages and 90,699 words of Liqe Liqawunt Yared Shiferaw's *Mets'hafe Ges Wesewasew* for deep verbal classification.
- [x] **Traditional Paradigm Manual Archival & Extraction:** Digitized all 509 pages of *Merho Ges Wesewasew Ze-Yared* into 4,041 authentic paradigm forms.
- [x] **Zero-Leakage Benchmark Creation:** Establish canonical 15% held-out test split (`merho_ges_gold_test.jsonl`) and 10% validation split (`merho_ges_gold_val.jsonl`) with 0.00% surface form overlap.
- [ ] **Broken Plural Template Catalog:** Expand the catalog of 13 major nominal broken plural templates (`noun_patterns.json`) to cover irregular construct-state declensions.

---

## 3. Downstream NLP & Machine Translation

- [x] **High-Precision Language ID Classification:** Apply 5-feature morphological discriminator to classify dictionary pairs into 2,780 true parallel sentences and 1,388 Ge'ez monolingual passages.
- [x] **Phrasebook Extraction:** Ingest 218 contextual parallel phrase pairs from *Rbahe Asma'e We-Anqets*.
- [ ] **Biblical Parallel Corpus (Genesis):** Align chapter/verse parallel texts (`genesis_geez.txt` and `genesis_amharic.txt`) for long-context translation benchmarks.
- [ ] **Hugging Face Datasets Integration:** Package and publish the curated `data/` repository on the Hugging Face Hub under a structured Python dataset loader.
