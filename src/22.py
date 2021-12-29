from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import utils


@dataclass
class Instruction:
    state: bool
    x_range: range
    y_range: range
    z_range: range


def parse_instruction(line: str) -> Instruction:
    state, ranges = line.split(" ")
    x_range, y_range, z_range = [c_range[2:].split("..") for c_range in ranges.split(",")]
    x_range = range(int(x_range[0]), int(x_range[1]) + 1)
    y_range = range(int(y_range[0]), int(y_range[1]) + 1)
    z_range = range(int(z_range[0]), int(z_range[1]) + 1)
    return Instruction(state=state == "on", x_range=x_range, y_range=y_range, z_range=z_range)


def part_one(path: Path) -> int:
    initialization: dict[tuple[int, int, int], bool] = {}
    instructions: list[Instruction] = utils.read_custom(path, parse_instruction)
    for instruction in instructions:
        if (
            -50 <= instruction.x_range.start <= instruction.x_range.stop <= 50 + 1
            and -50 <= instruction.y_range.start <= instruction.y_range.stop <= 50 + 1
            and -50 <= instruction.z_range.start <= instruction.z_range.stop <= 50 + 1
        ):
            for x in instruction.x_range:
                for y in instruction.y_range:
                    for z in instruction.z_range:
                        initialization[(x, y, z)] = instruction.state
    return sum(initialization.values())


class Cuboid:
    state: bool
    x_range: Range
    y_range: Range
    z_range: Range

    def __init__(self, state: bool, x_range: Range, y_range: Range, z_range: Range):
        self.state = state
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    @staticmethod
    def intersects(cuboid_1: Cuboid, cuboid_2: Cuboid) -> bool:
        return (
            Range.intersects(cuboid_1.x_range, cuboid_2.x_range)
            and Range.intersects(cuboid_1.y_range, cuboid_2.y_range)
            and Range.intersects(cuboid_1.z_range, cuboid_2.z_range)
        )

    def __hash__(self):
        return hash((self.x_range, self.y_range, self.z_range))

    def __eq__(self, other):
        if not isinstance(other, Cuboid):
            return NotImplemented
        return self.x_range == other.x_range and self.y_range == other.y_range and self.z_range == other.z_range

    def __contains__(self, item: Cuboid) -> bool:
        if not isinstance(item, Cuboid):
            return NotImplemented
        return item.x_range in self.x_range and item.y_range in self.y_range and item.z_range in self.z_range

    def is_valid(self) -> bool:
        return self.x_range.is_valid() and self.y_range.is_valid() and self.z_range.is_valid()

    def size(self) -> int:
        return self.x_range.size() * self.y_range.size() * self.z_range.size()

    def __str__(self):
        return f"[{'on' if self.state else 'off'}, X:{self.x_range}, Y:{self.y_range}, Z:{self.z_range}]"


class Range:
    min: int
    max: int

    @staticmethod
    def intersects(range_1: Range, range_2: Range) -> bool:
        return range_1.min <= range_2.max and range_1.max >= range_2.min

    def __init__(self, r_min: int, r_max: int):
        self.min = r_min
        self.max = r_max

    def __hash__(self):
        return hash((self.min, self.max))

    def __eq__(self, other):
        if not isinstance(other, Range):
            return NotImplemented
        return self.min == other.min and self.max == other.max

    def __contains__(self, item: Range):
        if not isinstance(item, Range):
            return NotImplemented
        return self.min <= item.min <= item.max <= self.max

    def is_valid(self) -> bool:
        return self.max >= self.min

    def size(self) -> int:
        return self.max - self.min + 1

    def __str__(self):
        return f"({self.min}, {self.max})"


def parse_cuboid(line: str) -> Cuboid:
    state, ranges = line.split(" ")
    x_range, y_range, z_range = [c_range[2:].split("..") for c_range in ranges.split(",")]
    x_range = Range(r_min=int(x_range[0]), r_max=int(x_range[1]))
    y_range = Range(r_min=int(y_range[0]), r_max=int(y_range[1]))
    z_range = Range(r_min=int(z_range[0]), r_max=int(z_range[1]))
    return Cuboid(state=state == "on", x_range=x_range, y_range=y_range, z_range=z_range)


def split_reactor_range(reactor_cuboid_range: Range, instruction_range: Range) -> list[Range]:
    if instruction_range not in reactor_cuboid_range:
        raise Exception(f"reactor_cuboid_range must contain instruction_range, {reactor_cuboid_range}, {instruction_range}")

    return [
        reactor_range
        for reactor_range in (
            Range(reactor_cuboid_range.min, instruction_range.min - 1),
            Range(instruction_range.min, instruction_range.max),
            Range(instruction_range.max + 1, reactor_cuboid_range.max),
        )
        if reactor_range.is_valid()
    ]


def make_sub_reactor_cuboids(reactor_cuboid: Cuboid, instruction: Cuboid) -> list[Cuboid]:
    if instruction not in reactor_cuboid:
        return [reactor_cuboid]

    return [
        Cuboid(state=reactor_cuboid.state, x_range=new_x_range, y_range=new_y_range, z_range=new_z_range)
        for new_x_range in split_reactor_range(reactor_cuboid.x_range, instruction.x_range)
        for new_y_range in split_reactor_range(reactor_cuboid.y_range, instruction.y_range)
        for new_z_range in split_reactor_range(reactor_cuboid.z_range, instruction.z_range)
        if (new_x_range != instruction.x_range) or (new_y_range != instruction.y_range) or (new_z_range != instruction.z_range)
    ]


