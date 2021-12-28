from pathlib import Path

import utils


def safe_matrix_get(matrix: list[list[int]], col: int, row: int, default: int) -> int:
    if not (0 <= row < len(matrix)) or not (0 <= col < len(matrix)):
        return default
    return matrix[row][col]


def convolution(image: list[list[int]], col: int, row: int, default: int) -> int:
    return int("".join(str(safe_matrix_get(image, col + dx, row + dy, default)) for dy in range(-1, 2) for dx in range(-1, 2)), 2)


def process_image(algorithm: list[int], image: list[list[int]], steps: int) -> list[list[int]]:
    default: int = 0
    for _ in range(steps):
        image = [[algorithm[convolution(image, col, row, default)] for col in range(-1, len(image) + 1)] for row in range(-1, len(image) + 1)]
        default = algorithm[int(str(default) * 9, 2)]
    return image


def main(path: Path, n: int) -> int:
    lines = utils.read_lines(path)
    algorithm: list[int] = [1 if ch == "#" else 0 for ch in lines[0]]
    image: list[list[int]] = [[1 if ch == "#" else 0 for ch in line] for line in lines[2:]]
    image = process_image(algorithm, image, n)
    return sum(sum(row) for row in image)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "20.txt"
    print("Part 1:")
    print(main(input_path, 2))
    print("Part 2:")
    print(main(input_path, 50))
