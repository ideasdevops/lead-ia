#!/bin/bash
# Script para verificar el estado del backend dentro del contenedor

echo "🔍 Verificando estado del backend..."
echo ""

echo "1️⃣ Estado de Supervisor:"
supervisorctl status
echo ""

echo "2️⃣ Logs de error del backend (últimas 50 líneas):"
echo "---"
tail -50 /var/log/supervisor/backend.err.log
echo "---"
echo ""

echo "3️⃣ Logs de salida del backend (últimas 50 líneas):"
echo "---"
tail -50 /var/log/supervisor/backend.out.log
echo "---"
echo ""

echo "4️⃣ Verificando si Flask está escuchando en puerto 5000:"
netstat -tlnp | grep 5000 || echo "❌ No hay proceso escuchando en puerto 5000"
echo ""

echo "5️⃣ Procesos Python corriendo:"
ps aux | grep python | grep -v grep || echo "❌ No hay procesos Python corriendo"
echo ""

echo "6️⃣ Intentando iniciar backend manualmente:"
cd /app/backend
echo "📦 Directorio: $(pwd)"
echo "📦 DATABASE_URL: $(if [ -n "$DATABASE_URL" ]; then echo "Configurada"; else echo "NO CONFIGURADA"; fi)"
echo ""
echo "Ejecutando: python run.py"
echo "---"

