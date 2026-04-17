import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def generate_gif_frames(x, y1, y2, impuls, fps=60, output_dir="frames"):
    os.makedirs(output_dir, exist_ok=True)

    t_start = x[0]
    t_end = x[-1]
    duration = t_end - t_start

    total_frames = int(duration * fps)

    print(f"Generowanie {total_frames} klatek ({fps} FPS)...")

    for frame in range(total_frames):
        t = t_start + frame / fps

        fig, ax1 = plt.subplots(figsize=(16,9))

        # --- główny wykres ---
        ax1.plot(x, y1, linewidth=0.3)
        ax1.plot(x, y2, "g-", linewidth=1.0)

        ax1.set_xlabel("Czas [s]")
        ax1.set_ylabel("Ciąg [N]")

        # --- impuls ---
        ax2 = ax1.twinx()
        ax2.plot(x, impuls, "r--", linewidth=1.5)

        # --- pionowa linia czasu ---
        ax1.axvline(t, linestyle="-", linewidth=2)

        ax2.set_ylabel("Impuls [Ns]")

        plt.title(f"Czas: {t:.3f} s")

        plt.grid(True)
        plt.tight_layout()

        filename = os.path.join(output_dir, f"frame_{frame:05d}.png")
        plt.savefig(filename, dpi=150)
        plt.close(fig)

        if frame % 100 == 0:
            print(f"{frame}/{total_frames}")

    print("Klatki wygenerowane.")


def create_gif_from_frames(frames_dir, output_gif, fps=60):
    frame_files = sorted([
        f for f in os.listdir(frames_dir)
        if f.endswith(".png")
    ])

    if not frame_files:
        print("Brak klatek!")
        return

    print(f"Znaleziono {len(frame_files)} klatek. Tworzenie GIF...")

    images = []
    for fname in frame_files:
        path = os.path.join(frames_dir, fname)
        img = Image.open(path)
        images.append(img)

    duration = int(1000 / fps)  # ms na klatkę

    images[0].save(
        output_gif,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )

    print(f"GIF zapisany jako: {output_gif}")