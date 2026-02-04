from dataclasses import dataclass

from utils import file_name, show_bool_grid


@dataclass
class Command:
    cmd: str
    value: int = 0
    time: int = 2


def get_data(file):
    for row in file.split('\n'):
        cmd = Command(*row.split(' '))
        cmd.value = int(cmd.value)
        if row.startswith('n'):
            cmd.time = 1
        yield cmd


def run_program(commands):
    checkpoints = {i * 40 + 20: 1 for i in range(6)}
    points = [i * 40 + 20 for i in range(6)]
    cycle = 0
    X = 1
    for command in commands:
        cycle += command.time
        if points and cycle >= points[0]:
            checkpoints[points[0]] = X
            points.pop(0)
        X += command.value
    score = sum(k * v for k, v in checkpoints.items())
    return score


def sprite(X):
    return {X - 1, X, X + 1}


def draw_line(commands):
    cycle = 0
    X = 1
    screen = []
    row = []

    for command in commands:
        for _ in range(command.time):
            beam = cycle % 40
            if beam == 0 and row:
                screen.append(row)
                row = []
            row.append(beam not in sprite(X))
            cycle += 1
        X += command.value

    if row:
        screen.append(row)
    return screen


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    commands = get_data(file)
    score = run_program(commands)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    commands = get_data(file)
    screen = draw_line(list(commands))
    show_bool_grid(screen)
    score = 0
    if tgt:
        score = 0
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

    part_one(test_file, 13140)
    part_one(data_file)
    part_two(test_file)
    part_two(data_file)


if __name__ == '__main__':
    main()
