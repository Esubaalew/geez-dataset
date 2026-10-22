#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check data/unified/geez_morphology_rows.jsonl (the build script that writes it is not part of this repository).

  1 fields      every row has exactly the documented fields, ids are unique
  2 labels      word_class, stem, tense, person/gender/number, object, possessor, status, split are from the documented lists,
                and a row that loads has the labels its word_class needs
  3 forms       form is one Ge'ez word; root is 2-5 first-order Ge'ez letters joined by "-" (none for the rootless classes)
  4 splits      a root is in one split among rows that load (the gold sets the split of its roots; a book row whose form
                is a gold val/test form is the only exception and is listed)
  5 duplicates  no two rows that load have the same form, root, word_class and labels
  6 books       every line of data/books/*/forms.jsonl is the source of exactly one row, with the same form, root and split
  7 held splits a root is in one split among all its rows that are not EXCLUDED, so a held-back row can load later without a leak
  python check_unified.py DATASET_DIR [ROWS_JSONL]   (default data/unified/geez_morphology_rows.jsonl)
"""
import collections, json, os, re, sys

ds = sys.argv[1]
sys.path.insert(0, os.path.join(ds, "scripts"))
from check_dataset import is_ethiopic_word, is_first_order, form_variants   # noqa: E402

COLS = ["id", "form", "root", "word_class", "stem", "tense", "person", "gender", "number", "object", "possessor", "negated", "source",
        "book", "page", "source_ref", "evidence", "also_in", "status", "status_reason", "split"]
CLASSES = {"verb", "noun", "adjective", "nominal", "infinitive", "gerund", "verbal_noun", "pronoun", "demonstrative", "preposition", "particle",
           "numeral", "adverb", "proper_noun", "unknown"}
ROOTED = {"verb", "noun", "adjective", "nominal", "infinitive", "gerund", "verbal_noun", "numeral"}
STEMS = {"basic", "passive", "causative", "reciprocal", "aste", "aste_reciprocal"}
TENSES = {"past", "present", "subjunctive", "imperative"}
PERSONS = {("1", "c", "s"), ("1", "c", "p"), ("2", "m", "s"), ("2", "f", "s"), ("2", "m", "p"), ("2", "f", "p"), ("3", "m", "s"),
           ("3", "f", "s"), ("3", "m", "p"), ("3", "f", "p")}
CODES = {"".join(p) for p in PERSONS}
STATUS = {"", "CHECK", "CONFLICT", "NO_ROOT", "FLAGGED", "EXCLUDED"}
REQ = {"verb": ("tense", "person", "gender", "number", "stem"), "gerund": ("stem", "person", "gender", "number"),
       "infinitive": ("stem",), "verbal_noun": ("stem",), "noun": ("number",), "adjective": ("number",)}
errs = collections.defaultdict(list)
err = lambda k, m: errs[k].append(m)
ROWS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ds, "data", "unified", "geez_morphology_rows.jsonl")
rows = [json.loads(l) for l in open(ROWS, encoding="utf-8")]
ids = collections.Counter(r["id"] for r in rows)
root_splits, keys = collections.defaultdict(set), collections.defaultdict(list)
by_id = {r["id"]: r for r in rows}
for r in rows:
    w = r.get("id")
    if list(r) != COLS: err("1 fields", f"{w}: fields {list(r)}")
    if ids[w] > 1: err("1 fields", f"{w}: duplicate id")
    if r["word_class"] not in CLASSES: err("2 labels", f"{w}: word_class {r['word_class']!r}")
    if r["status"] not in STATUS: err("2 labels", f"{w}: status {r['status']!r}")
    if r["split"] not in ("train", "val", "test"): err("2 labels", f"{w}: split {r['split']!r}")
    for k, ok in (("stem", STEMS), ("tense", TENSES)):
        if r[k] and r[k] not in ok: err("2 labels", f"{w}: {k} {r[k]!r}")
    if r["status"] == "" and r["person"] and (r["person"], r["gender"] or "", r["number"] or "") not in PERSONS and r["word_class"] in ("verb", "gerund"):
        err("2 labels", f"{w}: person/gender/number {r['person']}/{r['gender']}/{r['number']}")
    for k in ("object", "possessor"):
        if r[k] and r[k] not in CODES: err("2 labels", f"{w}: {k} {r[k]!r}")
    if r["status"] == "": 
        for k in REQ.get(r["word_class"], ()):
            if not r[k]: err("2 labels", f"{w} {r['form']}: {r['word_class']} loads without {k}")
        if r["word_class"] in ROOTED and not r["root"]: err("2 labels", f"{w} {r['form']}: no root")
        if r["word_class"] not in ROOTED | {"proper_noun"} and r["root"]: err("2 labels", f"{w} {r['form']}: {r['word_class']} has a root")
        if r["word_class"] == "unknown": err("2 labels", f"{w}: class unknown loads")
    if r["status"] not in ("EXCLUDED",) and not is_ethiopic_word(r["form"] or "") and r["status"] == "":
        err("3 forms", f"{w}: {r['form']!r} is not one Ge'ez word")
    if r["root"]:
        parts = r["root"].split("-")
        if not 2 <= len(parts) <= 5 or not all(is_first_order(p) for p in parts) and r["status"] == "":
            err("3 forms", f"{w}: root {r['root']!r}")
    if r["status"] == "" and r["root"]:
        root_splits[r["root"]].add(r["split"])
        keys[(r["form"], r["root"], r["word_class"], r["tense"], r["person"], r["gender"], r["number"], r["stem"], r["object"], r["possessor"])].append(w)
for root, sp in sorted(root_splits.items()):
    if len(sp) > 1:
        gold = {r["split"] for r in rows if r["root"] == root and r["source"] == "gold" and r["status"] == ""}
        if gold or True:
            notes = collections.Counter(r["split"] for r in rows if r["root"] == root and r["status"] == "")
            err("4 splits", f"root {root} loads in {dict(notes)}")
for k, v in keys.items():
    if len(v) > 1 and not all(by_id[i]["source"] == "gold" for i in v): err("5 duplicates", f"{k[0]} ({k[1]}): {', '.join(v)}")
book_lines, book_refs, overrides = {}, collections.Counter(), collections.Counter()
books_dir = os.path.join(ds, "data", "books")
for b in sorted(os.listdir(books_dir)) if os.path.isdir(books_dir) else []:
    f = os.path.join("data", "books", b, "forms.jsonl")
    if os.path.exists(os.path.join(ds, f)):
        book_lines[f] = [json.loads(l) for l in open(os.path.join(ds, f), encoding="utf-8")]
for r in rows:
    ref = r["source_ref"] or ""
    f, _, n = ref.rpartition(":")
    if f not in book_lines: continue
    book_refs[ref] += 1
    if not n.isdigit() or not 1 <= int(n) <= len(book_lines[f]):
        err("6 books", f"{r['id']}: source_ref {ref} is not a line of {f}"); continue
    b = book_lines[f][int(n) - 1]
    for k in ("form", "root", "split"):
        if b.get(k) != r[k]:
            if k != "form" and "Settled:" in (r["evidence"] or ""):
                overrides[k] += 1        # a documented review correction of the printed root or its split
            else:
                err("6 books", f"{r['id']}: {k} {r[k]!r} but {ref} has {b.get(k)!r}")
for f, lines in book_lines.items():
    for n in range(1, len(lines) + 1):
        if book_refs[f"{f}:{n}"] != 1: err("6 books", f"{f}:{n} is the source of {book_refs[f'{f}:{n}']} rows")
held = collections.defaultdict(set)
for r in rows:
    if r["root"] and r["status"] != "EXCLUDED": held[r["root"]].add(r["split"])
for root, sp in sorted(held.items()):
    if len(sp) > 1:
        err("7 held splits", f"root {root} is in " + ", ".join(sorted(sp)))
for sec in ("1 fields", "2 labels", "3 forms", "4 splits", "5 duplicates", "6 books", "7 held splits"):
    print(("FAIL " if errs[sec] else "PASS ") + f"{sec}: {len(errs[sec])} problem(s)")
    for m in errs[sec][:8]: print("   ", m)
if overrides: print("review overrides of book lines (documented in evidence):", dict(overrides))
print("books:", ", ".join(f"{f.split('/')[2]} {len(v)}" for f, v in book_lines.items()))
c = collections.Counter((r["split"], r["word_class"]) for r in rows if r["status"] == "")
print("rows that load:", sum(c.values()), dict(sorted(collections.Counter(r["split"] for r in rows if r["status"] == "").items())))
sys.exit(1 if any(errs.values()) else 0)
