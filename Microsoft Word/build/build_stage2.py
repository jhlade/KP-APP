#!/usr/bin/env python3
"""Stage 2: doplni ribbon Abs. prace (customUI + ikona) do .dotm, ktery uz
ma naimportovane a zkompilovane makro (vystup stage 1 po ulozeni ve Wordu).

Pouziti:
    python3 build_stage2.py [input.dotm] [output.dotm]

Vychozi: input  = build/out/kp-app_stage1.dotm (vedle tohoto skriptu)
         output = build/out/kp-app.dotm
"""
import sys
import zipfile
from pathlib import Path

REPO_WORD_DIR = Path(__file__).resolve().parent.parent
BUILD_ASSETS = REPO_WORD_DIR / "build" / "customUI"
OUT_DIR = Path(__file__).resolve().parent / "out"

DEFAULT_INPUT = OUT_DIR / "kp-app_stage1.dotm"
DEFAULT_OUTPUT = OUT_DIR / "kp-app.dotm"

EXTENSIBILITY_REL_TYPE = (
    "http://schemas.microsoft.com/office/2006/relationships/ui/extensibility"
)


def main() -> None:
    input_dotm = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_dotm = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    if not input_dotm.is_file():
        raise SystemExit(f"Chybi vstupni .dotm (je hotova stage 1 + ulozeni ve Wordu?): {input_dotm}")
    if not (BUILD_ASSETS / "customUI.xml").is_file():
        raise SystemExit(f"Chybi ribbon assety v: {BUILD_ASSETS}")

    output_dotm.parent.mkdir(parents=True, exist_ok=True)
    if output_dotm.exists():
        output_dotm.unlink()

    with zipfile.ZipFile(input_dotm, "r") as src:
        names = set(src.namelist())
        if "word/vbaProject.bin" not in names:
            raise SystemExit(
                "word/vbaProject.bin chybi ve vstupu - makro jeste neni "
                "naimportovane/ulozene. Nejdriv dokoncit stage 1 ve Wordu."
            )

        root_rels_xml = src.read("_rels/.rels").decode("utf-8")
        if "customUI/customUI.xml" in root_rels_xml:
            raise SystemExit("Vstup uz ma customUI relationship - neni co delat.")

        root_rels_xml = root_rels_xml.replace(
            "</Relationships>",
            '<Relationship Id="rIdCustomUI" Type="%s" Target="customUI/customUI.xml"/></Relationships>'
            % EXTENSIBILITY_REL_TYPE,
        )

        with zipfile.ZipFile(output_dotm, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                data = src.read(item.filename)
                if item.filename == "_rels/.rels":
                    data = root_rels_xml.encode("utf-8")
                dst.writestr(item, data)

            for asset in sorted(BUILD_ASSETS.rglob("*")):
                if asset.is_dir():
                    continue
                arcname = "customUI/" + str(asset.relative_to(BUILD_ASSETS))
                dst.write(asset, arcname)

    print(f"Vytvoreno: {output_dotm}")
    with zipfile.ZipFile(output_dotm) as check:
        for name in sorted(check.namelist()):
            if name.startswith("customUI") or name == "word/vbaProject.bin":
                print("  ", name)


if __name__ == "__main__":
    main()
