<!DOCTYPE html>
<html lang="en">

<body>

  <h1>Employee Training Assistant</h1>

  <p>
    An AI-powered onboarding and HR assistant designed to help Toyotetsu employees adapt faster, 
    reduce repetitive HR questions, and access company information securely and efficiently.
  </p>

  <h1>Overview</h1>

  <p>
    The Toyotetsu Employee Training Assistant is an intelligent chatbot that supports employees 
    throughout their onboarding and daily HR processes. It leverages 
    <strong>Retrieval-Augmented Generation (RAG)</strong> to provide accurate, document-grounded 
    answers using official HR handbooks, guidelines, and instructions. Through seamless integration 
    with <strong>N8N</strong> and <strong>FastMCP (MCP Server)</strong>, it also supports automated 
    workflows and modular agent communication.
  </p>

  <h1>Features</h1>

  <ul>
    <li><strong>FAQ Support:</strong> Answers frequently asked questions based on verified HR documents.</li>
    <li><strong>Smart Routing:</strong> Directs users to the right department or contact number when information is not available.</li>
    <li><strong>Document-Based Knowledge:</strong> Uses internal HR manuals and policies as knowledge sources for RAG.</li>
    <li><strong>Onboarding Assistance:</strong> Guides new employees through the orientation process and formal company procedures.</li>
    <li><strong>Automated Flows (N8N):</strong> Handles workflow automation such as notifications and information updates.</li>
    <li><strong>Data Security:</strong> Ensures all answers are generated from approved internal data — maintaining full compliance and confidentiality.</li>
    <li><strong>Customizable:</strong> Each department can tailor the assistant’s data and workflows to fit its specific needs.</li>
  </ul>

  <h1>Technologies Used</h1>

  <ul>
    <li>FastAPI</li>
    <li>Qwen 2.5 7B</li>
    <li>FastMCP (MCP Server)</li>
    <li>RAG (Retrieval-Augmented Generation)</li>
    <li>SQLite</li>
    <li>N8N</li>
    <li>HTML</li>
    <li>CSS</li>
    <li>JavaScript</li>
  </ul>

  <h1>System Architecture</h1>

  <p>The system follows a modular and secure architecture:</p>
  <ol class="numbered-list">
    <li><strong>User Interface (HTML/CSS/JS):</strong> Employees interact through a chat interface.</li>
    <li><strong>FastAPI Backend:</strong> Handles user requests and manages the main chatbot logic.</li>
    <li><strong>RAG Pipeline:</strong> Retrieves relevant context from HR documents.</li>
    <li><strong>Qwen 2.5 7B Model:</strong> Generates intelligent, context-aware responses.</li>
    <li><strong>FastMCP (MCP Server):</strong> Enables modular communication between model and components.</li>
    <li><strong>N8N Automations:</strong> Executes automated workflows such as routing or alerts.</li>
    <li><strong>SQLite Database:</strong> Logs conversations and manages document metadata.</li>
  </ol>

  <h1>N8N Workflows</h1>

  <img width="717" height="322" alt="image" src="https://github.com/user-attachments/assets/c07a7c49-ef53-4cf6-b305-d6ab03f50d09" />

  <img width="717" height="160" alt="image" src="https://github.com/user-attachments/assets/2085c4d3-72fb-4bab-bc1d-8ca584ba38cb" />

  <h1>GUI and Overview</h1>

  <img width="1247" height="813" alt="image" src="https://github.com/user-attachments/assets/c0ff43ae-34df-4633-bde8-2ef686efcd5d" />

</body>
</html>
