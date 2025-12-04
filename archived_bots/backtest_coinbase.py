#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 BACKTESTING ENGINE - Intelligent Investment Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backtesting con datos históricos de Coinbase para validar estrategia
ANTES de arriesgar capital real.

OBJETIVO: Demostrar que la estrategia es rentable con datos del pasado
"""

import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage"

def fetch_historical_data(symbol: str = "BTC-USD", days: int = 30) -> pd.DataFrame:
    """Obtiene datos históricos de Coinbase"""
    
    print(f"📊 Obteniendo {days} días de datos históricos de {symbol}...")
    
    # Coinbase limit: max 300 candles per request
    # Para 30 días necesitamos múltiples requests
    all_candles = []
    
    # Dividir en chunks de 5 días (120 candles por chunk)
    chunks = days // 5
    
    for chunk in range(chunks):
        end_time = datetime.now() - timedelta(days=chunk * 5)
        start_time = end_time - timedelta(days=5)
        
        url = f"{COINBASE_API_URL}/market/products/{symbol}/candles"
        params = {
            "granularity": "ONE_HOUR",
            "start": int(start_time.timestamp()),
            "end": int(end_time.timestamp())
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "candles" in data and data["candles"]:
                all_candles.extend(data["candles"])
                print(f"   ✅ Chunk {chunk+1}/{chunks}: {len(data['candles'])} candles")
            
        except Exception as e:
            print(f"   ⚠️  Error en chunk {chunk+1}: {e}")
            continue
    
    if not all_candles:
        print(f"❌ No se encontraron candles")
        return pd.DataFrame()
    
    # Parse candles
    df = pd.DataFrame(all_candles)
    
    # Convert columns
    df['timestamp'] = pd.to_datetime(df['start'], unit='s')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    
    # Sort by timestamp and remove duplicates
    df = df.sort_values('timestamp').drop_duplicates(subset=['timestamp']).reset_index(drop=True)
    
    print(f"✅ {len(df)} candles obtenidas ({df['timestamp'].min()} → {df['timestamp'].max()})")
    
    return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores técnicos (RSI, MACD, SMA)"""
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    # SMA
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    return df


