from PIL import Image
import glob

# lista plików w kolejności
file_list = sorted(glob.glob("frames/frame_*.png"))

# wczytanie obrazków
images = [Image.open(f) for f in file_list]

# zapis GIF
images[0].save(
    "thrust_animation.gif",
    save_all=True,
    append_images=images[1:],
    duration=50,
    loop=0
)