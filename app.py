# app.py
import os
from flask import Flask, request, jsonify
from trading_analysis import get_ta_summary, InvalidSymbolError

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "ok", "msg": "TradingView TA backend running"})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    POST JSON body:
    {
      "symbol": "AAPL",
      "screener": "america",       # optional, default "america"
      "exchange": "NASDAQ",        # optional, default "NASDAQ"
      "interval": "1d"             # optional: "1m","5m","15m","1h","1d",...
    }
    """
    data = request.get_json(force=True, silent=True) or {}
    symbol = (data.get("symbol") or "").strip()
    if not symbol:
        return jsonify({"error": "missing 'symbol' in request body"}), 400

    screener = data.get("screener", "america")
    exchange = data.get("exchange", "NASDAQ")
    interval = data.get("interval", "1d")

    try:
        result = get_ta_summary(symbol=symbol, screener=screener, exchange=exchange, interval=interval)
    except InvalidSymbolError as e:
        return jsonify({"error": "invalid_symbol", "message": str(e)}), 400
    except Exception as e:
        # For production, you might want to log this to stderr or an external logger
        return jsonify({"error": "analysis_failed", "message": str(e)}), 500

    return jsonify(result), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # for Render use $PORT; locally default 5000
    app.run(host="0.0.0.0", port=port)
