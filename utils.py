import __main__


def file_name():
    """Extract day number from the main file name for loading data/test files."""
    raw = __main__.__file__
    raw = raw[raw.find("day") + 3:-3]
    return raw


def get_rect_neighbours(point, dims):
    options = ((-1, 0), (1, 0), (0, -1), (0, 1))
    rect_neighbours = []
    for option in options:
        pos = add(option, point)
        if valid(pos, dims):
            rect_neighbours.append(pos)
    return rect_neighbours


def get_all_neighbours(point, dims=None):
    options = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
    rect_neighbours = []
    for option in options:
        pos = add(option, point)
        if dims:
            if valid(pos, dims):
                rect_neighbours.append(pos)
        else:
            rect_neighbours.append(pos)
    return rect_neighbours


def is_adjacent(pointa, pointb):
    diffs = [abs(pointa[i] - pointb[i]) for i in range(len(pointa))]
    return max(diffs) < 2


def hat(vector):
    vector = [x // abs(x) if x else 0 for x in vector]
    return vector


def show_grid(grid):
    """Display a character grid."""
    for row in grid:
        print("".join(row))
    print("\n\n")


def show_bool_grid(grid):
    """Display a boolean grid as # (False) and . (True)."""
    for row in grid:
        n = ["." if x else "#" for x in row]
        print("".join(n))
    print("\n\n")


def valid(point, dims):
    """Check if a point is within grid bounds."""
    return greater(point, (-1 for _ in point)) and greater(dims, point)


def add(a, b):
    """Add two tuples element-wise."""
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    """Subtract two tuples element-wise."""
    return tuple(x - y for x, y in zip(a, b))


def greater(a, b):
    """Check if all elements in tuple a are greater than tuple b."""
    return all(tuple(x > y for x, y in zip(a, b)))


def taxicab(a, b):
    """Return the taxicab distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def prod(*args):
    """Calculate the product of all arguments."""
    ans = 1
    for x in args:
        ans *= x
    return ans


def scale(scalar, vector):
    """Scale a vector by a scalar."""
    return tuple(x * scalar for x in vector)

def show(ddict):
    for k, v in ddict.items():
        print(k, v)