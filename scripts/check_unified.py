#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check data/unified/geez_morphology_rows.jsonl (the build script that writes it is not part of this repository).

  1 fields      every row has exactly the documented fields, ids are unique
  2 labels      word_class, stem, tense, person/gender/number, object, possessor, status, split are from the documented lists,
                and a row that loads has the labels its word_class needs; a rootless adjective loads only when
                data/unified/rootless_derived.tsv gives its rootless base (see derived_problem)
  3 forms       form is one Ge'ez word; root is 2-5 first-order Ge'ez letters joined by "-" (none for the rootless classes)
  4 splits      a root is in one split among rows that load (the gold sets the split of its roots; a book row whose form
                is a gold val/test form is the only exception and is listed)
  5 duplicates  no two rows that load have the same form, root, word_class and labels
                (all-gold groups, or a set of ids listed in data/unified/allowed_duplicates.tsv, are kept;
                a listed set that is no longer a loading duplicate fails)
  6 books       every line of data/books/*/forms.jsonl is the source of exactly one row, with the same form, root and split
  7 held splits a root is in one split among all its rows that are not EXCLUDED, so a held-back row can load later without a leak
  8 form splits the rows that load and share a spelling, joined through their roots (a spelling with two readings and
                every root it reads as), are in one split; a group listed in data/unified/held_split_groups.tsv is
                reported, not failed, and a listed group that is in one split fails (take it off the list)
  python check_unified.py DATASET_DIR [ROWS_JSONL]   (default data/unified/geez_morphology_rows.jsonl)
"""
import argparse, collections, json, os, re, sys

def _parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dataset_dir", help="repository root that contains data/ and scripts/")
    ap.add_argument("rows_jsonl", nargs="?", default=None,
                    help="unified rows file (default: DATASET_DIR/data/unified/geez_morphology_rows.jsonl)")
    return ap.parse_args(argv)

args = _parse_args()
ds = args.dataset_dir
sys.path.insert(0, os.path.join(ds, "scripts"))
from check_dataset import is_ethiopic_word, form_variants, root_problem   # noqa: E402

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
ROWS = args.rows_jsonl or os.path.join(ds, "data", "unified", "geez_morphology_rows.jsonl")
rows = [json.loads(l) for l in open(ROWS, encoding="utf-8")]
ids = collections.Counter(r["id"] for r in rows)
root_splits, keys = collections.defaultdict(set), collections.defaultdict(list)
by_id = {r["id"]: r for r in rows}
# nouns that have no root (data/unified/rootless_nouns.tsv) load with an empty root
ROOTLESS = set()
_p = os.path.join(ds, "data/unified/rootless_nouns.tsv")
if os.path.exists(_p):
    ROOTLESS = {l.split("\t")[0] for l in open(_p, encoding="utf-8").read().splitlines()[1:] if l.strip()}
for _f in sorted(ROOTLESS - {r["form"] for r in rows if r["word_class"] == "noun"}):
    err("2 labels", f"rootless_nouns.tsv: {_f} is not a noun row")
# adjectives with no root that are derived from a rootless word (data/unified/rootless_derived.tsv: form, base, ref):
# one loads only if it ends in -ዊ, -ዊት or -ውያን and its base loads, with no root, as a listed noun or a name, in the same split
DERIVED_ENDINGS = ("ዊ", "ዊት", "ውያን")
DERIVED = {}
_p = os.path.join(ds, "data/unified/rootless_derived.tsv")
if os.path.exists(_p):
    for l in open(_p, encoding="utf-8").read().splitlines()[1:]:
        if l.strip():
            _c = l.split("\t")
            DERIVED[_c[0]] = _c[1] if len(_c) > 1 else ""
base_splits = collections.defaultdict(set)
for r in rows:
    if r["status"] == "" and not r["root"] and (r["word_class"] == "proper_noun" or (r["word_class"] == "noun" and r["form"] in ROOTLESS)):
        base_splits[r["form"]].add(r["split"])
def derived_problem(r):
    """Why a rootless adjective may not load, or None."""
    if r["form"] not in DERIVED: return "not in rootless_derived.tsv"
    if not r["form"].endswith(DERIVED_ENDINGS): return "does not end in -ዊ, -ዊት or -ውያን"
    b = DERIVED[r["form"]]
    if not base_splits.get(b): return f"its base {b!r} does not load as a rootless noun or name"
    if base_splits[b] != {r["split"]}: return f"its base {b} loads in {', '.join(sorted(base_splits[b]))}, not {r['split']}"
    return None
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
        if r["word_class"] == "adjective" and not r["root"]:
            if derived_problem(r): err("2 labels", f"{w} {r['form']}: no root ({derived_problem(r)})")
        elif r["word_class"] in ROOTED and not r["root"] and not (r["word_class"] == "noun" and r["form"] in ROOTLESS): err("2 labels", f"{w} {r['form']}: no root")
        if r["word_class"] not in ROOTED | {"proper_noun"} and r["root"]: err("2 labels", f"{w} {r['form']}: {r['word_class']} has a root")
        if r["word_class"] == "unknown": err("2 labels", f"{w}: class unknown loads")
    if r["status"] not in ("EXCLUDED",) and not is_ethiopic_word(r["form"] or "") and r["status"] == "":
        err("3 forms", f"{w}: {r['form']!r} is not one Ge'ez word")
    if r["root"] and r["status"] == "" and root_problem(r["root"]):
        err("3 forms", f"{w}: root {r['root']!r}")
    if r["status"] == "" and r["root"]:
        root_splits[r["root"]].add(r["split"])
        keys[(r["form"], r["root"], r["word_class"], r["tense"], r["person"], r["gender"], r["number"], r["stem"], r["object"], r["possessor"])].append(w)
# gold val/test spellings may pull a book row into another split than its root; list those, do not fail
gold_val_test_forms = {r["form"] for r in rows if r["source"] == "gold" and r["status"] == "" and r["split"] in ("val", "test")}
for root, sp in sorted(root_splits.items()):
    if len(sp) > 1:
        gold = {r["split"] for r in rows if r["root"] == root and r["source"] == "gold" and r["status"] == ""}
        loading = [r for r in rows if r["root"] == root and r["status"] == ""]
        notes = collections.Counter(r["split"] for r in loading)
        extras = [r for r in loading if r["split"] not in gold] if gold else loading
        listed = gold and len(gold) == 1 and extras and all(
            r["source"] != "gold" and r["form"] in gold_val_test_forms for r in extras)
        if listed:
            print(f"gold split exception (listed): root {root} loads in {dict(notes)}")
        else:
            err("4 splits", f"root {root} loads in {dict(notes)}")
# intentional multi-reading twins (same form+root+labels, different evidence), like gold አመንዘረ
allowed_dup_path = os.path.join(ds, "data", "unified", "allowed_duplicates.tsv")
allowed_dup_sets = {}  # frozenset(ids) -> reason
if os.path.exists(allowed_dup_path):
    with open(allowed_dup_path, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            if not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 4:
                err("5 duplicates", f"allowed_duplicates.tsv: bad line {line!r}"); continue
            idset = frozenset(i for i in cols[0].split(";") if i)
            if len(idset) < 2:
                err("5 duplicates", f"allowed_duplicates.tsv: need two or more ids, got {cols[0]!r}"); continue
            allowed_dup_sets[idset] = cols[3]
seen_allowed = set()
for k, v in keys.items():
    if len(v) <= 1:
        continue
    idset = frozenset(v)
    if all(by_id[i]["source"] == "gold" for i in v):
        continue
    if idset in allowed_dup_sets:
        seen_allowed.add(idset)
        print(f"allowed duplicate (listed): {k[0]} ({k[1]}): {', '.join(v)}")
        continue
    err("5 duplicates", f"{k[0]} ({k[1]}): {', '.join(v)}")
for idset, reason in allowed_dup_sets.items():
    if idset not in seen_allowed:
        err("5 duplicates", f"allowed_duplicates.tsv: {', '.join(sorted(idset))} is not a loading duplicate")
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
# 8 form splits: union of spellings and roots over the rows that load
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
loading = [r for r in rows if r["status"] == ""]
for r in loading:
    a = find("f:" + r["form"])
    if r["root"]:
        parent[a] = find("r:" + r["root"])
group_splits, group_forms = collections.defaultdict(set), collections.defaultdict(set)
for r in loading:
    g = find("f:" + r["form"])
    group_splits[g].add(r["split"]); group_forms[g].add(r["form"])
held_path = os.path.join(ds, "data", "unified", "held_split_groups.tsv")
held_groups = {}
if os.path.exists(held_path):
    with open(held_path, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            if line.strip():
                form = line.split("\t")[0]
                held_groups[form] = find("f:" + form)
listed = set(held_groups.values())
for g, sp in group_splits.items():
    if len(sp) > 1 and g not in listed:
        err("8 form splits", f"{', '.join(sorted(group_forms[g])[:4])}: the spelling and its roots load in {', '.join(sorted(sp))}")
for form, g in held_groups.items():
    if len(group_splits.get(g, ())) <= 1:
        err("8 form splits", f"{form} is listed in held_split_groups.tsv but loads in one split")
    else:
        print(f"held split group (listed): {form} loads in {', '.join(sorted(group_splits[g]))}")
for sec in ("1 fields", "2 labels", "3 forms", "4 splits", "5 duplicates", "6 books", "7 held splits", "8 form splits"):
    print(("FAIL " if errs[sec] else "PASS ") + f"{sec}: {len(errs[sec])} problem(s)")
    for m in errs[sec][:8]: print("   ", m)
if overrides: print("review overrides of book lines (documented in evidence):", dict(overrides))
print("books:", ", ".join(f"{f.split('/')[2]} {len(v)}" for f, v in book_lines.items()))
c = collections.Counter((r["split"], r["word_class"]) for r in rows if r["status"] == "")
print("rows that load:", sum(c.values()), dict(sorted(collections.Counter(r["split"] for r in rows if r["status"] == "").items())))
sys.exit(1 if any(errs.values()) else 0)
