from pathlib import Path

import utils


def part_one(path: Path) -> int:
    rows = utils.read_lines(path)

    columns = zip(*rows)
    gamma = [1 if column.count("1") * 2 >= len(column) else 0 for column in columns]
    epsilon = [1 - x for x in gamma]

    gamma = int("".join(map(str, gamma)), 2)
    epsilon = int("".join(map(str, epsilon)), 2)

    return gamma * epsilon


def part_two_rec(rows: list[str], most_common: bool, index: int = 0) -> int:
    if len(rows) == 1:
        return int("".join(rows[0]), 2)

    column = list(zip(*rows))[index]
    check_bit = 1 if column.count("1") * 2 >= len(column) else 0
    if not most_common:
        check_bit = 1 - check_bit

    check_bit = str(check_bit)
    return part_two_rec([s for s in rows if s[index] == check_bit], most_common, index + 1)


def part_two(path: Path) -> int:
    rows = utils.read_lines(path)
    return part_two_rec(rows, True) * part_two_rec(rows, False)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "03.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
