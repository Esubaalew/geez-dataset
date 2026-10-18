#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Apply a review of held rows to the unified rows and write a reviewed copy.

    python scripts/apply_review.py data/unified/review_2026-10-18.tsv

Input: a review table with one line per form (columns form, row_ids, review_word_class, review_root, review_note).
Output: data/unified/geez_morphology_rows_reviewed.jsonl (the base rows with the review applied). A row that
stays held records the review's proposal and the reason in its status_reason. The base file and the book
files are not changed.

A row of the review is settled (status "") only when the dataset itself supports it:

  * closed-class word (pronoun, demonstrative, preposition, particle, adverb, numeral) with no root:
    loads as that class with no root;
  * word with a root (noun, adjective, verb, ...): the root must already be the root of settled rows; the row
    takes that root's split, so no root crosses splits; a noun or adjective needs a number (from the row or
    from the review text: singular / plural); a verb needs tense, person, gender, number and stem on the row;
  * the settled row must not duplicate a row that already loads.

Anything else stays held. Its status_reason records the review's proposal and why it did not load:
the proposed root is not a root of settled rows, a noun or name has no root (the schema loads nouns only with
a root), or labels are missing. Names and primary nouns without a root are also written to
data/unified/review_2026-10-18_rootless_nouns.tsv for the analyser's list of rootless words.
"""
import collections
import csv
import json
import os
import re
import sys

ROOTLESS_CLASSES = {"pronoun", "demonstrative", "preposition", "particle", "adverb", "numeral"}
ROOTED = {"verb", "noun", "adjective", "nominal", "infinitive", "gerund", "verbal_noun"}
REQ = {"verb": ("tense", "person", "gender", "number", "stem"), "gerund": ("stem", "person", "gender", "number"),
       "infinitive": ("stem",), "verbal_noun": ("stem",), "noun": ("number",), "adjective": ("number",)}
ROOT_RE = re.compile(r"[\u1200-\u137f](-[\u1200-\u137f]){1,4}")


def number_from_text(text):
    t = text.lower()
    if re.search(r"\bplural\b|\bnumber=p\b|broken plural", t):
        return "p"
    if re.search(r"\bsingular\b|\bnumber=s\b|\bcollective\b", t):
        return "s"
    return None


def gender_from_text(text):
    t = text.lower()
    if "feminine" in t:
        return "f"
    if "masculine" in t:
        return "m"
    return None


def key(r):
    return (r["form"], r["root"], r["word_class"], r["tense"], r["person"], r["gender"], r["number"], r["stem"],
            r["object"], r["possessor"])


def main(review_path):
    ds = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    unified = os.path.join(ds, "data", "unified")
    rows = [json.loads(l) for l in open(os.path.join(unified, "geez_morphology_rows.jsonl"), encoding="utf-8")]
    by_id = {r["id"]: r for r in rows}
    root_split = {}
    for r in rows:
        if r["status"] == "" and r["root"]:
            root_split.setdefault(r["root"], r["split"])
    loaded_keys = {key(r) for r in rows if r["status"] == ""}
    stem = os.path.splitext(os.path.basename(review_path))[0]
    review = list(csv.DictReader(open(review_path, encoding="utf-8"), delimiter="\t"))

    log, counts, rootless_nouns = [], collections.Counter(), []
    for v in review:
        cls = v["review_word_class"].strip()
        root = v["review_root"].strip() or None
        note = v["review_note"].strip()
        for rid in v["row_ids"].split():
            r = by_id.get(rid)
            if r is None or r["status"] in ("", "EXCLUDED"):
                counts["skipped (already loads or excluded)"] += 1
                continue
            new = dict(r)
            new["word_class"] = cls or r["word_class"]
            reason = None
            if new["word_class"] in ROOTLESS_CLASSES:
                if root:
                    reason = f"review: {new['word_class']} given root {root}"
                else:
                    new["root"] = None
                    for k in ("stem", "tense", "person", "gender", "number", "object"):
                        new[k] = None
            elif new["word_class"] in ROOTED:
                if not root:
                    reason = "review: rootless noun (name or primary noun); the schema loads nouns only with a root"
                    rootless_nouns.append((r["form"], new["word_class"], note))
                elif not ROOT_RE.fullmatch(root):
                    reason = f"review: malformed root {root}"
                elif root not in root_split:
                    reason = f"review: proposed root {root} is not a root of settled rows; confirm in a book or dictionary"
                else:
                    new["root"] = root
                    new["split"] = root_split[root]
                    if new["word_class"] in ("noun", "adjective"):
                        new["number"] = new["number"] or number_from_text(note)
                        new["gender"] = new["gender"] or gender_from_text(note)
                    missing = [k for k in REQ.get(new["word_class"], ()) if not new[k]]
                    if missing:
                        reason = f"review: root {root} accepted but {', '.join(missing)} missing"
            else:
                reason = f"review: class {new['word_class']!r} does not load"
            if reason is None and key(new) in loaded_keys:
                reason = "review: same form and labels as a row that already loads"
            if reason is None:
                old_root = r["root"]
                new["status"], new["status_reason"] = "", ""
                tail = f"review 2026-10-18: {note}"
                if old_root and old_root != new["root"]:
                    tail += f" (book root {old_root} replaced)"
                new["evidence"] = (r["evidence"] + "; " if r["evidence"] else "") + tail
                loaded_keys.add(key(new))
                by_id[rid] = new
                counts["settled"] += 1
                outcome = "settled"
            else:
                new = dict(r)
                new["status_reason"] = (r["status_reason"] + "; " if r["status_reason"] else "") + \
                    f"{reason}; proposal: {cls} {root or 'no root'}"
                by_id[rid] = new
                counts[reason.split(";")[0].split(" root ")[0] if "proposed root" not in reason else
                       "held: proposed root not attested"] += 1
                outcome = "held"
            log.append((rid, r["form"], r["status"], outcome, by_id[rid]["word_class"], by_id[rid]["root"] or "",
                        by_id[rid]["split"], reason or ""))

    out_rows = [by_id[r["id"]] for r in rows]
    with open(os.path.join(unified, "geez_morphology_rows_reviewed.jsonl"), "w", encoding="utf-8") as f:
        for r in out_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(unified, f"{stem}_rootless_nouns.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["word", "word_class", "review_note"])
        w.writerows(sorted(set(rootless_nouns)))
    for k, c in counts.most_common():
        print(f"{c:6d}  {k}")
    print("rows that load: base", sum(r["status"] == "" for r in rows), "reviewed", sum(r["status"] == "" for r in out_rows))


if __name__ == "__main__":
    main(sys.argv[1])
