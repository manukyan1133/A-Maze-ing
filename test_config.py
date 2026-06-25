from config import parse
from maze import MazeGenerator
from display import display_maze
from pathfinder import find_path
from output import write_output


config = parse("config.txt")
maze = MazeGenerator(
    width=config['WIDTH'],
    height=config['HEIGHT'],
    entry=config['ENTRY'],
    exit=config['EXIT']
).generate()

display_maze(maze)

path = find_path(maze)
print(f"\nSolution path length: {len(path)} steps")
write_output(maze, config['OUTPUT_FILE'])
print(f"Output written to {config['OUTPUT_FILE']}")
