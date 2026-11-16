"""Formatting helpers — energy (kWh) and power (kW) are labelled distinctly."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation


def num(value, digits: int = 1) -> str:
    if value is None:
        return "—"
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return str(value)
    fmt = f"{d:,.{digits}f}"
    return fmt.replace(",", " ")


def kwh(value, digits: int = 1) -> str:
    return f"{num(value, digits)} kWh"


def kw(value, digits: int = 1) -> str:
    return f"{num(value, digits)} kW"


def money(value, currency: str = "UZS") -> str:
    if value is None:
        return "—"
    return f"{num(value, 0)} {currency}"


def pct(value) -> str:
    if value is None:
        return "—"
    sign = "+" if Decimal(str(value)) > 0 else ""
    return f"{sign}{num(value, 1)}%"


def dashboard_text(data: dict, language: str, label: str) -> str:
    """Render a dashboard summary. Purely presentational: no numbers are computed."""
    from bots.common.i18n import t

    if not data.get("has_data"):
        return t(language, "no_data")
    consumption = data["consumption"]
    cost = data["cost"]
    trend = data["trend"]
    lines = [
        t(language, "dashboard_title", org="—", period=label).replace("<b>—</b>", ""),
        f"{t(language, 'kwh')}: <b>{kwh(consumption['total_kwh'], 2)}</b>",
        f"{t(language, 'cost')}: "
        + (money(cost["estimated"], cost["currency"]) if cost.get("estimated") is not None
           else t(language, "no_tariff")),
        f"{t(language, 'coverage')}: {num(consumption['data_coverage_pct'], 1)}%",
        f"{t(language, 'anomaly_count')}: {data['anomalies']['count']}",
    ]
    if trend.get("vs_previous_period_pct") is not None:
        lines.append(f"{t(language, 'trend')}: <b>{pct(trend['vs_previous_period_pct'])}</b>")
    return "\n".join(lines)
