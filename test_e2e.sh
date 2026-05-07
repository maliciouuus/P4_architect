#!/bin/bash

REPO="/home/sacha/Public/openclassroom/architect/P4_architect"
cd "$REPO"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐 DataShare — Tests E2E (Playwright)"
echo "  $(date '+%d/%m/%Y %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Vérifier que l'application tourne
echo "▶ Vérification que l'application est démarrée..."
if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo ""
    echo "  ⚠️  Le frontend n'est pas accessible sur http://localhost:5173"
    echo "  Lance d'abord : bash start.sh"
    echo ""
    exit 1
fi

if ! curl -s http://localhost:8000/api > /dev/null 2>&1; then
    echo ""
    echo "  ⚠️  Le backend n'est pas accessible sur http://localhost:8000"
    echo "  Lance d'abord : bash start.sh"
    echo ""
    exit 1
fi

echo "  ✅ Frontend OK — http://localhost:5173"
echo "  ✅ Backend OK  — http://localhost:8000/api"
echo ""

# Activer le venv et lancer les tests
echo "▶ Activation de l'environnement Python..."
cd e2e
source venv/bin/activate

echo "▶ Lancement des 11 scénarios Playwright..."
echo ""

pytest -v

EXIT_CODE=$?

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $EXIT_CODE -eq 0 ]; then
    echo "  ✅ Tous les tests E2E sont passants"
else
    echo "  ❌ Certains tests ont échoué"
    echo "  Screenshots d'échec dans : e2e/"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $EXIT_CODE
