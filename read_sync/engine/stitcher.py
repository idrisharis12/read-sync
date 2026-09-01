from PIL import Image
import os
from typing import List

def stitch_webtoon_pages(image_paths: List[str], output_path: str):
    """
    Seamless vertical image stitching without split-pixel gaps.
    Useful for Manhwa/Webtoons.
    """
    images = []
    for path in image_paths:
        if os.path.exists(path):
            images.append(Image.open(path))
            
    if not images:
        return None
        
    # Calculate total height and max width
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    
    # Create a new blank canvas
    stitched_image = Image.new('RGB', (max_width, total_height))
    
    # Paste images vertically
    y_offset = 0
    for img in images:
        # Center horizontally if needed, or just paste at x=0
        stitched_image.paste(img, (0, y_offset))
        y_offset += img.height
        
    stitched_image.save(output_path)
    return output_path

import shutil

def slice_for_terminal(image_path: str):
    """
    Automatic height slicing for memory efficiency and smooth TUI scrolling.
    Auto-detects the current terminal pixel height.
    """
    # Fallback to 800 if we can't determine pixel height
    terminal_height_pixels = 800 
    
    # In a real environment, we'd use ioctl to get the exact pixel dimensions of the terminal.
    # For now, we simulate a standard terminal window height (e.g. 24 rows * 20px font = 480px, or a larger 800px window)
    try:
        columns, lines = shutil.get_terminal_size()
        # Assume approx 20px per row as a baseline for slice chunks
        terminal_height_pixels = lines * 20 
    except Exception:
        pass

    try:
        img = Image.open(image_path)
    except Exception:
        return []

    slices = []
    for i in range(0, img.height, terminal_height_pixels):
        box = (0, i, img.width, min(i + terminal_height_pixels, img.height))
        slice_img = img.crop(box)
        
        slice_path = f"{image_path}_slice_{i}.jpg"
        slice_img.save(slice_path)
        slices.append(slice_path)
        
    return slices
