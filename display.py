import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze import MazeGenerator


def generate_palette() -> dict[str, str]:
    return {
        "WALL": random.choice([
            "\033[40m  \033[0m",
            "\033[100m  \033[0m",
            "\033[47m  \033[0m",
            "\033[107m  \033[0m",
            "\033[44m  \033[0m",
            "\033[45m  \033[0m",
            "\033[41m  \033[0m"
        ]),

        "SPACE": "  ",

        "PATH": random.choice([
            "\033[42m  \033[0m",
            "\033[43m  \033[0m",
            "\033[46m  \033[0m",
            "\033[105m  \033[0m",
            "\033[106m  \033[0m",
            "\033[102m  \033[0m",
            "\033[103m  \033[0m"
        ]),

        "START": random.choice([
            "\033[48;5;46m  \033[0m",
            "\033[48;5;82m  \033[0m",
            "\033[48;5;118m  \033[0m",
            "\033[48;5;154m  \033[0m"
        ]),

        "END": random.choice([
            "\033[48;5;196m  \033[0m",
            "\033[48;5;160m  \033[0m",
            "\033[48;5;124m  \033[0m",
            "\033[48;5;88m  \033[0m"
        ]),

        "PATTERN_42_COLOR": random.choice([
            "\033[48;5;93m  \033[0m",
            "\033[48;5;57m  \033[0m",
            "\033[48;5;99m  \033[0m",
            "\033[48;5;135m  \033[0m",
            "\033[48;5;141m  \033[0m",
            "\033[48;5;177m  \033[0m"
        ]),

        "BORDER": random.choice([
            "\033[40m  \033[0m",
            "\033[100m  \033[0m",
            "\033[47m  \033[0m",
            "\033[107m  \033[0m",
            "\033[43m  \033[0m",
            "\033[45m  \033[0m",
            "\033[41m  \033[0m"
        ])
    }


PALETTE = generate_palette()


def display_maze(
    maze: "MazeGenerator",
    path_steps: str = "",
    show_path: bool = True
) -> None:
    """Display the maze as ASCII art in the terminal."""

    # 1. Trace the path coordinates from the solution string
    palette = PALETTE
    path_cells = set()
    if show_path and path_steps:
        curr_x, curr_y = maze.entry
        path_cells.add((curr_x, curr_y))
        for move in path_steps:
            if move == 'N':
                curr_y -= 1
            elif move == 'S':
                curr_y += 1
            elif move == 'E':
                curr_x += 1
            elif move == 'W':
                curr_x -= 1
            path_cells.add((curr_x, curr_y))

    # 2. Build a full block matrix (size multiplied to handle walls as blocks)
    render_w = maze.width * 2 + 1
    render_h = maze.height * 2 + 1
    display_grid = [
        [palette["WALL"] for _ in range(render_w)]
        for _ in range(render_h)
        ]

    # 3. Fill in open passages and pathways
    for y in range(maze.height):
        for x in range(maze.width):
            bx = x * 2 + 1
            by = y * 2 + 1

            if hasattr(maze, 'is_pattern_42') and maze.is_pattern_42(x, y):
                display_grid[by][bx] = palette["PATTERN_42_COLOR"]
            else:
                display_grid[by][bx] = palette["SPACE"]

            # Open North connections and color them if within "42"
            if not maze.grid[y][x]['N'] and y > 0:
                if (
                    hasattr(maze, 'is_pattern_42')
                    and maze.is_pattern_42(x, y)
                    and maze.is_pattern_42(x, y - 1)
                ):
                    display_grid[by - 1][bx] = palette["PATTERN_42_COLOR"]
                else:
                    display_grid[by - 1][bx] = palette["SPACE"]

            # Open South connections and color them if within "42"
            if not maze.grid[y][x]['S'] and y < maze.height - 1:
                if (
                    hasattr(maze, 'is_pattern_42')
                    and maze.is_pattern_42(x, y)
                    and maze.is_pattern_42(x, y + 1)
                ):
                    display_grid[by + 1][bx] = palette["PATTERN_42_COLOR"]
                else:
                    display_grid[by + 1][bx] = palette["SPACE"]

            # Open West connections and color them if within "42"
            if not maze.grid[y][x]['W'] and x > 0:
                if (
                    hasattr(maze, 'is_pattern_42')
                    and maze.is_pattern_42(x, y)
                    and maze.is_pattern_42(x - 1, y)
                ):
                    display_grid[by][bx - 1] = palette["PATTERN_42_COLOR"]
                else:
                    display_grid[by][bx - 1] = palette["SPACE"]

            # Open East connections and color them if within "42"
            if not maze.grid[y][x]['E'] and x < maze.width - 1:
                if (hasattr(maze, 'is_pattern_42')
                    and maze.is_pattern_42(x, y)
                        and maze.is_pattern_42(x + 1, y)):
                    display_grid[by][bx + 1] = palette["PATTERN_42_COLOR"]
                else:
                    display_grid[by][bx + 1] = palette["SPACE"]
    # 4. Insert Entry/Exit holes in outer borders
    ex, ey = maze.entry
    display_grid[ey * 2 + 1][ex * 2 + 1] = palette["START"]
    # Open outer wall at entry
    if ey == 0:
        display_grid[0][ex * 2 + 1] = palette["SPACE"]
    elif ey == maze.height - 1:
        display_grid[render_h - 1][ex * 2 + 1] = palette["SPACE"]

    xx, xy = maze.exit
    display_grid[xy * 2 + 1][xx * 2 + 1] = palette["END"]
    # Open outer wall at exit
    if xy == 0:
        display_grid[0][xx * 2 + 1] = palette["SPACE"]
    elif xy == maze.height - 1:
        display_grid[render_h - 1][xx * 2 + 1] = palette["SPACE"]

    # 5. overlay the solution path steps
    if path_steps and show_path:
        curr_x, curr_y = maze.entry
        for move in path_steps:
            if move == 'N':
                next_x, next_y = curr_x, curr_y - 1
            elif move == 'S':
                next_x, next_y = curr_x, curr_y + 1
            elif move == 'E':
                next_x, next_y = curr_x + 1, curr_y
            elif move == 'W':
                next_x, next_y = curr_x - 1, curr_y

            # Place standard dot in core spaces and between connection points
            bx, by = curr_x * 2 + 1, curr_y * 2 + 1
            nbx, nby = next_x * 2 + 1, next_y * 2 + 1

            curr = curr_x, curr_y
            if curr != maze.entry and (curr) != maze.exit:
                display_grid[by][bx] = palette["PATH"]
            display_grid[(by + nby) // 2][(bx + nbx) // 2] = palette["PATH"]

            curr_x, curr_y = next_x, next_y

    # 6. Print the matrix out onto the terminal
    print("\n" + "\n".join("".join(row) for row in display_grid) + "\n")
