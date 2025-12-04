# 🤖 SISTEMA DE TRADING AUTÓNOMO

## 🚀 Características Revolucionarias

Este NO es un bot simple. Es un **sistema autónomo completo** que:

### ✅ Funcionalidades Avanzadas

1. **Trading 100% Autónomo**
   - Compra y vende sin intervención humana
   - Análisis continuo 24/7
   - Decisiones basadas en múltiples indicadores

2. **Indicadores Técnicos Profesionales**
   - **RSI** (Relative Strength Index) - Detecta sobrecompra/sobreventa
   - **MACD** (Moving Average Convergence Divergence) - Tendencias
   - **Bollinger Bands** - Volatilidad y puntos de entrada/salida
   - **Momentum** - Fuerza de movimientos
   - **Volatility** - Ajuste dinámico de riesgo

3. **Gestión de Riesgo Avanzada**
   - **Stop Loss automático**: 2% por posición
   - **Take Profit automático**: 5% por posición
   - **Kill Switch triple nivel**: 2% / 3% / 5% MDD
   - **Position sizing dinámico**: Ajustado a volatilidad
   - **Max posiciones simultáneas**: Diversificación controlada

4. **Inteligencia de Decisión**
   - Sistema de confianza (confidence score)
   - Solo ejecuta con 60%+ de confianza
   - Combina múltiples señales
   - Aprende de patrones de precio

5. **Dashboard en Tiempo Real**
   - Visualización web profesional
   - Actualización cada 5 segundos
   - Métricas completas
   - Historial de trades

6. **Monitoreo y Logs**
   - Registro de todas las decisiones
   - Guardado automático de sesiones
   - Análisis de performance
   - Win rate y métricas avanzadas

---

## 📋 Requisitos

```bash
pip install numpy requests flask
```

---

## 🎯 ¿Cómo Funciona?

### 1. Análisis Continuo
El sistema revisa el mercado cada 30 segundos:
```
Precio BTC → Indicadores técnicos → Señal de trading → Decisión
```

### 2. Generación de Señales

#### RSI (Índice de Fuerza Relativa)
- **< 30**: Oversold → Señal de COMPRA (fuerte)
- **> 70**: Overbought → Señal de VENTA (fuerte)
- **40-60**: Neutral

#### MACD
- **MACD > Signal + Histogram > 0**: Tendencia alcista → COMPRA
- **MACD < Signal + Histogram < 0**: Tendencia bajista → VENTA

#### Bollinger Bands
- **Precio ≤ Banda inferior**: Posible rebote → COMPRA
- **Precio ≥ Banda superior**: Posible retroceso → VENTA

#### Momentum
- **> +1%**: Impulso positivo → COMPRA
- **< -1%**: Impulso negativo → VENTA

### 3. Sistema de Confianza
El bot combina todas las señales y calcula un **confidence score**:
- **60-75%**: Señal moderada → Ejecuta con precaución
- **75-90%**: Señal fuerte → Ejecuta con confianza
- **90-100%**: Señal muy fuerte → Ejecuta con máxima confianza

Solo ejecuta si `confidence >= 60%`

### 4. Protecciones Automáticas

#### Stop Loss (2%)
Si precio baja 2% desde entrada → Vende automáticamente
```
Ejemplo: Compra a $100,000 → Stop Loss en $98,000
```

#### Take Profit (5%)
Si precio sube 5% desde entrada → Vende automáticamente
```
Ejemplo: Compra a $100,000 → Take Profit en $105,000
```

#### Kill Switch
- **Warning (2% MDD)**: Alerta, continúa operando
- **Critical (3% MDD)**: Alerta crítica, continúa con precaución
- **Emergency (5% MDD)**: DETIENE TODO, cierra todas las posiciones

---

## 🚀 Uso

### Opción 1: Solo el Bot Autónomo

```bash
python autonomous_trading_system.py
```

**Prompts interactivos:**
1. Selecciona modo:
   - `1` = Paper Trading (simulado, SIN riesgo)
   - `2` = Live Trading (real, CON dinero)

2. Si seleccionas Live, confirma escribiendo:
   ```
   SI ACEPTO AUTONOMO
   ```

3. Duración en horas (1-24):
   ```
   24  # Para 1 día completo
   ```

### Opción 2: Bot + Dashboard (RECOMENDADO)

**Terminal 1 - Bot:**
```bash
python autonomous_trading_system.py
```

**Terminal 2 - Dashboard:**
```bash
python dashboard_autonomous.py
```

