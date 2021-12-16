from pathlib import Path
from typing import Callable

import utils


def triangle(n: int) -> int:
    return (1 + n) * n // 2


def cost(crabs: list[int], level: int, f: Callable[[int], int]) -> int:
    return sum(f(abs(level - height)) for height in crabs)


def main(path: Path, f: Callable[[int], int] = lambda x: x) -> int:
    crabs: list[int] = [int(v) for v in utils.read_lines(path)[0].split(",")]
    return min(cost(crabs, level, f) for level in range(min(crabs), max(crabs) + 1))


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "07.txt"
    print("Part 1:")
    print(main(input_path))
    print("Part 2:")
    print(main(input_path, triangle))
