#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DASHBOARD MULTI-CRYPTO
Visualización en tiempo real de múltiples cryptos
"""

from flask import Flask, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Crypto Trading Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 1.8em;
            font-weight: bold;
        }
        .cryptos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .crypto-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid rgba(255,255,255,0.2);
        }
        .crypto-card.holding {
            border-color: #4ade80;
            box-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
        }
        .crypto-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .crypto-name {
            font-size: 1.3em;
            font-weight: bold;
        }
        .crypto-price {
            font-size: 1.5em;
            color: #fbbf24;
        }
        .signal {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }
        .signal.buy { background: #10b981; }
        .signal.sell { background: #ef4444; }
        .signal.hold { background: #6b7280; }
        .confidence {
            font-size: 0.9em;
            margin-top: 5px;
            opacity: 0.9;
        }
        .reasons {
            margin-top: 10px;
            font-size: 0.85em;
            opacity: 0.8;
        }
        .position-info {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.2);
            font-size: 0.9em;
        }
        .opportunities {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .opportunity-item {
            padding: 10px;
            margin: 10px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }
        .timestamp {
            text-align: center;
            margin-top: 20px;
            opacity: 0.7;
            font-size: 0.9em;
        }
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Multi-Crypto Trading Dashboard</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Portfolio Value</div>
                <div class="stat-value" id="portfolio">$0.00</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Cash Available</div>
                <div class="stat-value" id="cash">$0.00</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Open Positions</div>
                <div class="stat-value" id="positions">0/3</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total P&L</div>
                <div class="stat-value" id="pnl">$0.00 (0%)</div>
            </div>
        </div>
        
        <div class="cryptos-grid" id="cryptos">
            <!-- Cryptos will be loaded here -->
        </div>
        
        <div class="opportunities">
            <h2>🎯 Top Opportunities</h2>
            <div id="opportunities">
                <!-- Opportunities will be loaded here -->
            </div>
        </div>
        
        <div class="timestamp" id="timestamp">Loading...</div>
    </div>
    
    <script>
        function updateDashboard() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    // Update stats
                    document.getElementById('portfolio').textContent = '$' + data.portfolio_value.toFixed(2);
                    document.getElementById('cash').textContent = '$' + data.cash.toFixed(2);
                    document.getElementById('positions').textContent = data.positions_count + '/3';
                    
                    const pnl = data.pnl;
                    const pnlPct = data.pnl_pct;
                    const pnlClass = pnl >= 0 ? 'positive' : 'negative';
                    document.getElementById('pnl').innerHTML = 
                        `<span class="${pnlClass}">$${pnl.toFixed(2)} (${pnlPct >= 0 ? '+' : ''}${pnlPct.toFixed(2)}%)</span>`;
                    
                    // Update cryptos
                    const cryptosDiv = document.getElementById('cryptos');
                    cryptosDiv.innerHTML = '';
                    
                    data.cryptos.forEach(crypto => {
                        const isHolding = data.positions.hasOwnProperty(crypto.pair);
                        const cardClass = isHolding ? 'crypto-card holding' : 'crypto-card';
                        
                        let positionHTML = '';
                        if (isHolding) {
                            const pos = data.positions[crypto.pair];
                            const posClass = pos.pnl_pct >= 0 ? 'positive' : 'negative';
                            positionHTML = `
                                <div class="position-info">
                                    <strong>HOLDING:</strong> ${pos.quantity.toFixed(8)}<br>
                                    Entry: $${pos.entry_price.toFixed(2)}<br>
                                    P&L: <span class="${posClass}">${pos.pnl_pct >= 0 ? '+' : ''}${pos.pnl_pct.toFixed(2)}%</span>
                                </div>
                            `;
                        }
                        
                        const signalClass = crypto.signal.toLowerCase();
                        const signalEmoji = crypto.signal === 'BUY' ? '🟢' : crypto.signal === 'SELL' ? '🔴' : '⚪';
                        
                        cryptosDiv.innerHTML += `
                            <div class="${cardClass}">
                                <div class="crypto-header">
                                    <div class="crypto-name">${crypto.pair}</div>
                                    <div class="crypto-price">$${crypto.price.toLocaleString()}</div>
                                </div>
                                <div>
                                    ${signalEmoji} <span class="signal ${signalClass}">${crypto.signal}</span>
                                    <div class="confidence">Confidence: ${crypto.confidence.toFixed(0)}%</div>
                                </div>
                                <div class="reasons">
                                    ${crypto.reasons.slice(0, 2).join(' • ')}
                                </div>
                                ${positionHTML}
                            </div>
                        `;
                    });
                    
                    // Update opportunities
                    const oppDiv = document.getElementById('opportunities');
                    oppDiv.innerHTML = '';
                    
                    if (data.opportunities.length === 0) {
                        oppDiv.innerHTML = '<p>No high-confidence opportunities at the moment</p>';
                    } else {
                        data.opportunities.forEach((opp, index) => {
                            oppDiv.innerHTML += `
                                <div class="opportunity-item">
                                    <strong>${index + 1}. ${opp.pair}</strong> - ${opp.signal} (${opp.confidence.toFixed(0)}%)<br>
                                    <small>${opp.reasons.slice(0, 2).join(' • ')}</small>
                                </div>
                            `;
                        });
                    }
                    
                    // Update timestamp
                    document.getElementById('timestamp').textContent = 
                        'Last update: ' + new Date(data.timestamp).toLocaleString();
                })
                .catch(error => {
                    console.error('Error updating dashboard:', error);
                    document.getElementById('timestamp').textContent = 'Error loading data';
                });
        }
        
        // Update every 5 seconds
        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """API endpoint que devuelve el estado actual del sistema"""
    try:
        # Buscar el archivo de sesión más reciente
        session_files = [f for f in os.listdir('.') if f.startswith('multi_crypto_session_') and f.endswith('.json')]
        
        if not session_files:
            return {
                "timestamp": datetime.now().isoformat(),
                "portfolio_value": 40.0,
                "cash": 40.0,
                "positions_count": 0,
                "positions": {},
                "pnl": 0.0,
                "pnl_pct": 0.0,
                "cryptos": [],
                "opportunities": []
            }
        
        # Ordenar por fecha y tomar el más reciente
        latest_session = sorted(session_files)[-1]
        
        with open(latest_session, 'r') as f:
            data = json.load(f)
        
        # Calcular P&L de posiciones
        positions_with_pnl = {}
        for pair, pos in data.get('positions', {}).items():
            # Aquí necesitaríamos el precio actual, por ahora usamos entry_price
            positions_with_pnl[pair] = {
                "quantity": pos["quantity"],
                "entry_price": pos["entry_price"],
                "pnl_pct": 0.0  # Sería calculado con precio actual
            }
        
        return {
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "portfolio_value": data.get("portfolio_value", 40.0),
            "cash": data.get("cash", 40.0),
            "positions_count": len(data.get("positions", {})),
            "positions": positions_with_pnl,
            "pnl": data.get("portfolio_value", 40.0) - data.get("initial_capital", 40.0),
            "pnl_pct": ((data.get("portfolio_value", 40.0) - data.get("initial_capital", 40.0)) / data.get("initial_capital", 40.0)) * 100,
            "cryptos": [
                {
                    "pair": "BTC-USD",
                    "price": 93000,
                    "signal": "HOLD",
                    "confidence": 0,
                    "reasons": ["Gathering data..."]
                }
            ],
            "opportunities": []
        }
    
    except Exception as e:
        print(f"Error loading session: {e}")
        return {
            "timestamp": datetime.now().isoformat(),
            "portfolio_value": 40.0,
            "cash": 40.0,
            "positions_count": 0,
            "positions": {},
            "pnl": 0.0,
            "pnl_pct": 0.0,
            "cryptos": [],
            "opportunities": [],
            "error": str(e)
        }

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 MULTI-CRYPTO DASHBOARD")
    print("="*80)
    print("\nDashboard running at: http://localhost:5000")
    print("Press CTRL+C to stop\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
