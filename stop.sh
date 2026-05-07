#!/bin/bash

REPO="/home/sacha/Public/openclassroom/architect/P4_architect"
cd "$REPO"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🛑 DataShare — Arrêt"
echo "  $(date '+%d/%m/%Y %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker compose down

echo ""
echo "  ✅ Tous les services sont arrêtés."
echo "  Les données PostgreSQL et fichiers uploadés sont conservés."
echo ""
echo "  Relancer : bash start.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
