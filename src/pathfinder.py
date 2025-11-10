"""
PathFinder - Implementação do Algoritmo A* para resolução de labirintos 2D
Autor: Pedro Carbonaro
Descrição: Contém a implementação central do algoritmo A* com suporte a movimentos
           ortogonais e diagonais, incluindo a função heurística de Manhattan.
"""

import heapq
from typing import List, Tuple, Optional, Set
import math


class Node:
    """
    Representa um nó (célula) no labirinto durante a busca A*.
    
    Atributos:
        position (Tuple[int, int]): Coordenadas (linha, coluna) do nó
        parent (Optional[Node]): Nó pai no caminho (para reconstrução do caminho)
        g_cost (float): Custo real do caminho do início até este nó
        h_cost (float): Estimativa heurística do custo deste nó até o objetivo
        f_cost (float): Custo total (f = g + h)
    """
    
    def __init__(self, position: Tuple[int, int], parent: Optional['Node'] = None):
        """
        Inicializa um novo nó.
        
        Args:
            position: Tupla (linha, coluna) representando a posição no labirinto
            parent: Nó pai no caminho (None para o nó inicial)
        """
        self.position = position
        self.parent = parent
        self.g_cost = 0.0  # Custo do início até este nó
        self.h_cost = 0.0  # Estimativa heurística até o objetivo
        self.f_cost = 0.0  # Custo total (g + h)
    
    def __eq__(self, other) -> bool:
        """Compara dois nós baseado em suas posições."""
        if not isinstance(other, Node):
            return False
        return self.position == other.position
    
    def __lt__(self, other) -> bool:
        """Comparação para a fila de prioridade (heap)."""
        return self.f_cost < other.f_cost
    
    def __hash__(self) -> int:
        """Hash baseado na posição para uso em sets."""
        return hash(self.position)
    
    def __repr__(self) -> str:
        """Representação em string do nó."""
        return f"Node({self.position}, f={self.f_cost:.2f})"


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calcula a distância de Manhattan entre duas posições.
    
    A distância de Manhattan é a soma das diferenças absolutas das coordenadas.
    É uma heurística admissível para movimentos ortogonais (cima, baixo, esquerda, direita).
    
    Fórmula: h(n) = |x1 - x2| + |y1 - y2|
    
    Args:
        pos1: Tupla (linha, coluna) da primeira posição
        pos2: Tupla (linha, coluna) da segunda posição
    
    Returns:
        float: Distância de Manhattan entre as duas posições
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calcula a distância Euclidiana entre duas posições.
    
    Útil quando movimentos diagonais são permitidos.
    
    Fórmula: h(n) = √((x1 - x2)² + (y1 - y2)²)
    
    Args:
        pos1: Tupla (linha, coluna) da primeira posição
        pos2: Tupla (linha, coluna) da segunda posição
    
    Returns:
        float: Distância Euclidiana entre as duas posições
    """
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def get_neighbors(position: Tuple[int, int], rows: int, cols: int, 
                  allow_diagonal: bool = False) -> List[Tuple[Tuple[int, int], float]]:
    """
    Retorna os vizinhos válidos de uma posição no labirinto.
    
    Args:
        position: Posição atual (linha, coluna)
        rows: Número de linhas no labirinto
        cols: Número de colunas no labirinto
        allow_diagonal: Se True, permite movimentos diagonais
    
    Returns:
        Lista de tuplas (posição_vizinha, custo_movimento)
    """
    row, col = position
    neighbors = []
    
    # Movimentos ortogonais (custo 1.0)
    orthogonal_moves = [
        (-1, 0),  # Cima
        (1, 0),   # Baixo
        (0, -1),  # Esquerda
        (0, 1)    # Direita
    ]
    
    for dr, dc in orthogonal_moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append(((new_row, new_col), 1.0))
    
    # Movimentos diagonais (custo √2 ≈ 1.414)
    if allow_diagonal:
        diagonal_moves = [
            (-1, -1),  # Cima-Esquerda
            (-1, 1),   # Cima-Direita
            (1, -1),   # Baixo-Esquerda
            (1, 1)     # Baixo-Direita
        ]
        
        for dr, dc in diagonal_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors.append(((new_row, new_col), math.sqrt(2)))
    
    return neighbors


def reconstruct_path(node: Node) -> List[Tuple[int, int]]:
    """
    Reconstrói o caminho do início até o nó atual seguindo os pais.
    
    Args:
        node: Nó final (objetivo)
    
    Returns:
        Lista de posições formando o caminho do início ao fim
    """
    path = []
    current = node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Inverte para obter do início ao fim


def a_star(maze_grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int],
           allow_diagonal: bool = False, use_euclidean: bool = False,
           exploration_callback=None) -> Optional[Tuple[List[Tuple[int, int]], float]]:
    """
    Implementação do Algoritmo A* para encontrar o menor caminho em um labirinto.
    
    O A* combina:
    - g(n): custo real do caminho do início até o nó atual
    - h(n): estimativa heurística do custo do nó atual até o objetivo
    - f(n) = g(n) + h(n): função de avaliação total
    
    Args:
        maze_grid: Matriz representando o labirinto (valores são pesos das células)
        start: Posição inicial (linha, coluna)
        end: Posição objetivo (linha, coluna)
        allow_diagonal: Se True, permite movimentos diagonais
        use_euclidean: Se True, usa distância Euclidiana; caso contrário, Manhattan
        exploration_callback: Função chamada a cada nó explorado (para visualização)
    
    Returns:
        Tupla (caminho, custo_total) se encontrado, None caso contrário
        - caminho: Lista de posições do início ao fim
        - custo_total: Custo total do caminho encontrado
    """
    rows = len(maze_grid)
    cols = len(maze_grid[0]) if rows > 0 else 0
    
    # Escolhe a função heurística
    heuristic = euclidean_distance if use_euclidean else manhattan_distance
    
    # Cria o nó inicial
    start_node = Node(start)
    start_node.g_cost = 0
    start_node.h_cost = heuristic(start, end)
    start_node.f_cost = start_node.g_cost + start_node.h_cost
    
    # Listas abertas (a explorar) e fechadas (já exploradas)
    open_list = []
    heapq.heappush(open_list, start_node)
    open_set: Set[Tuple[int, int]] = {start}
    closed_set: Set[Tuple[int, int]] = set()
    
    # Dicionário para rastrear o melhor g_cost para cada posição
    g_costs = {start: 0.0}
    
    # Estatísticas
    nodes_explored = 0
    
    while open_list:
        # Pega o nó com menor f_cost
        current_node = heapq.heappop(open_list)
        current_pos = current_node.position
        
        # Remove da lista aberta
        open_set.discard(current_pos)
        
        # Se já foi explorado com um custo melhor, ignora
        if current_pos in closed_set:
            continue
        
        # Marca como explorado
        closed_set.add(current_pos)
        nodes_explored += 1
        
        # Callback para visualização (se fornecido)
        if exploration_callback:
            exploration_callback(current_pos, current_node.f_cost)
        
        # Verifica se chegou ao objetivo
        if current_pos == end:
            path = reconstruct_path(current_node)
            print(f"\n✓ Caminho encontrado!")
            print(f"  Nós explorados: {nodes_explored}")
            print(f"  Custo total: {current_node.g_cost:.2f}")
            print(f"  Tamanho do caminho: {len(path)} células")
            return path, current_node.g_cost
        
        # Explora os vizinhos
        for neighbor_pos, move_cost in get_neighbors(current_pos, rows, cols, allow_diagonal):
            # Verifica se é obstáculo (valor -1 indica obstáculo)
            if maze_grid[neighbor_pos[0]][neighbor_pos[1]] == -1:
                continue
            
            # Já explorado?
            if neighbor_pos in closed_set:
                continue
            
            # Calcula o custo considerando o peso da célula
            cell_weight = maze_grid[neighbor_pos[0]][neighbor_pos[1]]
            tentative_g_cost = current_node.g_cost + (move_cost * cell_weight)
            
            # Se já encontramos um caminho melhor para este vizinho, ignora
            if neighbor_pos in g_costs and tentative_g_cost >= g_costs[neighbor_pos]:
                continue
            
            # Cria novo nó para o vizinho
            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.g_cost = tentative_g_cost
            neighbor_node.h_cost = heuristic(neighbor_pos, end)
            neighbor_node.f_cost = neighbor_node.g_cost + neighbor_node.h_cost
            
            # Atualiza o melhor custo conhecido
            g_costs[neighbor_pos] = tentative_g_cost
            
            # Adiciona à lista aberta
            if neighbor_pos not in open_set:
                heapq.heappush(open_list, neighbor_node)
                open_set.add(neighbor_pos)
    
    # Não encontrou caminho
    print(f"\n✗ Sem solução!")
    print(f"  Nós explorados: {nodes_explored}")
    return None


# Função auxiliar para testes
if __name__ == "__main__":
    # Exemplo de uso básico
    test_maze = [
        [1, 1, -1, 1, 1],
        [1, 1, -1, 1, -1],
        [1, -1, 1, 1, 1],
        [-1, 1, 1, 1, -1]
    ]
    
    start_pos = (0, 0)
    end_pos = (3, 3)
    
    print("Testando A* com movimentos ortogonais:")
    result = a_star(test_maze, start_pos, end_pos, allow_diagonal=False)
    if result:
        path, cost = result
        print(f"Caminho: {path}")
        print(f"Custo: {cost}")
