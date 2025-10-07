🧠 <h1>Toyotetsu Employee Training Assistant</h1>

An AI-powered onboarding and HR assistant designed to help Toyotetsu employees adapt faster, reduce repetitive HR questions, and access company information securely and efficiently.

🚀 Overview

The Toyotetsu Employee Training Assistant is an intelligent chatbot that supports employees throughout their onboarding and daily HR processes.
It leverages Retrieval-Augmented Generation (RAG) to provide accurate, document-grounded answers using official HR handbooks, guidelines, and instructions.
Through seamless integration with N8N and FastMCP (MCP Server), it also supports automated workflows and modular agent communication.

🧩 Features

💬 FAQ Support: Answers frequently asked questions based on verified HR documents.

🧭 Smart Routing: Directs users to the right department or contact number when information is not available.

📚 Document-Based Knowledge: Uses internal HR manuals and policies as knowledge sources for RAG.

👥 Onboarding Assistance: Guides new employees through the orientation process and formal company procedures.

🔄 Automated Flows (N8N): Handles workflow automation such as notifications and information updates.

🔒 Data Security: Ensures all answers are generated from approved internal data — maintaining full compliance and confidentiality.

⚙️ Customizable: Each department can tailor the assistant’s data and workflows to fit its specific needs.

🛠️ Technologies Used

1-)FastAPI

2-)Qwen 2.5 7B

3-)FastMCP (MCP Server)

4-)RAG (Retrieval-Augmented Generation)

5-)SQLite

6-)N8N

7-)HTML

8-)CSS

9-)JavaScript

📈 System Architecture

The system follows a modular and secure architecture:

1-)User Interface (HTML/CSS/JS): Employees interact through a chat interface.

2-)FastAPI Backend: Handles user requests and manages the main chatbot logic.

3-)RAG Pipeline: Retrieves relevant context from HR documents.

4-)Qwen 2.5 7B Model: Generates intelligent, context-aware responses.

5-)FastMCP (MCP Server): Enables modular communication between model and components.

6-)N8N Automations: Executes automated workflows such as routing or alerts.

7-)SQLite Database: Logs conversations and manages document metadata.


N8N Workflows


<img width="717" height="322" alt="image" src="https://github.com/user-attachments/assets/c07a7c49-ef53-4cf6-b305-d6ab03f50d09" />

<img width="717" height="160" alt="image" src="https://github.com/user-attachments/assets/2085c4d3-72fb-4bab-bc1d-8ca584ba38cb" />


GUI and Overview


<img width="1247" height="813" alt="image" src="https://github.com/user-attachments/assets/c0ff43ae-34df-4633-bde8-2ef686efcd5d" />


