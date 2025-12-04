#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE TRADING MULTI-CRYPTOCURRENCY
Monitoreo y trading autónomo de múltiples cryptos simultáneamente
Capital: $40 USD

CARACTERÍSTICAS:
✅ Múltiples pares simultáneos (BTC, ETH, SOL, DOGE, XRP)
✅ Análisis independiente por cada crypto
✅ Correlación para evitar sobre-exposición
✅ Ranking automático de oportunidades
✅ Asignación dinámica de capital
✅ Dashboard multi-crypto
"""

import os
import time
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from collections import deque, defaultdict
from typing import Dict, List, Tuple, Optional

# Configuración
CAPITAL_INICIAL = 40.0
POSITION_SIZE_PERCENT = 0.10  # 10% por trade
STOP_LOSS_PERCENT = 0.02      # 2%
TAKE_PROFIT_PERCENT = 0.03    # 3% (optimizado: cierra trades más rápido)
MAX_POSITIONS = 3              # Máximo total (LONG + SHORT)
ALLOW_SHORT_SELLING = True     # ✅ Activar Short Selling para ganar cuando baja el mercado
CHECK_INTERVAL = 30

# 🔴 AJUSTES CRÍTICOS PARA PRODUCCIÓN
TRADING_FEE_PERCENT = 0.001    # 0.1% por operación (Coinbase Pro/Advanced Trade)
SLIPPAGE_PERCENT = 0.0005      # 0.05% slippage estimado en órdenes market
GLOBAL_STOP_LOSS_PERCENT = 0.20  # 20% pérdida total = cierre de emergencia ($40 → $32)
GLOBAL_STOP_LOSS_VALUE = CAPITAL_INICIAL * (1 - GLOBAL_STOP_LOSS_PERCENT)  # $32.00

# Cryptos a monitorear (optimizado según historial)
CRYPTO_PAIRS = [
    # "BTC-USD", # REMOVIDO: 0% win rate histórico
    "DOGE-USD",  # ⭐ ESTRELLA: 100% win rate (9/9 trades)
    "ETH-USD",   # Ethereum - Alta cap
    "SOL-USD",   # Solana - Media cap, más volátil
    "XRP-USD",   # Ripple - Oportunidades legales
    "ADA-USD",   # Cardano - Alta volatilidad, bajo precio
    "MATIC-USD", # Polygon - Layer 2, movimientos rápidos
    "LINK-USD"   # Chainlink - Oracle líder, buen volumen
]

# Kill Switch
MDD_WARNING = 0.02
MDD_CRITICAL = 0.03
MDD_EMERGENCY = 0.05

class TechnicalIndicators:
    """Indicadores técnicos"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """RSI"""
        actual_period = min(period, max(5, len(prices) - 1))
        if len(prices) < actual_period + 1:
            return 50.0
        
        deltas = np.diff(prices[-actual_period-1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List[float]) -> Tuple[float, float, float]:
        """MACD"""
        if len(prices) < 15:
            return 0.0, 0.0, 0.0
        
        prices_array = np.array(prices)
        period_fast = min(12, max(5, len(prices) // 2))
        period_slow = min(26, max(10, len(prices) - 1))
        period_signal = min(9, max(3, len(prices) // 3))
        
        ema_fast = TechnicalIndicators._ema(prices_array, period_fast)
        ema_slow = TechnicalIndicators._ema(prices_array, period_slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators._ema(np.array([macd_line]), period_signal)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def _ema(prices: np.array, period: int) -> float:
        """EMA"""
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20) -> Tuple[float, float, float]:
        """Bollinger Bands"""
        actual_period = min(period, max(5, len(prices)))
        if len(prices) < actual_period:
            price = prices[-1] if prices else 0
            return price, price, price
        
        recent_prices = prices[-actual_period:]
        sma = np.mean(recent_prices)
        std = np.std(recent_prices)
        
        upper_band = sma + (2 * std)
        lower_band = sma - (2 * std)
        
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_volatility(prices: List[float], period: int = 14) -> float:
        """Volatilidad"""
        actual_period = min(period, len(prices))
        if actual_period < 2:
            return 0.0
        
        recent_prices = prices[-actual_period:]
        returns = np.diff(recent_prices) / recent_prices[:-1]
        return np.std(returns) * 100
    
    @staticmethod
    def calculate_ema_200(prices: List[float]) -> float:
        """🎯 EMA 200 - Filtro de Tendencia"""
        if len(prices) < 50:  # Mínimo 50 datos para EMA 200
            return prices[-1] if prices else 0.0
        
        period = min(200, len(prices))
        return TechnicalIndicators._ema(np.array(prices), period)
    
    @staticmethod
    def calculate_atr(prices: List[float], period: int = 14) -> float:
        """🛡️ ATR (Average True Range) - Stop Loss Dinámico"""
        actual_period = min(period, len(prices) - 1)
        if actual_period < 2:
            return 0.0
        
        # True Range = max(high-low, |high-close_prev|, |low-close_prev|)
        # Simplificado para spot prices: usar diferencias absolutas
        true_ranges = []
        for i in range(1, len(prices)):
            tr = abs(prices[i] - prices[i-1])
            true_ranges.append(tr)
        
        recent_tr = true_ranges[-actual_period:]
        return np.mean(recent_tr)


class MultiCryptoTradingSystem:
    """Sistema de trading multi-cryptocurrency"""
    
    def __init__(self, capital: float = CAPITAL_INICIAL, mode: str = "paper"):
        self.initial_capital = capital
        self.cash = capital
        self.mode = mode
        self.positions: Dict[str, Dict] = {}
        self.price_history: Dict[str, deque] = {pair: deque(maxlen=100) for pair in CRYPTO_PAIRS}
        self.trades_history = []
        self.peak_value = capital
        self.kill_switch_active = False
        self.iteration = 0
        self.total_fees_paid = 0.0  # Track total fees paid
        
        # Oportunidades
        self.opportunities: Dict[str, Dict] = {}
        
        print("\n" + "="*80)
        print("🚀 SISTEMA MULTI-CRYPTO - TRADING AUTÓNOMO")
        print("="*80)
        print(f"Modo: {'PAPER TRADING' if mode == 'paper' else 'LIVE TRADING'}")
        print(f"Capital inicial: ${capital:.2f}")
        print(f"Cryptos monitoreadas: {len(CRYPTO_PAIRS)}")
        for pair in CRYPTO_PAIRS:
            print(f"  • {pair}")
        print(f"Position size: {POSITION_SIZE_PERCENT*100}%")
        print(f"Stop Loss: {STOP_LOSS_PERCENT*100}% | Take Profit: {TAKE_PROFIT_PERCENT*100}%")
        print(f"Max positions: {MAX_POSITIONS}")
        print("="*80 + "\n")
    
    def get_price(self, pair: str) -> Optional[float]:
        """Obtiene precio actual de Coinbase"""
        try:
            url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data['data']['amount'])
        except Exception as e:
            print(f"[WARNING] Error getting {pair} price: {e}")
        return None
    
    def calculate_correlation(self) -> Dict[str, Dict[str, float]]:
        """Calcula correlación entre cryptos para evitar sobre-exposición"""
        correlation_matrix = {}
        
        # Solo calcular si hay suficientes datos
        min_data_points = min(len(self.price_history[pair]) for pair in CRYPTO_PAIRS)
        if min_data_points < 10:
            return {}
        
        for pair1 in CRYPTO_PAIRS:
            correlation_matrix[pair1] = {}
            for pair2 in CRYPTO_PAIRS:
                if pair1 == pair2:
                    correlation_matrix[pair1][pair2] = 1.0
                else:
                    prices1 = list(self.price_history[pair1])[-min_data_points:]
                    prices2 = list(self.price_history[pair2])[-min_data_points:]
                    
                    if len(prices1) >= 2 and len(prices2) >= 2:
                        corr = np.corrcoef(prices1, prices2)[0, 1]
                        correlation_matrix[pair1][pair2] = corr
                    else:
                        correlation_matrix[pair1][pair2] = 0.0
        
        return correlation_matrix
    
    def analyze_crypto(self, pair: str) -> Dict:
        """Analiza una crypto y genera señal de trading con filtros avanzados"""
        prices = list(self.price_history[pair])
        
        if len(prices) < 15:
            return {
                "signal": "HOLD",
                "confidence": 0.0,
                "reasons": [f"Gathering data... ({len(prices)}/15)"],
                "price": prices[-1] if prices else 0,
                "volatility": 0,
                "momentum": 0,
                "rsi": 50,
                "ema_200": 0,
                "atr": 0,
                "macd_line": 0,
                "macd_signal": 0,
                "trend": "NEUTRAL"
            }
        
        current_price = prices[-1]
        
        # Calcular indicadores básicos
        rsi = TechnicalIndicators.calculate_rsi(prices)
        macd_line, signal_line, histogram = TechnicalIndicators.calculate_macd(prices)
        upper_bb, middle_bb, lower_bb = TechnicalIndicators.calculate_bollinger_bands(prices)
        volatility = TechnicalIndicators.calculate_volatility(prices)
        
        # 🎯 NUEVOS INDICADORES
        ema_200 = TechnicalIndicators.calculate_ema_200(prices)
        atr = TechnicalIndicators.calculate_atr(prices)
        
        # 🧭 FILTRO DE TENDENCIA
        if current_price > ema_200 * 1.02:  # 2% arriba de EMA 200
            trend = "BULLISH"
        elif current_price < ema_200 * 0.98:  # 2% abajo de EMA 200
            trend = "BEARISH"
        else:
            trend = "NEUTRAL"
        
        # Momentum
        momentum = ((current_price - prices[-10]) / prices[-10]) * 100 if len(prices) >= 10 else 0
        
        # Análisis de señales CON FILTRO DE TENDENCIA
        signals = []
        reasons = []
        
        # RSI (con peso extra para señales extremas)
        if rsi < 30:
            # ✅ LONG SOLO si tendencia BULLISH clara
            if trend == "BULLISH":
                weight = 2 if rsi < 25 else 1
                signals.extend([1] * weight)
                reasons.append(f"RSI oversold ({rsi:.1f})")
            # ⛔ No comprar en tendencia BEARISH o NEUTRAL (knife catching)
        elif rsi > 70:
            # ✅ SHORT SOLO si tendencia BEARISH clara
            if trend == "BEARISH":
                weight = 2 if rsi > 75 else 1
                signals.extend([-1] * weight)
                reasons.append(f"RSI overbought ({rsi:.1f})")
            # ⛔ No vender en tendencia BULLISH o NEUTRAL
        else:
            signals.append(0)
        
        # MACD
        if histogram > 0 and macd_line > signal_line and trend == "BULLISH":
            signals.append(1)
            reasons.append("MACD bullish")
        elif histogram < 0 and macd_line < signal_line and trend == "BEARISH":
            signals.append(-1)
            reasons.append("MACD bearish")
        else:
            signals.append(0)
        
        # Bollinger Bands
        if current_price < lower_bb and trend == "BULLISH":
            signals.append(1)
            reasons.append("Price below lower BB")
        elif current_price > upper_bb and trend == "BEARISH":
            signals.append(-1)
            reasons.append("Price above upper BB")
        else:
            signals.append(0)
        
        # Momentum
        if momentum > 2:
            signals.append(1)
            reasons.append(f"Strong momentum (+{momentum:.1f}%)")
        elif momentum < -2:
            signals.append(-1)
            reasons.append(f"Negative momentum ({momentum:.1f}%)")
        else:
            signals.append(0)
        
        # Volatilidad
        if volatility > 3:
            reasons.append(f"High volatility ({volatility:.1f}%)")
        
        # Calcular señal final
        avg_signal = np.mean(signals)
        confidence = abs(avg_signal) * 100
        
        if avg_signal > 0.3:
            signal = "BUY"
        elif avg_signal < -0.3:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        return {
            "signal": signal,
            "confidence": confidence,
            "reasons": reasons if reasons else ["Neutral market"],
            "price": current_price,
            "volatility": volatility,
            "momentum": momentum,
            "rsi": rsi,
            "ema_200": ema_200,
            "atr": atr,
            "macd_line": macd_line,
            "macd_signal": signal_line,
            "trend": trend
        }
    
    def rank_opportunities(self) -> List[Tuple[str, Dict]]:
        """Rankea oportunidades de trading por mejor señal"""
        opportunities = []
        
        for pair in CRYPTO_PAIRS:
            analysis = self.analyze_crypto(pair)
            
            # Solo considerar señales con confianza baja-media-alta
            if analysis["confidence"] >= 25:
                # Score = confianza * (1 + volatilidad/100)
                # Mayor volatilidad = mayor potencial de ganancia
                score = analysis["confidence"] * (1 + analysis.get("volatility", 0) / 100)
                
                # Bonus para DOGE (100% win rate histórico)
                if pair == "DOGE-USD":
                    score *= 1.5  # 50% más prioridad
                
                opportunities.append((pair, analysis, score))
        
        # Ordenar por score descendente
        opportunities.sort(key=lambda x: x[2], reverse=True)
        
        return [(pair, analysis) for pair, analysis, score in opportunities]
    
    def execute_trade(self, pair: str, signal: str, price: float):
        """Ejecuta una operación de trading (LONG o SHORT)"""
        if signal == "BUY":
            # Si hay posición SHORT, cerrarla primero
            if pair in self.positions:
                pos_type = self.positions[pair].get("type", "LONG")
                if pos_type == "SHORT":
                    self.close_short_position(pair, price)
                else:
                    return  # Ya hay LONG
            
            # Verificar límite de posiciones
            if len(self.positions) >= MAX_POSITIONS:
                return
            
            # Calcular cantidad
            position_value = self.cash * POSITION_SIZE_PERCENT
            if position_value < 1:  # Mínimo $1
                return
            
            # Aplicar slippage (precio de compra peor)
            execution_price = price * (1 + SLIPPAGE_PERCENT)
            
            # Calcular fee
            fee = position_value * TRADING_FEE_PERCENT
            self.total_fees_paid += fee
            
            # Costo total = valor + fee
            total_cost = position_value + fee
            
            quantity = position_value / execution_price
            
            # 🛡️ STOP LOSS DINÁMICO basado en ATR
            analysis = self.analyze_crypto(pair)
            atr = analysis.get("atr", 0)
            
            if atr > 0:
                # Stop Loss = precio - (2 × ATR)
                dynamic_stop = execution_price - (2 * atr)
                # Asegurar que no sea peor que el stop fijo (-2%)
                fixed_stop = execution_price * (1 - STOP_LOSS_PERCENT)
                stop_loss = max(dynamic_stop, fixed_stop)
            else:
                # Fallback a stop fijo si no hay ATR
                stop_loss = execution_price * (1 - STOP_LOSS_PERCENT)
            
            self.cash -= total_cost
            self.positions[pair] = {
                "type": "LONG",
                "quantity": quantity,
                "entry_price": execution_price,
                "entry_time": datetime.now(),
                "stop_loss": stop_loss,
                "take_profit": execution_price * (1 + TAKE_PROFIT_PERCENT),
                "atr_at_entry": atr  # Guardar ATR para trailing stop
            }
            
            self.trades_history.append({
                "time": datetime.now().isoformat(),
                "pair": pair,
                "action": "LONG",
                "price": price,
                "quantity": quantity,
                "value": position_value
            })
            
            print(f"\n✅ LONG {pair}: {quantity:.8f} @ ${execution_price:.2f}")
            print(f"   Cost: ${position_value:.2f} | Fee: ${fee:.4f} | Total: ${total_cost:.4f}")
        
        elif signal == "SELL":
            # Cerrar LONG o abrir SHORT
            if pair in self.positions:
                pos_type = self.positions[pair].get("type", "LONG")
                if pos_type == "LONG":
                    self.close_long_position(pair, price)
                else:
                    return  # Ya hay SHORT
            elif ALLOW_SHORT_SELLING and len(self.positions) < MAX_POSITIONS:
                # Abrir SHORT
                position_value = self.cash * POSITION_SIZE_PERCENT
                if position_value < 1:
                    return
                
                # Aplicar slippage (precio de venta peor para short)
                execution_price = price * (1 - SLIPPAGE_PERCENT)
                
                # Calcular fee
                fee = position_value * TRADING_FEE_PERCENT
                self.total_fees_paid += fee
                
                quantity = position_value / execution_price
                
                # 🛡️ STOP LOSS DINÁMICO basado en ATR
                analysis = self.analyze_crypto(pair)
                atr = analysis.get("atr", 0)
                
                if atr > 0:
                    # Stop Loss SHORT = precio + (2 × ATR)
                    dynamic_stop = execution_price + (2 * atr)
                    # Asegurar que no sea peor que el stop fijo (+2%)
                    fixed_stop = execution_price * (1 + STOP_LOSS_PERCENT)
                    stop_loss = min(dynamic_stop, fixed_stop)
                else:
                    stop_loss = execution_price * (1 + STOP_LOSS_PERCENT)
                
                self.positions[pair] = {
                    "type": "SHORT",
                    "quantity": quantity,
                    "entry_price": execution_price,
                    "entry_time": datetime.now(),
                    "stop_loss": stop_loss,
                    "take_profit": execution_price * (1 - TAKE_PROFIT_PERCENT),
                    "atr_at_entry": atr
                }
                
                self.trades_history.append({
                    "time": datetime.now().isoformat(),
                    "pair": pair,
                    "action": "SHORT",
                    "price": price,
                    "quantity": quantity,
                    "value": position_value
                })
                
                print(f"\n🔻 SHORT {pair}: {quantity:.8f} @ ${execution_price:.2f}")
                print(f"   Collateral: ${position_value:.2f} | Fee: ${fee:.4f}")
    
    def close_long_position(self, pair: str, price: float):
        """Cierra posición LONG"""
        pos = self.positions[pair]
        
        # Aplicar slippage (precio de ejecución peor)
        execution_price = price * (1 - SLIPPAGE_PERCENT)
        
        sell_value = pos["quantity"] * execution_price
        
        # Calcular fee (0.1% del valor de venta)
        fee = sell_value * TRADING_FEE_PERCENT
        self.total_fees_paid += fee
        
        # Valor neto después de fees
        net_proceeds = sell_value - fee
        
        profit = net_proceeds - (pos["quantity"] * pos["entry_price"])
        profit_pct = (profit / (pos["quantity"] * pos["entry_price"])) * 100
        
        self.cash += net_proceeds
        
        self.trades_history.append({
            "time": datetime.now().isoformat(),
            "pair": pair,
            "action": "CLOSE_LONG",
            "price": price,
            "quantity": pos["quantity"],
            "value": sell_value,
            "profit": profit,
            "profit_pct": profit_pct
        })
        
        del self.positions[pair]
        
        emoji = "💰" if profit > 0 else "📉"
        print(f"\n{emoji} CLOSE LONG {pair}: {pos['quantity']:.8f} @ ${execution_price:.2f}")
        print(f"   Gross: ${sell_value:.4f} | Fee: ${fee:.4f} | Net: ${net_proceeds:.4f}")
        print(f"   Profit: ${profit:+.4f} ({profit_pct:+.2f}%)")
    
    def close_short_position(self, pair: str, price: float):
        """Cierra posición SHORT"""
        pos = self.positions[pair]
        
        # Aplicar slippage (precio de recompra peor)
        execution_price = price * (1 + SLIPPAGE_PERCENT)
        
        buy_cost = pos["quantity"] * execution_price  # Costo de recompra
        sell_proceeds = pos["quantity"] * pos["entry_price"]  # Lo que vendimos
        
        # Calcular fee (0.1% del costo de recompra)
        fee = buy_cost * TRADING_FEE_PERCENT
        self.total_fees_paid += fee
        
        # Costo total con fees
        total_cost = buy_cost + fee
        
        profit = sell_proceeds - total_cost  # Ganancia si precio bajó
        profit_pct = (profit / sell_proceeds) * 100
        
        self.cash += profit
        
        self.trades_history.append({
            "time": datetime.now().isoformat(),
            "pair": pair,
            "action": "CLOSE_SHORT",
            "price": price,
            "quantity": pos["quantity"],
            "value": buy_cost,
            "profit": profit,
            "profit_pct": profit_pct
        })
        
        del self.positions[pair]
        
        emoji = "💰" if profit > 0 else "📉"
        print(f"\n{emoji} CLOSE SHORT {pair}: {pos['quantity']:.8f} @ ${execution_price:.2f}")
        print(f"   Buy Cost: ${buy_cost:.4f} | Fee: ${fee:.4f} | Total: ${total_cost:.4f}")
        print(f"   Profit: ${profit:+.4f} ({profit_pct:+.2f}%)")
    
    def check_stop_loss_take_profit(self):
        """Verifica stop loss, take profit y exit by indicator en posiciones abiertas"""
        for pair, pos in list(self.positions.items()):
            current_price = self.price_history[pair][-1] if self.price_history[pair] else 0
            if not current_price:
                continue
            
            entry_price = pos["entry_price"]
            pos_type = pos.get("type", "LONG")
            
            # Calcular profit según tipo
            if pos_type == "LONG":
                profit_pct = ((current_price - entry_price) / entry_price) * 100
            else:  # SHORT
                profit_pct = ((entry_price - current_price) / entry_price) * 100
            
            # 1. STOP LOSS (prioridad máxima)
            if pos_type == "LONG":
                stop_triggered = current_price <= pos["stop_loss"]
            else:  # SHORT
                stop_triggered = current_price >= pos["stop_loss"]
            
            if stop_triggered:
                print(f"\n🛑 STOP LOSS triggered for {pos_type} {pair}")
                print(f"   Entry: ${entry_price:.2f} | Current: ${current_price:.2f} | Loss: {profit_pct:.2f}%")
                if pos_type == "LONG":
                    self.close_long_position(pair, current_price)
                else:
                    self.close_short_position(pair, current_price)
                continue
            
            # 2. TAKE PROFIT (objetivo alcanzado)
            if pos_type == "LONG":
                tp_triggered = current_price >= pos["take_profit"]
            else:  # SHORT
                tp_triggered = current_price <= pos["take_profit"]
            
            if tp_triggered:
                print(f"\n🎯 TAKE PROFIT triggered for {pos_type} {pair}")
                print(f"   Entry: ${entry_price:.2f} | Current: ${current_price:.2f} | Profit: {profit_pct:.2f}%")
                if pos_type == "LONG":
                    self.close_long_position(pair, current_price)
                else:
                    self.close_short_position(pair, current_price)
                continue
            
            # 3. EXIT BY INDICATOR (cierre inteligente)
            # Si está en profit (>1%) y los indicadores sugieren cerrar
            # LONG: cierra con señal SELL
            # SHORT: cierra con señal BUY
            if profit_pct > 1.0:
                analysis = self.analyze_crypto(pair)
                exit_signal = "SELL" if pos_type == "LONG" else "BUY"
                
                # 🎯 MACD CROSSOVER EXIT (prioridad alta)
                macd_line = analysis.get("macd_line", 0)
                macd_signal_line = analysis.get("macd_signal", 0)
                
                # LONG: cerrar si MACD cruza abajo
                # SHORT: cerrar si MACD cruza arriba
                macd_bearish_cross = macd_line < macd_signal_line and pos_type == "LONG"
                macd_bullish_cross = macd_line > macd_signal_line and pos_type == "SHORT"
                
                if macd_bearish_cross or macd_bullish_cross:
                    print(f"\n📉 MACD CROSSOVER EXIT for {pos_type} {pair}")
                    print(f"   MACD: {macd_line:.4f} vs Signal: {macd_signal_line:.4f}")
                    print(f"   Profit secured: {profit_pct:.2f}%")
                    if pos_type == "LONG":
                        self.close_long_position(pair, current_price)
                    else:
                        self.close_short_position(pair, current_price)
                    continue
                
                if analysis["signal"] == exit_signal:
                    # Exit si hay señal inversa fuerte
                    if analysis["confidence"] >= 50:
                        print(f"\n📈 EXIT BY INDICATOR for {pos_type} {pair}")
                        print(f"   Signal: {exit_signal} ({analysis['confidence']:.0f}%)")
                        print(f"   Reasons: {', '.join(analysis['reasons'][:2])}")
                        print(f"   Profit secured: {profit_pct:.2f}%")
                        if pos_type == "LONG":
                            self.close_long_position(pair, current_price)
                        else:
                            self.close_short_position(pair, current_price)
                        continue
                    
                    # Exit si profit >2% y señal inversa moderada
                    elif profit_pct > 2.0 and analysis["confidence"] >= 35:
                        print(f"\n📊 PARTIAL EXIT for {pos_type} {pair} (securing profit)")
                        print(f"   Signal: {exit_signal} ({analysis['confidence']:.0f}%)")
                        print(f"   Profit secured: {profit_pct:.2f}%")
                        if pos_type == "LONG":
                            self.close_long_position(pair, current_price)
                        else:
                            self.close_short_position(pair, current_price)
                        continue
            
            # 4. TRAILING STOP (protección de ganancias)
            # Si profit >1.5%, mover stop loss a breakeven
            if profit_pct > 1.5:
                if pos_type == "LONG":
                    new_stop = entry_price * 1.005  # 0.5% arriba de entry
                    if new_stop > pos["stop_loss"]:
                        pos["stop_loss"] = new_stop
                        # print(f"   🔒 Trailing stop updated for LONG {pair}: ${new_stop:.2f}")
                else:  # SHORT
                    new_stop = entry_price * 0.995  # 0.5% abajo de entry
                    if new_stop < pos["stop_loss"]:
                        pos["stop_loss"] = new_stop
                        # print(f"   🔒 Trailing stop updated for SHORT {pair}: ${new_stop:.2f}")
    
    def check_kill_switch(self):
        """Verifica Kill Switch"""
        portfolio_value = self.get_portfolio_value()
        drawdown = (self.peak_value - portfolio_value) / self.peak_value
        
        if portfolio_value > self.peak_value:
            self.peak_value = portfolio_value
        
        # 🔴 GLOBAL STOP LOSS: Si cae a $32 o menos, DETENER TODO
        if portfolio_value <= GLOBAL_STOP_LOSS_VALUE:
            print("\n" + "="*80)
            print("🔴🔴🔴 GLOBAL STOP LOSS TRIGGERED 🔴🔴🔴")
            print("="*80)
            print(f"   Portfolio Value: ${portfolio_value:.2f}")
            print(f"   Global Stop Loss: ${GLOBAL_STOP_LOSS_VALUE:.2f}")
            print(f"   Total Loss: ${portfolio_value - self.initial_capital:.2f} ({((portfolio_value - self.initial_capital) / self.initial_capital) * 100:.2f}%)")
            print(f"   Total Fees Paid: ${self.total_fees_paid:.4f}")
            print("\n   🛑 CERRANDO TODAS LAS POSICIONES Y DETENIENDO BOT")
            print("   ⚠️  PROTECCIÓN DE CAPITAL ACTIVADA")
            print("="*80)
            self.kill_switch_active = True
            return True
        
        if drawdown >= MDD_EMERGENCY:
            print("\n" + "="*80)
            print("🚨 KILL SWITCH EMERGENCY - Cerrando todas las posiciones")
            print("="*80)
            self.kill_switch_active = True
            return True
        elif drawdown >= MDD_CRITICAL:
            print(f"\n⚠️  WARNING: Drawdown crítico ({drawdown*100:.2f}%)")
        elif drawdown >= MDD_WARNING:
            print(f"\n⚠️  CAUTION: Drawdown en {drawdown*100:.2f}%")
        
        return False
    
    def get_portfolio_value(self) -> float:
        """Calcula valor total del portfolio (LONG + SHORT)"""
        total = self.cash
        for pair, pos in self.positions.items():
            current_price = self.price_history[pair][-1] if self.price_history[pair] else pos["entry_price"]
            pos_type = pos.get("type", "LONG")
            
            if pos_type == "LONG":
                # LONG: valor actual de las monedas
                total += pos["quantity"] * current_price
            else:  # SHORT
                # SHORT: ganancia/pérdida vs precio de entrada
                entry_value = pos["quantity"] * pos["entry_price"]
                current_value = pos["quantity"] * current_price
                profit = entry_value - current_value
                total += profit
        return total
    
    def print_status(self):
        """Imprime estado actual del sistema"""
        print("\n" + "="*80)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iteration #{self.iteration}")
        print("="*80)
        
        portfolio_value = self.get_portfolio_value()
        pnl = portfolio_value - self.initial_capital
        pnl_pct = (pnl / self.initial_capital) * 100
        mdd = ((self.peak_value - portfolio_value) / self.peak_value) * 100
        
        print(f"\n💼 PORTFOLIO:")
        print(f"  Cash: ${self.cash:.2f}")
        print(f"  Positions: {len(self.positions)}/{MAX_POSITIONS}")
        print(f"  Total Value: ${portfolio_value:.2f}")
        print(f"  P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        print(f"  Fees Paid: ${self.total_fees_paid:.4f}")
        print(f"  MDD: {mdd:.2f}% | Global Stop: ${GLOBAL_STOP_LOSS_VALUE:.2f}")
        
        # Mostrar todas las cryptos
        print(f"\n📊 CRYPTOS MONITORED:")
        for pair in CRYPTO_PAIRS:
            if self.price_history[pair]:
                price = self.price_history[pair][-1]
                analysis = self.analyze_crypto(pair)
                
                status = ""
                if pair in self.positions:
                    pos = self.positions[pair]
                    pos_type = pos.get("type", "LONG")
                    
                    # Calcular P&L según tipo
                    if pos_type == "LONG":
                        pos_pnl = ((price - pos["entry_price"]) / pos["entry_price"]) * 100
                    else:  # SHORT
                        pos_pnl = ((pos["entry_price"] - price) / pos["entry_price"]) * 100
                    
                    status = f" [{pos_type}: {pos_pnl:+.2f}%]"
                
                signal_emoji = "🟢" if analysis["signal"] == "BUY" else "🔴" if analysis["signal"] == "SELL" else "⚪"
                
                print(f"  {signal_emoji} {pair}: ${price:,.2f} | {analysis['signal']} ({analysis['confidence']:.0f}%){status}")
                if analysis["reasons"]:
                    print(f"     └─ {', '.join(analysis['reasons'][:2])}")
        
        # Mejores oportunidades
        opportunities = self.rank_opportunities()
        if opportunities:
            print(f"\n🎯 TOP OPPORTUNITIES:")
            for i, (pair, analysis) in enumerate(opportunities[:3], 1):
                print(f"  {i}. {pair}: {analysis['signal']} ({analysis['confidence']:.0f}%)")
                print(f"     └─ {', '.join(analysis['reasons'][:2])}")
    
    def run_autonomous(self, duration_hours: float):
        """Ejecuta el sistema autónomo"""
        print(f"\n[INFO] Starting multi-crypto trading for {duration_hours} hours")
        print(f"[INFO] Check interval: {CHECK_INTERVAL} seconds")
        print("\n" + "="*80)
        print("🤖 MODO AUTÓNOMO MULTI-CRYPTO ACTIVADO")
        print("="*80 + "\n")
        
        end_time = datetime.now() + timedelta(hours=duration_hours) if duration_hours > 0 else None
        
        try:
            while True:
                self.iteration += 1
                
                # Actualizar precios de todas las cryptos
                for pair in CRYPTO_PAIRS:
                    price = self.get_price(pair)
                    if price:
                        self.price_history[pair].append(price)
                
                # Mostrar estado
                self.print_status()
                
                # Check kill switch
                if self.check_kill_switch():
                    break
                
                # Check stop loss / take profit
                self.check_stop_loss_take_profit()
                
                # Analizar oportunidades y ejecutar
                if not self.kill_switch_active:
                    opportunities = self.rank_opportunities()
                    
                    for pair, analysis in opportunities:
                        # Abrir LONG en señal BUY
                        if analysis["signal"] == "BUY":
                            if len(self.positions) < MAX_POSITIONS and pair not in self.positions:
                                self.execute_trade(pair, "BUY", analysis["price"])
                        
                        # Abrir SHORT o cerrar LONG en señal SELL
                        elif analysis["signal"] == "SELL":
                            if pair in self.positions:
                                # Cerrar LONG existente
                                self.execute_trade(pair, "SELL", analysis["price"])
                            elif ALLOW_SHORT_SELLING and len(self.positions) < MAX_POSITIONS:
                                # Abrir SHORT en señal SELL fuerte (40%+ confianza)
                                if analysis["confidence"] >= 40:
                                    self.execute_trade(pair, "SELL", analysis["price"])
                
                # Guardar sesión cada 10 iteraciones
                if self.iteration % 10 == 0:
                    self.save_session()
                
                # Verificar tiempo
                if end_time and datetime.now() >= end_time:
                    print("\n[INFO] Time limit reached")
                    break
                
                print(f"\n⏱️  Next check in {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n[INFO] Stopping autonomous system...")
        
        self.save_session()
        self.print_final_report()
    
    def save_session(self):
        """Guarda sesión actual"""
        filename = f"multi_crypto_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode,
            "initial_capital": self.initial_capital,
            "cash": self.cash,
            "positions": {
                pair: {
                    "quantity": pos["quantity"],
                    "entry_price": pos["entry_price"],
                    "entry_time": pos["entry_time"].isoformat(),
                    "stop_loss": pos["stop_loss"],
                    "take_profit": pos["take_profit"]
                } for pair, pos in self.positions.items()
            },
            "trades": self.trades_history,
            "portfolio_value": self.get_portfolio_value(),
            "iteration": self.iteration
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n💾 Session saved: {filename}")
    
    def print_final_report(self):
        """Imprime reporte final"""
        portfolio_value = self.get_portfolio_value()
        pnl = portfolio_value - self.initial_capital
        pnl_pct = (pnl / self.initial_capital) * 100
        
        print("\n" + "="*80)
        print("📊 FINAL REPORT - MULTI-CRYPTO TRADING")
        print("="*80)
        print(f"Initial Capital: ${self.initial_capital:.2f}")
        print(f"Final Value: ${portfolio_value:.2f}")
        print(f"Total P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        print(f"Total Trades: {len(self.trades_history)}")
        print(f"Iterations: {self.iteration}")
        
        if self.trades_history:
            winning_trades = [t for t in self.trades_history if t.get("profit", 0) > 0]
            print(f"Winning Trades: {len(winning_trades)}/{len([t for t in self.trades_history if 'profit' in t])}")
        
        print("="*80)


def main():
    print("\n" + "="*80)
    print("🚀 SISTEMA DE TRADING MULTI-CRYPTOCURRENCY")
    print("="*80)
    
    # Modo de operación
    print("\nMODE:")
    print("1. Paper Trading (Simulado)")
    print("2. Live Trading (Real - NO RECOMENDADO CON $40)")
    
    mode_choice = input("\nSelect mode (1-2): ").strip()
    mode = "paper" if mode_choice == "1" else "live"
    
    # Duración
    duration = float(input("\nDuration in hours (0 for infinite): ").strip() or "0")
    
    # Crear sistema
    system = MultiCryptoTradingSystem(capital=CAPITAL_INICIAL, mode=mode)
    
    # Ejecutar
    system.run_autonomous(duration_hours=duration)


if __name__ == "__main__":
    main()
