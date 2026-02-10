from collections import deque
from utils import file_name, add

ADJS = (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1), (0, -1, 0)


def valid3d(point, dims):
    return all(0 <= p < d for p, d in zip(point, dims))


def get_grid(file):
    spots = []
    for row in file.split('\n'):
        spots.append(tuple(int(x) for x in row.split(',')))
    xes, yes, zes = list(zip(*spots))
    max_x, max_y, max_z = max(xes) + 1, max(yes) + 1, max(zes) + 1
    grid = [[[False for _ in range(max_z)] for _ in range(max_y)] for _ in range(max_x)]
    for x, y, z in spots:
        grid[x][y][z] = True
    return grid, spots


def find_neighbours(grid, spot):
    """Count exposed faces for part 1 (faces not touching another cube)."""
    sides = 6
    dims = (len(grid), len(grid[0]), len(grid[0][0]))
    for x, y, z in [add(a, spot) for a in ADJS]:
        if not valid3d((x, y, z), dims):
            continue  # Out of bounds = exposed face, keep the side
        if grid[x][y][z]:
            sides -= 1  # Neighbor cube, not exposed
    return sides


def fill(grid, dims):
    """BFS flood fill from (0,0,0), marking external air as 'a'."""
    queue = deque([(0, 0, 0)])
    grid[0][0][0] = "a"
    while queue:
        spot = queue.popleft()
        for adj in ADJS:
            nx, ny, nz = add(adj, spot)
            if not valid3d((nx, ny, nz), dims):
                continue
            if grid[nx][ny][nz] == ".":
                grid[nx][ny][nz] = "a"
                queue.append((nx, ny, nz))


def complexify(grid):
    """Convert bool grid to string grid with 1-cell padding on all sides."""
    old_x, old_y, old_z = len(grid), len(grid[0]), len(grid[0][0])
    # New grid is 2 bigger in each dimension (padding on both sides)
    new_grid = [[["." for _ in range(old_z + 2)] for _ in range(old_y + 2)] for _ in range(old_x + 2)]
    # Copy original data shifted by +1
    for x in range(old_x):
        for y in range(old_y):
            for z in range(old_z):
                if grid[x][y][z]:
                    new_grid[x + 1][y + 1][z + 1] = "#"
    return new_grid


def find_neighbours_2(grid, spot):
    """Count faces touching external air 'a' (for part 2)."""
    sides = 0
    dims = (len(grid), len(grid[0]), len(grid[0][0]))
    for x, y, z in [add(a, spot) for a in ADJS]:
        if not valid3d((x, y, z), dims):
            sides += 1  # Out of bounds = definitely external
            continue
        if grid[x][y][z] == "a":
            sides += 1
    return sides


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    grid, spots = get_grid(file)
    score = 0
    for spot in spots:
        score += find_neighbours(grid, spot)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    """ Let's do this by BFS fill starting at 0,0,0 """
    print("\n\n", "Part two!", "\n")
    grid, spots = get_grid(file)
    grid = complexify(grid)  # Pads by 1, so coords shift by +1
    dims = (len(grid), len(grid[0]), len(grid[0][0]))
    fill(grid, dims)
    score = 0
    for x, y, z in spots:
        # Shift coordinates to match padded grid
        score += find_neighbours_2(grid, (x + 1, y + 1, z + 1))
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

    part_one(test_file, 64)
    part_one(data_file)  # 3363 is too low
    part_two(test_file, 58)
    part_two(data_file)


if __name__ == '__main__':
    main()
