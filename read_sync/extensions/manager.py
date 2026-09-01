import json
import os
import requests
from pathlib import Path

EXT_DIR = Path.home() / ".config" / "read-sync" / "extensions"
EXT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_REPO = "https://raw.githubusercontent.com/kodjodevf/mangayomi-extensions/main/index.json"

def fetch_index(repo_url: str = DEFAULT_REPO):
    """Fetches the extension registry index."""
    print(f"Fetching extension index from {repo_url}...")
    resp = requests.get(repo_url)
    resp.raise_for_status()
    return resp.json()

def list_available():
    """Lists available JS extensions from the index."""
    index = fetch_index()
    # Return a unique list of extensions by name
    exts = {}
    for ext in index:
        # Prefer english versions for listing simplicity
        if ext.get('lang') == 'en':
            exts[ext['name'].lower()] = ext
    return list(exts.values())

def install_extension(name: str):
    """Downloads and saves the JS source code for the requested extension."""
    exts = {e['name'].lower(): e for e in list_available()}
    
    name_lower = name.lower()
    if name_lower not in exts:
        print(f"Extension '{name}' not found in the 'en' registry.")
        return False
        
    ext_data = exts[name_lower]
    js_url = ext_data.get('sourceCodeUrl')
    
    print(f"Downloading {name} extension from {js_url}...")
    resp = requests.get(js_url)
    resp.raise_for_status()
    
    js_code = resp.text
    # Save the JS file
    file_path = EXT_DIR / f"{name_lower}.js"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(js_code)
        
    print(f"Successfully installed {name} to {file_path}")
    return True

def get_installed():
    """Returns a list of installed extension names."""
    installed = []
    for file in EXT_DIR.glob("*.js"):
        installed.append(file.stem)
    return installed

def load_extension_code(name: str):
    """Loads the JS code for an installed extension."""
    file_path = EXT_DIR / f"{name.lower()}.js"
    if not file_path.exists():
        raise FileNotFoundError(f"Extension {name} is not installed.")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
