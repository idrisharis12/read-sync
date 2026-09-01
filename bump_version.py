#!/usr/bin/env python3
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def get_current_version():
    config_file = BASE_DIR / "read_sync" / "__init__.py"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    raise ValueError("Could not find __version__ in read_sync/__init__.py")

def calculate_next_version(current, bump_type):
    parts = current.split(".")
    major, minor, patch = map(int, parts)
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    elif re.match(r"^\d+\.\d+\.\d+$", bump_type):
        return bump_type
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")

def update_file(path, pattern, replacement):
    if not path.exists():
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(pattern, replacement, content)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  ✓ Updated {path.relative_to(BASE_DIR)}")
        return True
    return False

def bump_all(new_ver):
    curr = get_current_version()
    print(f"🚀 Bumping version: v{curr} ──► v{new_ver}\n")
    update_file(BASE_DIR / "read_sync" / "__init__.py", r'__version__\s*=\s*["\'][^"\']+["\']', f'__version__ = "{new_ver}"')
    update_file(BASE_DIR / "pyproject.toml", r'version\s*=\s*["\'][^"\']+["\']', f'version = "{new_ver}"')
    update_file(BASE_DIR / "PKGBUILD", r"pkgver=[^\n]+", f"pkgver={new_ver}")
    update_file(BASE_DIR / "read_sync" / "server" / "app.py", r'"version":\s*["\'][^"\']+["\']', f'"version": "{new_ver}"')
    print(f"\n✨ Version successfully bumped to v{new_ver}")

def main():
    if len(sys.argv) < 2:
        print(f"Current version: v{get_current_version()}")
        return
    bump_arg = sys.argv[1].lower().lstrip("v")
    curr = get_current_version()
    new_ver = calculate_next_version(curr, bump_arg)
    bump_all(new_ver)

if __name__ == "__main__":
    main()
