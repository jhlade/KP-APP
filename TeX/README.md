Připraveno pro [TeXLive](https://www.tug.org/texlive/) (XeLaTeX/LuaLaTeX,
Biber). Předpokládá se alespoň základní orientace v&nbsp;syntaxi LaTeXu.
Zjednodušené stažení v&nbsp;jednom
archivu: [`app.tar.gz`](./app.tar.gz?raw=true).

TeXLive jako prostředí lze i&nbsp;dockerizovat z&nbsp;oficiálního
obrazu `texlive/texlive`.

**Organizace**
* `metadata.tex` - prostředí s&nbsp;proměnnými daty, zde vyplníte jména, název
práce, klíčová slova, a&nbsp;další
* `app.tex` - základní dokument s&nbsp;členěním celé práce, při výchozím použití
do něj není nutné zasahovat
* `text-uvod.tex` - text úvodu práce
* `text-prace.tex` - vlastní text práce
* `text-zaver.tex` - text závěru práce
* `prilohy.tex` - prostor pro přílohy
* `literatura.bib` - seznam literatury ve&nbsp;formátu BibTeX
* `struktura/podekovani.tex` - text poděkování, lze vypnout v&nbsp;základním
dokumentu
* `struktura/shrnuti.tex` - text anotace
* `struktura/shrnuti-cizi.tex` - text anotace v&nbsp;cizím jazyce
* `struktura/slovnik.tex` - slovník pro úpravu zalamování slov

**Makefile**<br>
Překlad do PDF lze zajistit jednoduchým zavoláním `make`, konečný výsledek bude
uložen jako `app.pdf` s&nbsp;odpovídajícími metadaty, vznikne také návrh
desek `app-desky.pdf`. Archivace (výsledné) práce je možné provést zavoláním
`make archive`, čímž vznikne archiv `app.tar.gz` obsahující čistý TeXový kód
a&nbsp;výsledné PDF.
