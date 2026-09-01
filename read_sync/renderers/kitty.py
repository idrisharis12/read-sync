import os
import sys
import base64

def render_image_kitty(image_path: str):
    """
    Renders an image to the terminal using the native Kitty Graphics Protocol.
    This provides zero-latency direct GPU rasterization.
    """
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return

    # Kitty graphics protocol magic sequence
    # \x1b_G ... \x1b\\
    # a=T (transmit and display)
    # f=100 (PNG), f=24 (RGB), f=32 (RGBA). We will use base64 transmission.
    
    with open(image_path, "rb") as f:
        image_data = f.read()

    b64_data = base64.b64encode(image_data).decode('ascii')
    
    # We transmit in chunks if it's large, but for simplicity here we do it all at once
    sys.stdout.write(f"\x1b_Ga=T,f=100,m=0;{b64_data}\x1b\\")
    sys.stdout.flush()

def is_kitty_supported():
    term = os.environ.get("TERM", "")
    return "kitty" in term or os.environ.get("KITTY_WINDOW_ID") is not None
