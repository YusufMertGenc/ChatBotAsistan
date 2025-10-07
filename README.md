<!DOCTYPE html>
<html lang="en">

<body>

  <h1>Employee Training Assistant</h1>

  <p>
    An AI-powered, fully customizable assistant designed to support every department. 
    It helps employees adapt faster, interpret reports, reduce repetitive 
    questions, and access company information securely and efficiently. 
    The assistant’s knowledge base can easily be updated through an intuitive interface 
    where departments can upload their own documents and data sources.
  </p>

  <h1>Overview</h1>

  <p>
    Employee Assistant is an intelligent and adaptable chatbot that can be used across 
    various business units such as HR, finance, operations, and management. 
    It leverages <strong>Retrieval-Augmented Generation (RAG)</strong> to provide accurate, 
    document-grounded answers using official company handbooks, reports, and instructions. 
    Through seamless integration with <strong>N8N</strong> and <strong>FastMCP (MCP Server)</strong>, 
    it also supports automated workflows and modular agent communication.
  </p>

  <p>
    From a data security standpoint, the system is extremely safe — 
    all responses are generated locally using a <strong>private on-premise LLM</strong>, 
    ensuring that no sensitive company data ever leaves the organization’s infrastructure.
  </p>

  <h1>Features</h1>

  <ul>
    <li><strong>FAQ Support:</strong> Answers frequently asked questions based on verified internal documents.</li>
    <li><strong>Smart Routing:</strong> Directs users to the right department or contact number when information is not available.</li>
    <li><strong>Document-Based Knowledge:</strong> Uses uploaded internal manuals, policies, and reports as knowledge sources for RAG.</li>
    <li><strong>Cross-Department Use:</strong> Can be customized for HR, finance, R&D, operations, or any other team with department-specific data.</li>
    <li><strong>Automated Flows (N8N):</strong> Handles workflow automation such as notifications, report generation, and information updates.</li>
    <li><strong>Data Security:</strong> Maintains strict confidentiality by using a local company-hosted LLM.</li>
    <li><strong>Customizable:</strong> Each department can tailor the assistant’s data and workflows to fit its specific needs through the web interface.</li>
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
    <li><strong>RAG Pipeline:</strong> Retrieves relevant context from department-specific documents.</li>
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
