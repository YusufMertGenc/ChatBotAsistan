const CHAT_API   = "http://localhost:5678/webhook/hr-ask";   // n8n
const UPLOAD_API = `${location.origin}/upload`;               // FastAPI
const FILES_API  = `${location.origin}/files`;

const chat = document.getElementById("chat");
const q    = document.getElementById("q");
const go   = document.getElementById("go");
const uploadBtn = document.getElementById("upload");
const fileInput = document.getElementById("files");
const fileList  = document.getElementById("fileList");
const fileCount = document.getElementById("fileCount");
const dropzone  = document.getElementById("dropzone");

function now(){ const d=new Date(); return d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}); }
function el(tag, props={}, html=""){ const e=document.createElement(tag); Object.assign(e, props); if(html) e.innerHTML=html; return e; }
function scrollBottom(){ chat.scrollTop = chat.scrollHeight; }
function asArray(x){ if(Array.isArray(x))return x; if(typeof x==='string'){ try{const v=JSON.parse(x);return Array.isArray(v)?v:[];}catch{return []} } return []; }
function escapeHtml(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

function tidyAnswer(raw){
  const lines = String(raw || '').trim().split(/\r?\n/);
  const out = []; let listOpen = false;
  const closeList =()=>{ if(listOpen){ out.push('</ul>'); listOpen=false; } };

  for(const line of lines){
    if(/^\s*[\*\-]\s+/.test(line)){                    // madde
      if(!listOpen){ out.push('<ul style="margin:4px 0 8px 18px">'); listOpen=true; }
      out.push('<li>'+escapeHtml(line.replace(/^\s*[\*\-]\s+/,''))+'</li>');
    }else if(/^\s*\*\*(.+)\*\*\s*$/.test(line)){       // **Başlık**
      closeList();
      const title=line.replace(/^\s*\*\*(.+)\*\*\s*$/,"$1");
      out.push('<h4>'+escapeHtml(title)+'</h4>');
    }else if(line.trim()===''){
      closeList();
    }else{
      closeList();
      out.push('<p>'+escapeHtml(line.trim())+'</p>');
    }
  }
  closeList();
  return out.join('');
}

/* === MESAJ OLUŞTURUCU === */
function addMsg(role, html, opts={}){
  // role: "user" veya "assistant"
  const row = el("div",{className:"msg " + (role==="user"?"u":"a")});
  const bubble = el("div",{className:"bubble"});
  bubble.innerHTML = html; row.appendChild(bubble);

  if(opts.guard === "n8n-guard:no_context"){
    bubble.appendChild(el("div",{className:"meta"},"⚠️ Bağlam bulunamadı — dokümanda yer almayabilir."));
  }
  if(opts.sources && opts.sources.length){
    const badges = el("div",{className:"badges"});
    opts.sources.forEach(s=> badges.appendChild(el("span",{className:"badge"}, s)));
    bubble.appendChild(badges);
  }
  if(opts.details && opts.details.length){
    const toggle = el("div",{className:"src-toggle"},"Bulunan pasajları göster/gizle");
    const list = el("ul",{style:"margin:6px 0 0 18px; display:none;"});
    opts.details.forEach(h=>{
      const pg = h.page ? ` s.${h.page}` : "";
      list.appendChild(el("li",{}, `<strong>[${h.source}${pg}]</strong> ${escapeHtml(h.text || '')}`));
    });
    toggle.onclick = ()=>{ list.style.display = (list.style.display==="none")?"block":"none"; };
    bubble.appendChild(toggle); bubble.appendChild(list);
  }

  bubble.appendChild(el("div",{className:"meta"}, now()));
  chat.appendChild(row); scrollBottom(); return row;
}

/* === BUSY KİLİDİ === */
function setBusy(isBusy){
  q.disabled  = isBusy;
  go.disabled = isBusy;
  const composer = document.querySelector(".composer");
  if (composer) composer.classList.toggle("busy", isBusy);
}

/* === KARŞILAMA === */
addMsg("assistant","Merhaba! Ben TOYOTETSU Asistan. Size nasıl yardımcı olabilirim?");

/* === SOHBET === */
async function ask(){
  const query = q.value.trim(); if(!query){ q.focus(); return; }
  addMsg("user", escapeHtml(query));
  const typing = addMsg("assistant", `<span class="meta">Yazıyor…</span>`);
  setBusy(true);
  try{
    const r = await fetch(CHAT_API, {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ query, k: 12 })
    });
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    typing.remove();
    addMsg("assistant", tidyAnswer(data.answer || "Cevap üretilemedi."), {
      sources: asArray(data.used_sources),
      details: asArray(data.snippets),
      query, guard: data.guard
    });
  }catch(e){
    typing.remove(); addMsg("assistant", `Bir hata oluştu: ${escapeHtml(e.message || String(e))}`);
  }finally{
    setBusy(false);
    q.value=""; q.focus();
  }
}
go.onclick = ask;
q.addEventListener("keydown",(e)=>{ if(e.key==="Enter" && !go.disabled && !q.disabled) ask(); });

