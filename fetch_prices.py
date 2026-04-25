#!/usr/bin/env python3
"""
fetch_prices.py
Reads portfolio.json, fetches current prices via yfinance,
writes prices.json. Run by GitHub Actions daily.
"""

import json
import sys
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    print("yfinance not installed. Run: pip install yfinance")
    sys.exit(1)


def fetch_prices(tickers: list[str]) -> dict:
    prices = {}
    if not tickers:
        return prices

    print(f"Fetching prices for: {', '.join(tickers)}")

    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            info = t.fast_info
            price = getattr(info, "last_price", None)
            name  = getattr(info, "regular_market_previous_close", None)

            # fallback: use history
            if price is None:
                hist = t.history(period="2d")
                if not hist.empty:
                    price = float(hist["Close"].iloc[-1])

            # get short name from .info (slower but reliable)
            try:
                meta = t.info
                short_name = meta.get("shortName") or meta.get("longName") or ticker
            except Exception:
                short_name = ticker

            if price is not None:
                prices[ticker] = {
                    "price": round(float(price), 6),
                    "name": short_name,
                    "ok": True,
                }
                print(f"  {ticker:15s} -> {price:.4f}  ({short_name})")
            else:
                prices[ticker] = {"price": None, "name": ticker, "ok": False}
                print(f"  {ticker:15s} -> FAILED (no price found)")

        except Exception as e:
            prices[ticker] = {"price": None, "name": ticker, "ok": False}
            print(f"  {ticker:15s} -> ERROR: {e}")

    return prices


def main():
    # Load portfolio
    try:
        with open("portfolio.json", "r") as f:
            portfolio = json.load(f)
    except FileNotFoundError:
        print("portfolio.json not found — nothing to fetch.")
        sys.exit(0)

    positions = portfolio.get("positions", [])
    open_positions = [p for p in positions if not p.get("closed", False)]

    tickers = list({p["ticker"] for p in open_positions if p.get("ticker")})

    if not tickers:
        print("No open positions — nothing to fetch.")
        # still write an empty prices.json so the dashboard doesn't fail
        output = {
            "updated": datetime.now(timezone.utc).isoformat(),
            "prices": {}
        }
        with open("prices.json", "w") as f:
            json.dump(output, f, indent=2)
        return

    prices = fetch_prices(tickers)

    output = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "prices": prices,
    }

    with open("prices.json", "w") as f:
        json.dump(output, f, indent=2)

    ok  = sum(1 for v in prices.values() if v["ok"])
    bad = len(prices) - ok
    print(f"\nDone: {ok} succeeded, {bad} failed.")
    print(f"prices.json updated at {output['updated']}")


if __name__ == "__main__":
    main()
