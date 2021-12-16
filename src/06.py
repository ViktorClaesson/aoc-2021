from collections import Counter
from pathlib import Path

import utils


def main(path: Path, days: int) -> int:
    lines = utils.read_lines(path)
    fish = Counter(map(int, lines[0].split(",")))
    for day in range(days):
        fish = {rem - 1: count for rem, count in fish.items()}
        if -1 in fish:
            fish[8] = fish[-1]
            if 6 in fish:
                fish[6] += fish[-1]
            else:
                fish[6] = fish[-1]
            del fish[-1]
    return sum(fish.values())


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "06.txt"
    print("Part 1:")
    print(main(input_path, days=80))
    print("Part 2:")
    print(main(input_path, days=256))
