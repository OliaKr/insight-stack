# InsightStack – Multi-Agent Strategic Analyzer

**InsightStack** is an AI-powered tool that provides strategic insights based on multi-departmental reports. This application leverages AI agents to analyze reports from different business departments, such as Sales, Support, and Operations, and provides actionable insights in a user-friendly dashboard. The application is powered by Azure OpenAI and built with the Model Context Protocol (MCP), providing a robust foundation for AI-driven analysis.

## Overview:

Provides businesses with strategic insights by analyzing reports from various departments. The application integrates advanced AI models from Azure OpenAI and utilizes Autogen AgentChat for orchestrating multi-agent collaboration.

## 🔧 Key Features

- 🧠 AI-powered insights from sales, support, and operations reports
- 📦 MCP-compliant structure: external context via FastAPI endpoints
- 🤖 Azure OpenAI-powered LLM inference
- 🖥️ Streamlit UI to trigger analysis and display results
- 🔁 Fixed-role orchestration across Sales, Support, Ops, and Coordinator agents
- ⚙️ Longtime memory integration to retain previous analysis and improve insights over time

## Technologies Used

- Azure OpenAI
- Autogen AgentChat: A framework for agent-based collaboration, which allows agents to analyze reports and collaborate autonomously.
- Streamlit: A Python library to build interactive web applications and dashboards for displaying insights
- Pandas: For managing and displaying tabular data
- Hugging Face: For model hosting and access to pre-trained models (e.g., sentence transformers for text embeddings).
- Redis: Used for storing and managing memory of past reports and insights

## Setup and Installation

- Before running the application, ensure you have the following installed:

- Python 3.8+ (Recommended: Create a virtual environment)
- Redis (Local or through a service)
- Required Python packages (listed below)

## Installation Steps:

1. Clone the repository

```bash
git clone https://github.com/your-repository/insight-sync.git
cd insight-sync

```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt

```

4. Set up your environment variables

```bash
AZURE_DEPLOYMENT_ID=your_deployment_id
AZURE_API_KEY=your_api_key
AZURE_API_VERSION=your_api_version
AZURE_OPENAI_ENDPOINT=your_azure_endpoint

```

5. Start Redis

```bash
redis-server

```

6. Run the app

```bash
streamlit run app.py

```

7. Visit http://localhost:8501 in your web browser to view the application
