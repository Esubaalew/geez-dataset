"""Rootless adjectives load only through data/unified/rootless_derived.tsv (scripts/check_unified.py, check 2)."""
import json, os, shutil, subprocess, sys

DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["id", "form", "root", "word_class", "stem", "tense", "person", "gender", "number", "object", "possessor", "negated", "source",
        "book", "page", "source_ref", "evidence", "also_in", "status", "status_reason", "split"]


def row(i, form, word_class, split="train", root=None, gender=None):
    r = dict.fromkeys(COLS)
    r.update(id=f"u{i:06d}", form=form, root=root, word_class=word_class, gender=gender, number="s", negated=False,
             source="book", evidence="", also_in=[], status="", status_reason="", split=split)
    return r


def check(tmp_path, rows, derived, rootless=("ኀነፊ",)):
    shutil.copytree(os.path.join(DS, "scripts"), tmp_path / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    u = tmp_path / "data" / "unified"
    u.mkdir(parents=True)
    (u / "rootless_nouns.tsv").write_text("form\tsource\n" + "".join(f"{f}\ttest\n" for f in rootless), encoding="utf-8")
    (u / "rootless_derived.tsv").write_text("form\tbase\tref\n" + "".join(f"{f}\t{b}\ttest\n" for f, b in derived), encoding="utf-8")
    (u / "geez_morphology_rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    p = subprocess.run([sys.executable, str(tmp_path / "scripts" / "check_unified.py"), str(tmp_path)], capture_output=True, text=True)
    line = next(l for l in p.stdout.splitlines() if "2 labels" in l)
    return line.startswith("PASS"), p.stdout


def test_derived_adjective_loads(tmp_path):
    ok, out = check(tmp_path, [row(1, "ኀነፊ", "noun"), row(2, "ኀነፋዊ", "adjective", gender="m")], [("ኀነፋዊ", "ኀነፊ")])
    assert ok, out


def test_wrong_ending_rejected(tmp_path):
    ok, out = check(tmp_path, [row(1, "ኀነፊ", "noun"), row(2, "ኀነፋይ", "adjective")], [("ኀነፋይ", "ኀነፊ")])
    assert not ok and "-ዊ" in out


def test_base_not_rootless_rejected(tmp_path):
    ok, out = check(tmp_path, [row(1, "ሰማይ", "noun", root="ሰ-መ-የ"), row(2, "ሰማያዊ", "adjective")], [("ሰማያዊ", "ሰማይ")], rootless=())
    assert not ok and "does not load as a rootless" in out


def test_split_mismatch_rejected(tmp_path):
    ok, out = check(tmp_path, [row(1, "ኀነፊ", "noun", split="val"), row(2, "ኀነፋዊ", "adjective")], [("ኀነፋዊ", "ኀነፊ")])
    assert not ok and "loads in val" in out


def test_unlisted_adjective_rejected(tmp_path):
    ok, out = check(tmp_path, [row(1, "ኀነፊ", "noun"), row(2, "ኀነፋዊ", "adjective")], [])
    assert not ok and "not in rootless_derived.tsv" in out
