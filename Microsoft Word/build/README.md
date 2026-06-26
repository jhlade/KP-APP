# Abs. práce – sestavení `.dotm` s ribbonem

## 1. Stage 1 – holý macro-enabled .dotm bez ribbonu

```sh
python3 "Microsoft Word/build/build_stage1.py"
```

Vznikne `Microsoft Word/build/out/kp-app_stage1.dotm`. Bez karty "Abs. práce".

## 2. Import makra ve Wordu (manuálně)

1. Otevře se `Microsoft Word/build/out/kp-app_stage1.dotm` ve Wordu.
2. `Alt+F11` → `File → Import File…` → vybere se
   `Microsoft Word/build/OptionalPagesRibbon.bas`.
   - Pokud import hodí `&H80004005`, `.bas` se zkopíruje na plochu a importuje se odtud.
3. `Debug → Compile VBAProject`.
4. VBA editor se zavře, uloží se (`Cmd+S`), formát **Word Macro-Enabled
   Template (.dotm)**, cíl `Microsoft Word/build/out/kp-app_stage2.dotm`
   (Save As).

## 3. Stage 2 – doplnění ribbonu

```sh
python3 "Microsoft Word/build/build_stage2.py" \
  "Microsoft Word/build/out/kp-app_stage2.dotm" \
  "Microsoft Word/build/out/kp-app.dotm"
```

Bez argumentů: vstup/výstup `kp-app_stage1.dotm`/`kp-app.dotm` v `out/`.

Výsledek: `Microsoft Word/build/out/kp-app.dotm`.

## Úprava roku v šabloně

```sh
python3 "Microsoft Word/build/update_date.py" ROK
```

Mění jen rok v polích "Rok" a "Datum prohlášení" – den/měsíc zůstává, jaký
je aktuálně v šabloně. Upravuje `kp-app.dotx` na místě, commit se provádí
manuálně.

## Strukturní příprava šablony (záložky volitelných bloků)

```sh
python3 "Microsoft Word/build/build_dotx_blocks.py"
```

Jednorázově vloží do `kp-app.dotx` záložky `OPT_BLANK_FRONT`,
`OPT_BLANK_BACK`, `OPT_THANKS`, `OPT_THANKS_ANCHOR` a koncový zalom stránky za
poděkováním. Makro (`OptionalPagesRibbon.bas`) detekuje stav výhradně přes
tyto záložky. Skript je idempotentní (pokud záložky existují, skončí bez
zápisu). Spouští se z čisté šablony; pokud je třeba znovu, nejdřív
`git checkout -- "Microsoft Word/kp-app.dotx"`, pak `update_date.py` a
`build_dotx_blocks.py`.

## Po ověření

Soubor `out/kp-app.dotm` (gitignored) se přesune do `Microsoft Word/kp-app.dotm`.
