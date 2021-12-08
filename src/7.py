from typing import Callable


def triangle(n: int) -> int:
    if n <= 0:
        return 0
    return (1 + n) * n // 2


def cost(crabs: list[int], level: int, f: Callable[[int], int]) -> int:
    return sum(f(abs(level - height)) for height in crabs)


def main(f: Callable[[int], int] = lambda x: x) -> int:
    with open("src/7.txt") as file:
        crabs: list[int] = list(map(int, file.read().splitlines()[0].split(",")))
    return min(cost(crabs, level, f) for level in range(min(crabs), max(crabs) + 1))


if __name__ == "__main__":
    print(main())
    print(main(triangle))
