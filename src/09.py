from pathlib import Path

import utils


def get_neighbours(matrix: list[list], row: int, col: int) -> list[tuple[int, int]]:
    return [
        (neighbour_row, neighbour_col)
        for neighbour_row, neighbour_col in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        if 0 <= neighbour_row < len(matrix) and 0 <= neighbour_col < len(matrix[neighbour_row])
    ]


def part_one(path: Path) -> int:
    matrix = utils.read_matrix(path)
    return sum(
        1 + matrix[row][col]
        for row in range(len(matrix))
        for col in range(len(matrix[row]))
        if all(matrix[row][col] < matrix[neighbour_row][neighbour_col] for neighbour_row, neighbour_col in get_neighbours(matrix, row, col))
    )


def fill_basin(matrix: list[list[bool]], row: int, col: int) -> int:
    if matrix[row][col]:
        return 0
    matrix[row][col] = True
    return 1 + sum(fill_basin(matrix, neighbour_row, neighbour_col) for neighbour_row, neighbour_col in get_neighbours(matrix, row, col))


def get_basin_sizes(matrix: list[list[int]]) -> list[int]:
    basin_sizes: list[int] = []
    bool_matrix: list[list[bool]] = [[n == 9 for n in row] for row in matrix]
    for row in range(len(bool_matrix)):
        for col in range(len(bool_matrix)):
            if not bool_matrix[row][col]:
                basin_sizes.append(fill_basin(bool_matrix, row, col))
    return basin_sizes


def part_two(path: Path) -> int:
    matrix = utils.read_matrix(path)
    basin_sizes: list[int] = sorted(get_basin_sizes(matrix), reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "09.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
