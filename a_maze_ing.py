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

    maze.generate(algorithm=algo, animate=False)

    path = find_path(maze)
    path_string = "".join(path)

    show_path = True

    while True:
        display_maze(maze, path_string, show_path)

        print("\nCommands:")
        print("r - regenerate maze")
        print("p - show/hide shortest path")
        print("b - animate generation (bonus)")
        print("c - change wall colours")
        print("q - quit")

        choice = input("Choice: ").lower()

        if choice == "q":
            break

        elif choice == "p":
            show_path = not show_path

        elif choice == "r":
            maze.generate(algorithm=algo, animate=False)
            path = find_path(maze)
            path_string = "".join(path)

        elif choice == "b":
            print("\nAnimating maze generation...")
            maze.generate(algorithm=algo, animate=True)
            path = find_path(maze)
            path_string = "".join(path)

        elif choice == "c":
            from display import generate_palette
            import display
            display.PALETTE = generate_palette()

    write_output(maze, config['OUTPUT_FILE'])
    print(f"\nMaze written to {config['OUTPUT_FILE']}")


if __name__ == '__main__':
    main()
