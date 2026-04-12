import matplotlib.pyplot as plt

INPUT_FILE = "static3_FIRE.txt"
OUTPUT_FILE = "FINAL_combined_static_fire.png"

ENG_OUTPUT_FILE = "R7_static_fire_3_filtr_sav_gol_21_3.eng"

# INPUT_FILE = "cold1_FLOW_wyciete.txt"
# OUTPUT_FILE = "FINAL_combined_cold1_flow.png"

# ENG_OUTPUT_FILE = "R7_cold_flow_1_filtr_sav_gol_21_3.eng"

WSP_B = -563            # wartość z tenso wzorcowej, która odpowiada 0 kg
WSP_A = 0.04521833745   # współczynnik kalibracji, wyznaczony za pomocą metody najmniejszych kwadratów z danych z tensobelki wzorcowej

TIMESTAMP_OFFSET_MICROS_ARDUINO = 144129096  # korekta offsetu czasowego (w milisekundach) między Arduino a rzeczywistym czasem, jeśli jest znana, tylko dla aspektów wizualnych

SR_KR_OKNO = 10           # liczba punktów do obliczenia średniej kroczącej
SAVGOL_WINDOW = 21           # liczba punktów do obliczenia filtru Savitzky-Golay (musi być nieparzysta)
SAVGOL_ORDER = 3             # rząd wielomianu dla filtru Savitzky-Golay


def save_as_eng_file(seconds, newtons, filename_out):
    with open(filename_out, "w", encoding="utf-8") as file_out:
        first_time = seconds[0]
        file_out.write("Majda-2 140 1950 P 20.0 34.0 SimLE_SimBa")
        for sec, newton in zip(seconds, newtons):
            time_sec = (sec - first_time)  # czas w sekundach od pierwszego pomiaru
            file_out.write(f"\n{time_sec:.6f} {newton:.3f}")

# # === LICZENIE IMPULSU (metoda trapezów) ===
# impuls = 0.0
# impuls_values.append(0.0)

# for i in range(1, len(x_values)):
#     dt = x_values[i] - x_values[i-1]
    
#     # możesz zmienić na y_values jeśli chcesz bez wygładzania
#     f1 = y_values_srednia_kroczaca[i-1]
#     f2 = y_values_srednia_kroczaca[i]
    
#     pole = (f1 + f2) / 2 * dt
#     impuls += pole
    
#     impuls_values.append(impuls)

# print(f"Impuls całkowity: {impuls:.2f} Ns")

def impuls_trapezy(x, y):
    impuls = 0.0
    impuls_values = [0.0]

    for i in range(1, len(x)):
        dt = x[i] - x[i-1]
        f1 = y[i-1]
        f2 = y[i]
        pole = (f1 + f2) / 2 * dt
        impuls += pole
        impuls_values.append(impuls)

    return impuls_values
    # return impuls

timestamps_second = []
x_values_micros = []
y_values = []
y_values_srednia_kroczaca = []
suma_surowych = 0
suma_surowych_count = 0
maks_ciag_surowe = -float("inf")
maks_ciag_filtr = -float("inf")

debug_i = 0

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        
        line = line.strip()
        if not line:
            continue
        
        try:
            # 2026-03-21 14:02:18.743179 | 2105756 -599
            parts = line.split("|")
            parts_new = parts[1].split()

            # filtracja bitów - zakładam, że dane są w formacie 32-bitowym i chcę wyzerować najmłodsze bity, aby zredukować szum
            x = 0  # Number of bits to zero out
            raw_int = int(parts_new[1].strip())

            suma_surowych += raw_int
            suma_surowych_count += 1

            zeroed_int = (raw_int >> x) << x
            value = float(zeroed_int) - WSP_B

            # value = float(parts_new[1].strip()) - WSP_B # odjęcie wartości z tenso wzorcowej

            # y_values.append(value * WSP_A)  # przemnożenie przez współczynnik kalibracji
            ciag_N = value * WSP_A * 9.80665
            y_values.append(ciag_N) # ciąg w Newtonach

            if ciag_N > maks_ciag_surowe:
                maks_ciag_surowe = ciag_N

            x_values_micros.append(((int(parts_new[0].strip())-TIMESTAMP_OFFSET_MICROS_ARDUINO)/1000000))  # konwersja z mikrosekund na sekundy

            # srednia krocząca
            if len(y_values) >= SR_KR_OKNO:
                srednia = sum(y_values[-SR_KR_OKNO:]) / SR_KR_OKNO
                y_values_srednia_kroczaca.append(srednia)
            else:
                y_values_srednia_kroczaca.append(value * WSP_A * 9.80665)  # dla pierwszych 9 punktów, gdy nie ma jeszcze 10 wartości

        except (IndexError, ValueError):
            continue


