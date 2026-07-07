#!/usr/bin/env python3
"""Analiza logów hamowni: filtr Savitzky-Golay, impuls, wykres ciągu."""

import argparse

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from gif_maker import create_gif_from_frames, generate_gif_frames

DEFAULT_WSP_B = -563
DEFAULT_WSP_A = 0.04521833745
DEFAULT_TIMESTAMP_OFFSET = 144129096
DEFAULT_SR_KR_OKNO = 10
DEFAULT_SAVGOL_WINDOW = 21
DEFAULT_SAVGOL_ORDER = 3


def parse_args():
    parser = argparse.ArgumentParser(description="Analiza ciągu z logu hamowni GS.")
    parser.add_argument("--input", "-i", required=True, help="Plik wejściowy z logiem hamowni")
    parser.add_argument("--output", "-o", default="thrust.png", help="Plik wykresu PNG")
    parser.add_argument("--eng-output", help="Plik wyjściowy .eng (opcjonalnie)")
    parser.add_argument("--wsp-b", type=float, default=DEFAULT_WSP_B, help="Offset tensobelki [kg]")
    parser.add_argument("--wsp-a", type=float, default=DEFAULT_WSP_A, help="Współczynnik kalibracji")
    parser.add_argument(
        "--timestamp-offset",
        type=int,
        default=DEFAULT_TIMESTAMP_OFFSET,
        help="Korekta offsetu czasu Arduino [µs]",
    )
    parser.add_argument("--savgol-window", type=int, default=DEFAULT_SAVGOL_WINDOW)
    parser.add_argument("--savgol-order", type=int, default=DEFAULT_SAVGOL_ORDER)
    parser.add_argument("--generate-gif", action="store_true", help="Generuj animację GIF")
    return parser.parse_args()


def save_as_eng_file(seconds, newtons, filename_out):
    with open(filename_out, "w", encoding="utf-8") as file_out:
        first_time = seconds[0]
        file_out.write("Majda-2 140 1950 P 20.0 34.0 SimLE_SimBa")
        for sec, newton in zip(seconds, newtons):
            time_sec = sec - first_time
            file_out.write(f"\n{time_sec:.6f} {newton:.3f}")


def impuls_trapezy(x, y):
    impuls = 0.0
    impuls_values = [0.0]

    for i in range(1, len(x)):
        dt = x[i] - x[i - 1]
        f1 = y[i - 1]
        f2 = y[i]
        pole = (f1 + f2) / 2 * dt
        impuls += pole
        impuls_values.append(impuls)

    return impuls_values


def load_thrust_data(input_file, wsp_b, wsp_a, timestamp_offset, sr_kr_okno):
    x_values_micros = []
    y_values = []
    y_values_srednia_kroczaca = []
    suma_surowych = 0
    suma_surowych_count = 0
    maks_ciag_surowe = -float("inf")

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split("|")
                parts_new = parts[1].split()

                raw_int = int(parts_new[1].strip())
                suma_surowych += raw_int
                suma_surowych_count += 1

                zeroed_int = raw_int
                value = float(zeroed_int) - wsp_b
                ciag_n = value * wsp_a * 9.80665
                y_values.append(ciag_n)

                if ciag_n > maks_ciag_surowe:
                    maks_ciag_surowe = ciag_n

                x_values_micros.append(
                    (int(parts_new[0].strip()) - timestamp_offset) / 1_000_000
                )

                if len(y_values) >= sr_kr_okno:
                    srednia = sum(y_values[-sr_kr_okno:]) / sr_kr_okno
                    y_values_srednia_kroczaca.append(srednia)
                else:
                    y_values_srednia_kroczaca.append(ciag_n)

            except (IndexError, ValueError):
                continue

    if suma_surowych_count > 0:
        avg_surowych = suma_surowych / suma_surowych_count
        print(f"Średnia wartość surowych danych: {avg_surowych:.2f}")

    return x_values_micros, y_values, y_values_srednia_kroczaca, maks_ciag_surowe


