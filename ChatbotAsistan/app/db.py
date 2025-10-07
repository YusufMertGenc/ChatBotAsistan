from __future__ import annotations
import os, sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("HRQA_DB", Path(__file__).resolve().parents[1] / "ik.db"))

def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # timeout: başka işlem yazıyorsa bekle; check_same_thread: asyncio/pooling için
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # --- Jurnal modu ---
    # WAL: çoklu okur / tek yazar senaryosunda daha az "locked" üretir.
    # Eğer WAL istemiyorsan bir alt satırı DELETE olarak değiştir.
    conn.execute("PRAGMA journal_mode=WAL;")     # alternatif: DELETE
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout=5000;")    # 5 sn bekle

    # Şema (ilk bağlantıda yaratır, sonraki bağlantılarda hızlı geçer)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS docs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source TEXT,
      page INTEGER,
      chunk_id INTEGER,
      section_title TEXT,
      text TEXT,
      source_norm TEXT,
      section_title_norm TEXT,
      text_norm TEXT
    );
    """)
    return conn
