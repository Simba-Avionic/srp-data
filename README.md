# srp-data
Repozytorium zawiera dane z testów zebrane przez SimBa

# R7:

## Static 21.03.2026
| Konfiguracja Systemu | Parametry Operacyjne | Wyniki Silnikowe |
| :--- | :--- | :--- |
| **Soft:** [v0.2.0](https://github.com/Simba-Avionic/srp/releases/tag/v0.2.0) | **Utleniacz:** 9.7 kg $N_2O$ | **$I_{tot}$:** 22 629.98 Ns |
| **Hardware:** Engine Board | **Ciśnienie:** 55 Bar | **Max Thrust:** 5000 N |
| **Próbkowanie Tensobelki:** 320 Hz | **Temp. Otoczenia:** 12°C | **Burn Time:** 8 s |
| **Próbkowanie Ciśnienia:** 200Hz | **Odpalenie:** GS Control Panel | |


| Analiza Ciśnienia | Analiza Ciągu |
|:---:|:---:|
| ![Tank And Chamber Pressure Chart](/2026_03_21_static/charts/static_21_03_2026.png) | ![Thrust Chart](/2026_03_21_static/charts/thrust_21_03_2026.png) |

### Post-Mortem
- Posiadanie na test 1 szt elektroniki to znacznie za mało
- Trzeba przygotowywać timeline operacji i lepiej dbać o komunikacje
- Silnik dalej ma problemy ze spalaniem
- Warto używać tych samych definicji mavlink na wszystkich urządzeniach
- Zapraszamy znacznie mniej osób na testy
- 1.5s między zapłonem a otwarciem zaworu to znacząco za dużo -> zmniejszamy do 1s

| Name | Link |
|:---:|:---:|
| Nagrania GS | https://drive.google.com/drive/folders/1AGRGQf30OjB5krCccZ41o4zvRlFLRCa3 |
| Zdjęcia | https://drive.google.com/drive/folders/1ha7BySZP3P9nL3pT8ho_HKYNsEz_x-fi?usp=sharing |
| Dane GS | https://drive.google.com/drive/folders/17EoyJrxY-R3s7VpP74ydGx4Yyb9mqma4 |

-----------------------

## Static 21.02.2026
| Konfiguracja Systemu | Parametry Operacyjne | Wyniki Silnikowe |
| :--- | :--- | :--- |
| **Soft:** [v0.1.0](https://github.com/Simba-Avionic/srp/releases/tag/v0.1) | **Utleniacz:** 5.1 kg $N_2O$ | **$I_{tot}$:** unknown |
| **Hardware:** DevBoard | **Ciśnienie:** 50 Bar | **Max Thrust:** 5000 N |
| **Próbkowanie Tensobelki:** 320 Hz | **Temp. Otoczenia:** 7°C | **Burn Time:** unknown |
| **Próbkowanie Ciśnienia:** 10Hz | **Odpalenie:** srp-app | |


| Analiza Ciśnienia | Analiza Ciągu |
|:---:|:---:|
| ![Tank And Chamber Pressure Chart](/2026_02_21_static/charts/static_21_02_2026.png) | ![Thrust Chart](/2026_02_21_static/charts/thrust_21_02_2026.png) |

### Post-Mortem
- Trzeba zwiększyć częstotliwość próbkowania ciśnienia aby zobaczyć oscylacje
- Silnik ma nierówne spalanie -> zmniejszenie proporcji paliwa do utleniacza
- Warto by lepiej mocować połączenie tensobelki aby nie stracić danych po 2s
- 2s między zapłonem a otwarciem zaworu to znacząco za dużo -> zmniejszamy do 1.5s

| Name | Link |
|:---:|:---:|
| Nagrania GS | https://drive.google.com/drive/folders/15RPaZ5ydAYWAkqbo0ocqHZPF6PtVwEi4 |
| Nagrania Telefon | https://drive.google.com/drive/folders/1-hqclorNGLzYF2rBlWpgVt7yDxVAMdAb |
| Dane GS | https://drive.google.com/drive/folders/1qZy7ktI1JaxVaSpvzJJgnKRyEVECuHN2 |

-----------------------


## Test Hydrostatyczny 12.12.2025

| Test | Ciśnienie  | Czas|
| :--- | :--- | :--- |
| Zbiornik | 105 Bar | 5 min |
| Komora | 60 Bar | 5 min|

![Hydrotsatic  Tank Pressure](/2026_12_12_hydrostatic/charts/2025_12_12_hydrostatic.png)

### Post-Mortem
- To że wskazania z czujników zgadzają się dla 1 Bar nie znaczy że czujnik działa
- Kabelki lutowane na kolanie lubią przerywać i szumić choć i tak nie jest źle

| Name | Link |
|:---:|:---:|

-----------------------
