from pathlib import Path

import utils


def part_one(path: Path) -> int:
    lines = utils.read_custom(path, int)
    return sum(1 for c, n in zip(lines, lines[1:]) if c < n)


def part_two(path: Path) -> int:
    lines = utils.read_custom(path, int)
    lines = [sum(values) for values in zip(lines, lines[1:], lines[2:])]
    return sum(1 for c, n in zip(lines, lines[1:]) if c < n)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "01.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
