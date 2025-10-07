from __future__ import annotations
from typing import Dict, Any, List, Tuple
from app.db import get_conn
from app.normalizer import tr_normalize
import re

THRESHOLD = 7.0      # önce düşük tut: kaçırmamak için
W_PHRASE  = 40.0      # tam ifade çok değerli
W_TOKHIT  = 12.0      # her ortak terim makul katkı
W_TITLE   = 10.0       # başlık bonusu ama sınırlı
W_NEAR    = 14.0      # yakınlık önemli ama tek başına belirleyici değil
W_FUZZY   = 9.0      # yazım farkları/ekler için orta-üst seviye


try:
    from rapidfuzz import fuzz
except Exception:
    fuzz = None

TR_STOP = {"ve","ile","veya","de","da","ki","mi","mı","mu","mü","bir","bu","şu","o",
           "için","icin","gibi","ne","nedir","nelerdir","neler","kaç","kac",
           "nasıl","nasil","hangi","neydi"}

def _tokens(s: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9çğıöşü]+", tr_normalize(s)) if t not in TR_STOP]

def _near_bonus(qt: List[str], tt: List[str], window: int = 8) -> float:
    if len(qt) < 2 or not tt:
        return 0.0
    pos = {}
    for i, w in enumerate(tt):
        pos.setdefault(w, []).append(i)
    bonus = 0.0
    seen = set()
    for i in range(len(qt)):
        for j in range(i+1, len(qt)):
            a, b = qt[i], qt[j]
            key = tuple(sorted((a,b)))
            if key in seen or a not in pos or b not in pos:
                continue
            seen.add(key)
            ia, ib = pos[a], pos[b]
            pa = pb = 0
            best = 10**9
            while pa < len(ia) and pb < len(ib):
                best = min(best, abs(ia[pa]-ib[pb]))
                if ia[pa] < ib[pb]: pa += 1
                else: pb += 1
            if best <= window:
                bonus += W_NEAR * (1.0 - best/(window+1))
    return min(W_NEAR, bonus)

def _detect_columns(conn) -> Dict[str, str]:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(docs);").fetchall()}
    if {"source","section_title","text"}.issubset(cols):
        return {"source":"source","title":"section_title","text":"text","page":"page"}
    # eski alternatif şema
    return {"source":"doc_id","title":"title_raw","text":"text_raw","page":"order_in_section"}

def _score_item(q_norm: str, q_terms: List[str], row: Dict[str, Any]) -> float:
    text  = (row.get("text") or "").strip()
    title = (row.get("title") or "").strip()
    if not text:
        return 0.0

    t_norm   = tr_normalize(text)
    t_tokens = _tokens(t_norm)
    score = 0.0

    # 1) ham ifade (phrase)
    if len(q_norm.split()) >= 2 and q_norm in t_norm:
        score += W_PHRASE

    # 2) ortak terim
    inter = set(t_tokens) & set(q_terms)
    score += min(W_TOKHIT * len(inter), 30.0)

    # 3) yakınlık (NEAR benzeri)
    score += _near_bonus(list(inter if inter else q_terms), t_tokens)

    # 4) fuzzy (opsiyonel)
    if fuzz:
        try:
            fr = fuzz.token_set_ratio(q_norm, t_norm)  # 0..100
            score += min(W_FUZZY, fr * (W_FUZZY/100.0))
        except Exception:
            pass

    # 5) başlık bonusu
    if title:
        title_hits = set(_tokens(title)) & set(q_terms)
        score += min(W_TITLE, 3.0 * len(title_hits))

    return score

def _compose_answer(chunks: List[Dict[str,Any]]) -> str:
    parts: List[str] = []
    for c in chunks[:6]:
        t = (c.get("text") or "").strip()
        t = re.sub(r"\s+", " ", t)
        if t and (not parts or t not in parts[-1]):
            parts.append(t)
    return "\n".join(parts)[:1200].strip()

def search_docs(question: str) -> Dict[str, Any]:
    q = (question or "").strip()
    if not q:
        return {"answer":"", "used_sources":[]}

    conn = get_conn()
    col = _detect_columns(conn)

    rows = conn.execute(
        f"SELECT {col['source']} as source, {col['title']} as title, "
        f"{col['text']} as text, {col.get('page','NULL')} as page, chunk_id "
        f"FROM docs"
    ).fetchall()
    if not rows:
        return {"answer":"", "used_sources":[]}

    q_norm  = tr_normalize(q)
    q_terms = _tokens(q_norm)

    scored: List[Tuple[float, Dict[str,Any]]] = []
    for r in rows:
        row = {k: r[k] for k in r.keys()}
        s = _score_item(q_norm, q_terms, row)
        if s > 0:
            scored.append((s, row))

    if not scored:
        return {"answer":"", "used_sources":[]}

    scored.sort(key=lambda x: x[0], reverse=True)
    top_score, top = scored[0]
    if top_score < THRESHOLD:
        return {"answer":"", "used_sources":[]}

    # aynı kaynak + aynı başlık (yoksa sayfa) etrafında grupla
    key = (top["source"], top.get("title") or f"p{top.get('page')}")
    group = [r for _, r in scored if (r["source"], r.get("title") or f"p{r.get('page')}") == key][:6]

    answer = _compose_answer(group)
    used_sources = sorted({r["source"] for r in group})
    return {"answer": answer, "used_sources": used_sources}
