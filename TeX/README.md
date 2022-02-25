Připraveno pro TeXLive (XeLaTeX/LuaLaTeX, Biber). Předpokládá se alespoň
základní orientace v&nbsp;syntaxi LaTeXu.

<b>Organizace</b>
* `metadata.tex` - prostředí s&nbsp;proměnnými daty
* `app.tex` - základní dokument, do něj lze doplnit vlastní text (ať už vložením
souborů, nebo přímo)
* `literatura.bib` - seznam literatury ve&nbsp;formátu BibTeX
* `struktura/podekovani.tex` - text poděkování, lze vypnout v&nbsp;základním
dokumentu
* `struktura/shrnuti.tex` - text anotace
* `struktura/shrnuti-cizi.tex` - text anotace v&nbsp;cizím jazyce
* `struktura/slovnik.tex` - slovník pro úpravu zalamování slov

<b>Makefile</b>
Překlad do PDF lze zajistit jednoduchým zavoláním `make`, konečný výsledek bude
uložen jako `app.pdf`.
