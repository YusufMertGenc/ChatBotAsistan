🧠 Toyotetsu Employee Training Assistant

An AI-powered onboarding and HR assistant designed to help Toyotetsu employees adapt faster, reduce repetitive HR questions, and access company information effortlessly.

🚀 Overview

The Toyotetsu Employee Training Assistant is an intelligent chatbot that supports new employees during their onboarding process.
It answers HR-related questions using verified internal documents, assists with daily procedures, and guides users to the right department when necessary.

The assistant leverages Retrieval-Augmented Generation (RAG) to provide context-aware and document-grounded responses, ensuring accuracy and reliability.

🧩 Features

💬 FAQ Support: Answers frequently asked HR and company questions.

🧭 Smart Department Routing: Directs users to the right contact or department when needed.

📚 Document-Based Knowledge: Uses internal HR manuals and policies as data sources for RAG.

👥 Onboarding Assistance: Helps new hires understand workflows, policies, and formalities.

🔄 Automated Flows with N8N: Integrates automation workflows (notifications, updates, or report handling).

🔒 Secure Data Handling: All answers are generated from approved company documents — no external data access.

🛠️ Technologies Used
Component	Description
FastAPI	Backend framework for serving API endpoints and chatbot logic
Qwen 2.5 7B	Open-source large language model used for natural language understanding
FastMCP	Modular framework for managing multi-component agent communication
RAG (Retrieval-Augmented Generation)	Combines document retrieval with LLM responses for accuracy
SQLite	Lightweight database for chat history and user data
N8N	Automation tool for workflow orchestration and background processes
HTML, CSS, JavaScript	Frontend technologies for the web-based chat interface
