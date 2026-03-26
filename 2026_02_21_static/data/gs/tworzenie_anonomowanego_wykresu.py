import matplotlib.pyplot as plt
import datetime
import os

INPUT_FILE = "hamownia_log_j.txt"
OUTPUT_DIR = "frames"  # folder na wszystkie klatki

WSP_B = -666
WSP_A = 0.04521833745

STEP = 50  # co ile próbek wstawiać timestamp na osi X

# --- Wczytanie danych ---
y_values = []
timestamps_short = []

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        
        try:
            parts = line.split("|")

            timestamp_str = parts[0].strip()
            dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

            short_ts = f"{dt.second:02d}.{int(dt.microsecond/10000):02d}"

            value = float(parts[1].strip()) - WSP_B
            y_values.append(value * WSP_A * 9.80665)
            timestamps_short.append(short_ts)

        except (IndexError, ValueError):
            continue

if not y_values:
    print("Brak danych!")
    exit()

# --- Przygotowanie folderu ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

tick_positions = list(range(0, len(y_values), STEP))
tick_labels = [timestamps_short[i] for i in tick_positions]

# --- Generowanie klatek ---
for i in range(0, len(y_values), 16):
    plt.figure(figsize=(16, 9))
    plt.plot(y_values, linewidth=0.8, color="blue")
    plt.ylim(-1000, 6000)
    
    # pionowy wskaźnik
    plt.axvline(x=i, color="red", linestyle="--", linewidth=1.2, alpha=0.8)
    
    plt.xlabel("Time [s]", fontsize=14)
    plt.ylabel("Thrust [N]", fontsize=14)
    plt.title("Static Fire no. 1 - Thrust vs Time", fontsize=16)
    
    plt.grid(True)
    plt.xticks(tick_positions, tick_labels, rotation=45, fontsize=9)
    
    plt.tight_layout()
    
    # zapis klatki
    filename = os.path.join(OUTPUT_DIR, f"frame_{i:05d}.png")
    plt.savefig(filename, dpi=150)  # dpi mniejsze, żeby szybciej generować
    plt.close()
    
print(f"Gotowe! Wygenerowano {len(y_values)} klatek w folderze '{OUTPUT_DIR}'")