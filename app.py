from flask import Flask, request, jsonify
from flask_cors import CORS
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
        return {
            "symbol": symbol,
            "interval": interval,
            "summary": analysis.summary,
            "indicators": analysis.indicators,
            "oscillators": analysis.oscillators,
            "moving_averages": analysis.moving_averages,
        }

    except Exception as e:
        return {"error": str(e)}

# ---------------- Flask API ----------------
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route("/")
def home():
    return jsonify({"message": "NSE Technical Analysis API is running 🚀"})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.json or {}
    symbol = data.get("symbol", "").strip().upper()
    interval = data.get("interval", "1d").strip()

    if not symbol:
        return jsonify({"error": "Missing 'symbol' parameter"}), 400

    result = get_ta_summary(symbol, interval)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
