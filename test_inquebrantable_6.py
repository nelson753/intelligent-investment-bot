#!/usr/bin/env python3
"""
TEST INQUEBRANTABLE 6: Cross-validation Anti-overfitting

Valida:
- Split correcto de datos (60/20/20)
- Detección de overfitting (test < 80% train)
- Walk-forward analysis con ventanas móviles
- Registro de validaciones
"""

import pytest
import sys
import numpy as np
from datetime import datetime
from intelligent_investment_bot import (
    CrossValidator,
    PPOTradingAgent,
    MarketEnvironment
)

class TestInquebrantable6:
    """Suite de tests para Cross-validation"""
    
    def test_data_split_60_20_20(self):
        """Verifica split correcto de datos (60% train, 20% val, 20% test)"""
        validator = CrossValidator()
        
        # Crear dataset de 100 elementos
        data = list(range(100))
        
        train, val, test = validator.split_data(data, train_pct=0.6, val_pct=0.2, test_pct=0.2)
        
        assert len(train) == 60
        assert len(val) == 20
        assert len(test) == 20
        assert len(train) + len(val) + len(test) == 100
        print(f"[OK] Split correcto: Train={len(train)}, Val={len(val)}, Test={len(test)}")
    
    def test_data_split_no_overlap(self):
        """Verifica que no haya overlap entre train/val/test"""
        validator = CrossValidator()
        
        data = list(range(100))
        train, val, test = validator.split_data(data)
        
        # Verificar que sean secuenciales sin overlap
        assert train[-1] < val[0]
        assert val[-1] < test[0]
        print("[OK] NO hay overlap entre train/val/test")
    
    def test_overfitting_detection_positive(self):
        """Detecta overfitting cuando test << train"""
        validator = CrossValidator()
        
        # Simular buen performance en train, malo en test
        train_perf = {
            "avg_reward": 100,
            "avg_return": 0.10,  # 10% return
            "sharpe_ratio": 1.5
        }
        
        test_perf = {
            "avg_reward": 20,
            "avg_return": 0.02,  # 2% return (20% de train)
            "sharpe_ratio": 0.3
        }
        
        is_overfitted = validator.detect_overfitting(train_perf, test_perf, threshold=0.8)
        
        assert is_overfitted == True
        assert len(validator.overfitting_alerts) > 0
        print("[OK] Overfitting detectado correctamente (test=20% de train)")
    
    def test_no_overfitting_detection(self):
        """NO detecta overfitting cuando test >= 80% train"""
        validator = CrossValidator()
        
        # Simular performance similar en train y test
        train_perf = {
            "avg_reward": 100,
            "avg_return": 0.10,  # 10%
            "sharpe_ratio": 1.5
        }
        
        test_perf = {
            "avg_reward": 90,
            "avg_return": 0.09,  # 9% (90% de train)
            "sharpe_ratio": 1.4
        }
        
        is_overfitted = validator.detect_overfitting(train_perf, test_perf, threshold=0.8)
        
        assert is_overfitted == False
        print("[OK] NO overfitting: test=90% de train (>80% threshold)")
    
    def test_overfitting_with_negative_returns(self):
        """Maneja correctamente returns negativos"""
        validator = CrossValidator()
        
        # Train con pérdidas pequeñas, test con pérdidas grandes
        train_perf = {
            "avg_return": -0.02,  # -2%
        }
        
        test_perf = {
            "avg_return": -0.05,  # -5% (peor que train)
        }
        
        is_overfitted = validator.detect_overfitting(train_perf, test_perf)
        
        # Con returns negativos, test peor → overfitting
        assert is_overfitted == True
        print("[OK] Overfitting detectado con returns negativos")
    
    def test_overfitting_alert_structure(self):
        """Verifica estructura de alertas de overfitting"""
        validator = CrossValidator()
        
        train_perf = {"avg_return": 0.10}
        test_perf = {"avg_return": 0.02}
        
        validator.detect_overfitting(train_perf, test_perf)
        
        alert = validator.overfitting_alerts[-1]
        assert "timestamp" in alert
        assert "train_return" in alert
        assert "test_return" in alert
        assert "ratio" in alert
        assert "action" in alert
        assert alert["action"] == "re-training_required"
        print("[OK] Estructura de alerta correcta")
    
    def test_walk_forward_window_size(self):
        """Verifica tamaño de ventanas en walk-forward analysis"""
        validator = CrossValidator()
        ppo_agent = PPOTradingAgent()
        
        # Crear historial de precios de 40 días
        price_history = [90000 * (1 + 0.001 * i) for i in range(40)]
        
        validation = validator.walk_forward_analysis(ppo_agent, price_history, window_size=30)
        
        assert validation["validated"] == True
        assert validation["train_samples"] == 30
        assert validation["test_samples"] == 7
        print(f"[OK] Ventanas walk-forward: Train={validation['train_samples']}, Test={validation['test_samples']}")
    
    def test_walk_forward_insufficient_data(self):
        """Verifica rechazo con datos insuficientes"""
        validator = CrossValidator()
        ppo_agent = PPOTradingAgent()
        
        # Solo 20 días (insuficiente para window_size=30)
        price_history = [90000] * 20
        
        validation = validator.walk_forward_analysis(ppo_agent, price_history, window_size=30)
        
        assert validation["validated"] == False
        assert validation["reason"] == "insufficient_data"
        print("[OK] Rechaza datos insuficientes correctamente")
    
    def test_validation_history_logging(self):
        """Verifica que se registren validaciones"""
        validator = CrossValidator()
        ppo_agent = PPOTradingAgent()
        
        initial_count = len(validator.validation_history)
        
        price_history = [90000 * (1 + 0.001 * i) for i in range(40)]
        validator.walk_forward_analysis(ppo_agent, price_history)
        
        assert len(validator.validation_history) == initial_count + 1
        
        validation = validator.validation_history[-1]
        assert "timestamp" in validation
        assert "window_size" in validation
        assert "validated" in validation
        print("[OK] Validaciones registradas en historial")
    
    def test_performance_evaluation_structure(self):
        """Verifica estructura de evaluación de performance"""
        validator = CrossValidator()
        ppo_agent = PPOTradingAgent()
        env = MarketEnvironment()
        
        # Evaluar (con 1 episodio para rapidez)
        performance = validator.evaluate_performance(ppo_agent, env, num_episodes=1)
        
        assert "avg_reward" in performance
        assert "avg_return" in performance
        assert "std_return" in performance
        assert "sharpe_ratio" in performance
        assert "max_drawdown" in performance
        print("[OK] Estructura de performance correcta")
    
    def test_multiple_overfitting_alerts(self):
        """Verifica registro de múltiples alertas"""
        validator = CrossValidator()
        
        # Generar 3 alertas
        for i in range(3):
            train_perf = {"avg_return": 0.10}
            test_perf = {"avg_return": 0.02 * (i + 1)}  # Varía test performance
            validator.detect_overfitting(train_perf, test_perf)
        
        assert len(validator.overfitting_alerts) >= 2  # Al menos 2 deben ser overfitting
        print(f"[OK] Múltiples alertas registradas: {len(validator.overfitting_alerts)}")
    
    def test_threshold_customization(self):
        """Verifica que se pueda personalizar threshold"""
        validator = CrossValidator()
        
        train_perf = {"avg_return": 0.10}
        test_perf = {"avg_return": 0.07}  # 70% de train
        
        # Con threshold=0.8 → NO overfitting
        is_overfitted_80 = validator.detect_overfitting(train_perf, test_perf, threshold=0.8)
        assert is_overfitted_80 == True  # 70% < 80%
        
        # Con threshold=0.6 → NO overfitting
        is_overfitted_60 = validator.detect_overfitting(train_perf, test_perf, threshold=0.6)
        assert is_overfitted_60 == False  # 70% > 60%
        
        print("[OK] Threshold personalizable: 80% vs 60%")

