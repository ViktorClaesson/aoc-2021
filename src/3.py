def part_one() -> int:
    with open('aoc/3.txt') as file:
        ls = map(list, file.read().splitlines())

    ls = zip(*ls)
    gamma = list(map(lambda bits: 1 if sum(map(int, bits)) / len(bits) >= 0.5 else 0, ls))
    epsilon = [1 - x for x in gamma]

    gamma = int(''.join(map(str, gamma)), 2)
    epsilon = int(''.join(map(str, epsilon)), 2)

    return gamma * epsilon


def part_two_rec(ls: list[str], most_common: bool, index: int = 0) -> int:
    if len(ls) == 1:
        return int(''.join(ls[0]), 2)

    bits = list(zip(*ls))[index]
    check_bit = 1 if sum(map(int, bits)) / len(bits) >= 0.5 else 0
    if not most_common:
        check_bit = 1 - check_bit

    check_bit = str(check_bit)
    return part_two_rec([s for s in ls if s[index] == check_bit], most_common, index+1)


def part_two() -> int:
    with open('aoc/3.txt') as file:
        ls = file.read().splitlines()
    return part_two_rec(ls, True) * part_two_rec(ls, False)


if __name__ == '__main__':
    print(part_one())
    print(part_two())
