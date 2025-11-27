#!/usr/bin/env python3
"""
🧪 TEST INQUEBRANTABLE 1: Multi-level Kill Switch + Circuit Breaker

Valida los 3 niveles de protección de capital:
- WARNING (3% MDD): Reduce position size 50%
- CRITICAL (5% MDD): Cierra posiciones + Circuit Breaker 1h
- EMERGENCY (8% MDD): Shutdown completo
"""

import pytest
import sys
from datetime import datetime, timedelta
from intelligent_investment_bot import (
    RiskManager, 
    MarketEnvironment, 
    TRADING_CONFIG,
    RISK_CONFIG
)

class TestInquebrantable1:
    """Suite de tests para Multi-level Kill Switch"""
    
    def test_risk_config_levels(self):
        """Verifica que los 3 niveles estén configurados correctamente"""
        assert RISK_CONFIG["warning_drawdown_threshold"] == 0.03  # 3%
        assert RISK_CONFIG["max_drawdown_threshold"] == 0.05      # 5%
        assert RISK_CONFIG["emergency_drawdown_threshold"] == 0.08 # 8%
        assert RISK_CONFIG["circuit_breaker_cooldown"] == 3600    # 1 hora
        print("[OK] Niveles de Kill Switch correctos: 3%, 5%, 8%")
    
    def test_warning_level_3_percent(self):
        """WARNING level (3% MDD) debe reducir position size pero no detener bot"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Simular pérdida del 3.5% (WARNING level)
        initial = TRADING_CONFIG["initial_capital"]
        env.portfolio_value = initial * 0.965  # -3.5%
        env.peak_value = initial
        env.price_history = [100, 95]  # Datos para MDD
        
        diagnosis = risk_mgr.analyze_risk(env)
        
        assert diagnosis["diagnosis"] == "WARNING"
        assert diagnosis["risk_level"] == "WARNING"
        assert risk_mgr.current_risk_level == "WARNING"
        assert not risk_mgr.kill_switch_active  # Bot sigue activo
        assert risk_mgr.circuit_breaker_until is None  # Sin circuit breaker
        print("[OK] WARNING level (3%) funciona: bot activo, position reducida")
    
    def test_critical_level_5_percent(self):
        """CRITICAL level (5% MDD) debe cerrar posiciones + activar Circuit Breaker"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Simular pérdida del 5.5% (CRITICAL level)
        initial = TRADING_CONFIG["initial_capital"]
        env.portfolio_value = initial * 0.945  # -5.5%
        env.peak_value = initial
        env.price_history = [100, 94]
        env.current_position = 0.5  # Simular posición abierta
        env.cash = initial * 0.5
        
        diagnosis = risk_mgr.analyze_risk(env)
        
        assert diagnosis["diagnosis"] == "CRITICAL"
        assert diagnosis["risk_level"] == "CRITICAL"
        assert risk_mgr.kill_switch_active  # Bot detenido
        assert risk_mgr.circuit_breaker_until is not None  # Circuit Breaker activo
        
        # Verificar que Circuit Breaker dura ~1 hora
        cooldown = (risk_mgr.circuit_breaker_until - datetime.now()).total_seconds()
        assert 3595 <= cooldown <= 3605  # ~3600 segundos ±5s
        
        print("[OK] CRITICAL level (5%) funciona: Kill Switch + Circuit Breaker 1h")
    
    def test_emergency_level_8_percent(self):
        """EMERGENCY level (8% MDD) debe hacer shutdown completo"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Simular pérdida del 8.5% (EMERGENCY level)
        initial = TRADING_CONFIG["initial_capital"]
        env.portfolio_value = initial * 0.915  # -8.5%
        env.peak_value = initial
        env.price_history = [100, 91]
        env.current_position = 0.5
        env.cash = initial * 0.5
        
        diagnosis = risk_mgr.analyze_risk(env)
        
        assert diagnosis["diagnosis"] == "EMERGENCY"
        assert diagnosis["risk_level"] == "EMERGENCY"
        assert risk_mgr.kill_switch_active  # Bot completamente detenido
        assert risk_mgr.circuit_breaker_until is not None  # Circuit Breaker extendido
        
        print("[OK] EMERGENCY level (8%) funciona: Shutdown completo")
    
    def test_circuit_breaker_blocks_trades(self):
        """Circuit Breaker debe bloquear TODOS los trades durante cooldown"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Activar Circuit Breaker manualmente
        risk_mgr.circuit_breaker_until = datetime.now() + timedelta(seconds=10)
        
        # Intentar trade BUY
        can_buy = risk_mgr.should_allow_trade(env, action=0)
        assert not can_buy  # Bloqueado por Circuit Breaker
        
        # Intentar trade SELL
        can_sell = risk_mgr.should_allow_trade(env, action=1)
        assert not can_sell  # Bloqueado por Circuit Breaker
        
        print("[OK] Circuit Breaker bloquea todos los trades")
    
    def test_circuit_breaker_auto_deactivation(self):
        """Circuit Breaker debe desactivarse automáticamente después del cooldown"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Activar Circuit Breaker con 1 segundo de cooldown
        risk_mgr.circuit_breaker_until = datetime.now() + timedelta(seconds=0.5)
        risk_mgr.kill_switch_active = True
        
        # Trades bloqueados durante cooldown
        assert not risk_mgr.should_allow_trade(env, action=0)
        
        # Esperar que expire
        import time
        time.sleep(0.6)
        
        # Verificar que se desactivó automáticamente
        can_trade = risk_mgr.should_allow_trade(env, action=0)
        assert can_trade  # Desbloqueado
        assert risk_mgr.circuit_breaker_until is None
        assert not risk_mgr.kill_switch_active
        assert risk_mgr.current_risk_level == "OK"
        
        print("[OK] Circuit Breaker se desactiva automáticamente")
    
    def test_warning_reduces_position_size(self):
        """WARNING level debe reducir position size al 50%"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Activar WARNING level
        risk_mgr.current_risk_level = "WARNING"
        
        # Position size normal: 8%
        normal_max = TRADING_CONFIG["position_size_percent"]
        
        # Simular posición del 5% (debería permitir)
        env.current_position = 0.5
        env.price_history = [100]
        env.portfolio_value = 1000
        env.cash = 500
        
        # Position value = 0.5 * 100 = 50 (5% de 1000)
        # WARNING reduce max position a 4% (8% / 2)
        # 50/1000 = 5% > 4% → NO debería permitir
        can_buy = risk_mgr.should_allow_trade(env, action=0)
        assert not can_buy  # Bloqueado por position size reducido
        
        print("[OK] WARNING reduce position size al 50%")
    
    def test_risk_events_logging(self):
        """Verificar que eventos de riesgo se registran para AI 4"""
        env = MarketEnvironment()
        risk_mgr = RiskManager()
        
        # Simular CRITICAL level
        initial = TRADING_CONFIG["initial_capital"]
        env.portfolio_value = initial * 0.94  # -6%
        env.peak_value = initial
        env.price_history = [100]
        env.current_position = 0
        
        # Debe crear evento en risk_events
        initial_events = len(risk_mgr.risk_events)
        risk_mgr.analyze_risk(env)
        
        assert len(risk_mgr.risk_events) > initial_events
        
        # Verificar estructura del evento
        event = risk_mgr.risk_events[-1]
        assert "timestamp" in event
        assert "trigger" in event
        assert event["trigger"] == "CRITICAL"
        assert "portfolio_value" in event
        assert "circuit_breaker_until" in event
        
        print("[OK] Eventos de riesgo se registran correctamente para AI 4")

