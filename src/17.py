import math
from pathlib import Path

import utils


def triangle(n: int) -> int:
    return n * (n + 1) // 2


def x_n(x0: int, n: int) -> int:
    n = min(n, abs(x0))
    return n * x0 - triangle(n - 1)


def y_n(y0: int, n: int) -> int:
    return n * y0 - triangle(n - 1)


def max_height(y0: int) -> int:
    return y_n(y0, max(y0, 0))


def part_one(path: Path) -> int:
    _, y_range = utils.read_lines(path)[0][13:].split(", ")
    y_min, _ = [int(v) for v in y_range[2:].split("..")]
    # y_n = y_0 * n - n * (n - 1) * 0.5
    # =>
    # y_0 = (y_n + n * (n - 1) * 0.5) / n

    # n = -2 * y_n (P.S. just saw that this was consistently a answer)
    # => y_0 = (y_n + -2 * y_n * (-2 * y_n - 1) * 0.5) / (-2 * y_n)
    # => y_0 = -(y_n + y_n * (2 * y_n + 1)) / (2 * y_n)
    # => y_0 = -(1 + 2 * y_n + 1) / 2
    # => y_0 = -(1 + y_n)

    # to maximize the height from y_0 we want to pick the lowest y, aka y_min
    return max_height(-(y_min + 1))


def part_two(path: Path) -> int:
    x_range, y_range = utils.read_lines(path)[0][13:].split(", ")
    x_min, x_max = [int(v) for v in x_range[2:].split("..")]
    y_min, y_max = [int(v) for v in y_range[2:].split("..")]
    paths: set[tuple[int, int]] = {
        (x0, y0)
        for n in range(1, -2 * y_min + 1)
        for y in range(y_min, y_max + 1)
        for y0 in [math.floor((y + n * (n - 1) / 2) / n), math.ceil((y + n * (n - 1) / 2) / n)]
        if y_n(y0, n) == y
        for x in range(x_min, x_max + 1)
        for x0 in range(x // n, x + 1)
        if x_n(x0, n) == x
    }
    return len(paths)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "17.txt"
    print(part_one(input_path))
    print(part_two(input_path))
