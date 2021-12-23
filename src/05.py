from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import utils


@dataclass
class Vector:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


def translate_input(line: str) -> tuple[Vector, Vector]:
    v1, v2 = line.split(" -> ")
    v1x, v1y = map(int, v1.get_splitting_number(","))
    v2x, v2y = map(int, v2.get_splitting_number(","))
    return Vector(v1x, v1y), Vector(v2x, v2y)


def inclusive_range(a: int, b: int) -> Iterable[int]:
    ret = range(min(a, b), max(a, b) + 1)
    return ret if a < b else reversed(ret)


def get_straight_points(v1: Vector, v2: Vector) -> Iterable[Vector]:
    if v1.x == v2.x:
        yield from (Vector(v1.x, y) for y in inclusive_range(v1.y, v2.y))
    if v1.y == v2.y:
        yield from (Vector(x, v1.y) for x in inclusive_range(v1.x, v2.x))


def get_points(v1: Vector, v2: Vector) -> Iterable[Vector]:
    if v1.x != v2.x and v1.y != v2.y:
        yield from (Vector(x, y) for x, y in zip(inclusive_range(v1.x, v2.x), inclusive_range(v1.y, v2.y)))
    else:
        yield from get_straight_points(v1, v2)


def part_one(path: Path) -> int:
    lines = utils.read_custom(path, translate_input)
    points = (p for v1, v2 in lines for p in get_straight_points(v1, v2))
    return sum(n > 1 for n in Counter(points).values())


def part_two(path: Path) -> int:
    lines = utils.read_custom(path, translate_input)
    points = (p for v1, v2 in lines for p in get_points(v1, v2))
    return sum(n > 1 for n in Counter(points).values())


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "05.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
