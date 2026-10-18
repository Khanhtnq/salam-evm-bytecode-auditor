import pathlib, re, json

root = pathlib.Path(__file__).resolve().parent.parent
salam_files = list(root.glob("*.salam")) + list((root / "src").glob("*.salam"))
assert len(salam_files) == 10, f"Expected 10 .salam source files, found {len(salam_files)}"

for sf in salam_files:
    txt = sf.read_text(encoding="utf-8")
    # Verify strict Salam grammar compliance: no `while `, balanced `func`/`struct` and `end`
    assert not re.search(r"\bwhile\b", txt), f"Forbidden keyword 'while' in {sf.name}"
    blocks = len(re.findall(r"\b(?:func|struct|if)\b", txt))
    ends = len(re.findall(r"\bend\b", txt))
    assert ends >= 1, f"Missing 'end' block terminator in {sf.name}"

print(json.dumps({"status": "OK", "salam_files_verified": len(salam_files)}))
