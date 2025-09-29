from tradingview_ta import TA_Handler, Interval, Exchange
from tradingview_ta import exceptions as tv_exceptions

# map common interval strings -> Interval constants
INTERVAL_MAP = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "30m": Interval.INTERVAL_30_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY,
    "1w": Interval.INTERVAL_1_WEEK,
    "1M": Interval.INTERVAL_1_MONTH,
}

def get_interval_constant(interval_str: str):
    return INTERVAL_MAP.get(interval_str, Interval.INTERVAL_1_DAY)

def get_ta_summary(symbol: str, screener: str = "india", exchange: str = "NSE", interval: str = "1d"):
    """
    Returns tradingview_ta analysis summary for a given symbol.
    Use symbol like "RELIANCE" and exchange "NSE", screener "india".
    """
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=get_interval_constant(interval)
        )
        analysis = handler.get_analysis()
        # main summary recommendation + indicator values
        summary = {
            "RECOMMENDATION": analysis.summary.get("RECOMMENDATION"),
            "BUY": analysis.summary.get("BUY"),
            "NEUTRAL": analysis.summary.get("NEUTRAL"),
            "SELL": analysis.summary.get("SELL"),
            # raw indicators (a subset)
            "indicators": analysis.indicators,
            "oscillators": analysis.moving_averages if hasattr(analysis, "moving_averages") else {},
        }
        return summary
    except tv_exceptions.NoData:
        raise Exception("No data returned for symbol/exchange/screener. Check symbol and that the market is open.")
    except Exception as e:
        # surface the underlying error
        raise
