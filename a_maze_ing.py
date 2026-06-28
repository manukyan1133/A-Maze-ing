import sys
from config import parse
from maze import MazeGenerator
from display import display_maze
from output import write_output
from pathfinder import find_path


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config = parse(sys.argv[1])

    maze_seed = config.get('SEED', None)
    if maze_seed is not None:
        try:
            maze_seed = int(maze_seed)
        except ValueError:
            maze_seed = None

    animate_bonus = config.get('ANIMATE', False)
    if isinstance(animate_bonus, str):
        animate_bonus = animate_bonus.lower() == 'true'

    algo = config.get('ALGORITHM', 'dfs')

    maze = MazeGenerator(
        width=config['WIDTH'],
        height=config['HEIGHT'],
        entry=config['ENTRY'],
        exit=config['EXIT'],
        perfect=config['PERFECT'],
        seed=maze_seed
    )

    maze.generate(algorithm=algo, animate=animate_bonus)

    path = find_path(maze)
    path_string = "".join(path)

    display_maze(maze, path_steps=path_string)

    write_output(maze, config['OUTPUT_FILE'])
    print(f"\nMaze written to {config['OUTPUT_FILE']}")


if __name__ == '__main__':
    main()
