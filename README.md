# Render + TradingView_TA — Indian Market

Simple Flask app that uses `python-tradingview-ta` to fetch TradingView technical analysis for Indian stocks (NSE).

## Quick start (locally)
1. `git clone <repo>`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python app.py` (opens on http://localhost:5000)

## Deploy to Render
1. Push this repo to GitHub.
2. On Render, create a new **Web Service** → Connect your GitHub repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 3`
5. Set environment variable `PORT` if necessary (Render sets $PORT automatically).

## Notes
- Use `symbol` as the ticker (e.g., `RELIANCE`), `exchange` should be `NSE`, and `screener` typically `india`. Confirm exact naming with the TradingView list (tvdb) if you get `No data`. :contentReference[oaicite:1]{index=1}
- The `tradingview_ta` library may require proxying or retries if TradingView blocks requests; handle exceptions and exponential retries in production. :contentReference[oaicite:2]{index=2}
