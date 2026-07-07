# srp-data

Repozytorium danych i dokumentacji testów rakiet SimLE SimBa.

Dokumentacja jest publikowana jako [mdBook na GitHub Pages](https://simba-avionic.github.io/srp-data/).

## Struktura

```
srp-data/
├── src/              # dokumentacja mdBook (wykresy, raporty testów)
│   ├── SUMMARY.md    # spis treści
│   └── R7/           # rakieta R7
│       ├── README.md
│       ├── common/   # schematy wspólne
│       └── tests/    # raporty per test
├── data/             # surowe dane testów
│   └── R7/
│       └── <typ>/YYYY-MM-DD/
│           ├── gs/   # Ground Station (hamownia, tenso)
│           └── sw/   # Software (logi telemetrii)
├── scripts/          # skrypty analizy danych
└── _templates/       # szablony nowych rakiet i testów
```

## Konwencje nazewnictwa

| Element | Format | Przykład |
|---------|--------|----------|
| Rakieta | `R` + numer lub nazwa | `R7`, `Liquid-Rurku` |
| Data testu | ISO `YYYY-MM-DD` | `2026-03-21` |
| Typ testu | `static`, `cold-flow`, `hydro`, `launch`, `combustion-chamber` | `cold-flow` |

## Dodawanie nowej rakiety

1. Skopiuj `_templates/rocket/` → `src/RX/` i `data/RX/`
2. Uzupełnij `src/RX/README.md`
3. Dodaj wpis w `src/SUMMARY.md`

## Dodawanie nowego testu

1. Skopiuj `_templates/test/README.md` do `src/RX/tests/<typ>/YYYY-MM-DD/`
2. Dodaj surowe dane do `data/RX/<typ>/YYYY-MM-DD/gs/` i `sw/`
3. Wygeneruj wykresy i skopiuj PNG do katalogu raportu w `src/`
4. Dodaj wpis w `src/SUMMARY.md`

## Analiza danych GS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd data/R7/static/2026-03-21/gs
python ../../../../../scripts/gs/wyniki_savgol.py \
  --input static2_FIRE_wyciety_test_enginowane.txt \
  --output thrust.png
```

Szczegóły: [scripts/gs/README.md](scripts/gs/README.md).

## Lokalny podgląd dokumentacji

```bash
mdbook serve
```
