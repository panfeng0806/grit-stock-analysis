# Real-Time Market Data Sources

Quick-reference for fetching live A-share stock prices, used in Phase 2/3 of GRIT analysis.

## A-Share Stocks (沪深)

### East Money API (东方财富) — Primary

```python
import urllib.request, json

# SECID format: 0.{code} for SZ, 1.{code} for SH
url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.300866&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f60,f116,f117,f162,f167,f168,f169,f170,f171'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    d = json.loads(resp.read())['data']
    price = d.get('f43') / 100          # 最新价(元)
    prev_close = d.get('f60') / 100      # 昨收
    change_pct = d.get('f169') / 100     # 涨跌幅(%)
    mkt_cap = d.get('f116') / 1e8        # 总市值(亿)
    pe_ttm = d.get('f162') / 100         # PE-TTM
    pb = d.get('f167') / 100             # PB
    high_52w = d.get('f51') / 100        # 52周最高
    low_52w = d.get('f52') / 100         # 52周最低
```

**Key fields:**
| Field | Meaning | Unit |
|:---|:---|:---|
| f43 | 最新价 | 分(÷100=元) |
| f58 | 股票名称 | str |
| f60 | 昨收 | 分 |
| f116 | 总市值 | 元(÷1e8=亿) |
| f117 | 流通市值 | 元 |
| f162 | PE-TTM | ×100 |
| f167 | PB | ×100 |
| f169 | 涨跌幅 | ×100 |
| f170 | 5日涨跌幅 | ×100 |
| f171 | 20日涨跌幅 | ×100 |

**Note:** The historical K-line endpoint (`push2his.eastmoney.com`) may be blocked or throttle connections. Use the basic quote endpoint above for real-time snapshots — it's more reliable.

### One-liner Shell

```bash
python3 -c "
import urllib.request, json
url='https://push2.eastmoney.com/api/qt/stock/get?secid=0.300866&fields=f43,f58,f116,f162,f167'
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
d=json.loads(urllib.request.urlopen(req,timeout=10).read())['data']
print(f'{d[\"f58\"]}: {d[\"f43\"]/100}元 | PE:{d[\"f162\"]/100:.1f} | PB:{d[\"f167\"]/100:.2f} | 市值:{d[\"f116\"]/1e8:.0f}亿')
"
```

## US Stocks (美股) — placeholder

For future use; not yet validated in GRIT sessions.

## HK Stocks (港股) — placeholder

For future use; not yet validated in GRIT sessions.

---

> **Usage in GRIT**: Call the one-liner during Phase 2 or 3 to populate the 估值素材 section. Do NOT use stale prices from raw/ PDFs or Excel files — market data must be real-time at analysis time.
