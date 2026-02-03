from utils import file_name

SCORES = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}
OUTCOMES = {"X": 0, "Y": 3, "Z": 6}
WINS = {
    "C": "X",
    "A": "Y",
    "B": "Z",
}
DRAWS = {
    "A": "X",
    "B": "Y",
    "C": "Z",
}
LOSSES = {
    "A": "Z",
    "B": "X",
    "C": "Y",
}
CALL = {
    "X": LOSSES,
    "Y": DRAWS,
    "Z": WINS
}


def get_rows(file):
    return [tuple(row.split(' ')) for row in file.split('\n')]


def score_row(row):
    score = SCORES[row[1]]
    if WINS[row[0]] == row[1]:
        return score + 6
    elif DRAWS[row[0]] == row[1]:
        return score + 3
    return score


def score_row_2(row):
    return OUTCOMES[row[1]] + SCORES[CALL[row[1]][row[0]]]


def run_part(file, score_fn, label, tgt=None):
    print(f"\n\n {label} \n")
    rows = get_rows(file)
    score = sum(score_fn(x) for x in rows)
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

    run_part(test_file, score_row, "Part one!", 15)
    run_part(data_file, score_row, "Part one!")
    run_part(test_file, score_row_2, "Part two!", 12)
    run_part(data_file, score_row_2, "Part two!")


if __name__ == '__main__':
    main()
