# Tether Competitor Data Extraction

## Background

Tether (USDT) is an unlisted private company. No Wind/Choice Excel is available.
The only public financial data comes from quarterly BDO assurance reports published
on Tether's website. These reports contain:

- Total assets (≈ USDT in circulation + excess reserves)
- USDT liabilities (tokens issued, ≈ circulation)
- Excess of assets over liabilities (≈ quarterly retained profit)
- Reserve composition breakdown (T-Bills, Cash, Repo, Bitcoin, Precious Metals, Secured Loans)

## Extraction Pattern

The following Python regex patterns reliably extract key numbers from Tether's
BDO-assured quarterly reports after `pdftotext -layout`:

```python
import subprocess, re

txt = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], capture_output=True, text=True).stdout

# Total assets — look for the "$XXX,XXX,XXX,XXX" after "amount to"
assets = 0
m = re.search(r'amount\s+to\s+US?\$?\s*([\d,]+(?:\.\d+)?)', txt, re.IGNORECASE)
if m:
    assets = float(m.group(1).replace(',',''))

# USDT liabilities (tokens in circulation)
liab = 0
m = re.search(r'liabilities.*?amount\s+to\s+US?\$?\s*([\d,]+(?:\.\d+)?)', txt, re.IGNORECASE)
if m:
    liab = float(m.group(1).replace(',',''))

# Excess (profit) — "liabilities ... by US$ X,XXX,XXX,XXX"
excess = 0
m = re.search(r'liabilities.*?by\s+US?\$?\s*([\d,]+(?:\.\d+)?)', txt, re.IGNORECASE)
if m:
    excess = float(m.group(1).replace(',',''))

# T-Bills percentage
m = re.search(r'U\.?S\.?\s*Treasury\s*Bills?.*?([\d,]{10,}(?:\.\d+)?)', txt, re.IGNORECASE)
tbills = float(m.group(1).replace(',','')) if m else 0
tbills_pct = tbills / assets * 100 if assets else 0

# Bitcoin holdings
m = re.search(r'Bitcoin.*?([\d,]{7,}(?:\.\d+)?)', txt, re.IGNORECASE)
btc = float(m.group(1).replace(',','')) if m else 0
btc_pct = btc / assets * 100 if assets else 0
```

## CRCL Benchmark Data (from Q1 2026 extraction)

| Quarter | USDT Assets | USDT Circulation | Quarterly Profit | T-Bills% | BTC% |
|:---|:---:|:---:|:---:|:---:|:---:|
| Q4 2023 | $916亿 | $916亿 | N/A | 68.9% | 3.1% |
| Q1 2024 | $1,103亿 | $1,040亿 | N/A | 67.1% | 4.9% |
| Q2 2024 | $1,184亿 | $1,131亿 | N/A | 68.3% | 4.0% |
| Q3 2024 | $1,255亿 | $1,194亿 | $60.9亿 | 67.4% | 3.8% |
| Q4 2024 | $1,437亿 | $1,366亿 | $70.9亿 | 65.7% | 5.5% |
| Q1 2025 | $1,493亿 | $1,437亿 | $55.9亿 | 66.0% | 5.1% |
| Q2 2025 | $1,626亿 | $1,571亿 | $54.7亿 | 64.9% | 5.5% |
| Q3 2025 | $1,812亿 | $1,744亿 | $67.8亿 | 62.0% | 5.4% |
| Q4 2025 | $1,929亿 | $1,865亿 | $63.4亿 | 63.4% | 4.4% |
| Q1 2026 | $1,918亿 | $1,835亿 | $82.3亿 | 61.0% | 3.5% |

## Key Comparison

- **Tether quarterly profit**: $55-82亿 vs **Circle FY2025 Non-GAAP NI**: ~$5.2亿
- Tether's profit = ~50x Circle's. Root cause: Tether pays ZERO distribution costs (no Coinbase split)
- Tether T-Bills % declining (69%→61%) as it diversifies into Bitcoin, precious metals, and secured loans
- Tether holds $48-100亿 in Bitcoin (3-5.5% of total assets)
- Circle's USDC at $770亿 (Q1'26) vs Tether's USDT at $1,835亿 = 2.4x gap
