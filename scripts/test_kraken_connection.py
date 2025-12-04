#!/usr/bin/env python3
"""Test de conexión a Kraken API"""

import os
import requests
import hmac
import hashlib
import base64
import time
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

def get_kraken_signature(urlpath, data, secret):
    """Genera firma para autenticación de Kraken"""
    postdata = urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def test_kraken_connection():
    """Testea conexión a Kraken"""
    
    api_key = os.getenv("KRAKEN_API_KEY", "")
    api_secret = os.getenv("KRAKEN_API_SECRET", "")
    
    if not api_key or not api_secret:
        print("❌ KRAKEN_API_KEY o KRAKEN_API_SECRET no encontrados en .env")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🔐 API Secret: {api_secret[:10]}...")
    
    # Test 1: Public endpoint (no auth)
    print("\n📊 Test 1: Obteniendo precio BTC/USD (público)...")
    try:
        response = requests.get(
            "https://api.kraken.com/0/public/Ticker",
            params={"pair": "XBTUSD"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("error") and len(data["error"]) > 0:
            print(f"❌ Error: {data['error']}")
        else:
            price = data["result"]["XXBTZUSD"]["c"][0]
            print(f"✅ Precio BTC: ${float(price):,.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Private endpoint (balance)
    print("\n💰 Test 2: Obteniendo balance (privado)...")
    try:
        url = "https://api.kraken.com/0/private/Balance"
        urlpath = "/0/private/Balance"
        
        nonce = str(int(time.time() * 1000))
        data = {"nonce": nonce}
        
        headers = {
            "API-Key": api_key,
            "API-Sign": get_kraken_signature(urlpath, data, api_secret)
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("error") and len(result["error"]) > 0:
            print(f"❌ Error de autenticación: {result['error']}")
            print("\n💡 Posibles causas:")
            print("   1. API Key o Secret incorrectos")
            print("   2. Permisos insuficientes (necesitas 'Query Funds')")
            print("   3. IP bloqueada (si configuraste restricción de IP)")
        else:
            balances = result.get("result", {})
            print(f"✅ Balance obtenido:")
            if balances:
                for currency, amount in balances.items():
                    print(f"   {currency}: {float(amount):,.4f}")
            else:
                print("   (Cuenta vacía)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 Testing Kraken API Connection...\n")
    test_kraken_connection()
