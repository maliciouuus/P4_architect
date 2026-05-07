#!/bin/bash

REPO="/home/sacha/Public/openclassroom/architect/P4_architect"
cd "$REPO/backend-nest"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔬 DataShare — Tests unitaires (Jest)"
echo "  $(date '+%d/%m/%Y %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "▶ Lancement des 32 tests..."
echo ""

npm test

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "▶ Génération du rapport de couverture..."
echo ""

npm run test:cov

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 Rapport HTML disponible ici :"
echo "  backend-nest/coverage/lcov-report/index.html"
echo ""
echo "  Ouvrir dans le navigateur :"
echo "  xdg-open coverage/lcov-report/index.html"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
