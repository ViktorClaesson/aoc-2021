from pathlib import Path
from typing import Callable, TypeVar

T = TypeVar("T")


def read_lines(path: Path) -> list[str]:
    with path.open() as file:
        return file.read().splitlines()


def read_custom(path: Path, f: Callable[[str], T]) -> list[T]:
    return [f(line) for line in read_lines(path)]


def read_matrix(path: Path) -> list[list[int]]:
    return [[int(ch) for ch in row] for row in read_lines(path)]


def get_neighbours(matrix: list[list], x: int, y: int, diagonal: bool) -> list[tuple[int, int]]:
    possible_neighbours = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    if diagonal:
        possible_neighbours += [(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
    return [(nx, ny) for nx, ny in possible_neighbours if 0 <= ny < len(matrix) if 0 <= nx < len(matrix[ny])]
