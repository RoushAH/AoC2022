import re
from sympy import symbols, Eq, solve

from utils import file_name, valid


class Sensor:
    def __init__(self, x, y, bx, by):
        x, y, bx, by = map(int, (x, y, bx, by))
        self.pos = [x, y]
        self.range = abs(bx - x) + abs(by - y)

    def is_in_range(self, pos):
        return abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1]) <= self.range

    def blocks_in_row(self, row):
        if self.pos[1] + self.range < row or self.pos[1] - self.range > row:
            return set()
        spare = 0
        if self.pos[1] - self.range <= row < self.pos[1]:
            spare = self.range - self.pos[1] + row
        elif self.pos[1] + self.range >= row > self.pos[1]:
            spare = self.range + self.pos[1] - row
        elif row == self.pos[1]:
            spare = self.range * 2 - 1
        return {n for n in range(self.pos[0] - spare, self.pos[0] + spare + 1)}

    def get_c_vals(self):
        return [self.pos[1] - self.pos[0] + self.range + 1,
                self.pos[1] - self.pos[0] - self.range - 1,
                self.pos[1] + self.pos[0] + self.range + 1,
                self.pos[1] + self.pos[0] - self.range - 1]

    def __repr__(self):
        return f'{self.pos[0]},{self.pos[1]} R={self.range}'


def get_sensors(file):
    sensors = []
    beacons = set()
    for row in file.split("\n"):
        nums = list(map(int, re.findall(r"-?\d+", row)))
        sensors.append(Sensor(*nums))
        beacons.add((nums[2], nums[3]))  # beacon x, y
    return sensors, beacons


def part_one(file, tgt=None, row_in_question=None):
    print("\n\n", "Part one!", "\n")
    sensors, beacons = get_sensors(file)
    blocs = set()
    for sensor in sensors:
        blocs.update(sensor.blocks_in_row(row_in_question))
    score = len(blocs) - sum(1 for b in beacons if b[1] == row_in_question)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def part_two(file, tgt=None, maximum=20):
    print("\n\n", "Part two!", "\n")
    sensors, beacons = get_sensors(file)
    lefties, righties = [], []
    x, y = symbols('x, y')
    for sensor in sensors:
        c_vals = sensor.get_c_vals()
        lefties.append(Eq(y, x + c_vals[0]))
        lefties.append(Eq(y, x + c_vals[1]))
        righties.append(Eq(y, -x + c_vals[2]))
        righties.append(Eq(y, -x + c_vals[3]))
    crosses = set()
    for l in lefties:
        for r in righties:
            soln = solve((l, r), (x, y))
            if all(v.is_integer for v in soln.values()):
                crosses.add((soln[x], soln[y]))
    crosses = set(filter(lambda c: valid(c, [maximum, maximum]), crosses))
    print(len(crosses), crosses)
    score = 0
    mult = 4000000
    for cross in crosses:
        for s in sensors:
            if s.is_in_range(cross):
                break
        else:
            score = cross[0] * mult + cross[1]
            break
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

    part_one(test_file, 26, 10)
    part_one(data_file, row_in_question=2000000)
    part_two(test_file, 56000011)
    part_two(data_file, maximum = 4000000)


if __name__ == '__main__':
    main()
