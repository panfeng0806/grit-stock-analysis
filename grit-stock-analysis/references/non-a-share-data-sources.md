# Non-A-Share Real-Time Data Sources

> Applies to: NYSE, NASDAQ, HKEX, and other non-A-share stocks analyzed via GRIT.
> For A-share data, use eastmoney (push2.eastmoney.com) as described in `real-time-data-sources.md`.

## Stock Price & Market Cap

### Yahoo Finance v8 (primary, but flaky)
```bash
# Add User-Agent header — without it, curl often gets empty response
curl -s -H "User-Agent: Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/FUFU?interval=1d&range=5d" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);m=d['chart']['result'][0]['meta'];print(f'Price: \${m[\"regularMarketPrice\"]}')"
```

**Pitfalls:**
- Returns empty/JSON error without User-Agent header on some tickers
- Market cap often missing from chart endpoint — use quote endpoint as fallback
- May rate-limit; don't hammer it

### Financial Modeling Prep (fallback)
```bash
curl -s "https://financialmodelingprep.com/api/v3/quote/FUFU?apikey=demo"
```
- Free tier limited, but `apikey=demo` works for occasional use
- Returns price, marketCap, sharesOutstanding in one call

## Cryptocurrency Prices

### CoinGecko (reliable, free, no API key)
```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
```
- Works for BTC, ETH, and 1000+ other coins
- Rate limit ~10-30 calls/minute on free tier
- Use for: BTC price (critical for mining stocks like FUFU/MARA/RIOT), ETH, etc.

## SEC EDGAR Filings (20-F, 10-K, 6-K, 8-K)

### Financial Statement Extraction Strategy

SEC filings use text-based table formatting — NOT HTML tables. Simple `grep` for line items often misses context. Effective approach:

**Priority order for data extraction:**
1. **6-K quarterly press releases** — financial highlights in narrative form. Example: `grep -i 'Total revenue was\|net income\|Adjusted EBITDA'` catches the press release summary
2. **20-F Management Discussion & Analysis (MD&A)** — directly quotes financial figures in prose. Search for `Year ended December 31, 2025 compared to`
3. **20-F formal financial statements** — last resort, tables are dense and hard to parse

**Key search patterns for SEC filings:**
```bash
# Revenue / Profit
grep -i 'Total revenues\|net.*income\|net.*loss\|gross profit\|Adjusted EBITDA' file.txt

# Balance Sheet
grep -i 'Total current assets\|Total assets\|Total.*liabilities\|Total.*equity\|Cash and cash equivalents\|Digital assets' file.txt

# Shares Outstanding (usually in cover page header)
grep -i 'ordinary shares issued and outstanding\|Class A.*shares\|Class B.*shares' file.txt

# Segment Revenue
grep -i 'Cloud.*mining.*revenue\|Self-mining.*revenue\|Mining.*equipment.*revenue' file.txt
```

**For Bitcoin/crypto mining companies specifically:**
- Search for: `hashrate\|EH/s\|mining capacity\|self-mined\|cloud-mined\|breakeven\|cost.*mine.*BTC\|BTC.*produced\|bitcoin.*held\|fleet efficiency\|J/Th`
- Company monthly operational updates (filed as 6-K exhibits) contain granular hashrate/production data


When the user includes a `股价走势.csv` in raw/:
- This is the **most reliable** source for historical prices
- Use the last row for current price
- Format typically: Date,Close,High,Low,Volume

## OCR for Scanned/Image-based PDFs

Many research reports (especially from Chinese brokerages or older Seeking Alpha snapshots) are image-based PDFs that `pdftotext` returns empty. Setup:

```bash
# Install tesseract with language packs
sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# Python dependencies
pip install pytesseract pdf2image --break-system-packages
```

**OCR extraction script:**
```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path('report.pdf', dpi=200)
for i, img in enumerate(images):
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    print(f'=== Page {i+1} ===')
    print(text[:1500])
```

- `chi_sim+eng` handles mixed CN/EN content well
- `dpi=200` balances quality vs speed; 300 for small text
- First run `tesseract --list-langs` to verify language packs installed
- ⚠️ OCR text will have artifacts (typos, broken formatting) — read for meaning not precision
## Data Source Priority (non-A-share)
1. User-provided Excel in raw/ (financial data — highest confidence)
2. User-provided CSV in raw/ (historical prices)
3. CoinGecko (crypto prices — BTC/ETH for mining stocks)
4. 6-K press release narrative (easiest financial extraction)
5. 20-F MD&A section (prose financial references)
6. Yahoo Finance v8 + User-Agent header (real-time stock price)
7. OCR'd research reports (medium confidence, artifact-prone)
8. Financial Modeling Prep demo key
9. 20-F formal financial statements (hardest to parse)
10. Mark as "未识别" if all fail
