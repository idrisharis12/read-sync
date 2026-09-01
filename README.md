# read-sync — Terminal-Native Manga & Comic Reader

`read-sync` is a CLI tool to **read manga, comics, and webtoons entirely in the terminal**, utilizing sandboxed community scrapers, zero-latency image rendering, and automatic library tracking.

<p align="center">
  <img src="https://img.shields.io/badge/read--sync-Terminal_Reader-00E676?style=for-the-badge&logo=gnometerminal" alt="read-sync logo" />
</p>

<h1 align="center">📖 read-sync</h1>

<p align="center">
  <b>The Ultimate High-Performance Terminal Manga Reader & Headless OPDS Server</b>
</p>

<p align="center">
  <i>Read any manga from your terminal with <b>64x parallel pre-fetching</b>, <b>native Kitty/Sixel graphics</b>, <b>sandboxed QuickJS extensions</b>, and automatic real-time watch progress sync to <b>MyAnimeList</b>, <b>AniList</b> & <b>MangaUpdates</b>.</i>
</p>

<p align="center">
  <a href="https://github.com/idrisharis12/read-sync/stargazers"><img src="https://img.shields.io/github/stars/idrisharis12/read-sync?style=for-the-badge&logo=github&color=FFD700" alt="GitHub Stars" /></a>
  <a href="https://github.com/idrisharis12/read-sync/releases"><img src="https://img.shields.io/github/v/release/idrisharis12/read-sync?style=for-the-badge&color=00E676&logo=rocket" alt="Release" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-0088FF.svg?style=for-the-badge&logo=opensourceinitiative" alt="License: MIT" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" /></a><br>
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-2D3748?style=for-the-badge&logo=linux" alt="Platform" />
  <img src="https://img.shields.io/badge/Graphics-Kitty%20%7C%20Sixel-00C853?style=for-the-badge&logo=codeforces" alt="Native Graphics" />
  <img src="https://img.shields.io/badge/Tracking-MAL%20%7C%20AniList%20%7C%20MU-7C4DFF?style=for-the-badge&logo=graphql" alt="Multi-Platform Tracking" />
</p>

---

## 📦 Changelog & Recent Updates

<details>
<summary><b>✨ What's New in v0.1.x (Click to expand)</b></summary>

### v0.1.1
- **✨ Automated Release Workflow** — Added `ani-sync` style Makefile, `git-update.sh`, and `bump_version.py`.
- **🚀 Textual UI Engine** — Implemented the TUI interface with DataTable library layout.
- **⚡ Parallel Pre-Fetching Engine** — Spawns 64x worker swarms buffering straight to `/dev/shm`.
- **🛡️ Sandboxed JS Scrapers** — Built QuickJS integration for evaluating Tachiyomi/Mihon and Keiyoushi extensions securely.
- **☁️ Headless Server** — Shipped `FastAPI` OPDS endpoints for KOReader and Kavita integration.

</details>

---

<div align="center">
<pre><code>
  📖 <b style="color: #00E676;">read-sync</b> ❯ 🔍 Search: <i style="color: #FFD700;">solo leveling</i>
  ╭────────────────────────────────────────────────────────────────────────╮
  │ <span style="color: #00E676;">▶</span>  1. Solo Leveling (200 Chapters) [Webtoon Mode]                      │
  │    2. Solo Leveling: Ragnarok                                          │
  ╰────────────────────────────────────────────────────────────────────────╯
  ⚡ <b style="color: #00E676;">[Turbo Swarm: 64 Workers Active]</b> ──► [RAM-Disk: /dev/shm] ──► <b style="color: #FFD700;">[Kitty Graphics: 0.00s Delay]</b>
  ✂️ <b style="color: #FF6F00;">[Webtoon Stitcher: Slicing to Terminal Height]</b>
  🔄 <b style="color: #7C4DFF;">[Cloud Sync: MAL ✓ | AniList ✓]</b> ──► [Library: SQLite Updated 📚]
</code></pre>
</div>

---

## 📑 Table of Contents
- [✨ Core Features](#-core-features)
- [📦 Quick Installation](#-quick-installation)
- [🚀 Detailed Usage](#-detailed-usage)
- [⚙️ Headless Server Setup](#️-headless-server-setup)

---

## ✨ Core Features

- **🛡️ Modular Extension Repository Engine**: Zero hardcoded scrapers. Load community extensions (e.g., Keiyoushi) with the sandboxed QuickJS/WebAssembly execution runtime without restarting.
- **🖥️ True Terminal Native Renderers**: Supports pure zero-latency GPU rasterization using the **Kitty Graphics Protocol**, **Sixel Engine**, or **iTerm2 Inline Images**. 
- **✂️ Webtoon & Manhwa Dynamic Stitcher**: Seamless vertical image stitching without split-pixel gaps. Automatically slices vertical strips perfectly to your terminal height so you can scroll smoothly.
- **📚 SQLite Library & Scrobbling**: Complete multi-cloud tracking across **AniList**, **MyAnimeList**, **MangaUpdates**, and **Kitsu**.
- **🌐 Headless Suwayomi OPDS Server**: Spawn a background FastAPI server on `port 4567` to serve your library to external e-readers like **KOReader** and **Kavita**.
- **⚡ Parallel Chapter Swarm**: Downloads batches of chapters using 64 asynchronous workers directly into your system's `/dev/shm` RAM-disk to save SSD writes.

---

## 📦 Quick Installation

### 🚀 Universal Bash Installer (Linux / macOS)
```bash
curl -fsSL https://raw.githubusercontent.com/idrisharis12/read-sync/main/install.sh | bash
```

### 🪟 Windows (PowerShell)
```powershell
iwr -useb https://raw.githubusercontent.com/idrisharis12/read-sync/main/install.ps1 | iex
```

### 🏹 Arch Linux (AUR)
```bash
# Clone the PKGBUILD or use yay
yay -S read-sync
```

### 🐍 Pip (Python 3.8+)
```bash
git clone https://github.com/idrisharis12/read-sync.git
cd read-sync
make install
```

---

## 🚀 Detailed Usage

### 1. Search & Read
Search interactively using the built-in Textual TUI:
```bash
read-sync "chainsaw man"
read-sync "solo leveling" --mode webtoon
read-sync continue
```

### 2. Manage Extensions
Load external Keiyoushi/Mihon standard scraper registries:
```bash
read-sync repo add https://keiyoushi.github.io/extensions/index.min.json
read-sync ext list
read-sync ext install mangadex comick
```

### 3. Library Management
```bash
read-sync library                     # Open Textual Library UI
read-sync check                       # Check remote for new chapters
read-sync import backup.tachibk       # Migrate your Tachiyomi/Mihon backup!
```

### 4. Cloud Authentication
```bash
read-sync auth anilist
read-sync auth mal
```

### 5. Batch Archiver
Download full series into portable `.cbz` files with ComicInfo.xml metadata:
```bash
read-sync "berserk" -d 1-50 --cbz
```

---

## ⚙️ Headless Server Setup
Run the background server to host your library over the local network via REST/OPDS APIs:
```bash
read-sync serve --port 4567
```
- Open `http://localhost:4567` in your browser for the Web UI.
- Use `http://localhost:4567/opds` in **KOReader**, **Kavita**, or **Moon+ Reader**.

---

<p align="center">
  <i>Developed with ❤️ by the read-sync community.</i>
</p>
