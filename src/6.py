from collections import Counter


def main(days: int) -> int:
    with open("src/6.txt") as file:
        lines = file.read().splitlines()
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
    print(main(days=80))
    print(main(days=256))
