from collections import deque

from utils import file_name, get_rect_neighbours


def get_data(file):
    grid = []
    start = 0, 0
    end = 0, 0
    for i, row in enumerate(file.split('\n')):
        if "S" in row:
            start = i, row.index('S')
        if "E" in row:
            end = i, row.index('E')
        row = list(row.replace("S", "a").replace("E", "z"))
        row = list(map(ord, row))
        grid.append(row)
    return grid, start, end


def find_path(grid, start, end):
    seed = start, 0
    dims = len(grid), len(grid[0])
    next_steps = deque([seed])
    been_there = {(start)}
    print(been_there)
    while next_steps:
        pos, cost = next_steps.popleft()
        if pos == end:
            return cost
        alt = grid[pos[0]][pos[1]]
        neighbours = get_rect_neighbours(pos, dims)
        neighbours = list({n for n in neighbours} - been_there)
        neighbours = list(filter(lambda n: grid[n[0]][n[1]] - alt < 2, neighbours))
        neighbours = list(map(lambda n: tuple([n, cost + 1]), neighbours))
        next_steps.extend(neighbours)
        been_there.update(n[0] for n in neighbours)


def find_back_path(grid, start):
    seed = start, 0
    dims = len(grid), len(grid[0])
    next_steps = deque([seed])
    been_there = {(start)}
    print(been_there)
    while next_steps:
        pos, cost = next_steps.popleft()
        if grid[pos[0]][pos[1]] == ord('a'):
            return cost
        alt = grid[pos[0]][pos[1]]
        neighbours = get_rect_neighbours(pos, dims)
        neighbours = list({n for n in neighbours} - been_there)
        neighbours = list(filter(lambda n:  alt - grid[n[0]][n[1]] < 2, neighbours))
        neighbours = list(map(lambda n: tuple([n, cost + 1]), neighbours))
        next_steps.extend(neighbours)
        been_there.update(n[0] for n in neighbours)


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    grid, start, end = get_data(file)
    score = find_path(grid, start, end)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    grid, start, end = get_data(file)
    score = find_back_path(grid, end)
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

    part_one(test_file, 31)
    part_one(data_file)
    part_two(test_file, 29)
    part_two(data_file)


if __name__ == '__main__':
    main()
