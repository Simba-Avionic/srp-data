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

| Name | Link |
|:---:|:---:|
| Nagrania GS | https://drive.google.com/drive/folders/15RPaZ5ydAYWAkqbo0ocqHZPF6PtVwEi4 |
| Nagrania Telefon | https://drive.google.com/drive/folders/1-hqclorNGLzYF2rBlWpgVt7yDxVAMdAb |
| Dane GS | https://drive.google.com/drive/folders/1qZy7ktI1JaxVaSpvzJJgnKRyEVECuHN2 |

-----------------------