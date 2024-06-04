**Verze pro Microsoft Word**

[Přímo ke stažení zde jako `kp-app.dotx`](./kp-app.dotx?raw=true). Nepoužívejte
v&nbsp;jiných programech, není pro ně stavěná.

**Tato šablona byla po minimálních úpravách úspěšně použita i&nbsp;pro**
* UK FF
* HAMU
* UHK PdF

**Jiné poznámky**

Dodatečná šablona pro pevné desky ([`kp-app-desky.dotx`](./kp-app-desky.dotx?raw=true)) je
pouze orientační! Pouze při&nbsp;požadavku na&nbsp;vlastní zlatotisk (třeba
s&nbsp;logem školy) odevzdejte jako plně vektorové PDF.

Aby zůstala zachována funkčnost šablony i v uložených na ní založených
dokumentech, je potřeba je ukládat ve formátu Microsoft OOXML (přípona `.docx`),
nikoliv jako ODF (soubory `.odt`). Tato volba se provádí při prvním spuštění MS
Office a jde později změnit v nabídce Soubor-Možnosti-Ukládání. Případně lze
každý soubor explicitně uložit do formátu v nabídce podporovaných typů.
![Uložení souboru jako `.docx`](https://github.com/jhlade/KP-APP/blob/assets/editory/msword-docx.png?raw=true)

**Přehled hlavních definovaných stylů**

* `Základní text` - tímto stylem jsou psány všechny odstavce vlastního textu
práce (nepoužíváme styl `Normální` kvůli konfliktům, ale třeba se to časem povede
srovnat)
* `1-Nadpis` - hlavní nadpis kapitoly, vždy začíná na nové stránce, pod tímto
nadpisem *musí* být vždy umístěn stručný odstavec textu s&nbsp;úvodem do dané
kapitoly
* `2-Podnadpis` - nadpis podkapitoly, hlavní jednotka členění práce
* `3-Pod-pod-nadpis` - třetí úroveň nadpisu pro&nbsp;jemnější členění práce
* `4-pod-pod-pod-nadpis` - čtvrtá úroveň - *víceméně nepoužívat, tento nadpis
nebude umístěn v&nbsp;obsahu*
* `1-Nadpis pro přílohy` - hlavní nadpis pro přílohy, číslování pomocí velkých
písmen abecedy, nadpisy budou zahrnuty v&nbsp;obsahu *Seznam příloh*
* `1-Nadpis bez čísla` - povinné nečíslované nadpisy Úvod, Závěr, Literatura
* `2-Podnadpis bez čísla` - *nepoužívat mimo Úvod nebo Seznam literatury*,
typické použití je pro&nbsp;jemnější členění *Úvodu*, kde se může samostatně
nacházet *Motivace*, *Stav bádání* apod.
* `Vlastní seznam literatury` - upravený seznam s oddělenými odstavci
pro&nbsp;uvedení jednotlivých citovaných položek
* dále existují nadpisy bez zařazení do obsahu - tyto nadpisy tedy nebudou
zobrazeny v hlavním obsahu práce