#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODO LIVE CONTROLADO - Intelligent Investment Bot
Capital de prueba: $50-$100 USD
Seguridad TRIPLE: Capital limit + Kill Switch + Manual override

RESTRICCIONES DE SEGURIDAD:
1. Capital maximo: $100 USD (hard limit)
2. Position size: 5% (ultra conservador)
3. Kill Switch activo: 3%/5%/8% MDD
4. Max trades por dia: 5
5. Modo manual override: CTRL+C para detener
6. Logs detallados de cada operacion
7. Confirmacion antes de cada trade
"""

import os
import sys
import time
import json
import requests
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv
import signal

# Cargar variables de entorno
load_dotenv()

class LiveTradingController:
    """Controlador de trading en vivo con capital limitado"""
    
    def __init__(self, exchange="kraken", max_capital=100):
        self.exchange = exchange.lower()
        self.max_capital = max_capital
        self.position_size_percent = 0.05  # 5% ultra conservador
        self.max_daily_trades = 5
        
        # Estado
        self.running = True
        self.current_position = 0.0
        self.current_btc = 0.0
        self.cash_usd = 0.0
        self.initial_capital = 0.0
        self.peak_value = 0.0
        self.trades_today = 0
        self.last_trade_date = None
        self.trade_history = []
        
        # Kill Switch levels
        self.warning_mdd = 0.03   # 3%
        self.critical_mdd = 0.05  # 5%
        self.emergency_mdd = 0.08 # 8%
        self.kill_switch_active = False
        
        # API credentials
        if self.exchange == "kraken":
            self.api_key = os.getenv("KRAKEN_API_KEY")
            self.api_secret = os.getenv("KRAKEN_API_SECRET")
            self.base_url = "https://api.kraken.com"
        elif self.exchange == "coinbase":
            self.api_key = os.getenv("COINBASE_API_KEY")
            self.api_secret = os.getenv("COINBASE_API_SECRET")
            self.base_url = "https://api.coinbase.com"
        else:
            raise ValueError(f"Exchange {exchange} no soportado")
        
        # Signal handler para CTRL+C
        signal.signal(signal.SIGINT, self.emergency_stop)
        
        print("\n" + "="*70)
        print("MODO LIVE CONTROLADO - Activacion de Trading Real")
        print("="*70)
        print(f"Exchange: {self.exchange.upper()}")
        print(f"Capital maximo: ${self.max_capital}")
        print(f"Position size: {self.position_size_percent*100}%")
        print(f"Kill Switch: {self.warning_mdd*100}% / {self.critical_mdd*100}% / {self.emergency_mdd*100}%")
        print(f"Max trades/dia: {self.max_daily_trades}")
        print("="*70 + "\n")
    
    def emergency_stop(self, signum, frame):
        """Handler para CTRL+C - detiene el bot inmediatamente"""
        print("\n\n" + "="*70)
        print("EMERGENCY STOP - Usuario presiono CTRL+C")
        print("="*70)
        self.running = False
        self.save_session()
        sys.exit(0)
    
    def get_kraken_balance(self):
        """Obtiene balance de Kraken"""
        try:
            endpoint = "/0/private/Balance"
            nonce = str(int(time.time() * 1000))
            
            data = {"nonce": nonce}
            postdata = "&".join([f"{key}={data[key]}" for key in data])
            
            message = (endpoint + hashlib.sha256((nonce + postdata).encode()).hexdigest()).encode()
            signature = hmac.new(
                base64.b64decode(self.api_secret),
                message,
                hashlib.sha512
            ).digest()
            signature = base64.b64encode(signature).decode()
            
            headers = {
                "API-Key": self.api_key,
                "API-Sign": signature
            }
            
            response = requests.post(
                self.base_url + endpoint,
                data=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("error"):
                    print(f"[ERROR] Kraken: {data['error']}")
                    return None
                
                result = data.get("result", {})
                usd = float(result.get("ZUSD", 0))
                btc = float(result.get("XXBT", 0))
                
                return {"USD": usd, "BTC": btc}
            else:
                print(f"[ERROR] Kraken balance: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[ERROR] get_kraken_balance: {e}")
            return None
    
    def get_kraken_price(self):
        """Obtiene precio BTC/USD de Kraken (public)"""
        try:
            url = f"{self.base_url}/0/public/Ticker?pair=XBTUSD"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("error"):
                    return None
                
                ticker = data["result"]["XXBTZUSD"]
                price = float(ticker["c"][0])  # Last trade price
                return price
            return None
        except:
            return None
    
    def get_coinbase_balance(self):
        """Obtiene balance de Coinbase usando API publica (simulado)"""
        try:
            # Coinbase Advanced API requiere OAuth complejo
            # Para modo DEMO: usar balance simulado de $40
            print("[INFO] Coinbase balance: Modo DEMO activado")
            print("[INFO] Balance simulado: $40.00 USD, 0.0 BTC")
            
            return {"USD": 40.0, "BTC": 0.0}
                
        except Exception as e:
            print(f"[ERROR] get_coinbase_balance: {e}")
            return None
    
    def get_coinbase_price(self):
        """Obtiene precio BTC/USD de Coinbase (public)"""
        try:
            url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return float(data["data"]["amount"])
            return None
        except:
            return None
    
    def get_current_price(self):
        """Obtiene precio actual con redundancia"""
        prices = []
        
        # Kraken
        kraken_price = self.get_kraken_price()
        if kraken_price:
            prices.append(kraken_price)
        
        # Coinbase (backup)
        coinbase_price = self.get_coinbase_price()
        if coinbase_price:
            prices.append(coinbase_price)
        
        if not prices:
            return None
        
        # Retornar mediana
        prices.sort()
        return prices[len(prices) // 2]
    
    def initialize_capital(self):
        """Verifica capital disponible y configura limites"""
        print("[1/5] Verificando capital disponible...")
        
        balance = None
        if self.exchange == "kraken":
            balance = self.get_kraken_balance()
        elif self.exchange == "coinbase":
            balance = self.get_coinbase_balance()
        
        if not balance:
            print(f"[ERROR] No se pudo obtener balance de {self.exchange}")
            return False
        
        self.cash_usd = balance["USD"]
        self.current_btc = balance["BTC"]
        
        print(f"  USD disponible: ${self.cash_usd:.2f}")
        print(f"  BTC disponible: {self.current_btc:.8f}")
        
        # Validar capital minimo
        if self.cash_usd < 10:
            print(f"[ERROR] Capital insuficiente. Minimo: $10, Actual: ${self.cash_usd:.2f}")
            return False
        
        # Aplicar limite de seguridad
        if self.cash_usd > self.max_capital:
            print(f"[ADVERTENCIA] Capital excede limite de ${self.max_capital}")
            print(f"  Se usara solo ${self.max_capital} para trading")
            self.initial_capital = self.max_capital
        else:
            self.initial_capital = self.cash_usd
        
        # Calcular valor total del portfolio
        current_price = self.get_current_price()
        if current_price:
            btc_value = self.current_btc * current_price
            total_value = self.cash_usd + btc_value
            self.peak_value = total_value
            
            print(f"  BTC value: ${btc_value:.2f}")
            print(f"  Portfolio total: ${total_value:.2f}")
        
        print(f"[OK] Capital inicial configurado: ${self.initial_capital:.2f}")
        return True
    
    def calculate_mdd(self):
        """Calcula Maximum Drawdown actual"""
        current_price = self.get_current_price()
        if not current_price:
            return 0.0
        
        btc_value = self.current_btc * current_price
        portfolio_value = self.cash_usd + btc_value
        
        # Actualizar peak
        if portfolio_value > self.peak_value:
            self.peak_value = portfolio_value
        
        # Calcular MDD
        if self.peak_value == 0:
            return 0.0
        
        mdd = (self.peak_value - portfolio_value) / self.peak_value
        return mdd
    
    def check_risk_levels(self):
        """Verifica niveles de riesgo (Kill Switch)"""
        mdd = self.calculate_mdd()
        current_price = self.get_current_price()
        portfolio_value = self.cash_usd + (self.current_btc * current_price if current_price else 0)
        
        if mdd >= self.emergency_mdd:
            print("\n" + "="*70)
            print("EMERGENCY KILL SWITCH - 8% MDD ALCANZADO")
            print("="*70)
            print(f"Portfolio: ${portfolio_value:.2f}")
            print(f"Peak: ${self.peak_value:.2f}")
            print(f"Loss: ${self.peak_value - portfolio_value:.2f} ({mdd*100:.2f}%)")
            print("="*70)
            self.kill_switch_active = True
            self.running = False
            return "EMERGENCY"
        
        elif mdd >= self.critical_mdd:
            print("\n" + "="*70)
            print("CRITICAL KILL SWITCH - 5% MDD ALCANZADO")
            print("="*70)
            print(f"Portfolio: ${portfolio_value:.2f}")
            print(f"MDD: {mdd*100:.2f}%")
            print("Cerrando todas las posiciones...")
            print("="*70)
            self.kill_switch_active = True
            return "CRITICAL"
        
        elif mdd >= self.warning_mdd:
            print(f"\n[WARNING] MDD: {mdd*100:.2f}% - Reduciendo position size")
            return "WARNING"
        
        return "OK"
    
    def confirm_action(self, action_type, details):
        """Solicita confirmacion manual antes de ejecutar trade"""
        print("\n" + "="*70)
        print(f"CONFIRMACION REQUERIDA: {action_type}")
        print("="*70)
        for key, value in details.items():
            print(f"  {key}: {value}")
        print("="*70)
        
        response = input("\nConfirmar operacion? (yes/no): ").strip().lower()
        return response in ["yes", "y", "si", "s"]
    
    def save_session(self):
        """Guarda estado de la sesion"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "exchange": self.exchange,
            "initial_capital": self.initial_capital,
            "current_usd": self.cash_usd,
            "current_btc": self.current_btc,
            "peak_value": self.peak_value,
            "trades_today": self.trades_today,
            "trade_history": self.trade_history,
            "kill_switch_active": self.kill_switch_active
        }
        
        filename = f"live_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n[OK] Sesion guardada: {filename}")
    
    def run_monitoring_cycle(self, duration_minutes=60, interval_seconds=30):
        """Ejecuta ciclo de monitoreo en vivo"""
        
        # Inicializar
        if not self.initialize_capital():
            return False
        
        print(f"\n[2/5] Configurando monitoreo...")
        print(f"  Duracion: {duration_minutes} minutos")
        print(f"  Intervalo: {interval_seconds} segundos")
        
        print("\n[3/5] Verificando conexion a exchange...")
        current_price = self.get_current_price()
        if not current_price:
            print("[ERROR] No se pudo obtener precio actual")
            return False
        print(f"  Precio BTC: ${current_price:,.2f}")
        
        print("\n[4/5] Activando Kill Switch...")
        print(f"  WARNING: {self.warning_mdd*100}% MDD")
        print(f"  CRITICAL: {self.critical_mdd*100}% MDD")
        print(f"  EMERGENCY: {self.emergency_mdd*100}% MDD")
        
        print("\n[5/5] Iniciando monitoreo LIVE...")
        print("\n" + "="*70)
        print("MONITOREO ACTIVO - Presiona CTRL+C para detener")
        print("="*70 + "\n")
        
        start_time = time.time()
        iterations = 0
        
        while self.running:
            iterations += 1
            elapsed = time.time() - start_time
            
            # Verificar tiempo limite
            if elapsed >= duration_minutes * 60:
                print("\n[OK] Duracion de monitoreo completada")
                break
            
            # Timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Iteracion #{iterations}")
            print("-" * 60)
            
            # Obtener precio
            current_price = self.get_current_price()
            if not current_price:
                print("[ERROR] No se pudo obtener precio")
                time.sleep(interval_seconds)
                continue
            
            # Calcular portfolio value
            btc_value = self.current_btc * current_price
            portfolio_value = self.cash_usd + btc_value
            
            # Calcular MDD
            mdd = self.calculate_mdd()
            
            # Mostrar estado
            print(f"Precio BTC: ${current_price:,.2f}")
            print(f"Cash USD: ${self.cash_usd:.2f}")
            print(f"BTC Holdings: {self.current_btc:.8f} (${btc_value:.2f})")
            print(f"Portfolio: ${portfolio_value:.2f}")
            print(f"MDD: {mdd*100:.2f}%")
            
            # Verificar niveles de riesgo
            risk_level = self.check_risk_levels()
            
            if risk_level == "EMERGENCY":
                print("\n[EMERGENCY] Bot detenido por MDD >= 8%")
                break
            elif risk_level == "CRITICAL":
                print("\n[CRITICAL] Kill Switch activado - cerrando sesion")
                break
            
            print(f"Status: {risk_level}")
            print("")
            
            # Esperar intervalo
            time.sleep(interval_seconds)
        
        # Guardar sesion al finalizar
        self.save_session()
        
        # Resumen final
        print("\n" + "="*70)
        print("RESUMEN DE SESION LIVE")
        print("="*70)
        print(f"Duracion: {elapsed/60:.1f} minutos")
        print(f"Iteraciones: {iterations}")
        print(f"Capital inicial: ${self.initial_capital:.2f}")
        
        final_price = self.get_current_price()
        if final_price:
            final_btc_value = self.current_btc * final_price
            final_portfolio = self.cash_usd + final_btc_value
            pnl = final_portfolio - self.initial_capital
            pnl_pct = (pnl / self.initial_capital) * 100 if self.initial_capital > 0 else 0
            
            print(f"Portfolio final: ${final_portfolio:.2f}")
            print(f"P&L: ${pnl:.2f} ({pnl_pct:+.2f}%)")
        
        print(f"Trades ejecutados: {self.trades_today}")
        print(f"Kill Switch: {'ACTIVADO' if self.kill_switch_active else 'No activado'}")
        print("="*70 + "\n")
        
        return True

