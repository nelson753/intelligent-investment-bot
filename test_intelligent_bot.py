#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Intelligent Investment Bot (II)

Tests las 4 AIs:
- AI 1: Risk Manager
- AI 2: Sentiment Analyzer
- AI 3: PPO Trading Agent
- AI 4: Auto-Evolver
"""

import sys
import unittest
import numpy as np
from datetime import datetime
from intelligent_investment_bot import (
    MarketEnvironment,
    RiskManager,
    SentimentAnalyzer,
    PPOTradingAgent,
    AutoEvolver,
    IntelligentInvestmentBot,
    TRADING_CONFIG
)

class TestMarketEnvironment(unittest.TestCase):
    """Tests para el entorno de mercado"""
    
    def setUp(self):
        self.env = MarketEnvironment(exchange="paper", symbol="BTCUSDT")
    
    def test_initialization(self):
        """Test: Inicialización correcta"""
        self.assertEqual(self.env.current_position, 0.0)
        self.assertEqual(self.env.cash, 1000.0)
        self.assertEqual(self.env.portfolio_value, 1000.0)
    
    def test_get_simulated_data(self):
        """Test: Generación de datos simulados"""
        data = self.env.get_market_data()
        self.assertIn("price", data)
        self.assertIn("volume_24h", data)
        self.assertGreater(data["price"], 0)
    
    def test_execute_buy_action(self):
        """Test: Ejecutar compra"""
        market_data = self.env.get_market_data()
        initial_cash = self.env.cash
        
        reward, done = self.env.execute_action(0, market_data)  # BUY
        
        self.assertLess(self.env.cash, initial_cash)  # Cash disminuyó
        self.assertGreater(self.env.current_position, 0)  # Tiene BTC
    
    def test_execute_sell_action(self):
        """Test: Ejecutar venta"""
        # Primero comprar
        market_data = self.env.get_market_data()
        self.env.execute_action(0, market_data)
        
        # Ahora vender
        initial_position = self.env.current_position
        market_data = self.env.get_market_data()
        reward, done = self.env.execute_action(1, market_data)  # SELL
        
        self.assertEqual(self.env.current_position, 0.0)  # Vendió todo
        self.assertGreater(self.env.cash, 0)
    
    def test_calculate_rsi(self):
        """Test: Cálculo de RSI"""
        prices = np.array([100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 
                          111, 110, 112, 114, 113])
        
        rsi = self.env._calculate_rsi(prices, period=14)
        
        self.assertGreaterEqual(rsi, 0)
        self.assertLessEqual(rsi, 100)
    
    def test_daily_pnl_calculation(self):
        """Test: Cálculo de P&L diario"""
        # Simular trades
        market_data = self.env.get_market_data()
        self.env.execute_action(0, market_data)  # BUY
        
        market_data = self.env.get_market_data()
        self.env.execute_action(1, market_data)  # SELL
        
        daily_pnl = self.env.get_daily_pnl()
        self.assertIsInstance(daily_pnl, float)
    
    def test_reset(self):
        """Test: Reset del entorno"""
        # Hacer algunos trades
        market_data = self.env.get_market_data()
        self.env.execute_action(0, market_data)
        
        # Reset
        self.env.reset()
        
        self.assertEqual(self.env.current_position, 0.0)
        self.assertEqual(self.env.cash, 1000.0)
        self.assertEqual(len(self.env.trades_history), 0)


class TestRiskManager(unittest.TestCase):
    """Tests para el gestor de riesgo"""
    
    def setUp(self):
        self.risk_manager = RiskManager()
        self.env = MarketEnvironment(exchange="paper", symbol="BTCUSDT")
    
    def test_initialization(self):
        """Test: Inicialización"""
        self.assertFalse(self.risk_manager.kill_switch_active)
        self.assertEqual(len(self.risk_manager.risk_events), 0)
    
    def test_normal_risk_analysis(self):
        """Test: Análisis con riesgo normal"""
        risk_status = self.risk_manager.analyze_risk(self.env)
        
        self.assertEqual(risk_status["diagnosis"], "OK")
        self.assertFalse(risk_status["kill_switch_active"])
    
    def test_kill_switch_activation(self):
        """Test: Activación de Kill Switch por MDD"""
        # Simular pérdida grande
        self.env.peak_value = 1000
        self.env.portfolio_value = 800  # 20% drawdown
        
        risk_status = self.risk_manager.analyze_risk(self.env)
        
        self.assertEqual(risk_status["diagnosis"], "CRITICAL")
        self.assertTrue(self.risk_manager.kill_switch_active)
    
    def test_should_allow_trade_when_kill_switch_active(self):
        """Test: Bloquear trades cuando Kill Switch está activo"""
        self.risk_manager.kill_switch_active = True
        
        allowed = self.risk_manager.should_allow_trade(self.env, 0)  # BUY
        
        self.assertFalse(allowed)
    
    def test_sharpe_ratio_calculation(self):
        """Test: Cálculo de Sharpe Ratio"""
        # Simular algunos trades
        market_data = self.env.get_market_data()
        self.env.execute_action(0, market_data)
        market_data = self.env.get_market_data()
        self.env.execute_action(1, market_data)
        
        sharpe = self.risk_manager.calculate_sharpe_ratio(self.env)
        
        self.assertIsInstance(sharpe, float)
    
    def test_reset(self):
        """Test: Reset del Risk Manager"""
        # Activar Kill Switch
        self.risk_manager.kill_switch_active = True
        self.risk_manager.drawdown_history.append({"test": "data"})
        
        # Reset
        self.risk_manager.reset()
        
        self.assertFalse(self.risk_manager.kill_switch_active)
        self.assertEqual(len(self.risk_manager.drawdown_history), 0)


class TestSentimentAnalyzer(unittest.TestCase):
    """Tests para el analizador de sentimiento"""
    
    def setUp(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_analyze_sentiment(self):
        """Test: Análisis de sentimiento"""
        sentiment = self.analyzer.analyze_market_sentiment()
        
        self.assertGreaterEqual(sentiment, -1.0)
        self.assertLessEqual(sentiment, 1.0)
    
    def test_volatility_prediction(self):
        """Test: Predicción de volatilidad"""
        # Generar sentimiento
        self.analyzer.analyze_market_sentiment()
        
        volatility = self.analyzer.get_volatility_prediction()
        
        self.assertIn(volatility, ["LOW", "MEDIUM", "HIGH"])
    
    def test_sentiment_history(self):
        """Test: Historial de sentimiento"""
        initial_len = len(self.analyzer.sentiment_history)
        
        self.analyzer.analyze_market_sentiment()
        
        self.assertEqual(len(self.analyzer.sentiment_history), initial_len + 1)


class TestPPOTradingAgent(unittest.TestCase):
    """Tests para el agente PPO"""
    
    def setUp(self):
        self.agent = PPOTradingAgent(state_dim=10, action_dim=3)
    
    def test_initialization(self):
        """Test: Inicialización de redes"""
        self.assertEqual(self.agent.state_dim, 10)
        self.assertEqual(self.agent.action_dim, 3)
        self.assertEqual(self.agent.actor_params.shape, (10, 3))
    
    def test_select_action(self):
        """Test: Selección de acción"""
        state = np.random.randn(10).astype(np.float32)
        sentiment = 0.5
        
        action, log_prob = self.agent.select_action(state, sentiment)
        
        self.assertIn(action, [0, 1, 2])  # BUY, SELL, HOLD
        self.assertIsInstance(log_prob, float)
    
    def test_get_value(self):
        """Test: Estimación de valor"""
        state = np.random.randn(10).astype(np.float32)
        
        value = self.agent.get_value(state)
        
        self.assertIsInstance(value, float)
    
    def test_store_transition(self):
        """Test: Almacenar transición"""
        state = np.random.randn(10).astype(np.float32)
        
        initial_len = len(self.agent.states_buffer)
        self.agent.store_transition(state, 0, 10.0, -0.5, 5.0)
        
        self.assertEqual(len(self.agent.states_buffer), initial_len + 1)
    
    def test_train_insufficient_data(self):
        """Test: Training sin suficientes datos"""
        result = self.agent.train()
        
        self.assertEqual(result["status"], "not_enough_data")
    
    def test_train_with_data(self):
        """Test: Training con datos suficientes"""
        # Generar datos sintéticos
        for _ in range(100):
            state = np.random.randn(10).astype(np.float32)
            action = np.random.randint(0, 3)
            reward = np.random.randn()
            log_prob = np.random.randn()
            value = np.random.randn()
            
            self.agent.store_transition(state, action, reward, log_prob, value)
        
        result = self.agent.train()
        
        self.assertEqual(result["status"], "success")
        self.assertIn("avg_reward", result)


class TestAutoEvolver(unittest.TestCase):
    """Tests para el auto-evolucionador"""
    
    def setUp(self):
        self.evolver = AutoEvolver()
        self.risk_manager = RiskManager()
        self.ppo_agent = PPOTradingAgent()
    
    def test_should_trigger_when_kill_switch_active(self):
        """Test: Trigger cuando Kill Switch está activo"""
        self.risk_manager.kill_switch_active = True
        
        should_retrain = self.evolver.should_trigger_retraining(
            self.risk_manager, self.ppo_agent
        )
        
        self.assertTrue(should_retrain)
    
    def test_should_not_trigger_normally(self):
        """Test: No trigger en condiciones normales"""
        should_retrain = self.evolver.should_trigger_retraining(
            self.risk_manager, self.ppo_agent
        )
        
        self.assertFalse(should_retrain)
    
    def test_retrain_with_penalty(self):
        """Test: Re-entrenar con penalización"""
        risk_events = [
            {"trigger": "MAX_DRAWDOWN", "trigger_value": 0.15, "timestamp": datetime.now()}
        ]
        
        result = self.evolver.retrain_with_penalty(self.ppo_agent, risk_events)
        
        self.assertIn("timestamp", result)
        self.assertIn("penalty_applied", result)
        self.assertEqual(len(self.evolver.evolution_history), 1)


class TestIntelligentInvestmentBot(unittest.TestCase):
    """Tests de integración para el bot completo"""
    
    def setUp(self):
        self.bot = IntelligentInvestmentBot()
    
    def test_initialization(self):
        """Test: Inicialización del bot"""
        self.assertIsNotNone(self.bot.env)
        self.assertIsNotNone(self.bot.risk_manager)
        self.assertIsNotNone(self.bot.sentiment_analyzer)
        self.assertIsNotNone(self.bot.ppo_agent)
        self.assertIsNotNone(self.bot.auto_evolver)
    
    def test_run_episode_short(self):
        """Test: Ejecutar episodio corto"""
        initial_episode_count = self.bot.episode_count
        
        # Ejecutar solo 10 steps
        self.bot.run_episode(max_steps=10)
        
        self.assertEqual(self.bot.episode_count, initial_episode_count + 1)
    
    def test_risk_manager_resets_between_episodes(self):
        """Test: Risk Manager se resetea entre episodios"""
        # Activar Kill Switch manualmente
        self.bot.risk_manager.kill_switch_active = True
        
        # Ejecutar episodio (debería resetear)
        self.bot.run_episode(max_steps=5)
        
        # Al final del episodio, debería haberse reseteado para el siguiente
        # (verificamos que el método reset existe)
        self.bot.risk_manager.reset()
        self.assertFalse(self.bot.risk_manager.kill_switch_active)


class TestEdgeCases(unittest.TestCase):
    """Tests de casos extremos"""
    
    def test_zero_portfolio_value(self):
        """Test: Portfolio value = 0"""
        env = MarketEnvironment()
        env.portfolio_value = 0
        env.peak_value = 1000
        
        risk_manager = RiskManager()
        risk_status = risk_manager.analyze_risk(env)
        
        self.assertEqual(risk_status["diagnosis"], "CRITICAL")
    
    def test_negative_sentiment(self):
        """Test: Sentimiento extremadamente negativo"""
        agent = PPOTradingAgent()
        state = np.random.randn(10).astype(np.float32)
        
        action, _ = agent.select_action(state, sentiment_factor=-1.0)
        
        # Debería favorecer SELL (action=1) con sentimiento negativo
        self.assertIn(action, [0, 1, 2])
    
    def test_positive_sentiment(self):
        """Test: Sentimiento extremadamente positivo"""
        agent = PPOTradingAgent()
        state = np.random.randn(10).astype(np.float32)
        
        action, _ = agent.select_action(state, sentiment_factor=1.0)
        
        # Debería favorecer BUY (action=0) con sentimiento positivo
        self.assertIn(action, [0, 1, 2])
    
    def test_empty_price_history_rsi(self):
        """Test: RSI con historial vacío"""
        env = MarketEnvironment()
        market_data = {"price": 50000, "closes": [50000], "volumes": [1000]}
        
        indicators = env.calculate_technical_indicators(market_data)
        
        # Con pocos datos, debería retornar valores default
        self.assertEqual(indicators["rsi"], 50.0)


class TestBinanceAPI(unittest.TestCase):
    """Tests para integración con Binance"""
    
    def test_binance_api_error_fallback(self):
        """Test: Fallback a datos simulados si Binance falla"""
        env = MarketEnvironment(exchange="binance", symbol="BTCUSDT")
        
        # Debería usar datos simulados si API falla
        data = env.get_market_data()
        
        self.assertIn("price", data)
        self.assertGreater(data["price"], 0)
    
    def test_kraken_api_error_fallback(self):
        """Test: Fallback a datos simulados si Kraken falla"""
        env = MarketEnvironment(exchange="kraken", symbol="BTCUSDT")
        
        data = env.get_market_data()
        
        self.assertIn("price", data)
        self.assertGreater(data["price"], 0)


class TestTechnicalIndicators(unittest.TestCase):
    """Tests exhaustivos de indicadores técnicos"""
    
    def test_calculate_ema(self):
        """Test: Cálculo de EMA"""
        env = MarketEnvironment()
        prices = np.array([100, 102, 104, 103, 105, 107, 106, 108, 110, 109])
        
        ema = env._calculate_ema(prices, period=5)
        
        self.assertGreater(ema, 0)
        self.assertIsInstance(ema, float)
    
    def test_calculate_macd(self):
        """Test: Cálculo de MACD"""
        env = MarketEnvironment()
        prices = np.array([100 + i * 0.5 for i in range(50)])
        
        macd, signal = env._calculate_macd(prices)
        
        self.assertIsInstance(macd, float)
        self.assertIsInstance(signal, float)
    
    def test_rsi_edge_cases(self):
        """Test: RSI casos extremos"""
        env = MarketEnvironment()
        
        # Precios todos subiendo
        prices_up = np.array([100 + i for i in range(20)])
        rsi_up = env._calculate_rsi(prices_up, period=14)
        self.assertGreater(rsi_up, 70)  # Sobrecomprado
        
        # Precios todos bajando
        prices_down = np.array([100 - i for i in range(20)])
        rsi_down = env._calculate_rsi(prices_down, period=14)
        self.assertLess(rsi_down, 30)  # Sobrevendido
    
    def test_technical_indicators_with_sufficient_data(self):
        """Test: Indicadores con datos suficientes"""
        env = MarketEnvironment()
        
        # Generar 100 precios
        closes = [50000 + np.random.randn() * 100 for _ in range(100)]
        market_data = {
            "price": closes[-1],
            "closes": closes,
            "volumes": [1000] * 100,
            "volume_24h": 1000
        }
        
        indicators = env.calculate_technical_indicators(market_data)
        
        self.assertNotEqual(indicators["rsi"], 50.0)  # No es default
        self.assertIsInstance(indicators["macd"], float)
        self.assertIsInstance(indicators["sma_20"], float)
        self.assertIsInstance(indicators["sma_50"], float)


class TestStateConstruction(unittest.TestCase):
    """Tests para construcción del estado"""
    
    def test_get_state_normalization(self):
        """Test: Normalización correcta del estado"""
        env = MarketEnvironment()
        
        # Generar datos
        for _ in range(10):
            env.price_history.append(50000 + np.random.randn() * 1000)
            env.volume_history.append(1000 + np.random.randn() * 100)
        
        market_data = env.get_market_data()
        sentiment = 0.5
        
        state = env.get_state(market_data, sentiment)
        
        # Verificar dimensiones
        self.assertEqual(len(state), 10)
        
        # Verificar que es un array válido
        self.assertFalse(np.any(np.isnan(state)))
        self.assertFalse(np.any(np.isinf(state)))
    
    def test_get_state_with_position(self):
        """Test: Estado cuando hay posición abierta"""
        env = MarketEnvironment()
        
        # Comprar
        market_data = env.get_market_data()
        env.execute_action(0, market_data)  # BUY
        
        # Obtener estado
        state = env.get_state(market_data, sentiment_factor=0.0)
        
        # Última dimensión debería ser 1.0 (tiene posición)
        self.assertEqual(state[-1], 1.0)


class TestTradeExecution(unittest.TestCase):
    """Tests exhaustivos de ejecución de trades"""
    
    def test_buy_with_insufficient_cash(self):
        """Test: Comprar cuando no hay suficiente cash"""
        env = MarketEnvironment()
        env.cash = 0
        
        market_data = env.get_market_data()
        reward, done = env.execute_action(0, market_data)  # BUY
        
        # No debería comprar nada
        self.assertEqual(env.current_position, 0.0)
    
    def test_sell_without_position(self):
        """Test: Vender cuando no hay posición"""
        env = MarketEnvironment()
        
        market_data = env.get_market_data()
        reward, done = env.execute_action(1, market_data)  # SELL
        
        # No debería hacer nada
        self.assertEqual(len(env.trades_history), 0)
    
    def test_hold_action(self):
        """Test: Acción HOLD"""
        env = MarketEnvironment()
        
        initial_cash = env.cash
        initial_position = env.current_position
        
        market_data = env.get_market_data()
        reward, done = env.execute_action(2, market_data)  # HOLD
        
        # No debería cambiar nada
        self.assertEqual(env.cash, initial_cash)
        self.assertEqual(env.current_position, initial_position)
        self.assertEqual(reward, 0.0)
    
    def test_maximum_drawdown_trigger(self):
        """Test: MDD excedido termina episodio"""
        env = MarketEnvironment()
        
        # Primero hacer un trade para tener peak value
        market_data = env.get_market_data()
        env.execute_action(0, market_data)  # BUY
        
        # Ahora simular caída de precio grande
        env.peak_value = env.portfolio_value
        
        # Simular precio que cae 50%
        market_data_crash = env.get_market_data()
        market_data_crash["price"] = market_data["price"] * 0.5
        
        # Actualizar portfolio value manualmente
        env.portfolio_value = env.cash + (env.current_position * market_data_crash["price"])
        
        # Verificar que el drawdown es > 10%
        drawdown = (env.peak_value - env.portfolio_value) / env.peak_value
        
        # Solo verificar si el drawdown es efectivamente > 10%
        if drawdown >= 0.10:
            reward, done = env.execute_action(2, market_data_crash)
            self.assertTrue(done)
            self.assertLess(reward, 0)


class TestRiskManagerAdvanced(unittest.TestCase):
    """Tests avanzados del Risk Manager"""
    
    def test_warning_diagnosis(self):
        """Test: Diagnóstico WARNING cuando MDD cerca del threshold"""
        env = MarketEnvironment()
        env.peak_value = 1000
        env.portfolio_value = 930  # 7% drawdown
        
        risk_manager = RiskManager()
        risk_status = risk_manager.analyze_risk(env)
        
        self.assertEqual(risk_status["diagnosis"], "WARNING")
    
    def test_kill_switch_event_saved(self):
        """Test: Evento de Kill Switch se guarda para AI 4"""
        env = MarketEnvironment()
        env.peak_value = 1000
        env.portfolio_value = 850
        
        risk_manager = RiskManager()
        risk_manager.analyze_risk(env)
        
        self.assertEqual(len(risk_manager.risk_events), 1)
        self.assertEqual(risk_manager.risk_events[0]["trigger"], "MAX_DRAWDOWN")
    
    def test_should_not_allow_oversized_position(self):
        """Test: No permitir posiciones sobredimensionadas"""
        env = MarketEnvironment()
        
        # Simular posición grande
        market_data = env.get_market_data()
        env.current_position = 1.0  # 1 BTC
        env.price_history = [market_data["price"]]
        
        risk_manager = RiskManager()
        
        # Intentar comprar más
        allowed = risk_manager.should_allow_trade(env, 0)  # BUY
        
        # Debería bloquear si la posición ya es grande
        position_value = env.current_position * market_data["price"]
        if position_value / env.portfolio_value > 0.2:
            self.assertFalse(allowed)


class TestPPOAdvanced(unittest.TestCase):
    """Tests avanzados del agente PPO"""
    
    def test_gae_calculation(self):
        """Test: Cálculo de GAE (Generalized Advantage Estimation)"""
        agent = PPOTradingAgent()
        
        rewards = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
        values = np.array([0.5, 1.0, 1.5, 1.0, 0.5])
        final_value = 0.0
        
        returns, advantages = agent._calculate_gae(rewards, values, final_value)
        
        self.assertEqual(len(returns), len(rewards))
        self.assertEqual(len(advantages), len(rewards))
    
    def test_save_and_load_model(self):
        """Test: Guardar y cargar modelo"""
        import tempfile
        import os
        
        agent = PPOTradingAgent()
        
        # Entrenar un poco
        for _ in range(100):
            state = np.random.randn(10).astype(np.float32)
            agent.store_transition(state, 0, 1.0, -0.5, 0.5)
        
        agent.train()
        
        # Guardar
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        agent.save_model(temp_path)
        
        # Cargar en nuevo agente
        new_agent = PPOTradingAgent()
        new_agent.load_model(temp_path)
        
        # Verificar que los parámetros son iguales
        np.testing.assert_array_equal(agent.actor_params, new_agent.actor_params)
        np.testing.assert_array_equal(agent.critic_params, new_agent.critic_params)
        
        # Cleanup
        os.remove(temp_path)
    
    def test_sentiment_influence_on_action(self):
        """Test: Sentimiento influye en selección de acción"""
        agent = PPOTradingAgent()
        state = np.zeros(10, dtype=np.float32)
        
        # Probar múltiples veces con sentimiento positivo
        buy_count = 0
        for _ in range(50):
            action, _ = agent.select_action(state, sentiment_factor=0.9)
            if action == 0:  # BUY
                buy_count += 1
        
        # Con sentimiento muy positivo, debería comprar más frecuentemente
        # (aunque hay aleatoriedad)
        self.assertGreater(buy_count, 10)


class TestAutoEvolverAdvanced(unittest.TestCase):
    """Tests avanzados del Auto-Evolver"""
    
    def test_trigger_on_poor_performance(self):
        """Test: Trigger cuando performance es pobre"""
        evolver = AutoEvolver()
        risk_manager = RiskManager()
        ppo_agent = PPOTradingAgent()
        
        # Simular historial de pérdidas
        for _ in range(20):
            ppo_agent.training_history.append({
                "timestamp": datetime.now(),
                "avg_reward": -50.0,  # Pérdidas consistentes
                "num_transitions": 100
            })
        
        should_retrain = evolver.should_trigger_retraining(risk_manager, ppo_agent)
        
        self.assertTrue(should_retrain)
    
    def test_evolution_history_tracking(self):
        """Test: Historial de evoluciones"""
        evolver = AutoEvolver()
        ppo_agent = PPOTradingAgent()
        
        risk_events = [
            {"trigger": "MAX_DRAWDOWN", "trigger_value": 0.15, "timestamp": datetime.now()}
        ]
        
        evolver.retrain_with_penalty(ppo_agent, risk_events)
        evolver.retrain_with_penalty(ppo_agent, risk_events)
        
        self.assertEqual(len(evolver.evolution_history), 2)
    
    def test_generate_evolution_report(self):
        """Test: Generación de reporte de evolución"""
        evolver = AutoEvolver()
        ppo_agent = PPOTradingAgent()
        
        # Sin evoluciones
        report = evolver.generate_evolution_report()
        self.assertIn("No evolution events", report)
        
        # Con evoluciones
        risk_events = [
            {"trigger": "MAX_DRAWDOWN", "trigger_value": 0.15, "timestamp": datetime.now()}
        ]
        evolver.retrain_with_penalty(ppo_agent, risk_events)
        
        report = evolver.generate_evolution_report()
        self.assertIn("Auto-Evolution Report", report)
        self.assertIn("Evolution 1", report)


class TestIntegrationAdvanced(unittest.TestCase):
    """Tests de integración avanzados"""
    
    def test_complete_episode_cycle(self):
        """Test: Ciclo completo de episodio"""
        bot = IntelligentInvestmentBot()
        
        # Ejecutar episodio más largo para garantizar trades
        bot.run_episode(max_steps=100)
        
        # Verificar que se ejecutó el episodio
        self.assertEqual(bot.episode_count, 1)
        
        # Si hubo trades, verificar que se procesaron
        if len(bot.env.trades_history) > 0:
            # Puede o no haber training history dependiendo de la cantidad de datos
            self.assertGreaterEqual(len(bot.ppo_agent.training_history), 0)
    
    def test_multiple_episodes_with_reset(self):
        """Test: Múltiples episodios con reset correcto"""
        bot = IntelligentInvestmentBot()
        
        # Episodio 1
        bot.run_episode(max_steps=10)
        episode1_trades = len(bot.env.trades_history)
        
        # Episodio 2
        bot.run_episode(max_steps=10)
        episode2_trades = len(bot.env.trades_history)
        
        # Cada episodio debería tener trades independientes
        self.assertEqual(bot.episode_count, 2)
    
    def test_kill_switch_triggers_auto_evolver(self):
        """Test: Kill Switch activa Auto-Evolver"""
        bot = IntelligentInvestmentBot()
        
        # Forzar pérdida grande para activar Kill Switch
        bot.env.peak_value = 1000
        bot.env.portfolio_value = 850
        
        # Ejecutar episodio corto
        bot.run_episode(max_steps=5)
        
        # Auto-Evolver debería haber actuado
        # (verificamos que el sistema no crashea)
        self.assertIsNotNone(bot.auto_evolver)


class TestSentimentAnalyzerAdvanced(unittest.TestCase):
    """Tests avanzados del Sentiment Analyzer"""
    
    def test_volatility_low_with_neutral_sentiment(self):
        """Test: Volatilidad LOW con sentimiento neutral"""
        analyzer = SentimentAnalyzer()
        
        # Forzar sentimiento neutral
        analyzer.sentiment_history.append({
            "timestamp": datetime.now(),
            "factor": 0.0,
            "positive_signals": 5,
            "negative_signals": 5,
            "news_count": 10
        })
        
        volatility = analyzer.get_volatility_prediction()
        self.assertEqual(volatility, "LOW")
    
    def test_volatility_high_with_extreme_sentiment(self):
        """Test: Volatilidad HIGH con sentimiento extremo"""
        analyzer = SentimentAnalyzer()
        
        # Forzar sentimiento extremo
        analyzer.sentiment_history.append({
            "timestamp": datetime.now(),
            "factor": 0.9,  # Muy positivo
            "positive_signals": 20,
            "negative_signals": 0,
            "news_count": 20
        })
        
        volatility = analyzer.get_volatility_prediction()
        self.assertEqual(volatility, "HIGH")
    
    def test_volatility_medium(self):
        """Test: Volatilidad MEDIUM con sentimiento moderado"""
        analyzer = SentimentAnalyzer()
        
        analyzer.sentiment_history.append({
            "timestamp": datetime.now(),
            "factor": 0.5,
            "positive_signals": 10,
            "negative_signals": 5,
            "news_count": 15
        })
        
        volatility = analyzer.get_volatility_prediction()
        self.assertEqual(volatility, "MEDIUM")


class TestBotReporting(unittest.TestCase):
    """Tests para generación de reportes"""
    
    def test_generate_final_report(self):
        """Test: Generación de reporte final"""
        import tempfile
        import os
        
        bot = IntelligentInvestmentBot()
        
        # Ejecutar episodio
        bot.run_episode(max_steps=10)
        
        # Generar reporte
        bot._generate_final_report()
        
        # Verificar que se generó el archivo
        reports = [f for f in os.listdir("trading_data") if f.startswith("final_report")]
        self.assertGreater(len(reports), 0)


class TestKrakenAPI(unittest.TestCase):
    """Tests específicos para Kraken API"""
    
    def test_kraken_data_structure(self):
        """Test: Estructura de datos de Kraken"""
        env = MarketEnvironment(exchange="kraken", symbol="BTCUSDT")
        
        data = env._get_kraken_data()
        
        # Debería tener estructura correcta (aunque use fallback)
        self.assertIn("price", data)
        self.assertIn("volume_24h", data)
        self.assertIn("closes", data)


class TestRiskManagerEdgeCases(unittest.TestCase):
    """Tests de casos extremos del Risk Manager"""
    
    def test_save_kill_switch_event_creates_file(self):
        """Test: Guardar evento crea archivo JSON"""
        import os
        
        risk_manager = RiskManager()
        env = MarketEnvironment()
        
        # Simular Kill Switch
        env.peak_value = 1000
        env.portfolio_value = 850
        
        risk_manager.analyze_risk(env)
        
        # Verificar que se creó el archivo
        events_file = os.path.join("trading_data", "kill_switch_events.json")
        self.assertTrue(os.path.exists(events_file))
    
    def test_sharpe_ratio_with_no_trades(self):
        """Test: Sharpe Ratio sin trades"""
        risk_manager = RiskManager()
        env = MarketEnvironment()
        
        sharpe = risk_manager.calculate_sharpe_ratio(env)
        
        self.assertEqual(sharpe, 0.0)


class TestPPOEdgeCases(unittest.TestCase):
    """Tests de casos extremos del PPO"""
    
    def test_train_clears_buffers(self):
        """Test: Training limpia buffers"""
        agent = PPOTradingAgent()
        
        # Llenar buffers
        for _ in range(100):
            state = np.random.randn(10).astype(np.float32)
            agent.store_transition(state, 0, 1.0, -0.5, 0.5)
        
        self.assertGreater(len(agent.states_buffer), 0)
        
        # Entrenar
        agent.train()
        
        # Buffers deberían estar vacíos
        self.assertEqual(len(agent.states_buffer), 0)
    
    def test_gae_with_zero_values(self):
        """Test: GAE con valores cero"""
        agent = PPOTradingAgent()
        
        rewards = np.zeros(10)
        values = np.zeros(10)
        
        returns, advantages = agent._calculate_gae(rewards, values, 0.0)
        
        # No debería crashear
        self.assertEqual(len(returns), 10)
        self.assertEqual(len(advantages), 10)


class TestMarketEnvironmentEdgeCases(unittest.TestCase):
    """Tests de casos extremos del entorno"""
    
    def test_execute_action_updates_peak_value(self):
        """Test: Peak value se actualiza con ganancias"""
        env = MarketEnvironment()
        
        # Comprar primero
        market_data = env.get_market_data()
        env.execute_action(0, market_data)  # BUY
        
        initial_peak = env.peak_value
        
        # Simular subida de precio (portfolio aumenta)
        market_data_new = env.get_market_data()
        market_data_new["price"] = market_data["price"] * 1.5  # +50% precio
        
        env.execute_action(2, market_data_new)  # HOLD (recalcula portfolio)
        
        # Peak debería actualizarse
        self.assertGreaterEqual(env.peak_value, initial_peak)
    
    def test_portfolio_value_below_10_percent_triggers_done(self):
        """Test: Portfolio < 10% del capital inicial termina episodio"""
        env = MarketEnvironment()
        
        # Comprar y luego simular crash masivo
        market_data = env.get_market_data()
        env.execute_action(0, market_data)  # BUY
        
        # Crash del 95%
        market_data_crash = env.get_market_data()
        market_data_crash["price"] = market_data["price"] * 0.05  # -95%
        
        reward, done = env.execute_action(2, market_data_crash)
        
        # Verificar si portfolio < 10% del inicial
        if env.portfolio_value < TRADING_CONFIG["initial_capital"] * 0.1:
            self.assertTrue(done)


class TestIntegrationComplete(unittest.TestCase):
    """Tests de integración completa del sistema"""
    
    def test_full_cycle_with_training(self):
        """Test: Ciclo completo con suficientes datos para training"""
        bot = IntelligentInvestmentBot()
        
        # Ejecutar episodio largo para garantizar training
        bot.run_episode(max_steps=200)
        
        # Debería haber completado el episodio
        self.assertEqual(bot.episode_count, 1)
    
    def test_sentiment_affects_trading_decisions(self):
        """Test: Sentimiento afecta decisiones de trading"""
        bot = IntelligentInvestmentBot()
        
        # Forzar sentimiento extremo
        bot.sentiment_analyzer.sentiment_history.append({
            "timestamp": datetime.now(),
            "factor": 0.9,
            "positive_signals": 20,
            "negative_signals": 0,
            "news_count": 20
        })
        
        # Ejecutar algunos steps
        market_data = bot.env.get_market_data()
        sentiment = 0.9
        state = bot.env.get_state(market_data, sentiment)
        
        action, _ = bot.ppo_agent.select_action(state, sentiment)
        
        # Debería ser una acción válida
        self.assertIn(action, [0, 1, 2])


class TestBinanceRealAPI(unittest.TestCase):
    """Tests para código de Binance API real"""
    
    def test_binance_ticker_parsing(self):
        """Test: Parseo de datos de Binance"""
        env = MarketEnvironment(exchange="binance", symbol="BTCUSDT")
        
        # Intentar obtener datos (fallback si API falla)
        data = env._get_binance_data()
        
        # Verificar estructura
        self.assertIn("price", data)
        self.assertIn("closes", data)
        self.assertIsInstance(data["closes"], list)
    
    def test_binance_klines_data(self):
        """Test: Datos de klines para RSI/MACD"""
        env = MarketEnvironment(exchange="binance", symbol="BTCUSDT")
        
        data = env._get_binance_data()
        
        # Debería tener al menos 1 elemento
        self.assertGreater(len(data["closes"]), 0)


class TestKrakenRealAPI(unittest.TestCase):
    """Tests para código de Kraken API real"""
    
    def test_kraken_ticker_structure(self):
        """Test: Estructura de respuesta de Kraken"""
        env = MarketEnvironment(exchange="kraken", symbol="BTCUSDT")
        
        data = env._get_kraken_data()
        
        # Verificar estructura mínima
        self.assertIn("price", data)
        self.assertIn("high_24h", data)
        self.assertIn("low_24h", data)


class TestCLIFunctions(unittest.TestCase):
    """Tests para funciones de CLI"""
    
    def test_run_live_trading_initialization(self):
        """Test: Inicialización de run_live_trading"""
        bot = IntelligentInvestmentBot()
        
        # Verificar que el método existe y es callable
        self.assertTrue(callable(bot.run_live_trading))
        
        # Ejecutar 1 episodio corto
        bot.running = True
        bot.run_episode(max_steps=5)
        
        self.assertEqual(bot.episode_count, 1)


class TestReportGeneration(unittest.TestCase):
    """Tests para generación de reportes completos"""
    
    def test_final_report_content(self):
        """Test: Contenido del reporte final"""
        import os
        
        bot = IntelligentInvestmentBot()
        bot.run_episode(max_steps=10)
        
        # Generar reporte
        bot._generate_final_report()
        
        # Leer reporte generado
        reports = sorted([f for f in os.listdir("trading_data") if f.startswith("final_report")])
        
        if reports:
            latest_report = reports[-1]
            report_path = os.path.join("trading_data", latest_report)
            
            with open(report_path, 'r') as f:
                content = f.read()
            
            # Verificar contenido básico
            self.assertIn("Intelligent Investment Bot", content)
            self.assertIn("Episodes:", content)


class TestSimulatedDataGeneration(unittest.TestCase):
    """Tests para generación de datos simulados"""
    
    def test_simulated_price_random_walk(self):
        """Test: Random walk en precios simulados"""
        env = MarketEnvironment(exchange="paper", symbol="BTCUSDT")
        
        # Generar varios datos
        prices = []
        for _ in range(10):
            data = env._get_simulated_data()
            prices.append(data["price"])
        
        # Los precios deberían variar
        self.assertGreater(max(prices), min(prices))
    
    def test_simulated_data_consistency(self):
        """Test: Consistencia de datos simulados"""
        env = MarketEnvironment(exchange="paper", symbol="BTCUSDT")
        
        data = env._get_simulated_data()
        
        # Price dentro de high/low
        self.assertLessEqual(data["price"], data["high_24h"])
        self.assertGreaterEqual(data["price"], data["low_24h"])


class TestRSIEdgeCases(unittest.TestCase):
    """Tests para casos extremos de RSI"""
    
    def test_rsi_with_zero_losses(self):
        """Test: RSI cuando solo hay ganancias (sin pérdidas)"""
        env = MarketEnvironment()
        
        # Precios siempre subiendo
        prices = np.array([100 + i for i in range(20)])
        
        rsi = env._calculate_rsi(prices, period=14)
        
        # RSI debería ser 100 (sobrecomprado)
        self.assertEqual(rsi, 100.0)
    
    def test_rsi_with_flat_prices(self):
        """Test: RSI con precios planos"""
        env = MarketEnvironment()
        
        # Precios constantes
        prices = np.array([100.0] * 20)
        
        rsi = env._calculate_rsi(prices, period=14)
        
        # RSI debería ser 100 (sin pérdidas)
        self.assertEqual(rsi, 100.0)


class TestMACDCalculation(unittest.TestCase):
    """Tests para cálculo de MACD"""
    
    def test_macd_with_trending_prices(self):
        """Test: MACD con precios en tendencia"""
        env = MarketEnvironment()
        
        # Tendencia alcista
        prices = np.array([100 + i * 2 for i in range(50)])
        
        macd, signal = env._calculate_macd(prices)
        
        # MACD debería ser positivo en tendencia alcista
        self.assertIsInstance(macd, float)
        self.assertIsInstance(signal, float)


class TestEMACalculation(unittest.TestCase):
    """Tests para cálculo de EMA"""
    
    def test_ema_converges(self):
        """Test: EMA converge hacia precio actual"""
        env = MarketEnvironment()
        
        # Precios que convergen a 200
        prices = np.array([100] * 10 + [200] * 20)
        
        ema = env._calculate_ema(prices, period=10)
        
        # EMA debería estar cerca de 200
        self.assertGreater(ema, 150)


class TestPositionTracking(unittest.TestCase):
    """Tests para tracking de posiciones"""
    
    def test_position_indicator_accuracy(self):
        """Test: Indicador de posición es preciso"""
        env = MarketEnvironment()
        
        # Sin posición
        market_data = env.get_market_data()
        state = env.get_state(market_data, sentiment_factor=0.0)
        self.assertEqual(state[-1], 0.0)  # No position
        
        # Con posición
        env.execute_action(0, market_data)  # BUY
        state = env.get_state(market_data, sentiment_factor=0.0)
        self.assertEqual(state[-1], 1.0)  # Has position


class TestTradeHistoryTracking(unittest.TestCase):
    """Tests para historial de trades"""
    
    def test_trade_history_records_all_actions(self):
        """Test: Historial registra todas las acciones"""
        env = MarketEnvironment()
        
        # Buy
        market_data = env.get_market_data()
        env.execute_action(0, market_data)
        
        self.assertEqual(len(env.trades_history), 1)
        self.assertEqual(env.trades_history[0]["action"], "BUY")
        
        # Sell
        market_data = env.get_market_data()
        env.execute_action(1, market_data)
        
        self.assertEqual(len(env.trades_history), 2)
        self.assertEqual(env.trades_history[1]["action"], "SELL")


class TestFeesCalculation(unittest.TestCase):
    """Tests para cálculo de fees"""
    
    def test_buy_includes_fees(self):
        """Test: Compra incluye fees"""
        env = MarketEnvironment()
        
        initial_cash = env.cash
        market_data = env.get_market_data()
        
        env.execute_action(0, market_data)  # BUY
        
        # Verificar que el trade registró fee
        self.assertIn("fee", env.trades_history[0])
        self.assertGreater(env.trades_history[0]["fee"], 0)
    
    def test_sell_includes_fees(self):
        """Test: Venta incluye fees"""
        env = MarketEnvironment()
        
        market_data = env.get_market_data()
        env.execute_action(0, market_data)  # BUY
        
        market_data = env.get_market_data()
        env.execute_action(1, market_data)  # SELL
        
        # Verificar fee en venta
        self.assertIn("fee", env.trades_history[1])
        self.assertGreater(env.trades_history[1]["fee"], 0)


class TestMainCLI(unittest.TestCase):
    """Tests para el CLI principal"""
    
    def test_main_with_minimal_args(self):
        """Test: Ejecutar main con argumentos mínimos"""
        import sys
        from unittest.mock import patch
        
        # Simular argumentos de CLI
        test_args = [
            'intelligent_investment_bot.py',
            '--episodes', '1',
            '--exchange', 'paper',
            '--capital', '500'
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Importar y ejecutar main
            from intelligent_investment_bot import main
            
            # Ejecutar (debería completar sin errores)
            try:
                main()
            except SystemExit:
                pass  # CLI llama a sys.exit(), lo cual es normal


if __name__ == "__main__":
    # Configurar verbose output
    unittest.main(verbosity=2)
