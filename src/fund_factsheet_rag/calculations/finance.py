from decimal import Decimal
import numpy as np
import re

def cagr(start_value: float, end_value: float, years: float) -> float:
    return float((Decimal(end_value) / Decimal(start_value)) ** (Decimal(1) / Decimal(years)) - Decimal(1))

def calculate_cagr(start_value: float, end_value: float, years: float) -> float:
    """Wrapper for cagr function - calculates compound annual growth rate"""
    return cagr(start_value, end_value, years)

def parse_numeric_value(text: str) -> float:
    """
    Extract numeric value from text string
    Handles formats like: "12.5%", "Rs. 1,234.56", "1234.56"
    """
    if not text:
        return 0.0

    # Remove currency symbols, commas, and percentage signs
    cleaned = re.sub(r'[Rs.,₹%\s]', '', str(text))

    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0

def sharpe_ratio(returns, risk_free_rate, periods_per_year):
    arr = np.array(returns)
    excess = arr - (risk_free_rate / periods_per_year)
    ann_excess = np.mean(excess) * periods_per_year
    ann_vol = np.std(arr, ddof=1) * np.sqrt(periods_per_year)
    return float(ann_excess / ann_vol)
