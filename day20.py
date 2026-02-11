from collections import deque

from utils import file_name


def get_data(file, key=1):
    numbers = file.split('\n')
    numbers = list(map(int, numbers))
    # Each element is (original_index, value) to handle duplicates
    indexed = [(i, v*key) for i, v in enumerate(numbers)]
    rotator = deque(indexed)
    return indexed, rotator


def rotate_to(d, item):
    idx = d.index(item)  # Now finds the specific (index, value) tuple
    d.rotate(-idx)


def score_me(d):
    # Find the tuple with value 0
    zero_item = next(item for item in d if item[1] == 0)
    rotate_to(d, zero_item)
    actual = 1000 % len(d)
    s = 0
    for i in range(3):
        d.rotate(-actual)
        s += d[0][1]  # Get the value from the tuple
    return s


def mix(order, d):
    for item in order:
        rotate_to(d, item)
        d.popleft()
        d.rotate(-item[1])  # Rotate by the value
        d.appendleft(item)
    return d

def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    rotator = mix(*get_data(file))
    print(rotator, score_me(rotator))
    score = score_me(rotator)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    key = 811589153
    o, d = get_data(file, key)
    for i in range(10):
        d = mix(o,d)
    score = score_me(d)
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

    part_one(test_file, 3)
    part_one(data_file) # 4240 too low
    part_two(test_file, 1623178306)
    part_two(data_file)


if __name__ == '__main__':
    main()
