import math
from math import prod

from utils import file_name


class Monkey:
    def __init__(self, operation, test, t, f, items, divisor=3):
        self.operation = operation
        self.test = int(test)
        self.t = int(t)
        self.f = int(f)
        self.items = items
        self.inspections = 0
        self.divisor = divisor

    def op(self, item):
        operation = self.operation.replace("old", str(item))
        return eval(operation)

    def op_next(self):
        item = self.items.pop(0)
        item = self.op(item) // self.divisor
        self.inspections += 1
        return (self.t, item) if item % self.test == 0 else (self.f, item)

    def catch(self, item):
        self.items.append(item)

    def __repr__(self):
        return f"Monkey({self.operation}, divisible by {self.test}, monkey {self.t} if true, else monkey {self.f}, items {self.items})"


def get_data(file, divisor=3):
    monkeys = []
    for monkey in file.split('\n\n'):
        monkey_data = monkey.split('\n')
        items = list(map(int, monkey_data[1].split(':')[1].split(",")))
        operation = monkey_data[2].split("=")[1]
        test = monkey_data[3].split("by")[1]
        t = monkey_data[4].split("monkey")[1]
        f = monkey_data[5].split("monkey")[1]
        monkey = Monkey(operation, test, t, f, items, divisor)
        monkeys.append(monkey)
    return monkeys

def score_them(monkeys):
    scorez = []
    for monkey in monkeys:
        scorez.append(monkey.inspections)
    scorez = sorted(scorez, reverse=True)
    print(scorez)
    return prod(scorez[:2])

def get_cleaner(monkeys):
    vals = [monkey.test for monkey in monkeys]
    LCM = math.lcm(*vals)

    def clean(item):
        return item % LCM
    return clean

def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    monkeys = get_data(file)
    for round in range(1, 21):
        print("Round {}".format(round))
        for monkey in monkeys:
            while monkey.items:
                catcher, item = monkey.op_next()
                monkeys[catcher].catch(item)
    score = score_them(monkeys)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    monkeys = get_data(file, 1)
    clean = get_cleaner(monkeys)
    for round in range(1, 10001):
        if round % 100 == 0:
            print("{}%".format(round//100))
        for monkey in monkeys:
            while monkey.items:
                catcher, item = monkey.op_next()
                item = clean(item)
                monkeys[catcher].catch(item)
    score = score_them(monkeys)
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

    part_one(test_file, 10605)
    part_one(data_file)
    part_two(test_file, 2713310158)
    part_two(data_file)


if __name__ == '__main__':
    main()
