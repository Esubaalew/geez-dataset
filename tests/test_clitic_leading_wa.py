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


def test_no_second_preposition_but_wa_and_za_allowed(tmp_path):
    rows = [row(1, "ዐራት", "noun", None), row(52232, "በዐራት", "noun", None)]
    out = build(tmp_path, rows)
    forms = {r["form"] for r in out if r["base_id"] == "u052232"}
    assert "ዘበዐራት" in forms and "ወዘበዐራት" in forms
    assert "ወበዐራት" in {r["form"] for r in out}  # also ወበ + ዐራት
    assert not {"ለበዐራት", "በበዐራት", "ከበዐራት", "እምበዐራት", "ወለበዐራት", "ዘእምበዐራት"} & forms


def test_second_preposition_rooted_and_root_letters(tmp_path):
    rows = [row(1, "ጽድቅከ", "noun", "ጸ-ደ-ቀ"), row(20, "በጽድቅከ", "noun", "ጸ-ደ-ቀ"),
            row(2, "ረከት", "noun", "በ-ረ-ከ"), row(21, "በረከት", "noun", "በ-ረ-ከ")]
    out = build(tmp_path, rows)
    assert all(not any(x in (r["proclitic"] or "") for x in "ለበከ") and "እም" not in (r["proclitic"] or "")
               for r in out if r["base_id"] == "u000020")
    # a root that starts with በ keeps its prepositions
    assert any(r["proclitic"] and any(x in r["proclitic"] for x in ("ለ", "በ", "እም")) for r in out if r["base_id"] == "u000021")


def test_rooted_prefix_blocked_without_bare_row(tmp_path):
    # ለምድሩ (root መ-ደ-ረ) has no bare ምድሩ row; still no second preposition
    forms = {r["form"] for r in build(tmp_path, [row(51119, "ለምድሩ", "noun", "መ-ደ-ረ")])}
    assert "ለለምድሩሰ" not in forms
    assert not any(f.startswith(("ለለ", "በለ", "ከለ", "እምለ", "ወለለ", "ወበለ", "ወእምለ", "ዘእምለ")) for f in forms)


def test_rootless_ka_prefix_not_blocked(tmp_path):
    rows = [row(1, "በሎ", "noun", None), row(29579, "ከበሎ", "noun", None)]
    forms = {r["form"] for r in build(tmp_path, rows) if r["base_id"] == "u029579"}
    assert "ለከበሎ" in forms and "ወለከበሎ" in forms


def test_bare_wa_always_kept(tmp_path):
    rows = [row(14794, "መኑ", "pronoun", None),
            row(53976, "ወቀዳሚ", "noun", "ቀ-ደ-መ", "proclitic ወ-")]
    out = build(tmp_path, rows)
    mn = [r for r in out if r["base_id"] == "u014794"]
    assert any(r["form"] == "ወመኑ" and r["proclitic"] == "ወ" and not r["enclitic"] for r in mn), mn
    assert len(mn) <= 3
    assert all(not r["proclitic"] for r in out if r["base_id"] == "u053976")


def test_bare_za_always_kept(tmp_path):
    rows = [row(i, f, wc, r) for i, f, wc, r in [(30, "ቀተለ", "verb", "ቀ-ተ-ለ"), (31, "ንጉሥ", "noun", "ነ-ገ-ሠ"), (32, "መንገሥት", "noun", "መ-ነ-ገ")]]
    out = build(tmp_path, rows)
    for r in rows:
        kids = [o for o in out if o["base_id"] == r["id"]]
        assert len(kids) <= 3
        assert any(o["form"] == "ዘ" + r["form"] and o["proclitic"] == "ዘ" and not o["enclitic"] for o in kids), kids
        assert any(o["form"] == "ወ" + r["form"] and not o["enclitic"] for o in kids), kids
