# Static 21.02.2026

## Konfiguracja i Wyniki

| Konfiguracja Systemu | Parametry Operacyjne | Wyniki Silnikowe |
| :--- | :--- | :--- |
| **Software:** [v0.1.0](https://github.com/Simba-Avionic/srp/releases/tag/v0.1) |  **Utleniacz:** 5.1kg \\( N_2O \\) ± 200g | **\\( I_{tot} \\):** unknown |
| **Hardware:** [DevBoard](../../../common/DevBoard_schematic.pdf) | **Ciśnienie:** 50Bar | **Max Thrust:** 5000N |
| **Próbkowanie Tensobelki:** 320Hz | **Temp. Otoczenia:** 7°C | **Burn Time:** unknown |
| **Próbkowanie Ciśnienia zbiornika:** 10Hz | **Odpalenie:** srp-app | |
| **Próbkowanie Ciśnienia komory:** 10Hz | **Paliwo:** parafina + czarny barwnik do świec | |

### Wewnętrzny układ komory spalania
![Przekrój komory spalania](static_1_CombustionChamber.JPG)

## Wykresy 

![Tank And Chamber Pressure Chart](pressure.png)
![Thrust Chart](thrust.png) 

## Post-Mortem

### Komora spalania

![Postmortem ziarna komory spalania](static_1_postmortem_grain.png)

Po spalaniu ziarno było bardzo porowate, dwa możliwe powody:
1. Ziarno miało duże porowatości po odlewaniu
2. Ziarno zbytnio się topiło i zaczęły odlatywać większe stopione kawałki parafiny

Silnik miał bardzo nierówne spalanie, bardzo go dusiło i generował wiele czadu. Powodem duszenia był za duży udział paliwa w spalaniu, dlatego należało zmniejszyć regresję (szybkość wypalania) ziarna. 

Aby osiągnąć mniej paliwa w spalaniu postanowiono zmienić mieszankę ziarna na 84% parafina, 15% hotglue, 1% sadza. Powinno to również poprawić sytuację, jeżeli powód 2. porowatości po spalaniu jest tym prawdziwym. 
Aby osiągnać mniej porowate postanowiono dodatkowo zastosować w procesie odlewania próżnię.
Dla polepszenia spalania postanowiono dodać mixer pomiędzy ziarnem i post combustion chamber.

### Reszta wniosków
- Trzeba zwiększyć częstotliwość próbkowania ciśnienia, aby zobaczyć oscylacje
- Warto by lepiej mocować połączenie tensobelki, aby nie stracić danych po 2s -> brakowało śrubek mocujących złącze
- 2s między zapłonem a otwarciem zaworu to znacząco za dużo -> zmniejszamy do 1.5s

## Materiały

| |
|:---:|
[Nagrania GS](  https://drive.google.com/drive/folders/15RPaZ5ydAYWAkqbo0ocqHZPF6PtVwEi4)
[Nagrania Telefon ](  https://drive.google.com/drive/folders/1-hqclorNGLzYF2rBlWpgVt7yDxVAMdAb)
[Dane GS ](  https://drive.google.com/drive/folders/1qZy7ktI1JaxVaSpvzJJgnKRyEVECuHN2)

-----------------------