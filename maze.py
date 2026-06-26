import os
import time
import random
from typing import List, Dict, Tuple


class MazeGenerator:
    """Generates a maze using recursive backtracker algorithm."""

    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 seed: int | None = None, perfect: bool = True) -> None:
        """Initialize the maze with given dimensions and settings."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.solution: List[str] = []
        random.seed(seed)
        self.grid: List[List[Dict[str, bool]]] = self._init_grid()

        self.pattern_42_cells: set[Tuple[int, int]] = set()
        self._embed_42_pattern()

    def _init_grid(self) -> List[List[Dict[str, bool]]]:
        """Create empty grid where every cell has all 4 walls closed."""
        grid: List[List[Dict[str, bool]]] = []
        for _ in range(self.height):
            row: List[Dict[str, bool]] = []
            for _ in range(self.width):
                row.append({
                    'N': True,
                    'E': True,
                    'S': True,
                    'W': True,
                })
            grid.append(row)
        return grid

    def _embed_42_pattern(self) -> None:
        """Defines and places the '42' pattern of closed cells in the center."""
        pattern = [
            [1, 0, 1, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 1, 1, 1]
        ]
        p_height = len(pattern)
        p_width = len(pattern[0])

        if self.width < p_width + 4 or self.height < p_height + 4:
            print("Error: Maze size is too small to contain the '42' pattern.")
            return

        start_x = (self.width - p_width) // 2
        start_y = (self.height - p_height) // 2

        for py in range(p_height):
            for px in range(p_width):
                if pattern[py][px] == 1:
                    target_x = start_x + px
                    target_y = start_y + py
                    
                    if (target_x, target_y) != self.entry and (target_x, target_y) != self.exit:
                        self.pattern_42_cells.add((target_x, target_y))

    def is_pattern_42(self, x: int, y: int) -> bool:
        """Check if a specific cell belongs to the '42' pattern.
        
        Useful for applying custom background colors during rendering.
        """
        return (x, y) in self.pattern_42_cells


    def _get_neighbours(self, x: int, y: int) -> List[Tuple[str, int, int]]:
        """Get all valid neighbouring cells."""
        neighbours: List[Tuple[str, int, int]] = []
        if y > 0:
            neighbours.append(('N', x, y - 1))
        if x < self.width - 1:
            neighbours.append(('E', x + 1, y))
        if y < self.height - 1:
            neighbours.append(('S', x, y + 1))
        if x > 0:
            neighbours.append(('W', x - 1, y))
        return neighbours

    def _carve(self, x: int, y: int,
               visited: List[List[bool]],
               animate : bool = False) -> None:
        """Carve paths through the maze using recursive backtracking."""
        visited[y][x] = True
        neighbours = self._get_neighbours(x, y)
        random.shuffle(neighbours)
        opposite: Dict[str, str] = {
            'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'
        }
        for direction, nx, ny in neighbours:
            if not visited[ny][nx]:
                self.grid[y][x][direction] = False
                self.grid[ny][nx][opposite[direction]] = False

                if animate:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    from display import display_maze
                    print("--- Genering Maze (Bonus Animation) ---")
                    display_maze(self) 
                    time.sleep(0.05)   

                self._carve(nx, ny, visited)

    def _generate_prim(self, animate: bool = False) -> None:
            """Generate the maze using Prim's algorithm (Randomized)."""
            import os
            import time

            visited = [[False] * self.width for _ in range(self.height)]
            
            for cx, cy in self.pattern_42_cells:
                visited[cy][cx] = True

            start_x, start_y = self.entry
            visited[start_y][start_x] = True

            walls_list = []
            
            for direction, nx, ny in self._get_neighbours(start_x, start_y):
                if (nx, ny) not in self.pattern_42_cells:
                    walls_list.append((start_x, start_y, direction, nx, ny))

            opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

            while walls_list:
                edge = random.choice(walls_list)
                walls_list.remove(edge)
                
                x, y, direction, nx, ny = edge

                if not visited[ny][nx]:
                    self.grid[y][x][direction] = False
                    self.grid[ny][nx][opposite[direction]] = False
                    
                    visited[ny][nx] = True

                    for next_dir, nnx, nny in self._get_neighbours(nx, ny):
                        if not visited[nny][nnx] and (nnx, nny) not in self.pattern_42_cells:
                            walls_list.append((nx, ny, next_dir, nnx, nny))

                    if animate:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("--- Generating Maze (Prim's Algorithm) ---")
                        from display import display_maze
                        display_maze(self)
                        time.sleep(0.02)

    def generate(self, algorithm: str = "dfs", animate: bool = False) -> 'MazeGenerator':
        """Generate the maze using the selected algorithm."""
        algorithm = algorithm.lower()
        
        if algorithm == "prim":
            self._generate_prim(animate)
        else:
            visited = [[False] * self.width for _ in range(self.height)]
            for cx, cy in self.pattern_42_cells:
                visited[cy][cx] = True
            start_x, start_y = self.entry
            self._carve(start_x, start_y, visited, animate)
            
        return self
