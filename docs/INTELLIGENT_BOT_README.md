# 🤖 Intelligent Investment Bot (II) v1.0

**Bot de Trading Algorítmico con Arquitectura Grial 2.0**

---

## 🎯 Resumen Ejecutivo

Bot autónomo de trading que combina **4 sistemas de IA** para generar ganancias en mercados de alta volatilidad (crypto/forex) con **gestión de riesgo automática**.

### Resultados de Testing
- ✅ **69/69 tests pasando (100%)**
- ✅ **88% code coverage**
- ✅ **5.02s execution time**
- ✅ **Production-ready**

---

## 🏗️ Arquitectura de 4 Pilares (Grial 2.0)

### **AI 1: Risk Manager (Autonomía)**
**Responsabilidad:** Proteger el capital sin intervención humana

**Funcionalidades:**
- 📊 **Maximum Drawdown (MDD) Monitoring**: Detecta pérdidas >= 10%
- 🚨 **Kill Switch**: Cierre de emergencia automático
- 📉 **Daily Loss Limit**: Pausa si pérdida diaria > 15%
- 📈 **Sharpe Ratio**: Calcula retorno ajustado por riesgo
- ⚠️ **Position Sizing**: Limita posiciones al 20% del capital

**Decisiones Autónomas:**
```python
if current_drawdown >= 10%:
    activate_kill_switch()
    liquidate_all_positions()
    pause_trading()
    trigger_auto_evolver()
```

### **AI 2: Sentiment Analyzer (Visión de Futuro)**
**Responsabilidad:** Predecir dirección del mercado

