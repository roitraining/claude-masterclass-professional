from app.tax import rate_for


def total_with_tax(subtotal_cents, region):
    """Return the total in cents including tax for the region."""
    return round(subtotal_cents * (1 + rate_for(region)))


def invoice_lines(items, region):
    lines = []
    for name, cents in items:
        lines.append((name, total_with_tax(cents, region)))
    return lines
