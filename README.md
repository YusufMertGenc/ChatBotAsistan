<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Toyotetsu Employee Training Assistant — README</title>
  <style>
    body { font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; line-height:1.6; color:#0f172a; background:#f8fafc; padding:32px; }
    .container { max-width:900px; margin:0 auto; background:#fff; padding:28px 36px; border-radius:12px; box-shadow:0 6px 30px rgba(2,6,23,0.08); }
    h1{ font-size:28px; margin-bottom:6px; }
    h2{ font-size:18px; margin-top:20px; color:#0b1220; }
    p{ margin:8px 0 12px; color:#334155; }
    ul{ margin:8px 0 12px 20px; color:#334155; }
    pre{ background:#0b1220; color:#e6eef8; padding:12px; border-radius:8px; overflow:auto; }
    code{ background:#eef2ff; padding:2px 6px; border-radius:6px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Courier New", monospace; }
    table { border-collapse:collapse; width:100%; margin-top:8px; }
    th, td { text-align:left; padding:10px; border-bottom:1px solid #eef2ff; }
    .muted { color:#64748b; font-size:13px; }
    .badge { display:inline-block; background:#eef2ff; color:#0b1220; padding:6px 10px; border-radius:999px; font-weight:600; margin-right:8px; }
    .cta { display:inline-block; margin-top:12px; background:#0ea5a4; color:#fff; padding:10px 14px; border-radius:8px; text-decoration:none; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🧠 Toyotetsu Employee Training Assistant</h1>
    <p class="muted">AI-powered onboarding and HR assistant for Toyotetsu — secure, document-grounded, and automation-ready.</p>

    <h2>🚀 Overview</h2>
    <p>
      The <strong>Toyotetsu Employee Training Assistant</strong> is an intelligent chatbot that helps employees during onboarding and daily HR interactions. It provides accurate answers derived from verified internal documents using a Retrieval-Augmented Generation (RAG) pipeline, integrates with automation via N8N, and supports modular agent communication through FastMCP.
    </p>

    <h2>🧩 Features</h2>
    <ul>
      <li><strong>FAQ Support</strong>: Answers common HR and company questions from verified documents.</li>
      <li><strong>Smart Routing</strong>: Directs users to the correct department or contact when needed.</li>
      <li><strong>Document-Based Knowledge (RAG)</strong>: Retrieves and uses internal PDFs/Word docs for grounded responses.</li>
      <li><strong>Onboarding Assistance</strong>: Guides new hires through formal procedures and orientation steps.</li>
      <li><strong>Automated Flows (N8N)</strong>: Triggers notifications, escalations, or follow-ups via workflow automation.</li>
      <li><strong>Data Security</strong>: All outputs are produced from approved internal sources, ensuring compliance and confidentiality.</li>
      <li><strong>Customizable</strong>: Departments can adapt data and workflows to their needs.</li>
    </ul>

    <h2>🛠️ Technologies Used</h2>
    <table>
      <thead>
        <tr><th>Component</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr><td><span class="badge">FastAPI</span></td><td>Backend framework for API endpoints and main chatbot logic.</td></tr>
        <tr><td><span class="badge">Qwen 2.5 7B</span></td><td>Open-source LLM used for understanding and generating responses.</td></tr>
        <tr><td><span class="badge">FastMCP (MCP Server)</span></td><td>Manages modular communication between AI components.</td></tr>
        <tr><td><span class="badge">RAG</span></td><td>Retrieval-Augmented Generation pipeline for document-grounded answers.</td></tr>
        <tr><td><span class="badge">SQLite</span></td><td>Lightweight database for session and conversation logs.</td></tr>
        <tr><td><span class="badge">N8N</span></td><td>Workflow automation and orchestration (notifications, integrations).</td></tr>
        <tr><td><span class="badge">HTML / CSS / JavaScript</span></td><td>Frontend chat interface and interaction layer.</td></tr>
      </tbody>
    </table>

    <h2>📈 System Architecture</h2>
    <p>The system follows a modular workflow:</p>
    <ol>
      <li>User interacts with the <em>web chat UI</em> (HTML/CSS/JS).</li>
      <li>Requests go to the <strong>FastAPI</strong> backend.</li>
      <li><strong>RAG</strong> retrieves relevant context from HR documents.</li>
      <li><strong>Qwen 2.5 7B</strong> generates context-aware responses.</li>
      <li><strong>FastMCP</strong> (MCP Server) coordinates multi-component communication.</li>
      <li><strong>N8N</strong> triggers automation workflows when escalation or follow-up is required.</li>
      <li><strong>SQLite</strong> logs conversations and document metadata.</li>
    </ol>

N8N Workflows


<img width="717" height="322" alt="image" src="https://github.com/user-attachments/assets/c07a7c49-ef53-4cf6-b305-d6ab03f50d09" />

<img width="717" height="160" alt="image" src="https://github.com/user-attachments/assets/2085c4d3-72fb-4bab-bc1d-8ca584ba38cb" />


GUI and Overview


<img width="1247" height="813" alt="image" src="https://github.com/user-attachments/assets/c0ff43ae-34df-4633-bde8-2ef686efcd5d" />


