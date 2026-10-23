"""No proclitic is added before a source row's conjunction ወ- (scripts/build_clitic_forms.py)."""
import json, os, shutil, subprocess, sys

DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def row(i, form, word_class, root, evidence=""):
    return dict(id=f"u{i:06d}", form=form, root=root, word_class=word_class, stem=None, tense=None, person=None,
                gender=None, number="s", object=None, possessor=None, negated=False, source="book", book="t",
                page=None, source_ref="t", evidence=evidence, also_in=[], status="", status_reason="", split="train")


def build(tmp_path, rows):
    shutil.copytree(os.path.join(DS, "scripts"), tmp_path / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    u = tmp_path / "data" / "unified"
    u.mkdir(parents=True)
    (u / "geez_morphology_rows_reviewed.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    subprocess.run([sys.executable, str(tmp_path / "scripts" / "build_clitic_forms.py")], check=True, capture_output=True)
    out = [json.loads(l) for l in open(tmp_path / "data" / "clitics" / "clitic_forms.jsonl", encoding="utf-8")]
    return out


def test_no_prefix_before_conjunction_wa(tmp_path):
    rows = [row(1, "ቀዳሚ", "noun", "ቀ-ደ-መ"),
            row(53976, "ወቀዳሚ", "noun", "ቀ-ደ-መ", "noun, root ቀ-ደ-መ; proclitic ወ-"),
            row(6, "ወለደ", "verb", "ወ-ለ-ደ")]
    out = build(tmp_path, rows)
    wa = [r for r in out if r["base_id"] == "u053976"]
    assert all(not r["proclitic"] for r in wa), wa
    assert "እምወቀዳሚ" not in {r["form"] for r in out}
    assert wa and all(r["enclitic"] for r in wa)
    assert any(r["proclitic"] for r in out if r["base_id"] == "u000006")
    assert "ወወለደኒ" in {r["form"] for r in out}


def test_suffix_forms_of_wa_row_still_build(tmp_path):
    rows = [row(1, "ቀዳሚ", "noun", "ቀ-ደ-መ"), row(53976, "ወቀዳሚ", "noun", "ቀ-ደ-መ", "proclitic ወ-")]
    forms = {r["form"] for r in build(tmp_path, rows) if r["base_id"] == "u053976"}
    assert {"ወቀዳሚሂ", "ወቀዳሚኑ"} <= forms, forms


def test_wa_row_with_enclitic_gets_no_prefix(tmp_path):
    rows = [row(10, "ገሰሰ", "verb", "ገ-ሰ-ሰ"), row(50266, "ወገሰሰኒ", "verb", "ገ-ሰ-ሰ"),
            row(11, "ምድርነ", "noun", "መ-ደ-ረ"), row(52178, "ወምድርነኒ", "noun", "መ-ደ-ረ"),
            row(12, "አልዓዛር", "proper_noun", None), row(52663, "ወአልዓዛርሰ", "proper_noun", None),
            row(13, "ለደ", "verb", "ወ-ለ-ደ"), row(6, "ወለደኒ", "verb", "ወ-ለ-ደ")]
    out = build(tmp_path, rows)
    for uid in ("u050266", "u052178", "u052663"):
        assert all(not r["proclitic"] for r in out if r["base_id"] == uid), uid
    assert "ወወገሰሰኒ" not in {r["form"] for r in out}
    # a root that starts with ወ keeps its proclitics even if the rest looks like a form
    assert any(r["proclitic"] for r in out if r["base_id"] == "u000006")
