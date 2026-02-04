from collections import namedtuple

from utils import file_name

File = namedtuple('File', ['size', 'name'])


class Directory:
    def __init__(self, name, ):
        self.name = name
        self.subdirs = []
        self.files = []

    def add_subdir(self, subdir):
        self.subdirs.append(subdir)

    def add_file(self, file):
        self.files.append(file)

    def get_size(self):
        size = sum(f.size for f in self.files) + sum(d.get_size() for d in self.subdirs)
        return size

    def __repr__(self):
        return f'{self.name}, {self.get_size()}, {self.files}, {self.subdirs}'


def get_score(directories):
    score = 0
    for d in directories.values():
        size = d.get_size()
        if size <= 100000:
            score += size
    return score

def explore_volume(directories, file):
    path = []
    for row in file.split("\n"):
        if row.startswith("$ cd .."):
            path.pop()
        elif row.startswith("$ cd"):
            d_name = row.split(" ")[-1]
            path.append(d_name)
            full_path = "/".join(path)
            if full_path not in directories:
                directories[full_path] = Directory(full_path)
        elif row.startswith("$"):
            pass
        elif row.startswith("dir"):
            sub_name = row.split(" ")[-1]
            sub_path = "/".join(path + [sub_name])
            sub_dir = Directory(sub_path)
            directories[sub_path] = sub_dir
            directories["/".join(path)].add_subdir(sub_dir)
        else:
            s, n = row.split(" ")
            s = int(s)
            directories["/".join(path)].add_file(File(s, n))


def part_one(file, tgt=None):
    print("\n\n", "Part one!", "\n")
    directories = {}
    explore_volume(directories, file)
    score = get_score(directories)
    if tgt:
        print("Great success!") if score == tgt else print(f"Awww, too bad, target is {tgt}, not {score}")
    else:
        print(f"Score is {score}")


def score_2(directories, tgt):
    print(tgt)
    possibles = [d.get_size() for d in directories.values()]
    possibles = filter(lambda p: p >= tgt, possibles)
    return min(possibles)


def part_two(file, tgt=None):
    print("\n\n", "Part two!", "\n")
    total = 70000000
    need = 30000000
    directories = {}
    explore_volume(directories, file)
    full = directories["/"].get_size()
    target = need - (total - full)
    score = score_2(directories, target)
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

    part_one(test_file, 95437)
    part_one(data_file)
    part_two(test_file, 24933642)
    part_two(data_file)


if __name__ == '__main__':
    main()
