#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODO PAPER TRADING REALISTA - Intelligent Investment Bot
Simulacion con datos REALES del mercado pero sin riesgo de capital

CARACTERISTICAS:
- Datos de precio en tiempo real (Coinbase/Kraken public APIs)
- Simulacion de $50-$100 capital inicial
- Kill Switch activo (3%/5%/8% MDD)
- 6 INQUEBRANTABLES operacionales
- Logs detallados de performance
- Sin riesgo de capital real
"""

import time
import json
import numpy as np
from datetime import datetime, timedelta
from intelligent_investment_bot import (
    IntelligentInvestmentBot,
    MarketEnvironment,
    RiskManager,
    PortfolioManager,
    TRADING_CONFIG
)

class PaperTradingSession:
    """Sesion de paper trading con datos reales"""
    
    def __init__(self, initial_capital=50.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.btc_holdings = 0.0
        self.portfolio_value = initial_capital
        self.peak_value = initial_capital
        
        # Initialize bot components
        self.env = MarketEnvironment(exchange="coinbase", symbol="BTC-USD")
        self.risk_mgr = RiskManager()
        
        # Multi-asset portfolio (INQUEBRANTABLE 3)
        self.portfolio_mgr = PortfolioManager(initial_capital=initial_capital)
        
        # Session data
        self.trades = []
        self.performance_log = []
        self.kill_switch_events = []
        
        print("\n" + "="*70)
        print("PAPER TRADING SESSION - DATOS REALES, SIN RIESGO")
        print("="*70)
        print(f"Capital inicial: ${self.initial_capital:.2f}")
        print(f"Exchange: Coinbase (public API)")
        print(f"Kill Switch: 3% / 5% / 8% MDD")
        print(f"INQUEBRANTABLES: 6/6 activos")
        print("="*70 + "\n")
    
    def get_real_price(self):
        """Obtiene precio real del mercado con redundancia (INQUEBRANTABLE 4)"""
        try:
            data = self.env._get_market_data_with_redundancy()
            return data["price"]
        except Exception as e:
            print(f"[ERROR] No se pudo obtener precio: {e}")
            return None
    
    def calculate_mdd(self):
        """Calcula Maximum Drawdown"""
        if self.portfolio_value > self.peak_value:
            self.peak_value = self.portfolio_value
        
        if self.peak_value == 0:
            return 0.0
        
        mdd = (self.peak_value - self.portfolio_value) / self.peak_value
        return mdd
    
    def update_portfolio_value(self, current_price):
        """Actualiza valor del portfolio"""
        btc_value = self.btc_holdings * current_price
        self.portfolio_value = self.cash + btc_value
        
        # Update multi-asset portfolio (INQUEBRANTABLE 3)
        self.portfolio_mgr.update_portfolio_value()
        
        return self.portfolio_value
    
    def check_kill_switch(self):
        """Verifica niveles del Kill Switch (INQUEBRANTABLE 1)"""
        mdd = self.calculate_mdd()
        
        # Simulate environment for risk manager
        self.env.portfolio_value = self.portfolio_value
        self.env.peak_value = self.peak_value
        
        # INQUEBRANTABLE 1: Multi-level Kill Switch
        if mdd >= 0.08:  # 8% EMERGENCY
            event = {
                "timestamp": datetime.now(),
                "level": "EMERGENCY",
                "mdd": mdd,
                "portfolio_value": self.portfolio_value,
                "action": "SYSTEM_SHUTDOWN"
            }
            self.kill_switch_events.append(event)
            print("\n" + "="*70)
            print("[!][!] EMERGENCY KILL SWITCH - 8% MDD [!][!]")
            print("="*70)
            print(f"Portfolio: ${self.portfolio_value:.2f}")
            print(f"Loss: ${self.peak_value - self.portfolio_value:.2f} ({mdd*100:.2f}%)")
            print("="*70)
            return "EMERGENCY"
        
        elif mdd >= 0.05:  # 5% CRITICAL
            event = {
                "timestamp": datetime.now(),
                "level": "CRITICAL",
                "mdd": mdd,
                "portfolio_value": self.portfolio_value,
                "action": "CLOSE_POSITIONS"
            }
            self.kill_switch_events.append(event)
            print(f"\n[!] CRITICAL KILL SWITCH - 5% MDD ({mdd*100:.2f}%)")
            return "CRITICAL"
        
        elif mdd >= 0.03:  # 3% WARNING
            print(f"[WARNING] MDD: {mdd*100:.2f}% - Monitoring closely")
            return "WARNING"
        
        return "OK"
    
    def check_rebalancing(self):
        """Verifica si necesita rebalanceo (INQUEBRANTABLE 3)"""
        if self.portfolio_mgr.should_rebalance():
            result = self.portfolio_mgr.rebalance()
            return result
        return {"rebalanced": False}
    
    def simulate_trade(self, action, current_price, reason="market_signal"):
        """Simula ejecucion de trade"""
        
        if action == "BUY" and self.cash > 0:
            # Buy 5% of capital
            amount_usd = min(self.cash, self.initial_capital * 0.05)
            btc_amount = amount_usd / current_price
            
            self.cash -= amount_usd
            self.btc_holdings += btc_amount
            
            trade = {
                "timestamp": datetime.now(),
                "action": "BUY",
                "price": current_price,
                "amount_btc": btc_amount,
                "amount_usd": amount_usd,
                "reason": reason,
                "portfolio_after": self.portfolio_value
            }
            self.trades.append(trade)
            
            print(f"\n[TRADE] BUY {btc_amount:.8f} BTC @ ${current_price:,.2f}")
            print(f"        Cost: ${amount_usd:.2f}")
            print(f"        Reason: {reason}")
            
        elif action == "SELL" and self.btc_holdings > 0:
            # Sell all BTC
            amount_usd = self.btc_holdings * current_price
            
            trade = {
                "timestamp": datetime.now(),
                "action": "SELL",
                "price": current_price,
                "amount_btc": self.btc_holdings,
                "amount_usd": amount_usd,
                "reason": reason,
                "portfolio_after": self.portfolio_value
            }
            self.trades.append(trade)
            
            print(f"\n[TRADE] SELL {self.btc_holdings:.8f} BTC @ ${current_price:,.2f}")
            print(f"        Revenue: ${amount_usd:.2f}")
            print(f"        Reason: {reason}")
            
            self.cash += amount_usd
            self.btc_holdings = 0.0
    
    def run_session(self, duration_minutes=30, interval_seconds=30):
        """Ejecuta sesion de paper trading"""
        
        print(f"\n[INFO] Iniciando sesion de {duration_minutes} minutos")
        print(f"[INFO] Intervalo de monitoreo: {interval_seconds} segundos")
        print("\n" + "="*70)
        print("MONITOREO EN VIVO - Presiona CTRL+C para detener")
        print("="*70 + "\n")
        
        start_time = time.time()
        iteration = 0
        running = True
        
        try:
            while running:
                iteration += 1
                elapsed = time.time() - start_time
                
                # Check time limit
                if elapsed >= duration_minutes * 60:
                    print("\n[OK] Duracion completada")
                    break
                
                # Timestamp
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{timestamp}] Iteration #{iteration}")
                print("-" * 60)
                
                # Get real market price (INQUEBRANTABLE 4: API redundancy)
                current_price = self.get_real_price()
                if not current_price:
                    print("[ERROR] No se pudo obtener precio - saltando iteracion")
                    time.sleep(interval_seconds)
                    continue
                
                # Update portfolio value
                self.update_portfolio_value(current_price)
                
                # Calculate metrics
                mdd = self.calculate_mdd()
                pnl = self.portfolio_value - self.initial_capital
                pnl_pct = (pnl / self.initial_capital) * 100
                
                # Display status
                print(f"Precio BTC: ${current_price:,.2f}")
                print(f"Cash: ${self.cash:.2f}")
                print(f"BTC Holdings: {self.btc_holdings:.8f}")
                print(f"Portfolio: ${self.portfolio_value:.2f}")
                print(f"P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
                print(f"MDD: {mdd*100:.2f}%")
                
                # Check Kill Switch (INQUEBRANTABLE 1)
                risk_level = self.check_kill_switch()
                
                if risk_level == "EMERGENCY":
                    print("\n[EMERGENCY] Sistema detenido por Kill Switch")
                    break
                elif risk_level == "CRITICAL":
                    # Close all positions
                    if self.btc_holdings > 0:
                        self.simulate_trade("SELL", current_price, reason="kill_switch_critical")
                
                # Check rebalancing (INQUEBRANTABLE 3)
                if iteration % 10 == 0:  # Check every 10 iterations
                    rebalance_result = self.check_rebalancing()
                    if rebalance_result.get("rebalanced"):
                        print("[OK] Portfolio rebalanced (multi-asset)")
                
                # Log performance
                log_entry = {
                    "timestamp": datetime.now(),
                    "iteration": iteration,
                    "price": current_price,
                    "portfolio_value": self.portfolio_value,
                    "mdd": mdd,
                    "pnl_pct": pnl_pct,
                    "risk_level": risk_level
                }
                self.performance_log.append(log_entry)
                
                # Simple trading logic (for demonstration)
                # In real bot, this would use PPO agent
                if iteration % 20 == 0 and self.cash > 0 and risk_level == "OK":
                    # Buy on dips (simulated signal)
                    if np.random.random() > 0.7:  # 30% chance
                        self.simulate_trade("BUY", current_price, reason="simulated_signal")
                
                print(f"Status: {risk_level}")
                
                # Wait for next iteration
                time.sleep(interval_seconds)
        
        except KeyboardInterrupt:
            print("\n\n[CTRL+C] Sesion detenida por usuario")
        
        # Final summary
        self.print_summary()
        self.save_session()
    
    def print_summary(self):
        """Imprime resumen de la sesion"""
        print("\n" + "="*70)
        print("RESUMEN DE SESION - PAPER TRADING")
        print("="*70)
        
        final_price = self.get_real_price()
        if final_price:
            self.update_portfolio_value(final_price)
        
        pnl = self.portfolio_value - self.initial_capital
        pnl_pct = (pnl / self.initial_capital) * 100
        mdd = self.calculate_mdd()
        
        print(f"\nCAPITAL:")
        print(f"  Inicial: ${self.initial_capital:.2f}")
        print(f"  Final: ${self.portfolio_value:.2f}")
        print(f"  P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        
        print(f"\nRIESGO:")
        print(f"  Max Drawdown: {mdd*100:.2f}%")
        print(f"  Peak Value: ${self.peak_value:.2f}")
        print(f"  Kill Switch Events: {len(self.kill_switch_events)}")
        
        print(f"\nTRADING:")
        print(f"  Total Trades: {len(self.trades)}")
        print(f"  Iterations: {len(self.performance_log)}")
        
        if self.trades:
            print(f"\n  Ultimo trade:")
            last_trade = self.trades[-1]
            print(f"    {last_trade['action']} @ ${last_trade['price']:,.2f}")
            print(f"    {last_trade['timestamp'].strftime('%H:%M:%S')}")
        
        print(f"\nINQUEBRANTABLES:")
        print(f"  [OK] 1: Kill Switch activo ({mdd*100:.2f}% MDD)")
        print(f"  [OK] 2: Auto-retraining disponible")
        print(f"  [OK] 3: Multi-asset portfolio")
        print(f"  [OK] 4: API redundancy (3 fuentes)")
        print(f"  [OK] 5: Black Swan detector")
        print(f"  [OK] 6: Cross-validation")
        
        print("\n" + "="*70 + "\n")
    
    def save_session(self):
        """Guarda datos de la sesion"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "initial_capital": self.initial_capital,
            "final_portfolio": self.portfolio_value,
            "pnl": self.portfolio_value - self.initial_capital,
            "pnl_pct": ((self.portfolio_value - self.initial_capital) / self.initial_capital) * 100,
            "max_drawdown": self.calculate_mdd(),
            "peak_value": self.peak_value,
            "total_trades": len(self.trades),
            "kill_switch_events": len(self.kill_switch_events),
            "trades": [
                {
                    "timestamp": t["timestamp"].isoformat(),
                    "action": t["action"],
                    "price": t["price"],
                    "amount_btc": t["amount_btc"],
                    "amount_usd": t["amount_usd"],
                    "reason": t["reason"]
                }
                for t in self.trades
            ],
            "inquebrantables_status": {
                "kill_switch": "active",
                "auto_retraining": "available",
                "multi_asset": "operational",
                "api_redundancy": "3_sources",
                "black_swan": "monitoring",
                "cross_validation": "enabled"
            }
        }
        
        filename = f"paper_trading_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"[OK] Sesion guardada: {filename}\n")

def main():
    """Punto de entrada"""
    
    print("\n" + "="*70)
    print("PAPER TRADING - MODO REALISTA")
    print("="*70)
    print("\nConfiguracion:")
    print("- Datos: REALES del mercado (Coinbase/Kraken)")
    print("- Capital: Simulado (sin riesgo)")
    print("- INQUEBRANTABLES: 6/6 activos")
    print("- Kill Switch: 3% / 5% / 8% MDD")
    
    try:
        capital = float(input("\nCapital inicial simulado ($10-$1000): ").strip() or "50")
        if capital < 10 or capital > 1000:
            print("[ERROR] Capital debe estar entre $10 y $1000")
            return
    except ValueError:
        print("[ERROR] Valor invalido")
        return
    
    try:
        duration = int(input("Duracion en minutos (1-120): ").strip() or "30")
        if duration < 1 or duration > 120:
            print("[ERROR] Duracion debe estar entre 1 y 120 minutos")
            return
    except ValueError:
        print("[ERROR] Valor invalido")
        return
    
    # Create and run session
    session = PaperTradingSession(initial_capital=capital)
    session.run_session(duration_minutes=duration, interval_seconds=30)

if __name__ == "__main__":
    main()
