#!/usr/bin/env python3
"""Zapise zalozky a strukturu volitelnych bloku do kp-app.dotx.

Bloky (vsechny ve vychozim stavu PRITOMNE):
  - OPT_BLANK_FRONT  obeplne predni prazdnou stranku (prazdny odstavec +
                     rucni zalom stranky). Predni matter je necislovany,
                     takze je bez cisla i bez samostatneho oddilu.
  - OPT_BLANK_BACK   zalozka-znacka na terminalni prazdne strane (uz je bez
                     cisla - footer3.xml nema pole PAGE). Makro ji prepina pres
                     SectionStart (nextPage/continuous), oddil se NEMAZE.
  - OPT_THANKS       obeplne spacer (567 b.) + SDT podekovani + NOVY koncovy
                     zalom stranky. Zalom za podpisem zustava natvrdo mimo
                     zalozku, takze Obsah je vzdy na vlastni strance.
  - OPT_THANKS_ANCHOR  nulova kotva tesne pred Obsahem pro znovuvlozeni.

Upravuje kp-app.dotx na miste. Hlida pocty vyskytu; pokud uz zalozky
existuji, skonci bez zapisu (idempotence).

Pouziti:
    python3 build_dotx_blocks.py
"""
import zipfile
from pathlib import Path

REPO_WORD_DIR = Path(__file__).resolve().parent.parent
TARGET_DOTX = REPO_WORD_DIR / "kp-app.dotx"

NEW_BREAK_PARA = (
    '<w:p><w:pPr><w:pStyle w:val="ZkladnText"/></w:pPr>'
    '<w:r><w:br w:type="page"/></w:r></w:p>'
)
# Kotva OBEPNE odstavec 49379A80 (continuous zalom + TOC) - nenulova, takze
# ji mazani bloku OPT_THANKS nemuze "spolknout".
THANKS_ANCHOR_START = '<w:bookmarkStart w:id="904" w:name="OPT_THANKS_ANCHOR"/>'


def repl(data, old, new, *, count=1):
    found = data.count(old)
    if found != count:
        raise SystemExit(f"Cekano {count}x, nalezeno {found}x:\n  {old[:80]}...")
    return data.replace(old, new)


def main():
    if not TARGET_DOTX.is_file():
        raise SystemExit(f"Chybi sablona: {TARGET_DOTX}")

    with zipfile.ZipFile(TARGET_DOTX, "r") as src:
        infolist = src.infolist()
        files = {it.filename: src.read(it.filename) for it in infolist}

    d = files["word/document.xml"].decode("utf-8")

    if "OPT_BLANK_FRONT" in d or "OPT_THANKS" in d or "OPT_BLANK_BACK" in d:
        raise SystemExit("Zalozky uz existuji - konec bez zapisu (idempotence).")

    # --- FRONT: obal [729D810C + 1F6CA0DF] zalozkou OPT_BLANK_FRONT ---
    d = repl(
        d,
        '<w:p w14:paraId="729D810C"',
        '<w:bookmarkStart w:id="901" w:name="OPT_BLANK_FRONT"/><w:p w14:paraId="729D810C"',
    )
    d = repl(
        d,
        '</w:p><w:p w14:paraId="25645A10"',
        '</w:p><w:bookmarkEnd w:id="901"/><w:p w14:paraId="25645A10"',
    )

    # --- BACK: zalozka-znacka na 7C5578DF + zruseni cisla terminalniho oddilu ---
    d = repl(
        d,
        '<w:p w14:paraId="7C5578DF"',
        '<w:bookmarkStart w:id="902" w:name="OPT_BLANK_BACK"/><w:p w14:paraId="7C5578DF"',
    )
    d = repl(
        d,
        '</w:p><w:sectPr w:rsidR="00567D88" w:rsidRPr="00656E8A"',
        '</w:p><w:bookmarkEnd w:id="902"/><w:sectPr w:rsidR="00567D88" w:rsidRPr="00656E8A"',
    )
    # Terminalni oddil uz je bez cisla: footerReference rId11 -> footer3.xml,
    # ktery NEMA pole PAGE. Nechavame ho byt; cislo na sdilene strance pri
    # vypnuti zadni strany resi makro (Footer.LinkToPrevious).

    # --- THANKS: zalozka kolem spacer+SDT+novy zalom, kotva pred Obsahem ---
    d = repl(
        d,
        '<w:p w14:paraId="1D4B5B6C"',
        '<w:bookmarkStart w:id="903" w:name="OPT_THANKS"/><w:p w14:paraId="1D4B5B6C"',
    )
    d = repl(
        d,
        '</w:sdt><w:p w14:paraId="49379A80"',
        "</w:sdt>" + NEW_BREAK_PARA + '<w:bookmarkEnd w:id="903"/>'
        + THANKS_ANCHOR_START + '<w:p w14:paraId="49379A80"',
    )
    # kotva (id 904) konci az za odstavcem 49379A80, pred nadpisem Obsah
    d = repl(
        d,
        '</w:p><w:p w14:paraId="752EF517"',
        '</w:p><w:bookmarkEnd w:id="904"/><w:p w14:paraId="752EF517"',
    )

    files["word/document.xml"] = d.encode("utf-8")

    tmp = TARGET_DOTX.with_suffix(".dotx.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for it in infolist:
            dst.writestr(it, files[it.filename])
    tmp.replace(TARGET_DOTX)

    print(f"Upraveno: {TARGET_DOTX}")
    print("  + OPT_BLANK_FRONT, OPT_BLANK_BACK, OPT_THANKS, OPT_THANKS_ANCHOR")
    print("  + koncovy zalom stranky za podekovanim")


if __name__ == "__main__":
    main()