Luego abre en tu navegador:
```
http://localhost:5000
```

---

## 📊 Dashboard Web

El dashboard muestra en tiempo real:

### Métricas Principales
- **Portfolio Value**: Valor total actual
- **P&L**: Ganancia/Pérdida ($ y %)
- **Max Drawdown**: Máxima caída desde el pico
- **Total Trades**: Número de operaciones
- **Win Rate**: Porcentaje de trades ganadores
- **Cash**: Efectivo disponible
- **Posiciones**: Número de posiciones abiertas
- **Precio BTC**: Precio actual de Bitcoin

### Señales Actuales
- Estado de cada indicador técnico
- Valores en tiempo real

### Historial de Trades
- Últimas 10 operaciones
- Detalles completos (precio, cantidad, P&L)
- Razón de la operación (señal, stop loss, take profit)

---

## 📈 Ejemplos de Operación

### Escenario 1: Mercado Alcista
```
[10:00:00] Iteration #1
  Precio BTC: $90,000
  RSI: 28 (Oversold)
  MACD: Bullish
  Bollinger: Precio en banda inferior
  
🎯 SEÑAL: BUY (Confidence: 85%)

[BUY] BTC-USD
  Price: $90,000
  Amount: 0.00004444 ($4.00 USD)
  Stop Loss: $88,200
  Take Profit: $94,500
```

### Escenario 2: Take Profit Activado
```
[11:30:00] Iteration #45
  Precio BTC: $94,600

💰 TAKE PROFIT TRIGGERED for BTC-USD

[SELL] BTC-USD - TAKE_PROFIT
  Entry: $90,000 → Exit: $94,600
  Amount: 0.00004444
  P&L: $+0.20 (+5.11%)
```

### Escenario 3: Stop Loss Activado
```
[14:15:00] Iteration #87
  Precio BTC: $88,100

🛑 STOP LOSS TRIGGERED for BTC-USD

[SELL] BTC-USD - STOP_LOSS
  Entry: $90,000 → Exit: $88,100
  Amount: 0.00004444
  P&L: $-0.08 (-2.11%)
```

---

## 🛡️ Seguridad

### Niveles de Protección

1. **Paper Trading First**
   - SIEMPRE empieza en modo simulado
   - Valida estrategia sin riesgo
   - Confirma que todo funciona

2. **Confirmación Explícita**
   - Para live trading necesitas escribir exactamente:
   - `SI ACEPTO AUTONOMO`

3. **Kill Switch Automático**
   - Detiene todo si MDD >= 5%
   - Cierra todas las posiciones
   - Protege tu capital

4. **Stop Loss Individual**
   - Cada posición tiene su propio stop loss
   - Límita pérdidas al 2% por trade

5. **Position Limits**
   - Máximo 3 posiciones simultáneas
   - Diversificación de riesgo

6. **CTRL+C Emergency Stop**
   - Detiene inmediatamente
   - Guarda sesión
   - Cierra posiciones si es necesario

---

## 📁 Archivos Generados

### Sessions JSON
```
autonomous_session_20251202_103045.json
```

Contiene:
- Estado completo del portfolio
- Historial de trades
- Log de decisiones
- Métricas de performance

### Estructura del JSON
```json
{
  "timestamp": "2025-12-02T10:30:45",
  "mode": "PAPER",
  "initial_capital": 40.0,
  "final_portfolio": 42.15,
  "cash": 38.20,
  "positions": {
    "BTC-USD": {
      "amount": 0.00004444,
      "entry_price": 90000,
      "stop_loss": 88200,
      "take_profit": 94500
    }
  },
  "pnl": 2.15,
  "pnl_pct": 5.375,
  "max_drawdown": 0.018,
  "total_trades": 8,
  "trade_history": [...],
  "decisions_log": [...]
}
```

---

## 🎓 Mejores Prácticas

### 1. Fase de Prueba (Paper Trading)
```bash
# Día 1-3: Paper trading 24h/día
python autonomous_trading_system.py
# Modo: 1 (Paper)
# Duración: 24 horas
```

**Revisa:**
- ✅ P&L positivo
- ✅ MDD < 3%
- ✅ Win rate > 50%
- ✅ 0 Kill Switch events

### 2. Fase Piloto (Live con vigilancia)
```bash
# Día 4-7: Live trading con monitoreo
# Terminal 1:
python autonomous_trading_system.py
# Modo: 2 (Live)
# Duración: 8 horas

# Terminal 2:
python dashboard_autonomous.py
```

