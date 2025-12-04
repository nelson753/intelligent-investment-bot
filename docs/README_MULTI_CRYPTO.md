# 🚀 SISTEMA MULTI-CRYPTO TRADING

Sistema de trading autónomo que monitorea y opera **5 criptomonedas simultáneamente** para maximizar oportunidades.

## 📊 Cryptos Monitoreadas

1. **BTC-USD** (Bitcoin) - Alta capitalización, menor volatilidad
2. **ETH-USD** (Ethereum) - Alta capitalización, DeFi líder
3. **SOL-USD** (Solana) - Media capitalización, alta velocidad
4. **DOGE-USD** (Dogecoin) - Alta volatilidad, comunidad activa
5. **XRP-USD** (Ripple) - Pagos internacionales

## ✨ Características Avanzadas

### 🎯 Análisis Independiente
- Cada crypto tiene sus propios indicadores técnicos
- RSI, MACD, Bollinger Bands personalizados
- Análisis de momentum y volatilidad individual

### 🔗 Correlación Entre Activos
- Matriz de correlación para evitar sobre-exposición
- Previene tener múltiples posiciones en activos altamente correlacionados
- Diversificación inteligente del riesgo

### 📈 Ranking de Oportunidades
- Sistema de scoring automático
- Prioriza señales de alta confianza
- Mayor score = Mayor confianza × Volatilidad
- Asigna capital a las mejores oportunidades primero

### 💡 Ventajas Multi-Crypto

**Más Oportunidades:**
- 5 mercados = 5× más posibilidades de señales
- Siempre hay movimiento en alguna crypto
- No dependes de un solo activo

**Mejor Diversificación:**
- Riesgo distribuido en múltiples activos
- Menor exposición a crashes individuales
- Portfolio más balanceado

**Optimización de Capital:**
- Asigna automáticamente a mejores señales
- Maximiza retorno esperado
- Evita oportunidades mediocres

## 🚀 Uso Rápido

```bash
# Ejecutar el bot multi-crypto
python multi_crypto_trading.py

# Opciones:
# 1. Paper Trading (Simulado) ← Recomendado para empezar
# 2. Live Trading (Real)

# Dashboard en tiempo real (en otra terminal)
python dashboard_multi_crypto.py
# Abre: http://localhost:5000
```

## 📊 Dashboard Multi-Crypto

El dashboard muestra:
- **Vista de todas las cryptos** monitoreadas
- **Señales en tiempo real** (BUY/SELL/HOLD)
- **Posiciones activas** con P&L individual
- **Top 3 oportunidades** rankeadas automáticamente
- **Portfolio total** y estadísticas

## 🎮 Ejemplo de Uso

```bash
# Terminal 1: Ejecutar bot
python multi_crypto_trading.py
> Select mode: 1  # Paper Trading
> Duration: 1     # 1 hora

# Terminal 2: Dashboard
python dashboard_multi_crypto.py

# Navegador: http://localhost:5000
```

## 📈 Cómo Funciona

### 1. Recolección de Datos
```
Cada 30 segundos:
├─ BTC-USD: $93,000
├─ ETH-USD: $3,400
├─ SOL-USD: $220
├─ DOGE-USD: $0.40
└─ XRP-USD: $2.10
```

### 2. Análisis Independiente
```
Por cada crypto:
├─ RSI (sobrecompra/sobreventa)
├─ MACD (momentum)
├─ Bollinger Bands (volatilidad)
├─ Momentum (tendencia)
└─ Señal: BUY/SELL/HOLD + Confianza %
```

### 3. Ranking de Oportunidades
```
Score = Confianza × (1 + Volatilidad/100)

Ejemplo:
1. SOL-USD: BUY (75%) → Score: 82.5
2. DOGE-USD: BUY (68%) → Score: 74.8
3. ETH-USD: BUY (62%) → Score: 64.2
```

### 4. Ejecución Automática
```
Si confianza ≥ 60%:
├─ Top oportunidad → Ejecuta primero
├─ Segunda mejor → Si hay capital
└─ Tercera mejor → Si hay capital
Max 3 posiciones simultáneas
```

## ⚙️ Configuración

