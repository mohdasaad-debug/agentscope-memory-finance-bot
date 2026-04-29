<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&width=1400&height=220&text=AgentScope%20Memory%20Finance%20Bot&fontAlign=50&fontAlignY=38&fontSize=52&color=0:0ea5e9,100:22c55e&animation=fadeIn&fontColor=ffffff" alt="header"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2500&pause=1000&center=true&vCenter=true&width=700&lines=Persistent+AI+Memory+per+User;Local+LLM+via+Ollama+(Llama3.2);Live+Yahoo+Finance+Data+with+yfinance;Built+with+AgentScope+%2B+ReActAgent" alt="typing animation"/>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="python"></a>
  <a href="https://ollama.com/"><img src="https://img.shields.io/badge/LLM-Ollama%20Local%20Model-black" alt="ollama"></a>
  <a href="https://pypi.org/project/yfinance/"><img src="https://img.shields.io/badge/Data-yfinance-16a34a" alt="yfinance"></a>
  <a href="https://docs.agentscope.io/"><img src="https://img.shields.io/badge/Framework-AgentScope-0ea5e9" alt="agentscope"></a>
  <img src="https://img.shields.io/badge/Memory-SQLite%20Per%20User-f59e0b" alt="memory">
</p>

## Overview

**AgentScope Memory Finance Bot** is a local-first AI finance assistant that combines:

* Persistent per-user memory stored in SQLite
* Local LLM inference using **Ollama (Llama 3.2)**
* Live market data via `yfinance`
* Tool-augmented reasoning using AgentScope `ReActAgent`

This project is designed for **fully local execution (no OpenAI dependency)**.

---

## Features

* 🧠 Persistent memory per user (`memories/<user_id>.db`)
* 🏦 Stock market quotes via `yfinance`
* 🤖 Local LLM via Ollama (`llama3.2:3b`)
* 🔧 Tool-based reasoning (ReAct agent architecture)
* ⚡ Async memory + engine lifecycle management

---

## Project Structure

```text
.
|-- main.py
|-- pyproject.toml
|-- uv.lock
|-- .env (optional, not required for LLM)
`-- memories/      # auto-created at runtime
```

---

## Local Setup (IMPORTANT)

### 1. Prerequisites

Install:

* Python 3.12+
* Ollama

Check Python:

```bash
python --version
```

---

### 2. Install Ollama (Required)

Install Ollama:
[https://ollama.com/download](https://ollama.com/download)

Then pull the model:

```bash
ollama pull llama3.2:3b
```

Start server:

```bash
ollama serve
```

Ensure it runs on:

```text
http://localhost:11434
```

---

### 3. Create project

```bash
git clone https://github.com/pawan941394/agentscope-memory-finance-bot.git
cd agentscope-memory-finance-bot
```

or

```bash
mkdir agentscope-memory-finance-bot
cd agentscope-memory-finance-bot
```

---

### 4. Virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
.venv\Scripts\activate      # windows
```

---

### 5. Install dependencies

```bash
pip install agentscope sqlalchemy aiosqlite yfinance
```

or

```bash
uv sync
```

---

## Run the app

```bash
python main.py
```

You will see:

```text
Enter user id:
```

Use same user_id to continue memory across sessions.

---

## How it works (Architecture)

* **Agent:** AgentScope `ReActAgent`
* **Model:** Ollama (`llama3.2:3b`)
* **Memory:** AsyncSQLAlchemyMemory (SQLite per user)
* **Tool:** Yahoo Finance via `yfinance`

---

## Tool: Stock Quotes

Example tool input:

```text
AAPL, MSFT, TSLA
```

Output includes:

* Price
* Change
* Volume
* Day high/low

---

## Example Prompts

* “Get AAPL, MSFT and summarize market movement”
* “Compare NVDA vs AMD performance”
* “What do you remember about my investing style?”

---

## Memory Design

* Stored in: `memories/<sanitized_user_id>.db`
* Backend: SQLite (async)
* Session: `default_session`

---

## Notes

* Fully local LLM (no OpenAI API required)
* Market data is via `yfinance` (may be delayed)
* Designed for learning agent systems + tool use

---

## Troubleshooting

### Ollama not responding

```bash
ollama serve
```

### Model missing

```bash
ollama pull llama3.2:3b
```

### Import errors

```bash
pip install agentscope sqlalchemy aiosqlite yfinance
```

---

## Roadmap

* Streamlit UI/FE
* Multi-agent finance assistant

---

## Contributing

PRs welcome. Keep it simple, local-first, and modular.

---

## License

MIT

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=120&color=0:22c55e,100:0ea5e9" alt="footer"/>
</p>
