def part_one() -> int:
    with open('aoc/1.txt') as file:
        ls = list(map(int, file.read().splitlines()))
        return sum(1 for c, n in zip(ls, ls[1:]) if c < n)


def part_two() -> int:
    with open('aoc/1.txt') as file:
        ls = list(map(int, file.read().splitlines()))
        ls = list(map(sum, zip(ls, ls[1:], ls[2:])))
        return sum(1 for c, n in zip(ls, ls[1:]) if c < n)


if __name__ == '__main__':
    print(part_one())
    print(part_two())
