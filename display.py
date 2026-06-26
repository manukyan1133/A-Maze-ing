from maze import MazeGenerator
from typing import Any

def display_maze(maze: Any, path_steps: str = "") -> None:
    """Display the maze as ASCII art in the terminal."""

    # 1. Trace the path coordinates from the solution string
    path_cells = set()
    if path_steps:
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

    # ANSI Escape codes for background/text coloring (Chapter V requirement)
    WALL = "\033[40m  \033[0m"       # Black block for walls
    SPACE = "  "                    # Empty path space
    PATH = "\033[43;5;196m  \033[0m"
    START = "\033[48;5;46m  \033[0m"    # Green
    END = "\033[48;5;21m  \033[0m"     # Blue
    PATTERN_42_COLOR = "\033[48;5;24m  \033[0m"
    
    # 2. Build a full block matrix (size multiplied to handle walls as blocks)
    render_w = maze.width * 2 + 1
    render_h = maze.height * 2 + 1
    display_grid = [[WALL for _ in range(render_w)] for _ in range(render_h)]

    # 3. Fill in open passages and pathways
    for y in range(maze.height):
        for x in range(maze.width):
            bx = x * 2 + 1
            by = y * 2 + 1

            if hasattr(maze, 'is_pattern_42') and maze.is_pattern_42(x, y):
                display_grid[by][bx] = PATTERN_42_COLOR
            else:
                display_grid[by][bx] = SPACE

            # Open North connections and color them if within "42"
            if not maze.grid[y][x]['N'] and y > 0:
                if hasattr(maze, 'is_pattern_42') and maze.is_pattern_42(x, y) and maze.is_pattern_42(x, y - 1):
                    display_grid[by - 1][bx] = PATTERN_42_COLOR
                else:
                    display_grid[by - 1][bx] = SPACE
                    
            # Open South connections and color them if within "42"
            if not maze.grid[y][x]['S'] and y < maze.height - 1:
                if hasattr(maze, 'is_pattern_42') and maze.is_pattern_42(x, y) and maze.is_pattern_42(x, y + 1):
                    display_grid[by + 1][bx] = PATTERN_42_COLOR
                else:
                    display_grid[by + 1][bx] = SPACE

            # Open West connections and color them if within "42"
            if not maze.grid[y][x]['W'] and x > 0:
                if hasattr(maze, 'is_pattern_42') and maze.is_pattern_42(x, y) and maze.is_pattern_42(x - 1, y):
                    display_grid[by][bx - 1] = PATTERN_42_COLOR
                else:
                    display_grid[by][bx - 1] = SPACE
                    
            # Open East connections and color them if within "42"
            if not maze.grid[y][x]['E'] and x < maze.width - 1:
                if hasattr(maze, 'is_pattern_42') and maze.is_pattern_42(x, y) and maze.is_pattern_42(x + 1, y):
                    display_grid[by][bx + 1] = PATTERN_42_COLOR
                else:
                    display_grid[by][bx + 1] = SPACE
    # 4. Insert Entry/Exit holes in outer borders
    ex, ey = maze.entry
    display_grid[ey * 2 + 1][ex * 2 + 1] = START
    # Open outer wall at entry
    if ey == 0:
        display_grid[0][ex * 2 + 1] = SPACE
    elif ey == maze.height - 1:
        display_grid[render_h - 1][ex * 2 + 1] = SPACE

    xx, xy = maze.exit
    display_grid[xy * 2 + 1][xx * 2 + 1] = END
    # Open outer wall at exit
    if xy == 0:
        display_grid[0][xx * 2 + 1] = SPACE
    elif xy == maze.height - 1:
        display_grid[render_h - 1][xx * 2 + 1] = SPACE

    # 5. overlay the solution path steps
    if path_steps:
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
                display_grid[by][bx] = PATH
            display_grid[(by + nby) // 2][(bx + nbx) // 2] = PATH

            curr_x, curr_y = next_x, next_y

    # 6. Print the matrix out onto the terminal
    print("\n" + "\n".join("".join(row) for row in display_grid) + "\n")
