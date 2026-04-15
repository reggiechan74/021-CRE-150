"""
Financial Utilities — minimal extraction for tenant-credit plugin.

Provides safe_divide and calculate_financial_ratios used by credit_analysis.py.
Extracted from Shared_Utils/financial_utils.py in vp-real-estate (2025-10-30).
Only the two functions required by credit_analysis.py are included here to avoid
pulling in the scipy/numpy-financial dependencies of the full shared module.
"""

from typing import Dict, Optional


def safe_divide(
    numerator: float,
    denominator: float,
    default: Optional[float] = None
) -> Optional[float]:
    """
    Safely perform division, handling division by zero.

    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Value to return if denominator is 0 (None if not specified)

    Returns:
        Result of division, or default if denominator is 0
    """
    if denominator == 0:
        return default
    return numerator / denominator


def calculate_financial_ratios(financial_data: Dict[str, float]) -> Dict[str, Optional[float]]:
    """
    Calculate comprehensive set of financial ratios.

    Args:
        financial_data: Dictionary containing financial statement items (balance sheet
        and income statement line items plus annual_rent for rent coverage ratios).

    Returns:
        Dictionary of calculated ratios with None for ratios that cannot be calculated.
    """
    ratios = {}

    # Liquidity Ratios
    ratios['current_ratio'] = safe_divide(
        financial_data.get('current_assets', 0),
        financial_data.get('current_liabilities', 0)
    )

    ratios['quick_ratio'] = safe_divide(
        financial_data.get('current_assets', 0) - financial_data.get('inventory', 0),
        financial_data.get('current_liabilities', 0)
    )

    ratios['cash_ratio'] = safe_divide(
        financial_data.get('cash_and_equivalents', 0),
        financial_data.get('current_liabilities', 0)
    )

    # Leverage Ratios
    ratios['debt_to_equity'] = safe_divide(
        financial_data.get('total_liabilities', 0),
        financial_data.get('shareholders_equity', 0)
    )

    ratios['debt_to_assets'] = safe_divide(
        financial_data.get('total_liabilities', 0),
        financial_data.get('total_assets', 0)
    )

    ratios['interest_coverage'] = safe_divide(
        financial_data.get('ebit', 0),
        financial_data.get('interest_expense', 0)
    )

    # Profitability Ratios
    ratios['net_profit_margin'] = safe_divide(
        financial_data.get('net_income', 0),
        financial_data.get('revenue', 0)
    )

    ratios['roa'] = safe_divide(
        financial_data.get('net_income', 0),
        financial_data.get('total_assets', 0)
    )

    ratios['roe'] = safe_divide(
        financial_data.get('net_income', 0),
        financial_data.get('shareholders_equity', 0)
    )

    ratios['gross_margin'] = safe_divide(
        financial_data.get('gross_profit', 0),
        financial_data.get('revenue', 0)
    )

    # Rent Coverage Ratios (lease-specific)
    ratios['rent_to_revenue'] = safe_divide(
        financial_data.get('annual_rent', 0),
        financial_data.get('revenue', 0)
    )

    ratios['ebitda_to_rent'] = safe_divide(
        financial_data.get('ebitda', 0),
        financial_data.get('annual_rent', 0)
    )

    # Working Capital
    ratios['working_capital'] = (
        financial_data.get('current_assets', 0) -
        financial_data.get('current_liabilities', 0)
    )

    return ratios
