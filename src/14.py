from collections import Counter, defaultdict
from typing import Callable, Any, Generator
from functools import reduce


Polymer = dict[str, int]


def repeat(fn: Callable[[Any], Any], initial: Any, n: int) -> Any:
    return reduce(lambda acc, _: fn(acc), range(n), initial)

def repeat_generator(fn: Callable[[Any], Any], initial: Any) -> Generator[Any, None, None]:
    while True:
        yield initial
        initial = fn(initial)


def part_one() -> int:
    with open("src/14.txt") as file:
        ls = file.read().splitlines()

    polymer: str = ls[0]
    rules: dict[str, str] = {pair: insert for pair, insert in (rule.split(' -> ') for rule in ls[2:])}

    for i in range(10):
        polymer = ''.join(f"{A}{rules.get(f'{A}{B}', '')}" for A, B in zip(polymer, polymer[1:] + ' '))

    character_counts = Counter(polymer)
    return max(character_counts.values()) - min(character_counts.values())


def part_two() -> int:
    with open("src/14.txt") as file:
        ls: list[str] = file.read().splitlines()

    polymer: dict[str, int] = {key: value for key, value in Counter(''.join(chs) for chs in zip(ls[0], ls[0][1:] + ' ')).items()}
    rules: dict[str, str] = {pair: insert for pair, insert in (rule.split(' -> ') for rule in ls[2:])}

    for _ in range(40):
        new_polymer = defaultdict(int)
        for pair, count in polymer.items():
            if pair in rules:
                middle_ch = rules.get(pair)
                left_pair, right_pair = pair[0] + middle_ch, middle_ch + pair[1]
                new_polymer[left_pair] += count
                new_polymer[right_pair] += count
            else:
                new_polymer[pair] += count
        polymer = new_polymer

    character_counts = [sum(value for key, value in polymer.items() if key[0] == ch) for ch in set(key[0] for key in polymer.keys())]
    return max(character_counts) - min(character_counts)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
