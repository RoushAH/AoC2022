from utils import file_name, add, is_adjacent, sub, hat

MOVES = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}


def get_data(file):
    for row in file.split("\n"):
        dir, dst = row.split(" ")
        dst = int(dst)
        yield dir, dst


def track_moves(moves, n_knots=2):
    # knots[0] = head, knots[-1] = tail
    knots = [(0, 0)] * n_knots
    hist = {knots[-1]}

    for dir, dst in moves:
        for _ in range(dst):
            # move head
            knots[0] = add(knots[0], MOVES[dir])

            # each knot follows the one in front
            for i in range(1, n_knots):
                leader = knots[i - 1]
                follower = knots[i]

                if not is_adjacent(leader, follower):
                    diff = hat(sub(leader, follower))
                    knots[i] = add(follower, diff)

            hist.add(knots[-1])

    return len(hist)


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    moves = get_data(file)
    score = track_moves(moves)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    moves = get_data(file)
    score = track_moves(moves,10)
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
    with open(f"test/{filename}_2.txt", 'r') as f:
        test_file_2 = f.read()

    part_one(test_file, 13)
    part_one(data_file)
    part_two(test_file_2, 36)
    part_two(data_file)


if __name__ == '__main__':
    main()
