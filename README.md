
# Multi-Agent Research System

A Streamlit-based research assistant that coordinates multiple agents and tools to perform web search, scraping, synthesis, and PDF report generation. It demonstrates an experimental pipeline combining:

- LangGraph ReAct-style agent orchestration
- Mistral AI chat model via `langchain-mistralai`
- Tavily web search (`langchain-tavily`) for retrieving candidate URLs
- A custom scraping tool (BeautifulSoup) to extract page content
- Markdown-to-PDF export using `xhtml2pdf`

This project is intended as a research/demo scaffold — adapt it to your needs and never commit secrets.

**Contents**

- `app.py` — Streamlit frontend and orchestration of the research flow (UI, PDF export).
- `agents.py` — Agent factory that constructs the LLM + LangGraph ReAct agent.
- `tools.py` — Tool definitions including the `scrape_url` tool and the Tavily search wrapper.
- `requirements.txt` — Python dependencies required to run the app.
- `.env.example` — Example environment variables (copy to `.env` and fill values locally).

**Architecture & Flow**

1. The user types a research question into the Streamlit UI (`app.py`).
2. API keys are supplied via the Streamlit sidebar or a local `.env` file and injected into environment variables.
3. `agents.get_research_agent()` (from `agents.py`) initializes a Mistral-based LLM and creates a LangGraph ReAct agent wired to the tools from `tools.get_research_tools()`.
4. The agent first uses Tavily search to find relevant URLs, optionally calls `scrape_url` to extract text from 1–2 pages, then synthesizes a final report in Markdown with a fixed structure.
5. The app displays the Markdown report and offers a PDF download generated with a styled HTML template and `xhtml2pdf`.

**Key Files Explained**

- `app.py`: Handles the Streamlit UI and higher-level orchestration.
	- Sidebar: accepts `MISTRAL_API_KEY` and `TAVILY_API_KEY` (both optional if set via `.env`).
	- `generate_pdf_from_markdown()`: Converts the Markdown report into a styled PDF byte stream.
	- Main flow: validates keys and query, constructs system + human messages, invokes the agent, shows the output, and provides a PDF download button.

- `agents.py`: Responsible for creating the language model instance and the LangGraph agent.
	- Reads `MISTRAL_API_KEY` from the environment.
	- Uses `ChatMistralAI` from `langchain_mistralai` and `create_react_agent` from `langgraph` to return a ready-to-invoke agent.

- `tools.py`: Provides the agent tools.
	- `scrape_url(url)`: A LangChain `@tool` that fetches a page and extracts headline and paragraph text via BeautifulSoup. It returns a text snippet (up to a configured length).
	- `get_research_tools()`: Initializes Tavily search with `TAVILY_API_KEY` and returns the tools list used by the agent.

**Requirements / Dependencies**

See `requirements.txt` for exact pinned versions. Important packages include `streamlit`, `langchain`, `langgraph`, `langchain-mistralai`, `langchain-tavily`, `beautifulsoup4`, `xhtml2pdf`, and `python-dotenv`.

**Environment Variables**

- `MISTRAL_API_KEY` — API key for Mistral LLM access (used by `agents.py`).
- `TAVILY_API_KEY` — API key for Tavily search (used by `tools.py`).

Do not commit actual keys. Use `.env.example` as a template and add `.env` to `.gitignore`.

**Setup (Windows example)**

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy the environment example and fill in keys locally:

```powershell
copy .env.example .env
# then edit .env with your editor and paste keys
```

4. Run the Streamlit app:

```powershell
streamlit run app.py
```

**Usage Notes & Safety**

- The app will prompt for API keys in the sidebar if they are not present in environment variables.
- The `scrape_url` tool performs HTTP requests and parses HTML. Use responsibly and respect robots.txt and site terms.
- The project is a research/demo scaffold — review and harden before any production use.

**Extending the Project**

- Add more tools (fact-checkers, citation extractors, PDF metadata, or HTML sanitizers).
- Replace or extend the agent prompts and system instructions in `app.py`.
- Add caching for search/scrape results to reduce repeated network calls.

**Contributing**

If you'd like contributions:

1. Fork the repo.
2. Create a feature branch.
3. Send a pull request describing your changes.

**License**

This project does not include a license file yet. If you want, add an open-source license such as MIT or Apache-2.0.

**Contact**

Project owner / repo: https://github.com/challasumanth64/Multi-AI-Agent-Research-System

