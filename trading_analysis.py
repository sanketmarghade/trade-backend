from tradingview_ta import TA_Handler, Interval
from typing import Dict, Any

class InvalidSymbolError(Exception):
    pass

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
}

_DEFAULT_SCREENER = "india"
_DEFAULT_EXCHANGE = "NSE"   # use string, not Exchange.NSE

def get_ta_summary(symbol: str, interval: str = "1d") -> Dict[str, Any]:
    symbol = symbol.strip().upper()
    if not symbol:
        raise InvalidSymbolError("empty symbol")

    if interval not in _INTERVAL_MAP:
        raise InvalidSymbolError(f"unsupported interval: {interval}")

    handler = TA_Handler(
        symbol=symbol,
        screener=_DEFAULT_SCREENER,
        exchange=_DEFAULT_EXCHANGE,
        interval=_INTERVAL_MAP[interval],
    )

    try:
        analysis = handler.get_analysis()
    except Exception as e:
        raise InvalidSymbolError(f"failed to fetch TA for {symbol}: {e}")

    return {
        "symbol": symbol,
        "interval": interval,
        "summary": analysis.summary,
        "indicators": analysis.indicators,
    }
