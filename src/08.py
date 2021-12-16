from pathlib import Path

import utils


def part_one(path: Path) -> int:
    lines = utils.read_custom(path, lambda line: line.split(" | ")[1].split())
    easy = (2, 3, 4, 7)
    return sum(len(part) in easy for line in lines for part in line)


def calculate_output(numbers: list[str], output: list[str]) -> int:
    # 1 is the only number with two rows
    one = next(n for n in numbers if len(n) == 2)
    # 1 is the only number with three rows
    seven = next(n for n in numbers if len(n) == 3)
    # 1 is the only number with four rows
    four = next(n for n in numbers if len(n) == 4)
    # 1 is the only number with seven rows
    eight = next(n for n in numbers if len(n) == 7)

    # 3 is the only number with five rows that uses both rows in 1
    three = next(n for n in numbers if len(n) == 5 and all(ch in n for ch in one))
    # 9 is the only number with six rows that has five rows in common with 3
    nine = next(n for n in numbers if len(n) == 6 and sum(ch in three for ch in n) == 5)

    # 6 is the only number with six rows that doesn't use both rows in 1
    six = next(n for n in numbers if len(n) == 6 and not all(ch in n for ch in one))
    # 5 is the only number with five rows that has five rows in common with 6
    five = next(n for n in numbers if len(n) == 5 and sum(ch in six for ch in n) == 5)

    # 0 is the only one left with six rows
    zero = next(n for n in numbers if len(n) == 6 and n not in (six, nine))
    # 2 is the only one left with five rows
    two = next(n for n in numbers if len(n) == 5 and n not in (five, three))

    translator = {
        "".join(sorted(zero)): "0",
        "".join(sorted(one)): "1",
        "".join(sorted(two)): "2",
        "".join(sorted(three)): "3",
        "".join(sorted(four)): "4",
        "".join(sorted(five)): "5",
        "".join(sorted(six)): "6",
        "".join(sorted(seven)): "7",
        "".join(sorted(eight)): "8",
        "".join(sorted(nine)): "9",
    }

    return int("".join(translator["".join(sorted(s))] for s in output))


def part_two(path: Path) -> int:
    lines = utils.read_custom(path, lambda line: [part.split() for part in line.split(" | ")])
    return sum(calculate_output(numbers, output) for numbers, output in lines)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "08.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