def run_all_tests():
    """Ejecuta todos los tests y muestra resultados"""
    print("\n" + "="*70)
    print("TEST VALIDACION INQUEBRANTABLE 6: Cross-validation")
    print("="*70 + "\n")
    
    suite = TestInquebrantable6()
    tests = [
        ("Split 60/20/20", suite.test_data_split_60_20_20),
        ("NO overlap entre sets", suite.test_data_split_no_overlap),
        ("Detección de overfitting", suite.test_overfitting_detection_positive),
        ("NO falsos positivos", suite.test_no_overfitting_detection),
        ("Manejo returns negativos", suite.test_overfitting_with_negative_returns),
        ("Estructura de alertas", suite.test_overfitting_alert_structure),
        ("Walk-forward window size", suite.test_walk_forward_window_size),
        ("Rechazo datos insuficientes", suite.test_walk_forward_insufficient_data),
        ("Logging de validaciones", suite.test_validation_history_logging),
        ("Estructura de performance", suite.test_performance_evaluation_structure),
        ("Múltiples alertas", suite.test_multiple_overfitting_alerts),
        ("Threshold personalizable", suite.test_threshold_customization),
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
        print("INQUEBRANTABLE 6 - VALIDADO AL 100%")
    else:
        print(f"ADVERTENCIA: {failed} tests fallidos")
    print("="*70 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
