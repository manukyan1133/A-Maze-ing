import sys
from config import parse
from maze import MazeGenerator
from display import display_maze
from output import write_output
from pathfinder import find_path  # Import the pathfinder here


def main() -> None:
    """Main entry point for the maze generator."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config = parse(sys.argv[1])

    maze = MazeGenerator(
        width=config['WIDTH'],
        height=config['HEIGHT'],
        entry=config['ENTRY'],
        exit=config['EXIT'],
        perfect=config['PERFECT']
    ).generate()

    # Calculate the path BEFORE displaying the maze
    path = find_path(maze)
    path_string = "".join(path)

    # Pass the path string to the display function
    display_maze(maze, path_steps=path_string)

    write_output(maze, config['OUTPUT_FILE'])
    print(f"\nMaze written to {config['OUTPUT_FILE']}")


if __name__ == '__main__':
    main()
