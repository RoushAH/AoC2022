from utils import file_name


def split(l):
    return tuple(map(int, l.split("-")))


def get_data(file):
    out = []
    for row in file.split('\n'):
        a, b = row.split(',')
        a = split(a)
        b = split(b)
        out.append((a, b))
    return out


def check_row(a, b):
    return (a[0] <= b[0] and a[1] >= b[1]) or (a[0] >= b[0] and a[1] <= b[1])


def check_overlap(a, b):
    return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1] or b[1] >= a[1] >= b[0] or b[0] >= a[0] >= b[1]


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    rows = get_data(file)
    print(rows)
    score = sum(check_row(*x) for x in rows)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    rows = get_data(file)
    print(rows)
    score = sum(check_overlap(*x) for x in rows)
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

    part_one(test_file, 2)
    part_one(data_file)
    part_two(test_file,4)
    part_two(data_file)


if __name__ == '__main__':
    main()
