#!/usr/bin/env python3
"""Build data/clitics/clitic_forms.jsonl: proclitic and enclitic forms made by rule from settled rows.

Run from the repository root:

    python scripts/build_clitic_forms.py

Ge'ez writes its proclitics joined to the next word (ወ "and", ዘ relative / "of", ለ "to, for", በ "in, by",
እም "from") and its enclitics joined to the end of the word (ሰ "as for", ኒ / ሂ "also", ኑ question). The
labelled rows of this repository are bare forms, so running text such as ለሕዝብ, ወገብረ or ዘለዓለም has no
row. This script adds such forms by rule:

  * The source is every row of data/unified/geez_morphology_rows_reviewed.jsonl with an empty status.
  * A clitic form is the clitic string joined to the bare form, with no change of spelling.
  * The new row copies root, word class and all features from its source row. Its evidence names the
    source row, so every root still traces to a book or gold record, never to a tool or model.
  * The new row keeps the split of its source row, so no root crosses splits.
  * Which clitics a row receives depends on its word class: the prepositions ለ, በ, እም join nominals only;
    ወ and ዘ join any word; enclitics join any word.
  * A noun with no root receives every proclitic of PRO_ROOTLESS_NOUN (no enclitics); a form made this way
    is dropped if it is a row of the books or is made from a row of another split.
  * A source row whose leading ወ is the conjunction proclitic (form starts with ወ, root does not, and the
    evidence notes proclitic ወ- or the form without ወ is a row of the same root) gets no proclitic: ወ is
    always the outermost proclitic, so nothing can stand before it. Enclitics still join.
  * Every other source row receives at most VARIANTS_PER_ROW forms. The choice is a fixed hash of the row id, so
    the file is the same on every run.

The output has the fields of the unified rows plus `proclitic`, `enclitic` and `base_id`.
Train only on rows with split "train".
"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "unified", "geez_morphology_rows_reviewed.jsonl")
OUT_DIR = os.path.join(ROOT, "data", "clitics")
OUT = os.path.join(OUT_DIR, "clitic_forms.jsonl")
VARIANTS_PER_ROW = 3

NOMINAL = {"noun", "adjective", "nominal", "infinitive", "verbal_noun", "gerund", "numeral", "proper_noun"}
CLOSED = {"particle", "preposition", "pronoun", "demonstrative", "adverb"}
PRO_NOMINAL = ["ወ", "ለ", "በ", "እም", "ዘ", "ወለ", "ወበ", "ወእም", "ዘበ", "ዘእም"]
PRO_VERB = ["ወ", "ዘ", "ወዘ"]
PRO_CLOSED = ["ወ"]
# full proclitic set for nouns with no root (the sample of 3 is too thin to teach 'root: none')
PRO_ROOTLESS_NOUN = ["ወ", "ለ", "በ", "ከ", "እም", "ዘ", "ወለ", "ወበ", "ወከ", "ወእም", "ዘእም", "ወዘ"]
ENCLITICS = ["ሰ", "ኒ", "ሂ", "ኑ"]


def options(word_class):
    if word_class in NOMINAL:
        pro = PRO_NOMINAL
    elif word_class == "verb":
        pro = PRO_VERB
    elif word_class in CLOSED:
        pro = PRO_CLOSED
    else:
        return []
    combos = [(p, "") for p in pro] + [("", e) for e in ENCLITICS] + [(p, e) for p in pro[:2] for e in ENCLITICS[:2]]
    return combos


def pick(row_id, combos, k):
    ranked = sorted(combos, key=lambda c: hashlib.sha256(f"{row_id}|{c[0]}|{c[1]}".encode()).hexdigest())
    return ranked[:k]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    seen = set()
    bare_forms = set()
    rows = []
    with open(SRC, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                bare_forms.add(r["form"])
                rows.append(r)
    roots_of_form = {}
    for r in rows:
        roots_of_form.setdefault(r["form"], set()).add(r.get("root"))

    def leading_wa(r):
        f, root, ev = r["form"], r.get("root") or "", r.get("evidence") or ""
        if not f.startswith("ወ") or len(f) < 3 or root.startswith("ወ"):
            return False
        if "proclitic ወ-" in ev or "ወ-" in ev.split(";")[0]:
            return True
        return r.get("root") in roots_of_form.get(f[1:], set())

    def rootless_noun(r):
        return r.get("word_class") == "noun" and not r.get("root")

    def combos_of(r):
        if rootless_noun(r):
            combos = [(p, "") for p in PRO_ROOTLESS_NOUN]
        else:
            combos = pick(r["id"], options(r.get("word_class")), VARIANTS_PER_ROW)
        if leading_wa(r):
            combos = [(p, e) for p, e in combos if not p]
        return combos

    # forms made from rows of more than one split: such a rootless-noun form is not written
    form_splits = {}
    for r in rows:
        if not r.get("status"):
            for pro, enc in combos_of(r):
                form_splits.setdefault(pro + r["form"] + enc, set()).add(r["split"])
    n_out = 0
    counts = {}
    with open(OUT, "w", encoding="utf-8") as out:
        for r in rows:
            if r.get("status"):
                continue
            for pro, enc in combos_of(r):
                if rootless_noun(r) and len(form_splits[pro + r["form"] + enc]) > 1:
                    continue
                form = pro + r["form"] + enc
                # a string that is already a form of the books is left to the books
                if form in bare_forms:
                    continue
                key = (form, r.get("root"), r.get("word_class"), r.get("stem"), r.get("tense"), r.get("person"),
                       r.get("gender"), r.get("number"), r.get("object"), r.get("possessor"), r["split"])
                if key in seen:
                    continue
                seen.add(key)
                new = dict(r)
                new.update(id=f"{r['id']}c{n_out}", form=form, proclitic=pro or None, enclitic=enc or None,
                           base_id=r["id"], source="clitic_rule",
                           evidence=f"rule: {pro or '-'} + form of {r['id']} + {enc or '-'}; root and features of {r['id']}",
                           also_in=None)
                out.write(json.dumps(new, ensure_ascii=False) + "\n")
                n_out += 1
                counts[r["split"]] = counts.get(r["split"], 0) + 1
    print(f"{n_out} clitic forms written to {os.path.relpath(OUT, ROOT)} by split: {counts}")


if __name__ == "__main__":
    main()
