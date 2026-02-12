from collections import defaultdict

from utils import file_name

# Direction checks: (zone offsets, move offset)
DIRECTIONS = [
    ([(-1, -1), (-1, 0), (-1, 1)], (-1, 0)),  # N
    ([(1, -1), (1, 0), (1, 1)], (1, 0)),       # S
    ([(-1, -1), (0, -1), (1, -1)], (0, -1)),   # W
    ([(-1, 1), (0, 1), (1, 1)], (0, 1)),       # E
]

ALL_NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def get_elves(file):
    elves = set()
    for i, row in enumerate(file.split('\n')):
        for j, char in enumerate(row):
            if char == "#":
                elves.add((i, j))
    return elves


def do_step(elves: set, dir_start: int):
    proposals = {}  # elf -> proposed position

    for elf in elves:
        # Check all 8 neighbors
        has_neighbor = any((elf[0] + dr, elf[1] + dc) in elves for dr, dc in ALL_NEIGHBORS)

        if not has_neighbor:
            proposals[elf] = elf
            continue

        # Try each direction in priority order
        proposed = False
        for i in range(4):
            zone, move = DIRECTIONS[(dir_start + i) % 4]
            if all((elf[0] + dr, elf[1] + dc) not in elves for dr, dc in zone):
                proposals[elf] = (elf[0] + move[0], elf[1] + move[1])
                proposed = True
                break

        if not proposed:
            proposals[elf] = elf

    # Count proposals to each destination
    dest_count = defaultdict(list)
    for elf, dest in proposals.items():
        dest_count[dest].append(elf)

    # Build new elf positions
    new_elves = set()
    for dest, proposers in dest_count.items():
        if len(proposers) == 1:
            new_elves.add(dest)
        else:
            new_elves.update(proposers)

    return new_elves


def score_me(elves: set) -> int:
    wyes, exes = zip(*elves)
    width = max(exes) - min(exes) + 1
    height = max(wyes) - min(wyes) + 1
    return width * height - len(elves)


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    elves = get_elves(file)
    for i in range(10):
        elves = do_step(elves, i % 4)
    score = score_me(elves)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    elves = get_elves(file)
    score = 1
    new_elves = do_step(elves, (score - 1) % 4)
    while new_elves != elves:
        elves = new_elves
        score += 1
        new_elves = do_step(elves, (score - 1) % 4)
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

    part_one(test_file, 110)
    part_one(data_file)
    part_two(test_file, 20)
    part_two(data_file) # 953 too high


if __name__ == '__main__':
    main()
