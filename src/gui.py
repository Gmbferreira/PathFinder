"""
Módulo para interface gráfica do PathFinder usando Pygame.
Autor: Guilherme Martini
Branch: feature/gui-pygame
"""import pygame
import sys
import time
from typing import List, Tuple, Optional, Set
from src.maze import Maze


class MazeGUI:
    """
    Interface gráfica para visualização de labirintos e algoritmo A*.
    
    Atributos:
        cell_size (int): Tamanho de cada célula em pixels
        margin (int): Margem entre células em pixels
        fps (int): Frames por segundo para animação
    """
    
    # Cores (RGB)
    COLOR_BACKGROUND = (245, 245, 245)
    COLOR_WALL = (50, 50, 50)
    COLOR_FREE = (255, 255, 255)
    COLOR_START = (76, 175, 80)
    COLOR_END = (33, 150, 243)
    COLOR_PATH = (255, 235, 59)
    COLOR_EXPLORED = (200, 230, 201)
    COLOR_CURRENT = (255, 152, 0)
    COLOR_GRID = (200, 200, 200)
    COLOR_TEXT = (50, 50, 50)
    
    # Cores para diferentes pesos de terreno
    TERRAIN_COLORS = {
        1: (255, 255, 255),   # Branco - terreno normal
        2: (255, 248, 220),   # Amarelo claro - custo baixo
        3: (255, 235, 205),   # Bege
        4: (255, 222, 173),   # Navajo white
        5: (255, 200, 124),   # Laranja claro
        6: (255, 160, 122),   # Salmão claro
        7: (240, 128, 128),   # Coral claro
        8: (205, 92, 92),     # Indian red
        9: (178, 34, 34),     # Firebrick
        10: (139, 0, 0)       # Vermelho escuro - custo alto
    }
    
    def __init__(self, maze: Maze, cell_size: int = 40, margin: int = 2, fps: int = 30):
        """
        Inicializa a interface gráfica.
        
        Args:
            maze: Objeto Maze a ser visualizado
            cell_size: Tamanho de cada célula em pixels
            margin: Espaçamento entre células
            fps: Frames por segundo para animação
        """
        self.maze = maze
        self.cell_size = cell_size
        self.margin = margin
        self.fps = fps
        
        # Calcula dimensões da janela
        self.info_panel_width = 300
        self.info_panel_height = 150
        self.grid_width = maze.cols * (cell_size + margin) + margin
        self.grid_height = maze.rows * (cell_size + margin) + margin
        self.window_width = self.grid_width + self.info_panel_width
        self.window_height = max(self.grid_height, self.info_panel_height) + 100
        
        # Estado da visualização
        self.explored_cells: Set[Tuple[int, int]] = set()
        self.current_cell: Optional[Tuple[int, int]] = None
        self.path: Optional[List[Tuple[int, int]]] = None
        self.cost: float = 0.0
        self.is_complete: bool = False
        self.animation_speed: float = 0.05  # segundos entre frames
        
        # Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("PathFinder A* - Visualização")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_large = pygame.font.Font(None, 36)
    
    def get_cell_color(self, row: int, col: int) -> Tuple[int, int, int]:
        """
        Retorna a cor apropriada para uma célula.
        
        Args:
            row: Linha da célula
            col: Coluna da célula
        
        Returns:
            Tupla RGB da cor
        """
        pos = (row, col)
        cell_value = self.maze.grid[row][col]
        
        # Prioridade: caminho > atual > explorado > especiais > terreno
        if self.path and pos in self.path:
            return self.COLOR_PATH
        elif pos == self.current_cell and not self.is_complete:
            return self.COLOR_CURRENT
        elif pos in self.explored_cells:
            return self.COLOR_EXPLORED
        elif pos == self.maze.start:
            return self.COLOR_START
        elif pos == self.maze.end:
            return self.COLOR_END
        elif cell_value == -1:
            return self.COLOR_WALL
        else:
            # Retorna cor baseada no peso do terreno
            if cell_value in self.TERRAIN_COLORS:
                return self.TERRAIN_COLORS[cell_value]
            elif cell_value > 10:
                return self.TERRAIN_COLORS[10]
            else:
                return self.COLOR_FREE
    
    def draw_grid(self) -> None:
        """Desenha o grid do labirinto."""
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                # Calcula posição do retângulo
                x = col * (self.cell_size + self.margin) + self.margin
                y = row * (self.cell_size + self.margin) + self.margin
                
                # Desenha célula
                color = self.get_cell_color(row, col)
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.cell_size, self.cell_size))
                
                # Desenha borda
                pygame.draw.rect(self.screen, self.COLOR_GRID,
                               (x, y, self.cell_size, self.cell_size), 1)
                
                # Desenha peso da célula (se > 1 e não for obstáculo)
                pos = (row, col)
                cell_value = self.maze.grid[row][col]
                if cell_value > 1 and pos != self.maze.start and pos != self.maze.end:
                    weight_text = self.font_small.render(str(cell_value), True, self.COLOR_TEXT)
                    text_rect = weight_text.get_rect(center=(x + self.cell_size // 2, 
                                                             y + self.cell_size // 2))
                    self.screen.blit(weight_text, text_rect)
                
                # Desenha S ou E
                if pos == self.maze.start:
                    text = self.font.render('S', True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, 
                                                     y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)
                elif pos == self.maze.end:
                    text = self.font.render('E', True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, 
                                                     y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)
    
    def draw_info_panel(self) -> None:
        """Desenha painel de informações."""
        panel_x = self.grid_width + 10
        panel_y = 10
        
        # Título
        title = self.font_large.render("PathFinder A*", True, self.COLOR_TEXT)
        self.screen.blit(title, (panel_x, panel_y))
        
        y_offset = panel_y + 50
        
        # Informações do labirinto
        info_texts = [
            f"Dimensões: {self.maze.rows}x{self.maze.cols}",
            f"Início: {self.maze.start}",
            f"Fim: {self.maze.end}",
            "",
            f"Células exploradas: {len(self.explored_cells)}",
        ]
        
        if self.path:
            info_texts.append(f"Comprimento do caminho: {len(self.path)}")
            info_texts.append(f"Custo total: {self.cost:.2f}")
        
        if self.is_complete:
            if self.path:
                status_text = "✓ Caminho encontrado!"
                status_color = (76, 175, 80)
            else:
                status_text = "✗ Sem solução"
                status_color = (244, 67, 54)
            
            status = self.font.render(status_text, True, status_color)
            self.screen.blit(status, (panel_x, y_offset))
            y_offset += 35
        
        for text in info_texts:
            rendered = self.font_small.render(text, True, self.COLOR_TEXT)
            self.screen.blit(rendered, (panel_x, y_offset))
            y_offset += 25
        
        # Legenda
        legend_y = self.window_height - 150
        legend_title = self.font.render("Legenda:", True, self.COLOR_TEXT)
        self.screen.blit(legend_title, (panel_x, legend_y))
        
        legend_items = [
            (self.COLOR_START, "Início"),
            (self.COLOR_END, "Fim"),
            (self.COLOR_WALL, "Obstáculo"),
            (self.COLOR_PATH, "Caminho"),
            (self.COLOR_EXPLORED, "Explorado"),
        ]
        
        legend_y += 30
        for color, label in legend_items:
            pygame.draw.rect(self.screen, color, (panel_x, legend_y, 15, 15))
            text = self.font_small.render(label, True, self.COLOR_TEXT)
            self.screen.blit(text, (panel_x + 20, legend_y))
            legend_y += 20
    
    def update_exploration(self, position: Tuple[int, int]) -> None:
        """
        Atualiza a visualização com uma nova célula explorada.
        
        Args:
            position: Posição da célula sendo explorada
        """
        self.explored_cells.add(position)
        self.current_cell = position
        self.draw()
    
    def set_path(self, path: List[Tuple[int, int]], cost: float) -> None:
        """
        Define o caminho encontrado.
        
        Args:
            path: Lista de posições formando o caminho
            cost: Custo total do caminho
        """
        self.path = path
        self.cost = cost
        self.is_complete = True
        self.current_cell = None
    
    def set_no_solution(self) -> None:
        """Marca que não há solução."""
        self.is_complete = True
        self.current_cell = None
    
    def draw(self) -> None:
        """Redesenha toda a tela."""
        self.screen.fill(self.COLOR_BACKGROUND)
        self.draw_grid()
        self.draw_info_panel()
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def handle_events(self) -> bool:
        """
        Processa eventos do Pygame.
        
        Returns:
            False se deve fechar a janela, True caso contrário
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def run_animation(self, path: Optional[List[Tuple[int, int]]] = None,
                     cost: Optional[float] = None) -> None:
        """
        Executa animação completa (exploração + caminho).
        
        Args:
            path: Caminho final (opcional)
            cost: Custo do caminho (opcional)
        """
        running = Truex
        
        # Animação inicial
        self.draw()
        time.sleep(0.5)
        
        # Se houver caminho, mostra
        if path:
            self.set_path(path, cost or 0.0)
        else:
            self.set_no_solution()
        
        # Loop principal
        while running:
            running = self.handle_events()
            self.draw()
            time.sleep(0.016)  # ~60 FPS
        
        pygame.quit()
    
    def wait_for_close(self) -> None:
        """Mantém a janela aberta até o usuário fechar."""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        pygame.quit()


def visualize_maze_gui(maze: Maze, path: Optional[List[Tuple[int, int]]] = None,
                       cost: Optional[float] = None, 
                       explored: Optional[Set[Tuple[int, int]]] = None,
                       animate: bool = True) -> None:
    """
    Função auxiliar para visualizar um labirinto com GUI.
    
    Args:
        maze: Objeto Maze
        path: Caminho encontrado (opcional)
        cost: Custo do caminho (opcional)
        explored: Células exploradas (opcional)
        animate: Se True, anima a exploração
    """
    gui = MazeGUI(maze)
    
    if explored:
        gui.explored_cells = explored
    
    if path:
        gui.set_path(path, cost or 0.0)
    elif explored:
        gui.set_no_solution()
    
    gui.draw()
    gui.wait_for_close()


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
    
    visualize_maze_gui(maze, path, 7.0, explored)
