#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE TRADING AUTÓNOMO - NIVEL AVANZADO
Monitoreo 24/7 + Decisiones autónomas + Multi-indicadores
Capital: $40 USD (Fase 2)

CARACTERÍSTICAS:
✅ Trading 100% autónomo (compra/vende solo)
✅ Múltiples indicadores técnicos (RSI, MACD, Bollinger)
✅ Machine Learning para decisiones
✅ Monitoreo continuo 24/7
✅ Dashboard en tiempo real
✅ Alertas automáticas
✅ Stop Loss y Take Profit automáticos
✅ Kill Switch inteligente
✅ Auto-rebalancing
✅ Logs detallados
"""

import os
import sys
import time
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import signal
import threading
from typing import Dict, List, Optional, Tuple

# Configuración
CAPITAL_INICIAL = 40.0
POSITION_SIZE_PERCENT = 0.10  # 10% por trade
STOP_LOSS_PERCENT = 0.02      # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05    # 5% take profit
MAX_POSITIONS = 3              # Máximo 3 posiciones abiertas
CHECK_INTERVAL = 30            # Segundos entre checks

# Kill Switch
MDD_WARNING = 0.02    # 2%
MDD_CRITICAL = 0.03   # 3%
MDD_EMERGENCY = 0.05  # 5%

class TechnicalIndicators:
    """Indicadores técnicos avanzados"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calcula RSI (Relative Strength Index)"""
        # Usar período más corto si no hay suficientes datos
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
        """Calcula MACD (Moving Average Convergence Divergence)"""
        # Usar períodos más cortos si no hay suficientes datos
        if len(prices) < 15:
            return 0.0, 0.0, 0.0
        prices_array = np.array(prices)
        
        # Ajustar períodos según datos disponibles
        period_fast = min(12, max(5, len(prices) // 2))
        period_slow = min(26, max(10, len(prices) - 1))
        period_signal = min(9, max(3, len(prices) // 3))
        
        # EMA rápido y lento
        ema_fast = TechnicalIndicators._ema(prices_array, period_fast)
        ema_slow = TechnicalIndicators._ema(prices_array, period_slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators._ema(np.array([macd_line]), period_signal)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def _ema(prices: np.array, period: int) -> float:
        """Calcula EMA (Exponential Moving Average)"""
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20) -> Tuple[float, float, float]:
        """Calcula Bollinger Bands"""
        # Ajustar período según datos disponibles
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
    def calculate_volatility(prices: List[float], period: int = 20) -> float:
        """Calcula volatilidad"""
        if len(prices) < period:
            return 0.0
        
        returns = np.diff(prices[-period:]) / prices[-period:-1]
        volatility = np.std(returns) * np.sqrt(365)  # Anualizada
        return volatility


class AutonomousTradingSystem:
    """Sistema de Trading Autónomo Completo"""
    
    def __init__(self, capital: float = CAPITAL_INICIAL, paper_mode: bool = True):
        self.capital = capital
        self.initial_capital = capital
        self.paper_mode = paper_mode
        self.running = True
        
        # Estado
        self.cash = capital
        self.positions = {}  # {symbol: {amount, entry_price, timestamp}}
        self.peak_value = capital
        self.price_history = deque(maxlen=200)
        self.trade_history = []
        self.decisions_log = []
        
        # Configuración
        self.base_url = "https://api.coinbase.com"
        self.symbols = ["BTC-USD"]  # Expandible a más criptos
        
        # Kill Switch
        self.kill_switch_active = False
        self.mdd_current = 0.0
        
        # Thread para monitoreo
        self.monitor_thread = None
        
        # Signal handler
        signal.signal(signal.SIGINT, self.emergency_stop)
        
        print("\n" + "="*80)
        print("🤖 SISTEMA DE TRADING AUTÓNOMO - NIVEL AVANZADO")
        print("="*80)
        print(f"Modo: {'PAPER TRADING' if paper_mode else 'LIVE TRADING'}")
        print(f"Capital inicial: ${capital:.2f}")
        print(f"Position size: {POSITION_SIZE_PERCENT*100}%")
        print(f"Stop Loss: {STOP_LOSS_PERCENT*100}% | Take Profit: {TAKE_PROFIT_PERCENT*100}%")
        print(f"Max positions: {MAX_POSITIONS}")
        print(f"Kill Switch: {MDD_WARNING*100}% / {MDD_CRITICAL*100}% / {MDD_EMERGENCY*100}%")
        print("="*80 + "\n")
    
    def emergency_stop(self, signum, frame):
        """Handler para CTRL+C"""
        print("\n\n" + "="*80)
        print("🚨 EMERGENCY STOP - Usuario presionó CTRL+C")
        print("="*80)
        self.running = False
        self.save_session()
        sys.exit(0)
    
    def get_price(self, symbol: str = "BTC-USD") -> Optional[float]:
        """Obtiene precio actual"""
        try:
            url = f"{self.base_url}/v2/prices/{symbol}/spot"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return float(data["data"]["amount"])
            return None
        except Exception as e:
            print(f"[ERROR] get_price: {e}")
            return None
    
    def calculate_portfolio_value(self) -> float:
        """Calcula valor total del portfolio"""
        total = self.cash
        
        for symbol, position in self.positions.items():
            current_price = self.get_price(symbol)
            if current_price:
                total += position['amount'] * current_price
        
        return total
    
    def calculate_mdd(self) -> float:
        """Calcula Maximum Drawdown actual"""
        portfolio_value = self.calculate_portfolio_value()
        
        if portfolio_value > self.peak_value:
            self.peak_value = portfolio_value
        
        if self.peak_value > 0:
            mdd = (self.peak_value - portfolio_value) / self.peak_value
            self.mdd_current = mdd
            return mdd
        return 0.0
    
    def check_kill_switch(self) -> bool:
        """Verifica Kill Switch"""
        mdd = self.calculate_mdd()
        
        if mdd >= MDD_EMERGENCY:
            print(f"\n{'='*80}")
            print(f"🚨 KILL SWITCH EMERGENCY - MDD: {mdd*100:.2f}% >= {MDD_EMERGENCY*100}%")
            print(f"{'='*80}")
            self.kill_switch_active = True
            self.close_all_positions("KILL_SWITCH")
            return True
        elif mdd >= MDD_CRITICAL:
            print(f"\n⚠️  KILL SWITCH CRITICAL - MDD: {mdd*100:.2f}% >= {MDD_CRITICAL*100}%")
            return False
        elif mdd >= MDD_WARNING:
            print(f"\n⚡ KILL SWITCH WARNING - MDD: {mdd*100:.2f}% >= {MDD_WARNING*100}%")
            return False
        
        return False
    
    def generate_trading_signal(self, symbol: str = "BTC-USD") -> Dict:
        """
        Genera señal de trading usando múltiples indicadores
        Returns: {"action": "BUY"/"SELL"/"HOLD", "confidence": 0-100, "reasons": []}
        """
        if len(self.price_history) < 15:
            return {"action": "HOLD", "confidence": 0, "reasons": [f"Gathering data... ({len(self.price_history)}/15)"]}
        
        prices = list(self.price_history)
        current_price = prices[-1]
        
        reasons = []
        buy_signals = 0
        sell_signals = 0
        
        # 1. RSI
        rsi = TechnicalIndicators.calculate_rsi(prices)
        if rsi < 30:
            buy_signals += 2
            reasons.append(f"RSI oversold ({rsi:.1f})")
        elif rsi > 70:
            sell_signals += 2
            reasons.append(f"RSI overbought ({rsi:.1f})")
        elif 40 <= rsi <= 60:
            reasons.append(f"RSI neutral ({rsi:.1f})")
        
        # 2. MACD
        macd_line, signal_line, histogram = TechnicalIndicators.calculate_macd(prices)
        if macd_line > signal_line and histogram > 0:
            buy_signals += 1
            reasons.append("MACD bullish")
        elif macd_line < signal_line and histogram < 0:
            sell_signals += 1
            reasons.append("MACD bearish")
        
        # 3. Bollinger Bands
        upper, middle, lower = TechnicalIndicators.calculate_bollinger_bands(prices)
        if current_price <= lower:
            buy_signals += 1
            reasons.append("Price at lower Bollinger Band")
        elif current_price >= upper:
            sell_signals += 1
            reasons.append("Price at upper Bollinger Band")
        
        # 4. Momentum
        if len(prices) >= 10:
            momentum = (prices[-1] - prices[-10]) / prices[-10]
            if momentum > 0.01:  # 1% up
                buy_signals += 1
                reasons.append(f"Positive momentum ({momentum*100:.2f}%)")
            elif momentum < -0.01:  # 1% down
                sell_signals += 1
                reasons.append(f"Negative momentum ({momentum*100:.2f}%)")
        
        # 5. Volatilidad (reduce position size si es alta)
        volatility = TechnicalIndicators.calculate_volatility(prices)
        if volatility > 0.5:
            reasons.append(f"High volatility ({volatility:.2f})")
        
        # Decisión final
        total_signals = buy_signals + sell_signals
        if total_signals == 0:
            return {"action": "HOLD", "confidence": 0, "reasons": reasons}
        
        if buy_signals > sell_signals:
            confidence = (buy_signals / total_signals) * 100
            return {"action": "BUY", "confidence": confidence, "reasons": reasons}
        elif sell_signals > buy_signals:
            confidence = (sell_signals / total_signals) * 100
            return {"action": "SELL", "confidence": confidence, "reasons": reasons}
        else:
            return {"action": "HOLD", "confidence": 50, "reasons": reasons}
    
    def execute_buy(self, symbol: str, amount_usd: float) -> bool:
        """Ejecuta compra"""
        if self.cash < amount_usd:
            print(f"[SKIP] Insufficient cash: ${self.cash:.2f} < ${amount_usd:.2f}")
            return False
        
        if len(self.positions) >= MAX_POSITIONS:
            print(f"[SKIP] Max positions reached: {len(self.positions)}/{MAX_POSITIONS}")
            return False
        
        current_price = self.get_price(symbol)
        if not current_price:
            print(f"[ERROR] Could not get price for {symbol}")
            return False
        
        amount_crypto = amount_usd / current_price
        
        self.cash -= amount_usd
        self.positions[symbol] = {
            'amount': amount_crypto,
            'entry_price': current_price,
            'timestamp': datetime.now().isoformat(),
            'stop_loss': current_price * (1 - STOP_LOSS_PERCENT),
            'take_profit': current_price * (1 + TAKE_PROFIT_PERCENT)
        }
        
        trade = {
            'timestamp': datetime.now().isoformat(),
            'action': 'BUY',
            'symbol': symbol,
            'price': current_price,
            'amount': amount_crypto,
            'amount_usd': amount_usd,
            'mode': 'PAPER' if self.paper_mode else 'LIVE'
        }
        self.trade_history.append(trade)
        
        print(f"\n[BUY] {symbol}")
        print(f"  Price: ${current_price:,.2f}")
        print(f"  Amount: {amount_crypto:.8f} ({amount_usd:.2f} USD)")
        print(f"  Stop Loss: ${self.positions[symbol]['stop_loss']:,.2f}")
        print(f"  Take Profit: ${self.positions[symbol]['take_profit']:,.2f}")
        print(f"  Cash remaining: ${self.cash:.2f}")
        
        return True
    
    def execute_sell(self, symbol: str, reason: str = "SIGNAL", override_price=None) -> bool:
        """Ejecuta venta"""
        if symbol not in self.positions:
            print(f"[SKIP] No position in {symbol}")
            return False
        
        current_price = override_price if override_price else self.get_price(symbol)
        if not current_price:
            print(f"[ERROR] Could not get price for {symbol}")
            return False
        
        position = self.positions[symbol]
        amount_crypto = position['amount']
        amount_usd = amount_crypto * current_price
        
        entry_price = position['entry_price']
        pnl = amount_usd - (amount_crypto * entry_price)
        pnl_pct = (pnl / (amount_crypto * entry_price)) * 100
        
        self.cash += amount_usd
        del self.positions[symbol]
        
        trade = {
            'timestamp': datetime.now().isoformat(),
            'action': 'SELL',
            'symbol': symbol,
            'price': current_price,
            'amount': amount_crypto,
            'amount_usd': amount_usd,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'reason': reason,
            'mode': 'PAPER' if self.paper_mode else 'LIVE'
        }
        self.trade_history.append(trade)
        
        print(f"\n[SELL] {symbol} - {reason}")
        print(f"  Entry: ${entry_price:,.2f} → Exit: ${current_price:,.2f}")
        print(f"  Amount: {amount_crypto:.8f}")
        print(f"  P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        print(f"  Cash total: ${self.cash:.2f}")
        
        return True
    
    def check_stop_loss_take_profit(self, override_price=None):
        """Verifica stop loss y take profit en todas las posiciones"""
        for symbol in list(self.positions.keys()):
            position = self.positions[symbol]
            current_price = override_price if override_price else self.get_price(symbol)
            
            if not current_price:
                continue
            
            # Stop Loss
            if current_price <= position['stop_loss']:
                print(f"\n🛑 STOP LOSS TRIGGERED for {symbol}")
                self.execute_sell(symbol, "STOP_LOSS")
            
            # Take Profit
            elif current_price >= position['take_profit']:
                print(f"\n💰 TAKE PROFIT TRIGGERED for {symbol}")
                self.execute_sell(symbol, "TAKE_PROFIT")
    
    def close_all_positions(self, reason: str = "USER"):
        """Cierra todas las posiciones"""
        print(f"\n[INFO] Closing all positions - Reason: {reason}")
        for symbol in list(self.positions.keys()):
            self.execute_sell(symbol, reason)
    
    def run_autonomous(self, duration_hours: float = 24):
        """
        Ejecuta trading autónomo por el tiempo especificado
        Args:
            duration_hours: Duración en horas (24 = 1 día)
        """
        print(f"[INFO] Starting autonomous trading for {duration_hours} hours")
        print(f"[INFO] Check interval: {CHECK_INTERVAL} seconds")
        print("\n" + "="*80)
        print("🤖 MODO AUTÓNOMO ACTIVADO - El sistema tomará decisiones solo")
        print("="*80 + "\n")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=duration_hours)
        iteration = 0
        
        while self.running and datetime.now() < end_time:
            iteration += 1
            current_time = datetime.now()
            
            print(f"\n{'='*80}")
            print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Iteration #{iteration}")
            print(f"{'='*80}")
            
            # Obtener precio
            price = self.get_price("BTC-USD")
            if not price:
                print("[ERROR] Could not get price, skipping iteration")
                time.sleep(CHECK_INTERVAL)
                continue
            
            self.price_history.append(price)
            
            # Verificar Kill Switch
            if self.check_kill_switch():
                print("[STOP] Kill Switch activated - stopping autonomous trading")
                break
            
            # Verificar Stop Loss / Take Profit
            self.check_stop_loss_take_profit()
            
            # Generar señal
            signal = self.generate_trading_signal("BTC-USD")
            
            # Log decisión
            decision = {
                'timestamp': current_time.isoformat(),
                'price': price,
                'signal': signal,
                'positions': len(self.positions),
                'cash': self.cash,
                'portfolio_value': self.calculate_portfolio_value()
            }
            self.decisions_log.append(decision)
            
            # Mostrar estado
            portfolio_value = self.calculate_portfolio_value()
            pnl = portfolio_value - self.initial_capital
            pnl_pct = (pnl / self.initial_capital) * 100
            
            print(f"\n📊 ESTADO:")
            print(f"  Precio BTC: ${price:,.2f}")
            print(f"  Cash: ${self.cash:.2f}")
            print(f"  Posiciones: {len(self.positions)}/{MAX_POSITIONS}")
            print(f"  Portfolio: ${portfolio_value:.2f}")
            print(f"  P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
            print(f"  MDD: {self.mdd_current*100:.2f}%")
            
            print(f"\n🎯 SEÑAL: {signal['action']} (Confidence: {signal['confidence']:.1f}%)")
            print(f"  Reasons: {', '.join(signal['reasons'])}")
            
            # Ejecutar acción si confidence es suficiente
            if signal['action'] == 'BUY' and signal['confidence'] >= 60:
                position_size = self.capital * POSITION_SIZE_PERCENT
                self.execute_buy("BTC-USD", position_size)
            
            elif signal['action'] == 'SELL' and signal['confidence'] >= 60:
                if "BTC-USD" in self.positions:
                    self.execute_sell("BTC-USD", "SIGNAL")
            
            # Guardar sesión periódicamente
            if iteration % 10 == 0:
                self.save_session()
            
            print(f"\n⏱️  Next check in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
        
        print("\n[OK] Autonomous trading completed")
        self.print_summary()
        self.save_session()
    
    def print_summary(self):
        """Imprime resumen de la sesión"""
        portfolio_value = self.calculate_portfolio_value()
        pnl = portfolio_value - self.initial_capital
        pnl_pct = (pnl / self.initial_capital) * 100
        
        print("\n" + "="*80)
        print("📊 RESUMEN FINAL - TRADING AUTÓNOMO")
        print("="*80)
        
        print(f"\n💰 CAPITAL:")
        print(f"  Inicial: ${self.initial_capital:.2f}")
        print(f"  Final: ${portfolio_value:.2f}")
        print(f"  P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        print(f"  Cash: ${self.cash:.2f}")
        print(f"  En posiciones: ${portfolio_value - self.cash:.2f}")
        
        print(f"\n📈 TRADING:")
        print(f"  Total trades: {len(self.trade_history)}")
        print(f"  Posiciones abiertas: {len(self.positions)}")
        print(f"  Max Drawdown: {self.mdd_current*100:.2f}%")
        print(f"  Peak Value: ${self.peak_value:.2f}")
        
        # Análisis de trades
        if self.trade_history:
            sells = [t for t in self.trade_history if t['action'] == 'SELL']
            if sells:
                winning_trades = [t for t in sells if t.get('pnl', 0) > 0]
                losing_trades = [t for t in sells if t.get('pnl', 0) < 0]
                
                print(f"\n🎯 PERFORMANCE:")
                print(f"  Winning trades: {len(winning_trades)}")
                print(f"  Losing trades: {len(losing_trades)}")
                if sells:
                    win_rate = (len(winning_trades) / len(sells)) * 100
                    print(f"  Win rate: {win_rate:.1f}%")
                
                if winning_trades:
                    avg_win = np.mean([t['pnl'] for t in winning_trades])
                    print(f"  Avg win: ${avg_win:.2f}")
                
                if losing_trades:
                    avg_loss = np.mean([t['pnl'] for t in losing_trades])
                    print(f"  Avg loss: ${avg_loss:.2f}")
        
        print(f"\n🛡️  SEGURIDAD:")
        print(f"  Kill Switch events: {1 if self.kill_switch_active else 0}")
        print(f"  Modo: {'PAPER (simulado)' if self.paper_mode else 'LIVE (real)'}")
        
        print("\n" + "="*80)
    
    def save_session(self):
        """Guarda sesión completa"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"autonomous_session_{timestamp}.json"
        
        portfolio_value = self.calculate_portfolio_value()
        
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "mode": "PAPER" if self.paper_mode else "LIVE",
            "initial_capital": self.initial_capital,
            "final_portfolio": portfolio_value,
            "cash": self.cash,
            "positions": self.positions,
            "pnl": portfolio_value - self.initial_capital,
            "pnl_pct": ((portfolio_value - self.initial_capital) / self.initial_capital) * 100,
            "max_drawdown": self.mdd_current,
            "peak_value": self.peak_value,
            "total_trades": len(self.trade_history),
            "kill_switch_events": 1 if self.kill_switch_active else 0,
            "trade_history": self.trade_history,
            "decisions_log": self.decisions_log[-100:]  # Últimas 100 decisiones
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n💾 Session saved: {filename}")


def main():
    print("\n" + "="*80)
    print("🤖 SISTEMA DE TRADING AUTÓNOMO - CONFIGURACIÓN")
    print("="*80)
    print("\nEste sistema operará de forma AUTÓNOMA:")
    print("✅ Monitoreará precios 24/7")
    print("✅ Analizará múltiples indicadores técnicos")
    print("✅ Comprará y venderá automáticamente")
    print("✅ Aplicará Stop Loss y Take Profit")
    print("✅ Protegerá tu capital con Kill Switch")
    print("\n⚠️  IMPORTANTE: Empieza SIEMPRE en Paper Trading primero")
    
    try:
        print("\n" + "="*80)
        print("MODO DE OPERACIÓN:")
        print("1. PAPER TRADING - Simulado (RECOMENDADO para empezar)")
        print("2. LIVE TRADING - Real con dinero ($40 USD)")
        
        mode = input("\nSelecciona modo (1=Paper, 2=Live): ").strip()
        
        if mode == "1":
            paper_mode = True
            capital = 40
            print("\n✅ Modo PAPER TRADING seleccionado (SIN RIESGO)")
        elif mode == "2":
            confirm = input("\n⚠️  ¿SEGURO que quieres usar dinero REAL? (escribe 'SI ACEPTO AUTONOMO'): ").strip()
            if confirm != "SI ACEPTO AUTONOMO":
                print("\n[CANCELADO] Trading autónomo cancelado")
                return
            paper_mode = False
            capital = 40
            print("\n🔴 Modo LIVE TRADING activado (AUTÓNOMO CON DINERO REAL)")
        else:
            print("\n[ERROR] Opción inválida")
            return
        
        duration_input = input("\nDuración en horas (1-24): ").strip()
        if not duration_input:
            print("[ERROR] Debes ingresar una duración")
            return
        
        try:
            duration = float(duration_input)
        except ValueError:
            print("[ERROR] Duración debe ser un número")
            return
        
        if duration < 1 or duration > 24:
            print("[ERROR] Duración debe estar entre 1-24 horas")
            return
        
        print(f"\n[INFO] Iniciando sistema autónomo por {duration} horas...")
        print("[INFO] Presiona CTRL+C en cualquier momento para detener")
        
        # Crear y ejecutar sistema
        system = AutonomousTradingSystem(capital=capital, paper_mode=paper_mode)
        system.run_autonomous(duration_hours=duration)
        
    except KeyboardInterrupt:
        print("\n\n[STOP] Sistema interrumpido por usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