def backtest_strategy(df: pd.DataFrame, initial_capital: float = 1000.0) -> dict:
    """Ejecuta backtest de estrategia simple"""
    
    print(f"\n🔍 Ejecutando backtest con ${initial_capital:,.2f}...")
    
    # Configuración
    position_size_percent = 0.08  # 8% del capital por trade
    fee_percent = 0.006  # 0.6% fee
    
    # Estado
    cash = initial_capital
    position = 0.0  # BTC holding
    trades = []
    portfolio_values = []
    
    for i in range(len(df)):
        row = df.iloc[i]
        price = row['close']
        rsi = row['rsi']
        macd = row['macd']
        macd_signal = row['macd_signal']
        
        # Calculate portfolio value
        portfolio_value = cash + (position * price)
        portfolio_values.append(portfolio_value)
        
        # Skip if insufficient data
        if pd.isna(rsi) or pd.isna(macd):
            continue
        
        # Simple strategy: RSI + MACD
        # BUY: RSI < 30 (oversold) AND MACD > Signal
        # SELL: RSI > 70 (overbought) OR MACD < Signal
        
        if position == 0 and rsi < 35 and macd > macd_signal:
            # BUY
            trade_amount = cash * position_size_percent
            btc_to_buy = trade_amount / price
            fee = trade_amount * fee_percent
            
            if cash >= trade_amount + fee:
                position = btc_to_buy
                cash -= (trade_amount + fee)
                
                trades.append({
                    'timestamp': row['timestamp'],
                    'action': 'BUY',
                    'price': price,
                    'amount': btc_to_buy,
                    'fee': fee,
                    'portfolio_value': portfolio_value
                })
        
        elif position > 0 and (rsi > 65 or macd < macd_signal):
            # SELL
            proceeds = position * price
            fee = proceeds * fee_percent
            
            cash += (proceeds - fee)
            
            trades.append({
                'timestamp': row['timestamp'],
                'action': 'SELL',
                'price': price,
                'amount': position,
                'fee': fee,
                'portfolio_value': portfolio_value
            })
            
            position = 0.0
    
    # Final portfolio value
    final_value = cash + (position * df.iloc[-1]['close'])
    
    # Calculate metrics
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    num_trades = len(trades)
    total_fees = sum([t['fee'] for t in trades])
    
    # Win rate
    winning_trades = 0
    for i in range(1, len(trades)):
        if trades[i]['action'] == 'SELL':
            buy_price = trades[i-1]['price']
            sell_price = trades[i]['price']
            if sell_price > buy_price:
                winning_trades += 1
    
    win_rate = (winning_trades / (num_trades // 2)) * 100 if num_trades > 0 else 0
    
    # Max drawdown
    portfolio_array = np.array(portfolio_values)
    cumulative_max = np.maximum.accumulate(portfolio_array)
    drawdowns = (portfolio_array - cumulative_max) / cumulative_max
    max_drawdown = abs(drawdowns.min()) * 100 if len(drawdowns) > 0 else 0
    
    # Sharpe Ratio (simplified)
    returns = np.diff(portfolio_array) / portfolio_array[:-1]
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if len(returns) > 0 and returns.std() > 0 else 0
    
    return {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'num_trades': num_trades,
        'total_fees': total_fees,
        'win_rate': win_rate,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe,
        'trades': trades
    }


def print_backtest_results(results: dict):
    """Imprime resultados del backtest"""
    
    print("\n" + "="*70)
    print("📈 BACKTEST RESULTS - INTELLIGENT INVESTMENT BOT")
    print("="*70)
    print(f"💰 Initial Capital:  ${results['initial_capital']:,.2f}")
    print(f"💵 Final Value:      ${results['final_value']:,.2f}")
    print(f"📊 Total Return:     {results['total_return']:+.2f}%")
    print(f"📉 Max Drawdown:     {results['max_drawdown']:.2f}%")
    print(f"⚡ Sharpe Ratio:     {results['sharpe_ratio']:.2f}")
    print(f"🎯 Win Rate:         {results['win_rate']:.1f}%")
    print(f"📝 Total Trades:     {results['num_trades']}")
    print(f"💸 Total Fees:       ${results['total_fees']:.2f}")
    print("="*70)
    
    # Recommendation
    if results['total_return'] > 10 and results['sharpe_ratio'] > 1.0:
        print("✅ RECOMMENDATION: Strategy is PROFITABLE - Good for live trading!")
    elif results['total_return'] > 0 and results['sharpe_ratio'] > 0.5:
        print("⚠️  RECOMMENDATION: Strategy is MARGINALLY profitable - Use with caution")
    else:
        print("❌ RECOMMENDATION: Strategy is NOT profitable - DO NOT use live!")
    
    print("\n💡 To improve:")
    if results['max_drawdown'] > 10:
        print("   - Reduce position size (currently 8%)")
    if results['win_rate'] < 50:
        print("   - Adjust RSI thresholds (currently 35/65)")
    if results['sharpe_ratio'] < 1.0:
        print("   - Train PPO agent longer (50+ episodes)")


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║         📊 BACKTESTING ENGINE - II Bot v1.0                          ║
║                                                                       ║
║  Testing strategy with 30 days of REAL Coinbase data                ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Fetch historical data
    df = fetch_historical_data(symbol="BTC-USD", days=30)
    
    if df.empty:
        print("❌ No se pudieron obtener datos históricos")
        exit(1)
    
    # Calculate indicators
    df = calculate_technical_indicators(df)
    
    # Run backtest
    results = backtest_strategy(df, initial_capital=1000.0)
    
    # Print results
    print_backtest_results(results)
    
    # Save trades to CSV
    trades_df = pd.DataFrame(results['trades'])
    if not trades_df.empty:
        trades_df.to_csv('trading_data/backtest_trades.csv', index=False)
        print(f"\n💾 Trades saved to: trading_data/backtest_trades.csv")
