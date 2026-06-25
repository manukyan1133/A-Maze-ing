from maze import MazeGenerator
from pathfinder import find_path
from typing import Dict


def cell_to_hex(cell: Dict[str, bool]) -> str:
    """Convert a cell's walls to a hex digit."""
    value = 0
    if cell['N']:
        value += 1   # bit 0
    if cell['E']:
        value += 2   # bit 1
    if cell['S']:
        value += 4   # bit 2
    if cell['W']:
        value += 8   # bit 3
    return hex(value)[2:].upper()


def write_output(maze: MazeGenerator, filepath: str) -> None:
    """Write maze to output file in hex format."""
    path = find_path(maze)

    with open(filepath, 'w') as f:
        for y in range(maze.height):
            row = ''
            for x in range(maze.width):
                row += cell_to_hex(maze.grid[y][x])
            f.write(row + '\n')

        f.write('\n')
        f.write(f"{maze.entry[0]},{maze.entry[1]}\n")
        f.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        f.write(''.join(path) + '\n')
