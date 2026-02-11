import re
import sympy as sp

from utils import file_name

""" I want to implement this as a tree, but might be annoying. 
    Instead, let's just do iterated computation -- loop over, if can compute, do. Else jog on """

pattern = re.compile(
    r"""
    ^(?P<id>\w+):\s+
    (
        (?P<value>\d+)                              # integer case
        |
        (?P<o1>\w+)\s*(?P<op>[+\-*/])\s*(?P<o2>\w+) # expression case
    )
    $
    """,
    re.VERBOSE,
)


def parse_line(line: str):
    m = pattern.match(line.strip())
    if not m:
        raise ValueError(f"Invalid line: {line}")

    if m.group("value") is not None:
        return (m.group("id"), int(m.group("value")))

    return (
        m.group("id"),
        m.group("o1"),
        m.group("op"),
        m.group("o2"),
    )


FOUR_LOWER_BOUNDED = re.compile(
    r"(?:(?<=^)|(?<=[\s()]))"   # start OR space/parenthesis before
    r"[a-z]{4}"                # exactly four lowercase letters
    r"(?:(?=$)|(?=[\s()]))"    # end OR space/parenthesis after
)
def find_groups(s: str) -> list[str]:
    return FOUR_LOWER_BOUNDED.findall(s)


OPS = {"+": lambda a, b: a + b,
       "-": lambda a, b: a - b,
       "*": lambda a, b: a * b,
       "/": lambda a, b: a // b, }


def get_monkeys(file):
    monkeys = {}
    for row in file.split('\n'):
        ln = parse_line(row)
        if len(ln) == 2:
            monkeys[ln[0]] = ln[1]
        else:
            monkeys[ln[0]] = ln[1], OPS[ln[2]], ln[3]
    return monkeys


def get_new_monkeys(file):
    monkeys = {}
    for row in file.split('\n'):
        ln = parse_line(row)
        if ln[0] == "root":
            ln = ln[0], ln[1], "=", ln[3]
        if len(ln) == 2:
            monkeys[ln[0]] = int(ln[1])
        else:
            monkeys[ln[0]] = " ".join(ln[1:])
    return monkeys


def get_root(monkeys):
    ct = len(monkeys)
    while ct:
        ct = 0
        for k, v in monkeys.items():
            if isinstance(v, (int, float)):
                continue
            l, op, r = v
            if isinstance(monkeys[l], (int, float)) and isinstance(monkeys[r], (int, float)):
                monkeys[k] = op(monkeys[l], monkeys[r])
            else:
                ct += 1
    return monkeys["root"]


def flatten(monkeys):
    equation = monkeys["root"]
    print(equation, find_groups(equation))
    groups = find_groups(equation)
    while len(groups) > 0:
        var = groups.pop()
        if var == "humn":
            pass
        else:
            val = monkeys.pop(var)
            val = f"({val})"
            equation = equation.replace(var, val)
            groups = find_groups(equation)
        # print(equation, groups)
    return equation


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    monkeys = get_monkeys(file)

    score = int(get_root(monkeys))
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    monkeys = get_new_monkeys(file)
    # for k, v in monkeys.items():
    #     print(f"{k}: {v}")
    equation = flatten(monkeys)
    humn = sp.symbols("humn")
    eq = sp.Eq(*list(map(eval,equation.split("="))))
    print(eq, sp.solve(eq))
    score = int(sp.solve(eq)[0])
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

    part_one(test_file, 152)
    part_one(data_file)
    part_two(test_file, 301)
    part_two(data_file)


if __name__ == '__main__':
    main()
