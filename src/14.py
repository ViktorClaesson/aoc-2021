from collections import Counter, defaultdict
from pathlib import Path

import utils

Polymer = dict[str, int]


def part_one(path: Path) -> int:
    lines = utils.read_lines(path)

    polymer: str = lines[0]
    rules: dict[str, str] = {pair: insert for pair, insert in (rule.split(" -> ") for rule in lines[2:])}

    for i in range(10):
        polymer = "".join(f"{A}{rules.get(f'{A}{B}', '')}" for A, B in zip(polymer, polymer[1:] + " "))

    character_counts = Counter(polymer)
    return max(character_counts.values()) - min(character_counts.values())


def part_two(path: Path) -> int:
    lines = utils.read_lines(path)

    polymer: dict[str, int] = {key: value for key, value in Counter("".join(chs) for chs in zip(lines[0], lines[0][1:] + " ")).items()}
    rules: dict[str, str] = {pair: insert for pair, insert in (rule.split(" -> ") for rule in lines[2:])}

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
    input_path = Path(__file__).parents[1] / "inputs" / "14.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
