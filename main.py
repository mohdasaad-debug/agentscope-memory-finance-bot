from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import AsyncSQLAlchemyMemory
from agentscope.message import TextBlock
from agentscope.tool import (
    Toolkit,
    ToolResponse,
    execute_python_code,
    execute_shell_command,
)
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from pathlib import Path
import os
import re
import json
import asyncio
import yfinance as yf

load_dotenv()


def sanitize_user_id(user_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", user_id.strip())
    return safe or "default_user"


async def get_yahoo_finance_quote(
    symbols: str,
    region: str = "US",
    lang: str = "en-US",
) -> ToolResponse:
    """Fetch near real-time Yahoo Finance quote data for ticker symbols
    using the `yfinance` Python package.

    Args:
        symbols (`str`):
            Comma-separated symbols, e.g. "AAPL,MSFT,TSLA".
        region (`str`, defaults to `"US"`):
            Kept for compatibility. Not used by yfinance.
        lang (`str`, defaults to `"en-US"`):
            Kept for compatibility. Not used by yfinance.

    Returns:
        `ToolResponse`:
            JSON payload with quote metrics per symbol.
    """
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    if not symbol_list:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text='{"error":"No symbols provided. Example: AAPL,MSFT"}',
                ),
            ],
        )

    def _to_number(value: object) -> float | int | None:
        if isinstance(value, (int, float)):
            return value
        return None

    def _fetch_symbol_quote(symbol: str) -> dict:
        ticker = yf.Ticker(symbol)
        info = ticker.info if isinstance(ticker.info, dict) else {}
        try:
            fast_info = dict(ticker.fast_info) if ticker.fast_info else {}
        except Exception:
            fast_info = {}

        return {
            "symbol": symbol,
            "name": info.get("shortName") or info.get("longName"),
            "price": _to_number(
                fast_info.get("lastPrice"),
            ) or _to_number(info.get("regularMarketPrice")),
            "change": _to_number(info.get("regularMarketChange")),
            "change_percent": _to_number(info.get("regularMarketChangePercent")),
            "currency": info.get("currency") or fast_info.get("currency"),
            "market_state": info.get("marketState"),
            "market_time": info.get("regularMarketTime"),
            "day_high": _to_number(
                fast_info.get("dayHigh"),
            ) or _to_number(info.get("regularMarketDayHigh")),
            "day_low": _to_number(
                fast_info.get("dayLow"),
            ) or _to_number(info.get("regularMarketDayLow")),
            "volume": _to_number(
                fast_info.get("lastVolume"),
            ) or _to_number(info.get("regularMarketVolume")),
            "market_cap": _to_number(
                fast_info.get("marketCap"),
            ) or _to_number(info.get("marketCap")),
            "exchange": info.get("fullExchangeName")
            or info.get("exchange")
            or fast_info.get("exchange"),
        }

    try:
        quotes = []
        for symbol in symbol_list:
            quote = await asyncio.to_thread(_fetch_symbol_quote, symbol)
            quotes.append(quote)

        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=json.dumps(
                        {
                            "requested_symbols": symbol_list,
                            "count": len(quotes),
                            "quotes": quotes,
                            "note": (
                                "Data fetched via yfinance. Quotes may be "
                                "delayed depending on exchange."
                            ),
                            "region": region,
                            "lang": lang,
                        },
                        indent=2,
                    ),
                ),
            ],
        )
    except Exception as exc:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=json.dumps(
                        {
                            "error": "Failed to fetch Yahoo Finance data.",
                            "details": str(exc),
                            "requested_symbols": symbol_list,
                        },
                        indent=2,
                    ),
                ),
            ],
        )


async def main():
    user_id = (
        input("Enter user id (for persistent memory): ").strip()
        or "default_user"
    )
    session_id = "default_session"

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
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(get_yahoo_finance_quote)

    agent = ReActAgent(
        name="Friday",
        sys_prompt="You're a helpful assistant named Friday.",
        model=OpenAIChatModel(
            model_name="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            stream=True,
        ),
        memory=memory,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
    )

    user = UserAgent(name="user")

    msg = None
    try:
        while True:
            msg = await agent(msg)
            msg = await user(msg)
            if msg.get_text_content() == "exit":
                break
    finally:
        await memory.close()
        await engine.dispose()


asyncio.run(main())
