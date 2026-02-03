from utils import file_name


def get_data(file):
    out = []
    for row in file.split("\n\n"):
        elf = list(map(int, row.split("\n")))
        out.append(elf)
    return out


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    elves = get_data(file)
    elf_total = [sum(e) for e in elves]
    score = max(elf_total)
    print(elf_total)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    elves = get_data(file)
    elf_total = sorted([sum(e) for e in elves], reverse=True)
    score = sum(elf_total[:3])
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

    part_one(test_file, 24000)
    part_one(data_file)
    part_two(test_file, 45000)
    part_two(data_file)


if __name__ == '__main__':
    main()
