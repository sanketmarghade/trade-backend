# trading_analysis.py
from tradingview_ta import TA_Handler, Interval, Exchange
from typing import Dict, Any

class InvalidSymbolError(Exception):
    pass

# Map friendly interval strings to tradingview_ta Interval constants
_INTERVAL_MAP = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "30m": Interval.INTERVAL_30_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "2h": Interval.INTERVAL_2_HOURS,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY,
    "1w": Interval.INTERVAL_1_WEEK,
    "1M": Interval.INTERVAL_1_MONTH,
}

def _map_interval(interval: str):
    interval = (interval or "1d").strip()
    return _INTERVAL_MAP.get(interval, Interval.INTERVAL_1_DAY)

def get_ta_summary(symbol: str, screener: str = "america", exchange: str = "NASDAQ", interval: str = "1d") -> Dict[str, Any]:
    """
    Returns a dict containing:
      - symbol, screener, exchange, interval
      - analysis summary (recommendation counts)
      - indicators (raw indicators dict from tradingview_ta)
      - moving averages and oscillators (if available)
    Raises InvalidSymbolError if tradingview_ta can't find the symbol.
    """
    if not symbol or not symbol.strip():
        raise InvalidSymbolError("symbol is empty")

    tv_interval = _map_interval(interval)

    handler = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=tv_interval
    )

    try:
        analysis = handler.get_analysis()
    except Exception as e:
        # tradingview_ta raises for invalid symbols or network issues. Wrap to give a clearer message.
        raise InvalidSymbolError(f"failed to get analysis for {symbol} on {exchange}/{screener} ({interval}): {e}")

    # analysis object has several attributes. We'll extract the most useful ones.
    result = {
        "symbol": symbol,
        "screener": screener,
        "exchange": exchange,
        "interval": interval,
        "summary": analysis.summary if hasattr(analysis, "summary") else None,
        "indicators": analysis.indicators if hasattr(analysis, "indicators") else None,
    }

    # moving_averages and oscillators are properties if available
    if hasattr(analysis, "moving_averages"):
        result["moving_averages"] = analysis.moving_averages
    if hasattr(analysis, "oscillators"):
        result["oscillators"] = analysis.oscillators

    # Optionally include extra info if present
    try:
        if hasattr(analysis, "time"):
            result["analysis_time"] = str(analysis.time)
    except Exception:
        pass

    return result
