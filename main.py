
from tradingview_ta import TA_Handler, Interval, exceptions as tv_exceptions

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
    Get TradingView technical analysis summary for an Indian stock.
    Example: symbol="RELIANCE", exchange="NSE", screener="india"
    """
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=get_interval_constant(interval)
        )
        analysis = handler.get_analysis()
        return {
            "summary": analysis.summary,
            "indicators": analysis.indicators,
        }
    except tv_exceptions.NoData:
        raise Exception("No data returned. Check symbol/exchange/screener.")
