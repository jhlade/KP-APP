Šablona je připravena pro [XeLaTeX](https://www.tug.org/texlive/) a&nbsp;[Biber](https://biblatex-biber.sourceforge.net/),
sazba předpokládá alespoň základní orientaci v&nbsp;syntaxi LaTeXu.

**Organizace**
* `metadata.tex` - prostředí s&nbsp;proměnnými daty, zde vyplníte jména, název
práce, klíčová slova, a&nbsp;další
* `app.tex` - základní dokument s&nbsp;členěním celé práce, při výchozím použití
do něj není nutné zasahovat
* `app-desky.tex` - samostatný dokument s&nbsp;deskami práce
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

Oba hlavní dokumenty (`app.tex` i&nbsp;`app-desky.tex`) mají na&nbsp;prvním řádku
direktivu `% !TeX program = xelatex` - editory a&nbsp;Overleaf díky ní automaticky
zvolí správný překladač bez ručního nastavení.

---

## Overleaf

Nejjednodušší způsob, jak práci rozpracovat bez instalace čehokoliv lokálně.

[![Open in Overleaf](https://img.shields.io/badge/Open%20in-Overleaf-47A141?style=for-the-badge&logo=overleaf&logoColor=white)](https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Fjhlade%2FKP-APP%2Ftex%2FTeX%2Fapp.zip)

Tlačítko naimportuje aktuální [`app.zip`](./app.zip?raw=true) přímo z&nbsp;větve
`tex` jako nový Overleaf projekt. Pokud tlačítko nefunguje (např. po&nbsp;sloučení
do&nbsp;jiné větve, kde se cesta/název větve změní), postupujte manuálně:

1. Stáhněte si zazipovaný projekt - buď přímo [`app.zip`](./app.zip?raw=true),
nebo si lokálně (pokud máte TeXLive/MacTeX) vytvořte čerstvý zip příkazem
`make archive-zip`.
2. V&nbsp;Overleaf zvolte **New Project → Upload Project** a&nbsp;nahrajte
výsledný `.zip`.
3. Projekt obsahuje dva nezávislé hlavní dokumenty - `app.tex` (text práce)
a&nbsp;`app-desky.tex` (desky). V&nbsp;Overleaf přes **Menu → Main document**
zvolte, který z&nbsp;nich se má aktuálně kompilovat.
4. Díky `% !TeX program = xelatex` na&nbsp;prvním řádku obou dokumentů Overleaf
sám nastaví překladač na&nbsp;XeLaTeX a&nbsp;biblatex/Biber se autodetekuje
z&nbsp;`\usepackage[backend=biber]{biblatex}` v&nbsp;`sablona.tex` - žádné
další ruční nastavení v&nbsp;Menu nepotřebujete.

---

## Lokální překlad - macOS (MacTeX) a&nbsp;Linux (TeXLive)

Na&nbsp;obou systémech se používá stejný `Makefile` a&nbsp;stejné nástroje
(`xelatex`, `biber`, standardní shellové utility).

**Instalace**
* macOS: [MacTeX](https://www.tug.org/mactex/) (obsahuje XeLaTeX i&nbsp;Biber,
binárky se automaticky přidají do&nbsp;PATH přes `/Library/TeX/texbin`).
* Linux: TeXLive, minimálně balíčky `texlive-xetex`, `texlive-lang-czech`
a&nbsp;`biber` (případně `texlive-bibtex-extra`); pro plnou sadu balíčků lze
použít `texlive-full`. Distribuci lze i&nbsp;dockerizovat z&nbsp;oficiálního
obrazu `texlive/texlive`.

**Použití Makefile**<br>
Překlad do&nbsp;PDF lze zajistit jednoduchým zavoláním `make`, konečný výsledek
bude uložen jako `app.pdf` s&nbsp;odpovídajícími metadaty, vznikne také návrh
desek `app-desky.pdf`.

* `make` - přeloží práci i&nbsp;desky a&nbsp;uklidí dočasné soubory
* `make open` - otevře `app.pdf` ve&nbsp;výchozím prohlížeči (macOS `open`,
Linux `xdg-open`)
* `make archive` - vytvoří archiv `app.tar.gz` s&nbsp;čistým TeXovým kódem
a&nbsp;výslednými PDF
* `make archive-zip` - vytvoří `app.zip` se&nbsp;stejným obsahem, vhodný
pro&nbsp;přímý upload do&nbsp;Overleaf
* `make clean` / `make softclean` - smazání produktů, resp. jen dočasných
souborů
* `make help` - výpis všech dostupných cílů s&nbsp;popisem

---

## Windows (TeXLive nebo&nbsp;MiKTeX)

Samotný překlad přes `xelatex`/`biber` na&nbsp;Windows funguje stejně jako
na&nbsp;macOS/Linuxu (obě distribuce - [TeXLive](https://www.tug.org/texlive/)
i&nbsp;[MiKTeX](https://miktex.org/) - tyto nástroje obsahují). Samotný
**`Makefile` ale na&nbsp;čistém Windows (cmd/PowerShell) nepůjde spustit**,
protože vyžaduje `make`, `rm` a&nbsp;`tar`, které tam nativně nejsou.

**Možnost A - spustit Makefile**<br>
Doinstalujte prostředí s&nbsp;Unixovými nástroji a&nbsp;GNU Make:
* [WSL](https://learn.microsoft.com/cs-cz/windows/wsl/) (doporučeno,
fakticky Linux pod Windows) - v&nbsp;něm postupujte podle sekce výše,
* nebo Git Bash / [MSYS2](https://www.msys2.org/) s&nbsp;doinstalovaným
`make`.

**Možnost B - bez Makefile**<br>
Spusťte příkazy přímo v&nbsp;příkazové řádce TeXLive/MiKTeX:
```
xelatex app
biber app
xelatex app
xelatex app
```
a&nbsp;pro desky `xelatex app-desky`.

**Možnost C - GUI editor**<br>
Otevřete `app.tex` (nebo `app-desky.tex`) v&nbsp;editoru jako
[TeXstudio](https://www.texstudio.org/) nebo MiKTeX Console - direktiva
`% !TeX program = xelatex` na&nbsp;prvním řádku zajistí automatickou volbu
správného překladače.
