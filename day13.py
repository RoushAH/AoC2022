from math import prod

from utils import file_name


def get_pairs(file):
    pairs = []
    for pair in file.split('\n\n'):
        pair = pair.split('\n')
        pair = list(map(eval, pair))
        pairs.append(pair)
    return pairs


def is_in_order(a, b):
    for i in range(min(len(a), len(b))):
        left = a[i]
        right = b[i]
        if left == right:
            continue
        elif all(isinstance(p, int) for p in [left, right]):
            return left < right
        elif all(isinstance(p, list) for p in [left, right]):
            return is_in_order(left, right)
        elif isinstance(left, int):
            left = [left]
            ans = is_in_order(left, right)
            if ans is not None:
                return ans
            continue
        elif isinstance(right, int):
            right = [right]
            ans = is_in_order(left, right)
            if ans is not None:
                return ans
            continue
    if len(a) == len(b): return None
    return len(a) < len(b)


def get_singles(file):
    elements = []
    for row in file.split('\n'):
        if row.strip() == '':
            continue
        elements.append(eval(row))
    elements.append([[2]])
    elements.append([[6]])
    return elements


def sort_me(elements):
    sorted_jobs = [elements.pop()]
    while elements:
        next = elements.pop()
        pos = 0
        while pos < len(sorted_jobs) and is_in_order(sorted_jobs[pos], next):
            pos += 1
        sorted_jobs.insert(pos, next)
    return sorted_jobs


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    pairs = get_pairs(file)
    score = 0
    for i, pair in enumerate(pairs, 1):
        if is_in_order(*pair):
            score += i
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    elements = get_singles(file)
    elements = sort_me(elements)
    score = prod([elements.index(m) + 1 for m in [[[2]],[[6]]]])
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

    part_one(test_file, 13)
    part_one(data_file)  # 6593 too low
    part_two(test_file, 140)
    part_two(data_file)


if __name__ == '__main__':
    main()
