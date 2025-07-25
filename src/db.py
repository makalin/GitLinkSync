import sqlite3

DB_PATH = "links.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        followed INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def save_link(url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO links (url) VALUES (?)", (url,))
        conn.commit()
    finally:
        conn.close()

def get_links():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url, followed FROM links")
    results = c.fetchall()
    conn.close()
    return results

def mark_as_followed(url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE links SET followed = 1 WHERE url = ?", (url,))
    conn.commit()
    conn.close() 