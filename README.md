<div align="center">

<img src="https://img.shields.io/badge/read--sync-Terminal_Reader-00E676?style=for-the-badge&logo=gnometerminal" alt="read-sync logo" width="300" />

# 📖 read-sync

**The Ultimate High-Performance Terminal Manga Reader & Headless OPDS Server**

[![GitHub Stars](https://img.shields.io/github/stars/idrisharis12/read-sync?style=for-the-badge&logo=github&color=FFD700)](https://github.com/idrisharis12/read-sync/stargazers)
[![Release](https://img.shields.io/github/v/release/idrisharis12/read-sync?style=for-the-badge&color=00E676&logo=rocket)](https://github.com/idrisharis12/read-sync/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-0088FF.svg?style=for-the-badge&logo=opensourceinitiative)](LICENSE)
<br>
[![Platform Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#)
[![Platform macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)](#)
[![Platform Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#)
[![Graphics Kitty/Sixel](https://img.shields.io/badge/Graphics-Kitty%20%7C%20Sixel-00C853?style=for-the-badge&logo=codeforces)](#)

*Read manga, comics, and webtoons entirely in your terminal with **64x parallel pre-fetching**, native **Kitty/Sixel GPU rendering**, sandboxed **QuickJS extensions**, and real-time **AniList / MyAnimeList** sync!*

[**🚀 Quick Install**](#-quick-installation) • 
[**📋 CheatSheet**](CHEATSHEET.md) • 
[**✨ Features**](#-core-features) • 
[**⚙️ Headless Server**](#️-headless-server-setup)

</div>

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

## ✨ Core Features

| Feature | Description |
| :--- | :--- |
| **🛡️ Extension Engine** | Zero hardcoded scrapers. Uses the sandboxed **QuickJS** engine to evaluate JS scrapers (e.g. Mangayomi/Keiyoushi) on the fly securely. |
| **🖥️ Native Rendering** | Pure zero-latency GPU rasterization using **Kitty Graphics Protocol**, **Sixel**, or iTerm2 inline images. |
| **✂️ Webtoon Stitcher** | Seamless vertical stitching for Manhwa/Webtoons. Automatically slices strips perfectly to your terminal height for smooth scrolling. |
| **⚡ 64x Swarm Download** | Fetches chapter batches using 64 concurrent asynchronous workers straight to `/dev/shm` (RAM) to save SSD wear. |
| **☁️ Cloud Scrobbling** | Connects to **AniList**, **MyAnimeList**, **MangaUpdates**, and **Kitsu** to auto-sync your library via GraphQL/OAuth. |
| **🌐 Headless Server** | Background `FastAPI` instance hosts an **OPDS catalog** server on `port 4567` for Kavita, KOReader, and Moon+ Reader. |

---

## ⚡ Hardware & Performance Footprint

Because `read-sync` bypasses heavy Electron frameworks and browser engines, it is incredibly resource-efficient, making it perfect for older hardware, homelabs, or Raspberry Pis.

| Resource | Usage Details |
| :--- | :--- |
| **💾 Storage (Disk)** | **~75 MB** for the standalone executable or Python environment.<br>Library metadata is stored in a highly compressed **SQLite** database (`~/.config/read-sync/library.db`), taking less than **5 MB** for a massive library.<br>Downloaded archives (`.cbz`) depend on your usage. |
| **🧠 RAM (Memory)** | **~40 MB - 80 MB** baseline for the Textual TUI and QuickJS engine.<br>**Temporary `/dev/shm` Buffer:** When reading, chapters are buffered directly into RAM to save SSD wear. A standard 30-page manga chapter consumes about **~30 MB** of RAM dynamically. (Pillow webtoon stitching may temporarily spike to ~150 MB for massive continuous images). |
| **⚙️ CPU (Processing)**| **< 2%** during reading. Image rendering is completely offloaded to your terminal's GPU (via the Kitty Graphics Protocol).<br>The **64x Parallel Downloader** is asynchronous (I/O bound), meaning it downloads at maximum line-speed without bottlenecking your CPU threads. |

---

## 🚀 Quick Installation

**`read-sync` is shipped as a single, compiled standalone executable for all platforms.** No Python setup required!

### 📥 1. Download the Latest Release Binary

Go to the [**Releases Page**](https://github.com/idrisharis12/read-sync/releases/latest) and download the binary for your OS:

- 🐧 **Linux**: `read-sync-linux`
- 🍎 **macOS**: `read-sync-macos`
- 🪟 **Windows**: `read-sync-windows.exe`

### ⚙️ 2. Install via Command Line (Alternative)

<details>
<summary><b>🐧 Linux / 🍎 macOS (Bash Auto-Install)</b></summary>
<br>

```bash
curl -fsSL https://raw.githubusercontent.com/idrisharis12/read-sync/main/install.sh | bash
```
</details>

<details>
<summary><b>🪟 Windows (PowerShell Auto-Install)</b></summary>
<br>

```powershell
iwr -useb https://raw.githubusercontent.com/idrisharis12/read-sync/main/install.ps1 | iex
```
</details>

<details>
<summary><b>🐍 Build from Source (Pip / Make)</b></summary>
<br>

```bash
git clone https://github.com/idrisharis12/read-sync.git
cd read-sync
make install
```
</details>

---

## 📖 How to Use

*(Check out the [**CheatSheet**](CHEATSHEET.md) for a full command reference!)*

### First Time Setup: Install Scrapers
`read-sync` comes with zero scrapers built-in for safety. Install some from the community registry:
```bash
read-sync ext list
read-sync ext install comick
```

### Search & Read
Pop open the TUI or use the direct native fallback reader:
```bash
read-sync                       # Open interactive library UI
read-sync read "chainsaw man"   # Read immediately via terminal GPU
```

### Connect AniList / MAL Tracker
```bash
read-sync auth anilist
```

---

## 🌐 Headless Server Setup
You can run `read-sync` in the background to serve your local downloaded `.cbz` manga library to tablets and e-readers via standard OPDS.

```bash
read-sync serve --port 4567
```
1. Open `http://localhost:4567` in your browser.
2. In **KOReader** or **Kavita**, add `http://localhost:4567/opds` to your network libraries!

---
<div align="center">
  <i>Developed with ❤️ by the read-sync community.</i>
</div>
