"""Merged dictionary source corrections must not regress to older OCR."""
import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("dictionary_mirrors", Path(__file__).parents[1] / "scripts/check_dictionary_mirrors.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def test_source_fields_and_roots_checked_but_other_annotations_remain_independent(tmp_path):
    p = tmp_path / "data/lexicon"
    p.mkdir(parents=True)
    source = dict(id=4, headword_geez="መስተበቅል", amharic_definition="source", forms=["በቅል"], page_number=1,
                  inferred_root="b-q-l")
    merged = dict(source, source_lexicon=checker.SOURCE, pos="independent annotation")
    modern = dict(headword_geez="other", source_lexicon="another book")
    (p / "classical_dictionary_kidane_wold.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
    target = p / "geez_amharic_dictionary.jsonl"
    target.write_text(json.dumps(merged) + "\n" + json.dumps(modern) + "\n", encoding="utf-8")
    assert checker.check(tmp_path) == []
    merged["headword_geez"] = "old OCR"
    target.write_text(json.dumps(merged) + "\n", encoding="utf-8")
    assert checker.check(tmp_path) == ["Kidane id 4: stale headword_geez"]
