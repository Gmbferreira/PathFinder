"""
Maze - Representação e validação de labirintos
Autor: Bruna Barbosa
Descrição: Classe para representar labirintos 2D, incluindo parsing de entrada,
           validação de estrutura e conversão entre diferentes formatos.
"""

from typing import List, Tuple, Optional, Dict


class Maze:
    """
    Representa um labirinto 2D com métodos para validação e manipulação.
    
    Convenções:
        - Células livres: representadas por 'S', 'E', '0', ou valores numéricos >= 1
        - Obstáculos: representados por '1' (na notação do projeto) ou -1 internamente
        - Início: 'S' ou 's'
        - Fim: 'E' ou 'e'
        - Pesos: valores numéricos indicam custo de travessia
    
    Atributos:
        grid (List[List[int]]): Matriz numérica do labirinto
        rows (int): Número de linhas
        cols (int): Número de colunas
        start (Tuple[int, int]): Posição inicial (linha, coluna)
        end (Tuple[int, int]): Posição final (linha, coluna)
        original_grid (List[List[str]]): Grid original antes da conversão
    """
    
    def __init__(self, input_maze: List[List[str]]):
        """
        Inicializa um labirinto a partir de uma matriz de strings.
        
        Args:
            input_maze: Matriz de strings representando o labirinto
        
        Raises:
            ValueError: Se o labirinto for inválido (formato, sem S/E, etc.)
        """
        self.original_grid = [row[:] for row in input_maze]  # Cópia profunda
        self.rows = len(input_maze)
        self.cols = len(input_maze[0]) if self.rows > 0 else 0
        self.start: Optional[Tuple[int, int]] = None
        self.end: Optional[Tuple[int, int]] = None
        self.grid: List[List[int]] = []
        
        # Valida e converte o labirinto
        self._validate_structure()
        self._find_start_end()
        self._convert_to_numeric()
    
    def _validate_structure(self) -> None:
        """
        Valida a estrutura básica do labirinto.
        
        Raises:
            ValueError: Se o labirinto tiver formato inválido
        """
        if self.rows == 0:
            raise ValueError("Labirinto vazio! O labirinto deve ter ao menos uma célula.")
        
        if self.cols == 0:
            raise ValueError("Labirinto sem colunas! Cada linha deve ter ao menos uma célula.")
        
        # Verifica se todas as linhas têm o mesmo número de colunas
        for i, row in enumerate(self.original_grid):
            if len(row) != self.cols:
                raise ValueError(
                    f"Linha {i} tem {len(row)} colunas, mas esperava-se {self.cols} colunas. "
                    f"Todas as linhas devem ter o mesmo tamanho."
                )
    
    def _find_start_end(self) -> None:
        """
        Encontra as posições de início (S) e fim (E) no labirinto.
        
        Raises:
            ValueError: Se S ou E não forem encontrados ou houver duplicatas
        """
        start_found = False
        end_found = False
        
        for i in range(self.rows):
            for j in range(self.cols):
                cell = str(self.original_grid[i][j]).strip().upper()
                
                if cell == 'S':
                    if start_found:
                        raise ValueError(
                            f"Múltiplos pontos de início encontrados! "
                            f"Apenas um 'S' deve estar presente no labirinto."
                        )
                    self.start = (i, j)
                    start_found = True
                
                elif cell == 'E':
                    if end_found:
                        raise ValueError(
                            f"Múltiplos pontos de fim encontrados! "
                            f"Apenas um 'E' deve estar presente no labirinto."
                        )
                    self.end = (i, j)
                    end_found = True
        
        if not start_found:
            raise ValueError(
                "Ponto de início 'S' não encontrado! "
                "O labirinto deve conter exatamente um 'S'."
            )
        
        if not end_found:
            raise ValueError(
                "Ponto de fim 'E' não encontrado! "
                "O labirinto deve conter exatamente um 'E'."
            )
    
    def _convert_to_numeric(self) -> None:
        """
        Converte o labirinto de strings para valores numéricos.
        
        Convenção interna:
            -1: Obstáculo (célula bloqueada)
            >= 1: Célula livre (valor indica peso/custo de travessia)
        """
        self.grid = []
        
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = str(self.original_grid[i][j]).strip().upper()
                
                if cell == 'S' or cell == 'E':
                    # Início e fim são células livres com peso 1
                    row.append(1)
                elif cell == '0':
                    # Célula livre padrão com peso 1
                    row.append(1)
                elif cell == '1':
                    # Obstáculo (na notação do projeto, '1' é obstáculo)
                    row.append(-1)
                else:
                    # Tenta converter para número (pode ser peso customizado)
                    try:
                        value = int(cell)
                        if value < 0:
                            # Valores negativos são obstáculos
                            row.append(-1)
                        elif value == 0:
                            # Zero tratado como célula livre peso 1
                            row.append(1)
                        else:
                            # Valor positivo é o peso da célula
                            row.append(value)
                    except ValueError:
                        # Caractere desconhecido, trata como obstáculo
                        row.append(-1)
            
            self.grid.append(row)
    
    @staticmethod
    def from_string(maze_string: str) -> 'Maze':
        """
        Cria um labirinto a partir de uma string multi-linha.
        
        Args:
            maze_string: String representando o labirinto (linhas separadas por \\n)
        
        Returns:
            Objeto Maze
        
        Example:
            >>> maze_str = '''
            ... S 0 1 0 0
            ... 0 0 1 0 1
            ... 1 0 1 0 0
            ... 1 0 0 E 1
            ... '''
            >>> maze = Maze.from_string(maze_str)
        """
        lines = maze_string.strip().split('\n')
        maze_grid = [line.split() for line in lines if line.strip()]
        return Maze(maze_grid)
    
    @staticmethod
    def from_array(maze_array: List[List]) -> 'Maze':
        """
        Cria um labirinto a partir de uma matriz (lista de listas).
        
        Args:
            maze_array: Matriz representando o labirinto
        
        Returns:
            Objeto Maze
        """
        maze_grid = [[str(cell) for cell in row] for row in maze_array]
        return Maze(maze_grid)
    
    def get_dimensions(self) -> Tuple[int, int]:
        """Retorna as dimensões do labirinto (linhas, colunas)."""
        return self.rows, self.cols
    
    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Verifica se uma posição está dentro dos limites do labirinto.
        
        Args:
            position: Tupla (linha, coluna)
        
        Returns:
            True se a posição é válida, False caso contrário
        """
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_obstacle(self, position: Tuple[int, int]) -> bool:
        """
        Verifica se uma posição é um obstáculo.
        
        Args:
            position: Tupla (linha, coluna)
        
        Returns:
            True se a posição é um obstáculo, False caso contrário
        """
        if not self.is_valid_position(position):
            return True  # Fora dos limites é considerado obstáculo
        row, col = position
        return self.grid[row][col] == -1
    
    def get_cell_weight(self, position: Tuple[int, int]) -> int:
        """
        Retorna o peso (custo) de uma célula.
        
        Args:
            position: Tupla (linha, coluna)
        
        Returns:
            Peso da célula (-1 para obstáculos)
        """
        if not self.is_valid_position(position):
            return -1
        row, col = position
        return self.grid[row][col]
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas sobre o labirinto.
        
        Returns:
            Dicionário com informações estatísticas
        """
        total_cells = self.rows * self.cols
        obstacles = sum(1 for row in self.grid for cell in row if cell == -1)
        free_cells = total_cells - obstacles
        
        # Calcula peso médio das células livres
        free_weights = [cell for row in self.grid for cell in row if cell > 0]
        avg_weight = sum(free_weights) / len(free_weights) if free_weights else 0
        
        return {
            'dimensions': (self.rows, self.cols),
            'total_cells': total_cells,
            'free_cells': free_cells,
            'obstacles': obstacles,
            'obstacle_percentage': (obstacles / total_cells) * 100,
            'average_weight': avg_weight,
            'start': self.start,
            'end': self.end
        }
    
    def __str__(self) -> str:
        """Retorna uma representação em string do labirinto."""
        lines = []
        for i, row in enumerate(self.original_grid):
            lines.append(' '.join(str(cell) for cell in row))
        return '\n'.join(lines)
    
    def __repr__(self) -> str:
        """Representação formal do objeto."""
        return f"Maze({self.rows}x{self.cols}, start={self.start}, end={self.end})"


# Função auxiliar para testes
if __name__ == "__main__":
    # Teste básico
    print("=== Teste 1: Labirinto do enunciado ===")
    test_maze_str = """
    S 0 1 0 0
    0 0 1 0 1
    1 0 1 0 0
    1 0 0 E 1
    """
    
    try:
        maze = Maze.from_string(test_maze_str)
        print(f"Labirinto criado: {maze}")
        print(f"\nGrid numérico:")
        for row in maze.grid:
            print(row)
        print(f"\nEstatísticas:")
        stats = maze.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    except ValueError as e:
        print(f"Erro: {e}")
    
    # Teste com labirinto inválido
    print("\n\n=== Teste 2: Labirinto sem ponto final ===")
    invalid_maze_str = """
    S 0 1 0 0
    0 0 1 0 1
    """
    
    try:
        maze = Maze.from_string(invalid_maze_str)
    except ValueError as e:
        print(f"Erro esperado capturado: {e}")
