"""Fake backend for Brightwater Outfitters. A thin accessor over data/shop.json.

This module stands in for a real order system. All data is fictional.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_SHOP = json.loads((DATA_DIR / "shop.json").read_text(encoding="utf-8"))
_NOTES = json.loads((DATA_DIR / "order_notes.json").read_text(encoding="utf-8"))

AS_OF: str = _SHOP["as_of"]
POLICY_TOPICS: list[str] = sorted(_SHOP["policies"])
ORDER_ID_RE = re.compile(r"^BW-\d{4}$")


def get_order(order_id: str) -> dict | None:
    """Return the order record for an id such as BW-1003, or None.

    The record carries ``as_of`` so date questions ("can I still return this?")
    are answered against the fixture's own date rather than whatever the model
    believes today is. Without it the return-window answers drift as real time
    passes the window.
    """
    key = (order_id or "").strip().upper()
    rec = _SHOP["orders"].get(key)
    return {"order_id": key, "as_of": AS_OF, **rec} if rec else None


def get_customer(email: str) -> dict | None:
    """Return the customer record for an email address, or None."""
    key = (email or "").strip().lower()
    rec = _SHOP["customers"].get(key)
    return {"email": key, **rec} if rec else None


def get_policy(topic: str) -> str | None:
    """Return policy text for one of POLICY_TOPICS (exact match), or None."""
    return _SHOP["policies"].get((topic or "").strip())


def get_notes(order_id: str) -> list[str] | None:
    """Return the notes for an order. Used by the Lab 2 MCP server."""
    key = (order_id or "").strip().upper()
    if key not in _SHOP["orders"]:
        return None
    return list(_NOTES.get(key, []))
