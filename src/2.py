def translate_input(command: str) -> tuple[int, int]:
    direction, amount = command.split()
    amount = int(amount)

    if direction == 'forward':
        return amount, 0
    if direction == 'up':
        return 0, -amount
    if direction == 'down':
        return 0, amount
    raise 'Unknown direction'


def part_one() -> int:
    with open('aoc/two.txt') as file:
        ls = file.read().splitlines()

    # ls -> list[tuple[horizontal_change, vertical_change]]
    ls = map(translate_input, ls)

    # ls -> tuple[list[horizontal_change], list[vertical_change]]
    ls = zip(*ls)

    # ls -> tuple[net_horizontal_change, net_vertical_change]
    ls = tuple(map(sum, ls))

    return ls[0] * ls[1]


def part_two() -> int:
    with open('aoc/two.txt') as file:
        ls = file.read().splitlines()

    # ls -> list[tuple[steps_forward, aim_change]]
    ls = map(translate_input, ls)

    # ls -> list[tuple[steps_forward, net_aim_change]] (note: net_aim_change is at the time instance that the list index represents)
    net_aim = 0
    ls = ((steps_forward, (net_aim := change_in_aim + net_aim)) for steps_forward, change_in_aim in ls)

    # ls -> list[tuple[horizontal_change, vertical_change]]
    ls = ((steps_forward, net_aim * steps_forward) for steps_forward, net_aim in ls)

    # ls -> tuple[list[horizontal_change], list[vertical_change]]
    ls = zip(*ls)

    # ls -> tuple[net_horizontal_change, net_vertical_change]
    ls = tuple(map(sum, ls))

    return ls[0] * ls[1]


if __name__ == '__main__':
    print(part_one())
    print(part_two())
