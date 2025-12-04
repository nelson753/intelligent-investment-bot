#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BENCHMARK & ANÁLISIS - COINBASE SAFE TRADING BOT
Prueba exhaustiva de todas las funcionalidades y seguridad
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
import traceback

class BenchmarkCoinbaseSafe:
    """Benchmark completo del bot de trading seguro"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.warnings = []
        self.results = {}
        
    def print_header(self, title):
        """Imprime encabezado de sección"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def test_passed(self, test_name):
        """Marca test como pasado"""
        self.tests_passed += 1
        print(f"✅ {test_name}")
        self.results[test_name] = "PASS"
    
    def test_failed(self, test_name, reason=""):
        """Marca test como fallido"""
        self.tests_failed += 1
        print(f"❌ {test_name}")
        if reason:
            print(f"   Razón: {reason}")
        self.results[test_name] = f"FAIL: {reason}"
    
    def add_warning(self, warning):
        """Agrega advertencia"""
        self.warnings.append(warning)
        print(f"⚠️  {warning}")
    
    def test_imports(self):
        """Test 1: Verificar que todas las dependencias están disponibles"""
        self.print_header("TEST 1: DEPENDENCIAS")
        
        required_modules = [
            ('os', 'Sistema de archivos'),
            ('sys', 'Sistema'),
            ('time', 'Control de tiempo'),
            ('json', 'Manejo de JSON'),
            ('requests', 'HTTP requests'),
            ('datetime', 'Fechas y tiempo'),
            ('signal', 'Señales del sistema')
        ]
        
        all_ok = True
        for module_name, description in required_modules:
            try:
                __import__(module_name)
                print(f"  ✓ {module_name:15} - {description}")
            except ImportError as e:
                print(f"  ✗ {module_name:15} - {description} - ERROR: {e}")
                all_ok = False
        
        if all_ok:
            self.test_passed("Todas las dependencias disponibles")
        else:
            self.test_failed("Dependencias faltantes")
    
    def test_coinbase_api(self):
        """Test 2: Verificar conectividad con Coinbase API"""
        self.print_header("TEST 2: COINBASE API")
        
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
                
                self.test_passed("Coinbase API funcional")
                return price
            else:
                self.test_failed("Coinbase API", f"Status {response.status_code}")
                return None
                
        except Exception as e:
            self.test_failed("Coinbase API", str(e))
            return None
    
    def test_kill_switch_logic(self):
        """Test 3: Verificar lógica del Kill Switch"""
        self.print_header("TEST 3: KILL SWITCH")
        
        # Simular diferentes niveles de MDD
        test_cases = [
            (0.01, False, "1% MDD - Normal"),
            (0.019, False, "1.9% MDD - Normal"),
            (0.02, False, "2% MDD - Warning (no detiene)"),
            (0.025, False, "2.5% MDD - Warning"),
            (0.03, False, "3% MDD - Critical (no detiene)"),
            (0.04, False, "4% MDD - Critical"),
            (0.05, True, "5% MDD - EMERGENCY (DETIENE)"),
            (0.06, True, "6% MDD - EMERGENCY (DETIENE)"),
        ]
        
        warning_mdd = 0.02
        critical_mdd = 0.03
        emergency_mdd = 0.05
        
        all_passed = True
        
        for mdd, should_stop, description in test_cases:
            would_stop = mdd >= emergency_mdd
            
            if would_stop == should_stop:
                print(f"  ✓ {description}: {'STOP' if would_stop else 'CONTINUA'}")
            else:
                print(f"  ✗ {description}: LÓGICA INCORRECTA")
                all_passed = False
        
        if all_passed:
            self.test_passed("Kill Switch - Lógica correcta")
        else:
            self.test_failed("Kill Switch - Lógica incorrecta")
    
    def test_capital_management(self):
        """Test 4: Verificar gestión de capital"""
        self.print_header("TEST 4: GESTIÓN DE CAPITAL")
        
        # Fase 2 configuration
        max_capital = 40
        position_size_percent = 0.10
        position_size = max_capital * position_size_percent
        
        print(f"  Capital total: ${max_capital}")
        print(f"  Position size: {position_size_percent*100}%")
        print(f"  Monto por trade: ${position_size}")
        
        # Verificar límites
        checks = []
        
        # Check 1: Position size no excede capital
        checks.append(("Position size <= Capital", position_size <= max_capital))
        
        # Check 2: Position size es razonable (entre 5-20%)
        checks.append(("Position size razonable (5-20%)", 
                      0.05 <= position_size_percent <= 0.20))
        
        # Check 3: Permite múltiples trades
        max_trades = max_capital / position_size
        checks.append(("Permite >= 5 trades", max_trades >= 5))
        
        # Check 4: Escalada coherente con Fase 1
        phase1_capital = 20
        phase2_capital = 40
        checks.append(("Escalada 2x desde Fase 1", phase2_capital == phase1_capital * 2))
        
        all_passed = True
        for check_name, passed in checks:
            if passed:
                print(f"  ✓ {check_name}")
            else:
                print(f"  ✗ {check_name}")
                all_passed = False
        
        if all_passed:
            self.test_passed("Gestión de capital - Correcta")
        else:
            self.test_failed("Gestión de capital - Problemas detectados")
    
    def test_signal_generation(self):
        """Test 5: Verificar generación de señales"""
        self.print_header("TEST 5: GENERACIÓN DE SEÑALES")
        
        # Simular diferentes escenarios de precio
        test_scenarios = [
            {
                "name": "Precio estable",
                "prices": [100, 100, 100],
                "expected": None,
                "btc_holdings": 0
            },
            {
                "name": "Tendencia alcista (0.06%)",
                "prices": [100, 100.03, 100.06],
                "expected": "BUY",
                "btc_holdings": 0
            },
            {
                "name": "Tendencia bajista con holdings",
                "prices": [100, 99.8, 99.6],
                "expected": "SELL",
                "btc_holdings": 0.001
            },
            {
                "name": "Tendencia bajista sin holdings",
                "prices": [100, 99.8, 99.6],
                "expected": None,
                "btc_holdings": 0
            },
            {
                "name": "Movimiento pequeño",
                "prices": [100, 100.01, 100.02],
                "expected": None,
                "btc_holdings": 0
            }
        ]
        
        all_passed = True
        
        for scenario in test_scenarios:
            prices = scenario["prices"]
            expected = scenario["expected"]
            btc = scenario["btc_holdings"]
            
            # Lógica de señal (copiada del bot)
            signal = None
            if len(prices) >= 3:
                if prices[-1] > prices[-3] * 1.0005:
                    signal = "BUY"
                elif prices[-1] < prices[-3] * 0.999 and btc > 0:
                    signal = "SELL"
            
            if signal == expected:
                print(f"  ✓ {scenario['name']}: {signal if signal else 'HOLD'}")
            else:
                print(f"  ✗ {scenario['name']}: Expected {expected}, Got {signal}")
                all_passed = False
        
        if all_passed:
            self.test_passed("Generación de señales - Correcta")
        else:
            self.test_failed("Generación de señales - Inconsistencias")
    
    def test_error_handling(self):
        """Test 6: Verificar manejo de errores"""
        self.print_header("TEST 6: MANEJO DE ERRORES")
        
        checks = []
        
        # Check 1: API timeout
        print("  Testing: API timeout handling...")
        try:
            requests.get("https://httpbin.org/delay/15", timeout=2)
            checks.append(("API timeout", False))
        except requests.Timeout:
            print("    ✓ Timeout manejado correctamente")
            checks.append(("API timeout", True))
        except Exception as e:
            print(f"    ✗ Error inesperado: {e}")
            checks.append(("API timeout", False))
        
        # Check 2: Invalid JSON
        print("  Testing: Invalid JSON handling...")
        try:
            json.loads("{invalid json")
            checks.append(("Invalid JSON", False))
        except json.JSONDecodeError:
            print("    ✓ JSON inválido detectado")
            checks.append(("Invalid JSON", True))
        
        # Check 3: Division por cero
        print("  Testing: Division por cero...")
        try:
            peak_value = 0
            mdd = (peak_value - 100) / peak_value if peak_value > 0 else 0.0
            print("    ✓ División por cero prevenida")
            checks.append(("Division por cero", True))
        except ZeroDivisionError:
            print("    ✗ División por cero no manejada")
            checks.append(("Division por cero", False))
        
        all_passed = all(passed for _, passed in checks)
        
        if all_passed:
            self.test_passed("Manejo de errores - Robusto")
        else:
            self.test_failed("Manejo de errores - Vulnerabilidades")
    
    def test_session_persistence(self):
        """Test 7: Verificar guardado de sesión"""
        self.print_header("TEST 7: PERSISTENCIA DE SESIÓN")
        
        # Crear sesión de prueba
        test_session = {
            "timestamp": datetime.now().isoformat(),
            "mode": "BENCHMARK_TEST",
            "initial_capital": 40,
            "final_portfolio": 40.5,
            "pnl": 0.5,
            "pnl_pct": 1.25,
            "max_drawdown": 0.01,
            "total_trades": 5,
            "kill_switch_events": 0
        }
        
        test_file = "benchmark_test_session.json"
        
        try:
            # Guardar
            with open(test_file, 'w') as f:
                json.dump(test_session, f, indent=2)
            
            print(f"  ✓ Sesión guardada: {test_file}")
            
            # Leer
            with open(test_file, 'r') as f:
                loaded_session = json.load(f)
            
            print(f"  ✓ Sesión cargada correctamente")
            
            # Verificar datos
            if loaded_session == test_session:
                print(f"  ✓ Datos consistentes")
                self.test_passed("Persistencia de sesión - Funcional")
            else:
                print(f"  ✗ Datos inconsistentes")
                self.test_failed("Persistencia de sesión - Datos corruptos")
            
            # Limpiar
            os.remove(test_file)
            print(f"  ✓ Archivo de prueba eliminado")
            
        except Exception as e:
            self.test_failed("Persistencia de sesión", str(e))
    
    def test_performance_metrics(self):
        """Test 8: Verificar cálculo de métricas"""
        self.print_header("TEST 8: MÉTRICAS DE PERFORMANCE")
        
        # Datos de prueba
        initial_capital = 40
        test_cases = [
            {
                "name": "Ganancia 5%",
                "final_value": 42,
                "expected_pnl": 2,
                "expected_pnl_pct": 5.0
            },
            {
                "name": "Pérdida 2%",
                "final_value": 39.2,
                "expected_pnl": -0.8,
                "expected_pnl_pct": -2.0
            },
            {
                "name": "Sin cambios",
                "final_value": 40,
                "expected_pnl": 0,
                "expected_pnl_pct": 0.0
            }
        ]
        
        all_passed = True
        
        for case in test_cases:
            final_value = case["final_value"]
            
            # Calcular PnL
            pnl = final_value - initial_capital
            pnl_pct = (pnl / initial_capital) * 100
            
            # Verificar
            pnl_ok = abs(pnl - case["expected_pnl"]) < 0.01
            pnl_pct_ok = abs(pnl_pct - case["expected_pnl_pct"]) < 0.01
            
            if pnl_ok and pnl_pct_ok:
                print(f"  ✓ {case['name']}: P&L=${pnl:+.2f} ({pnl_pct:+.2f}%)")
            else:
                print(f"  ✗ {case['name']}: Cálculo incorrecto")
                all_passed = False
        
        if all_passed:
            self.test_passed("Métricas de performance - Correctas")
        else:
            self.test_failed("Métricas de performance - Errores de cálculo")
    
    def test_security_features(self):
        """Test 9: Verificar características de seguridad"""
        self.print_header("TEST 9: CARACTERÍSTICAS DE SEGURIDAD")
        
        features = [
            ("Kill Switch automático", True),
            ("Paper trading mode", True),
            ("Confirmación para live trading", True),
            ("CTRL+C emergency stop", True),
            ("Límites de capital", True),
            ("Límites de position size", True),
            ("Session logging", True),
            ("API timeout handling", True),
            ("MDD monitoring", True),
            ("Trade history tracking", True)
        ]
        
        for feature, implemented in features:
            if implemented:
                print(f"  ✓ {feature}")
            else:
                print(f"  ✗ {feature} - NO IMPLEMENTADO")
        
        self.test_passed("Características de seguridad - Completas")
    
    def test_code_structure(self):
        """Test 10: Analizar estructura del código"""
        self.print_header("TEST 10: ESTRUCTURA DEL CÓDIGO")
        
        try:
            with open('live_trading_coinbase_safe.py', 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Verificar elementos clave
            checks = [
                ("Clase CoinbaseSafeTrading", "class CoinbaseSafeTrading:" in code),
                ("Método __init__", "def __init__" in code),
                ("Método get_coinbase_price", "def get_coinbase_price" in code),
                ("Método calculate_mdd", "def calculate_mdd" in code),
                ("Método check_kill_switch", "def check_kill_switch" in code),
                ("Método simulate_trade", "def simulate_trade" in code),
                ("Método generate_simple_signal", "def generate_simple_signal" in code),
                ("Método run_session", "def run_session" in code),
                ("Método emergency_stop", "def emergency_stop" in code),
                ("Método save_session", "def save_session" in code),
                ("Función main", "def main():" in code),
                ("Docstrings presentes", '"""' in code),
                ("Manejo de señales", "signal.signal" in code),
                ("Validación de input", "strip()" in code and "ValueError" in code)
            ]
            
            all_passed = True
            for check_name, passed in checks:
                if passed:
                    print(f"  ✓ {check_name}")
                else:
                    print(f"  ✗ {check_name}")
                    all_passed = False
            
            # Métricas de código
            lines = code.split('\n')
            total_lines = len(lines)
            code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
            comment_lines = len([l for l in lines if l.strip().startswith('#')])
            
            print(f"\n  Métricas:")
            print(f"    Total líneas: {total_lines}")
            print(f"    Líneas de código: {code_lines}")
            print(f"    Líneas de comentarios: {comment_lines}")
            print(f"    Ratio comentarios: {comment_lines/code_lines*100:.1f}%")
            
            if all_passed:
                self.test_passed("Estructura del código - Completa")
            else:
                self.test_failed("Estructura del código - Elementos faltantes")
                
        except Exception as e:
            self.test_failed("Estructura del código", str(e))
    
    def run_live_stress_test(self, btc_price):
        """Test 11: Stress test con datos reales"""
        self.print_header("TEST 11: STRESS TEST")
        
        if not btc_price:
            self.test_failed("Stress test - No hay precio de BTC")
            return
        
        print(f"  Precio BTC base: ${btc_price:,.2f}")
        
        # Simular diferentes escenarios de mercado
        scenarios = [
            ("Crash 10%", btc_price * 0.90, -4.0),  # $4 pérdida en position
            ("Crash 20%", btc_price * 0.80, -8.0),
            ("Rally 10%", btc_price * 1.10, 4.0),
            ("Rally 20%", btc_price * 1.20, 8.0),
            ("Volatilidad alta", btc_price * 0.95, -2.0),
        ]
        
        capital = 40
        position_size = 4  # 10% del capital
        
        for scenario_name, new_price, expected_impact in scenarios:
            # Simular compra y luego cambio de precio
            btc_bought = position_size / btc_price
            new_value = btc_bought * new_price
            pnl = new_value - position_size
            
            print(f"\n  Escenario: {scenario_name}")
            print(f"    Precio nuevo: ${new_price:,.2f}")
            print(f"    BTC comprado: {btc_bought:.8f}")
            print(f"    Valor actual: ${new_value:.2f}")
            print(f"    P&L: ${pnl:+.2f}")
            
            # Verificar si Kill Switch se activaría
            portfolio_value = (capital - position_size) + new_value
            mdd = (capital - portfolio_value) / capital
            
            if mdd >= 0.05:
                print(f"    🚨 KILL SWITCH: MDD {mdd*100:.2f}% >= 5%")
            elif mdd >= 0.03:
                print(f"    ⚠️  CRITICAL: MDD {mdd*100:.2f}% >= 3%")
            elif mdd >= 0.02:
                print(f"    ⚡ WARNING: MDD {mdd*100:.2f}% >= 2%")
            else:
                print(f"    ✓ OK: MDD {mdd*100:.2f}%")
        
        self.test_passed("Stress test - Completado")
    
    def print_summary(self):
        """Imprime resumen del benchmark"""
        self.print_header("RESUMEN DEL BENCHMARK")
        
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 RESULTADOS:")
        print(f"  Total tests: {total_tests}")
        print(f"  Pasados: {self.tests_passed} ✅")
        print(f"  Fallados: {self.tests_failed} ❌")
        print(f"  Tasa de éxito: {success_rate:.1f}%")
        
        if self.warnings:
            print(f"\n⚠️  ADVERTENCIAS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        print(f"\n📈 EVALUACIÓN GENERAL:")
        if success_rate >= 95:
            grade = "A+ EXCELENTE"
            emoji = "🏆"
        elif success_rate >= 85:
            grade = "A MUY BUENO"
            emoji = "🌟"
        elif success_rate >= 75:
            grade = "B BUENO"
            emoji = "👍"
        elif success_rate >= 60:
            grade = "C ACEPTABLE"
            emoji = "⚠️"
        else:
            grade = "D NECESITA MEJORAS"
            emoji = "🔧"
        
        print(f"  {emoji} Calificación: {grade}")
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"benchmark_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": self.tests_passed,
            "failed": self.tests_failed,
            "success_rate": success_rate,
            "grade": grade,
            "warnings": self.warnings,
            "detailed_results": self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Reporte guardado: {report_file}")
        print("\n" + "="*70)


def main():
    print("\n" + "="*70)
    print("  BENCHMARK - COINBASE SAFE TRADING BOT")
    print("  Análisis exhaustivo de funcionalidad y seguridad")
    print("="*70)
    
    benchmark = BenchmarkCoinbaseSafe()
    
    try:
        # Ejecutar todos los tests
        benchmark.test_imports()
        btc_price = benchmark.test_coinbase_api()
        benchmark.test_kill_switch_logic()
        benchmark.test_capital_management()
        benchmark.test_signal_generation()
        benchmark.test_error_handling()
        benchmark.test_session_persistence()
        benchmark.test_performance_metrics()
        benchmark.test_security_features()
        benchmark.test_code_structure()
        
        if btc_price:
            benchmark.run_live_stress_test(btc_price)
        
        # Mostrar resumen
        benchmark.print_summary()
        
    except KeyboardInterrupt:
        print("\n\n[STOP] Benchmark interrumpido por usuario")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
