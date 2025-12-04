# 🚀 Quick Start Script
# Inicia el bot de trading multi-crypto

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🤖 MULTI-CRYPTO AUTONOMOUS TRADING BOT v3.0              ║" -ForegroundColor Cyan
Write-Host "║  EMA 200 Trend Filter + ATR Dynamic SL + MACD Exits       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "📊 Capital: " -NoNewline -ForegroundColor White
Write-Host "`$40 USD" -ForegroundColor Green

Write-Host "💰 Modo: " -NoNewline -ForegroundColor White
Write-Host "Paper Trading " -NoNewline -ForegroundColor Yellow
Write-Host "(Precios reales, ejecuciones simuladas)" -ForegroundColor Gray

Write-Host "📈 Criptos: " -NoNewline -ForegroundColor White
Write-Host "DOGE★, ETH, SOL, XRP, ADA, MATIC, LINK`n" -ForegroundColor Cyan

Write-Host "🎯 Win Rate Histórico: " -NoNewline -ForegroundColor White
Write-Host "81.8% " -NoNewline -ForegroundColor Green
Write-Host "(11/13 trades)`n" -ForegroundColor Gray

Write-Host "════════════════════════════════════════════════════════════`n" -ForegroundColor DarkGray

# Verificar que el archivo existe
if (-not (Test-Path "multi_crypto_trading.py")) {
    Write-Host "❌ ERROR: No se encuentra multi_crypto_trading.py" -ForegroundColor Red
    Write-Host "   Asegúrate de estar en el directorio correcto`n" -ForegroundColor Yellow
    exit 1
}

# Preguntar confirmación
Write-Host "¿Iniciar bot de trading? (presiona Enter para continuar, Ctrl+C para cancelar)" -ForegroundColor Yellow
Read-Host

Write-Host "`n🚀 Iniciando bot...`n" -ForegroundColor Green
Write-Host "ℹ️  Presiona CTRL+C para detener el bot de forma segura`n" -ForegroundColor Cyan

# Ejecutar bot
python multi_crypto_trading.py
