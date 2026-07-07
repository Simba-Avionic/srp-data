# Skrypty Ground Station

Skrypty do analizy logów z hamowni (tensobelka, ciśnienie).

## Wymagania

```bash
pip install -r ../../requirements.txt
```

## wyniki_savgol.py

Główny skrypt analizy ciągu — filtr Savitzky-Golay, impuls całkowity, wykres PNG, opcjonalnie plik `.eng`.

Uruchamiaj z katalogu danych testu (`data/RX/<typ>/YYYY-MM-DD/gs/`):

```bash
python ../../../../../scripts/gs/wyniki_savgol.py \
  --input static2_FIRE_wyciety_test_enginowane.txt \
  --output thrust.png \
  --eng-output R7_static_fire_2_filtr_sav_gol_21_3.eng
```

Parametry kalibracji tensobelki (`--wsp-a`, `--wsp-b`) zależą od testu — sprawdź arkusz kalibracji lub poprzednie analizy.

## Pozostałe skrypty

| Skrypt | Opis |
|--------|------|
| `gif_maker.py` | Generowanie animacji GIF z klatek wykresu |
| `wyniki_legacy.py` | Prostsza analiza bez filtra SG (archiwum) |
| `wyniki_impuls_calkowity.py` | Wykres ciągu i impulsu (archiwum) |
| `timestampy.py` | Debug osi czasu na wykresie |
| `tworzenie_anonimowanego_wykresu.py` | Wykres bez metadanych |
| `wzorcowe_usrednianie.py` | Uśrednianie logów wzorcowych kalibracji |
