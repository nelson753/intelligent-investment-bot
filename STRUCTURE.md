# 📋 Estructura del Proyecto

Última actualización: Diciembre 3, 2025

## Archivos Principales (Raíz)

```
02_TRADING_BOTS/
├── multi_crypto_trading.py    # 🎯 BOT PRINCIPAL (40KB, ejecutar este)
├── README.md                   # 📖 Documentación principal
├── requirements.txt            # 📦 Dependencias (con explicaciones)
├── requirements_simple.txt     # 📦 Dependencias (solo nombres)
├── .gitignore                  # 🚫 Archivos ignorados por Git
│
├── start_bot.ps1              # 🚀 Script para iniciar el bot
├── start_dashboard.ps1        # 📊 Script para iniciar dashboard
└── analyze.ps1                # 📈 Script para analizar historial
```

## Directorios

### 📁 scripts/ - Utilidades y Scripts Auxiliares
```
scripts/
├── analyze_history.py          # Analiza rendimiento histórico
├── dashboard_multi_crypto.py   # Dashboard web Flask (puerto 5000)
├── test_coinbase_connection.py # Verifica conexión a Coinbase
├── test_kraken_connection.py   # Verifica conexión a Kraken
└── get_oanda_account.py        # Utilidad OANDA (no usado)
```

### 📚 docs/ - Documentación Completa
```
docs/
├── README_MULTI_CRYPTO.md            # Guía principal del bot
├── PRODUCTION_READY.md               # Features de producción
├── PRO_IMPROVEMENTS.md               # Mejoras avanzadas (EMA, ATR, MACD)
├── SHORT_SELLING_GUIDE.md            # Guía de ventas en corto
├── CRITICAL_FIX_TREND_FILTER.md      # Fix del filtro de tendencia
├── README_AUTONOMOUS.md              # Doc bot autónomo anterior
├── README_INTELLIGENT_INVESTMENT_BOT.md
├── INTELLIGENT_BOT_README.md
└── ANALISIS_ESTRUCTURA.md
```

### 💾 sessions/ - Sesiones de Trading Guardadas
```
sessions/
├── multi_crypto_session_*.json       # Sesiones del bot actual (50+ archivos)
├── autonomous_session_*.json         # Sesiones de bot anterior
├── coinbase_safe_session_*.json      # Sesiones antiguas
├── paper_trading_session_*.json      # Sesiones antiguas
├── live_session_*.json               # Sesiones antiguas
└── benchmark_report_*.json           # Reportes de benchmark

Total: 68 archivos de sesión
```

### 📊 trading_data/ - Datos de Trading
```
trading_data/
├── backtest_trades.csv              # Trades de backtesting
├── final_report_*.txt               # Reportes finales (15 archivos)
└── kill_switch_events.json          # Eventos de kill switch
```

### 🤖 trading_models/ - Modelos de Machine Learning
```
trading_models/
├── ppo_agent_ep10.json
├── ppo_agent_ep20.json
└── ppo_agent_ep30.json
```

### 📦 archived_bots/ - Bots Antiguos/Deprecados
```
archived_bots/
├── autonomous_trading_system.py      # Bot autónomo v1
├── intelligent_investment_bot.py     # Bot con ML
├── bot_demo.py                       # Demos iniciales
├── bot_auto_demo.py
├── paper_trading_realistic.py        # Paper trading v1
├── live_trading_controlled.py        # Live trading v1
├── live_trading_coinbase_safe.py     # Live trading v2
├── backtest_coinbase.py              # Backtesting
├── benchmark_autonomous_system.py    # Benchmark v1
├── benchmark_coinbase_safe.py        # Benchmark v2
├── dashboard_autonomous.py           # Dashboard v1
├── content_arbitrage_bot.py          # Bot de arbitraje
├── devto_monitor_bot.py              # Bot de monitoreo Dev.to
└── reddit_marketing_assistant.py     # Bot de Reddit

Total: 14 bots archivados
```

### 🗑️ __pycache__/ - Cache de Python
```
__pycache__/
└── *.pyc                             # Archivos compilados (ignorar)
```

## Uso Rápido

### Iniciar Bot Principal
```powershell
.\start_bot.ps1
# o
python multi_crypto_trading.py
```

### Ver Dashboard
```powershell
.\start_dashboard.ps1
# o
python scripts\dashboard_multi_crypto.py
# Luego abrir: http://localhost:5000
```

### Analizar Historial
```powershell
.\analyze.ps1
# o
python scripts\analyze_history.py
```

### Instalar Dependencias
```powershell
pip install -r requirements.txt
```

## Resumen de Archivos

| Categoría | Cantidad | Ubicación |
|-----------|----------|-----------|
| **Bot Activo** | 1 | `multi_crypto_trading.py` |
| **Scripts Auxiliares** | 5 | `scripts/` |
| **Documentación** | 9 | `docs/` |
| **Sesiones Guardadas** | 68 | `sessions/` |
| **Bots Archivados** | 14 | `archived_bots/` |
| **Scripts PowerShell** | 3 | Raíz |
| **Archivos Config** | 3 | Raíz (README, requirements, .gitignore) |

## Historial de Cambios

**Diciembre 3, 2025:**
- ✅ Reorganización completa del proyecto
- ✅ Creación de estructura de directorios
- ✅ Separación de docs, scripts, sessions, archived_bots
- ✅ Creación de README.md principal
- ✅ Creación de scripts PowerShell de inicio rápido
- ✅ Creación de requirements.txt
- ✅ Creación de .gitignore