def plot_thrust(x_values, y_values, y_values_savgol, impuls_values, impuls_total, output_file):
    fig, ax1 = plt.subplots(figsize=(16, 9))

    line1, = ax1.plot(x_values, y_values, linewidth=0.3, label="Dane surowe")
    line2, = ax1.plot(x_values, y_values_savgol, "g-", linewidth=1.0, label="Filtr Savitzky-Golay")
    ax1.set_xlabel("Czas [s]", fontsize=14)
    ax1.set_ylabel("Ciąg [N]", fontsize=14)

    ax2 = ax1.twinx()
    line3, = ax2.plot(x_values, impuls_values, "r--", linewidth=1.5, label="Impuls całkowity [Ns]")
    line4 = ax2.axhline(
        impuls_total,
        linestyle=":",
        linewidth=2,
        label=f"Impuls końcowy = {impuls_total:.1f} Ns",
    )
    ax2.set_ylabel("Impuls [Ns]", fontsize=14)

    lines = [line1, line2, line3, line4]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, fontsize=12, loc="best")

    plt.title("Ciąg silnika na hamowni + impuls całkowity", fontsize=16)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=600)
    print(f"Wykres zapisany jako: {output_file}")


def main():
    args = parse_args()

    x_values, y_values, y_values_srednia_kroczaca, maks_ciag_surowe = load_thrust_data(
        args.input,
        args.wsp_b,
        args.wsp_a,
        args.timestamp_offset,
        DEFAULT_SR_KR_OKNO,
    )

    if not y_values:
        print("Brak poprawnych danych w pliku.")
        raise SystemExit(1)

    print(
        f"Zastosowanie filtru Savitzky-Golay: "
        f"window_length={args.savgol_window}, polyorder={args.savgol_order}"
    )
    y_values_savgol = savgol_filter(
        y_values, window_length=args.savgol_window, polyorder=args.savgol_order
    )
    print("Filtr Savitzky-Golay zastosowany pomyślnie.")

    avg_thrust_not_filtered = sum(y_values) / len(y_values)
    avg_thrust_srednia_kroczaca = sum(y_values_srednia_kroczaca) / len(y_values_srednia_kroczaca)
    avg_thrust_savgol = sum(y_values_savgol) / len(y_values_savgol)

    print(f"Średni ciąg (dane nieprzefiltrowane): {avg_thrust_not_filtered:.2f} N")
    print(f"Średni ciąg (średnia krocząca): {avg_thrust_srednia_kroczaca:.2f} N")
    print(f"Średni ciąg (filtr Savitzky-Golay): {avg_thrust_savgol:.2f} N")

    impuls_sk = impuls_trapezy(x_values, y_values_srednia_kroczaca)
    impuls_sg = impuls_trapezy(x_values, y_values_savgol)
    impuls_raw = impuls_trapezy(x_values, y_values)

    print(f"IMPULS całkowity (średnia krocząca): {impuls_sk[-1]:.2f} Ns")
    print(f"IMPULS całkowity (filtr Savitzky-Golay): {impuls_sg[-1]:.2f} Ns")
    print(f"IMPULS całkowity (dane surowe): {impuls_raw[-1]:.2f} Ns")

    if args.eng_output:
        save_as_eng_file(x_values, y_values_savgol, args.eng_output)

    if maks_ciag_surowe > -float("inf"):
        print(f"Maksymalny ciąg (surowe): {maks_ciag_surowe:.2f} N")

    maks_ciag_filtr = max(y_values_savgol)
    print(f"Maksymalny ciąg (filtr Savitzky-Golay): {maks_ciag_filtr:.2f} N")

    impuls_values = impuls_sg
    impuls_total = impuls_values[-1]

    plot_thrust(x_values, y_values, y_values_savgol, impuls_values, impuls_total, args.output)

    if args.generate_gif:
        print("Generowanie klatek do GIFa...")
        generate_gif_frames(x_values, y_values, y_values_savgol, impuls_values, fps=60, output_dir="frames")
        create_gif_from_frames("frames", "animation.gif", fps=60)


if __name__ == "__main__":
    main()
