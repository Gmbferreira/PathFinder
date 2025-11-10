"""
Programa principal - Integração de todos os módulos do PathFinder A*.
Autor: Felipe Evangelista
Branch: feature/main-integration
"""

import sys
import argparse
from typing import Optional
from src.maze import Maze
from src.pathfinder import a_star
from src.visualizer import visualize_solution, print_header
from src.gui import visualize_maze_gui


def run_pathfinder(maze: Maze, allow_diagonal: bool = False, 
                   use_gui: bool = True, use_euclidean: bool = False) -> None:
    """
    Executa o algoritmo A* em um labirinto e visualiza o resultado.
    
    Args:
        maze: Objeto Maze
        allow_diagonal: Permitir movimentos diagonais
        use_gui: Usar interface gráfica (Pygame)
        use_euclidean: Usar distância Euclidiana ao invés de Manhattan
    """
    print_header("PATHFINDER A* - ENCONTRANDO O MENOR CAMINHO")
    
    print(f"\nConfigurações:")
    print(f"  • Movimentos diagonais: {'Sim' if allow_diagonal else 'Não'}")
    print(f"  • Heurística: {'Euclidiana' if use_euclidean else 'Manhattan'}")
    print(f"  • Interface: {'Gráfica (Pygame)' if use_gui else 'Console'}")
    
    print(f"\nDimensões do labirinto: {maze.rows}x{maze.cols}")
    print(f"Início: {maze.start}")
    print(f"Fim: {maze.end}")
    
    # Lista para armazenar células exploradas
    explored_cells = set()
    
    def exploration_callback(position, f_cost):
        """Callback para rastrear exploração."""
        explored_cells.add(position)
    
    print("\n🔍 Executando algoritmo A*...\n")
    
    # Executa o A*
    result = a_star(
        maze.grid,
        maze.start,
        maze.end,
        allow_diagonal=allow_diagonal,
        use_euclidean=use_euclidean,
        exploration_callback=exploration_callback
    )
    
    # Processa resultado
    if result:
        path, cost = result
        
        # Visualização no console
        visualize_solution(maze, path, cost, explored_cells, colored=True)
        
        # Visualização gráfica (se habilitado)
        if use_gui:
            try:
                print("\n📊 Abrindo visualização gráfica...")
                print("   (Pressione ESC ou feche a janela para sair)")
                visualize_maze_gui(maze, path, cost, explored_cells)
            except Exception as e:
                print(f"\n⚠ Erro ao abrir GUI: {e}")
                print("   Continuando apenas com visualização em console.")
    else:
        # Sem solução
        visualize_solution(maze, None, None, explored_cells, colored=True)
        
        if use_gui:
            try:
                print("\n📊 Abrindo visualização gráfica...")
                visualize_maze_gui(maze, None, None, explored_cells)
            except Exception as e:
                print(f"\n⚠ Erro ao abrir GUI: {e}")


def main():
    """Função principal com interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description='PathFinder A* - Resolve labirintos usando o algoritmo A*',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                          # Executa exemplo 1
  python main.py --example 2              # Executa exemplo 2
  python main.py --diagonal               # Permite movimentos diagonais
  python main.py --no-gui                 # Apenas visualização em console
  python main.py --example 3 --diagonal   # Exemplo 3 com diagonais
        """
    )
    
    parser.add_argument(
        '--example', '-e',
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=1,
        help='Número do exemplo a executar (1-5)'
    )
    
    parser.add_argument(
        '--diagonal', '-d',
        action='store_true',
        help='Permite movimentos diagonais (custo √2)'
    )
    
    parser.add_argument(
        '--no-gui', '-ng',
        action='store_true',
        help='Desabilita interface gráfica (apenas console)'
    )
    
    parser.add_argument(
        '--euclidean', '-eu',
        action='store_true',
        help='Usa distância Euclidiana ao invés de Manhattan'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Carrega labirinto de um arquivo'
    )
    
    args = parser.parse_args()
    
    # Carrega labirinto
    if args.file:
        try:
            with open(args.file, 'r') as f:
                maze_string = f.read()
            maze = Maze.from_string(maze_string)
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo '{args.file}' não encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Erro ao carregar arquivo: {e}")
            sys.exit(1)
    else:
        # Carrega exemplo pré-definido
        from examples.maze_examples import get_example
        maze = get_example(args.example)
    
    # Executa PathFinder
    try:
        run_pathfinder(
            maze,
            allow_diagonal=args.diagonal,
            use_gui=not args.no_gui,
            use_euclidean=args.euclidean
        )
    except KeyboardInterrupt:
        print("\n\n⚠ Execução interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
