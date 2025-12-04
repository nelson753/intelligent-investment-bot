# 📊 Analyze History Script
# Analiza el rendimiento histórico de todas las sesiones

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  📊 HISTORICAL ANALYSIS - Trading Sessions               ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

# Verificar que el archivo existe
if (-not (Test-Path "scripts\analyze_history.py")) {
    Write-Host "❌ ERROR: No se encuentra scripts\analyze_history.py" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Analizando sesiones guardadas...`n" -ForegroundColor Cyan

# Ejecutar análisis
python scripts\analyze_history.py

Write-Host "`n✅ Análisis completado`n" -ForegroundColor Green
