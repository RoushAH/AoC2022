from math import prod

from utils import file_name, show_grid, show_bool_grid


def get_grids(file):
    grid = []
    seen = []
    for row in file.split('\n'):
        row = list(map(int, list(row)))
        grid.append(row)
        s_row = [False for _ in row]
        s_row[0] = True
        s_row[-1] = True
        seen.append(s_row)
    seen[0] = [True] * len(seen[0])
    seen[-1] = [True] * len(seen[-1])
    return grid, seen


def explore_across(grid, seen):
    for i, row in enumerate(grid):
        # L to R
        if i == 0:
            continue
        cutoff = grid[i][0]
        for j, height in enumerate(row):
            if height > cutoff:
                seen[i][j] = True
                cutoff = height
        # R to L
        cutoff = grid[i][-1]
        for j in range(len(row) - 1, -1, -1):
            height = row[j]
            if height > cutoff:
                seen[i][j] = True
                cutoff = height


def explore_down(grid, seen):
    for j in range(len(grid[0])):
        # T to B
        if j == 0:
            continue
        cutoff = grid[0][j]
        for i in range(len(grid)):
            height = grid[i][j]
            if height > cutoff:
                seen[i][j] = True
                cutoff = height
        # B to T
        cutoff = grid[-1][j]
        for i in range(len(grid) - 1, -1, -1):
            height = grid[i][j]
            if height > cutoff:
                seen[i][j] = True
                cutoff = height


def measure_view(grid, i, j):
    l, r, u, d = j-1, j+1, i-1, i+1
    cutoff = grid[i][j]
    score = [0,0,0,0]
    while l >= 0:
        score[0] += 1
        if grid[i][l] >= cutoff:
            break
        l -= 1
    while r < len(grid):
        score[1] += 1
        if grid[i][r] >= cutoff:
            break
        r += 1
    while u >= 0:
        score[2] += 1
        if grid[u][j] >= cutoff:
            break
        u -= 1
    while d < len(grid):
        score[3] += 1
        if grid[d][j] >= cutoff:
            break
        d += 1
    return prod(score)


def find_best_view(grid):
    best_view = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            view = measure_view(grid, i, j)
            if view > best_view:
                best_view = view

    return best_view


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    grid, seen = get_grids(file)
    explore_across(grid, seen)
    explore_down(grid, seen)
    score = sum(sum(r) for r in seen)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    grid, _ = get_grids(file)
    score = find_best_view(grid)
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

    part_one(test_file, 21)
    part_one(data_file)
    part_two(test_file, 8)
    part_two(data_file)


if __name__ == '__main__':
    main()
