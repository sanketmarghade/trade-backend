from flask import Flask, request, jsonify
from trading_analysis import get_ta_summary, InvalidSymbolError

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "TradingView_TA API for Indian market (NSE) is running."})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.json or {}
    symbol = (data.get("symbol") or "").strip()
    interval = (data.get("interval") or "1d").strip()

    if not symbol:
        return jsonify({"error": "symbol is required"}), 400

    try:
        result = get_ta_summary(symbol=symbol, interval=interval)
    except InvalidSymbolError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "internal error", "detail": str(e)}), 500

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
