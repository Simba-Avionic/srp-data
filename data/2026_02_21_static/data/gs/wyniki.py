import matplotlib.pyplot as plt

INPUT_FILE = "hamownia_log_j.txt"
OUTPUT_FILE = "XD.png"

WSP_B = -666            # wartość z tenso wzorcowej, która odpowiada 0 kg
WSP_A = 0.04521833745   # współczynnik kalibracji, wyznaczony za pomocą metody najmniejszych kwadratów z danych z tensobelki wzorcowej

timestamps_second = []
y_values = []

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        
        line = line.strip()
        if not line:
            continue
        
        try:
            parts = line.split("|")

            value = float(parts[1].strip()) - WSP_B # odjęcie wartości z tenso wzorcowej
            y_values.append(value * WSP_A)  # przemnożenie przez współczynnik kalibracji
        except (IndexError, ValueError):
            continue


if not y_values:
    print("Brak poprawnych danych w pliku.")
    exit()

# === USTAWIENIA JAKOŚCI ===
plt.figure(figsize=(16,9))   # duży wykres (FullHD proporcje)
plt.plot(y_values, linewidth=0.8)

plt.xlabel("Numer próbki", fontsize=14)
plt.ylabel("Ciąg [kg]", fontsize=14)
plt.title("Ciąg silnika na hamowni", fontsize=16)

plt.grid(True)
plt.tight_layout()

# Zapis w wysokiej rozdzielczości
plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Wykres zapisany jako: {OUTPUT_FILE}")