def run_all_tests():
    """Ejecuta todos los tests y muestra resultados"""
    print("\n" + "="*70)
    print("TEST VALIDACION INQUEBRANTABLE 1: Multi-level Kill Switch")
    print("="*70 + "\n")
    
    suite = TestInquebrantable1()
    tests = [
        ("Configuración de niveles", suite.test_risk_config_levels),
        ("WARNING level (3% MDD)", suite.test_warning_level_3_percent),
        ("CRITICAL level (5% MDD)", suite.test_critical_level_5_percent),
        ("EMERGENCY level (8% MDD)", suite.test_emergency_level_8_percent),
        ("Circuit Breaker bloquea trades", suite.test_circuit_breaker_blocks_trades),
        ("Circuit Breaker auto-desactivación", suite.test_circuit_breaker_auto_deactivation),
        ("WARNING reduce position 50%", suite.test_warning_reduces_position_size),
        ("Logging de eventos de riesgo", suite.test_risk_events_logging),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"[OK] {name}")
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {name}: {e}")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {name}: ERROR - {e}")
    
    print("\n" + "="*70)
    print(f"RESULTADOS: {passed}/{len(tests)} tests passed")
    if failed == 0:
        print("INQUEBRANTABLE 1 - VALIDADO AL 100%")
    else:
        print(f"ADVERTENCIA: {failed} tests fallidos - revisar implementacion")
    print("="*70 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
