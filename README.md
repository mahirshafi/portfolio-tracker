# 📈 Portfolio Tracker

A GitHub-hosted stock portfolio tracker with automatic daily price updates via GitHub Actions and Yahoo Finance.

## Files

| File | Purpose |
|---|---|
| `index.html` | Dashboard (open in browser / GitHub Pages) |
| `portfolio.json` | Your positions (you manage this) |
| `prices.json` | Current prices (written by GitHub Actions) |
| `fetch_prices.py` | Price fetcher script (run by Actions) |
| `.github/workflows/update_prices.yml` | Daily automation |

## Setup

### 1. Create GitHub repo & push files
Create a new public repo (e.g. `portfolio-tracker`) and push all files.

### 2. Enable GitHub Pages
`Settings → Pages → Source: Deploy from branch → main → / (root)`

Your dashboard: `https://USERNAME.github.io/portfolio-tracker/`

### 3. Open dashboard & set repo path
Enter `username/repo-name` in the setup banner and click Save.

### 4. Add positions
Use the **+ Add Position** tab. After adding positions:
- Click **Download portfolio.json**
- Commit it to your repo: `git add portfolio.json && git commit -m "add positions" && git push`

### 5. Trigger first price fetch
Go to **GitHub → Actions → Update Stock Prices → Run workflow**

After that it runs automatically **Mon–Fri at 22:00 UTC**.

## Ticker formats

| Type | Format | Example |
|---|---|---|
| US Stocks | `TICKER` | `AAPL`, `FWONA`, `NVDA` |
| Forex | `XXXYYY=X` | `EURUSD=X`, `GBPUSD=X` |
| Crypto | `XXX-USD` | `BTC-USD`, `ETH-USD` |
| Futures | `XX=F` | `GC=F` (Gold), `CL=F` (Oil) |
| Indices | `^XXX` | `^GSPC` (S&P 500) |

## Manual price update
Go to `GitHub → Actions → Update Stock Prices → Run workflow` anytime.
