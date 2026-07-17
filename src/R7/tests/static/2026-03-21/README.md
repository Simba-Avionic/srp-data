# Static 21.03.2026

## Konfiguracja i Wyniki

| Konfiguracja Systemu | Parametry Operacyjne | Wyniki Silnikowe |
| :--- | :--- | :--- |
| **Software:** [v0.2.0](https://github.com/Simba-Avionic/srp/releases/tag/v0.2.0) | **Utleniacz:** 9.7kg \\( N_2O \\) ± 200g | **\\( I_{tot} \\):** 22 629.98Ns |
| **Hardware:** [Engine Computer](../../../common/EngineComputer_schematic.pdf) | **Ciśnienie:** 55 Bar | **Max Thrust:** 5000N |
| **Próbkowanie Tensobelki:** 320Hz | **Temp. Otoczenia:** 12°C | **Burn Time:** 8s |
| **Próbkowanie Ciśnienia zbiornika:** 200Hz | **Odpalenie:** GS Control Panel |  |
| **Próbkowanie Ciśnienia komory:** 200Hz | **Paliwo:** 84% parafina, 15% hotglue, 1% sadza | |

### Wewnętrzny układ komory spalania
![Combustion Chamber Cross Section](static_2_CombustionChamber.JPG)

## Wykresy 

### Wykres cisnienia Zbiornika i Komory
![Tank And Chamber Pressure Chart](pressure.png)

### Przybliżenie na oscylacje Ciśnienia Zbiornika i Komory
![Tank And Chamber Pressure Zoom](pressure_zoom.png)

### Wykres ciągu
![Thrust Chart](thrust.png)

## Post-Mortem

### Komora spalania

![Postmortem mixera komory spalania](static_2_postmortem_mixer.png)
![Postmortem ścianki komory spalania](static_2_postmortem_bulge.png)

#### Jak wyglądała komora po teście
Podczas spalaniu ułamała się zewnętrzna część mixera, co spodowało jego wyrwanie i odkrycie bardzo cienkiej warstwy izolacji na działanie spalania. Izolacja ta się przepaliła, powodując nadmierne nagrzanie się aluminiowej ścianki, która straciła wytrzymałość i pod wpływem ciśnienia się wybrzuszyła. Dodatkowo widoczne było małe pęknięcie w miejsce wybrzuszenia.  
Ścianka nie była możliwa do wykorzystania jeszcze raz, należało wykonać nową.

#### Jak działał silnik
Silnik miał dużo lepsze spalanie, jego działanie nadal jest niestabilne, ale duszenie i gaszenie silnika jest widoczne dopiero w trakcie spalania fazy gazowej. Głównym powodem duszenia nadal był zbyt duży udział paliwa w spalaniu.  
Główny powód niestabilności silnika nieznany, zmniejszenie udziału paliwa może poprawić sytuację.

#### Co postanowiono zmienić
Aby uniknąć sytuacji wyłamania elementu, który odsłania cienką izolację, postanowiono zastosować w washerach i mixerze łączenia geometryczne z dwóch stron. Zwiększono również grubości washerów i mixera.  
Aby osiągnąć mniej paliwa w spalania postanowiono skrócić ziarno o 5cm (z 49cm na 44cm).

### Reszta wniosków
- Posiadanie na test 1 szt elektroniki to znacznie za mało
- Trzeba przygotowywać timeline operacji i lepiej dbać o komunikacje
- Warto używać tych samych definicji mavlink na wszystkich urządzeniach
- Zapraszamy znacznie mniej osób na testy
- 1.5s między zapłonem a otwarciem zaworu to znacząco za dużo -> zmniejszamy do 1s

## Materiały
|  |
|:---:|
| [Nagrania GS ](https://drive.google.com/drive/folders/1AGRGQf30OjB5krCccZ41o4zvRlFLRCa3)
| [Zdjęcia ](https://drive.google.com/drive/folders/1ha7BySZP3P9nL3pT8ho_HKYNsEz_x-fi?usp=sharing)
| [Dane GS ]( https://drive.google.com/drive/folders/17EoyJrxY-R3s7VpP74ydGx4Yyb9mqma4)
