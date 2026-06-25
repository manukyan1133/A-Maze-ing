*This project has been created as part of the 42 curriculum by manmanuk and kchibukh.*

# A-Maze-ing

## Description
A maze generator in Python that generates perfect or imperfect mazes
using the Recursive Backtracker algorithm.

## Instructions
Install dependencies:
\```bash
make install
\```

Run the program:
\```bash
make run
\```

Or directly:
\```bash
python3 a_maze_ing.py config.txt
\```

## Config file format
\```
WIDTH=20        # maze width in cells
HEIGHT=15       # maze height in cells
ENTRY=0,0       # entry coordinates (x,y)
EXIT=19,14      # exit coordinates (x,y)
OUTPUT_FILE=maze.txt  # output filename
PERFECT=True    # single path maze?
\```

## Algorithm
Uses Recursive Backtracker (DFS):
- Start at entry cell
- Randomly visit unvisited neighbours
- Knock down walls between cells
- Backtrack when stuck
- Repeat until all cells visited

Chosen because it generates long winding paths,
making interesting perfect mazes.

## Reusable module
Install the package:
\```bash
pip install mazegen-1.0.0-py3-none-any.whl
\```

Basic usage:
\```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42
).generate()

print(maze.grid)      # full grid
print(maze.solution)  # solution path
\```

## Resources
- [Recursive Backtracker](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Python typing module](https://docs.python.org/3/library/typing.html)

### AI Usage
AI was used to clarify concepts like BFS pathfinding
and type hints. All logic was written and understood independently.

## Team
- manmanuk — maze generator, pathfinder, hex output, pip package
- kchibukh — config parser, display, main program, animation bonus