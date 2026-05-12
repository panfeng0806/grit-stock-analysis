# 实时数据源 — 全市场

GRIT 阶段2/3 抓取实时股价、市值、加密资产价格。

---

## A 股（沪深）

### 东方财富 API — 主力

```bash
python3 -c "
import urllib.request, json
url='https://push2.eastmoney.com/api/qt/stock/get?secid=0.000001&fields=f43,f58,f116,f162,f167,f169'
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
d=json.loads(urllib.request.urlopen(req,timeout=10).read())['data']
print(f'{d[\"f58\"]}: {d[\"f43\"]/100}元 | PE:{d[\"f162\"]/100:.1f} | PB:{d[\"f167\"]/100:.2f} | 市值:{d[\"f116\"]/1e8:.0f}亿')
"
```

**字段**：f43=最新价(÷100) | f58=名称 | f116=总市值(÷1e8=亿) | f162=PE-TTM(÷100) | f167=PB(÷100) | f169=涨跌幅(÷100)

secid: `0.{code}` 深市, `1.{code}` 沪市

---

## 美股（NYSE / NASDAQ）& 港股

### Yahoo Finance v8 chart — 主力 ✅ 已验证 2026-05-12

**美股**：
```bash
curl -sL -H "User-Agent: Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=1mo" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)['chart']['result'][0]
m=d['meta']
q=d['indicators']['quote'][0]
print(f'股价: \${m[\"regularMarketPrice\"]} | 52W高: \${m.get(\"fiftyTwoWeekHigh\",\"?\")} | 52W低: \${m.get(\"fiftyTwoWeekLow\",\"?\")} | 币种: {m[\"currency\"]}')
"
```

**港股**（⚠️ 去掉前导零：00000.HK→0000.HK）：
```bash
curl -sL -H "User-Agent: Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/0000.HK?interval=1d&range=3mo"
```

> ✅ **已多ticker验证**（AAPL/TSLA）均可正常返回。

### Yahoo Finance 端点状态

| 端点 | 状态 | 返回内容 |
|:---|:---|:---|
| `v8/finance/chart` | ✅ 可用 | 股价(regularMarketPrice)、OHLCV、52周高低、时间戳 |
| `v10/finance/quoteSummary` | ❌ 封禁 | Unauthorized / Invalid Crumb（需cookie+crumb） |
| `v7/finance/quote` | ❌ 封禁 | 同上 |

### chart 端点不返回的数据（必须自算）

chart端点 **不返回**：marketCap、trailingPE、forwardPE、sharesOutstanding、bookValue、EPS。

**自算方案**：
```
1. 股价 = chart端点 regularMarketPrice
2. 总股本 = 归母净利 ÷ EPS（从Wind Excel同一报告期）
3. 市值 = 股价 × 总股本
4. PE-TTM = 市值 ÷ TTM归母净利（最近4个季度之和）
5. PB = 股价 ÷ (股东权益 ÷ 总股本)
```

### 港股代码格式陷阱

Yahoo Finance 对港股代码**去掉前导零**：
```
✅ 0000.HK   — 正确
❌ 00000.HK  — 返回 "No data found, symbol may be delisted"
✅ 0005.HK   — 汇丰控股
```

**规则**：所有港股Yahoo查询一律去掉前导零。

### Python 解析常见错误

| 错误 | 原因 | 修复 |
|:---|:---|:---|
| `TypeError: 'NoneType' object is not subscriptable` | `d['chart']['result']` 为None | 先检查 `d['chart'].get('error')` |
| `TypeError: the JSON object must be str...` | 用了`json.load(sys.stdin)`而非`json.loads(sys.stdin.read())` | 用`json.loads(sys.stdin.read())` |
| `KeyError: 'regularMarketPrice'` | 用了quoteSummary端点而非chart端点 | 切换到v8/finance/chart |

### Financial Modeling Prep（兜底，免费tier 250次/天）

```bash
curl -s "https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=***"
```

> 返回 price, marketCap, sharesOutstanding 一步到位。仅限美股。demo key 有限额。

---

## 备用数据源（Yahoo 彻底不可用时）

- **美股**：Financial Modeling Prep (demo key可用)
- **加密**：CoinGecko API
- **A股**：东方财富 push2.eastmoney.com
- **港股**：暂无可靠免费备用源，建议用 CDP 浏览器抓取 Google Finance 或 AAStocks

---

## 加密资产

### CoinGecko（免费，无需 API key）

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
```

支持 BTC/ETH/1000+ 币种。免费 tier 约 10-30 次/分钟。挖矿股（MARA/RIOT 等）必须抓 BTC 现价。

---

## 使用规则

- **阶段2开始时** + **阶段5估值分析前** 各抓一次，确保估值基于最新行情
- 股价/PE/市值禁止用 raw 中 PDF/Excel 的历史数据
- 抓取失败则标注「数据源不可用」，而非编造
