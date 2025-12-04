#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DASHBOARD EN TIEMPO REAL - Trading Autónomo
Visualización web de todas las métricas y operaciones
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
import glob

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Página principal del dashboard"""
    html = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Trading Autónomo - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .status {
            display: inline-block;
            padding: 8px 20px;
            background: #10b981;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255,255,255,0.18);
        }
        
        .card h2 {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #a5b4fc;
        }
        
        .metric {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric.positive {
            color: #10b981;
        }
        
        .metric.negative {
            color: #ef4444;
        }
        
        .metric.neutral {
            color: #fbbf24;
        }
        
        .small-text {
            font-size: 0.9em;
            color: #d1d5db;
            margin-top: 5px;
        }
        
        .trade-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .trade-item {
            background: rgba(0,0,0,0.2);
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .trade-item.buy {
            border-left-color: #10b981;
        }
        
        .trade-item.sell {
            border-left-color: #ef4444;
        }
        
        .trade-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        .trade-details {
            font-size: 0.9em;
            color: #d1d5db;
        }
        
        .signals {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .signal-item {
            padding: 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .indicator {
            font-weight: bold;
        }
        
        .value {
            padding: 5px 12px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            font-size: 0.9em;
        }
        
        .refresh-info {
            text-align: center;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            margin-top: 20px;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .live-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #10b981;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 Sistema de Trading Autónomo</h1>
            <div class="status">
                <span class="live-indicator"></span>
                <span id="system-status">ACTIVO</span>
            </div>
        </header>
        
        <div class="grid">
            <div class="card">
                <h2>💰 Portfolio</h2>
                <div class="metric" id="portfolio-value">$0.00</div>
                <div class="small-text">
                    Inicial: <span id="initial-capital">$0.00</span>
                </div>
            </div>
            
            <div class="card">
                <h2>📈 P&L</h2>
                <div class="metric positive" id="pnl">$0.00</div>
                <div class="small-text">
                    <span id="pnl-pct">0.00%</span>
                </div>
            </div>
            
            <div class="card">
                <h2>📊 Max Drawdown</h2>
                <div class="metric neutral" id="mdd">0.00%</div>
                <div class="small-text">
                    Peak: <span id="peak-value">$0.00</span>
                </div>
            </div>
            
            <div class="card">
                <h2>🔄 Trades</h2>
                <div class="metric" id="total-trades">0</div>
                <div class="small-text">
                    Win Rate: <span id="win-rate">0%</span>
                </div>
            </div>
            
            <div class="card">
                <h2>💵 Cash</h2>
                <div class="metric" id="cash">$0.00</div>
                <div class="small-text">
                    Posiciones: <span id="positions">0</span>
                </div>
            </div>
            
            <div class="card">
                <h2>₿ Precio BTC</h2>
                <div class="metric" id="btc-price">$0.00</div>
                <div class="small-text" id="price-change">
                    --
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🎯 Señales Actuales</h2>
                <div class="signals" id="signals">
                    <div class="signal-item">
                        <span class="indicator">RSI</span>
                        <span class="value">--</span>
                    </div>
                    <div class="signal-item">
                        <span class="indicator">MACD</span>
                        <span class="value">--</span>
                    </div>
                    <div class="signal-item">
                        <span class="indicator">Bollinger</span>
                        <span class="value">--</span>
                    </div>
                    <div class="signal-item">
                        <span class="indicator">Momentum</span>
                        <span class="value">--</span>
                    </div>
                </div>
            </div>
            
            <div class="card" style="grid-column: span 2;">
                <h2>📝 Últimos Trades</h2>
                <div class="trade-list" id="trade-list">
                    <p style="text-align: center; color: #9ca3af;">
                        No hay trades aún...
                    </p>
                </div>
            </div>
        </div>
        
        <div class="refresh-info">
            ⚡ Actualización automática cada 5 segundos<br>
            <small>Última actualización: <span id="last-update">--</span></small>
        </div>
    </div>
    
    <script>
        async function fetchData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        
        function updateDashboard(data) {
            // Portfolio
            document.getElementById('portfolio-value').textContent = 
                '$' + data.portfolio_value.toFixed(2);
            document.getElementById('initial-capital').textContent = 
                '$' + data.initial_capital.toFixed(2);
            
            // P&L
            const pnlElement = document.getElementById('pnl');
            pnlElement.textContent = '$' + data.pnl.toFixed(2);
            pnlElement.className = 'metric ' + 
                (data.pnl > 0 ? 'positive' : data.pnl < 0 ? 'negative' : 'neutral');
            document.getElementById('pnl-pct').textContent = 
                data.pnl_pct.toFixed(2) + '%';
            
            // MDD
            const mddElement = document.getElementById('mdd');
            mddElement.textContent = (data.mdd * 100).toFixed(2) + '%';
            mddElement.className = 'metric ' + 
                (data.mdd >= 0.05 ? 'negative' : data.mdd >= 0.03 ? 'negative' : 
                 data.mdd >= 0.02 ? 'neutral' : 'positive');
            document.getElementById('peak-value').textContent = 
                '$' + data.peak_value.toFixed(2);
            
            // Trades
            document.getElementById('total-trades').textContent = data.total_trades;
            document.getElementById('win-rate').textContent = data.win_rate.toFixed(1) + '%';
            
            // Cash y posiciones
            document.getElementById('cash').textContent = '$' + data.cash.toFixed(2);
            document.getElementById('positions').textContent = data.positions;
            
            // Precio BTC
            document.getElementById('btc-price').textContent = 
                '$' + data.btc_price.toLocaleString('en-US', {minimumFractionDigits: 2});
            
            // Trades list
            updateTradeList(data.recent_trades);
            
            // Last update
            document.getElementById('last-update').textContent = 
                new Date().toLocaleTimeString();
            
            // Status
            document.getElementById('system-status').textContent = 
                data.kill_switch ? 'DETENIDO' : 'ACTIVO';
        }
        
        function updateTradeList(trades) {
            const tradeList = document.getElementById('trade-list');
            
            if (!trades || trades.length === 0) {
                tradeList.innerHTML = '<p style="text-align: center; color: #9ca3af;">No hay trades aún...</p>';
                return;
            }
            
            tradeList.innerHTML = trades.map(trade => {
                const pnlText = trade.pnl !== undefined ? 
                    ` | P&L: $${trade.pnl.toFixed(2)} (${trade.pnl_pct.toFixed(2)}%)` : '';
                const reasonText = trade.reason ? ` - ${trade.reason}` : '';
                
                return `
                    <div class="trade-item ${trade.action.toLowerCase()}">
                        <div class="trade-header">
                            <span>${trade.action} ${trade.symbol}</span>
                            <span>${new Date(trade.timestamp).toLocaleTimeString()}</span>
                        </div>
                        <div class="trade-details">
                            Precio: $${trade.price.toLocaleString('en-US', {minimumFractionDigits: 2})} | 
                            Cantidad: ${trade.amount.toFixed(8)}${pnlText}${reasonText}
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        // Actualizar cada 5 segundos
        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>
    '''
    return html

@app.route('/api/status')
def get_status():
    """API endpoint para obtener estado actual"""
    try:
        # Buscar la sesión más reciente
        session_files = glob.glob('autonomous_session_*.json')
        
        if not session_files:
            return jsonify({
                'portfolio_value': 40.0,
                'initial_capital': 40.0,
                'pnl': 0.0,
                'pnl_pct': 0.0,
                'mdd': 0.0,
                'peak_value': 40.0,
                'total_trades': 0,
                'win_rate': 0.0,
                'cash': 40.0,
                'positions': 0,
                'btc_price': 0.0,
                'recent_trades': [],
                'kill_switch': False
            })
        
        latest_session = max(session_files, key=os.path.getctime)
        
        with open(latest_session, 'r') as f:
            data = json.load(f)
        
        # Calcular win rate
        sells = [t for t in data.get('trade_history', []) if t['action'] == 'SELL']
        winning_trades = [t for t in sells if t.get('pnl', 0) > 0]
        win_rate = (len(winning_trades) / len(sells) * 100) if sells else 0
        
        # Obtener precio actual de BTC
        try:
            import requests
            response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot', timeout=5)
            btc_price = float(response.json()['data']['amount'])
        except:
            btc_price = 0.0
        
        return jsonify({
            'portfolio_value': data.get('final_portfolio', 40.0),
            'initial_capital': data.get('initial_capital', 40.0),
            'pnl': data.get('pnl', 0.0),
            'pnl_pct': data.get('pnl_pct', 0.0),
            'mdd': data.get('max_drawdown', 0.0),
            'peak_value': data.get('peak_value', 40.0),
            'total_trades': data.get('total_trades', 0),
            'win_rate': win_rate,
            'cash': data.get('cash', 40.0),
            'positions': len(data.get('positions', {})),
            'btc_price': btc_price,
            'recent_trades': data.get('trade_history', [])[-10:][::-1],
            'kill_switch': data.get('kill_switch_events', 0) > 0
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🌐 DASHBOARD EN TIEMPO REAL - Trading Autónomo")
    print("="*80)
    print("\n📊 Abriendo dashboard en: http://localhost:5000")
    print("⚡ Actualización automática cada 5 segundos")
    print("\nPresiona CTRL+C para detener\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
