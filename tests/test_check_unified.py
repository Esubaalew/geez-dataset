"""scripts/check_unified.py: usage, root-letter guard, gold split exception."""
import json, os, shutil, subprocess, sys

DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["id", "form", "root", "word_class", "stem", "tense", "person", "gender", "number", "object", "possessor", "negated", "source",
        "book", "page", "source_ref", "evidence", "also_in", "status", "status_reason", "split"]


def row(i, form, word_class="verb", split="train", root="ቀ-ተ-ለ", source="book", status="", **extra):
    r = dict.fromkeys(COLS)
    r.update(id=f"u{i:06d}", form=form, root=root, word_class=word_class, stem="basic", tense="past",
             person="3", gender="m", number="s", negated=False, source=source, evidence="", also_in=[],
             status=status, status_reason="", split=split)
    r.update(extra)
    return r


def run_check(tmp_path, rows):
    shutil.copytree(os.path.join(DS, "scripts"), tmp_path / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    u = tmp_path / "data" / "unified"
    u.mkdir(parents=True)
    (u / "geez_morphology_rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return subprocess.run([sys.executable, str(tmp_path / "scripts" / "check_unified.py"), str(tmp_path)],
                          capture_output=True, text=True)


def test_no_dataset_dir_prints_usage():
    p = subprocess.run([sys.executable, os.path.join(DS, "scripts", "check_unified.py")], capture_output=True, text=True)
    assert p.returncode == 2
    assert "IndexError" not in p.stderr
    assert "usage" in p.stderr.lower()
    assert "dataset_dir" in p.stderr


def test_multichar_root_part_is_reported(tmp_path):
    p = run_check(tmp_path, [row(1, "ቀተለ", root="ቀተ-ለ")])
    assert "TypeError" not in p.stderr
    assert "FAIL 3 forms" in p.stdout
    assert "ቀተ-ለ" in p.stdout


def test_gold_val_test_form_is_listed_not_failed(tmp_path):
    rows = [
        row(1, "ቀተለ", split="train", source="gold", root="ቀ-ተ-ለ"),
        row(2, "ይቅትል", split="val", source="gold", root="ቀ-ሠ-ረ", tense="present"),
        row(3, "ይቅትል", split="val", source="book", root="ቀ-ተ-ለ"),
    ]
    p = run_check(tmp_path, rows)
    assert "gold split exception (listed): root ቀ-ተ-ለ" in p.stdout
    assert "FAIL 4 splits" not in p.stdout


def test_plain_multi_split_root_fails(tmp_path):
    rows = [row(1, "ቀተለ", split="train"), row(2, "ቀተሉ", split="val")]
    p = run_check(tmp_path, rows)
    assert "FAIL 4 splits" in p.stdout
