"""Tax rates for the fictional Brightwater storefront."""

RATES = {"north": 0.05, "south": 0.08, "west": 0.0}


def rate_for(region):
    """Return the tax rate for a region, or 0.0 when the region is unknown."""
    return RATES.get(region, 0.0)
