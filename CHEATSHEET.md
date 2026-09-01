# ⚡ read-sync — Ultimate CLI CheatSheet & Command Reference

<p align="center">
  <img src="https://img.shields.io/badge/read--sync-Terminal_Reader-00E676?style=for-the-badge&logo=gnometerminal" alt="read-sync logo" />
</p>

<p align="center">
  <b>Comprehensive Quick-Reference, Keybindings, Flags, Extension Auth & Power-User Recipes for read-sync</b>
</p>

---

## 📑 Quick Navigation

- [⚡ Quick Start One-Liners](#-quick-start-one-liners)
- [🎮 Core Commands Reference](#-core-commands-reference)
- [🧩 Extension & Repo Management](#-extension--repo-management)
- [📚 Library & Tracking Actions](#-library--tracking-actions)
- [☁️ Platform Authentication Commands](#-platform-authentication-commands)
- [⚙️ Headless OPDS Server Controls](#️-headless-opds-server-controls)

---

## ⚡ Quick Start One-Liners

| Goal | Command |
| :--- | :--- |
| **Search & Read Interactive (TUI)** | `read-sync` |
| **Native Direct Read (Bypass TUI)** | `read-sync read "frieren"` |
| **Resume Last Manga** | `read-sync continue` *(or `read-sync -c`)* |
| **Open Library TUI** | `read-sync library` |
| **Check for New Chapters** | `read-sync check` |
| **List Available Extensions** | `read-sync ext list` |
| **Install Extension (Scraper)** | `read-sync ext install comick mangadex` |
| **Add Keiyoushi Repo** | `read-sync repo add <url>` |
| **Download Chapter to `.cbz`** | `read-sync "solo leveling" -d 1 --cbz` |
| **Batch Download Range** | `read-sync "jujutsu kaisen" -d 1-50` |
| **Read in Webtoon/Manhwa Mode** | `read-sync "tower of god" --mode webtoon` |
| **Authenticate AniList Tracking** | `read-sync auth anilist` |
| **Import Tachiyomi Backup** | `read-sync import backup.tachibk` |
| **Start Headless OPDS Server** | `read-sync serve --port 4567` |

---

## 🎮 Core Commands Reference

### 1. `read-sync [manga title]`
Opens the Textual TUI interface with the search pre-filled, querying all active extensions.
```bash
read-sync "demon slayer"
read-sync "death note"
```

### 2. `read-sync read [manga title]`
Bypasses the UI, utilizes the native Python fallback scraper, downloads the chapter into `/dev/shm`, and renders it immediately via the **Kitty Graphics Protocol**.
```bash
read-sync read "chainsaw man"
```

### 3. `read-sync library`
Opens the full-screen DataTable library view so you can organize your collections, view unread chapters, and jump back into reading.
```bash
read-sync library
```

---

## 🧩 Extension & Repo Management

### `read-sync ext list`
Connects to the `mangayomi-extensions` remote GitHub registry, parses the JSON index, and returns a list of all available English JavaScript extensions.

### `read-sync ext install [name]`
Downloads the raw JS scraper source code for an extension and installs it securely into your `~/.config/read-sync/extensions/` directory for the sandboxed QuickJS engine.
```bash
read-sync ext install comick
read-sync ext install asurascans
```

---

## 📚 Library & Tracking Actions

### `read-sync import [file]`
Restores your complete library, read history, and tracking statuses from a standard Tachiyomi/Mihon protocol buffers backup file (`.tachibk`).
```bash
read-sync import my_library_2023.tachibk
```

### `read-sync check`
Fires up 64x parallel background workers to rapidly ping the respective extension servers and notify you if any manga in your library have new releases.

---

## ☁️ Platform Authentication Commands

Link your cloud trackers so `read-sync` can automatically scrobble your chapter progress natively via GraphQL/REST.

| Service | Command |
| :--- | :--- |
| **AniList** | `read-sync auth anilist` |
| **MyAnimeList (MAL)** | `read-sync auth mal` |
| **MangaUpdates** | `read-sync auth mangaupdates` |
| **Kitsu** | `read-sync auth kitsu` |

*Run the command to launch the OAuth prompt and securely save the token in your local database.*

---

## ⚙️ Headless OPDS Server Controls

### `read-sync serve`
Spawns the embedded `FastAPI` instance. This acts as a headless bridge that exposes your local SQLite database and downloaded chapters to external e-readers.

- **Default Port**: `4567` (Change with `--port 8080`)
- **OPDS Endpoint**: `http://localhost:4567/opds` (Plug this into **KOReader**, **Kavita**, or **Moon+ Reader** for native tablet reading).
