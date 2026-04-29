from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import OllamaChatModel
from agentscope.memory import AsyncSQLAlchemyMemory
from agentscope.message import TextBlock
from agentscope.tool import Toolkit, ToolResponse
from agentscope.formatter import OllamaChatFormatter

from sqlalchemy.ext.asyncio import create_async_engine
from pathlib import Path
import re
import json
import asyncio
import yfinance as yf


# ------------------------
# utils
# ------------------------
def sanitize_user_id(user_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", user_id.strip())
    return safe or "default_user"


def parse_symbols(symbols: str) -> list[str]:
    try:
        parsed = json.loads(symbols)
        if isinstance(parsed, list):
            return [str(s).upper() for s in parsed]
    except Exception:
        pass

    cleaned = (
        symbols.replace("[", "")
        .replace("]", "")
        .replace('"', "")
        .replace("'", "")
    )
    return [s.strip().upper() for s in cleaned.split(",") if s.strip()]


# ------------------------
# tool
# ------------------------
async def get_yahoo_finance_quote(symbols: str) -> ToolResponse:
    """Fetch stock quotes using yfinance"""

    symbol_list = parse_symbols(symbols)

    if not symbol_list:
        return ToolResponse(
            content=[TextBlock(type="text", text='{"error":"No symbols provided"}')]
        )

    def _to_number(value):
        return value if isinstance(value, (int, float)) else None

    def _fetch(symbol):
        ticker = yf.Ticker(symbol)
        info = ticker.info if isinstance(ticker.info, dict) else {}

        try:
            fast_info = dict(ticker.fast_info) if ticker.fast_info else {}
        except Exception:
            fast_info = {}

        return {
            "symbol": symbol,
            "name": info.get("shortName") or info.get("longName"),
            "price": _to_number(fast_info.get("lastPrice"))
            or _to_number(info.get("regularMarketPrice")),
            "change": _to_number(info.get("regularMarketChange")),
            "change_percent": _to_number(info.get("regularMarketChangePercent")),
            "currency": info.get("currency"),
            "day_high": _to_number(fast_info.get("dayHigh")),
            "day_low": _to_number(fast_info.get("dayLow")),
            "volume": _to_number(fast_info.get("lastVolume")),
        }

    try:
        quotes = []
        for symbol in symbol_list:
            quote = await asyncio.to_thread(_fetch, symbol)
            quotes.append(quote)

        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=json.dumps(
                        {
                            "quotes": quotes,
                            "count": len(quotes),
                            "note": "Data via yfinance (may be delayed)",
                        },
                        indent=2,
                    ),
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2),
                )
            ]
        )

# ------------------------
# agent factory (FOR UI)
# ------------------------
async def create_agent(user_id: str):
    session_id = "streamlit_session"

    memory_dir = Path("memories")
    memory_dir.mkdir(parents=True, exist_ok=True)
    db_path = memory_dir / f"{sanitize_user_id(user_id)}.db"

    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path.as_posix()}")
    memory = AsyncSQLAlchemyMemory(
        engine_or_session=engine,
        session_id=session_id,
        user_id=user_id,
    )

    toolkit = Toolkit()
    toolkit.register_tool_function(get_yahoo_finance_quote)

    model = OllamaChatModel(
        model_name="llama3.2:3b",
        host="http://localhost:11434",
        stream=True,
    )

    agent = ReActAgent(
        name="Friday",
        sys_prompt="""
You are Friday, a helpful assistant.

Rules:
- Be concise
- Use tools when needed
- Tool arguments MUST be valid JSON objects
""",
        model=model,
        memory=memory,
        formatter=OllamaChatFormatter(),
        toolkit=toolkit,
    )

    return agent, memory, engine

# ------------------------
# main
# ------------------------
async def main():
    user_id = input("Enter user id: ").strip() or "default_user"
    session_id = "default_session"

    # memory
    memory_dir = Path("memories")
    memory_dir.mkdir(parents=True, exist_ok=True)
    db_path = memory_dir / f"{sanitize_user_id(user_id)}.db"

    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path.as_posix()}")
    memory = AsyncSQLAlchemyMemory(
        engine_or_session=engine,
        session_id=session_id,
        user_id=user_id,
    )

    # toolkit
    toolkit = Toolkit()
    toolkit.register_tool_function(get_yahoo_finance_quote)

    # ✅ LOCAL MODEL (Ollama)
    model = OllamaChatModel(
        model_name="llama3.2:3b",  # 🔥 best for your machine
        host="http://localhost:11434",
        stream=True,
    )

    # agent
    agent = ReActAgent(
        name="Friday",
        sys_prompt="""
You are Friday, a helpful assistant.

Rules:
- Be concise
- Use tools when needed
- Tool arguments MUST be valid JSON objects
""",
        model=model,
        memory=memory,
        formatter=OllamaChatFormatter(),
        toolkit=toolkit,
    )

    user = UserAgent(name="user")

    msg = None
    try:
        while True:
            msg = await agent(msg)
            msg = await user(msg)

            if msg.get_text_content().strip().lower() == "exit":
                break
    finally:
        await memory.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())