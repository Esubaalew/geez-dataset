#!/usr/bin/env python3
"""Check that the Merho Ges gold files are clean.

Run from the repository root:

    python scripts/check_dataset.py            # checks data/paradigms/
    python scripts/check_dataset.py --list     # also prints every problem, not only the first 20

It needs only Python 3.8+ (no packages). It exits with 0 when the files pass and 1 when they don't.

What "clean" means here (one line per check; ERROR fails the run, NOTE is information):

  1. every line of the three gold files is a JSON record with the documented fields;
  2. every form that loads is one Ge'ez word (Ethiopic letters only);
  3. every root written in the files (record or row) is 2 to 5 letters, each in the 1st order of its series (ቀ-ተ-ለ, not ቅ-ት-ል);
  4. no Latin letters in any form or root, loaded or not;
  5. every label is from the documented list below (type, tense, person/gender/number, stem, object);
  6. nouns and adjectives carry no verb labels (tense, person, object);
  7. no pair (form + all labels) appears twice, in one split or across splits;
  8. no root appears in more than one split (train / val / test);
  9. every row in merho_ges_gold_flagged_rows.tsv points at a real row holding that form;
 10. if data/paradigms/SHA256SUMS exists, every file matches its hash;
 11. no root field holds the placeholder "CHECK" (case-sensitive): the gold files and, next to the gold folder,
     the dictionaries, the Kidane Wold tables, verbs_rbha_anqets.jsonl and the synthetic files. A root field is a
     key named "root" or ending in "_root" (inferred_root, new_root, old_root, ...), at any depth. An unsettled
     root is null, with the reason in root_notes. Other placeholder-like values (an empty string, "TODO", "None",
     "?", "check" in another case, ...) are reported as NOTE lines and do not fail the run.

Check 7 skips a duplicate listed in merho_ges_gold_allowed_duplicates.tsv: same record (file_line + rows "0;1"),
or across records of one split (file_line empty, rows "193:1;195:0")
and reports a listed pair that is no longer a duplicate.

A "pair" is one form of one row with the labels the row gives it. A row's own root, stem, type and
object override the record's. Rows listed in the flagged-rows file, rows with an empty root and
records marked root_unsettled are kept in the files but do not load; the check counts them.
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import re
import sys

# ---- the documented label set (keep in step with docs/SCHEMA.md) ---------------------------------
TYPES = ("verb", "noun", "adjective")
TENSES = ("past", "present", "subjunctive", "imperative")  # jussive is written as subjunctive
STEMS = ("basic", "passive", "causative", "reciprocal", "aste")
GENDERS_ADJ = ("m", "f", "c", "")
NUMBERS = ("s", "p")
VERB_PERSONS = {("1", "c", "s"), ("1", "c", "p"), ("2", "m", "s"), ("2", "f", "s"), ("2", "m", "p"),
                ("2", "f", "p"), ("3", "m", "s"), ("3", "f", "s"), ("3", "m", "p"), ("3", "f", "p")}
OBJECTS = {"".join(p) for p in VERB_PERSONS}

GOLD = {"train": "merho_ges_gold_train.jsonl",
        "val": "merho_ges_gold_val.jsonl",
        "test": "merho_ges_gold_test.jsonl"}
FLAGGED = "merho_ges_gold_flagged_rows.tsv"
ALLOWED = "merho_ges_gold_allowed_duplicates.tsv"   # exact duplicates kept on purpose (same form printed twice)
RECORD_FIELDS = ("record_id", "category", "root", "table_data", "page_number")
RID = re.compile(r"^[0-9a-f]{12}$")

# check 11: files next to the gold folder whose root fields are checked (paths relative to data/; missing ones are noted)
ROOT_FIELD_FILES = ("geez_amharic_dictionary.jsonl", "lexicon/classical_dictionary_kidane_wold.jsonl",
                    "lexicon/modern_geez_amharic_dictionary.jsonl", "lexicon/kidane_wold_root_fixes.jsonl",
                    "lexicon/kidane_wold_verb_triples.jsonl", "lexicon/kidane_wold_verb_triples_rejected.jsonl",
                    "verbs_rbha_anqets.jsonl",
                    "paradigms/synthetic_morphology_train.jsonl", "paradigms/synthetic_morphology_analyze.jsonl",
                    "synthetic/synthetic_forms_for_val_test_roots.jsonl",
                    "synthetic/synthetic_forms_for_val_test_roots_analyze.jsonl")
ROOT_KEY = re.compile(r"^(root|\w+_root)$")
ROOT_PLACEHOLDER = "CHECK"
PLACEHOLDER_LIKE = {"", "check", "todo", "tbd", "unknown", "unsettled", "null", "none", "n/a", "na", "?", "??", "-", "--", "x", "xxx"}

LATIN = re.compile(r"[A-Za-z\u00C0-\u024F\u1E00-\u1EFF\u02B0-\u02FF]")


def is_ethiopic_word(s):
    return bool(s) and all(0x1200 <= ord(c) <= 0x137F for c in s)


def is_first_order(c):
    """1st-order letter of a Ge'ez series (ሀ ለ ሐ ... ቈ ኰ ጐ ኈ): every series is 8 code points wide."""
    cp = ord(c)
    return 0x1200 <= cp <= 0x137F and (cp - 0x1200) % 8 == 0


