from pathlib import Path

import utils


def get_neighbours(matrix: list[list], x: int, y: int):
    return [
        (nx, ny)
        for nx, ny in [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        if 0 <= ny < len(matrix)
        if 0 <= nx < len(matrix[ny])
    ]


def next_step(matrix: list[list[int]]) -> list[list[int]]:
    new_matrix = [[i + 1 for i in row] for row in matrix]
    flash_queue = {(x, y) for y, row in enumerate(new_matrix) for x, v in enumerate(row) if v == 10}
    while flash_queue:
        x, y = flash_queue.pop()
        for nx, ny in get_neighbours(new_matrix, x, y):
            new_matrix[ny][nx] += 1
            if new_matrix[ny][nx] == 10:
                flash_queue.add((nx, ny))
    return [[v if v < 10 else 0 for v in row] for row in new_matrix]


def part_one(path: Path) -> int:
    matrix = utils.read_matrix(path)
    flash_count: int = 0
    for i in range(100):
        matrix = next_step(matrix)
        flash_count += sum(row.count(0) for row in matrix)
    return flash_count


def part_two(path: Path) -> int:
    matrix = utils.read_matrix(path)
    step_count = 0
    while True:
        if all(v == 0 for row in matrix for v in row):
            break
        matrix = next_step(matrix)
        step_count += 1
    return step_count


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "input" / "11.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
