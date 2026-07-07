import pandas as pd
import matplotlib.pyplot as plt

# --- Częstotliwość logów ---
def czestotliwosc_data_csv(path='data.csv'):
    df = pd.read_csv(path)
    t = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f', errors='coerce')
    t = t.dropna()
    dt = t.diff().dt.total_seconds().dropna()
    dt = dt[dt > 0]  # tylko dodatnie (bez cofnięć zegara)
    n = len(df)
    czas_s = (t.max() - t.min()).total_seconds() if len(t) > 1 else 0
    mean_interval_s = float(dt.mean()) if len(dt) else 0
    freq_hz = 1 / mean_interval_s if mean_interval_s > 0 else 0
    print(f"--- {path} ---")
    print(f"  Liczba wpisow: {n}")
    print(f"  Sredni odstep miedzy logami: {mean_interval_s*1000:.2f} ms")
    print(f"  Czestotliwosc logowania: {freq_hz:.2f} Hz")
    if czas_s > 0:
        print(f"  Czas span (pierwszy-ostatni): {czas_s:.2f} s")
    print()

def czestotliwosc_log_csv(path='10_1.9.49.log.csv'):
    df = pd.read_csv(path, sep=';')
    if 'TIMESTAMP' not in df.columns:
        print(f"--- {path} --- brak kolumny TIMESTAMP")
        return
    ts = pd.to_numeric(df['TIMESTAMP'], errors='coerce').dropna()
    dt = ts.diff().dropna()
    dt = dt[dt > 0]
    n = len(df)
    mean_interval = float(dt.mean()) if len(dt) else 0
    # wartosci typu 9547109, roznice ~200 -> zalozenie: ms
    mean_interval_s = mean_interval / 1000
    freq_hz = 1 / mean_interval_s if mean_interval_s > 0 else 0
    print(f"--- {path} ---")
    print(f"  Liczba wpisow: {n}")
    print(f"  Sredni odstep miedzy logami: {mean_interval:.1f} ms")
    print(f"  Czestotliwosc logowania: {freq_hz:.2f} Hz")
    print()

czestotliwosc_data_csv('data.csv')
czestotliwosc_log_csv('10_1.9.49.log.csv')

# Wczytaj dane
df = pd.read_csv('data.csv')

# Konwersja timestamp na indeks czasowy (opcjonalnie - dla osi X)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f', errors='coerce')
# Jeśli dużo punktów, można próbkować co N-ty wiersz dla czytelności
# df = df.iloc[::10]  # co 10. wiersz

fig, ax1 = plt.subplots(figsize=(12, 6))

# Lewa oś - newdpressevent i newpressevent
ax1.set_xlabel('Czas / indeks')
ax1.set_ylabel('newdpressevent / newpressevent', color='#1f77b4')
line1, = ax1.plot(df.index, df['newdpressevent'], color='#1f77b4', alpha=0.8, label='newdpressevent')
line2, = ax1.plot(df.index, df['newpressevent'], color='#ff7f0e', alpha=0.8, label='newpressevent')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.grid(True, alpha=0.3)

# Prawa oś - temperatury
ax2 = ax1.twinx()
ax2.set_ylabel('Temperatura (°C?)', color='#2ca02c')
line3, = ax2.plot(df.index, df['newtempevent_1'], color='#2ca02c', alpha=0.8, label='newtempevent_1')
line4, = ax2.plot(df.index, df['newtempevent_2'], color='#d62728', alpha=0.8, label='newtempevent_2')
line5, = ax2.plot(df.index, df['newtempevent_3'], color='#9467bd', alpha=0.8, label='newtempevent_3')
ax2.tick_params(axis='y', labelcolor='#2ca02c')

# Legenda - łączymy linie z obu osi
lines = [line1, line2, line3, line4, line5]
ax1.legend(lines, [l.get_label() for l in lines], loc='upper right')

plt.title('newdpressevent / newpressevent (lewa oś) vs temperatury (prawa oś)')
fig.tight_layout()
plt.xlim(50000, 52000)
plt.savefig('wykres.png', dpi=150, bbox_inches='tight')
plt.show()
