import json
import os

from app.billing import invoice_lines
from app.tax import rate_for


def summary(items, region):
    lines = invoice_lines(items, region)
    grand = sum(cents for _, cents in lines)
    print(f"Region {region} taxed at {rate_for(region)}")
    return grand_total
