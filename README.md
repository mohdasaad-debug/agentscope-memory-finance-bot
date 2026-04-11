<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&width=1400&height=220&text=AgentScope%20Memory%20Finance%20Bot&fontAlign=50&fontAlignY=38&fontSize=52&color=0:0ea5e9,100:22c55e&animation=fadeIn&fontColor=ffffff" alt="header"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2500&pause=1000&center=true&vCenter=true&width=700&lines=Persistent+AI+Memory+per+User;Live+Yahoo+Finance+Data+with+yfinance;Built+with+AgentScope+%2B+ReActAgent" alt="typing animation"/>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.12%2B-blue.svg" alt="python"></a>
  <a href="https://pypi.org/project/yfinance/"><img src="https://img.shields.io/badge/Data-yfinance-16a34a" alt="yfinance"></a>
  <a href="https://docs.agentscope.io/"><img src="https://img.shields.io/badge/Framework-AgentScope-0ea5e9" alt="agentscope"></a>
  <img src="https://img.shields.io/badge/Memory-SQLite%20Per%20User-f59e0b" alt="memory">
</p>

## Overview

**AgentScope Memory Finance Bot** is an AI finance assistant that combines:
- Per-user persistent memory in SQLite
- Live market quote access through `yfinance`
- Tool-enabled reasoning with AgentScope `ReActAgent`

This project is a practical starter for building production-style personal AI agents.

## Features

- Persistent memory in `memories/<user_id>.db`
- Finance quote tool: `get_yahoo_finance_quote`
- Extra agent tools: `execute_python_code`, `execute_shell_command`
- Async resource lifecycle (clean DB close/dispose)
- User-specific memory isolation with safe user-id sanitization

## Project Structure

```text
.
|-- main.py
|-- pyproject.toml
|-- uv.lock
|-- .env
`-- memories/      # created automatically at runtime
```

## Quick Start

### 1. Clone

```bash
git clone https://github.com/pawan941394/agentscope-memory-finance-bot.git
cd agentscope-memory-finance-bot
```

### 2. Install dependencies

```bash
uv sync
```

If `agentscope` is not already installed:

```bash
uv add "agentscope[full]"
```

### 3. Add environment variables

Create `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run

```bash
uv run .\main.py
```

At startup:

```text
Enter user id (for persistent memory):
```

Use the same `user_id` on future runs to continue that user’s memory.

## Example Prompts

- `Use get_yahoo_finance_quote for AAPL,MSFT,TSLA and summarize the market move.`
- `Fetch NVDA quote and compare it with AMD in short bullet points.`
- `What do you remember about my investment preferences?`

## Memory Design

- Backend: `AsyncSQLAlchemyMemory`
- Storage file: `memories/<sanitized_user_id>.db`
- Session: `default_session` (can be extended later)

## Notes

- Data is fetched through `yfinance` (not direct Yahoo endpoint calls in your code).
- Some quote fields may be delayed depending on exchange.
- This project is educational and not financial advice.

## Roadmap

- Historical OHLCV tool (`period`, `interval`)
- Technical indicators (SMA, EMA, RSI)
- Watchlist and preference memory modules
- Streamlit/FastAPI UI

## Contributing

PRs and suggestions are welcome.  
If this project helps you, drop a star on the repo.

## License

MIT

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=120&color=0:22c55e,100:0ea5e9" alt="footer"/>
</p>
