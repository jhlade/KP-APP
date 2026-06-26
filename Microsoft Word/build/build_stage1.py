#!/usr/bin/env python3
"""Stage 1: kp-app.dotx -> holy macro-enabled .dotm bez ribbonu.

Vystup: build/out/ (gitignored) vedle tohoto skriptu.

Pouziti:
    python3 build_stage1_macro_shell.py [output.dotm]
"""
import sys
import zipfile
from pathlib import Path

REPO_WORD_DIR = Path(__file__).resolve().parent.parent
SOURCE_DOTX = REPO_WORD_DIR / "kp-app.dotx"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "out" / "kp-app_stage1.dotm"

MACRO_ENABLED_MAIN_CONTENT_TYPE = (
    "application/vnd.ms-word.template.macroEnabledTemplate.main+xml"
)
PLAIN_TEMPLATE_MAIN_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
)


def main() -> None:
    output_dotm = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT

    if not SOURCE_DOTX.is_file():
        raise SystemExit(f"Chybi zdrojova sablona: {SOURCE_DOTX}")

    output_dotm.parent.mkdir(parents=True, exist_ok=True)
    if output_dotm.exists():
        output_dotm.unlink()

    with zipfile.ZipFile(SOURCE_DOTX, "r") as src:
        content_types_xml = src.read("[Content_Types].xml").decode("utf-8")

        if PLAIN_TEMPLATE_MAIN_CONTENT_TYPE not in content_types_xml:
            raise SystemExit(
                "Neocekavany [Content_Types].xml - chybi override hlavniho dokumentu"
            )
        content_types_xml = content_types_xml.replace(
            PLAIN_TEMPLATE_MAIN_CONTENT_TYPE, MACRO_ENABLED_MAIN_CONTENT_TYPE
        )

        with zipfile.ZipFile(output_dotm, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                data = src.read(item.filename)
                if item.filename == "[Content_Types].xml":
                    data = content_types_xml.encode("utf-8")
                dst.writestr(item, data)

    print(f"Vytvoreno: {output_dotm}")
    print("Dale: otevrit ve Wordu, Alt+F11, import .bas, Compile, Save jako .dotm.")


if __name__ == "__main__":
    main()
