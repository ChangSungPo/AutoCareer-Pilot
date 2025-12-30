# 🚀 Zero-Cost AI Job Searcher

A sophisticated multi-agent system built with Python and Streamlit that automates the process of analyzing LinkedIn profiles and finding relevant job matches on the Y Combinator job board. This project leverages the **Model Context Protocol (MCP)** to bypass complex web scraping challenges.

---

## 🌟 Features

* **Intelligent Profile Analysis**: Extracts professional experience, skills, and education from any public LinkedIn URL.
* **Multi-Agent Orchestration**: Utilizes 6 specialized agents (LinkedIn Analyzer, Domain Classifier, URL Generator, Job Finder, URL Parser, and Summary Agent) to process data sequentially.
* **Flexible LLM Backend**: Supports **Google Gemini** for cloud-based reasoning or **Ollama (Llama 3.1)** for completely local, private execution.
* **Anti-Bot Scraping**: Integrated with **Bright Data MCP** to navigate LinkedIn's anti-scraping measures using Web Unlocker technology.
* **Modern UI**: Clean and interactive interface built with Streamlit.

---

## 🏗️ System Architecture

The workflow follows a linear agentic pipeline:
1.  **Scrape**: Fetch raw LinkedIn data via Bright Data MCP.
2.  **Analyze**: Extract structured career insights.
3.  **Suggest**: Classify the professional domain and suggest career paths.
4.  **Search**: Generate YC job board queries and find matching roles.
5.  **Summarize**: Consolidate all findings into a final Markdown report.

---

## 📋 Prerequisites

* **Python 3.10+**
* **Node.js & npm** (Required for the Bright Data MCP server)
* **Bright Data Account**: Credentials for Web Unlocker/Scraping Browser.
* **Optional**: [Ollama](https://ollama.com/) installed locally for local LLM support.

---

## ⚙️ Setup & Installation
1.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your credentials:
    ```env
    BRIGHT_DATA_API_KEY=your_api_token
    BROWSER_AUTH=customer_id:password
    WEB_UNLOCKER_ZONE=your_zone_name
    GEMINI_API_KEY=your_google_ai_studio_key
    ```

---

## 🚀 Usage

1.  **Launch the Application**:
    ```bash
    streamlit run app.py
    ```
2.  **Input Data**:
    * Enter your **Gemini API Key** (if using cloud mode).
    * Paste the **LinkedIn Profile URL** you wish to analyze.
3.  **View Results**: The agents will process the request in the background. Progress logs are visible in the terminal.

---

## 🛠️ Troubleshooting

* **Timeout Errors**: If you encounter `Waited 5.0 seconds` errors, it's because Bright Data needs more time to render the page.
* **Rate Limits (RPM)**: Gemini's free tier is limited to **5 RPM**. If you hit this limit, consider switching to the **Ollama** configuration in `job_agents.py` for unlimited local requests.

---