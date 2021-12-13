from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class Cave:
    name: str
    big: bool = field(init=False)
    connected_caves: list[Cave] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.big = self.name.isupper()

    def __lt__(self, other: Cave):
        return self.name.__lt__(other.name)

    def __str__(self) -> str:
        return self.name.__str__()


def get_paths_part_1(path: list[Cave], cave: Cave) -> Iterable[list[Cave]]:
    if cave.name == "end":
        yield ", ".join(map(str, [*path, cave]))
        return

    for next_cave in (c for c in cave.connected_caves if c.big or c not in path):
        yield from get_paths_part_1([*path, cave], next_cave)


def create_cave_network(connections: list[str]) -> Cave:
    caves = {}
    for line in connections:
        cave0_name, cave1_name = line.split("-")
        if cave0_name not in caves:
            caves[cave0_name] = Cave(name=cave0_name)
        if cave1_name not in caves:
            caves[cave1_name] = Cave(name=cave1_name)
        caves[cave0_name].connected_caves.append(caves[cave1_name])
        caves[cave1_name].connected_caves.append(caves[cave0_name])
    return caves["start"]


def part_one() -> int:
    with open("src/12.txt") as file:
        start = create_cave_network(connections=file.read().splitlines())
        return len(list(get_paths_part_1(path=[], cave=start)))


def get_paths_part_2(path: list[Cave], cave: Cave) -> Iterable[str]:
    if cave.name == "end" or (not cave.big and path.count(cave) == 1):
        yield from get_paths_part_1(path, cave)
        return

    for next_cave in (c for c in cave.connected_caves if c.name != "start"):
        yield from get_paths_part_2([*path, cave], next_cave)


def part_two() -> int:
    with open("src/12.txt") as file:
        start = create_cave_network(connections=file.read().splitlines())
        return len(list(get_paths_part_2(path=[], cave=start)))


if __name__ == "__main__":
    print(part_one())
    print(part_two())
