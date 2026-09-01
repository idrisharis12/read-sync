import sqlite3
import os
from pathlib import Path

# Use a config directory
CONFIG_DIR = Path.home() / ".config" / "read-sync"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = CONFIG_DIR / "library.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Manga table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT,
            url TEXT,
            title TEXT NOT NULL,
            author TEXT,
            artist TEXT,
            description TEXT,
            genre TEXT,
            status TEXT,
            thumbnail_url TEXT,
            in_library BOOLEAN DEFAULT 0,
            category TEXT DEFAULT 'Default'
        )
    """)

    # Chapter table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manga_id INTEGER,
            url TEXT NOT NULL,
            name TEXT NOT NULL,
            chapter_number REAL,
            date_upload INTEGER,
            read BOOLEAN DEFAULT 0,
            bookmark BOOLEAN DEFAULT 0,
            last_page_read INTEGER DEFAULT 0,
            FOREIGN KEY (manga_id) REFERENCES manga(id)
        )
    """)

    # Tracker table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manga_id INTEGER,
            sync_id INTEGER,
            tracker_type TEXT,
            status TEXT,
            score REAL,
            last_chapter_read INTEGER,
            FOREIGN KEY (manga_id) REFERENCES manga(id)
        )
    """)

    conn.commit()
    conn.close()

def add_manga(title: str, url: str, source_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO manga (title, url, source_id, in_library) VALUES (?, ?, ?, 1)", 
        (title, url, source_id)
    )
    conn.commit()
    conn.close()

def get_library():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM manga WHERE in_library = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
