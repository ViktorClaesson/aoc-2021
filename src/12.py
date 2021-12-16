from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import utils


@dataclass
class Cave:
    name: str
    big: bool = field(init=False)
    small: bool = field(init=False)
    connected_caves: list[Cave] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.big = self.name.isupper()
        self.small = not self.big

    def __lt__(self, other: Cave):
        return self.name.__lt__(other.name)

    def __str__(self) -> str:
        return self.name.__str__()


def create_cave_network(connections: list[str]) -> dict[str, Cave]:
    caves: dict[str, Cave] = {}
    for line in connections:
        cave_name_0, cave_name_1 = line.split("-")
        if cave_name_0 not in caves:
            caves[cave_name_0] = Cave(name=cave_name_0)
        if cave_name_1 not in caves:
            caves[cave_name_1] = Cave(name=cave_name_1)
        caves[cave_name_0].connected_caves.append(caves[cave_name_1])
        caves[cave_name_1].connected_caves.append(caves[cave_name_0])
    return caves


def get_paths_part_1(current_cave: Cave, previous_path: list[Cave] | None = None) -> Iterable[list[Cave]]:
    previous_path: list[Cave] = previous_path or []

    if current_cave.name == "end":
        yield ", ".join(map(str, [*previous_path, current_cave]))
        return

    for next_cave in (cave for cave in current_cave.connected_caves if cave.big or cave not in previous_path):
        yield from get_paths_part_1(current_cave=next_cave, previous_path=[*previous_path, current_cave])


def part_one(path: Path) -> int:
    cave_network = create_cave_network(connections=utils.read_lines(path))
    return len(list(get_paths_part_1(current_cave=cave_network["start"])))


def get_paths_part_2(current_cave: Cave, previous_path: list[Cave] | None = None) -> Iterable[str]:
    previous_path: list[Cave] = previous_path or []

    if current_cave.name == "end" or (current_cave.small and current_cave in previous_path):
        yield from get_paths_part_1(current_cave=current_cave, previous_path=previous_path)
        return

    for next_cave in (cave for cave in current_cave.connected_caves if cave.name != "start"):
        yield from get_paths_part_2(current_cave=next_cave, previous_path=[*previous_path, current_cave])


def part_two(path: Path) -> int:
    cave_network = create_cave_network(connections=utils.read_lines(path))
    return len(list(get_paths_part_2(current_cave=cave_network["start"])))


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "12.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
