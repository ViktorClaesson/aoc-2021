def part_one() -> int:
    with open("src/8.txt") as file:
        lines = file.read().splitlines()
    easy = (2, 3, 4, 7)
    return sum(len(part) in easy for line in lines for part in line.split(" | ")[1].split())


def calculate_output(numbers: list[str], output: list[str]) -> int:
    # 1 is the only number with two lines
    one = next(n for n in numbers if len(n) == 2)
    # 1 is the only number with three lines
    seven = next(n for n in numbers if len(n) == 3)
    # 1 is the only number with four lines
    four = next(n for n in numbers if len(n) == 4)
    # 1 is the only number with seven lines
    eight = next(n for n in numbers if len(n) == 7)

    # 3 is the only number with five lines that uses both lines in 1
    three = next(n for n in numbers if len(n) == 5 and all(ch in n for ch in one))
    # 9 is the only number with six lines that has five lines in common with 3
    nine = next(n for n in numbers if len(n) == 6 and sum(ch in three for ch in n) == 5)

    # 6 is the only number with six lines that doesn't use both lines in 1
    six = next(n for n in numbers if len(n) == 6 and not all(ch in n for ch in one))
    # 5 is the only number with five lines that has five lines in common with 6
    five = next(n for n in numbers if len(n) == 5 and sum(ch in six for ch in n) == 5)

    # 0 is the only one left with six lines
    zero = next(n for n in numbers if len(n) == 6 and n not in (six, nine))
    # 2 is the only one left with five lines
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


def part_two() -> int:
    with open("src/8.txt") as file:
        lines = file.read().splitlines()
    lines = [map(lambda s: s.split(), line.split(" | ")) for line in lines]
    return sum(calculate_output(numbers, output) for numbers, output in lines)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
