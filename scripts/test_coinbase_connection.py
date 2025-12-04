#!/usr/bin/env python3
"""Test de conexión a Coinbase API"""

import os
from dotenv import load_dotenv
from intelligent_investment_bot import MarketEnvironment

load_dotenv()

def test_coinbase_connection():
    """Testea conexión a Coinbase y obtiene market data"""
    
    print("🔑 Verificando credenciales...")
    api_key = os.getenv("COINBASE_API_KEY", "")
    api_secret = os.getenv("COINBASE_API_SECRET", "")
    
    if not api_key or not api_secret:
        print("❌ ERROR: No se encontraron COINBASE_API_KEY o COINBASE_API_SECRET en .env")
        print("\n📝 Crea un archivo .env con:")
        print("COINBASE_API_KEY=tu_key")
        print("COINBASE_API_SECRET=tu_secret")
        return
    
    print(f"✅ API Key encontrada: {api_key[:8]}...")
    print(f"✅ API Secret encontrada: {api_secret[:8]}...")
    
    print("\n🌐 Conectando a Coinbase Advanced Trade API...")
    env = MarketEnvironment(exchange="coinbase", symbol="BTC-USD")
    
    print("📊 Obteniendo market data...")
    data = env.get_market_data()
    
    print("\n" + "="*60)
    print("📈 COINBASE MARKET DATA - BTC/USD")
    print("="*60)
    print(f"💰 Precio actual: ${data['price']:,.2f}")
    print(f"📊 Volumen 24h: {data['volume_24h']:,.2f}")
    print(f"📈 Cambio 24h: {data['price_change_24h']:+.2f}%")
    print(f"🔝 High 24h: ${data['high_24h']:,.2f}")
    print(f"🔻 Low 24h: ${data['low_24h']:,.2f}")
    print(f"📉 Historical closes: {len(data['closes'])} data points")
    print(f"⏰ Timestamp: {data['timestamp']}")
    print("="*60)
    
    if data['closes'] and len(data['closes']) > 1:
        print("\n✅ CONEXIÓN EXITOSA - Datos reales de Coinbase!")
    else:
        print("\n⚠️ Usando datos simulados (verificar API keys)")

if __name__ == "__main__":
    test_coinbase_connection()
