#!/usr/bin/env python3
"""Script para obtener OANDA Account ID automáticamente"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_oanda_accounts():
    """Obtiene lista de cuentas de OANDA"""
    
    api_key = os.getenv("OANDA_API_KEY", "")
    environment = os.getenv("OANDA_ENVIRONMENT", "practice")
    
    if not api_key:
        print("❌ OANDA_API_KEY no encontrado en .env")
        return
    
    print(f"🔑 Testing API Key: {api_key[:20]}...")
    
    # URL según environment
    if environment == "practice":
        base_url = "https://api-fxpractice.oanda.com"
    else:
        base_url = "https://api-fxtrade.oanda.com"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🔍 Consultando cuentas en OANDA ({environment})...")
        print(f"📡 URL: {base_url}/v3/accounts")
        
        response = requests.get(f"{base_url}/v3/accounts", headers=headers, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text[:200]}...")
        
        response.raise_for_status()
        
        data = response.json()
        accounts = data.get("accounts", [])
        
        if not accounts:
            print("❌ No se encontraron cuentas")
            return
        
        print(f"\n✅ {len(accounts)} cuenta(s) encontrada(s):\n")
        
        for acc in accounts:
            account_id = acc.get("id")
            tags = acc.get("tags", [])
            
            print(f"   Account ID: {account_id}")
            print(f"   Tags: {', '.join(tags) if tags else 'N/A'}")
            print()
        
        # Actualizar .env automáticamente
        if len(accounts) == 1:
            account_id = accounts[0].get("id")
            print(f"💾 Actualizando .env con Account ID: {account_id}")
            
            # Leer .env actual
            with open(".env", "r") as f:
                lines = f.readlines()
            
            # Actualizar línea de OANDA_ACCOUNT_ID
            updated = False
            for i, line in enumerate(lines):
                if line.startswith("OANDA_ACCOUNT_ID="):
                    lines[i] = f"OANDA_ACCOUNT_ID={account_id}\n"
                    updated = True
                    break
            
            # Escribir .env actualizado
            with open(".env", "w") as f:
                f.writelines(lines)
            
            print("✅ .env actualizado exitosamente!")
        else:
            print("⚠️  Múltiples cuentas encontradas. Copia manualmente el Account ID al .env")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando a OANDA: {e}")

if __name__ == "__main__":
    get_oanda_accounts()
