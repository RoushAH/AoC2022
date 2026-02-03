from utils import file_name

SCORE = {}
for i in range(ord('a'), ord('z') + 1):
    SCORE[chr(i)] = i - 96
for i in range(ord('a'), ord('z') + 1):
    SCORE[chr(i - 32)] = i - 70


def get_rows(file):
    rows = []
    for row in file.split('\n'):
        l = len(row)
        a, b = set(row[:l // 2]), set(row[l // 2:])
        rows.append((a, b))
    return rows


def get_rows_2(file):
    rows = file.split('\n')
    rows = [set(x) for x in rows]
    return rows


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    rows = get_rows(file)
    overlaps = [s[0] & s[1] for s in rows]
    print("Overlaps:", overlaps)
    score = sum(SCORE[s.pop()] for s in overlaps)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    rows = get_rows_2(file)
    groups = [rows[i:i + 3] for i in range(0, len(rows), 3)]
    overlaps = [s[0] & s[1] & s[2] for s in groups]
    print("Overlaps:", overlaps)
    score = sum(SCORE[s.pop()] for s in overlaps)
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

    part_one(test_file, 157)
    part_one(data_file)
    part_two(test_file, 70)
    part_two(data_file)


if __name__ == '__main__':
    main()
