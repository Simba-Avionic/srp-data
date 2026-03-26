import matplotlib.pyplot as plt

INPUT_FILE = "static2_FIRE_wyciety_test.txt"
OUTPUT_FORCE = "wyciety_force.png"
OUTPUT_IMPULSE = "wyciety_impulse.png"

WSP_B = -666
WSP_A = 0.04521833745

SR_KR_OKNO = 10

x_values = []
y_values = []
y_values_srednia_kroczaca = []
impuls_values = []

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        
        try:
            parts = line.split("|")
            parts_new = parts[1].split()

            time_s = int(parts_new[0].strip()) / 1_000_000
            value = float(parts_new[1].strip()) - WSP_B

            force = value * WSP_A * 9.80665  # Newtony

            x_values.append(time_s)
            y_values.append(force)

            # średnia krocząca
            if len(y_values) >= SR_KR_OKNO:
                srednia = sum(y_values[-SR_KR_OKNO:]) / SR_KR_OKNO
            else:
                srednia = force

            y_values_srednia_kroczaca.append(srednia)

        except (IndexError, ValueError):
            continue

if not y_values:
    print("Brak danych")
    exit()

# === LICZENIE IMPULSU (metoda trapezów) ===
impuls = 0.0
impuls_values.append(0.0)

for i in range(1, len(x_values)):
    dt = x_values[i] - x_values[i-1]
    
    # możesz zmienić na y_values jeśli chcesz bez wygładzania
    f1 = y_values_srednia_kroczaca[i-1]
    f2 = y_values_srednia_kroczaca[i]
    
    pole = (f1 + f2) / 2 * dt
    impuls += pole
    
    impuls_values.append(impuls)

print(f"Impuls całkowity: {impuls:.2f} Ns")

# === WSPÓLNY WYKRES ===
fig, ax1 = plt.subplots(figsize=(16,9))

# --- SIŁA (lewa oś Y) ---
ax1.plot(x_values, y_values, linewidth=0.3, label="Ciąg (surowy)")
ax1.plot(x_values, y_values_srednia_kroczaca, linewidth=1.0, label="Ciąg (średnia krocząca)")

ax1.set_xlabel("Czas [s]")
ax1.set_ylabel("Ciąg [N]")
ax1.grid(True)

# --- IMPULS (prawa oś Y) ---
ax2 = ax1.twinx()
ax2.plot(x_values, impuls_values, linewidth=1.5, label="Impuls (narastający)")

ax2.set_ylabel("Impuls [Ns]")

# pozioma linia impulsu całkowitego
ax2.axhline(y=impuls, linestyle="--", linewidth=1, label=f"Impuls całkowity = {impuls:.2f} Ns")

# dodanie ticka dla impulsu
yticks = list(ax2.get_yticks())
yticks.append(impuls)
ax2.set_yticks(yticks)

# opis przy linii
ax2.text(
    x_values[-1],
    impuls,
    f"  {impuls:.2f} Ns",
    va='center'
)

# zakres osi impulsu
ax2.set_ylim(-200, impuls * 1.1)

# === LEGENDA Z OBU OSI ===
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Ciąg + Impuls całkowity")
plt.tight_layout()
# plt.savefig("wykres_combined.png", dpi=600)

print("Wykres zapisany jako: wykres_combined.png")