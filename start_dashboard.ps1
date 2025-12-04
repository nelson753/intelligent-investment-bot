# 🎨 Dashboard Script
# Inicia el dashboard web para visualizar trades en tiempo real

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  📊 TRADING DASHBOARD - Multi-Crypto Bot                 ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

Write-Host "🌐 URL: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5000" -ForegroundColor Cyan

Write-Host "📈 Visualiza: " -NoNewline -ForegroundColor White
Write-Host "Trades activos, P&L, historial`n" -ForegroundColor Gray

# Verificar que el archivo existe
if (-not (Test-Path "scripts\dashboard_multi_crypto.py")) {
    Write-Host "❌ ERROR: No se encuentra scripts\dashboard_multi_crypto.py" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Iniciando dashboard...`n" -ForegroundColor Green
Write-Host "ℹ️  Presiona CTRL+C para detener`n" -ForegroundColor Cyan

# Ejecutar dashboard
python scripts\dashboard_multi_crypto.py
