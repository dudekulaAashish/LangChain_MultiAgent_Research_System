# Multi-Agent Research Studio

A Streamlit app that turns a research question into a structured report. LangChain agents and chains handle web search, page reading, report writing, and a final critique. The app presents the report and research notes in a browser and lets you download the report as Markdown.

## How it works

For each topic, the pipeline runs these steps in order:

1. **Search:** a LangChain agent uses Tavily to find recent information.
2. **Read:** another agent selects a relevant URL and extracts its page content.
3. **Write:** an OpenAI chat model combines the search results and extracted content into a report with an introduction, key findings, conclusion, and sources.
4. **Review:** a critic chain evaluates the report and returns strengths, areas to improve, and a verdict.

The Streamlit interface displays the final report, critic feedback, search results, and scraped content in separate tabs. The report can be downloaded as a `.md` file.

## Requirements

- Python 3.11 (recommended)
- An OpenAI API key
- A Tavily API key

## Setup

Create and activate the project environment, then install the dependencies:

```powershell
conda create -n langagent python=3.11 -y
conda activate langagent
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root and add your API keys:

```dotenv
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

Keep `.env` private; do not commit real API keys to version control.

## Run the app

From the project root, start Streamlit:

```powershell
streamlit run app.py
```

Open the local URL printed in the terminal, enter a research topic, and select **Run research**. Each run calls the configured OpenAI and Tavily services.

## Project structure

```text
app.py                  Streamlit research interface
src/
  agents/agents.py      Search and reader agents, writer and critic chains
  pipeline/pipeline.py  Orchestrates the research workflow
  tools/tools.py        Tavily search and web-page scraping tools
requirements.txt        Python dependencies
```