/* === DOSYA LİSTELE / SİL === */
async function refreshFiles(){
  try{
    const r = await fetch(FILES_API);
    if(!r.ok) throw new Error("HTTP "+r.status);
    const data = await r.json();
    const files = Array.isArray(data.files)?data.files:[];
    fileList.innerHTML = ""; fileCount.textContent = files.length;
    if(!files.length){ fileList.innerHTML = "<li>Henüz dosya yok</li>"; return; }
    files.forEach(name=>{
      const li = document.createElement("li");
      li.className = "file-row";
      const left = document.createElement("div");
      left.textContent = name;
      const del = document.createElement("button");
      del.textContent = "Sil";
      del.className = "danger";
      del.onclick = async ()=>{
        if(!confirm(`Silinsin mi?\n${name}`)) return;
        try{
          const r = await fetch(`${FILES_API}/${encodeURIComponent(name)}`, {method:"DELETE"});
          if(!r.ok){
            if(r.status===423){ addMsg("assistant","❌ Silinemedi: Dosya kullanımda/kitli."); return; }
            throw new Error("HTTP "+r.status);
          }
          const res = await r.json();
          addMsg("assistant", `🗑️ Silindi: ${escapeHtml(res.deleted || name)}\n🔄 ${escapeHtml(String(res.indexed||0))} kayıt yeniden indekslendi.`);
          refreshFiles();
        }catch(e){
          addMsg("assistant", "❌ Silme hatası: "+escapeHtml(e.message||String(e)));
        }
      };
      li.appendChild(left); li.appendChild(del); fileList.appendChild(li);
    });
  }catch(e){
    fileList.innerHTML = "<li>Dosya listesi alınamadı: "+escapeHtml(e.message||String(e))+"</li>";
    fileCount.textContent = "0";
  }
}

/* === YÜKLEME (buton + drag&drop) === */
async function uploadFiles(){
  if(!fileInput.files.length){ addMsg("assistant","Dosya seçilmedi."); return; }
  const fd = new FormData(); for(const f of fileInput.files) fd.append("files", f);
  try{
    uploadBtn.disabled = true; fileInput.disabled = true;
    const r = await fetch(UPLOAD_API, {method:"POST", body:fd});
    if(!r.ok) throw new Error("HTTP "+r.status);
    const data = await r.json();
    addMsg("assistant", `📄 Yüklendi: ${escapeHtml((data.saved||[]).join(", "))}\n🔄 ${escapeHtml(String(data.indexed||0))} kayıt indekslendi.`);
    refreshFiles();
  }catch(e){
    addMsg("assistant","❌ Yükleme hatası: "+escapeHtml(e.message||String(e)));
  }finally{
    uploadBtn.disabled = false; fileInput.disabled = false; fileInput.value="";
  }
}
uploadBtn.onclick = uploadFiles;

/* Drag & Drop olayları */
if (dropzone){
  ["dragenter","dragover"].forEach(t => dropzone.addEventListener(t, (e)=>{
    e.preventDefault(); e.stopPropagation(); dropzone.classList.add("dragover");
  }));
  ["dragleave","dragend","drop"].forEach(t => dropzone.addEventListener(t, (e)=>{
    e.preventDefault(); e.stopPropagation(); dropzone.classList.remove("dragover");
  }));
  dropzone.addEventListener("drop", (e)=>{
    const files = e.dataTransfer?.files;
    if(files && files.length){
      fileInput.files = files;    // seçimi input’a geçir
      uploadFiles();              // otomatik yükle
    }
  });
}

refreshFiles();
