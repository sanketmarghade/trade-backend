from tradingview_ta import TA_Handler, Interval, Exchange

# Map friendly interval strings to tradingview_ta constants
INTERVAL_MAP = {
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


def get_ta_summary(symbol: str, interval: str = "1d"):
    """
    Get technical analysis summary for an Indian stock (NSE).
    
    Args:
        symbol (str): NSE stock symbol (e.g., "RELIANCE", "TCS", "INFY").
        interval (str): Time interval (default: "1d").
    
    Returns:
        dict: Analysis summary or error message
    """
    try:
        if interval not in INTERVAL_MAP:
            raise ValueError(f"Invalid interval '{interval}'. Use one of: {list(INTERVAL_MAP.keys())}")

        handler = TA_Handler(
            symbol=symbol,
            screener="india",   # For Indian stocks
            exchange="NSE",     # National Stock Exchange
            interval=INTERVAL_MAP[interval]
        )

        analysis = handler.get_analysis()

        if analysis is None:  # <-- prevent NoneType errors
            return {"error": f"No analysis available for symbol '{symbol}' on interval '{interval}'."}

        return {
            "symbol": symbol,
            "interval": interval,
            "summary": getattr(analysis, "summary", {}),
            "indicators": getattr(analysis, "indicators", {}),
            "oscillators": getattr(analysis, "oscillators", {}),
            "moving_averages": getattr(analysis, "moving_averages", {}),
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Example usage
    symbol = input("Enter NSE stock symbol (e.g., RELIANCE, TCS, INFY): ").strip().upper()
    interval = input("Enter interval (1m,5m,15m,30m,1h,2h,4h,1d,1w,1M): ").strip()

    if not interval:
        interval = "1d"  # default

    result = get_ta_summary(symbol, interval)
    print("\n=== Technical Analysis Result ===")
    print(result)
