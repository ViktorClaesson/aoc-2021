from dataclasses import dataclass, field


@dataclass
class Board:
    board_numbers: list[int]
    board_checked: list[bool] = field(init=False)
    _size: int = 5

    def __post_init__(self):
        self.board_checked = [False] * len(self.board_numbers)

    def _is_row_completed(self, row: int) -> bool:
        return all(b for b in self.board_checked[row * self._size : (row + 1) * self._size])

    def _is_col_completed(self, col: int) -> bool:
        return all(b for idx, b in enumerate(self.board_checked) if idx % self._size == col)

    def unchecked_sum(self) -> int:
        return sum(n for b, n in zip(self.board_checked, self.board_numbers) if not b)

    def has_won(self) -> bool:
        return any(self._is_row_completed(row) for row in range(self._size)) or any(self._is_col_completed(col) for col in range(self._size))

    def check(self, draw):
        self.board_checked = [b or v == draw for b, v in zip(self.board_checked, self.board_numbers)]


def load_boards(lines: list[str]) -> list[Board]:
    boards = []
    while len(lines) >= 5:
        boards.append(Board(board_numbers=[int(n) for line in lines[:5] for n in line.split()]))
        lines = lines[6:]
    return boards


def part_one() -> int:
    with open("src/4.txt") as file:
        lines = file.read().splitlines()
    draws: list[int] = [int(n) for n in lines[0].split(",")]
    boards: list[Board] = load_boards(lines[2:])

    for draw in draws:
        for board in boards:
            board.check(draw)
        if rets := [draw * board.unchecked_sum() for board in boards if board.has_won()]:
            return rets[0]
    return 0


def part_two() -> int:
    with open("src/4.txt") as file:
        lines = file.read().splitlines()
    draws: list[int] = [int(n) for n in lines[0].split(",")]
    boards: list[Board] = load_boards(lines[2:])

    for draw in draws:
        boards = [board for board in boards if not board.has_won()]
        for board in boards:
            board.check(draw)
        if len(boards) == 1 and boards[0].has_won():
            return draw * boards[0].unchecked_sum()
    return 0


if __name__ == "__main__":
    print(part_one())
    print(part_two())
