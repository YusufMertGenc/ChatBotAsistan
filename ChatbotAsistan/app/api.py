from __future__ import annotations
import os, time
from typing import Dict, Any
from pathlib import Path
from fastapi import FastAPI, Body, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import json
from .indexer import build_index, HR_DIR

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/hr-ask")



app = FastAPI(title="HR QA Gateway (no-retriever)", version="1.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


# Yardımcılar
def _ts() -> float:
    return time.time()


# Health & Yardım
@app.get("/health")
async def health():
    """
    Basit sağlık kontrolü.
    Not: n8n'e canlı ping atmaz; sadece URL'i döner.
    """
    return {
        "ok": True,
        "webhook": N8N_WEBHOOK_URL,
        "mode": "no-retriever",
    }





# ---- Güvenli isim yardımcıları ----
ALLOWED_EXTS = {".pdf", ".docx", ".doc", ".txt"}

def _safe_name(name: str) -> str:
    """
    - Yalnızca dosya adını alır (path traversal'a izin vermez)
    - Geçici Office dosyalarını (~$) reddeder
    - Uzantıyı doğrular
    """
    s = Path(name).name
    if s.startswith("~$"):
        raise HTTPException(status_code=400, detail="Temporary/locked file is not allowed.")
    ext = Path(s).suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail=f"Extension not allowed: {ext}")
    return s

def _list_current_files() -> list[str]:
    HR_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(
        [p.name for p in HR_DIR.iterdir()
         if p.is_file() and not p.name.startswith("~$")]
    )

# ---- Upload ----
@app.post("/upload")
async def upload_file(files: list[UploadFile] = File(...)):
    """
    Dosyaları hrdocs/ altına güvenli biçimde kaydeder,
    yazma bittiğinde indeksler (Windows kilit sorununu engeller).
    """
    HR_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []

    for f in files:
        safe = _safe_name(f.filename)
        dest = HR_DIR / safe

        # ÖNEMLİ: Önce tamamını belleğe al → sonra dosyaya yaz
        data = await f.read()
        with dest.open("wb") as out:
            out.write(data)

        saved.append(safe)

    n = build_index()
    return {"ok": True, "saved": saved, "indexed": n, "files": _list_current_files()}


@app.get("/files")
def list_files():
    return {"files": _list_current_files()}

# ---------- Delete (retry system because I can not delete .pdf) ----------x
@app.delete("/files/{filename}")
def delete_file(filename: str):
    safe = _safe_name(filename)
    path = HR_DIR / safe
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    last_err: Exception | None = None
    for _ in range(6):  # ~1.2s’ye kadar dene (6 * 0.2s) x
        try:
            path.unlink()
            break
        except PermissionError as e:
            last_err = e
            time.sleep(0.2)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Delete failed: {e!s}")
    else:
        # hâlâ kilitli
        raise HTTPException(status_code=423, detail="File is in use/locked. Close viewer/preview and retry.")

    n = build_index()
    return {"ok": True, "deleted": safe, "indexed": n, "files": _list_current_files()}


@app.post("/check-n8n")
async def check_n8n():
    """
    n8n webhook'un erişilebilirliğini test etmek için hafif bir POST.
    n8n tarafında özel ele alınmasına gerek yok; JSON dönerse 200 bekleriz.
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(N8N_WEBHOOK_URL, json={"query": "__ping__", "k": 1})
        return {"ok": r.status_code // 100 == 2, "status": r.status_code, "body": r.text[:200]}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)


# Upload & Index (MCP server’ın kullandığı veri için)
@app.post("/upload")
async def upload_file(files: list[UploadFile] = File(...)):
    """
    Sürükle-bırak upload için: dosyaları hrdocs/ altına kaydeder, ardından yeniden indexler.
    NOT: Buradaki index, MCP server’ın arama aracı için; bu gateway retriever kullanmaz.
    """
    saved = []
    for f in files:
        dest = HR_DIR / f.filename
        with dest.open("wb") as out:
            out.write(await f.read())
        saved.append(f.filename)
    n = build_index()
    current = [p.name for p in HR_DIR.iterdir() if p.is_file() and not p.name.startswith("~$")]
    return {"ok": True, "saved": saved, "indexed": n}


@app.post("/ask")
async def ask(payload: Dict[str, Any] = Body(...)):
    """
    UI bu endpoint'e POST yapar.
    1) İsteği doğrudan n8n webhook'una iletir.
    2) n8n erişilemezse ya da 2xx değilse HATA döner (fallback YOK).
    """
    query = (payload.get("query") or "").strip()
    k = int(payload.get("k", 6))

    if not query:
        return JSONResponse({"answer": "Soru boş.", "used_sources": [], "snippets": []}, status_code=400)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(N8N_WEBHOOK_URL, json={"query": query, "k": k})
        if 200 <= r.status_code < 300:
            # n8n'in döndürdüğünü aynen geçir
            return JSONResponse(r.json(), status_code=r.status_code)
        return JSONResponse(
            {
                "error": "AI agent yanıt veremedi",
                "status": r.status_code,
                "detail": r.text[:500],
                "via": "n8n-proxy"
            },
            status_code=r.status_code
        )
    except Exception as e:
        # n8n erişilemedi
        return JSONResponse(
            {
                "error": "n8n erişilemedi",
                "detail": f"{type(e).__name__}: {e}",
                "via": "n8n-proxy"
            },
            status_code=502
        )



WEB_DIR = Path(__file__).resolve().parents[1] / "web"
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
