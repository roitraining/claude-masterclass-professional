from tallybook.ledger import Entry, biggest_expense, monthly_total

ENTRIES = [
    Entry("2026-03-01", "pay", 250000),
    Entry("2026-03-05", "rent", -120000),
    Entry("2026-03-30", "groceries", -8450),
    Entry("2026-04-01", "pay", 250000),
]


def test_monthly_total_includes_every_entry_in_the_month():
    assert monthly_total(ENTRIES, "2026-03") == 121550


def test_monthly_total_other_month():
    assert monthly_total(ENTRIES, "2026-04") == 250000


def test_biggest_expense():
    assert biggest_expense(ENTRIES).label == "rent"


def test_biggest_expense_none():
    assert biggest_expense([Entry("2026-03-01", "pay", 1)]) is None
