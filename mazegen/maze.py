import random
from typing import List, Dict, Tuple


class MazeGenerator:
    """Generates a maze using recursive backtracker algorithm."""

    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 seed: int = 42, perfect: bool = True) -> None:
        """Initialize the maze with given dimensions and settings."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.solution: List[str] = []
        random.seed(seed)
        self.grid: List[List[Dict[str, bool]]] = self._init_grid()

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
               visited: List[List[bool]]) -> None:
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
                self._carve(nx, ny, visited)

    def generate(self) -> 'MazeGenerator':
        """Generate the maze and return self."""
        visited: List[List[bool]] = [
            [False] * self.width for _ in range(self.height)
        ]
        start_x, start_y = self.entry
        self._carve(start_x, start_y, visited)
        return self
