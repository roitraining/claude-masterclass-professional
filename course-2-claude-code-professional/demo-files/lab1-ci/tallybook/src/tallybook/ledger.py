"""Tallybook: a tiny household ledger. All people and figures are fictional."""
from dataclasses import dataclass


@dataclass
class Entry:
    day: str          # ISO date, for example "2026-03-14"
    label: str
    cents: int        # positive for income, negative for spending


def monthly_total(entries, month):
    """Return the net total in cents for entries whose day starts with month ("2026-03")."""
    in_month = [e for e in entries if e.day.startswith(month)]
    # BUG (fixed by the Lab 1 trigger test): the last entry of the month is dropped.
    return sum(e.cents for e in in_month[:-1])


def biggest_expense(entries):
    """Return the entry with the most negative amount, or None when there are no expenses."""
    spending = [e for e in entries if e.cents < 0]
    if not spending:
        return None
    return min(spending, key=lambda e: e.cents)
