#!/bin/bash

REPO="/home/sacha/Public/openclassroom/architect/P4_architect"
cd "$REPO"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 DataShare — Démarrage"
echo "  $(date '+%d/%m/%Y %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "▶ Démarrage des services Docker..."
docker compose up -d

echo ""
echo "▶ Attente que la base de données soit prête..."
sleep 3

echo ""
echo "▶ État des services :"
docker compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ DataShare est prêt"
echo ""
echo "  Frontend  →  http://localhost:5173"
echo "  API       →  http://localhost:8000/api"
echo "  Base      →  localhost:5433"
echo ""
echo "  Logs en direct : docker compose logs -f backend"
echo "  Arrêter       : bash stop.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
