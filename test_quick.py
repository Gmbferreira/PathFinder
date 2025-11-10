#!/usr/bin/env python3
"""
Script de teste rápido sem necessitar Pygame
Testa os módulos principais do PathFinder A*
"""

print("=" * 70)
print("TESTE RÁPIDO - PATHFINDER A*")
print("=" * 70)

# Teste 1: Importar módulos
print("\n[1/4] Testando imports...")
try:
    from src.maze import Maze
    from src.pathfinder import a_star
    from src.visualizer import visualize_solution
    print("✓ Imports OK!")
except ImportError as e:
    print(f"✗ Erro ao importar: {e}")
    exit(1)

# Teste 2: Criar labirinto
print("\n[2/4] Testando criação de labirinto...")
try:
    maze_str = """
    S 0 1 0 0
    0 0 1 0 1
    1 0 1 0 0
    1 0 0 E 1
    """
    maze = Maze.from_string(maze_str)
    print(f"✓ Labirinto criado: {maze.rows}x{maze.cols}")
except Exception as e:
    print(f"✗ Erro: {e}")
    exit(1)

# Teste 3: Executar A*
print("\n[3/4] Testando algoritmo A*...")
try:
    result = a_star(maze.grid, maze.start, maze.end, allow_diagonal=False)
    if result:
        path, cost = result
        print(f"✓ Caminho encontrado com {len(path)} células e custo {cost:.2f}")
    else:
        print("✗ Nenhum caminho encontrado")
        exit(1)
except Exception as e:
    print(f"✗ Erro: {e}")
    exit(1)

# Teste 4: Visualizar
print("\n[4/4] Testando visualização...")
try:
    visualize_solution(maze, path, cost, colored=False)
    print("\n✓ Visualização OK!")
except Exception as e:
    print(f"✗ Erro: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 70)
print("\n💡 Para testar com GUI, instale pygame e execute:")
print("   macOS/Linux: python3 main.py --example 1")
print("   Windows:     python main.py --example 1")
print("=" * 70)
