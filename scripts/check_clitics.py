#!/usr/bin/env python3
"""Check generated clitic forms against their settled source rows and held-out splits."""
import argparse
import collections
import json
from pathlib import Path

INHERITED = ("root", "word_class", "stem", "tense", "person", "gender", "number", "object", "possessor",
             "negated", "split", "book", "page", "source_ref")


def check(dataset_dir):
    ds = Path(dataset_dir)
    source = ds / "data/unified/geez_morphology_rows_reviewed.jsonl"
    target = ds / "data/clitics/clitic_forms.jsonl"
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    bases = {r["id"]: r for r in rows}
    bare_forms = {r["form"] for r in rows}
    errors, ids, keys = [], set(), set()
    splits = collections.defaultdict(set)
    with target.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            r = json.loads(line)
            label = f"line {n} ({r.get('id')})"
            if r.get("id") in ids:
                errors.append(f"{label}: duplicate id")
            ids.add(r.get("id"))
            base = bases.get(r.get("base_id"))
            if base is None:
                errors.append(f"{label}: unknown base_id")
                continue
            if base.get("status") or r.get("status") or r.get("source") != "clitic_rule":
                errors.append(f"{label}: source/base must be a settled clitic_rule row")
            for k in INHERITED:
                if r.get(k) != base.get(k):
                    errors.append(f"{label}: {k} differs from base {base['id']}")
            expected = (r.get("proclitic") or "") + base["form"] + (r.get("enclitic") or "")
            if r.get("form") != expected or not (r.get("proclitic") or r.get("enclitic")):
                errors.append(f"{label}: form does not join clitics to its base")
            if r.get("form") in bare_forms:
                errors.append(f"{label}: generated spelling is already a source form")
            key = (r.get("form"),) + tuple(r.get(k) for k in INHERITED[:11])
            if key in keys:
                errors.append(f"{label}: duplicate analysis")
            keys.add(key)
            splits[r.get("form")].add(r.get("split"))
    for form, values in sorted(splits.items()):
        if len(values) > 1:
            errors.append(f"{form}: generated spelling crosses splits {sorted(values)}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir")
    args = parser.parse_args()
    errors = check(args.dataset_dir)
    for error in errors[:20]:
        print(error)
    print(f"{'FAIL' if errors else 'PASS'} clitics: {len(errors)} problem(s)")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
