from operator import itemgetter

PAPER = set[tuple[int, int]]


def create_paper(ls: list[str]) -> PAPER:
    return {tuple(int(i) for i in line.split(",")) for line in ls}


def fold_index(index: int, fold_at: int) -> int:
    if index < fold_at:
        return index
    elif index > fold_at:
        return 2 * fold_at - index
    else:
        raise f"fold index ({index}) cannot be on the folding line ({fold_at})"


def fold_paper(paper: PAPER, instruction: str) -> PAPER:
    axis, index = instruction.split()[2].split("=")
    index = int(index)
    if axis == "x":
        return {(fold_index(x, index), y) for (x, y) in paper if x != index}
    elif axis == "y":
        return {(x, fold_index(y, index)) for (x, y) in paper if y != index}
    else:
        raise f"unknown axis: {axis}"


def part_one() -> int:
    with open("src/13.test.txt") as file:
        ls = file.read().splitlines()
    paper = create_paper([line for line in ls if "," in line])
    instructions = [line for line in ls if "=" in line]
    return len(fold_paper(paper, instructions[0]))


def part_two() -> str:
    with open("src/13.txt") as file:
        ls = file.read().splitlines()
    paper = create_paper([line for line in ls if "," in line])
    instructions = [line for line in ls if "=" in line]

    for instruction in instructions:
        paper = fold_paper(paper, instruction)

    range_x = range(max(map(itemgetter(0), paper)) + 1)
    range_y = range(max(map(itemgetter(1), paper)) + 1)
    return "\n".join("".join("#" if (x, y) in paper else "." for x in range_x) for y in range_y)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
