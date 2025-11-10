#!/bin/bash
# Script de teste rápido para macOS/Linux
# Testa o PathFinder A* sem necessitar Pygame

echo "======================================================================"
echo "TESTE RÁPIDO - PATHFINDER A* (macOS/Linux)"
echo "======================================================================"
echo ""

# Verifica se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRO: python3 não encontrado!"
    echo "Por favor, instale Python 3 de https://python.org"
    exit 1
fi

echo "Executando testes..."
echo ""

python3 test_quick.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "✅ SUCESSO: Todos os testes passaram!"
    echo "======================================================================"
else
    echo ""
    echo "======================================================================"
    echo "❌ ERRO: Alguns testes falharam!"
    echo "======================================================================"
    exit 1
fi

echo ""
echo "Para testar com interface gráfica (GUI):"
echo "  1. Crie ambiente virtual: python3 -m venv venv"
echo "  2. Ative: source venv/bin/activate"
echo "  3. Instale pygame: pip install pygame"
echo "  4. Execute: python3 main.py --example 1"
echo ""
