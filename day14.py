from utils import file_name, add


def points_on_line(p1, p2):
    (x1, y1), (x2, y2) = p1, p2

    if x1 == x2:  # vertical line
        step = 1 if y2 >= y1 else -1
        return [(x1, y) for y in range(y1, y2 + step, step)]

    if y1 == y2:  # horizontal line
        step = 1 if x2 >= x1 else -1
        return [(x, y1) for x in range(x1, x2 + step, step)]

    raise ValueError("Points are not aligned horizontally or vertically")


def get_data(file):
    blockers = set()
    for row in file.split('\n'):
        row = row.split('->')
        row = list(map(lambda m: m.split(","), row))
        row = [list(map(int, r)) for r in row]
        for i in range(len(row) - 1):
            blocks = points_on_line(row[i], row[i + 1])
            for block in blocks:
                blockers.add(tuple(block))
    bottom = max(b[1] for b in blockers) + 1
    return blockers, bottom

OPTIONS = ((0,1), (-1,1), (1,1))

def drop_sand(blockers, bottom):
    grains = 1
    start = 500, 0
    pos = 500, 0
    while pos[1] < bottom:
        # Move the grain down. If it can't generate a new one
        options = [add(pos, opt) for opt in OPTIONS]
        options = [o for o in options if o not in blockers]
        if len(options) == 0:
            grains += 1
            blockers.add(pos)
            pos = start
        else:
            pos = options[0]
    return grains - 1

def flood_sand(blockers, bottom):
    grains = 1
    start = 500, 0
    pos = 500, 0
    while True:
        # Move the grain down. If it can't generate a new one
        options = [add(pos, opt) for opt in OPTIONS]
        options = [o for o in options if o not in blockers]
        if len(options) == 0 or pos[1] == bottom:
            grains += 1
            blockers.add(pos)
            if start in blockers:
                return grains - 1
            pos = start
        else:
            pos = options[0]
    return grains - 1


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    blocks, bottom = get_data(file)
    score = drop_sand(blocks, bottom)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    blocks, bottom = get_data(file)
    score = flood_sand(blocks, bottom)
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

    part_one(test_file, 24)
    part_one(data_file)
    part_two(test_file, 93)
    part_two(data_file)


if __name__ == '__main__':
    main()
