# Multi-Agent AI Research System

An advanced Multi-Agent AI Research System built using LangChain, LCEL Runnable Pipelines, Tavily Search, Firecrawl Web Scraping, and Groq LLMs.

This project demonstrates how multiple AI agents collaborate using tools, reasoning, and web intelligence to perform deep research tasks automatically.

---

# Features

- Multi-Agent AI Architecture
- Tavily Search Integration
- Firecrawl Web Scraping
- ReAct Agent Framework
- LCEL Runnable Pipelines
- LangChain Tool Calling
- Streamlit User Interface
- Rich Terminal Output
- Modular Code Structure
- Environment Variable Support
- Groq LLM Integration

---

# Tech Stack

- Python
- LangChain
- LCEL (LangChain Expression Language)
- Groq API
- Tavily AI
- Firecrawl
- Streamlit
- Rich

---

# Project Structure

```bash
Multi Agent System/
│
├── .venv/
├── __pycache__/
├── .env
├── .gitignore
├── agents.py
├── app.py
├── pipeline.py
├── tools.py
├── requirements.txt

How It Works :-

User enters a research query
Search Agent searches the web using Tavily
Scraper Agent extracts webpage content using Firecrawl
ReAct Agent analyzes and reasons over collected data
LCEL pipeline processes the workflow
Final AI-generated research response is displayed

Installation

1. Create Virtual Environment
Windows
python -m venv .venv
.\.venv\Scripts\activate

Linux / Mac
python3 -m venv .venv
source .venv/bin/activate

2. Install Dependencies
python -m pip install -r requirements.txt

Requirements :-

langchain==0.2.17
langchain-core==0.2.43
langchain-community==0.2.19
langchain-groq==0.1.10
python-dotenv==1.0.1
requests==2.32.3
firecrawl-py
tavily-python
rich==13.7.1
streamlit

Environment Variables ---->

Create a .env file in the root directory.

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key

Running the Project ----->

Run with Python
python app.py

Run with Streamlit
streamlit run app.py

Core Components ----->

Tavily Search Tool - Used for intelligent web searching and retrieval.

Firecrawl - Used for extracting clean webpage content from URLs.

ReAct Agent - Handles reasoning and decision-making using tools.

LCEL Runnable Pipeline - Manages execution flow and orchestration between agents.

Groq LLM - Acts as the reasoning engine powering the agents.

Future Improvements --->

Multi-Agent Collaboration Graphs
PDF Research Report Generation
Memory Support
Vector Database Integration
Autonomous Research Loops
Streaming Responses
Source Citation System
Voice-Based Query Input

Use Cases ;-

AI Research Assistant
Automated Research Pipelines
Deep Web Research
Academic Research Support
AI Agent Experiments
LLM Workflow Demonstration

Author

Sania Khandakar

B.Tech CST

License

This project is for educational and research purposes.
