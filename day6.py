from utils import file_name


def find_starter(file, length):
    i = length
    while len(set(file[i-length:i])) < length:
        i += 1
    return i


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    score = find_starter(list(file), 4)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    score = find_starter(list(file), 14)
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

    part_one(test_file, 7)
    part_one(data_file)
    part_two(test_file, 19)
    part_two(data_file)


if __name__ == '__main__':
    main()
