"""
Módulo para visualização de labirintos no console com cores.
Autor: Rafael Marques Radieddine
Branch: feature/console-visualizer
"""

from typing import List, Tuple, Optional, Set
from src.maze import Maze
import sys


class Colors:
    """Códigos ANSI para cores no terminal."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Cores de texto
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Cores de fundo
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_GRAY = '\033[100m'


class Symbols:
    """Símbolos Unicode para melhor visualização."""
    WALL = '█'  # Obstáculo
    PATH = '•'  # Caminho
    START = 'S'  # Início
    END = 'E'  # Fim
    EMPTY = '·'  # Célula vazia
    EXPLORED = '░'  # Célula explorada
    ROBOT = '◉'  # Robô


def print_maze_simple(maze: Maze, path: Optional[List[Tuple[int, int]]] = None,
                     explored: Optional[Set[Tuple[int, int]]] = None) -> None:
    """
    Imprime o labirinto de forma simples (compatível com qualquer terminal).
    
    Args:
        maze: Objeto Maze a ser visualizado
        path: Lista de posições formando o caminho (opcional)
        explored: Conjunto de posições exploradas pelo algoritmo (opcional)
    """
    path_set = set(path) if path else set()
    explored_set = explored if explored else set()
    
    print("\nLabirinto:")
    print("=" * (maze.cols * 2 + 1))
    
    for i in range(maze.rows):
        line = ""
        for j in range(maze.cols):
            pos = (i, j)
            
            if pos == maze.start:
                line += "S "
            elif pos == maze.end:
                line += "E "
            elif maze.grid[i][j] == -1:
                line += "1 "
            elif pos in path_set:
                line += "* "
            elif pos in explored_set:
                line += ". "
            else:
                line += "0 "
        
        print(line.rstrip())
    
    print("=" * (maze.cols * 2 + 1))


def print_maze_colored(maze: Maze, path: Optional[List[Tuple[int, int]]] = None,
                       explored: Optional[Set[Tuple[int, int]]] = None,
                       show_weights: bool = False) -> None:
    """
    Imprime o labirinto com cores e símbolos Unicode (requer terminal com suporte).
    
    Args:
        maze: Objeto Maze a ser visualizado
        path: Lista de posições formando o caminho (opcional)
        explored: Conjunto de posições exploradas pelo algoritmo (opcional)
        show_weights: Se True, mostra os pesos das células
    """
    path_set = set(path) if path else set()
    explored_set = explored if explored else set()
    
    print(f"\n{Colors.BOLD}Labirinto ({maze.rows}x{maze.cols}):{Colors.RESET}")
    print("┌" + "─" * (maze.cols * 2) + "┐")
    
    for i in range(maze.rows):
        line = "│"
        for j in range(maze.cols):
            pos = (i, j)
            cell_value = maze.grid[i][j]
            
            if pos == maze.start:
                line += f"{Colors.BG_GREEN}{Colors.BOLD}{Symbols.START}{Colors.RESET} "
            elif pos == maze.end:
                line += f"{Colors.BG_BLUE}{Colors.BOLD}{Symbols.END}{Colors.RESET} "
            elif cell_value == -1:
                line += f"{Colors.GRAY}{Symbols.WALL}{Colors.RESET} "
            elif pos in path_set:
                line += f"{Colors.GREEN}{Colors.BOLD}{Symbols.PATH}{Colors.RESET} "
            elif pos in explored_set:
                line += f"{Colors.YELLOW}{Symbols.EXPLORED}{Colors.RESET} "
            else:
                if show_weights and cell_value > 1:
                    weight_color = Colors.CYAN if cell_value <= 3 else Colors.MAGENTA
                    line += f"{weight_color}{cell_value}{Colors.RESET} "
                else:
                    line += f"{Colors.GRAY}{Symbols.EMPTY}{Colors.RESET} "
        
        print(line + "│")
    
    print("└" + "─" * (maze.cols * 2) + "┘")


def print_path_coordinates(path: List[Tuple[int, int]], maze: Maze) -> None:
    """
    Imprime as coordenadas do caminho de forma formatada.
    
    Args:
        path: Lista de coordenadas do caminho
        maze: Objeto Maze (para destacar início e fim)
    """
    if not path:
        print(f"\n{Colors.RED}Nenhum caminho encontrado.{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}Menor caminho encontrado:{Colors.RESET}")
    print(f"Comprimento: {len(path)} células\n")
    
    formatted_path = []
    for i, pos in enumerate(path):
        if pos == maze.start:
            formatted_path.append(f"{Colors.GREEN}s{pos}{Colors.RESET}")
        elif pos == maze.end:
            formatted_path.append(f"{Colors.BLUE}e{pos}{Colors.RESET}")
        else:
            formatted_path.append(str(pos))
    
    # Imprime em formato de lista
    path_str = "[" + ", ".join(formatted_path) + "]"
    
    # Quebra em múltiplas linhas se necessário
    if len(path_str) > 80:
        print("[")
        for i, coord in enumerate(formatted_path):
            if i < len(formatted_path) - 1:
                print(f"  {coord},")
            else:
                print(f"  {coord}")
        print("]")
    else:
        print(path_str)


def print_statistics(maze: Maze, path: Optional[List[Tuple[int, int]]] = None,
                    cost: Optional[float] = None, nodes_explored: Optional[int] = None) -> None:
    """
    Imprime estatísticas sobre o labirinto e a busca.
    
    Args:
        maze: Objeto Maze
        path: Caminho encontrado (opcional)
        cost: Custo total do caminho (opcional)
        nodes_explored: Número de nós explorados (opcional)
    """
    stats = maze.get_statistics()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}═══ Estatísticas ═══{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Labirinto:{Colors.RESET}")
    print(f"  • Dimensões: {stats['dimensions'][0]} × {stats['dimensions'][1]}")
    print(f"  • Total de células: {stats['total_cells']}")
    print(f"  • Células livres: {stats['free_cells']}")
    print(f"  • Obstáculos: {stats['obstacles']} ({stats['obstacle_percentage']:.1f}%)")
    print(f"  • Peso médio: {stats['average_weight']:.2f}")
    print(f"  • Início: {stats['start']}")
    print(f"  • Fim: {stats['end']}")
    
    if path:
        print(f"\n{Colors.BOLD}Caminho:{Colors.RESET}")
        print(f"  • Comprimento: {len(path)} células")
        if cost is not None:
            print(f"  • Custo total: {Colors.GREEN}{cost:.2f}{Colors.RESET}")
    
    if nodes_explored is not None:
        print(f"\n{Colors.BOLD}Busca:{Colors.RESET}")
        print(f"  • Nós explorados: {nodes_explored}")
        if path:
            efficiency = (len(path) / nodes_explored) * 100
            print(f"  • Eficiência: {efficiency:.1f}%")


def print_legend() -> None:
    """Imprime a legenda dos símbolos usados na visualização."""
    print(f"\n{Colors.BOLD}Legenda:{Colors.RESET}")
    print(f"  {Colors.BG_GREEN}{Symbols.START}{Colors.RESET} = Início")
    print(f"  {Colors.BG_BLUE}{Symbols.END}{Colors.RESET} = Fim")
    print(f"  {Colors.GRAY}{Symbols.WALL}{Colors.RESET} = Obstáculo")
    print(f"  {Colors.GREEN}{Colors.BOLD}{Symbols.PATH}{Colors.RESET} = Caminho")
    print(f"  {Colors.YELLOW}{Symbols.EXPLORED}{Colors.RESET} = Explorado")
    print(f"  {Colors.GRAY}{Symbols.EMPTY}{Colors.RESET} = Célula livre")


def visualize_solution(maze: Maze, path: Optional[List[Tuple[int, int]]] = None,
                       cost: Optional[float] = None, explored: Optional[Set[Tuple[int, int]]] = None,
                       colored: bool = True, show_stats: bool = True) -> None:
    """
    Visualização completa da solução do labirinto.
    
    Args:
        maze: Objeto Maze
        path: Caminho encontrado (opcional)
        cost: Custo do caminho (opcional)
        explored: Posições exploradas (opcional)
        colored: Se True, usa visualização colorida
        show_stats: Se True, mostra estatísticas
    """
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{Colors.CYAN}PATHFINDER A* - SOLUÇÃO DO LABIRINTO{Colors.RESET}")
    print("=" * 70)
    
    # Visualiza o labirinto
    if colored and sys.stdout.isatty():
        print_maze_colored(maze, path, explored)
        print_legend()
    else:
        print_maze_simple(maze, path, explored)
    
    # Mostra coordenadas do caminho
    if path:
        print_path_coordinates(path, maze)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Sem solução!{Colors.RESET}")
        print("Não existe caminho válido entre o ponto inicial e final.")
    
    # Estatísticas
    if show_stats:
        nodes_count = len(explored) if explored else None
        print_statistics(maze, path, cost, nodes_count)
    
    print("\n" + "=" * 70 + "\n")


def print_header(title: str) -> None:
    """
    Imprime um cabeçalho formatado.
    
    Args:
        title: Título a ser exibido
    """
    width = max(70, len(title) + 10)
    print("\n" + "=" * width)
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(width)}{Colors.RESET}")
    print("=" * width)


def animate_exploration(position: Tuple[int, int], f_cost: float) -> None:
    """
    Callback para animação da exploração (versão simples para console).
    
    Args:
        position: Posição sendo explorada
        f_cost: Custo f do nó
    """
    # Esta é uma versão simples; pode ser expandida para animação real
    pass


# Função auxiliar para testes
if __name__ == "__main__":
    from src.maze import Maze
    
    # Teste de visualização
    test_maze_str = """
    S 0 1 0 0
    0 0 1 0 1
    1 0 1 0 0
    1 0 0 E 1
    """
    
    maze = Maze.from_string(test_maze_str)
    path = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
    explored = {(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (3, 1), (3, 2), (3, 3)}
    
    visualize_solution(maze, path, 7.0, explored)
