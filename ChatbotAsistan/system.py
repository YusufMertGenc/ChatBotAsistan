from __future__ import annotations
from fastmcp import FastMCP
from typing import Dict, List, Any
from datetime import date
from openai import OpenAI

# Yeni modüler yapı: retriever içe aktarımı
from app.retriever import search_docs as search_docs_core

server = FastMCP("CalisanEgitimAsistani")

CONTACTS: Dict[str, Dict[str, str]] = {
    "ik": {"unit": "İnsan Kaynakları", "phone": "+90 555 000 00 01", "email": "ik@ornek.com"},
}

# LLM (Ollama)
OLLAMA = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
LLM_MODEL = "qwen2.5:7b-instruct"
LLM_TEMP = 0.2
LLM_MAXTOK = 450
LLM_OPTS = {"num_ctx": 8192, "repeat_penalty": 1.15}

LLM_SYSTEM_PROMPT = """


""".strip()








def _no_context_answer() -> Dict[str, Any]:
    info = CONTACTS["ik"]
    return {
        "status": "no_context",
        "answer": f"Bu konu onaylı dokümanda yer almıyor. İK: {info['phone']} • {info['email']}",
        "used_sources": [],
        "snippets": [],
        "retrieved_at": date.today().isoformat(),
    }


# =====
# TOOLS
# =====
@server.tool(
    name="send_mail",
    description="ask_local çıktısını ilgili kurallara göre e-posta olarak gönderir. "
 )
async def send_mail(to: str, subject: str, body: str) -> Dict[str, Any]:
    import smtplib, ssl, re
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    FROM_ADDR = "yusufmertgencc@gmail.com"
    PASSWORD = "dlkv zgmp uxvf iyvs"  

    # --- sanitize: literal '\n' -> real newline; gereksiz kaçışları temizle
    def _sanitize(s: str) -> str:
        if not s:
            return ""
        s = s.replace("\\n", "\n").replace("\\t", "\t")
        s = s.replace("\r\n", "\n").replace("\r", "\n")
        s = re.sub(r"\n{3,}", "\n\n", s)
        return s.strip()

    def _split_main_and_sources(s: str) -> tuple[str, list[str]]:
        parts = s.split("\n")
        main_lines, srcs, in_src = [], [], False
        for line in parts:
            if not in_src and line.strip().lower().startswith("kaynaklar:"):
                in_src = True
                continue
            if in_src:
                for token in line.split(","):
                    t = token.strip()
                    if t:
                        srcs.append(t)
            else:
                main_lines.append(line)
        main = "\n".join(main_lines).strip()
        return main, srcs

    def _detect_numbered_list(lines: list[str]) -> bool:
        for ln in lines:
            if re.match(r"\s*(\d+[\.)]|\-|\•)\s+", ln):
                return True
        return False

    def _render_plain(main_text: str, sources: list[str]) -> str:
        lines = [ln.strip() for ln in main_text.split("\n") if ln.strip()]
        out = []
        out.append("")
        if _detect_numbered_list(lines):
            out.extend(lines)
        else:
            for p in lines:
                out.append(p)
                out.append("")
        if sources:
            out.append("Kaynaklar:")
            out.append(", ".join(sources))
            out.append("")
        out.append("Çalışan Eğitim Asistanı")
        return "\n".join(out).strip()

    def _render_html(main_text: str, sources: list[str]) -> str:
        lines = [ln.strip() for ln in main_text.split("\n") if ln.strip()]
        is_list = _detect_numbered_list(lines)

        def esc(x: str) -> str:
            import html
            return html.escape(x, quote=True)

        html_parts = []
        
        if is_list:
            if any(re.match(r"\s*\d+[\.)]\s+", ln) for ln in lines):
                html_parts.append("<ol>")
                for ln in lines:
                    ln_clean = re.sub(r"^\s*\d+[\.)]\s*", "", ln)
                    html_parts.append(f"<li>{esc(ln_clean)}</li>")
                html_parts.append("</ol>")
            else:
                html_parts.append("<ul>")
                for ln in lines:
                    ln_clean = re.sub(r"^\s*[\-\•]\s*", "", ln)
                    html_parts.append(f"<li>{esc(ln_clean)}</li>")
                html_parts.append("</ul>")
        else:
            for p in main_text.split("\n"):
                p = p.strip()
                if p:
                    html_parts.append(f"<p>{esc(p)}</p>")

        if sources:
            html_parts.append("<p style='margin-top:12px;margin-bottom:4px;'><strong>Kaynaklar:</strong></p>")
            html_parts.append("<ul>")
            for s in sources:
                html_parts.append(f"<li>{esc(s)}</li>")
            html_parts.append("</ul>")

        html_parts.append("<p style='margin-top:16px;'>Saygılarımla,<br/>Çalışan Eğitim Asistanı</p>")
        html_parts.append("</div>")
        return "".join(html_parts)

    # --- sanitize & böl
    body_s = _sanitize(body)
    main_text, sources = _split_main_and_sources(body_s)

    # --- multipart/alternative mail hazırla
    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_ADDR
    msg["To"] = to.strip()
    msg["Subject"] = subject

    plain = _render_plain(main_text, sources)
    html  = _render_html(main_text, sources)

    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html",  "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.starttls(context=context)
            s.login(FROM_ADDR, PASSWORD)
            s.sendmail(FROM_ADDR, [to.strip()], msg.as_string())
        return {"status": "success", "recipient": to}
    except Exception as e:
        return {"status": "error", "error": str(e)}






@server.tool(
    name="ask_local",
    description="Soruya göre dokümanlardan anahtar-kelime bağlamı getirir ve yerel LLM ile cevap üretir. mail gönderme durumunda send_mail tooluna gidecek texti verir.",
)
async def ask_local(
    question: str | None = None,
    query: str | None = None,
    k: int | str = 12,
) -> Dict[str, Any]:
    q = (question or query or "").strip()
    try:
        k = int(k)
    except Exception:
        k = 12

    if not q:
        out = _no_context_answer()
        out["question"] = ""
        return out

    res = search_docs_core(q)  # senkron çağrı, await YOK
    answer = res.get("answer", "")
    sources = res.get("used_sources", [])
    print(LLM_SYSTEM_PROMPT)
    if not answer:
    # bağlam yok → senin kurallarında chat'e hiçbir şey yazılmayacak
        return {"answer": "", "used_sources": []}

    return {"answer": answer,
            "used_sources": sources,
         "question": q,                              # <-- EKLENDİ
        "used_sources_csv": ", ".join(sources),  }


if __name__ == "__main__":
    server.run(transport="sse", host="0.0.0.0", port=3333, path="/mcp")
 

 