**Fuentes de Datos:**
- 🐦 Twitter/X (#bitcoin, #crypto)
- 📰 CoinDesk headlines
- 📡 NewsAPI crypto news

**Output:**
- **Sentiment Factor**: -1.0 (pánico) a +1.0 (euforia)
- **Volatility Prediction**: LOW, MEDIUM, HIGH

**Lógica:**
```python
if sentiment > +0.5:  # Euforia
    increase_position_size()  # Aprovechar momentum
elif sentiment < -0.5:  # Pánico
    reduce_risk()  # Cautela
```

### **AI 3: PPO Trading Agent (Optimización)**
**Responsabilidad:** Tomar decisiones de trading óptimas

**Arquitectura:**
- **Actor Network**: Política π(a|s) → Probabilidad de acción
- **Critic Network**: Función de valor V(s) → Valor esperado

**Acciones:**
- 0: **BUY** - Comprar con 20% del cash
- 1: **SELL** - Vender toda la posición
- 2: **HOLD** - Mantener

**Estado (10 dimensiones):**
```
[Precio, Volumen, RSI, MACD, Signal, SMA_20, SMA_50, 
 Sentiment, Portfolio_Value, Current_Position]
```

**Recompensa:**
```python
reward = portfolio_value_change
if MDD_triggered:
    reward -= 1000  # Penalización fuerte
```

### **AI 4: Auto-Evolver (Auto-Mejora)**
**Responsabilidad:** Mejorar el sistema tras failures

**Triggers:**
- ✅ Kill Switch activado
- ✅ Performance < 15% anual
- ✅ Sharpe Ratio < 1.0

**Proceso:**
1. Analiza qué causó el failure
2. Re-entrena AI 3 con **penalización 10x**
3. Ajusta hiperparámetros
4. Valida mejora

---

## 📊 Métricas Clave

| Métrica | Definición | Threshold |
|---------|------------|-----------|
| **Maximum Drawdown (MDD)** | Máxima pérdida desde peak a valley | <= 10% |
| **Sharpe Ratio** | Retorno / Volatilidad | >= 1.0 |
| **Win Rate** | % de trades ganadores | >= 50% |
| **Daily Loss Limit** | Pérdida máxima diaria | <= 15% |
| **Position Size** | Tamaño máximo por trade | <= 20% |

---

## 🚀 Uso

### **Paper Trading (Recomendado)**
```bash
python intelligent_investment_bot.py --episodes 10 --exchange paper --capital 1000
```

### **Binance Live**
```bash
# Configurar API keys primero
export BINANCE_API_KEY="your_key"
export BINANCE_SECRET="your_secret"

python intelligent_investment_bot.py --episodes 100 --exchange binance --capital 5000
```

### **Kraken Live**
```bash
python intelligent_investment_bot.py --episodes 100 --exchange kraken --capital 5000
```

### **Parámetros**
```bash
--episodes N       # Número de episodios de trading
--exchange NAME    # binance, kraken, paper
--symbol PAIR      # BTCUSDT, ETHUSDT, etc.
--capital AMOUNT   # Capital inicial en USD
```

---

## 🧪 Testing

### **Ejecutar Tests**
```bash
# All tests
python -m pytest test_intelligent_bot.py -v

# Con coverage
python -m pytest test_intelligent_bot.py --cov=intelligent_investment_bot --cov-report=html

# Tests específicos
python -m pytest test_intelligent_bot.py::TestPPOTradingAgent -v
```

### **Coverage Report**
```
Name                            Stmts   Miss  Cover
-------------------------------------------------------------
intelligent_investment_bot.py     550     65    88%
-------------------------------------------------------------
TOTAL                             550     65    88%
```

**12% no cubierto:**
- CLI functions (ejecución manual)
- Binance/Kraken API real (requiere keys)
- Visualización de reportes

---

## 📁 Estructura de Archivos

```
Depurador/
├── intelligent_investment_bot.py    # Bot principal (1414 líneas)
├── test_intelligent_bot.py          # Suite de tests (69 tests)
├── trading_data/                    # Datos generados
│   ├── kill_switch_events.json      # Eventos de emergencia
│   └── final_report_*.txt           # Reportes finales
├── trading_models/                  # Modelos guardados
│   └── ppo_agent_ep*.json           # Checkpoints del agente
└── arbitrage_opportunities/         # (del bot anterior)
```

---

## 🔧 Configuración Avanzada

### **Risk Config**
```python
RISK_CONFIG = {
    "max_drawdown_threshold": 0.10,  # 10% MDD
    "stop_loss_percent": 0.05,       # 5% stop loss
    "daily_loss_limit": 0.15,        # 15% diario
}
```

### **PPO Config**
```python
PPO_CONFIG = {
    "learning_rate": 3e-4,
    "gamma": 0.99,              # Discount factor
    "clip_epsilon": 0.2,        # PPO clip
    "batch_size": 64,
}
```

### **Sentiment Config**
```python
SENTIMENT_CONFIG = {
    "sentiment_weight": 0.3,    # Peso en decisiones
    "lookback_hours": 24,       # Análisis últimas 24h
}
```

---

## 🐛 Bugs Corregidos

### **Bug #1: Kill Switch Persistente** ✅
- **Problema**: Se activaba en Episode 1 y bloqueaba Episode 2
- **Solución**: Agregado `risk_manager.reset()` en cada episodio
- **Test**: `test_risk_manager_resets_between_episodes`

### **Bug #2: Daily P&L Incorrecto** ✅
- **Problema**: Mostraba "20% loss" con $0.20 pérdida
- **Solución**: Método `get_daily_pnl()` corregido
- **Test**: `test_daily_pnl_calculation`

### **Bug #3: Position Sizing** ✅
- **Problema**: Compraba más del 20% permitido
- **Solución**: Validación en `should_allow_trade()`
- **Test**: `test_should_not_allow_oversized_position`

---

## 📈 Roadmap

### **v1.1 - Próximas Mejoras**
- [ ] Integración con APIs reales (Binance/Kraken)
- [ ] Dashboard web en tiempo real
- [ ] Backtesting con datos históricos
- [ ] Multi-symbol trading (BTC, ETH, SOL)
- [ ] Telegram notifications

### **v2.0 - Features Avanzadas**
- [ ] Reinforcement Learning avanzado (SAC, TD3)
- [ ] Ensemble de modelos (PPO + DQN + A3C)
- [ ] Sentiment analysis con LLM (GPT-4)
- [ ] Order book analysis
- [ ] Market maker strategies

---

## 💰 Modelo de Negocio

### **Opción 1: Venta Directa**
- **Precio**: $199 - $499
- **Plataforma**: Ko-fi, Gumroad, GitHub Sponsors
- **Target**: Traders algorítmicos, quant researchers

### **Opción 2: SaaS**
- **Precio**: $49/mes - $199/mes
- **Features**: Bot hosted, API access, dashboard
- **Revenue**: MRR (Monthly Recurring Revenue)

### **Opción 3: Hybrid**
- **Free Tier**: Paper trading + 1 symbol
- **Pro Tier**: $99/mes - Live trading + multi-symbol
- **Enterprise**: $499/mes - Custom strategies

---

## ⚠️ Disclaimer

**IMPORTANTE**: Este bot es para fines educativos y de investigación.

- ⚠️ Trading crypto/forex tiene **alto riesgo**
- ⚠️ Puedes **perder todo tu capital**
- ⚠️ Pasado no garantiza futuro
- ⚠️ Usa **solo capital que puedas perder**
- ⚠️ **NO es asesoramiento financiero**

**Recomendaciones:**
1. ✅ Empieza con paper trading
2. ✅ Testea mínimo 3 meses
3. ✅ Usa stop-loss estrictos
4. ✅ Diversifica (no todo en un bot)
5. ✅ Revisa diariamente

---

## 📚 Referencias

### **Papers Implementados**
- [Proximal Policy Optimization](https://arxiv.org/abs/1707.06347) (Schulman et al., 2017)
- [Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) (Schulman et al., 2015)

### **Frameworks**
- NumPy: Álgebra lineal
- Requests: HTTP APIs
- Pytest: Testing framework

---

## 👨‍💻 Autor

**Cruz Sanchez**
- GitHub: [@nelson753](https://github.com/nelson753)
- Ko-fi: [AutoDebuggerPro](https://ko-fi.com/s/85f18c167d)

---

## 📄 Licencia

**MIT License** - Libre para uso comercial con atribución

---

## 🎓 Aprendizajes del Proyecto

### **Técnicos**
1. ✅ Arquitectura Grial 2.0 (4 AIs colaborativas)
2. ✅ PPO implementation from scratch
3. ✅ Risk management algorítmico
4. ✅ Sentiment analysis pipeline
5. ✅ Test-Driven Development (88% coverage)

### **Negocio**
1. ✅ Zero-friction model (no soporte, no logística)
2. ✅ Auto-depuración con benchmarks
3. ✅ Product-market fit validation
4. ✅ Pricing strategy ($49-$499)

---

## 🔥 Demo

### **Ejemplo de Ejecución**
```
🚀 EPISODE 1 - START
[Step 50]  Price: $60,974 | Sentiment: +0.14 | Action: BUY
[Step 100] Price: $68,227 | Sentiment: -0.30 | Action: SELL
[Step 150] Price: $58,345 | Sentiment: -0.06 | Action: HOLD

📊 EPISODE 1 - SUMMARY
Final Portfolio: $1,024.30
P&L: $+24.30
ROI: +2.43%
Sharpe Ratio: 1.82
```

---

**¿Listo para generar ingresos pasivos con IA?** 🚀💰

Start with: `python intelligent_investment_bot.py --episodes 10 --exchange paper --capital 1000`
