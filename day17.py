from utils import file_name, add

# The five rock shapes as sets of (x, y) coordinates
# Origin (0,0) is bottom-left of the shape's bounding box
ROCKS = [
    # Horizontal line: ####
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    # Plus sign:  .#.
    #             ###
    #             .#.
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    # L shape (backwards): ..#
    #                      ..#
    #                      ###
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    # Vertical line: #
    #                #
    #                #
    #                #
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    # Square: ##
    #         ##
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]

WIDTH = 7


def get_data(file):
    return file.strip()


def can_place(rock, pos, blocked):
    """Check if rock at position collides with walls, floor, or blocked cells."""
    for dx, dy in rock:
        x, y = pos[0] + dx, pos[1] + dy
        if x < 0 or x >= WIDTH:  # Hit wall
            return False
        if y < 0:  # Hit floor
            return False
        if (x, y) in blocked:  # Hit another rock
            return False
    return True


def simulate(jets, num_rocks):
    """Simulate rocks falling and return final tower height."""
    blocked = set()
    height = 0
    jet_idx = 0

    for rock_num in range(num_rocks):
        rock = ROCKS[rock_num % 5]
        # Spawn: left edge 2 units from wall, bottom 3 units above highest
        pos = (2, height + 3)

        while True:
            # Push by jet
            jet = jets[jet_idx % len(jets)]
            jet_idx += 1
            dx = 1 if jet == '>' else -1
            new_pos = (pos[0] + dx, pos[1])
            if can_place(rock, new_pos, blocked):
                pos = new_pos

            # Fall down
            new_pos = (pos[0], pos[1] - 1)
            if can_place(rock, new_pos, blocked):
                pos = new_pos
            else:
                # Rock comes to rest
                for dx, dy in rock:
                    x, y = pos[0] + dx, pos[1] + dy
                    blocked.add((x, y))
                    height = max(height, y + 1)
                break

    return height


def simulate_with_cycle_detection(jets, num_rocks):
    """Simulate with cycle detection for Part 2's massive numbers."""
    blocked = set()
    height = 0
    jet_idx = 0

    # Track states: (rock_idx, jet_idx, top_pattern) -> (rock_num, height)
    seen = {}
    heights = [0]  # heights[i] = height after rock i lands

    rock_num = 0
    while rock_num < num_rocks:
        rock_idx = rock_num % 5
        jet_mod = jet_idx % len(jets)

        # Create a fingerprint of the top ~30 rows
        top_pattern = frozenset(
            (x, height - y) for x, y in blocked
            if height - y <= 30
        )

        state = (rock_idx, jet_mod, top_pattern)

        if state in seen:
            # Found a cycle!
            prev_rock, prev_height = seen[state]
            cycle_len = rock_num - prev_rock
            height_per_cycle = height - prev_height

            # How many complete cycles can we skip?
            remaining = num_rocks - rock_num
            full_cycles = remaining // cycle_len
            leftover = remaining % cycle_len

            # Height from full cycles
            skip_height = full_cycles * height_per_cycle

            # Height from leftover rocks (look up from history)
            leftover_height = heights[prev_rock + leftover] - prev_height

            return height + skip_height + leftover_height

        seen[state] = (rock_num, height)

        # Normal simulation for one rock
        rock = ROCKS[rock_idx]
        pos = (2, height + 3)

        while True:
            jet = jets[jet_idx % len(jets)]
            jet_idx += 1
            dx = 1 if jet == '>' else -1
            new_pos = (pos[0] + dx, pos[1])
            if can_place(rock, new_pos, blocked):
                pos = new_pos

            new_pos = (pos[0], pos[1] - 1)
            if can_place(rock, new_pos, blocked):
                pos = new_pos
            else:
                for dx, dy in rock:
                    x, y = pos[0] + dx, pos[1] + dy
                    blocked.add((x, y))
                    height = max(height, y + 1)
                break

        rock_num += 1
        heights.append(height)

    return height


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    jets = get_data(file)
    score = simulate(jets, 2022)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    jets = get_data(file)
    score = simulate_with_cycle_detection(jets, 1_000_000_000_000)
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

    part_one(test_file, 3068)
    part_one(data_file)
    part_two(test_file, 1514285714288)
    part_two(data_file)


if __name__ == '__main__':
    main()
