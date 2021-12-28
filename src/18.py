from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from operator import add
from pathlib import Path

import utils


@dataclass
class LiteralNumber:
    value: int
    left_neighbour: LiteralNumber | None = None
    right_neighbour: LiteralNumber | None = None

    def __str__(self) -> str:
        return f"{self.value}"

    def magnitude(self) -> int:
        return self.value

    def split(self) -> SnailFishNumber:
        # create new literals
        left = LiteralNumber(self.value // 2)
        right = LiteralNumber((self.value + 1) // 2)

        # reroute neighbours
        left.right_neighbour = right
        if self.left_neighbour:
            left.left_neighbour = self.left_neighbour
            self.left_neighbour.right_neighbour = left

        right.left_neighbour = left
        if self.right_neighbour:
            right.right_neighbour = self.right_neighbour
            self.right_neighbour.left_neighbour = right

        return SnailFishNumber(left=left, right=right)


@dataclass
class SnailFishNumber:
    left: SnailFishNumber | LiteralNumber
    right: SnailFishNumber | LiteralNumber

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def get_edge_literal(self, left: bool) -> LiteralNumber:
        current = self
        while isinstance(current, SnailFishNumber):
            current = current.left if left else current.right
        return current

    def __add__(self, other: SnailFishNumber) -> SnailFishNumber:
        other_left_most: LiteralNumber = other.get_edge_literal(left=True)
        self_right_most: LiteralNumber = self.get_edge_literal(left=False)
        self_right_most.right_neighbour = other_left_most
        other_left_most.left_neighbour = self_right_most
        return SnailFishNumber(left=self, right=other).fully_reduced()

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def fully_reduced(self) -> SnailFishNumber:
        while self.did_explode() or self.did_split():
            pass
        return self

    def try_explode(self, nested_level: int) -> LiteralNumber:
        if nested_level >= 4 and isinstance(self.left, LiteralNumber) and isinstance(self.right, LiteralNumber):
            new_literal = LiteralNumber(value=0)

            # reroute neighbours
            if self.left.left_neighbour:
                self.left.left_neighbour.value += self.left.value
                new_literal.left_neighbour = self.left.left_neighbour
                self.left.left_neighbour.right_neighbour = new_literal
            if self.right.right_neighbour:
                self.right.right_neighbour.value += self.right.value
                new_literal.right_neighbour = self.right.right_neighbour
                self.right.right_neighbour.left_neighbour = new_literal
            return new_literal

    def did_explode(self, nested_level: int = 0) -> bool:
        if isinstance(self.left, SnailFishNumber):
            if result := self.left.try_explode(nested_level + 1):
                self.left = result
                return True
            elif self.left.did_explode(nested_level + 1):
                return True
        if isinstance(self.right, SnailFishNumber):
            if result := self.right.try_explode(nested_level + 1):
                self.right = result
                return True
            elif self.right.did_explode(nested_level + 1):
                return True
        return False

    def did_split(self) -> bool:
        if isinstance(self.left, LiteralNumber) and self.left.value >= 10:
            self.left = self.left.split()
            return True
        if isinstance(self.left, SnailFishNumber) and self.left.did_split():
            return True
        if isinstance(self.right, LiteralNumber) and self.right.value >= 10:
            self.right = self.right.split()
            return True
        if isinstance(self.right, SnailFishNumber) and self.right.did_split():
            return True
        return False


def split_top_level_comma(line: str) -> tuple[str, str]:
    nest_level = 0
    for index, character in enumerate(line):
        if character == "[":
            nest_level += 1
        elif character == "]":
            nest_level -= 1
        elif character == "," and nest_level == 0:
            return line[:index], line[index + 1 :]
    raise Exception(f"found no root level comma in line: {line}")


def parse_literal_numeral(line: str, previous_literal: LiteralNumber | None = None) -> tuple[LiteralNumber, LiteralNumber]:
    literal = LiteralNumber(value=int(line))
    if previous_literal:
        previous_literal.right_neighbour = literal
        literal.left_neighbour = previous_literal
    return literal, literal


def parse_snail_fish_number(line: str, previous_literal: LiteralNumber | None = None) -> tuple[SnailFishNumber, LiteralNumber]:
    left, right = split_top_level_comma(line[1:-1])
    left, previous_literal = (
        parse_literal_numeral(line=left, previous_literal=previous_literal)
        if len(left) == 1
        else parse_snail_fish_number(line=left, previous_literal=previous_literal)
    )
    right, previous_literal = (
        parse_literal_numeral(line=right, previous_literal=previous_literal)
        if len(right) == 1
        else parse_snail_fish_number(line=right, previous_literal=previous_literal)
    )
    return SnailFishNumber(left=left, right=right), previous_literal


def part_one(path: Path) -> int:
    snail_fish_numbers: list[SnailFishNumber] = utils.read_custom(path, lambda line: parse_snail_fish_number(line)[0])
    return reduce(add, snail_fish_numbers).magnitude()


def part_two(path: Path) -> int:
    numbers: list[str] = utils.read_lines(path)
    return max((parse_snail_fish_number(n1)[0] + parse_snail_fish_number(n2)[0]).magnitude() for n1 in numbers for n2 in numbers if n1 != n2)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "18.txt"

    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
