# 🚀 Quick Start Guide - Intelligent Investment Bot

## Installation (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/intelligent-investment-bot.git
cd intelligent-investment-bot
```

### 2. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using conda
conda create -n trading-bot python=3.10
conda activate trading-bot
pip install -r requirements.txt
```

### 3. Configure Environment (Optional - for live trading)
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
# For paper trading, skip this step
```

---

## Quick Test (Paper Trading - NO RISK)

### Test 1: Run Benchmark (2 minutes)
```bash
python intelligent_bot_tier1_full_benchmark.py
```

**Expected Output:**
```
TIER 1 BENCHMARK COMPLETO - 6 INQUEBRANTABLES
Score: 600/600 (100%)
Status: CERTIFICADO ✅
```

### Test 2: Paper Trading Session (10 minutes)
```bash
python paper_trading_realistic.py

# When prompted:
Capital inicial: 100
Duración (minutos): 10
```

**Expected Output:**
```
PAPER TRADING SESSION - DATOS REALES, SIN RIESGO
[Monitoring real Bitcoin prices...]
Final: Capital preserved ~100%
```

---

## Run Tests (1 minute)

```bash
# All tests
pytest -v

# Specific INQUEBRANTABLE
pytest test_inquebrantable_1.py -v  # Kill Switch
pytest test_inquebrantable_2.py -v  # Auto-retraining
pytest test_inquebrantable_3.py -v  # Multi-asset
pytest test_inquebrantable_4.py -v  # API Redundancy
pytest test_inquebrantable_5.py -v  # Black Swan
pytest test_inquebrantable_6.py -v  # Cross-validation
```

**Expected:** 59/59 tests passed ✅

---

## Live Trading (REAL MONEY - Use with Caution)

⚠️ **WARNING:** Only proceed after successful paper trading sessions.

### Prerequisites:
1. ✅ Completed paper trading test
2. ✅ API keys configured in `.env`
3. ✅ Small capital ready ($10-$50 recommended)

### Run Live Trading:
```bash
python live_trading_coinbase_safe.py

# Configuration:
Mode: 1 (Paper first to validate) or 2 (Live with real money)
Capital: Start with $10-$20
Duration: 5-10 minutes for first test
```

**Safety Features Active:**
- Kill Switch: 2%/3%/5% MDD
- Position size: 10% max
- Capital limit: $20 max (50% reserved)
- Emergency stop: CTRL+C anytime

---

## File Structure

```
intelligent-investment-bot/
├── intelligent_investment_bot.py          # Main bot (2,678 lines)
├── live_trading_coinbase_safe.py          # Live trading interface
├── paper_trading_realistic.py             # Paper trading interface
├── intelligent_bot_tier1_full_benchmark.py # Benchmark suite
├── test_inquebrantable_*.py               # Test files (6 files)
├── README.md                              # Full documentation
├── SETUP.md                               # This file
├── requirements.txt                       # Dependencies
├── .env.example                           # Environment template
└── LICENSE                                # Dual license
```

---

## Troubleshooting

### Error: "No module named 'sklearn'"
```bash
pip install scikit-learn
```

### Error: "EAPI:Invalid key" (live trading)
- Check your `.env` file has correct API keys
- Verify API keys are active on exchange
- Try paper trading first (doesn't need API keys)

### No trades generated
- Normal if market has low volatility
- Try longer session (30-60 min)
- Check that prices are updating (should see BTC price changing)

### High MDD in paper trading
- Reduce position_size in code (default: 10%)
- Use shorter sessions during volatile markets
- Adjust kill_switch levels if needed

---

## Next Steps

1. ✅ **Run benchmark** → Verify 600/600 score
2. ✅ **Paper trading 30 min** → Observe behavior
3. ✅ **Read full README.md** → Understand all features
4. ⚠️ **Live trading $10** → Only if confident
5. 📊 **Analyze JSON logs** → Review all sessions

---

## Support

- 📖 Full Documentation: `README.md`
- 🐛 Report Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📧 Commercial License: [your-email@example.com]

---

## Important Reminders

⚠️ **Trading involves risk** - Never invest more than you can afford to lose  
✅ **Always test with paper trading first**  
🛡️ **Never disable Kill Switch protections**  
📊 **Monitor all live trading sessions actively**  
💾 **Review session logs after each run**

---

**Ready to start?**

```bash
# 1. Test the system
python intelligent_bot_tier1_full_benchmark.py

# 2. Try paper trading
python paper_trading_realistic.py

# 3. Read the results and decide next steps
```

**Good luck and trade safely! 🚀**