def split_instruction_range(reactor_cuboid_range: Range, instruction_range: Range) -> list[Range]:
    if instruction_range.min < reactor_cuboid_range.min and instruction_range.max > reactor_cuboid_range.max:
        #    |------|    <- reactor
        # |------------| <- instruction
        #       =>
        #    |------|
        # |-||------||-|
        instruction_left = Range(instruction_range.min, reactor_cuboid_range.min - 1)
        instruction_middle = Range(reactor_cuboid_range.min, reactor_cuboid_range.max)
        instruction_right = Range(reactor_cuboid_range.max + 1, instruction_range.max)
        return [instruction_left, instruction_middle, instruction_right]
    elif instruction_range.min < reactor_cuboid_range.min <= instruction_range.max <= reactor_cuboid_range.max:
        #    |------|    <- reactor
        # |-------|      <- instruction
        #       =>
        #    |------|
        # |-||----|
        instruction_left = Range(instruction_range.min, reactor_cuboid_range.min - 1)
        instruction_right = Range(reactor_cuboid_range.min, instruction_range.max)
        return [instruction_left, instruction_right]
    elif reactor_cuboid_range.min <= instruction_range.min <= reactor_cuboid_range.max < instruction_range.max:
        #    |------|    <- reactor
        #      |-------| <- instruction
        #       =>
        #    |------|
        #      |----||-|
        instruction_left = Range(instruction_range.min, reactor_cuboid_range.max)
        instruction_right = Range(reactor_cuboid_range.max + 1, instruction_range.max)
        return [instruction_left, instruction_right]
    else:
        return [instruction_range]


def make_sub_instructions(reactor_cuboid: Cuboid, instruction: Cuboid) -> list[Cuboid]:
    if not Cuboid.intersects(reactor_cuboid, instruction):
        return [instruction]

    if instruction in reactor_cuboid:
        return [instruction]

    sub_instructions = [
        Cuboid(
            state=instruction.state,
            x_range=new_x_range,
            y_range=new_y_range,
            z_range=new_z_range,
        )
        for new_x_range in split_instruction_range(reactor_cuboid.x_range, instruction.x_range)
        for new_y_range in split_instruction_range(reactor_cuboid.y_range, instruction.y_range)
        for new_z_range in split_instruction_range(reactor_cuboid.z_range, instruction.z_range)
    ]
    return sub_instructions


def make_all_sub_instructions(reactor: set[Cuboid], instruction: Cuboid) -> set[Cuboid]:
    sub_instructions: set[Cuboid] = {instruction}
    for reactor_cuboid in reactor:
        sub_instructions = {
            new_sub_instruction
            for sub_instruction in sub_instructions
            for new_sub_instruction in make_sub_instructions(reactor_cuboid, sub_instruction)
        }
    return sub_instructions


def handle_instruction_for_reactor(reactor: set[Cuboid], instruction: Cuboid) -> set[Cuboid]:
    global part_1, part_2, part_3
    time_0 = datetime.now().timestamp()

    # 1. Filter out any reactor_cuboids that are a subset of the instruction cuboid
    new_reactor = {reactor_cuboid for reactor_cuboid in reactor if reactor_cuboid not in instruction}
    part_1 += datetime.now().timestamp() - time_0
    time_0 = datetime.now().timestamp()

    sub_instructions: set[Cuboid] = {instruction}
    while sub_instructions:
        sub_instruction = sub_instructions.pop()

        # 2. Split instruction into sub instructions until each sub_instruction either does not intersect any reactor_cuboid or is a subset of one
        if any(Cuboid.intersects(reactor_cuboid, sub_instruction) for reactor_cuboid in new_reactor if sub_instruction not in reactor_cuboid):
            new_sub_instructions = make_all_sub_instructions(new_reactor, sub_instruction)
            for new_sub_instruction in new_sub_instructions:
                if not any(Cuboid.intersects(reactor_cuboid, new_sub_instruction) for reactor_cuboid in new_reactor):
                    if new_sub_instruction.state:
                        new_reactor.add(new_sub_instruction)
                else:
                    sub_instructions.add(new_sub_instruction)
            continue

        part_2 += datetime.now().timestamp() - time_0
        time_0 = datetime.now().timestamp()

        # 3. Handle a sub instruction
        if sub_instruction.state:
            if not any(sub_instruction in reactor_cuboid for reactor_cuboid in new_reactor):
                new_reactor.add(sub_instruction)
        else:
            for reactor_cuboid in new_reactor:
                if sub_instruction in reactor_cuboid:
                    new_reactor.remove(reactor_cuboid)
                    new_reactor.update(make_sub_reactor_cuboids(reactor_cuboid, sub_instruction))
                    break
        part_3 += datetime.now().timestamp() - time_0
        time_0 = datetime.now().timestamp()

    return new_reactor


def part_two(path: Path) -> int:
    reactor: set[Cuboid] = set()
    instructions: list[Cuboid] = utils.read_custom(path, parse_cuboid)
    for index, instruction in enumerate(instructions):
        print(f"instruction {index+1} / {len(instructions)}")
        reactor = handle_instruction_for_reactor(reactor, instruction)

    return sum(reactor_cuboid.state * reactor_cuboid.size() for reactor_cuboid in reactor)


part_1 = 0
part_2 = 0
part_3 = 0
if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "22.txt"

    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))

    print(f"part_1 total time: {part_1:.3f}s")
    print(f"part_2 total time: {part_2:.3f}s")
    print(f"part_3 total time: {part_3:.3f}s")
