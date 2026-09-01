# read-sync

An end-to-end technical blueprint and architectural specification for `read-sync`, a terminal-native manga and comic reader.
It synthesizes the best design choices from Tachiyomi/Mihon (modular scraping, tracking, and multi-source library management), Keiyoushi (dynamic external repo indexing), Suwayomi (headless server and API routing), and Mangayomi (portable multi-source JS/Dart engine and tracker models).

## Features

- **Modular Extension Repository Engine:** Zero hardcoded scrapers. Uses external registries (e.g., Keiyoushi) with sandboxed JS/Python execution.
- **Headless Engine & TUI:** Dual modes - a Textual/FZF TUI for direct reading, and a FastAPI/OPDS headless server.
- **Adaptive Render Modes:** RTL manga, LTR comic, and Webtoon vertical strip modes with dynamic stitching and scaling.
- **Scrobbler & Library:** Auto-sync with AniList, MAL, MangaUpdates, Kitsu, etc. Local SQLite with categories.
- **Batch Downloader:** Parallel chapter downloader into `/dev/shm` buffer.
- **Terminal Image Rendering:** Native Kitty graphics, Sixel, iTerm2 inline, and external floating fallbacks.

## Quick Start

```bash
# Search & Read
read-sync "chainsaw man"
read-sync "solo leveling" --mode webtoon
read-sync continue

# Manage Extensions
read-sync repo add https://keiyoushi.github.io/extensions/index.min.json
read-sync ext list
read-sync ext install mangadex comick

# Library
read-sync library
read-sync check
read-sync import backup.tachibk

# Download
read-sync "berserk" -d 1-50 --cbz

# Server
read-sync serve --port 4567
```

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/.../install.sh | bash
```
