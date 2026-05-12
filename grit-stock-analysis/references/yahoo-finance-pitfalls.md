# Yahoo Finance API 实战陷阱（携程09961.HK v2.3）

## 1. 港股代码格式

Yahoo Finance对港股代码**去掉前导零**：
```
✅ 9961.HK   — 正确，返回正常数据
❌ 09961.HK  — 错误，返回 {"code":"Not Found","description":"No data found, symbol may be delisted"}
✅ 0780.HK   — 同程旅行
✅ 00700.HK  — 这个可能也需要去掉前导零，待验证（腾讯）
```

**规则**：所有港股Yahoo查询一律去掉前导零。

## 2. quoteSummary端点被封

`query2.finance.yahoo.com/v10/finance/quoteSummary` 返回：
```json
{"finance":{"result":null,"error":{"code":"Unauthorized","description":"Invalid Crumb"}}}
```

**需要cookie+crumble认证**，裸curl无法通过。

**症状**：`KeyError: 'quoteSummary'` 或 `KeyError: 'quoteResponse'`

## 3. 可用端点与不可用端点

| 端点 | 状态 | 返回内容 |
|:---|:---|:---|
| `v8/finance/chart` | ✅ 可用 | 股价(regularMarketPrice)、OHLCV、时间戳 |
| `v10/finance/quoteSummary` | ❌ 封禁 | Unauthorized / Invalid Crumb |
| `v7/finance/quote` | ❌ 封禁 | 同上或返回结构不同 |

## 4. chart端点不返回的数据（必须自算）

chart端点 **不返回**：
- marketCap
- trailingPE / forwardPE
- sharesOutstanding
- bookValue
- 52周高低

## 5. 自算方案

```python
# 步骤1: 从chart获取实时股价
price = meta['regularMarketPrice']

# 步骤2: 从Wind Excel获取总股本
# EPS(稀释) = 54.5, 净利润 = 380.66亿
total_shares = 380.66 / 54.5  # = 6.985亿股

# 步骤3: 自算市值
market_cap = price * total_shares

# 步骤4: 自算PE-TTM
pe_ttm = price / diluted_eps

# 步骤5: 自算PB
bps = 股东权益 / total_shares
pb = price / bps
```

## 6. 正确的curl调用格式

```bash
# 必须带User-Agent header
curl -sL "https://query1.finance.yahoo.com/v8/finance/chart/9961.HK?interval=1d&range=3mo" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# 解析返回
python3 -c "
import json, sys
d = json.load(sys.stdin)  # ⚠️ sys.stdin.read() 然后 json.loads，不是直接 json.load
r = d['chart']['result'][0]
meta = r['meta']
print(f'股价: {meta[\"regularMarketPrice\"]}')
"
```

## 7. 常见Python解析错误

| 错误 | 原因 | 修复 |
|:---|:---|:---|
| `TypeError: 'NoneType' object is not subscriptable` | `d['chart']['result']` 为None | 先检查 `d['chart'].get('error')` |
| `TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper` | 用了`json.load(sys.stdin)`而非`json.loads(sys.stdin.read())` | 用`json.loads(sys.stdin.read())` |
| `KeyError: 'regularMarketPrice'` | 用了quoteSummary端点而非chart端点 | 切换到v8/finance/chart |

## 8. 备用数据源

当Yahoo彻底不可用时：
- **美股**：Financial Modeling Prep (demo key可用)
- **加密**：CoinGecko API
- **A股**：东方财富 push2.eastmoney.com
- **港股**：暂无可靠免费备用源，建议用CDP浏览器抓取Google Finance或AAStocks
