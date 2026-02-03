import re
from collections import namedtuple, defaultdict

from utils import file_name

Move = namedtuple('Move', ["count", "ex", "ad"])


def get_nums(s):
    nums = list(map(int, re.findall(r'\d+', s)))
    return nums


def build_stax(string):
    rows = string.split('\n')
    count = int(rows[-1].split(' ')[-1])
    stax = {i + 1: [] for i in range(count)}
    for row in rows[:-1]:
        if len(row) < count * 4:
            row += " " * (count * 4 - len(row))
        for i in range(count):
            chr = row[i * 4 + 1]
            if chr != " ":
                stax[i + 1].append(chr)
    for s in stax:
        stax[s] = list(reversed(stax[s]))
    return stax


def get_data(file):
    a, b = file.split('\n\n')
    stax = build_stax(a)
    b = b.split('\n')
    moves = list(map(get_nums, b))
    moves = [Move(*n) for n in moves]
    return stax, moves


def do_move(stax: list[list[str]], move: Move):
    for i in range(move.count):
        crate = stax[move.ex].pop()
        stax[move.ad].append(crate)

def do_super_move(stax: list[list[str]], move: Move):
    grab, stax[move.ex] = stax[move.ex][-move.count:], stax[move.ex][:-move.count]
    stax[move.ad] = stax[move.ad] + grab


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    stacks, moves = get_data(file)
    print("Stacks:", stacks)
    for move in moves:
        do_move(stacks, move)
    score = "".join([s[-1] for s in stacks.values()])
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    stacks, moves = get_data(file)
    print("Stacks:", stacks)
    for move in moves:
        do_super_move(stacks, move)
    score = "".join([s[-1] for s in stacks.values()])
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

    part_one(test_file, "CMZ")
    part_one(data_file)
    part_two(test_file, "MCD")
    part_two(data_file)


if __name__ == '__main__':
    main()
