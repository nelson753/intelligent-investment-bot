#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALIZADOR DE HISTORIAL - Sistema Multi-Crypto
Lee todos los JSONs de sesiones pasadas y genera estadísticas
"""

import json
import os
from datetime import datetime
from typing import List, Dict
import glob

class TradingHistoryAnalyzer:
    """Analiza el historial completo de trading"""
    
    def __init__(self):
        self.sessions = []
        self.all_trades = []
        
    def load_all_sessions(self):
        """Carga todos los archivos de sesión"""
        session_files = glob.glob("multi_crypto_session_*.json")
        
        print(f"\n📁 Found {len(session_files)} session files\n")
        
        for file in sorted(session_files):
            try:
                with open(file, 'r') as f:
                    session = json.load(f)
                    session['filename'] = file
                    self.sessions.append(session)
                    
                    # Agregar trades a la lista global
                    if 'trades' in session:
                        for trade in session['trades']:
                            trade['session'] = file
                            self.all_trades.append(trade)
                            
                print(f"✅ Loaded: {file}")
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
        
        print(f"\n📊 Total sessions loaded: {len(self.sessions)}")
        print(f"📊 Total trades found: {len(self.all_trades)}")
    
    def analyze_performance(self):
        """Analiza performance general"""
        if not self.sessions:
            print("No sessions to analyze")
            return
        
        print("\n" + "="*80)
        print("📊 OVERALL PERFORMANCE ANALYSIS")
        print("="*80)
        
        # Estadísticas generales
        total_initial = sum(s.get('initial_capital', 0) for s in self.sessions)
        total_final = sum(s.get('portfolio_value', 0) for s in self.sessions)
        total_pnl = total_final - total_initial
        total_pnl_pct = (total_pnl / total_initial * 100) if total_initial > 0 else 0
        
        print(f"\n💼 CAPITAL:")
        print(f"  Initial Capital (all sessions): ${total_initial:.2f}")
        print(f"  Final Value (all sessions): ${total_final:.2f}")
        print(f"  Total P&L: ${total_pnl:+.2f} ({total_pnl_pct:+.2f}%)")
        
        # Análisis por sesión
        print(f"\n📅 SESSIONS BREAKDOWN:")
        for i, session in enumerate(self.sessions, 1):
            timestamp = session.get('timestamp', 'Unknown')
            initial = session.get('initial_capital', 0)
            final = session.get('portfolio_value', 0)
            pnl = final - initial
            pnl_pct = (pnl / initial * 100) if initial > 0 else 0
            iterations = session.get('iteration', 0)
            
            emoji = "💰" if pnl > 0 else "📉" if pnl < 0 else "⚪"
            
            print(f"\n  {emoji} Session {i}: {timestamp[:19]}")
            print(f"     Duration: {iterations} iterations")
            print(f"     P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
    
    def analyze_trades(self):
        """Analiza todos los trades ejecutados"""
        if not self.all_trades:
            print("\nNo trades to analyze")
            return
        
        print("\n" + "="*80)
        print("📈 TRADES ANALYSIS")
        print("="*80)
        
        # Separar por tipo
        buys = [t for t in self.all_trades if t['action'] == 'BUY']
        sells = [t for t in self.all_trades if t['action'] == 'SELL']
        
        print(f"\n📊 TRADE COUNTS:")
        print(f"  Total Trades: {len(self.all_trades)}")
        print(f"  Buys: {len(buys)}")
        print(f"  Sells: {len(sells)}")
        print(f"  Open Positions: {len(buys) - len(sells)}")
        
        # Análisis de trades cerrados (con profit)
        closed_trades = [t for t in sells if 'profit' in t]
        
        if closed_trades:
            winning = [t for t in closed_trades if t['profit'] > 0]
            losing = [t for t in closed_trades if t['profit'] < 0]
            
            total_profit = sum(t['profit'] for t in closed_trades)
            avg_profit = total_profit / len(closed_trades)
            
            win_rate = (len(winning) / len(closed_trades) * 100) if closed_trades else 0
            
            print(f"\n💰 CLOSED TRADES PERFORMANCE:")
            print(f"  Total Closed: {len(closed_trades)}")
            print(f"  Winners: {len(winning)} ({win_rate:.1f}%)")
            print(f"  Losers: {len(losing)}")
            print(f"  Total Profit: ${total_profit:+.4f}")
            print(f"  Avg Profit per Trade: ${avg_profit:+.4f}")
            
            if winning:
                avg_win = sum(t['profit'] for t in winning) / len(winning)
                avg_win_pct = sum(t['profit_pct'] for t in winning) / len(winning)
                print(f"  Avg Win: ${avg_win:.4f} ({avg_win_pct:+.2f}%)")
            
            if losing:
                avg_loss = sum(t['profit'] for t in losing) / len(losing)
                avg_loss_pct = sum(t['profit_pct'] for t in losing) / len(losing)
                print(f"  Avg Loss: ${avg_loss:.4f} ({avg_loss_pct:+.2f}%)")
    
    def analyze_by_crypto(self):
        """Analiza performance por cryptocurrency"""
        if not self.all_trades:
            return
        
        print("\n" + "="*80)
        print("💎 PERFORMANCE BY CRYPTOCURRENCY")
        print("="*80)
        
        # Agrupar por crypto
        crypto_trades = {}
        for trade in self.all_trades:
            pair = trade['pair']
            if pair not in crypto_trades:
                crypto_trades[pair] = {'buys': [], 'sells': []}
            
            if trade['action'] == 'BUY':
                crypto_trades[pair]['buys'].append(trade)
            else:
                crypto_trades[pair]['sells'].append(trade)
        
        # Analizar cada crypto
        for pair, trades in sorted(crypto_trades.items()):
            buys = trades['buys']
            sells = trades['sells']
            
            # Calcular profit solo de trades cerrados
            closed_sells = [t for t in sells if 'profit' in t]
            total_profit = sum(t.get('profit', 0) for t in closed_sells)
            
            emoji = "💰" if total_profit > 0 else "📉" if total_profit < 0 else "⚪"
            
            print(f"\n  {emoji} {pair}:")
            print(f"     Buys: {len(buys)} | Sells: {len(sells)}")
            print(f"     Open: {len(buys) - len(sells)}")
            
            if closed_sells:
                winning = len([t for t in closed_sells if t['profit'] > 0])
                print(f"     Closed Profit: ${total_profit:+.4f}")
                print(f"     Win Rate: {winning}/{len(closed_sells)}")
    
    def show_recent_trades(self, n=10):
        """Muestra los últimos N trades"""
        if not self.all_trades:
            return
        
        print("\n" + "="*80)
        print(f"🕐 LAST {n} TRADES")
        print("="*80)
        
        # Ordenar por timestamp
        sorted_trades = sorted(self.all_trades, 
                              key=lambda x: x.get('time', ''), 
                              reverse=True)[:n]
        
        for i, trade in enumerate(sorted_trades, 1):
            time = trade.get('time', 'Unknown')[:19]
            pair = trade.get('pair', 'Unknown')
            action = trade.get('action', 'Unknown')
            price = trade.get('price', 0)
            value = trade.get('value', 0)
            
            action_emoji = "🟢" if action == "BUY" else "🔴"
            
            print(f"\n  {i}. {action_emoji} {time}")
            print(f"     {pair}: {action} @ ${price:,.2f} (${value:.2f})")
            
            if 'profit' in trade:
                profit = trade['profit']
                profit_pct = trade['profit_pct']
                profit_emoji = "💰" if profit > 0 else "📉"
                print(f"     {profit_emoji} Profit: ${profit:+.4f} ({profit_pct:+.2f}%)")
    
    def get_best_worst_trades(self):
        """Encuentra mejores y peores trades"""
        closed_trades = [t for t in self.all_trades 
                        if t['action'] == 'SELL' and 'profit' in t]
        
        if not closed_trades:
            return
        
        print("\n" + "="*80)
        print("🏆 BEST & WORST TRADES")
        print("="*80)
        
        # Mejor trade
        best = max(closed_trades, key=lambda x: x['profit_pct'])
        print(f"\n💰 BEST TRADE:")
        print(f"  {best['pair']} @ ${best['price']:,.2f}")
        print(f"  Profit: ${best['profit']:+.4f} ({best['profit_pct']:+.2f}%)")
        print(f"  Time: {best['time'][:19]}")
        
        # Peor trade
        worst = min(closed_trades, key=lambda x: x['profit_pct'])
        print(f"\n📉 WORST TRADE:")
        print(f"  {worst['pair']} @ ${worst['price']:,.2f}")
        print(f"  Loss: ${worst['profit']:+.4f} ({worst['profit_pct']:+.2f}%)")
        print(f"  Time: {worst['time'][:19]}")
    
    def generate_recommendations(self):
        """Genera recomendaciones basadas en historial"""
        print("\n" + "="*80)
        print("💡 RECOMMENDATIONS BASED ON HISTORY")
        print("="*80)
        
        if not self.all_trades:
            print("\nNot enough data for recommendations")
            return
        
        # Análisis de win rate
        closed = [t for t in self.all_trades 
                 if t['action'] == 'SELL' and 'profit' in t]
        
        if len(closed) < 5:
            print("\n⚠️  Need at least 5 closed trades for meaningful analysis")
            print(f"   Current: {len(closed)} closed trades")
            print("   Recommendation: Run bot for 5-10 more hours")
            return
        
        win_rate = len([t for t in closed if t['profit'] > 0]) / len(closed) * 100
        avg_profit_pct = sum(t['profit_pct'] for t in closed) / len(closed)
        
        print(f"\n📊 Current Stats:")
        print(f"  Win Rate: {win_rate:.1f}%")
        print(f"  Avg Profit: {avg_profit_pct:+.2f}%")
        
        print(f"\n✅ Recommendations:")
        
        if win_rate >= 60:
            print("  • Excellent win rate! Consider increasing position size")
            print("  • Ready for live trading with small capital")
        elif win_rate >= 50:
            print("  • Good win rate. Continue testing")
            print("  • Need 1-2 more weeks of data before live")
        else:
            print("  • Win rate needs improvement")
            print("  • Review strategy parameters")
            print("  • Analyze losing trades for patterns")
        
        if avg_profit_pct > 0.5:
            print("  • Positive avg profit - strategy is working")
        else:
            print("  • Low avg profit - consider adjusting take profit")
        
        # Mejor crypto
        crypto_profits = {}
        for trade in closed:
            pair = trade['pair']
            if pair not in crypto_profits:
                crypto_profits[pair] = []
            crypto_profits[pair].append(trade['profit'])
        
        if crypto_profits:
            best_crypto = max(crypto_profits.items(), 
                            key=lambda x: sum(x[1]))
            print(f"\n🎯 Best Performing Crypto: {best_crypto[0]}")
            print(f"   Total Profit: ${sum(best_crypto[1]):+.4f}")


def main():
    print("\n" + "="*80)
    print("📊 TRADING HISTORY ANALYZER - Multi-Crypto Bot")
    print("="*80)
    
    analyzer = TradingHistoryAnalyzer()
    analyzer.load_all_sessions()
    
    if not analyzer.sessions:
        print("\n⚠️  No session files found!")
        print("   Run the bot first to generate trading history")
        return
    
    # Ejecutar análisis
    analyzer.analyze_performance()
    analyzer.analyze_trades()
    analyzer.analyze_by_crypto()
    analyzer.show_recent_trades(10)
    analyzer.get_best_worst_trades()
    analyzer.generate_recommendations()
    
    print("\n" + "="*80)
    print("✅ Analysis Complete")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