if not y_values:
    print("Brak poprawnych danych w pliku.")
    exit()

# print avg surowych
if suma_surowych_count > 0:
    avg_surowych = suma_surowych / suma_surowych_count
    print(f"Średnia wartość surowych danych: {avg_surowych:.2f}")

from scipy.signal import savgol_filter

print(f"Zastosowanie filtru Savitzky-Golay: window_length={SAVGOL_WINDOW}, polyorder={SAVGOL_ORDER}")
y_values_savgol = savgol_filter(y_values, window_length=SAVGOL_WINDOW, polyorder=SAVGOL_ORDER)
print("Filtr Savitzky-Golay zastosowany pomyślnie.")

print("IMPLUS całkowity (średnia krocząca): {:.2f} Ns".format(impuls_trapezy(x_values_micros, y_values_srednia_kroczaca)[-1]))
print("IMPLUS całkowity (filtr Savitzky-Golay): {:.2f} Ns".format(impuls_trapezy(x_values_micros, y_values_savgol)[-1]))
print("IMPLUS całkowity (dane surowe): {:.2f} Ns".format(impuls_trapezy(x_values_micros, y_values)[-1]))

save_as_eng_file(x_values_micros, y_values_savgol, ENG_OUTPUT_FILE)

if maks_ciag_surowe > -float("inf"):
    print(f"Maksymalny ciąg (surowe): {maks_ciag_surowe:.2f} N")

# wyznaczenie maksymalnego ciagu z danych po filtrze Savitzky-Golay
for ciag in y_values_savgol:
    if ciag > maks_ciag_filtr:
        maks_ciag_filtr = ciag
if maks_ciag_filtr > -float("inf"):
    print(f"Maksymalny ciąg (filtr Savitzky-Golay): {maks_ciag_filtr:.2f} N")

impuls_values = impuls_trapezy(x_values_micros, y_values_savgol)
impuls_total = impuls_values[-1]

# === USTAWIENIA JAKOŚCI ===
fig, ax1 = plt.subplots(figsize=(16,9))

# --- wykres ciągu ---
line1, = ax1.plot(x_values_micros, y_values, linewidth=0.3, label="Dane surowe")
line2, = ax1.plot(x_values_micros, y_values_savgol, "g-", linewidth=1.0, label="Filtr Savitzky-Golay")

ax1.set_xlabel("Czas [s]", fontsize=14)
ax1.set_ylabel("Ciąg [N]", fontsize=14)

# --- druga oś (impuls) ---
ax2 = ax1.twinx()

line3, = ax2.plot(x_values_micros, impuls_values, "r--", linewidth=1.5, label="Impuls całkowity [Ns]")

# pozioma linia końcowego impulsu
line4 = ax2.axhline(
    impuls_total,
    linestyle=":",
    linewidth=2,
    label=f"Impuls końcowy = {impuls_total:.1f} Ns"
)

ax2.set_ylabel("Impuls [Ns]", fontsize=14)

# --- wspólna legenda ---
lines = [line1, line2, line3, line4]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, fontsize=12, loc="best")

plt.title("Ciąg silnika na hamowni + impuls całkowity", fontsize=16)

plt.grid(True)
plt.tight_layout()

# zapis
plt.savefig(OUTPUT_FILE, dpi=600)

print(f"Wykres zapisany jako: {OUTPUT_FILE}")