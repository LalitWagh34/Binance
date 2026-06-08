# 🤖 Binance Trading Bot — Testnet

A clean, production-ready Python CLI trading bot for placing orders on Binance Testnet.
Built with structured logging, input validation, and proper error handling.

---

## ✨ Features

- ✅ Place **Market**, **Limit**, and **Stop Market** orders
- ✅ Supports **BUY** and **SELL** sides
- ✅ Clean **CLI interface** with argparse
- ✅ **Input validation** with clear error messages
- ✅ **Structured logging** to rotating log file
- ✅ **Exception handling** for API, network, and input errors
- ✅ Separated **client layer** and **CLI layer**

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py           # Binance API wrapper (auth + HTTP)
│   ├── orders.py           # Order placement logic
│   ├── validators.py       # Input validation
│   └── logging_config.py   # Rotating file + console logging
├── logs/
│   └── trading_bot.log     # Auto-generated on first run
├── cli.py                  # CLI entry point
├── .env.example            # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd trading_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Testnet API Keys

1. Go to 👉 [https://testnet.binance.vision](https://testnet.binance.vision)
2. Click **"Login with GitHub"**
3. Click **"Generate HMAC-SHA-256 Key"**
4. Copy your `API Key` and `Secret Key` — **Secret shown only once!**

### 5. Configure Environment

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

> ⚠️ Never commit `.env` to GitHub — it's already in `.gitignore`

---

## 🚀 How to Run

### Market Order

```bash
# BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

# SELL
python cli.py --symbol BTCUSDT --side SELL --type MARKET --qty 0.001
```

### Limit Order

```bash
# BUY
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 60000

# SELL
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 70000
```

### Stop Market Order ⭐ Bonus

```bash
# BUY
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --qty 0.001 --stop-price 65000

# SELL
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.001 --stop-price 60000
```

### Help

```bash
python cli.py --help
```

---

## 📤 Sample Output
```
==================================================
ORDER REQUEST SUMMARY
Symbol     : BTCUSDT
Side       : BUY
Type       : MARKET
Quantity   : 0.001
==================================================
ORDER RESPONSE
Order ID     : 123456789
Symbol       : BTCUSDT
Side         : BUY
Type         : MARKET
Status       : FILLED
Price        : 0
Avg Price    : 63135.20
Quantity     : 0.001
Executed Qty : 0.001
✅ Order placed successfully!
```
---

## ❌ Error Handling Examples

### Validation Error
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001
# ❌ Validation Error: Price is required for LIMIT orders.
```

### Invalid Side
```bash
python cli.py --symbol BTCUSDT --side HOLD --type MARKET --qty 0.001
# ❌ Validation Error: Invalid side: 'HOLD'. Must be one of: BUY, SELL
```

---

## 📋 Logging
```
All activity is logged to `logs/trading_bot.log`

2026-06-08T17:30:01 | INFO     | trading_bot.client | GET https://testnet.binance.vision/api/v3/time
2026-06-08T17:30:02 | INFO     | trading_bot.orders | Placing MARKET order: {'symbol': 'BTCUSDT', 'side': 'BUY', ...}
2026-06-08T17:30:02 | INFO     | trading_bot.orders | MARKET order success: {'orderId': 123456789, 'status': 'FILLED', ...}
2026-06-08T17:30:02 | INFO     | trading_bot.cli    | Order placed successfully: orderId=123456789
```
- Log file rotates at **5MB** (keeps last 3 backups)
- Console shows **warnings and errors only**
- File captures **everything** (DEBUG → CRITICAL)

---

## 📦 Requirements

requests==2.31.0
python-dotenv==1.0.0

- Python **3.8+**

---

## 📝 Assumptions & Notes

| Item | Detail |
|------|--------|
| Testnet used | `testnet.binance.vision` (Spot) — Futures testnet was down |
| API endpoint | `/api/v3/order` |
| Auth method | HMAC-SHA256 signed requests |
| LIMIT default | `timeInForce = GTC` (Good Till Cancelled) |
| Credentials | Loaded from `.env` file only |
| Real money | ❌ None — testnet fake USDT only |

---

## 👨‍💻 Author

Built as part of the **Primetrade.ai** Python Developer hiring task.
