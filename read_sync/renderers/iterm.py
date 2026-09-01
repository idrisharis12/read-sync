import sys
import base64
import os

def render_image_iterm(image_path: str):
    """
    Renders an image to the terminal using the iTerm2 inline image protocol.
    Supported by iTerm2 (macOS), VS Code Terminal, and WezTerm.
    """
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return

    with open(image_path, "rb") as f:
        image_data = f.read()

    b64_data = base64.b64encode(image_data).decode('ascii')
    
    # iTerm2 escape sequence: \033]1337;File=inline=1;width=100%:{base64}\a
    sys.stdout.write(f"\033]1337;File=inline=1;width=100%;preserveAspectRatio=1:{b64_data}\a\n")
    sys.stdout.flush()

def is_iterm_supported():
    term = os.environ.get("TERM_PROGRAM", "")
    return term in ["iTerm.app", "WezTerm", "vscode"]