```python
CRYPTO_PAIRS = [
    "BTC-USD",
    "ETH-USD", 
    "SOL-USD",
    "DOGE-USD",
    "XRP-USD"
]

CAPITAL_INICIAL = 40.0        # $40 USD
POSITION_SIZE_PERCENT = 0.10   # 10% por trade ($4)
MAX_POSITIONS = 3              # Máximo 3 cryptos a la vez
STOP_LOSS_PERCENT = 0.02       # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05     # 5% take profit
```

## 🛡️ Gestión de Riesgo

### Stop Loss & Take Profit
- Cada posición tiene SL/TP automático
- Se verifica cada iteración
- Cierre automático al alcanzar niveles

### Kill Switch Multi-Nivel
- **Warning (2%)**: Alerta, continúa
- **Critical (3%)**: Advertencia crítica
- **Emergency (5%)**: Cierra TODO

### Diversificación
- Máximo 3 posiciones abiertas
- Análisis de correlación
- Capital distribuido inteligentemente

## 📊 Ejemplo de Output

```
================================================================================
[2025-12-02 21:30:00] Iteration #15
================================================================================

💼 PORTFOLIO:
  Cash: $28.00
  Positions: 3/3
  Total Value: $42.50
  P&L: $+2.50 (+6.25%)
  MDD: 0.00%

📊 CRYPTOS MONITORED:
  🟢 BTC-USD: $93,500 | BUY (72%) [HOLDING: +1.2%]
     └─ MACD bullish, Strong momentum (+2.8%)
  
  ⚪ ETH-USD: $3,380 | HOLD (45%)
     └─ Neutral market
  
  🟢 SOL-USD: $225.50 | BUY (78%) [HOLDING: +3.5%]
     └─ RSI oversold (28.5), Price below lower BB
  
  🔴 DOGE-USD: $0.385 | SELL (65%)
     └─ RSI overbought (74.2), Negative momentum (-1.5%)
  
  🟢 XRP-USD: $2.15 | BUY (68%) [HOLDING: +2.1%]
     └─ MACD bullish, Strong momentum (+2.2%)

🎯 TOP OPPORTUNITIES:
  1. SOL-USD: BUY (78%)
     └─ RSI oversold (28.5), Price below lower BB
  2. BTC-USD: BUY (72%)
     └─ MACD bullish, Strong momentum (+2.8%)
  3. XRP-USD: BUY (68%)
     └─ MACD bullish, Strong momentum (+2.2%)
```

## 💡 Tips

1. **Empieza en Paper Trading** para ver cómo funciona
2. **Monitorea 1 hora** para ver varios ciclos
3. **Revisa el dashboard** para vista visual
4. **Analiza correlaciones** - evita cryptos que se mueven igual
5. **Mayor volatilidad = Mayor riesgo + Mayor potencial**

## 🔄 Comparación

### Bot Simple (1 Crypto)
- ✅ Fácil de entender
- ✅ Menor complejidad
- ❌ Pocas oportunidades
- ❌ Dependencia de 1 activo

### Bot Multi-Crypto (5 Cryptos)
- ✅ 5× más oportunidades
- ✅ Mejor diversificación
- ✅ Ranking automático
- ✅ Optimización de capital
- ⚠️ Mayor complejidad (pero automatizada)

## 🎯 Casos de Uso

**Mercado Lateral (BTC sin movimiento):**
- Bot simple: 0 señales ❌
- Multi-crypto: SOL/DOGE pueden tener señales ✅

**Alta Volatilidad General:**
- Bot simple: 1 operación máximo
- Multi-crypto: Hasta 3 operaciones simultáneas

**Caída de Bitcoin:**
- Bot simple: Solo puede SELL o esperar
- Multi-crypto: Otras altcoins pueden subir

## 📁 Archivos

- `multi_crypto_trading.py` - Sistema principal multi-crypto
- `dashboard_multi_crypto.py` - Dashboard web visual
- `multi_crypto_session_*.json` - Sesiones guardadas

## 🚀 Próximos Pasos

1. Ejecuta en Paper Trading por 1 hora
2. Observa qué cryptos generan más señales
3. Revisa correlaciones en el código
4. Ajusta CRYPTO_PAIRS si quieres otras monedas
5. Cuando te sientas cómodo, prueba con capital real pequeño

---

**¡Más cryptos = Más oportunidades!** 🚀