def root_problem(root):
    if not root:
        return "empty root"
    if "/" in root or "," in root:
        return "two roots joined"
    if LATIN.search(root):
        return "Latin letters in root"
    parts = root.split("-")
    if not 2 <= len(parts) <= 5:
        return "root is not 2-5 letters"
    for p in parts:
        if len(p) != 1 or not (0x1200 <= ord(p) <= 0x137F):
            return f"root letter {p!r} is not one Ge'ez letter"
        if not is_first_order(p):
            return f"root letter {p} is not in the 1st order"
    return None


def form_variants(cell):
    """The "/"-variants of a geez_form cell: "(...)" notes dropped, edge punctuation stripped."""
    out = []
    for v in re.sub(r"\([^)]*\)", " ", cell or "").split("/"):
        v = v.strip(" :፡።()[]፣,")
        if v:
            out.append(v)
    return out


def root_fields(obj, path=""):
    """(key path, value) for every root field (key "root" or "*_root") in a JSON value, at any depth."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if ROOT_KEY.match(k) and not isinstance(v, (dict, list)):
                yield p, v
            else:
                yield from root_fields(v, p)
    elif isinstance(obj, list):
        for v in obj:
            yield from root_fields(v, path + "[]")


def check_root_placeholders(where_file, n, obj, err, odd):
    for key, v in root_fields(obj):
        if v == ROOT_PLACEHOLDER:
            err("11 root placeholders", f"{where_file} line {n}: {key} is {v!r}")
        elif isinstance(v, str) and v.strip().lower() in PLACEHOLDER_LIKE:
            odd[(where_file, key, v)] += 1


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", default=os.path.join("data", "paradigms"), help="folder with the gold files")
    ap.add_argument("--list", action="store_true", help="print every problem")
    args = ap.parse_args()

    errors = collections.defaultdict(list)     # check -> [message]
    notes = collections.Counter()

    def err(check, msg):
        errors[check].append(msg)

    # flagged rows: (split, file line, row, form)
    flagged = set()
    fpath = os.path.join(args.data, FLAGGED)
    flagged_rows = []
    if os.path.exists(fpath):
        with open(fpath, encoding="utf-8", newline="") as f:
            flagged_rows = list(csv.DictReader(f, delimiter="\t"))
        for r in flagged_rows:
            flagged.add((r["split"], int(r["file_line"]), int(r["row"]), r["form"]))

    records = {}
    seen_ids = {}
    for split, name in GOLD.items():
        path = os.path.join(args.data, name)
        if not os.path.exists(path):
            err("1 records", f"{name}: file missing")
            continue
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except ValueError as e:
                    err("1 records", f"{split} line {n}: not JSON ({e})")
                    continue
                missing = [k for k in RECORD_FIELDS if k not in rec]
                if missing:
                    err("1 records", f"{split} line {n}: missing {', '.join(missing)}")
                rid = rec.get("record_id")
                if rid is not None:
                    if not RID.match(str(rid)):
                        err("1 records", f"{split} line {n}: record_id {rid!r} is not 12 hex characters")
                    elif rid in seen_ids:
                        err("1 records", f"{split} line {n}: record_id {rid} also at {seen_ids[rid]}")
                    else:
                        seen_ids[rid] = f"{split} line {n}"
                records[(split, n)] = rec

    pairs = collections.defaultdict(list)          # pair key -> [where]
    root_splits = collections.defaultdict(set)
    found_flagged = set()
    loaded = collections.Counter()

    # record-level stem: a schema value, and the rows' stem when they agree, else the first unflagged row's
    for (split, n), rec in records.items():
        rstem = rec.get("stem")
        if not rstem or rec.get("category") != "verb_conjugation":
            continue
        if rstem not in STEMS:
            err("5 labels", f"{split} line {n}: record stem {rstem!r} is not a schema value")
            continue
        rows = [(j, t) for j, t in enumerate(rec.get("table_data") or []) if (t.get("geez_form") or "").strip()]
        eff = [(j, t.get("stem") or rstem) for j, t in rows]
        if not eff:
            continue
        want = eff[0][1] if len({e for _, e in eff}) > 1 else eff[0][1]
        unflagged = [e for j, e in eff if not any(k[0] == split and k[1] == n and k[2] == j for k in flagged)]
        if len({e for _, e in eff}) > 1 and unflagged:
            want = unflagged[0]
        if rstem != want:
            err("5 labels", f"{split} line {n}: record stem {rstem!r}, rows say {want!r}")

    for (split, n), rec in records.items():
        rec_root = "" if rec.get("root_unsettled") else (rec.get("root") or "")
        if LATIN.search(rec.get("root") or ""):
            err("4 Latin", f"{split} line {n}: record root {rec.get('root')!r}")
        elif rec.get("root") and root_problem(rec["root"]):
            err("3 roots", f"{split} line {n}: record root {rec['root']!r}: {root_problem(rec['root'])}")
        for j, row in enumerate(rec.get("table_data") or []):
            where = f"{split} line {n} row {j}"
            cell = row.get("geez_form") or ""
            if LATIN.search(cell):
                err("4 Latin", f"{where}: form {cell!r}")
            if LATIN.search(row.get("root") or ""):
                err("4 Latin", f"{where}: row root {row.get('root')!r}")
            root = row.get("root") or rec_root
            variants = form_variants(cell)
            if not variants and (split, n, j, "") in flagged:
                found_flagged.add((split, n, j, ""))
            for v in variants:
                if (split, n, j, v) in flagged:
                    found_flagged.add((split, n, j, v))
            if not variants:
                notes["rows with no form (kept, not loaded)"] += 1
                continue
            if not root:
                notes["pairs not loaded: no root yet"] += len(variants)
                continue
            problem = root_problem(root)
            if problem:
                notes[f"pairs not loaded: {problem}"] += len(variants)
                if row.get("root") and not LATIN.search(root):
                    err("3 roots", f"{where}: row root {root!r}: {problem}")
                continue
            typ = row.get("type") or "verb"
            stem = row.get("stem") or rec.get("stem") or ""
            labels = {k: (row.get(k) or "") for k in ("tense", "person", "gender", "number", "object")}
            for v in variants:
                if (split, n, j, v) in flagged:
                    notes["pairs not loaded: flagged"] += 1
                    continue
                if not is_ethiopic_word(v):
                    err("2 forms", f"{where}: {v!r} is not one Ge'ez word")
                    continue
                # 5/6 labels
                if typ not in TYPES:
                    err("5 labels", f"{where} {v}: type {typ!r}")
                elif typ == "verb":
                    if labels["tense"] not in TENSES:
                        err("5 labels", f"{where} {v}: tense {labels['tense']!r}")
                    if (labels["person"], labels["gender"], labels["number"]) not in VERB_PERSONS:
                        err("5 labels", f"{where} {v}: person/gender/number "
                            f"{labels['person']!r}/{labels['gender']!r}/{labels['number']!r}")
                    if stem not in STEMS:
                        err("5 labels", f"{where} {v}: stem {stem!r}")
                    if labels["object"] and labels["object"] not in OBJECTS:
                        err("5 labels", f"{where} {v}: object {labels['object']!r}")
                else:
                    if labels["number"] not in NUMBERS:
                        err("5 labels", f"{where} {v}: {typ} number {labels['number']!r}")
                    if typ == "adjective" and labels["gender"] not in GENDERS_ADJ:
                        err("5 labels", f"{where} {v}: adjective gender {labels['gender']!r}")
                    extra = [k for k in ("tense", "person", "object") if labels[k]]
                    if extra:
                        err("6 nominal", f"{where} {v}: {typ} has verb labels {', '.join(extra)}")
                if typ == "verb":
                    key = (v, root, typ, labels["tense"], labels["person"], labels["gender"],
                           labels["number"], stem, labels["object"])
                elif typ == "adjective":
                    key = (v, root, typ, labels["gender"], labels["number"])
                else:
                    key = (v, root, typ, labels["number"])
                pairs[key].append((split, where))
                root_splits[root].add(split)
                loaded[split] += 1

    allowed = set()                                # (split, file line, form, rows) from the allowed-duplicates file
    apath = os.path.join(args.data, ALLOWED)
    if os.path.exists(apath):
        with open(apath, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter="	"):
                if ":" in r["rows"]:               # across records: rows "line:row;line:row", file_line empty
                    allowed.add((r["split"], None, r["form"], tuple(sorted(tuple(int(y) for y in x.split(":")) for x in r["rows"].split(";")))))
                else:
                    allowed.add((r["split"], int(r["file_line"]), r["form"], tuple(sorted(int(x) for x in r["rows"].split(";")))))
    used_allowed = set()
    for key, places in pairs.items():
        if len(places) > 1:
            m = [re.match(r"(\w+) line (\d+) row (\d+)$", w) for _, w in places]
            if all(m) and len({x.group(1) for x in m}) == 1:
                if len({x.group(2) for x in m}) == 1:
                    k = (m[0].group(1), int(m[0].group(2)), key[0], tuple(sorted(int(x.group(3)) for x in m)))
                else:
                    k = (m[0].group(1), None, key[0], tuple(sorted((int(x.group(2)), int(x.group(3))) for x in m)))
                if k in allowed:
                    used_allowed.add(k)
                    notes["exact duplicates kept on purpose (" + ALLOWED + ")"] += 1
                    continue
            err("7 duplicates", f"{key[0]} ({key[1]}): " + "; ".join(w for _, w in places))
    for root, splits in sorted(root_splits.items()):
        if len(splits) > 1:
            err("8 splits", f"root {root} is in {', '.join(sorted(splits))}")
    for k in sorted(allowed - used_allowed):
        where = f"line {k[1]} rows {k[3]}" if k[1] is not None else "rows " + ";".join(f"{a}:{b}" for a, b in k[3])
        err("7 duplicates", f"{ALLOWED}: {k[0]} {where} {k[2]!r} is not a duplicate in the files")
    for r in flagged_rows:
        k = (r["split"], int(r["file_line"]), int(r["row"]), r["form"])
        if k not in found_flagged:
            err("9 flagged", f"{r['split']} line {r['file_line']} row {r['row']}: form {r['form']!r} not in that row")

    # 11: no root field holds the placeholder CHECK (gold records, then the other files under data/)
    odd = collections.Counter()                    # (file, key path, value) -> count; reported, not an error
    for (split, n), rec in sorted(records.items()):
        check_root_placeholders(GOLD[split], n, rec, err, odd)
    data_dir = os.path.dirname(os.path.abspath(args.data))
    for rel in ROOT_FIELD_FILES:
        path = os.path.join(data_dir, rel)
        if not os.path.exists(path):
            notes[f"root placeholder check: {rel} not found, not checked"] += 1
            continue
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    try:
                        obj = json.loads(line)
                    except ValueError:
                        err("11 root placeholders", f"{rel} line {n}: not JSON")
                        continue
                    check_root_placeholders(rel, n, obj, err, odd)
    for (rel, key, v), c in sorted(odd.items()):
        notes[f"root field {key} = {v!r} in {rel} (placeholder-like, reported only)"] += c

    sums = os.path.join(args.data, "SHA256SUMS")
    if os.path.exists(sums):
        with open(sums, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    h, name = line.split(None, 1)
                    name = name.strip().lstrip("*")
                    p = os.path.join(args.data, name)
                    if not os.path.exists(p) or sha256(p) != h:
                        err("10 hashes", f"{name} does not match SHA256SUMS")

    # report
    print("pairs that load: " + ", ".join(f"{s} {loaded[s]}" for s in GOLD) + f" (records {len(records)})")
    for k, c in sorted(notes.items()):
        print(f"NOTE  {k}: {c}")
    checks = ["1 records", "2 forms", "3 roots", "4 Latin", "5 labels", "6 nominal", "7 duplicates",
              "8 splits", "9 flagged", "10 hashes", "11 root placeholders"]
    for c in checks:
        msgs = errors.get(c, [])
        print(f"{'PASS ' if not msgs else 'ERROR'} {c}: {len(msgs)} problem(s)")
        for m in (msgs if args.list else msgs[:20]):
            print(f"        {m}")
        if msgs and not args.list and len(msgs) > 20:
            print(f"        ... {len(msgs) - 20} more (use --list)")
    bad = sum(len(v) for v in errors.values())
    print("CLEAN" if not bad else f"NOT CLEAN: {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
