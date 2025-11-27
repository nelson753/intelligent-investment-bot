#!/usr/bin/env python3
"""
TEST INQUEBRANTABLE 2: Auto-retraining semanal + Detección de régimen

Valida:
- Re-entrenamiento automático cada 7 días
- Detección correcta de régimen de mercado (trending_up/down, lateral, volatile)
- Ajuste de estrategia según régimen detectado
"""

import pytest
import sys
import time
from datetime import datetime, timedelta
import numpy as np
from intelligent_investment_bot import (
    AutoEvolver,
    PPOTradingAgent,
    RiskManager,
    EVOLVER_CONFIG
)

class TestInquebrantable2:
    """Suite de tests para Auto-retraining semanal"""
    
    def test_weekly_retraining_trigger(self):
        """Verifica que se active re-entrenamiento después de 7 días"""
        evolver = AutoEvolver()
        
        # Simular que pasaron 8 días
        evolver.last_training_date = datetime.now() - timedelta(days=8)
        
        should_retrain = evolver.should_trigger_weekly_retraining()
        assert should_retrain == True
        print("[OK] Re-entrenamiento se activa después de 7 días")
    
    def test_no_premature_retraining(self):
        """Verifica que NO se active antes de 7 días"""
        evolver = AutoEvolver()
        
        # Simular que pasaron 5 días
        evolver.last_training_date = datetime.now() - timedelta(days=5)
        
        should_retrain = evolver.should_trigger_weekly_retraining()
        assert should_retrain == False
        print("[OK] NO se activa re-entrenamiento antes de 7 días")
    
    def test_regime_detection_trending_up(self):
        """Detecta régimen trending_up correctamente (+2% en 7 días)"""
        evolver = AutoEvolver()
        
        # Simular precio subiendo +4% en 7 días (0.67% diario)
        base_price = 90000
        price_history = []
        for i in range(7):
            price = base_price * (1.04 ** (i/6))  # Crecimiento exponencial hasta +4%
            price_history.append(price)
        
        regime = evolver.detect_market_regime(price_history)
        total_change = (price_history[-1] - price_history[0]) / price_history[0]
        assert regime == "trending_up", f"Expected trending_up, got {regime}. Change: {total_change*100:.2f}%"
        print(f"[OK] Régimen trending_up detectado: {price_history[0]:.0f} -> {price_history[-1]:.0f}")
    
    def test_regime_detection_trending_down(self):
        """Detecta régimen trending_down correctamente (-2% en 7 días)"""
        evolver = AutoEvolver()
        
        # Simular precio bajando -4% en 7 días (0.67% diario)
        base_price = 90000
        price_history = []
        for i in range(7):
            price = base_price * (0.96 ** (i/6))  # Decrecimiento exponencial hasta -4%
            price_history.append(price)
        
        regime = evolver.detect_market_regime(price_history)
        total_change = (price_history[-1] - price_history[0]) / price_history[0]
        assert regime == "trending_down", f"Expected trending_down, got {regime}. Change: {total_change*100:.2f}%"
        print(f"[OK] Régimen trending_down detectado: {price_history[0]:.0f} -> {price_history[-1]:.0f}")
    
    def test_regime_detection_lateral(self):
        """Detecta régimen lateral correctamente (< 2% cambio)"""
        evolver = AutoEvolver()
        
        # Simular precio lateral (oscila ±0.5%)
        base_price = 90000
        price_history = [base_price * (1 + 0.005 * np.sin(i)) for i in range(7)]
        
        regime = evolver.detect_market_regime(price_history)
        assert regime == "lateral"
        print(f"[OK] Régimen lateral detectado: rango {min(price_history):.0f} - {max(price_history):.0f}")
    
    def test_regime_detection_volatile(self):
        """Detecta régimen volátil correctamente (>10% volatilidad)"""
        evolver = AutoEvolver()
        
        # Simular alta volatilidad
        base_price = 90000
        price_history = [base_price * (1 + 0.15 * (1 if i % 2 == 0 else -1)) for i in range(7)]
        
        regime = evolver.detect_market_regime(price_history)
        assert regime == "volatile"
        print(f"[OK] Régimen volatile detectado: volatilidad extrema")
    
    def test_regime_adjustment_trending_up(self):
        """Verifica ajuste de estrategia para trending_up (más agresivo)"""
        evolver = AutoEvolver()
        ppo_agent = PPOTradingAgent()
        risk_manager = RiskManager()
        
        evolver.market_regime = "trending_up"
        
        # Re-entrenar con régimen trending_up
        evolution = evolver.retrain_with_penalty(ppo_agent, [])
        
        assert evolution["market_regime"] == "trending_up"
        assert evolution["regime_adjustment"]["position_size"] == 1.2  # Más agresivo
        assert evolution["regime_adjustment"]["risk_tolerance"] == 1.1
        print("[OK] Ajuste trending_up: position_size=1.2x, risk_tolerance=1.1x")
    
    def test_regime_adjustment_volatile(self):
        """Verifica ajuste de estrategia para volatile (muy conservador)"""
        evolver = AutoEvolver()
        ppo_agent = PPOTradingAgent()
        
        evolver.market_regime = "volatile"
        
        evolution = evolver.retrain_with_penalty(ppo_agent, [])
        
        assert evolution["market_regime"] == "volatile"
        assert evolution["regime_adjustment"]["position_size"] == 0.6  # Muy conservador
        assert evolution["regime_adjustment"]["risk_tolerance"] == 0.6
        print("[OK] Ajuste volatile: position_size=0.6x, risk_tolerance=0.6x")
    
    def test_training_date_update(self):
        """Verifica que se actualice fecha de último entrenamiento"""
        evolver = AutoEvolver()
        ppo_agent = PPOTradingAgent()
        
        old_date = evolver.last_training_date
        time.sleep(0.1)  # Pequeña pausa
        
        evolver.retrain_with_penalty(ppo_agent, [])
        
        new_date = evolver.last_training_date
        assert new_date > old_date
        print(f"[OK] Fecha de entrenamiento actualizada: {old_date} -> {new_date}")
    
    def test_evolution_history_logging(self):
        """Verifica que se registren eventos de evolución"""
        evolver = AutoEvolver()
        ppo_agent = PPOTradingAgent()
        
        initial_count = len(evolver.evolution_history)
        
        evolver.retrain_with_penalty(ppo_agent, [])
        
        assert len(evolver.evolution_history) == initial_count + 1
        
        last_evolution = evolver.evolution_history[-1]
        assert "timestamp" in last_evolution
        assert "market_regime" in last_evolution
        assert "regime_adjustment" in last_evolution
        print("[OK] Eventos de evolución registrados correctamente")

def run_all_tests():
    """Ejecuta todos los tests y muestra resultados"""
    print("\n" + "="*70)
    print("TEST VALIDACION INQUEBRANTABLE 2: Auto-retraining semanal")
    print("="*70 + "\n")
    
    suite = TestInquebrantable2()
    tests = [
        ("Re-entrenamiento después de 7 días", suite.test_weekly_retraining_trigger),
        ("NO re-entrenar antes de 7 días", suite.test_no_premature_retraining),
        ("Detección trending_up", suite.test_regime_detection_trending_up),
        ("Detección trending_down", suite.test_regime_detection_trending_down),
        ("Detección lateral", suite.test_regime_detection_lateral),
        ("Detección volatile", suite.test_regime_detection_volatile),
        ("Ajuste para trending_up", suite.test_regime_adjustment_trending_up),
        ("Ajuste para volatile", suite.test_regime_adjustment_volatile),
        ("Actualización de fecha", suite.test_training_date_update),
        ("Logging de evoluciones", suite.test_evolution_history_logging),
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
        print("INQUEBRANTABLE 2 - VALIDADO AL 100%")
    else:
        print(f"ADVERTENCIA: {failed} tests fallidos")
    print("="*70 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
