#!/usr/bin/env python3
"""Upravi rok ve dvou datumovych SDT polich kp-app.dotx (Rok + Datum
prohlaseni). Meni jen rok - den/mesic v datu prohlaseni zustava, jaky je
aktualne v sablone.

Pole se hledaji podle stabilnich kotev (w:tag="rok", w:id="99992015"), ne
podle konkretni hodnoty roku - skript je tedy mozne pustit opakovane pro
libovolny dalsi rok.

Pouziti:
    python3 update_date.py ROK
"""
import re
import sys
import zipfile
from pathlib import Path

REPO_WORD_DIR = Path(__file__).resolve().parent.parent
TARGET_DOTX = REPO_WORD_DIR / "kp-app.dotx"

ROK_PATTERN = re.compile(
    r'(<w:tag w:val="rok"/>.*?w:fullDate=")(\d{4})'
    r'(-\d{2}-\d{2}T00:00:00Z".*?<w:rStyle w:val="FORM-rok"/></w:rPr><w:t>)(\d{4})(</w:t>)',
    re.DOTALL,
)

DECLARATION_PATTERN = re.compile(
    r'(<w:id w:val="99992015"/>.*?w:fullDate=")(\d{4})'
    r'(-\d{2}-\d{2}T00:00:00Z".*?<w:rStyle w:val="FORM-datum"/></w:rPr><w:t>)([^<]*?)(\d{4})(</w:t>)',
    re.DOTALL,
)


def replace_rok(data: str, new_year: str) -> str:
    match = ROK_PATTERN.search(data)
    if not match:
        raise SystemExit("Pole Rok (w:tag=\"rok\") nenalezeno - konec bez zapisu.")
    new_block = match.group(1) + new_year + match.group(3) + new_year + match.group(5)
    return data[: match.start()] + new_block + data[match.end():]


def replace_declaration(data: str, new_year: str) -> str:
    match = DECLARATION_PATTERN.search(data)
    if not match:
        raise SystemExit("Pole Datum prohlaseni (w:id=\"99992015\") nenalezeno - konec bez zapisu.")
    new_block = (
        match.group(1) + new_year + match.group(3) + match.group(4) + new_year + match.group(6)
    )
    return data[: match.start()] + new_block + data[match.end():]


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit(__doc__)
    new_year = sys.argv[1]

    if not TARGET_DOTX.is_file():
        raise SystemExit(f"Chybi sablona: {TARGET_DOTX}")

    with zipfile.ZipFile(TARGET_DOTX, "r") as src:
        document_xml = src.read("word/document.xml").decode("utf-8")
        infolist = src.infolist()
        other_files = {
            item.filename: src.read(item.filename)
            for item in infolist
            if item.filename != "word/document.xml"
        }

    document_xml = replace_rok(document_xml, new_year)
    document_xml = replace_declaration(document_xml, new_year)

    tmp_path = TARGET_DOTX.with_suffix(".dotx.tmp")
    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in infolist:
            if item.filename == "word/document.xml":
                dst.writestr(item, document_xml.encode("utf-8"))
            else:
                dst.writestr(item, other_files[item.filename])
    tmp_path.replace(TARGET_DOTX)

    print(f"Upraveno: {TARGET_DOTX}")
    print(f"  Rok -> {new_year}")
    print(f"  Datum prohlaseni -> rok {new_year} (den/mesic beze zmeny)")


if __name__ == "__main__":
    main()
