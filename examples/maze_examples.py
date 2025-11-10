"""
Maze Examples - Exemplos de labirintos para testes
Autor: Felipe Evangelista
Descrição: Coleção de labirintos pré-definidos para demonstração e testes.
"""

from src.maze import Maze


def get_example(example_number: int) -> Maze:
    """
    Retorna um labirinto de exemplo.
    
    Args:
        example_number: Número do exemplo (1-5)
    
    Returns:
        Objeto Maze
    """
    examples = {
        1: get_example_1,
        2: get_example_2,
        3: get_example_3,
        4: get_example_4,
        5: get_example_5,
    }
    
    if example_number not in examples:
        raise ValueError(f"Exemplo {example_number} não existe. Escolha entre 1-5.")
    
    return examples[example_number]()


def get_example_1() -> Maze:
    """
    Exemplo 1: Labirinto do enunciado do projeto.
    Labirinto simples 4x5 com obstáculos.
    """
    maze_str = """
    S 0 1 0 0
    0 0 1 0 1
    1 0 1 0 0
    1 0 0 E 1
    """
    return Maze.from_string(maze_str)


def get_example_2() -> Maze:
    """
    Exemplo 2: Labirinto médio 8x8.
    Mais complexo com múltiplos caminhos possíveis.
    """
    maze_str = """
    S 0 0 1 0 0 0 1
    0 1 0 1 0 1 0 0
    0 1 0 0 0 1 1 0
    0 0 0 1 0 0 0 0
    1 1 0 1 1 1 0 1
    0 0 0 0 0 0 0 0
    0 1 1 1 1 1 1 0
    0 0 0 0 0 0 0 E
    """
    return Maze.from_string(maze_str)


def get_example_3() -> Maze:
    """
    Exemplo 3: Labirinto grande 12x12.
    Desafio maior com mais obstáculos.
    """
    maze_str = """
    S 0 0 0 1 0 0 0 0 0 0 0
    0 1 1 0 1 0 1 1 1 1 1 0
    0 0 0 0 0 0 0 0 0 0 0 0
    0 1 1 1 1 1 1 1 1 1 1 0
    0 0 0 0 0 0 0 0 0 0 0 0
    1 1 1 1 1 0 1 1 1 1 1 1
    0 0 0 0 0 0 0 0 0 0 0 0
    0 1 1 1 1 1 1 1 1 1 1 0
    0 0 0 0 0 0 0 0 0 0 0 0
    0 1 1 1 1 1 1 1 1 1 0 0
    0 0 0 0 0 0 0 0 0 0 0 1
    1 1 1 1 1 1 1 1 1 1 0 E
    """
    return Maze.from_string(maze_str)


def get_example_4() -> Maze:
    """
    Exemplo 4: Labirinto com diferentes pesos de terreno.
    Demonstra o conceito de terrenos com custos variados.
    """
    maze_str = """
    S 1 1 5 5 5
    1 1 1 5 5 5
    2 2 1 1 5 5
    2 2 2 1 1 1
    3 3 2 2 1 E
    """
    return Maze.from_string(maze_str)


def get_example_5() -> Maze:
    """
    Exemplo 5: Labirinto sem solução.
    O ponto final está completamente bloqueado.
    """
    maze_str = """
    S 0 0 0 0
    0 1 1 1 0
    0 1 E 1 0
    0 1 1 1 0
    0 0 0 0 0
    """
    return Maze.from_string(maze_str)


def print_all_examples():
    """Imprime todos os exemplos disponíveis."""
    from src.visualizer import print_maze_simple
    
    print("=" * 70)
    print("EXEMPLOS DE LABIRINTOS DISPONÍVEIS")
    print("=" * 70)
    
    descriptions = {
        1: "Labirinto do enunciado (4x5) - Simples",
        2: "Labirinto médio (8x8) - Complexidade média",
        3: "Labirinto grande (12x12) - Desafiador",
        4: "Labirinto com pesos (5x6) - Terrenos variados",
        5: "Labirinto sem solução (5x5) - Impossível"
    }
    
    for i in range(1, 6):
        print(f"\n{'='*70}")
        print(f"EXEMPLO {i}: {descriptions[i]}")
        print('='*70)
        maze = get_example(i)
        print_maze_simple(maze)
        stats = maze.get_statistics()
        print(f"\nDimensões: {stats['dimensions'][0]}x{stats['dimensions'][1]}")
        print(f"Células livres: {stats['free_cells']} | Obstáculos: {stats['obstacles']}")
        print(f"Início: {stats['start']} | Fim: {stats['end']}")


if __name__ == "__main__":
    print_all_examples()
