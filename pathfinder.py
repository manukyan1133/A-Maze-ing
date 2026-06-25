from collections import deque
from typing import List, Tuple, Dict, Set
from maze import MazeGenerator


def find_path(maze: MazeGenerator) -> List[str]:
    """Find shortest path from entry to exit using BFS."""
    start = maze.entry
    end = maze.exit

    queue: deque[Tuple[Tuple[int, int], List[str]]] = deque()
    queue.append((start, []))
    visited: Set[Tuple[int, int]] = set()
    visited.add(start)

    moves: Dict[str, Tuple[int, int]] = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        for direction, (dx, dy) in moves.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited:
                if not maze.grid[y][x][direction]:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [direction]))

    return []
