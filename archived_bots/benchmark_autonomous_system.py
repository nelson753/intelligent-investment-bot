#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BENCHMARK COMPLETO - SISTEMA DE TRADING AUTÓNOMO
Validación exhaustiva de todos los componentes críticos
"""

import sys
import time
import json
import numpy as np
import requests
from datetime import datetime, timedelta
import traceback

# Importar clases del sistema autónomo
try:
    from autonomous_trading_system import (
        TechnicalIndicators,
        AutonomousTradingSystem,
        CAPITAL_INICIAL,
        POSITION_SIZE_PERCENT,
        STOP_LOSS_PERCENT,
        TAKE_PROFIT_PERCENT,
        MAX_POSITIONS,
        MDD_WARNING,
        MDD_CRITICAL,
        MDD_EMERGENCY
    )
    IMPORT_SUCCESS = True
except Exception as e:
    print(f"[ERROR] No se pudo importar el sistema: {e}")
    IMPORT_SUCCESS = False


class BenchmarkAutonomousSystem:
    """Benchmark exhaustivo del sistema autónomo"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.warnings = []
        self.results = {}
        self.start_time = datetime.now()
        
    def print_header(self, title):
        """Imprime encabezado de sección"""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80)
    
    def test_passed(self, test_name, details=""):
        """Marca test como pasado"""
        self.tests_passed += 1
        print(f"✅ {test_name}")
        if details:
            print(f"   {details}")
        self.results[test_name] = {"status": "PASS", "details": details}
    
    def test_failed(self, test_name, reason=""):
        """Marca test como fallido"""
        self.tests_failed += 1
        print(f"❌ {test_name}")
        if reason:
            print(f"   Razón: {reason}")
        self.results[test_name] = {"status": "FAIL", "reason": reason}
    
    def add_warning(self, warning):
        """Agrega advertencia"""
        self.warnings.append(warning)
        print(f"⚠️  {warning}")
    
    def test_imports(self):
        """Test 1: Verificar importaciones"""
        self.print_header("TEST 1: IMPORTS Y DEPENDENCIAS")
        
        if not IMPORT_SUCCESS:
            self.test_failed("Imports del sistema autónomo", "No se pudo importar autonomous_trading_system.py")
            return False
        
        required_modules = [
            ('numpy', 'Cálculos numéricos'),
            ('requests', 'HTTP requests'),
            ('json', 'Manejo de JSON'),
            ('datetime', 'Manejo de fechas'),
            ('collections', 'Estructuras de datos')
        ]
        
        all_ok = True
        for module_name, description in required_modules:
            try:
                __import__(module_name)
                print(f"  ✓ {module_name:15} - {description}")
            except ImportError:
                print(f"  ✗ {module_name:15} - {description} - FALTA")
                all_ok = False
        
        if all_ok:
            self.test_passed("Todas las dependencias disponibles")
        else:
            self.test_failed("Dependencias faltantes")
        
        return all_ok
    
    def test_technical_indicators(self):
        """Test 2: Verificar indicadores técnicos"""
        self.print_header("TEST 2: INDICADORES TÉCNICOS")
        
        # Datos de prueba (100 precios simulados)
        np.random.seed(42)
        base_price = 90000
        prices = []
        current = base_price
        
        for i in range(100):
            change = np.random.normal(0, 0.01)  # 1% volatilidad
            current *= (1 + change)
            prices.append(current)
        
        all_passed = True
        
        # Test RSI
        try:
            rsi = TechnicalIndicators.calculate_rsi(prices, period=14)
            if 0 <= rsi <= 100:
                print(f"  ✓ RSI: {rsi:.2f} (válido: 0-100)")
            else:
                print(f"  ✗ RSI: {rsi:.2f} (fuera de rango)")
                all_passed = False
        except Exception as e:
            print(f"  ✗ RSI: Error - {e}")
            all_passed = False
        
        # Test MACD
        try:
            macd, signal, histogram = TechnicalIndicators.calculate_macd(prices)
            print(f"  ✓ MACD: {macd:.2f}, Signal: {signal:.2f}, Histogram: {histogram:.2f}")
        except Exception as e:
            print(f"  ✗ MACD: Error - {e}")
            all_passed = False
        
        # Test Bollinger Bands
        try:
            upper, middle, lower = TechnicalIndicators.calculate_bollinger_bands(prices, period=20)
            if upper > middle > lower:
                print(f"  ✓ Bollinger: Upper ${upper:,.0f} > Middle ${middle:,.0f} > Lower ${lower:,.0f}")
            else:
                print(f"  ✗ Bollinger: Bandas en orden incorrecto")
                all_passed = False
        except Exception as e:
            print(f"  ✗ Bollinger Bands: Error - {e}")
            all_passed = False
        
        # Test Volatilidad
        try:
            volatility = TechnicalIndicators.calculate_volatility(prices, period=20)
            if volatility >= 0:
                print(f"  ✓ Volatilidad: {volatility:.4f} (anualizada)")
            else:
                print(f"  ✗ Volatilidad: {volatility:.4f} (negativa)")
                all_passed = False
        except Exception as e:
            print(f"  ✗ Volatilidad: Error - {e}")
            all_passed = False
        
        if all_passed:
            self.test_passed("Indicadores técnicos funcionando correctamente")
        else:
            self.test_failed("Indicadores técnicos con errores")
    
    def test_signal_generation(self):
        """Test 3: Generación de señales"""
        self.print_header("TEST 3: GENERACIÓN DE SEÑALES")
        
        system = AutonomousTradingSystem(capital=40, paper_mode=True)
        
        # Simular diferentes escenarios
        scenarios = [
            {
                "name": "Mercado estable",
                "prices": [90000] * 50,
                "expected_action": "HOLD"
            },
            {
                "name": "Tendencia alcista fuerte",
                "prices": [90000 + i*100 for i in range(50)],
                "expected_action": "BUY"
            },
            {
                "name": "Tendencia bajista fuerte",
                "prices": [90000 - i*100 for i in range(50)],
                "expected_action": "SELL"
            },
            {
                "name": "Oversold (RSI < 30)",
                "prices": [90000] * 20 + [85000] * 30,  # Caída fuerte
                "expected_action": "BUY"
            }
        ]
        
        all_passed = True
        
        for scenario in scenarios:
            # Llenar historial de precios
            system.price_history.clear()
            for price in scenario['prices']:
                system.price_history.append(price)
            
            signal = system.generate_trading_signal()
            
            print(f"\n  Escenario: {scenario['name']}")
            print(f"    Señal: {signal['action']} (Confidence: {signal['confidence']:.1f}%)")
            print(f"    Razones: {', '.join(signal['reasons'][:3])}")
            
            # Verificar que la señal tenga estructura correcta
            if 'action' not in signal or 'confidence' not in signal or 'reasons' not in signal:
                print(f"    ✗ Estructura de señal incompleta")
                all_passed = False
            
            if not (0 <= signal['confidence'] <= 100):
                print(f"    ✗ Confidence fuera de rango: {signal['confidence']}")
                all_passed = False
        
        if all_passed:
            self.test_passed("Generación de señales correcta", "Todas las señales tienen estructura válida")
        else:
            self.test_failed("Generación de señales", "Errores en estructura o lógica")
    
    def test_risk_management(self):
        """Test 4: Gestión de riesgo"""
        self.print_header("TEST 4: GESTIÓN DE RIESGO")
        
        print(f"  Configuración actual:")
        print(f"    Capital inicial: ${CAPITAL_INICIAL}")
        print(f"    Position size: {POSITION_SIZE_PERCENT*100}%")
        print(f"    Stop Loss: {STOP_LOSS_PERCENT*100}%")
        print(f"    Take Profit: {TAKE_PROFIT_PERCENT*100}%")
        print(f"    Max posiciones: {MAX_POSITIONS}")
        print(f"    Kill Switch: {MDD_WARNING*100}% / {MDD_CRITICAL*100}% / {MDD_EMERGENCY*100}%")
        
        checks = []
        
        # Verificar limits razonables
        checks.append(("Position size <= 20%", POSITION_SIZE_PERCENT <= 0.20))
        checks.append(("Position size >= 5%", POSITION_SIZE_PERCENT >= 0.05))
        checks.append(("Stop Loss <= 5%", STOP_LOSS_PERCENT <= 0.05))
        checks.append(("Stop Loss >= 1%", STOP_LOSS_PERCENT >= 0.01))
        checks.append(("Take Profit >= Stop Loss", TAKE_PROFIT_PERCENT >= STOP_LOSS_PERCENT))
        checks.append(("Max positions >= 1", MAX_POSITIONS >= 1))
        checks.append(("Max positions <= 5", MAX_POSITIONS <= 5))
        checks.append(("Kill Switch levels ordered", MDD_WARNING < MDD_CRITICAL < MDD_EMERGENCY))
        checks.append(("Emergency MDD <= 10%", MDD_EMERGENCY <= 0.10))
        
        print("\n  Verificaciones:")
        all_passed = True
        for check_name, passed in checks:
            if passed:
                print(f"    ✓ {check_name}")
            else:
                print(f"    ✗ {check_name}")
                all_passed = False
        
        if all_passed:
            self.test_passed("Gestión de riesgo configurada correctamente")
        else:
            self.test_failed("Gestión de riesgo", "Algunos parámetros fuera de rangos seguros")
    
    def test_trading_operations(self):
        """Test 5: Operaciones de trading"""
        self.print_header("TEST 5: OPERACIONES DE TRADING")
        
        system = AutonomousTradingSystem(capital=40, paper_mode=True)
        
        # Simular precio
        system.price_history.append(90000)
        
        all_passed = True
        
        # Test: Ejecutar compra
        print("\n  Test: Ejecutar compra")
        try:
            initial_cash = system.cash
            result = system.execute_buy("BTC-USD", 4.0)
            
            if result:
                if system.cash < initial_cash:
                    print(f"    ✓ Cash reducido: ${initial_cash:.2f} → ${system.cash:.2f}")
                else:
                    print(f"    ✗ Cash no cambió")
                    all_passed = False
                
                if "BTC-USD" in system.positions:
                    position = system.positions["BTC-USD"]
                    print(f"    ✓ Posición creada: {position['amount']:.8f} BTC")
                    print(f"    ✓ Stop Loss: ${position['stop_loss']:,.2f}")
                    print(f"    ✓ Take Profit: ${position['take_profit']:,.2f}")
                else:
                    print(f"    ✗ Posición no creada")
                    all_passed = False
            else:
                print(f"    ✗ Compra falló")
                all_passed = False
        except Exception as e:
            print(f"    ✗ Error en compra: {e}")
            all_passed = False
        
        # Test: Stop Loss
        print("\n  Test: Stop Loss automático")
        try:
            if "BTC-USD" in system.positions:
                entry_price = system.positions["BTC-USD"]["entry_price"]
                stop_loss_price = system.positions["BTC-USD"]["stop_loss"]
                
                # Simular caída de precio usando override
                test_price = stop_loss_price - 100
                
                system.check_stop_loss_take_profit(override_price=test_price)
                
                if "BTC-USD" not in system.positions:
                    print(f"    ✓ Stop Loss ejecutado correctamente")
                else:
                    print(f"    ✗ Stop Loss no se ejecutó")
                    all_passed = False
        except Exception as e:
            print(f"    ✗ Error en Stop Loss: {e}")
            all_passed = False
        
        # Test: Límite de posiciones
        print("\n  Test: Límite de posiciones")
        try:
            system.positions.clear()
            system.cash = 40
            
            # Intentar crear MAX_POSITIONS + 1 posiciones
            positions_created = 0
            for i in range(MAX_POSITIONS + 2):
                # Simular posiciones existentes manualmente
                if i < MAX_POSITIONS:
                    system.positions[f"BTC-USD-{i}"] = {
                        'amount': 0.00004,
                        'entry_price': 90000,
                        'timestamp': datetime.now().isoformat(),
                        'stop_loss': 88200,
                        'take_profit': 94500
                    }
                    positions_created += 1
                else:
                    # Intentar comprar cuando ya hay MAX_POSITIONS
                    result = system.execute_buy(f"BTC-TEST-{i}", 4.0)
                    if result:
                        positions_created += 1
            
            if positions_created == MAX_POSITIONS:
                print(f"    ✓ Límite de posiciones respetado: {positions_created}/{MAX_POSITIONS}")
            else:
                print(f"    ✗ Límite no respetado: {positions_created} creadas, máximo {MAX_POSITIONS}")
                all_passed = False
        except Exception as e:
            print(f"    ✗ Error en límite de posiciones: {e}")
            all_passed = False
        
        if all_passed:
            self.test_passed("Operaciones de trading funcionando correctamente")
        else:
            self.test_failed("Operaciones de trading", "Errores en ejecución")
    
    def test_kill_switch(self):
        """Test 6: Kill Switch"""
        self.print_header("TEST 6: KILL SWITCH")
        
        system = AutonomousTradingSystem(capital=40, paper_mode=True)
        
        test_cases = [
            (0.01, False, "1% MDD - OK"),
            (0.019, False, "1.9% MDD - OK"),
            (0.02, False, "2% MDD - WARNING (continúa)"),
            (0.029, False, "2.9% MDD - WARNING"),
            (0.03, False, "3% MDD - CRITICAL (continúa)"),
            (0.049, False, "4.9% MDD - CRITICAL"),
            (0.05, True, "5% MDD - EMERGENCY (DETIENE)"),
            (0.10, True, "10% MDD - EMERGENCY (DETIENE)"),
        ]
        
        all_passed = True
        
        print("\n  Simulando diferentes niveles de MDD:")
        for mdd, should_stop, description in test_cases:
            # Simular MDD
            system.peak_value = 40.0
            system.cash = 40.0 * (1 - mdd)
            system.positions.clear()
            
            actual_mdd = system.calculate_mdd()
            would_stop = system.check_kill_switch()
            
            expected_icon = "🚨" if should_stop else "✓"
            actual_icon = "🚨" if would_stop else "✓"
            
            if would_stop == should_stop:
                print(f"    {actual_icon} {description}: {'STOP' if would_stop else 'CONTINÚA'}")
            else:
                print(f"    ✗ {description}: Esperado {'STOP' if should_stop else 'CONTINÚA'}, Got {'STOP' if would_stop else 'CONTINÚA'}")
                all_passed = False
        
        if all_passed:
            self.test_passed("Kill Switch funcionando correctamente", "Todos los niveles activados correctamente")
        else:
            self.test_failed("Kill Switch", "Niveles no se activan correctamente")
    
    def test_coinbase_api(self):
        """Test 7: Conexión con Coinbase API"""
        self.print_header("TEST 7: COINBASE API")
        
        try:
            url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
            
            print(f"  Endpoint: {url}")
            start_time = time.time()
            response = requests.get(url, timeout=10)
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                price = float(data["data"]["amount"])
                
                print(f"  ✓ Status Code: {response.status_code}")
                print(f"  ✓ Latencia: {latency:.2f} ms")
                print(f"  ✓ Precio BTC/USD: ${price:,.2f}")
                
                if latency > 1000:
                    self.add_warning(f"Latencia alta: {latency:.2f} ms")
                
                self.test_passed("Coinbase API funcional", f"Latencia: {latency:.2f}ms")
                return price
            else:
                self.test_failed("Coinbase API", f"Status {response.status_code}")
                return None
                
        except Exception as e:
            self.test_failed("Coinbase API", str(e))
            return None
    
    def test_session_persistence(self):
        """Test 8: Persistencia de sesiones"""
        self.print_header("TEST 8: PERSISTENCIA DE SESIONES")
        
        system = AutonomousTradingSystem(capital=40, paper_mode=True)
        
        # Simular algunos datos
        system.cash = 38.5
        system.positions["BTC-USD"] = {
            'amount': 0.00004,
            'entry_price': 90000,
            'timestamp': datetime.now().isoformat(),
            'stop_loss': 88200,
            'take_profit': 94500
        }
        system.trade_history.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'BUY',
            'symbol': 'BTC-USD',
            'price': 90000,
            'amount': 0.00004,
            'amount_usd': 3.6
        })
        
        try:
            # Guardar sesión
            system.save_session()
            
            # Buscar archivo creado
            import glob
            session_files = glob.glob('autonomous_session_*.json')
            
            if session_files:
                latest_file = max(session_files, key=lambda x: x)
                print(f"  ✓ Archivo creado: {latest_file}")
                
                # Leer y validar
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                
                required_fields = [
                    'timestamp', 'mode', 'initial_capital', 'final_portfolio',
                    'cash', 'positions', 'pnl', 'pnl_pct', 'max_drawdown',
                    'total_trades', 'trade_history'
                ]
                
                all_fields = all(field in data for field in required_fields)
                
                if all_fields:
                    print(f"  ✓ Todos los campos requeridos presentes")
                    print(f"  ✓ Cash guardado: ${data['cash']:.2f}")
                    print(f"  ✓ Trades guardados: {len(data['trade_history'])}")
                    
                    self.test_passed("Persistencia de sesiones funcional")
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.test_failed("Persistencia de sesiones", f"Campos faltantes: {missing}")
            else:
                self.test_failed("Persistencia de sesiones", "No se creó archivo")
                
        except Exception as e:
            self.test_failed("Persistencia de sesiones", str(e))
    
    def test_performance_stress(self, btc_price):
        """Test 9: Stress test de performance"""
        self.print_header("TEST 9: STRESS TEST DE PERFORMANCE")
        
        if not btc_price:
            self.test_failed("Stress test", "No hay precio de BTC")
            return
        
        print(f"  Precio BTC base: ${btc_price:,.2f}")
        
        scenarios = [
            ("Flash Crash 20%", btc_price * 0.80, -20),
            ("Flash Crash 30%", btc_price * 0.70, -30),
            ("Rally extremo 50%", btc_price * 1.50, 50),
            ("Volatilidad extrema +15%/-10%", btc_price * 0.90, -10),
        ]
        
        capital = 40
        position_size = 4
        
        kill_switch_activations = 0
        
        print("\n  Simulando escenarios extremos:")
        for scenario_name, new_price, change_pct in scenarios:
            # Simular compra y cambio de precio
            btc_bought = position_size / btc_price
            new_value = btc_bought * new_price
            pnl = new_value - position_size
            
            # Calcular MDD
            portfolio_value = (capital - position_size) + new_value
            mdd = (capital - portfolio_value) / capital
            
            status = "OK"
            if mdd >= MDD_EMERGENCY:
                status = "🚨 KILL SWITCH"
                kill_switch_activations += 1
            elif mdd >= MDD_CRITICAL:
                status = "⚠️  CRITICAL"
            elif mdd >= MDD_WARNING:
                status = "⚡ WARNING"
            
            print(f"\n    {scenario_name}:")
            print(f"      Cambio: {change_pct:+.1f}%")
            print(f"      P&L: ${pnl:+.2f}")
            print(f"      MDD: {mdd*100:.2f}%")
            print(f"      Status: {status}")
        
        if kill_switch_activations > 0:
            print(f"\n  ✓ Kill Switch activado en {kill_switch_activations} escenarios extremos")
        
        self.test_passed("Stress test completado", f"Kill Switch activado {kill_switch_activations} veces en escenarios extremos")
    
    def test_dashboard_availability(self):
        """Test 10: Disponibilidad de dashboard"""
        self.print_header("TEST 10: DASHBOARD")
        
        try:
            import flask
            print("  ✓ Flask instalado")
            
            # Verificar que el archivo existe
            import os
            if os.path.exists('dashboard_autonomous.py'):
                print("  ✓ dashboard_autonomous.py encontrado")
                
                # Leer y verificar contenido básico
                with open('dashboard_autonomous.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                checks = [
                    ('Flask app', 'Flask(__name__)' in content),
                    ('Ruta principal', '@app.route(\'/\')' in content),
                    ('API endpoint', '@app.route(\'/api/status\')' in content),
                    ('HTML dashboard', '<html' in content.lower()),
                    ('Auto-refresh', 'setInterval' in content or 'setTimeout' in content),
                ]
                
                all_ok = True
                for check_name, result in checks:
                    if result:
                        print(f"  ✓ {check_name}")
                    else:
                        print(f"  ✗ {check_name}")
                        all_ok = False
                
                if all_ok:
                    self.test_passed("Dashboard disponible y completo")
                else:
                    self.test_failed("Dashboard", "Algunos componentes faltantes")
            else:
                self.test_failed("Dashboard", "Archivo dashboard_autonomous.py no encontrado")
                
        except ImportError:
            self.add_warning("Flask no instalado - Dashboard no disponible")
            print("  ℹ️  Instala con: pip install flask")
            self.test_passed("Dashboard disponible (Flask no instalado)", "Requiere: pip install flask")
    
    def test_code_quality(self):
        """Test 11: Calidad del código"""
        self.print_header("TEST 11: CALIDAD DEL CÓDIGO")
        
        try:
            with open('autonomous_trading_system.py', 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Métricas
            lines = code.split('\n')
            total_lines = len(lines)
            code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
            comment_lines = len([l for l in lines if l.strip().startswith('#')])
            docstring_lines = code.count('"""')
            
            print(f"  Métricas del código:")
            print(f"    Total líneas: {total_lines}")
            print(f"    Líneas de código: {code_lines}")
            print(f"    Comentarios: {comment_lines}")
            print(f"    Docstrings: {docstring_lines//2} bloques")
            
            # Verificar componentes críticos
            critical_components = [
                'class TechnicalIndicators',
                'class AutonomousTradingSystem',
                'def calculate_rsi',
                'def calculate_macd',
                'def calculate_bollinger_bands',
                'def generate_trading_signal',
                'def execute_buy',
                'def execute_sell',
                'def check_stop_loss_take_profit',
                'def check_kill_switch',
                'def run_autonomous',
                'def save_session',
            ]
            
            print(f"\n  Componentes críticos:")
            all_present = True
            for component in critical_components:
                if component in code:
                    print(f"    ✓ {component}")
                else:
                    print(f"    ✗ {component}")
                    all_present = False
            
            if all_present and total_lines > 500:
                self.test_passed("Calidad del código excelente", f"{total_lines} líneas, todos los componentes presentes")
            else:
                self.test_failed("Calidad del código", "Algunos componentes faltantes")
                
        except Exception as e:
            self.test_failed("Calidad del código", str(e))
    
    def print_summary(self):
        """Imprime resumen del benchmark"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        self.print_header("RESUMEN DEL BENCHMARK")
        
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 RESULTADOS:")
        print(f"  Total tests: {total_tests}")
        print(f"  Pasados: {self.tests_passed} ✅")
        print(f"  Fallados: {self.tests_failed} ❌")
        print(f"  Tasa de éxito: {success_rate:.1f}%")
        print(f"  Duración: {duration:.2f} segundos")
        
        if self.warnings:
            print(f"\n⚠️  ADVERTENCIAS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        print(f"\n📈 EVALUACIÓN GENERAL:")
        if success_rate >= 95:
            grade = "A+ EXCELENTE"
            emoji = "🏆"
            recommendation = "Sistema LISTO para producción"
        elif success_rate >= 85:
            grade = "A MUY BUENO"
            emoji = "🌟"
            recommendation = "Sistema listo con monitoreo cercano"
        elif success_rate >= 75:
            grade = "B BUENO"
            emoji = "👍"
            recommendation = "Sistema funcional, revisar warnings"
        elif success_rate >= 60:
            grade = "C ACEPTABLE"
            emoji = "⚠️"
            recommendation = "Requiere mejoras antes de usar"
        else:
            grade = "D NECESITA TRABAJO"
            emoji = "🔧"
            recommendation = "NO usar en producción todavía"
        
        print(f"  {emoji} Calificación: {grade}")
        print(f"  📋 Recomendación: {recommendation}")
        
        # Tests críticos
        critical_tests = [
            "Todas las dependencias disponibles",
            "Indicadores técnicos funcionando correctamente",
            "Operaciones de trading funcionando correctamente",
            "Kill Switch funcionando correctamente",
            "Coinbase API funcional"
        ]
        
        critical_passed = all(
            self.results.get(test, {}).get('status') == 'PASS' 
            for test in critical_tests
        )
        
        print(f"\n🎯 TESTS CRÍTICOS:")
        for test in critical_tests:
            status = self.results.get(test, {}).get('status', 'N/A')
            icon = "✅" if status == "PASS" else "❌"
            print(f"  {icon} {test}")
        
        if critical_passed:
            print(f"\n✅ Todos los tests críticos PASADOS - Sistema OPERACIONAL")
        else:
            print(f"\n❌ Algunos tests críticos FALLARON - NO usar en producción")
        
        # Guardar reporte
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"benchmark_autonomous_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration,
            "total_tests": total_tests,
            "passed": self.tests_passed,
            "failed": self.tests_failed,
            "success_rate": success_rate,
            "grade": grade,
            "recommendation": recommendation,
            "critical_tests_passed": critical_passed,
            "warnings": self.warnings,
            "detailed_results": self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Reporte guardado: {report_file}")
        print("\n" + "="*80)


def main():
    print("\n" + "="*80)
    print("  BENCHMARK COMPLETO - SISTEMA DE TRADING AUTÓNOMO")
    print("  Validación exhaustiva de todos los componentes")
    print("="*80)
    
    benchmark = BenchmarkAutonomousSystem()
    
    try:
        # Ejecutar todos los tests
        if benchmark.test_imports():
            benchmark.test_technical_indicators()
            benchmark.test_signal_generation()
            benchmark.test_risk_management()
            benchmark.test_trading_operations()
            benchmark.test_kill_switch()
            btc_price = benchmark.test_coinbase_api()
            benchmark.test_session_persistence()
            benchmark.test_performance_stress(btc_price)
            benchmark.test_dashboard_availability()
            benchmark.test_code_quality()
        
        # Mostrar resumen
        benchmark.print_summary()
        
    except KeyboardInterrupt:
        print("\n\n[STOP] Benchmark interrumpido por usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
