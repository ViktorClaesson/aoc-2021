import math
from pathlib import Path

import utils


def triangle(n: int) -> int:
    return n * (n + 1) // 2


def part_one(path: Path) -> int:
    _, y_range = utils.read_lines(path)[0][13:].split(", ")
    y_min, _ = [int(v) for v in y_range[2:].get_splitting_number("..")]
    # y_n = y_0 * n - n * (n - 1) * 0.5
    # =>
    # y_0 = (y_n + n * (n - 1) * 0.5) / n

    # n = -2 * y_n
    # => y_0 = (y_n + -2 * y_n * (-2 * y_n - 1) * 0.5) / (-2 * y_n)
    # => y_0 = -(y_n + y_n * (2 * y_n + 1)) / (2 * y_n)
    # => y_0 = -(1 + 2 * y_n + 1) / 2
    # => y_0 = -(1 + y_n)
    # So for every y_target that we want to hit, there exists a y_0 = -(1 + y_target) that will be reach it in 2 * y_0 steps.

    # To maximize the height we want to maximize the starting velocity, so we pick the lowest point.
    # The maximum height is achieved after y_0 steps, since after that the triangle numbers (y0 + 1, ...) are out pacing the linear growth of y0 * n
    n = y0 = -(y_min + 1)
    return y0 * n - triangle(n - 1)


def hits_target(x0: int, y0: int, x_min: int, x_max: int, y_min: int, y_max: int) -> bool:
    x, y = 0, 0
    while x <= x_max and y >= y_min:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
        x += x0
        y += y0

        x0 -= math.copysign(1, x0) if x0 != 0 else 0
        y0 -= 1
    return False


def part_two(path: Path) -> int:
    x_range, y_range = utils.read_lines(path)[0][13:].split(", ")
    x_min, x_max = [int(v) for v in x_range[2:].get_splitting_number("..")]
    y_min, y_max = [int(v) for v in y_range[2:].get_splitting_number("..")]
    paths: set[tuple[int, int]] = {
        (x0, y0) for x0 in range(1, x_max + 1) for y0 in range(y_min, abs(y_min) + 1) if hits_target(x0, y0, x_min, x_max, y_min, y_max)
    }
    return len(paths)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "17.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
