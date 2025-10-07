from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Iterable
from app.db import get_conn
from app.normalizer import tr_normalize

HR_DIR = Path(__file__).resolve().parents[1] / "hrdocs"

def _coerce_record(r: Dict) -> Dict | None:
    # Reader’dan gelen alanları senin tablo şemana çeviriyoruz
    text = r.get("text_raw") or r.get("text") or r.get("content") or ""
    if not str(text).strip():
        return None
    return {
        "source": r.get("source") or r.get("filename") or r.get("name") or (Path(r["path"]).name if r.get("path") else "UNKNOWN"),
        "page": r.get("page"),
        "chunk_id": r.get("chunk_id", 0),
        "section_title": r.get("section_title") or r.get("title") or r.get("heading") or "",
        "text": str(text),
    }

def bulk_upsert(records: Iterable[Dict]) -> tuple[int,int]:
    conn = get_conn()
    ok = skipped = 0
    with conn:
        conn.execute("DELETE FROM docs;")
        for raw in records:
            r = _coerce_record(raw)
            if not r:
                skipped += 1
                continue
            conn.execute(
                """INSERT INTO docs (source, page, chunk_id, section_title, text,
                                     source_norm, section_title_norm, text_norm)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    r["source"], r["page"], r["chunk_id"], r["section_title"], r["text"],
                    tr_normalize(r["source"] or ""),
                    tr_normalize(r["section_title"] or ""),
                    tr_normalize(r["text"] or ""),
                ),
            )
            ok += 1
    return ok, skipped

def build_index() -> int:
    from .reader import load_dir
    items = load_dir(HR_DIR)  # Path kabul ediyor
    ok, _ = bulk_upsert(items)
    return ok
