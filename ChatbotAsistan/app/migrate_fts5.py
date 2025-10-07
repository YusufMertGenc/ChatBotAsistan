from app.db import get_conn

DDL_DOCS = """
CREATE VIRTUAL TABLE docs USING fts5(
  doc_id UNINDEXED,
  section_id UNINDEXED,
  order_in_section UNINDEXED,
  title_raw,
  title_norm,
  text_raw,
  text_norm,
  tokenize = "unicode61 remove_diacritics 2"
);
"""

DDL_SECTIONS = """
CREATE TABLE IF NOT EXISTS sections(
  section_id TEXT PRIMARY KEY,
  section_title TEXT
);
"""

REQUIRED_COLS = {"doc_id","section_id","order_in_section","title_raw","title_norm","text_raw","text_norm"}

def _get_existing_sql(conn):
    row = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='docs'").fetchone()
    return row[0] if row and row[0] else None

def _get_cols(conn):
    try:
        rows = conn.execute("PRAGMA table_info(docs);").fetchall()
        return {r[1] for r in rows} if rows else set()
    except Exception:
        return set()

def main():
    conn = get_conn()
    with conn:
        existing_sql = _get_existing_sql(conn)
        recreate = False
        if not existing_sql:
            recreate = True
        else:
            cols = _get_cols(conn)
            if not REQUIRED_COLS.issubset(cols):
                # Eski/uyumsuz şema → yeniden oluştur
                recreate = True

        if recreate:
            # Eski tabloyu kaldır ve doğru şema ile oluştur
            conn.execute("DROP TABLE IF EXISTS docs;")
            conn.execute(DDL_DOCS)

        # sections her halükârda var olsun
        conn.execute(DDL_SECTIONS)

    print("[FTS5] docs & sections hazır (güncel şema).")

if __name__ == "__main__":
    main()
