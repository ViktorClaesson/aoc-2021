def part_one() -> int:
    with open("src/8.txt") as file:
        lines = file.read().splitlines()
    easy = (2, 3, 4, 7)
    return sum(len(part) in easy for line in lines for part in line.split(" | ")[1].split())


def calculate_output(numbers: list[str], output: list[str]) -> int:
    one = next(number for number in numbers if len(number) == 2)
    seven = next(number for number in numbers if len(number) == 3)
    four = next(number for number in numbers if len(number) == 4)
    eight = next(number for number in numbers if len(number) == 7)

    three = next(number for number in numbers if len(number) == 5 and all(ch in number for ch in one))
    nine = next(number for number in numbers if len(number) == 6 and sum(ch in three for ch in number) == 5)

    six = next(number for number in numbers if len(number) == 6 and not all(ch in number for ch in one))
    five = next(number for number in numbers if len(number) == 5 and sum(ch in six for ch in number) == 5)

    zero = next(number for number in numbers if len(number) == 6 and number not in (six, nine))
    two = next(number for number in numbers if len(number) == 5 and number not in (five, three))

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
