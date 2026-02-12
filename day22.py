import re

from utils import file_name


# Directions: 0=Right, 1=Down, 2=Left, 3=Up
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse(file):
    map_part, path_part = file.split('\n\n')
    rows = map_part.split('\n')

    # Find max width for consistent indexing
    max_width = max(len(row) for row in rows)
    grid = [row.ljust(max_width) for row in rows]

    # Parse path: extract numbers and letters
    path = re.findall(r'(\d+|[LR])', path_part.strip())
    path = [int(x) if x.isdigit() else x for x in path]

    return grid, path


def find_start(grid):
    """Find leftmost open tile in top row."""
    for col, ch in enumerate(grid[0]):
        if ch == '.':
            return (0, col)
    raise ValueError("No start found")


def wrap_position(grid, row, col, direction):
    """Find the wrapped position when moving off the map."""
    dr, dc = DIRS[direction]
    height, width = len(grid), len(grid[0])

    # Go backwards until we find the edge
    r, c = row, col
    while True:
        nr, nc = (r - dr) % height, (c - dc) % width
        if grid[nr][nc] == ' ':
            break
        r, c = nr, nc
    return r, c


def move(grid, pos, direction, steps):
    """Move forward, wrapping around and stopping at walls."""
    row, col = pos
    dr, dc = DIRS[direction]
    height, width = len(grid), len(grid[0])

    for _ in range(steps):
        nr, nc = (row + dr) % height, (col + dc) % width

        # Handle wrapping through empty space
        if grid[nr][nc] == ' ':
            nr, nc = wrap_position(grid, nr, nc, direction)

        # Hit a wall? Stop.
        if grid[nr][nc] == '#':
            break

        row, col = nr, nc

    return row, col


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    grid, path = parse(file)

    pos = find_start(grid)
    facing = 0  # Start facing right

    for instruction in path:
        if instruction == 'L':
            facing = (facing - 1) % 4
        elif instruction == 'R':
            facing = (facing + 1) % 4
        else:
            pos = move(grid, pos, facing, instruction)

    row, col = pos
    # Password: 1-indexed row and column
    score = 1000 * (row + 1) + 4 * (col + 1) + facing
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def get_face_size(grid):
    """Determine cube face size from grid dimensions."""
    non_space = sum(1 for row in grid for c in row if c != ' ')
    # 6 faces on a cube, so total tiles = 6 * face_size^2
    face_size = int((non_space // 6) ** 0.5)
    return face_size


def cube_wrap(row, col, direction, face_size):
    """
    Given position about to leave the map and direction,
    return new (row, col, new_direction) after cube wrapping.

    Hardcoded for the two cube net shapes (test=4, real=50).
    """
    # Determine which face we're on and local position within face
    face_row, face_col = row // face_size, col // face_size
    local_row, local_col = row % face_size, col % face_size
    S = face_size - 1  # max index within face

    if face_size == 4:
        # Test input cube net:
        #     1
        #   234
        #     56
        transitions = {
            # (face_row, face_col, direction): (new_face_row, new_face_col, new_dir, row_expr, col_expr)
            (0, 2, 0): (2, 3, 2, lambda r, c: S - r, lambda r, c: S),  # 1 right -> 6 right (reversed)
            (0, 2, 2): (1, 1, 1, lambda r, c: 0, lambda r, c: r),      # 1 left -> 3 top
            (0, 2, 3): (1, 0, 1, lambda r, c: 0, lambda r, c: S - c),  # 1 top -> 2 top (reversed)
            (1, 0, 1): (2, 2, 3, lambda r, c: S, lambda r, c: S - c),  # 2 bottom -> 5 bottom (reversed)
            (1, 0, 2): (2, 3, 3, lambda r, c: S, lambda r, c: S - r),  # 2 left -> 6 bottom (reversed)
            (1, 0, 3): (0, 2, 1, lambda r, c: 0, lambda r, c: S - c),  # 2 top -> 1 top (reversed)
            (1, 1, 3): (0, 2, 0, lambda r, c: c, lambda r, c: 0),      # 3 top -> 1 left
            (1, 1, 1): (2, 2, 0, lambda r, c: S - c, lambda r, c: 0),  # 3 bottom -> 5 left (reversed)
            (1, 2, 0): (2, 3, 1, lambda r, c: 0, lambda r, c: S - r),  # 4 right -> 6 top (reversed)
            (2, 2, 2): (1, 1, 3, lambda r, c: S, lambda r, c: S - r),  # 5 left -> 3 bottom (reversed)
            (2, 2, 1): (1, 0, 3, lambda r, c: S, lambda r, c: S - c),  # 5 bottom -> 2 bottom (reversed)
            (2, 3, 0): (0, 2, 2, lambda r, c: S - r, lambda r, c: S),  # 6 right -> 1 right (reversed)
            (2, 3, 1): (1, 0, 0, lambda r, c: S - c, lambda r, c: 0),  # 6 bottom -> 2 left (reversed)
            (2, 3, 3): (1, 2, 2, lambda r, c: S - c, lambda r, c: S),  # 6 top -> 4 right (reversed)
        }
    else:
        # Real input cube net (face_size=50):
        #  12
        #  3
        # 45
        # 6
        transitions = {
            # Face 1 (0,1)
            (0, 1, 2): (2, 0, 0, lambda r, c: S - r, lambda r, c: 0),  # 1 left -> 4 left (reversed)
            (0, 1, 3): (3, 0, 0, lambda r, c: c, lambda r, c: 0),      # 1 top -> 6 left
            # Face 2 (0,2)
            (0, 2, 0): (2, 1, 2, lambda r, c: S - r, lambda r, c: S),  # 2 right -> 5 right (reversed)
            (0, 2, 1): (1, 1, 2, lambda r, c: c, lambda r, c: S),      # 2 bottom -> 3 right
            (0, 2, 3): (3, 0, 3, lambda r, c: S, lambda r, c: c),      # 2 top -> 6 bottom
            # Face 3 (1,1)
            (1, 1, 0): (0, 2, 3, lambda r, c: S, lambda r, c: r),      # 3 right -> 2 bottom
            (1, 1, 2): (2, 0, 1, lambda r, c: 0, lambda r, c: r),      # 3 left -> 4 top
            # Face 4 (2,0)
            (2, 0, 2): (0, 1, 0, lambda r, c: S - r, lambda r, c: 0),  # 4 left -> 1 left (reversed)
            (2, 0, 3): (1, 1, 0, lambda r, c: c, lambda r, c: 0),      # 4 top -> 3 left
            # Face 5 (2,1)
            (2, 1, 0): (0, 2, 2, lambda r, c: S - r, lambda r, c: S),  # 5 right -> 2 right (reversed)
            (2, 1, 1): (3, 0, 2, lambda r, c: c, lambda r, c: S),      # 5 bottom -> 6 right
            # Face 6 (3,0)
            (3, 0, 0): (2, 1, 3, lambda r, c: S, lambda r, c: r),      # 6 right -> 5 bottom
            (3, 0, 1): (0, 2, 1, lambda r, c: 0, lambda r, c: c),      # 6 bottom -> 2 top
            (3, 0, 2): (0, 1, 1, lambda r, c: 0, lambda r, c: r),      # 6 left -> 1 top
        }

    key = (face_row, face_col, direction)
    if key not in transitions:
        raise ValueError(f"No transition for {key}")

    new_face_row, new_face_col, new_dir, row_fn, col_fn = transitions[key]
    new_local_row = row_fn(local_row, local_col)
    new_local_col = col_fn(local_row, local_col)

    new_row = new_face_row * face_size + new_local_row
    new_col = new_face_col * face_size + new_local_col

    return new_row, new_col, new_dir


def move_cube(grid, pos, direction, steps, face_size):
    """Move forward on cube, wrapping around faces and stopping at walls."""
    row, col = pos

    for _ in range(steps):
        dr, dc = DIRS[direction]
        nr, nc = row + dr, col + dc
        new_dir = direction

        # Check if we need to wrap around the cube
        if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] == ' ':
            nr, nc, new_dir = cube_wrap(row, col, direction, face_size)

        # Hit a wall? Stop.
        if grid[nr][nc] == '#':
            break

        row, col, direction = nr, nc, new_dir

    return row, col, direction


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    grid, path = parse(file)
    face_size = get_face_size(grid)

    pos = find_start(grid)
    facing = 0  # Start facing right

    for instruction in path:
        if instruction == 'L':
            facing = (facing - 1) % 4
        elif instruction == 'R':
            facing = (facing + 1) % 4
        else:
            row, col, facing = move_cube(grid, pos, facing, instruction, face_size)
            pos = (row, col)

    row, col = pos
    score = 1000 * (row + 1) + 4 * (col + 1) + facing
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def main():
    filename = file_name()
    with open(f"data/{filename}.txt", 'r') as f:
        data_file = f.read()
    with open(f"test/{filename}.txt", 'r') as f:
        test_file = f.read()

    part_one(test_file, 6032)
    part_one(data_file)
    part_two(test_file, 5031)
    part_two(data_file)


if __name__ == '__main__':
    main()
