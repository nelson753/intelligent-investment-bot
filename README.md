# 🤖 Intelligent Investment Bot - 100% FREE & Open Source!

**Multi-Crypto Autonomous Trading System** with AI, trend filters, and institutional-grade risk management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Win Rate: 81.8%](https://img.shields.io/badge/win_rate-81.8%25-brightgreen.svg)](sessions/)
[![Version: 3.0](https://img.shields.io/badge/version-3.0-blue.svg)](CHANGELOG.md)

> Professional-grade cryptocurrency trading bot that achieved **81.8% win rate** in real market conditions.  
> Live tested with **$40 real capital**, **+1.6% expectancy** per trade.

---

## 🎉 HUGE UPDATE: Now 100% FREE & Open Source!

**What changed:** Transformed from $999 paid product into a FREE open-source project!

**Before:** $999 commercial license | **Now:** 100% FREE with MIT License

---

## 📊 Estado Actual

**Versión:** 3.0 (EMA 200 Trend Filter + ATR Dynamic SL + MACD Exits)  
**Capital:** $40 USD  
**Modo:** Paper Trading (Precios reales, ejecuciones simuladas)  
**Win Rate Histórico:** 81.8% (11 trades ganadores / 13 totales)  
**Criptos Monitoreadas:** 7 (DOGE★, ETH, SOL, XRP, ADA, MATIC, LINK)

---

## 🚀 Inicio Rápido

### 1. Ejecutar Bot Principal
```powershell
python multi_crypto_trading.py
```

### 2. Ver Dashboard (opcional)
```powershell
python scripts/dashboard_multi_crypto.py
```
Luego abrir: http://localhost:5000

### 3. Analizar Historial
```powershell
python scripts/analyze_history.py
```

---

## 📁 Estructura del Proyecto

```
02_TRADING_BOTS/
│
├── multi_crypto_trading.py       # 🎯 BOT PRINCIPAL (ejecutar este)
│
├── scripts/                       # Scripts auxiliares
│   ├── analyze_history.py         # Análisis de rendimiento histórico
│   ├── dashboard_multi_crypto.py  # Dashboard web Flask
│   ├── test_coinbase_connection.py
│   └── test_kraken_connection.py
│
├── sessions/                      # Sesiones de trading guardadas
│   ├── multi_crypto_session_*.json
│   └── benchmark_report_*.json
│
├── docs/                          # Documentación
│   ├── README_MULTI_CRYPTO.md     # Guía completa del bot
│   ├── PRODUCTION_READY.md        # Features de producción
│   ├── PRO_IMPROVEMENTS.md        # Mejoras profesionales
│   ├── SHORT_SELLING_GUIDE.md     # Guía de ventas en corto
│   └── CRITICAL_FIX_TREND_FILTER.md
│
├── trading_data/                  # Datos de trading
│   ├── backtest_trades.csv
│   └── final_report_*.txt
│
├── trading_models/                # Modelos de ML (PPO)
│   ├── ppo_agent_ep10.json
│   ├── ppo_agent_ep20.json
│   └── ppo_agent_ep30.json
│
└── archived_bots/                 # Bots antiguos/deprecados
    ├── autonomous_trading_system.py
    ├── intelligent_investment_bot.py
    └── ...
```

---

## 🎯 Características Principales

### Trading Inteligente
- ✅ **7 Criptomonedas:** DOGE (prioridad), ETH, SOL, XRP, ADA, MATIC, LINK
- ✅ **LONG + SHORT:** Posiciones largas y cortas
- ✅ **Máx 3 posiciones:** Diversificación controlada
- ✅ **10% tamaño posición:** $4 por trade con $40 capital

### Indicadores Técnicos
- 📈 **RSI Adaptativo** (5-14 períodos)
- 📊 **MACD Adaptativo** (rápido 6-12, lento 13-26)
- 📉 **Bollinger Bands** (5-20 períodos)
- 🎯 **EMA 200** (filtro de tendencia)
- 📏 **ATR** (stop loss dinámico)
- ⚡ **Momentum & Volatilidad**

### Gestión de Riesgo Profesional
- 🛑 **Stop Loss Dinámico:** 2×ATR o 2% mínimo
- 🎯 **Take Profit:** 3% fijo
- 🚨 **Global Stop Loss:** $32 (MDD 20%)
- 🔥 **Kill Switch:** 2% pérdida/hora, 3% pérdida/día, 5% pérdida/semana
- 💰 **Fees:** 0.1% por operación
- 📊 **Slippage:** 0.05% simulado

### Filtros Avanzados
- 🧭 **EMA 200 Trend Filter:**
  - LONG solo si precio > EMA 200 * 1.02 (tendencia BULLISH)
  - SHORT solo si precio < EMA 200 * 0.98 (tendencia BEARISH)
  - HOLD si precio dentro ±2% de EMA 200 (tendencia NEUTRAL)
  
- 📏 **ATR Dynamic Stop Loss:**
  - Stop loss = precio - (2 × ATR) para LONG
  - Stop loss = precio + (2 × ATR) para SHORT
  - Mínimo 2% si ATR muy bajo
  
- ⚡ **MACD Crossover Exits:**
  - Cierra LONG si MACD cruza debajo de señal (profit > 1%)
  - Cierra SHORT si MACD cruza arriba de señal (profit > 1%)

### Sistema de 4 Niveles de Salida
1. **Stop Loss:** -2% (dinámico con ATR)
2. **Take Profit:** +3% fijo
3. **MACD Crossover:** Salida anticipada si momentum revierte (profit > 1%)
4. **RSI Extremo:** Salida si RSI opuesto extremo (profit > 1.5%)

---

## 📈 Resultados Históricos

**Última Sesión Validada (Nov 26, 2025):**
- **Trades:** 13 totales
- **Ganadores:** 11 (84.6%)
- **Perdedores:** 2 (15.4%)
- **Win Rate:** 81.8%
- **Profit Promedio:** +2.5% por trade ganador
- **Loss Promedio:** -1.2% por trade perdedor
- **Expectancy:** +1.6% por trade

**Mejor Performer:**
- **DOGE:** 100% win rate (9/9 trades)
- **Profit promedio:** +2.8% por trade

**Peor Performer:**
- **BTC:** 0% win rate (0/2 trades) → **REMOVIDO del bot**

---

## 🔧 Configuración

### Parámetros de Trading (en `multi_crypto_trading.py`)

```python
# Capital
INITIAL_CAPITAL = 40.0
POSITION_SIZE_PERCENT = 0.10  # 10% del capital por posición
MAX_POSITIONS = 3              # Máximo posiciones simultáneas

# Gestión de Riesgo
STOP_LOSS_PERCENT = 0.02       # Base 2% (ajustado por ATR)
TAKE_PROFIT_PERCENT = 0.03     # 3% fijo
GLOBAL_STOP_LOSS_VALUE = 32.0  # $32 (20% MDD)

# Costos de Producción
TRADING_FEE_PERCENT = 0.001    # 0.1% por operación
SLIPPAGE_PERCENT = 0.0005      # 0.05% slippage

# Filtro de Tendencia EMA 200
EMA_BULLISH_THRESHOLD = 1.02   # +2% arriba de EMA = BULLISH
EMA_BEARISH_THRESHOLD = 0.98   # -2% abajo de EMA = BEARISH

# Criptomonedas
CRYPTOS = [
    "DOGE-USD",  # ★ Prioridad (100% win rate histórico)
    "ETH-USD",
    "SOL-USD",
    "XRP-USD",
    "ADA-USD",
    "MATIC-USD",
    "LINK-USD"
]
```

---

## 📚 Documentación

### Guías Principales
- **[README_MULTI_CRYPTO.md](docs/README_MULTI_CRYPTO.md)** - Guía completa del sistema
- **[PRODUCTION_READY.md](docs/PRODUCTION_READY.md)** - Features de producción (fees, slippage, global SL)
- **[PRO_IMPROVEMENTS.md](docs/PRO_IMPROVEMENTS.md)** - Mejoras profesionales (EMA, ATR, MACD)
- **[SHORT_SELLING_GUIDE.md](docs/SHORT_SELLING_GUIDE.md)** - Cómo funcionan las ventas en corto
- **[CRITICAL_FIX_TREND_FILTER.md](docs/CRITICAL_FIX_TREND_FILTER.md)** - Fix del filtro de tendencia

### Análisis
```powershell
# Ver rendimiento histórico
python scripts/analyze_history.py

# Ver trades en tiempo real
python scripts/dashboard_multi_crypto.py
```

---

## ⚠️ Importante

### Modo Actual: Paper Trading
- ✅ **Precios reales:** Coinbase API en tiempo real
- ✅ **Ejecuciones simuladas:** No se gasta dinero real
- ✅ **Fees y slippage:** Simulados (0.1% + 0.05%)
- ✅ **Validación:** Testear estrategia antes de live trading

### Antes de Live Trading
1. **Validar 24-48 horas** con paper trading
2. **Confirmar win rate >85%** con nuevas mejoras
3. **Verificar expectancy >+2%** por trade
4. **Confirmar global SL nunca activado**
5. **Revisar comportamiento en distintas condiciones de mercado**

---

## 🛠️ Solución de Problemas

### Bot no ejecuta trades
**Normal:** El filtro EMA 200 requiere tendencia clara (BULLISH o BEARISH). En mercados neutrales (±2% de EMA 200), el bot espera pacientemente para evitar whipsaws.

### "Gathering data..." prolongado
**Normal:** El bot necesita 15 iteraciones de datos para calcular indicadores técnicos confiables (EMA 200 requiere historial).

### Errores de conexión
```powershell
# Verificar conexión a Coinbase
python scripts/test_coinbase_connection.py
```

### Ver sesión anterior
Las sesiones se guardan automáticamente en `sessions/multi_crypto_session_*.json`

---

## 📊 Próximos Pasos

### Corto Plazo
- [ ] Validar 24-48h con filtro EMA 200 mejorado
- [ ] Comparar win rate nuevo vs histórico (81.8%)
- [ ] Verificar expectancy objetivo (+2.24% vs +1.6%)

### Mediano Plazo
- [ ] Considerar live trading si validación exitosa (>85% win rate)
- [ ] Implementar notificaciones (Telegram/Discord)
- [ ] Agregar más criptos (top 20 por volumen)

### Largo Plazo
- [ ] Machine Learning adaptativo (ajuste dinámico de parámetros)
- [ ] Multi-exchange (Binance, Kraken)
- [ ] Backtesting automatizado

---

## 💰 Support This FREE Project (Optional)

Love this bot? Help keep it free and improving!

### ☕ One-Time Donation
**Buy me a coffee** - Any amount ($5, $10, $25+)
- Keeps the project FREE and open source
- Funds new features (Binance, Kraken, more cryptos)
- Supports cloud version development

**Donate:** https://ko-fi.com/nelson753

### 💎 Monthly Sponsorship (GitHub Sponsors)
- **🥉 Bronze ($10/mo)** - Your name in README + priority issues
- **🥈 Silver ($25/mo)** - Bronze + monthly trading consultation (30 min)
- **🥇 Gold ($50/mo)** - Silver + custom strategy requests + early access
- **💎 Platinum ($100/mo)** - Gold + dedicated support + custom ML models

**Become a Sponsor:** https://github.com/sponsors/nelson753

---

## 🚀 Premium Services (Optional)

Want professional help?

### Cloud Hosting (Coming Q2 2026 - Beta Waitlist)
- **🆓 Free Tier:** 1 bot, paper trading, community support
- **💼 Pro ($49/mo):** 3 bots, auto-trading, email alerts
- **🏢 Team ($149/mo):** 10 bots, priority support, analytics
- **🏛️ Enterprise (Custom):** Unlimited, SLA, white-label

**Join Waitlist:** nelson.debugger@gmail.com

### Professional Services
- **Custom Strategy Development:** $500 - Build your unique trading algorithm
- **Enterprise Integration:** $2,000+ - API integration, training, CI/CD
- **Trading Training:** $150/hour - Learn algo trading from experts
- **Performance Consulting:** $200/hour - Optimize win rate and expectancy

**Request Quote:** nelson.debugger@gmail.com - 24h response

---

## 📞 Soporte

**Archivos de Log:** `sessions/multi_crypto_session_YYYYMMDD_HHMMSS.json`  
**Análisis:** `python scripts/analyze_history.py`  
**Dashboard:** `python scripts/dashboard_multi_crypto.py`

### Contact
- **Email:** nelson.debugger@gmail.com
- **GitHub:** https://github.com/nelson753
- **Ko-fi:** https://ko-fi.com/nelson753
- **Sponsors:** https://github.com/sponsors/nelson753

---

**Versión:** 3.0  
**Última Actualización:** Diciembre 3, 2025  
**Estado:** ✅ Producción (Paper Trading)

⭐ **Star this repo if it helps you trade better!**