**Monitorea activamente:**
- Cada hora las primeras 24h
- Cada 3 horas después

### 3. Fase Autónoma (Live 24/7)
```bash
# Semana 2+: Autónomo con checks diarios
python autonomous_trading_system.py
# Modo: 2 (Live)
# Duración: 24 horas
```

**Check diario:**
- Performance general
- MDD acumulado
- Ajustes si es necesario

---

## 📊 Métricas de Éxito

### KPIs Clave

1. **Win Rate**: > 50%
   - Porcentaje de trades ganadores

2. **Profit Factor**: > 1.5
   - Ganancias totales / Pérdidas totales

3. **Max Drawdown**: < 5%
   - Máxima caída desde el pico

4. **Sharpe Ratio**: > 1.0
   - Retorno ajustado por riesgo

5. **ROI Mensual**: > 5%
   - Retorno sobre inversión

---

## 🔧 Configuración Avanzada

### Ajustar Parámetros

En `autonomous_trading_system.py`:

```python
# Capital y position sizing
CAPITAL_INICIAL = 40.0           # Tu capital
POSITION_SIZE_PERCENT = 0.10     # 10% por trade

# Risk management
STOP_LOSS_PERCENT = 0.02         # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05       # 5% take profit
MAX_POSITIONS = 3                # Max posiciones

# Timing
CHECK_INTERVAL = 30              # Segundos entre checks

# Kill Switch
MDD_WARNING = 0.02               # 2% warning
MDD_CRITICAL = 0.03              # 3% critical
MDD_EMERGENCY = 0.05             # 5% emergency stop
```

### Confidence Threshold

En línea ~430:
```python
# Solo ejecuta si confidence >= 60%
if signal['action'] == 'BUY' and signal['confidence'] >= 60:
```

Puedes ajustar a:
- `70` = Más conservador
- `50` = Más agresivo

---

## 🚀 Escalamiento

### Fase 3: $80 USD
Criterios para duplicar capital:
- ✅ 30 días consecutivos con P&L positivo
- ✅ Win rate > 55%
- ✅ MDD máximo < 3%
- ✅ 0 Kill Switch events

### Fase 4: $160 USD
Criterios:
- ✅ 60 días en Fase 3 exitosos
- ✅ Win rate > 60%
- ✅ Sharpe ratio > 1.5

### Largo Plazo
Con crecimiento compuesto del 5% mensual:
- Mes 3: ~$46
- Mes 6: ~$54
- Mes 12: ~$72
- Año 2: ~$130

---

## ⚠️ IMPORTANTE

### ⛔ NO USAR LIVE TRADING SI:
- No has probado en paper mode primero
- No entiendes cómo funciona el sistema
- No puedes monitorear el dashboard
- Estás usando dinero que no puedes perder

### ✅ SÍ USAR LIVE TRADING SI:
- Paper trading fue exitoso (>7 días)
- Entiendes todos los indicadores
- Tienes el dashboard corriendo
- Capital es dinero que puedes arriesgar
- Has revisado todas las configuraciones

---

## 🆘 Troubleshooting

### El bot no ejecuta trades
**Causa**: Confidence score muy bajo
**Solución**: Ajusta threshold o espera mejores condiciones

### MDD muy alto
**Causa**: Mercado muy volátil o stop loss muy amplio
**Solución**: Reduce STOP_LOSS_PERCENT o aumenta MDD_WARNING

### Muchos Stop Loss
**Causa**: Stop loss muy ajustado
**Solución**: Aumenta STOP_LOSS_PERCENT de 2% a 3%

### Dashboard no carga
**Causa**: Puerto 5000 ocupado
**Solución**: Cambia puerto en `dashboard_autonomous.py`:
```python
app.run(host='0.0.0.0', port=5001)
```

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisa los logs en las sesiones JSON
2. Verifica el dashboard para métricas
3. Consulta este README

---

## 🏆 Conclusión

Este sistema NO es un juguete. Es una plataforma profesional de trading autónomo que:

✅ Toma decisiones basadas en análisis técnico real
✅ Protege tu capital con múltiples niveles de seguridad
✅ Opera 24/7 sin intervención humana
✅ Aprende y se adapta a condiciones del mercado
✅ Proporciona transparencia total con dashboard

**Úsalo sabiamente. Empieza con paper trading. Escala gradualmente.**

---

**Versión**: 1.0  
**Fecha**: Diciembre 2, 2025  
**Autor**: Sistema de Trading Autónomo  
**Licencia**: Uso personal
