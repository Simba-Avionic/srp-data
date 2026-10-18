# Static 15.10.2026

## Konfiguracja i Wyniki
| Konfiguracja Systemu | Parametry Operacyjne | Wyniki Silnikowe |
| :--- | :--- | :--- |
| **Hardware:** [Engine Computer](../../../common/EngineComputer_schematic.pdf) | **Utleniacz:** 9.7 kg \\( N_2O \\) ± 200g | **\\( I_{tot} \\):** 20222.9512 Ns |
| **Próbkowanie Ciśnienia zbiornika:** 10Hz | **Ciśnienie:** 52Bar | **Max Thrust:** 4750.7N |
| | **masa (wypalonego) paliwa:** 2.323 kg | |

<!--
| **Software:** [v0.3.0](https://github.com/Simba-Avionic/srp/releases/tag/v0.3.0) | | |
| **Próbkowanie Tensobelki:** 320Hz | **Temp. Otoczenia:** 10°C | **Burn Time:** 10s |
| **Próbkowanie Ciśnienia komory:** 166Hz | **Paliwo:** 84% parafina, 15% hotglue, 1% sadza | |
-->


## Wykresy 

### Wykres cisnienia Zbiornika i Komory

#### Cały  test

<div class="interactive-chart" data-chart="pressure.plot.json" data-title="Tank Pressure Chart (All)">
<details class="chart-fallback" open><summary>Archiwalny obraz PNG</summary>

![Tank And Chamber Pressure Chart](pressure.png)

</details>
</div>

#### Start

<div class="interactive-chart" data-chart="pressure_zoom.plot.json" data-title="Tank Pressure (Launch)">
<details class="chart-fallback" open><summary>Archiwalny obraz PNG</summary>

![Tank And Chamber Pressure Zoom](pressure_zoom.png)

</details>
</div>

### Wykres ciągu
<div class="interactive-chart" data-chart="thrust.plot.json" data-title="Thrust Chart">
<details class="chart-fallback" open><summary>Archiwalny obraz PNG</summary>

![Thrust Chart](thrust.png)

</details>
</div>

## Post-Mortem

### Reszta wniosków
- Nawet składając te samą rakietę 4 raz bez checklisty zdarzają się błędy
- Projekt TestBox jest super inicjatywą
- Zmniejszenie ciśnienia w komorze (poprzez rozszerzenie gardła dyszy) zmniejszyło amplitudę niestabilności spalania, ale nie wygłuszyło ich całkowicie
- Znacznie zmniejszyła się wydajność silnika (<180s ISP), co było spodziewane
- Średnie OF ~= 4.3


## Materiały

|  |
|:---:|
| [Zdjęcia & Nagrania](https://drive.google.com/drive/folders/1318bVYpF_e5ZVnfPuNZcweQkrWOe7sXs)
| [Dane GS]( https://drive.google.com/drive/folders/1lCE797Zv3mZs0NX4CaekcU8_AeBpV8zL)

