"""Demo 3: a small standalone MCP server over stdio. Two tools, deterministic results, fictional rates.

The agent in demo3_agent.py starts this file as a child process. Never print to stdout; it carries the protocol.
"""
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # newer releases
    from mcp.server import MCPServer as FastMCP  # type: ignore

mcp = FastMCP("rates")

ZONES = {"A": (5.00, 1.20), "B": (7.50, 1.80), "C": (12.00, 2.60)}  # base price, price per kilogram


@mcp.tool()
def list_zones() -> str:
    """List the shipping zones this server can quote: A, B and C. Use before quote_shipping if the customer has not named a zone."""
    return "Zones: A (home region), B (neighboring regions), C (remote areas)."


@mcp.tool()
def quote_shipping(weight_kg: float, zone: str) -> str:
    """Quote the shipping price for one package. Inputs: weight_kg in kilograms and zone, one of A, B or C. Returns the price in dollars. Do not use for returns or for delivery-time questions."""
    key = zone.strip().upper()
    if key not in ZONES:
        return f"Unknown zone {zone!r}. Valid zones: A, B, C."
    base, per_kg = ZONES[key]
    return f"Zone {key}, {weight_kg} kg: {base + per_kg * weight_kg:.2f} dollars."


if __name__ == "__main__":
    print("rates server starting", file=sys.stderr, flush=True)
    mcp.run(transport="stdio")
