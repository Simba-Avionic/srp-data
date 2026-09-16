# Interaktywne wykresy mdBook

Wykresy korzystają z lokalnego Plotly.js **basic 3.7.0** (MIT). Zoom,
przesuwanie, legenda, odczyty kursora i eksport PNG działają bez serwera
obliczeniowego i bez CDN. Dane są ładowane dopiero przy przewinięciu do wykresu.
Kontrolki serii są dostępne także z klawiatury. Obrazy archiwalne pozostają
w rozwijanej sekcji, przy wyłączonym JS i na wydruku.

## Dlaczego Plotly

- [Plotly: konfiguracja](https://plotly.com/javascript/configuration-options/):
  gotowe zoom/pan/reset/eksport i responsywność.
- [Legenda i zdarzenia](https://plotly.com/javascript/plotlyjs-events/):
  kliknięcie ukrywa serię, dwuklik izoluje ją.
- [Pakiety częściowe](https://github.com/plotly/plotly.js/blob/v3.7.0/dist/README.md):
  wystarczy basic, około 1.1 MB, współdzielony przez wszystkie nowe wykresy.
- [mdBook additional-js/css](https://rust-lang.github.io/mdBook/format/configuration/renderers.html):
  integracja bez dodatkowego preprocesora i zmian sposobu publikacji.
- Rozważony [Chart.js + zoom](https://www.chartjs.org/chartjs-plugin-zoom/latest/guide/integration):
  wymaga dodatkowego pluginu. Plotly ma wymagane interakcje w jednym pakiecie
  i jest już używane w istniejącym raporcie lotu.

## Odtwarzanie i sprawdzanie

```bash
python3 scripts/charts/generate.py
python3 scripts/charts/generate.py --check
python3 -m unittest discover -s tests -v
mdbook build
mdbook serve
```

Generator wymaga wyłącznie standardowej biblioteki Pythona. Pliki `*.plot.json`
są wersjonowane, więc zwykłe `mdbook build` wystarcza, również bez Pythona.
CI sprawdza zgodność JSON ze źródłami oraz interakcje w Chromium przed publikacją.

Testy interakcji (w drugim terminalu przy serwowaniu `book` na porcie 8765):

```bash
npm install --prefix /tmp/srp-browser playwright@1.63.0
/tmp/srp-browser/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/srp-browser/node_modules node tests/charts-browser.cjs
```

Inny adres: zmienna `CHARTS_URL`. Testy sprawdzają wszystkie 11 wykresów,
blokują zewnętrzną sieć, sprawdzają legendę, zoom prostokątem, pan, reset,
kontrolki serii, powiększenie, zoom kółkiem, odczyty kursora, eksport PNG, wydruk, szerokość mobilną i fallback. Zrzuty ekranu
powstają w `/tmp/srp-charts-{desktop,mobile}.png`.

## Pochodzenie i ograniczenia danych

- R7 marzec/kwiecień: ciśnienie `/100`, przesunięcia czasu i średnie kroczące
  zgodne z notebookami. Widoki oscylacji zachowują wszystkie próbki, bez
  wygładzania; mają wspólną oś sekund od początku okna testu.
- R7 luty: wartości bar z komunikatów DLT, forward fill i średnia zbiornika
  15 próbek zgodnie z notebookiem. Nie powielamy mylącej etykiety psi z jego
  wcześniejszej komórki.
- Ciąg marzec/kwiecień/cold-flow: istniejące eksporty `.eng`, bez zgadywania
  kalibracji i bez ponownego filtrowania. Impuls obliczany metodą trapezów.
  Eksporty mają już zaokrąglone próbki, więc całka może nieznacznie różnić
  się od raportu liczonego przed eksportem.
- Liquid cold-flow: okno notebooka 340–380 s. Zapisanej korekty pressure feed
  nie stosujemy ponownie; notebook nie potwierdza jednostki, co opisujemy na
  wykresie.
- Liquid static: oba pełne logi aplikacji, bo brak receptury okna archiwalnego
  PNG. Powtórzony nagłówek CSV jest pomijany, przerwy rejestracji >5 s nie są
  łączone linią. Czas jest liczony od początku każdego logu oddzielnie.
- Hydro oraz ciąg R7 z lutego pozostają obrazami: brak źródła hydro i pliku
  `hamownia_log_j.txt` używanego przez skrypt lutowy. Nie digitalizujemy PNG.
- Usunięto odwołania do nieistniejących wykresów ciśnienia R7 cold-flow oraz
  ciągu Liquid cold-flow, zastępując je opisem braku danych.
- Raport lotu ma już własny samodzielny interaktywny Plotly HTML; pozostaje
  osobnym raportem.

## Dodawanie wykresu

Dodaj deterministyczne przeliczenie w `generate.py`, jawne źródło i jednostki,
wygeneruj JSON i osadź go obok PNG:

```html
<div class="interactive-chart" data-chart="pressure.plot.json" data-title="Ciśnienie">
<details class="chart-fallback" open><summary>Archiwalny obraz PNG</summary>

![Ciśnienie](pressure.png)

</details>
</div>
```

Nie umieszczaj komponentu w tabeli. Zostaw puste linie wokół Markdown wewnątrz
HTML. Wartości niedostępne zapisuj jako `null`, nigdy `NaN` ani zero.

## Biblioteka

Źródło: https://cdn.plot.ly/plotly-basic-3.7.0.min.js

SHA-256: `c23b03591a6bdad0bd0f47a0c5c52305a5519812b73ce254be65cd841553c9c2`.
Licencja: `src/vendor/plotly-LICENSE`. Przy aktualizacji zmień nazwę pliku,
ścieżkę w `theme/charts.js`, hash oraz uruchom testy przeglądarkowe.