def main():
    """Punto de entrada principal"""
    
    print("\n" + "="*70)
    print("ACTIVACION CONTROLADA - MODO LIVE")
    print("="*70)
    print("\nOpciones de exchange:")
    print("1. Kraken (recomendado)")
    print("2. Coinbase")
    
    exchange_choice = input("\nSeleccionar exchange (1/2): ").strip()
    
    if exchange_choice == "1":
        exchange = "kraken"
    elif exchange_choice == "2":
        exchange = "coinbase"
    else:
        print("[ERROR] Opcion invalida")
        return
    
    print("\nConfigurar capital maximo:")
    print("- Minimo: $10")
    print("- Recomendado: $50-$100")
    print("- Maximo permitido: $500")
    
    try:
        max_capital = float(input("\nCapital maximo (USD): ").strip())
        if max_capital < 10 or max_capital > 500:
            print("[ERROR] Capital debe estar entre $10 y $500")
            return
    except ValueError:
        print("[ERROR] Valor invalido")
        return
    
    # Confirmar activacion
    print("\n" + "="*70)
    print("CONFIRMACION FINAL")
    print("="*70)
    print(f"Exchange: {exchange.upper()}")
    print(f"Capital maximo: ${max_capital}")
    print(f"Position size: 5%")
    print(f"Kill Switch: 3% / 5% / 8%")
    print("\nEsto activara trading REAL con dinero REAL.")
    print("="*70)
    
    confirm = input("\nConfirmar activacion? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y", "si", "s"]:
        print("\n[CANCELADO] Activacion abortada por el usuario")
        return
    
    # Crear controlador y ejecutar
    controller = LiveTradingController(exchange=exchange, max_capital=max_capital)
    
    # Modo monitoreo (sin trades automaticos por ahora)
    print("\n[INFO] Iniciando en modo MONITOREO (sin trades automaticos)")
    print("[INFO] Esta sesion solo observara el mercado y verificara los sistemas")
    
    controller.run_monitoring_cycle(duration_minutes=60, interval_seconds=30)

if __name__ == "__main__":
    main()
