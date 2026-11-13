"""
SQLite-backed cache layer.
Tables:
  email_cache    — keyed on Message-ID, avoids re-parsing the same email
  download_cache — keyed on URL, avoids re-downloading the same file
  cache_stats    — running hit/miss counters
"""
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).parent / 'cache' / 'cache.db'
DB_PATH.parent.mkdir(exist_ok=True)


def _conn():
    c = sqlite3.connect(str(DB_PATH))
    c.row_factory = sqlite3.Row
    return c


def init():
    db = _conn()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS email_cache (
        msg_id       TEXT PRIMARY KEY,
        subject      TEXT,
        sender       TEXT,
        date         TEXT,
        url_count    INTEGER DEFAULT 0,
        processed_at REAL
    );
    CREATE TABLE IF NOT EXISTS download_cache (
        url           TEXT PRIMARY KEY,
        filename      TEXT,
        size_bytes    INTEGER DEFAULT 0,
        status        TEXT,
        downloaded_at REAL
    );
    CREATE TABLE IF NOT EXISTS cache_stats (
        id              INTEGER PRIMARY KEY,
        email_hits      INTEGER DEFAULT 0,
        email_misses    INTEGER DEFAULT 0,
        download_hits   INTEGER DEFAULT 0,
        download_misses INTEGER DEFAULT 0
    );
    INSERT OR IGNORE INTO cache_stats (id) VALUES (1);
    """)
    db.commit()
    db.close()


def _bump(col):
    db = _conn()
    db.execute(f'UPDATE cache_stats SET {col}={col}+1 WHERE id=1')
    db.commit()
    db.close()


# ── Email cache ────────────────────────────────────────────────────────────────
def get_email(msg_id):
    db = _conn()
    row = db.execute('SELECT * FROM email_cache WHERE msg_id=?', (msg_id,)).fetchone()
    db.close()
    if row:
        _bump('email_hits')
        return dict(row)
    _bump('email_misses')
    return None


def save_email(em):
    db = _conn()
    db.execute(
        'INSERT OR REPLACE INTO email_cache (msg_id,subject,sender,date,url_count,processed_at) VALUES (?,?,?,?,?,?)',
        (em['msg_id'], em['subject'], em['sender'], em['date'], em['url_count'], time.time())
    )
    db.commit()
    db.close()


def list_emails():
    db = _conn()
    rows = db.execute('SELECT * FROM email_cache ORDER BY processed_at DESC LIMIT 200').fetchall()
    db.close()
    return [dict(r) for r in rows]


# ── Download cache ─────────────────────────────────────────────────────────────
def get_download(url):
    db = _conn()
    row = db.execute('SELECT * FROM download_cache WHERE url=?', (url,)).fetchone()
    db.close()
    if row:
        _bump('download_hits')
        return dict(row)
    _bump('download_misses')
    return None


def save_download(url, filename, size_bytes):
    db = _conn()
    db.execute(
        'INSERT OR REPLACE INTO download_cache (url,filename,size_bytes,status,downloaded_at) VALUES (?,?,?,?,?)',
        (url, filename, size_bytes, 'done', time.time())
    )
    db.commit()
    db.close()


def list_downloads():
    db = _conn()
    rows = db.execute('SELECT * FROM download_cache ORDER BY downloaded_at DESC').fetchall()
    db.close()
    return [dict(r) for r in rows]


# ── Stats & housekeeping ────────────────────────────────────────────────────────
def get_stats():
    db = _conn()
    stats = dict(db.execute('SELECT * FROM cache_stats WHERE id=1').fetchone() or {})
    stats['emails_cached']    = db.execute('SELECT COUNT(*) FROM email_cache').fetchone()[0]
    stats['downloads_cached'] = db.execute('SELECT COUNT(*) FROM download_cache').fetchone()[0]
    total_size = db.execute('SELECT COALESCE(SUM(size_bytes),0) FROM download_cache').fetchone()[0]
    stats['total_cached_mb'] = round(total_size / (1024 * 1024), 2)
    db.close()
    return stats


def clear_all():
    db = _conn()
    db.executescript("""
        DELETE FROM email_cache;
        DELETE FROM download_cache;
        UPDATE cache_stats SET email_hits=0,email_misses=0,download_hits=0,download_misses=0 WHERE id=1;
    """)
    db.commit()
    db.close()
