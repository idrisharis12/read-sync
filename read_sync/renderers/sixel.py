import subprocess
import os

def render_image_sixel(image_path: str):
    """
    Renders an image to the terminal using the Sixel Engine (Tier 2).
    Requires a Sixel-compatible terminal (Foot, xterm, Alacritty-sixel) and libsixel (img2sixel).
    """
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return

    try:
        # Use img2sixel to do the heavy lifting of Sixel quantization and rendering
        subprocess.run(["img2sixel", image_path])
    except FileNotFoundError:
        print("Sixel engine 'img2sixel' is not installed. Please install 'libsixel'.")
        # Fallback to ASCII block rendering (e.g. using chafa if installed)
        try:
            subprocess.run(["chafa", "-f", "sixel", image_path])
        except FileNotFoundError:
            print("No Sixel fallback (chafa) found either.")
