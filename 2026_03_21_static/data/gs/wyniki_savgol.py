import matplotlib.pyplot as plt

INPUT_FILE = "static2_FIRE_wyciety_test_enginowane.txt"
OUTPUT_FILE = "../../charts/thrust_12_03_2026.png"

WSP_B = -666            # wartość z tenso wzorcowej, która odpowiada 0 kg
WSP_A = 0.04521833745   # współczynnik kalibracji, wyznaczony za pomocą metody najmniejszych kwadratów z danych z tensobelki wzorcowej

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
    # impuls_values = [0.0]

    for i in range(1, len(x)):
        dt = x[i] - x[i-1]
        f1 = y[i-1]
        f2 = y[i]
        pole = (f1 + f2) / 2 * dt
        impuls += pole
        # impuls_values.append(impuls)

    # return impuls_values
    return impuls

timestamps_second = []
x_values_micros = []
y_values = []
y_values_srednia_kroczaca = []

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        
        line = line.strip()
        if not line:
            continue
        
        try:
            # 2026-03-21 14:02:18.743179 | 2105756 -599
            parts = line.split("|")
            parts_new = parts[1].split()

            value = float(parts_new[1].strip()) - WSP_B # odjęcie wartości z tenso wzorcowej
            # y_values.append(value * WSP_A)  # przemnożenie przez współczynnik kalibracji
            y_values.append(value * WSP_A * 9.80665) # ciąg w Newtonach
            x_values_micros.append((int(parts_new[0].strip())/1000000))  # konwersja z mikrosekund na sekundy

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

from scipy.signal import savgol_filter

print(f"Zastosowanie filtru Savitzky-Golay: window_length={SAVGOL_WINDOW}, polyorder={SAVGOL_ORDER}")
y_values_savgol = savgol_filter(y_values, window_length=SAVGOL_WINDOW, polyorder=SAVGOL_ORDER)
print("Filtr Savitzky-Golay zastosowany pomyślnie.")

print("IMPLUS całkowity (średnia krocząca): {:.2f} Ns".format(impuls_trapezy(x_values_micros, y_values_srednia_kroczaca)))
print("IMPLUS całkowity (filtr Savitzky-Golay): {:.2f} Ns".format(impuls_trapezy(x_values_micros, y_values_savgol)))
print("IMPLUS całkowity (dane surowe): {:.2f} Ns".format(impuls_trapezy(x_values_micros, y_values)))

save_as_eng_file(x_values_micros, y_values_savgol, "R7_static_fire_2_filtr_sav_gol_21_3.eng")

# === USTAWIENIA JAKOŚCI ===
plt.figure(figsize=(10, 6))   # duży wykres (FullHD proporcje)

# plt.plot(x_values_micros, y_values, "b.", markersize=1)  # niebieskie punkty, mniejszy rozmiar
plt.plot(x_values_micros, y_values, linewidth=0.3)
# srednia krocząca
plt.plot(x_values_micros, y_values_srednia_kroczaca, "r-", linewidth=1.0)  # czerwona linia dla średniej kroczącej
plt.plot(x_values_micros, y_values_savgol, "g-", linewidth=1.0)  # zielona linia dla filtru Savitzky-Golay

plt.xlabel("Czas [s]", fontsize=14)

# plt.ylabel("Ciąg [kg]", fontsize=14)
plt.ylabel("Ciąg [N]", fontsize=14)

plt.title("Ciąg silnika na hamowni", fontsize=16)

plt.legend(["Dane surowe", "Średnia krocząca", "Filtr Savitzky-Golay"], fontsize=12)

plt.grid(True)
plt.tight_layout()

# Zapis w wysokiej rozdzielczości
plt.savefig(OUTPUT_FILE, dpi=400)

print(f"Wykres zapisany jako: {OUTPUT_FILE}")