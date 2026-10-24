#!/usr/bin/env python3
"""Check typed Kidane Wold source fields in the merged dictionary.

The classical dictionary's headwords, definitions, forms and pages were corrected from
geezorg/data commit 3904462c in dataset commit 47a773a. The inferred roots share the same recorded corrections (including dataset commit
40b3e24 for entry 5944); other morphology annotations are independently curated.
"""
import argparse
import json
from pathlib import Path

SOURCE = "Kidane Wold Kifle (1948 E.C.)"
SOURCE_FIELDS = ("headword_geez", "amharic_definition", "forms", "page_number", "inferred_root")


def check(dataset_dir):
    root = Path(dataset_dir) / "data/lexicon"
    canonical = {r["id"]: r for line in (root / "classical_dictionary_kidane_wold.jsonl").read_text(encoding="utf-8").splitlines()
                 if line.strip() and (r := json.loads(line))}
    errors, seen = [], set()
    for line in (root / "geez_amharic_dictionary.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("source_lexicon") != SOURCE:
            continue
        ident = row.get("id")
        if ident in seen:
            errors.append(f"Kidane id {ident}: duplicate merged entry")
        seen.add(ident)
        if ident not in canonical:
            errors.append(f"Kidane id {ident}: no canonical entry")
            continue
        for field in SOURCE_FIELDS:
            if row.get(field) != canonical[ident].get(field):
                errors.append(f"Kidane id {ident}: stale {field}")
    errors.extend(f"Kidane id {ident}: absent from merged dictionary" for ident in sorted(canonical.keys() - seen))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir")
    args = parser.parse_args()
    errors = check(args.dataset_dir)
    for error in errors[:20]:
        print(error)
    print(f"{'FAIL' if errors else 'PASS'} dictionary source mirrors: {len(errors)} problem(s)")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
