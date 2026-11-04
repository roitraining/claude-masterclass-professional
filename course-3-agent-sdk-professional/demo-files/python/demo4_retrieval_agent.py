"""Demo 4: retrieval behind a tool call. The agent talks to the local retrieval MCP server.

    python3 demo4_retrieval_agent.py
    python3 demo4_retrieval_agent.py "How long is the warranty on a sleeping bag, and which document says so?"
"""
import asyncio
import sys
from pathlib import Path

from agent_core import make_options, print_record, require_api_key, run_task

SERVER = Path(__file__).resolve().parent.parent / "retrieval" / "server.py"

SYSTEM = (
    "You answer questions about Brightwater Outfitters, a fictional retailer, using only the knowledge base. "
    "Search first, read the best document, then answer. Cite the doc_id you used. "
    "Prefer documents marked current over documents marked superseded. If nothing relevant is found, say so."
)

DEFAULT_PROMPTS = [
    "How long is the warranty on a sleeping bag, and which document says so?",
    "What is the return window?",
]


async def main(prompts: list[str]) -> None:
    require_api_key()
    options = make_options(
        SYSTEM,
        mcp_servers={"retrieval": {"command": sys.executable, "args": [str(SERVER)]}},
        allowed_tools=["mcp__retrieval__search_docs", "mcp__retrieval__read_doc"],
        max_turns=8,
        max_budget_usd=0.25,
    )
    for p in prompts:
        print_record(await run_task(p, options))


if __name__ == "__main__":
    asyncio.run(main([" ".join(sys.argv[1:])] if len(sys.argv) > 1 else DEFAULT_PROMPTS))
