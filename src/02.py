from pathlib import Path

import utils


def translate_input(command: str) -> tuple[int, int]:
    direction, amount = command.split()
    amount = int(amount)

    if direction == "forward":
        return amount, 0
    if direction == "up":
        return 0, -amount
    if direction == "down":
        return 0, amount
    raise "Unknown direction"


def part_one(path: Path) -> int:
    # list[tuple[horizontal_change, vertical_change]]
    lines = utils.read_custom(path, translate_input)

    # transform from previous type to:
    # * tuple[list[horizontal_change], list[vertical_change]]
    lines = zip(*lines)

    # transform from previous type to:
    # * tuple[net_horizontal_change, net_vertical_change]
    lines = tuple(map(sum, lines))

    return lines[0] * lines[1]


def part_two(path: Path) -> int:
    # list[tuple[steps_forward, aim_change]]
    lines = utils.read_custom(path, translate_input)

    # transform from previous type to:
    # * list[tuple[steps_forward, net_aim_change]] (note: net_aim_change is at the time instance that the list index represents)
    net_aim = 0
    lines = ((steps_forward, (net_aim := change_in_aim + net_aim)) for steps_forward, change_in_aim in lines)

    # transform from previous type to:
    # * list[tuple[horizontal_change, vertical_change]]
    lines = ((steps_forward, net_aim * steps_forward) for steps_forward, net_aim in lines)

    # transform from previous type to:
    # * tuple[list[horizontal_change], list[vertical_change]]
    lines = zip(*lines)

    # transform from previous type to:
    # * tuple[net_horizontal_change, net_vertical_change]
    lines = tuple(map(sum, lines))

    return lines[0] * lines[1]


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "02.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
